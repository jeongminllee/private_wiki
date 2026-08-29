---
type: Error Note
title: Mistral Small 4 B200 vLLM 0.26 서빙 트러블슈팅
description: Mistral Small 4 119B를 B200 2장과 vLLM 0.26으로 기동하면서 확인한 checkpoint format, attention backend, 누락 shard, cache, IPC path와 CuTeDSL 문제의 진단 기록
tags: [error, mistral, vllm, b200, cuda, triton, cutedsl]
timestamp: 2026-08-20
status: active
---

# Situation

BF16 LoRA + FSDP2로 학습한 Mistral Small 4 119B G3 adapter는 새 process
reload·단일 inference와 blind decision 500건 평가를 통과했다. 다음 lifecycle gate로
vLLM 0.26.0에서 base model을 B200 두 장에 TP2로 기동하고, 그 위에 LoRA adapter를
연결하려 했다.

학습 환경은 PyTorch 2.12.1+cu130과 Axolotl 0.17.0을 사용한다. vLLM 0.26.0은 다른
PyTorch pin을 요구했으므로 학습 환경을 변경하지 않고 별도 serving project와 virtual
environment를 사용했다. 두 환경은 model artifact와 API contract만 공유한다.

# Current Status

| Gate | Status | 확인된 범위 |
| --- | --- | --- |
| 공식 Mistral native config 읽기 | PASS | `params.json`, Mistral tokenizer mode |
| 공식 native FP8 weight 읽기 | PASS | `consolidated-*` 7개 shard |
| B200 2장 TP2 배치 | PASS | GPU당 약 62,276 MiB 적재 관측 |
| engine/API server startup | PASS | `Application startup complete` |
| `/v1/completions` transport·decode | PASS | HTTP 응답, model routing, prompt 8 token과 decode 1 token 확인 |
| `/v1/chat/completions` text generation | PASS | chat template 적용 뒤 정확히 `OK` 생성 |
| G3 LoRA를 vLLM에 attach | BLOCK | HF/Axolotl의 분리된 `q_a_proj`·`kv_a_proj_with_mqa`와 vLLM native의 `fused_qkv_a_proj` 모듈 ABI 불일치 |
| vision request | PENDING/BLOCKED | CuTeDSL warmup 우회는 text-only 범위 |

따라서 현재 판정은 **official native FP8 base의 text-serving startup과 API transport
및 non-empty Chat Completions PASS**, **G3 LoRA native attach BLOCK**이다. vision은 계속
별도 PENDING/BLOCKED gate다.

## G3 LoRA Attach Attempt

2026-08-25 static LoRA 등록으로 base와 G3 adapter를 함께 기동했다. 두 B200의 TP2,
FP8 autotuning, CUDA graph profiling과 KV cache 생성은 정상적으로 끝났으며 GPU당 사용
가능 KV cache는 약 81.98 GiB였다. 실패 위치는 engine 준비 뒤
`init_static_loras → add_lora → check_unexpected_modules`였다.

핵심 오류는 다음 모듈 불일치다.

```text
adapter received:
  self_attn.q_a_proj
  self_attn.kv_a_proj_with_mqa

vLLM native model expected:
  fused_qkv_a_proj
```

G3 safetensors에는 총 720개 LoRA tensor가 있고 36개 layer 각각에 A/B tensor가
저장돼 있다. 즉 `q_a_proj` 72개와 `kv_a_proj_with_mqa` 72개, 합계 144개 tensor가
native executor의 fused target과 맞지 않아 거부됐다. adapter key의 긴
`language_model.model.layers.*` prefix 자체가 원인은 아니다. 같은 prefix를 쓰는
`q_b_proj`, `kv_b_proj`, `o_proj`와 shared expert target은 unexpected 목록에 없었다.

이는 training artifact 손상이나 rank·dtype·VRAM 문제가 아니다. Axolotl/Transformers
학습 graph는 두 projection을 별도 module로 노출하지만 vLLM native Mistral executor는
kernel 실행을 위해 하나의 `fused_qkv_a_proj`로 pack한다. 따라서 현재 adapter를 단순히
rename해서는 안 된다. 두 rank-16 delta를 정확히 합치려면 일반적으로 fused output에
대한 block 구성과 최대 rank 32가 필요하며, 새 artifact hash와 수치 동등성 검증이
필수다.

종료 시 보인 leaked semaphore/shared-memory warning은 worker 실패 뒤 cleanup 부산물이며
root cause가 아니다. MoE default config warning도 성능 경고일 뿐 attach 실패 원인이
아니다.

## API Smoke Attempt 1

2026-08-20 raw Completions API는 `text_completion` JSON을 정상 반환했다. served model은
`mistral-native-base-smoke`, system fingerprint는 vLLM 0.26.0 TP2를 가리켰고 usage는
prompt 8 token, completion 1 token이었다.

그러나 `choices[0].text`가 빈 문자열이고 `finish_reason`은 `stop`이었다. 이는 engine이
요청을 받아 tokenization과 decode를 수행한 뒤 첫 생성에서 EOS 또는 출력되지 않는 control
token을 선택한 상태와 일치한다. 따라서 다음처럼 판정한다.

- server process·HTTP endpoint·model routing: PASS
- tokenizer와 한 token decode: PASS
- 사용자에게 보이는 non-empty generation: PENDING

raw `/v1/completions`는 instruction model의 chat template를 자동으로 구성하지 않는다.
다음 검사는 `/v1/chat/completions`에 `system → user` messages와
`reasoning_effort: none`을 전달해 학습 때와 같은 대화 경계를 사용한다.

## API Smoke Attempt 2

같은 server에 Chat Completions 요청을 보내자 다음 증거가 확인됐다.

```text
object: chat.completion
model: mistral-native-base-smoke
assistant content: OK
finish_reason: stop
prompt/completion/total tokens: 28/2/30
system_fingerprint: vllm-0.26.0-tp2-6fa9d26e
```

`system → user` message를 native chat template로 28 token에 렌더링했고, 사용자에게 보이는
`OK`와 종료 token을 생성해 completion 2 token으로 정상 종료했다. 따라서 base model의
server startup, OpenAI-compatible Chat Completions, template, TP2 decode와 non-empty
text generation을 모두 PASS로 닫는다.

# Failure Chain

| 순서 | 관측된 오류 | 원인 판정 | 조치 | 결과 |
| ---: | --- | --- | --- | --- |
| 1 | `No model architectures are specified` | local HF BF16 config의 nested text architecture를 vLLM loader가 확정하지 못함 | official native Mistral format으로 진단 경로 변경 | 다음 단계 진입 |
| 2 | forced `FLASH_ATTN_MLA` backend 거부 | 공식 예시의 backend가 현재 B200·vLLM build에서 유효하지 않음 | backend 강제를 제거하고 auto selection 사용 | weight load 진입 |
| 3 | index가 가리키는 `consolidated-*` 7개 누락 | native index만 있고 실제 shard가 없는 불완전 local snapshot | 같은 immutable revision에서 누락 shard 다운로드 후 전수 확인 | native weight load PASS |
| 4 | shared-memory broadcast block 60초 대기 | worker가 compile/warmup 중이라 engine core가 기다림 | GPU·process와 뒤따르는 최초 오류를 계속 관찰 | 원인 자체가 아니라 대기 증상으로 분류 |
| 5 | Triton `.so`의 `failed to map segment` | `/tmp` executable mmap 제한으로 추정 | TorchInductor·Triton·CUDA cache를 실행 가능한 persistent 경로로 이동 | 해당 오류 해소 |
| 6 | ZMQ `ipc path ... longer than 107 characters` | 긴 project `TMPDIR`이 Unix socket path 한계를 초과 | `TMPDIR/TMP/TEMP`만 짧은 사용자 경로로 분리 | IPC bind PASS |
| 7 | CuTeDSL `TYPE_UNSTABLE_JOIN` | B200 SM100 FA4 split-KV warmup과 CUTLASS DSL 4.6.0의 알려진 조합 문제 | text-only에서 CuTeDSL warmup 비활성화 | API server startup PASS |

2026-08-25 B200의 `scripts/check_serving.sh`가 이 성공 옵션을 포함하지 않은 구버전으로
남아 있어 같은 7번 오류가 재발했다. GitHub 보존본과 비교해
`--kernel-config '{"enable_cutedsl_warmup": false}'`, executable cache 분리와 짧은
IPC temp가 빠진 것을 확인했다. 기존 script를 artifact에 백업하고 검증본 하나만
역동기화했으며, script SHA-256과 `bash -n`을 재검증했다.

# Cause and Solution Details

## 1. HF BF16 format과 Mistral native format은 별개다

공식 repository에는 두 계열의 weight 표현이 함께 있다.

```text
Hugging Face format
├─ config.json
├─ model.safetensors.index.json
└─ model-*.safetensors

Mistral native format
├─ params.json
├─ consolidated.safetensors.index.json
├─ consolidated-*.safetensors
└─ tekken.json
```

직접 만든 `*-bf16-local`은 공식 FP8 tensor를 BF16 값으로 복원해 Hugging Face
`model-*` shard로 저장한 checkpoint다. 이 폴더에 native `consolidated-*`가 없는 것은
변환 실패가 아니다.

여기서 두 축을 구분해야 한다.

- FP8/BF16: tensor의 **dtype과 수치 표현**
- `model-*`/`consolidated-*`: checkpoint의 **파일 format과 loader contract**

공식 native FP8 shard를 BF16 local 폴더에 복사하면 하나의 일관된 BF16 checkpoint가
되는 것이 아니다. 서로 다른 index와 dtype의 weight tree를 섞는 결과이므로 금지한다.

초기 HF BF16 기동의 `No model architectures are specified`는 checkpoint tensor가
손상됐다는 뜻이 아니라, 현재 vLLM loader가 multimodal top-level config와 nested text
config 사이에서 실행 architecture를 확정하지 못한 config compatibility 문제로
분리했다. base engine 자체를 먼저 검증하기 위해 공식 native format을 사용했다.

## 2. 공식 serving 예시의 attention backend는 환경별로 재검증한다

모델 카드의 예시는 `--attention-backend FLASH_ATTN_MLA`를 지정한다. 하지만 이번
B200·vLLM 0.26.0 build에서는 해당 backend가 현재 compute capability에 유효하지 않다는
오류가 발생했다.

모델 카드 명령은 출발점이지 모든 wheel·GPU 조합의 immutable 설정이 아니다. backend
강제를 제거한 뒤 vLLM auto selection이 지원 경로를 선택하게 하자 다음 단계로
진행했다. 여기서 B200이나 CUDA 13.0 전체가 지원되지 않는다고 결론 내리면 안 된다.

## 3. index 파일의 존재는 shard 완전성을 보장하지 않는다

native loader는 `consolidated.safetensors.index.json`을 읽은 다음, index가 참조한 7개
실제 shard를 요구했다. local directory에는 index가 있었지만 shard가 없어 다음 오류가
발생했다.

```text
FileNotFoundError: Weight files referenced in index but missing:
consolidated-00001-of-00007.safetensors ... consolidated-00007-of-00007.safetensors
```

왜 최초 download에서 이 파일들이 빠졌는지는 당시 로그만으로 확정하지 못했다.
selective download 또는 중단된 snapshot 가능성은 있으나 **추측**이다. 해결은 같은
immutable revision에서 `consolidated-*`를 내려받고 다음 세 항목을 함께 확인하는 것이다.

1. index의 weight map이 참조하는 고유 shard 수
2. 실제 directory의 shard 수
3. missing set이 0인지 여부

## 4. shared-memory 경고는 결과가 아니라 대기 상태다

```text
No available shared memory broadcast block found in 60 seconds.
```

이 메시지는 engine core가 worker의 shared-memory broadcast block을 오래 기다렸다는
뜻이다. 대형 model load, graph capture, kernel compilation 중 일시적으로 나타날 수 있다.
그 자체만으로 성공이나 deadlock을 판정하지 않는다.

- GPU memory가 변하고 compile progress가 이어지면 더 관찰한다.
- 같은 메시지만 반복되고 GPU·process가 정지하면 hang을 의심한다.
- 이후 Python/CUDA/Triton traceback이 나오면 그 **최초 오류**를 root cause로 본다.

이번에는 뒤이어 Triton shared object mmap 오류가 나왔으므로 shared-memory 메시지는
원인이 아니라 선행 증상이었다.

## 5. compilation cache와 IPC temp는 경로 요구가 다르다

Triton/TorchInductor가 `/tmp` 아래에서 만든 `.so`를 load할 때 다음 오류가 발생했다.

```text
ImportError: .../__triton_launcher...so: failed to map segment from shared object
```

실행 가능한 filesystem으로 cache를 옮긴 뒤 이 오류가 사라졌으므로 `/tmp`의 `noexec`
또는 executable mmap 정책 문제라는 진단을 강하게 지지한다. 다만 mount option을 기록한
출력이 없으므로 문서에서는 **고신뢰 추론**으로 남긴다.

처음에는 `TMPDIR`까지 긴 project cache 하위로 옮겼고, 이번에는 ZMQ가 그 경로에 IPC
socket 이름을 덧붙이면서 Linux Unix-domain socket path limit을 넘었다.

```text
zmq.error.ZMQError: ipc path "..." is longer than 107 characters
```

해결 원칙은 다음처럼 cache와 IPC temp를 분리하는 것이다.

```bash
export AEGISLM_MISTRAL_ROOT="<PROJECT_ROOT>"

# 생성된 .so를 다시 실행해야 하는 compilation cache
export TORCHINDUCTOR_CACHE_DIR="${AEGISLM_MISTRAL_ROOT}/serving/vllm/.runtime-cache/torchinductor"
export TRITON_CACHE_DIR="${AEGISLM_MISTRAL_ROOT}/serving/vllm/.runtime-cache/triton"
export CUDA_CACHE_PATH="${AEGISLM_MISTRAL_ROOT}/serving/vllm/.runtime-cache/cuda"

# Unix socket 이름이 뒤에 붙으므로 짧아야 하는 IPC temp
export TMPDIR="${HOME}/.vllm-tmp"
export TMP="${TMPDIR}"
export TEMP="${TMPDIR}"
```

`<PROJECT_ROOT>`는 실제 private server path를 wiki에 기록하지 않기 위한 placeholder다.

## 6. B200 CuTeDSL warmup 오류는 upstream 조합 문제와 일치한다

마지막 startup failure는 다음 형태였다.

```text
error[TYPE_UNSTABLE_JOIN]: n_block_first has type None on one path and Int32 on another
vllm_flash_attn/cute/flash_fwd_sm100.py:1484
```

이는 vLLM issue #51286의 B200/B300 SM100-family FA4 split-KV compile failure와
일치한다. issue의 재현 결과에서는 `nvidia-cutlass-dsl` 4.6.0·4.6.1이 실패하고
4.6.2 이상이 통과했다. vLLM PR #51566은 CUTLASS DSL을 4.6.2, 함께 묶인
`quack-kernels`를 0.6.4로 올리는 변경을 main에 병합했다.

현재 environment의 dependency pin을 즉석에서 깨지 않고, 우선 text-only base startup을
검증하기 위해 다음 workaround를 사용했다.

```text
--kernel-config '{"enable_cutedsl_warmup": false}'
```

이 옵션으로 `Application startup complete`까지 도달했다. 하지만 이것은 vision path의
근본 수정이 아니다. upstream issue에 따르면 긴 image sequence가 lazy compile을
촉발하면 같은 경로가 다시 실패할 수 있다. multimodal serving은 호환 pin을 별도
Work Order로 검증해야 한다.

# Known-Good Startup Skeleton

다음은 성공 조건을 보존한 **명령 골격**이다. model path와 service name은 실제 local
환경에 맞춰 넣고, 실행 전 native shard 전수 검사를 통과해야 한다.

```bash
vllm serve "${MISTRAL_NATIVE_MODEL_ROOT}" \
  --served-model-name mistral-small-4-119b \
  --tensor-parallel-size 2 \
  --config-format mistral \
  --load-format mistral \
  --tokenizer-mode mistral \
  --kernel-config '{"enable_cutedsl_warmup": false}'
```

공식 예제의 tool/reasoning parser, context length, batch token, concurrency와 GPU memory
비율은 base API smoke가 끝난 뒤 하나씩 추가한다. 첫 기동부터 모든 performance option을
동시에 넣으면 architecture, weight, kernel과 memory 문제를 분리하기 어렵다.

# LoRA Boundary

G3 LoRA artifact는 full model이 아니라 base weight에 더하는 adapter delta다. 따라서
다음 관계가 성립한다.

```text
공식 native FP8 base startup PASS
    != local BF16 base + G3 LoRA의 vLLM serving PASS
```

G3 adapter는 local BF16 base와 PEFT에서 reload·inference 및 blind 500 평가를 이미
통과했다. 그러나 vLLM 0.26의 dynamic LoRA loader가 이 Mistral MoE adapter의 standard
module target과 expert `target_parameters`를 모두 지원하는지는 별도 문제다. 지금까지의
vLLM 오류는 adapter attach 전에 발생했으므로 LoRA 자체가 원인은 아니었다.

또한 adapter가 학습한 base는 local BF16 복원본이다. 공식 native FP8 base에 같은
adapter를 붙이는 것은 수치적으로 동일한 base라는 보장이 없으므로, 단순히 load된다는
이유만으로 품질을 승인하지 않는다. serving 후보는 base revision·format·dtype과 adapter
provenance를 함께 고정하고 기존 contract로 다시 평가한다.

# Prevention

- training과 serving resolver가 다른 PyTorch를 요구하면 environment를 분리하고 두 lock을
  각각 보존한다.
- model directory를 dtype만으로 부르지 않고 `HF BF16`, `native FP8`처럼 format도 함께
  기록한다.
- index·shard count·missing set·hash를 startup 전에 검사한다.
- model card의 backend flag는 GPU compute capability와 설치된 wheel에서 다시 검증한다.
- `ChildFailedError`나 engine-core summary보다 각 worker의 최초 traceback을 먼저 찾는다.
- compilation cache는 executable filesystem, IPC temp는 짧은 경로라는 서로 다른 요구를
  반영한다.
- workaround에는 text-only 또는 특정 sequence 범위 같은 적용 한계를 함께 기록한다.
- `Application startup complete` 뒤 `/v1/models`, completion, output schema를 따로 검사한다.
- LoRA attach 후에는 base-only와 adapter-enabled 응답을 구분해 동일한 held-out smoke와
  SHA-256 evidence를 남긴다.

# Next Actions

1. **완료**: base server의 Chat Completions에서 비어 있지 않은 non-reasoning 응답을
   확인한다.
2. request/response와 server log를 secret·private path 없이 evidence로 보존한다.
3. **BLOCK 확인**: vLLM 0.26 native executor가 G3의 split `q_a`·`kv_a` LoRA를
   `fused_qkv_a_proj` target으로 받지 못한다.
4. 빠른 보존 경로는 이미 PASS한 local BF16 base + Transformers/PEFT reload inference를
   유지한다.
5. vLLM이 반드시 필요하면 serving-only adapter pack 변환, split target을 지원하는 별도
   vLLM runtime 또는 새 serving-compatible adapter 학습을 별도 Work Order로 비교한다.
6. 변환·재학습 artifact는 새 hash와 새 held-out 평가 없이 기존 G3 PASS를 상속하지 않는다.
7. vision serving은 CUTLASS DSL/QuACK 호환 pin을 동결한 새 environment에서 별도로 검증한다.

# Related Concepts

- [Mistral 공식 FP8 체크포인트의 로컬 BF16 변환 이해](../projects/Fine_Tuned/fundamentals/mistral_fp8_to_bf16_checkpoint_conversion.md)
- [Mistral Small 4 119B G3 Blind 500 Source Decision PASS](../projects/Fine_Tuned/training/mistral_small_4_119b_g3_blind500_decision_20260820.md)
- [Mistral F5-X 첫 파인튜닝 실습 워크북](../projects/Fine_Tuned/training/mistral_f5x_first_finetuning_workbook_20260809.md)
- [Mistral Fused Expert가 bitsandbytes INT_MAX를 초과해 QLoRA 실패](mistral-fused-expert-bitsandbytes-intmax-qlora.md)
- [Mistral PixtralProcessor TorchVision 누락](mistral-pixtralprocessor-torchvision-missing.md)
- [Mistral 전수 Preflight의 잘못된 Empty Target 판정](mistral-preflight-empty-target-batchencoding.md)
- [LLM 생명주기 환경 설계](../infra/llm-lifecycle-environment-design.md)

# Citations

- [Mistral Small 4 119B 공식 모델 카드와 vLLM 예시](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603)
- [공식 repository의 HF/native 이중 파일 구조](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/tree/main)
- [vLLM issue #51286: SM100 FA4 split-KV CuTeDSL compile failure](https://github.com/vllm-project/vllm/issues/51286)
- [vLLM PR #51566: CUTLASS DSL 4.6.2와 QuACK 0.6.4 pin](https://github.com/vllm-project/vllm/pull/51566)
