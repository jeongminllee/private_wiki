---
type: Study Note
title: Mistral 공식 FP8 체크포인트의 로컬 BF16 변환 이해
description: Mistral Small 4 119B 공식 FP8 weight를 scale로 역변환해 학습용 BF16 safetensors로 저장하는 과정의 수학, 파일 구조, 한계와 실무 검증 절차
tags: [mistral, fp8, bf16, quantization, safetensors, fine-tuning]
timestamp: 2026-08-11
status: active
---

# 한 줄 결론

이번 작업은 원래 BF16 weight를 무손실로 복구한 것이 아니다. 공식 checkpoint에 저장된
FP8 근사값과 inverse scale을 이용해 같은 근사값을 BF16 tensor로 **펼쳐 저장**한
것이다. 그 결과 일반적인 Transformers·Axolotl BF16 학습 경로에서 다루기 쉬워지지만,
FP8 양자화 때 사라진 정밀도는 되살아나지 않는다.

# 현재 실험 상태

- 원본: `model/mistral-small-4-119b-2603`
- 출력: `model/mistral-small-4-119b-2603-bf16-local`
- 변환 방식: Mistral이 공개한 FP8 descale 식
- 관찰: 최종 BF16 경로에 shard와 metadata 파일이 생성됨
- 해석: 변환기는 임시 `.incomplete`를 내부 검증 후에만 최종 경로로 rename하므로,
  최종 경로의 존재는 내부 변환·저장 검사가 끝났다는 강한 증거다.
- 독립 구조 검사: `PASS` (2026-08-11)
- TorchVision runtime 검사: `PASS` (2026-08-11)
- tokenizer·processor·chat template 검사: `PASS` (2026-08-11)
- dataset tokenizer 전수 preflight: `PASS` (2026-08-18)
- 남은 확인: 전체 파일 SHA-256 inventory, 실제 model load canary

## 독립 구조 검사 실측값

| 항목 | 결과 |
| --- | ---: |
| source revision | `a11f36bebf709121056b1dbcc943d1c6afbe494d` |
| index tensor | 765 |
| 실제 tensor | 765 |
| shard | 35 |
| 저장 byte | 238,802,597,888 |
| dtype | BF16 765개 |
| FP8 잔여 | 0 |
| scale tensor 잔여 | 0 |
| 누락 shard | 0 |
| descale 변환 tensor | 360 |

index와 실제 key 집합이 같고 모든 tensor가 BF16이므로 checkpoint 구조 gate는
통과했다. 다만 이 결과만으로 tokenizer 계약, model load와 학습 가능성을 최종
판정하지 않는다.

## PixtralProcessor와 TorchVision 의존성

첫 `AutoProcessor` 검사에서는 `PixtralProcessor requires the Torchvision library`
오류가 발생했다. Mistral Small 4는 text-only 데이터로 학습하더라도 architecture와
processor가 vision 입력 경로를 포함하는 multimodal 모델이다. `AutoProcessor`는 image
전처리 component까지 구성하므로 import 시점에 TorchVision이 필요하다.

공식 호환 조합인 `torch==2.12.1+cu130`과 `torchvision==0.27.1+cu130`을 같은
PyTorch CUDA 13.0 index에서 설치했다. 검사 결과 CUDA 사용 가능, B200 2장 인식과
두 package pin이 모두 통과했다. 이는 단순한 선택적 이미지 도구 설치가 아니라
processor 전체를 재현하는 runtime dependency 보완이다.

## Processor와 chat template 실측값

| 항목 | 결과 |
| --- | --- |
| config | `Mistral3Config`, model type `mistral3` |
| config dtype | `torch.bfloat16` |
| quantization config | 없음 |
| processor | `PixtralProcessor` |
| tokenizer backend | `TokenizersBackend` |
| vocabulary | 131,072 |
| BOS / EOS / PAD | `<s>` / `</s>` / `<pad>` |
| smoke prompt token | 30 |
| `[THINK]`·`[/THINK]` | 0 |

`reasoning_effort="none"` smoke prompt는 다음 구조로 렌더링됐다.

```text
<s>
[SYSTEM_PROMPT]...[/SYSTEM_PROMPT]
[MODEL_SETTINGS]{"reasoning_effort": "none"}[/MODEL_SETTINGS]
[INST]...[/INST]
```

`<s>`는 sequence 시작, `SYSTEM_PROMPT`는 고정 지침, `MODEL_SETTINGS`는 요청별
reasoning mode, `INST`는 사용자 지시 경계를 나타낸다. 이 모델은 generation prompt
뒤에 별도의 일반적인 `assistant` 문자열을 붙이지 않아도 `[/INST]` 다음 위치를 model
응답 시작점으로 해석한다. 다음 dataset 검사는 완성된 assistant message를 넣었을 때
이 prompt prefix 뒤에 target과 EOS가 일관되게 이어지는지 확인한다.

## Dataset sample template gate

train과 validation 첫 행에 실제 local tokenizer를 적용한 3-A 검사가 PASS했다.

| split | prompt token | assistant target token | 전체 token | THINK | EOS |
| --- | ---: | ---: | ---: | ---: | --- |
| train | 318 | 10 | 328 | 0 | true |
| validation | 380 | 10 | 390 | 0 | true |

두 sample 모두 `system → user → assistant` 순서, prompt prefix와 assistant target의
token 경계, rendered assistant content, 2,048-token 제한과 EOS 종료가 일치했다.
이는 sample-level template 호환성 증거이며, 전체 11,000건과 Axolotl label masking의
최종 증거는 아니다.

동결된 assistant target은 정확히 `{"assessment": value}` 한 필드 JSON이고 value는
`present`, `not_observed`, `uncertain` 중 하나다. 전체 preflight는 train 10,000건과
validation 1,000건 모두에 이 계약과 system prompt SHA-256 `9a72abf0…52ef`를
적용해야 한다.

## Dataset 전수 tokenizer gate

2026-08-18에 실제 local Mistral tokenizer로 11,000건 전수를 검사해 3-B gate가
PASS했다.

| 항목 | train | validation |
| --- | ---: | ---: |
| row | 10,000 | 1,000 |
| `present` | 5,000 | 500 |
| `not_observed` | 5,000 | 500 |
| token min / p50 / p95 / p99 / max | 254 / 381 / 830 / 927 / 1,505 | 254 / 382 / 759 / 920 / 1,497 |
| assistant target token min / max | 7 / 10 | 7 / 10 |
| 2,048 token 초과 | 0 | 0 |
| THINK marker | 0 | 0 |

전체 고유 record ID는 11,000개이며 dataset·manifest·system prompt SHA-256도 동결값과
일치했다. 첫 실행에서 `train:1: empty target`이 발생했지만 데이터 문제가 아니라
Transformers 5.x 반환 객체의 `.input_ids`를 꺼내지 않은 검사 코드 문제였다. 해결
과정은 [Mistral 전수 Preflight의 잘못된 Empty Target 판정](../../../errors/mistral-preflight-empty-target-batchencoding.md)에 기록했다.

# 1. 원본 FP8 checkpoint에는 무엇이 있었나

공식 Hugging Face checkpoint는 대략 다음 두 종류의 tensor를 함께 저장한다.

1. FP8로 표현된 weight tensor
2. weight를 원래 값의 범위로 되돌리는 `*_scale_inv` tensor

일부 runtime을 위한 activation scale도 들어 있다. activation scale은 추론 runtime이
중간 activation을 저정밀도로 처리할 때 사용하는 보조 정보다. BF16 학습에서는 매
forward pass마다 activation을 새로 계산하므로, plain BF16 checkpoint에는 이를 남기지
않는다.

공식 설정의 `dtype: bfloat16`은 모델이 지향하는 계산 dtype을 나타낼 수 있지만,
실제 shard 저장 dtype까지 BF16이라는 뜻은 아니다. 이 모델의 `quantization_config`와
`params.json`은 weight가 FP8 E4M3 형식임을 별도로 선언한다. dtype 판단은 config 한
필드가 아니라 safetensors header와 quantization metadata를 함께 봐야 한다.

# 2. 변환에서 실제로 한 계산

weight마다 저장된 FP8 값 `q`와 inverse scale `s_inv`가 있다고 하자. 변환기는 다음을
계산한다.

```text
W_hat = BF16(q) × BF16(s_inv)
```

여기서 `W_hat`은 원래 weight `W`의 정확한 복원값이 아니라 FP8로 양자화된 값을
scale로 원래 수치 범위에 되돌린 근사값이다.

```text
원래 BF16/FP32 weight W
        │ quantize·round·clip
        ▼
FP8 값 q + inverse scale s_inv
        │ descale 후 BF16에 저장
        ▼
BF16 근사값 W_hat
```

양자화 과정에서 여러 실수가 같은 FP8 값으로 반올림될 수 있다. 따라서 일반적으로
`W != W_hat`이며, BF16으로 dtype을 넓혀도 이미 발생한 rounding·clipping error는
없어지지 않는다. BF16 변환의 목적은 품질을 원상복구하는 것이 아니라 **runtime
호환성과 학습 가능성**을 얻는 것이다.

# 3. FP8과 BF16의 학술적 차이

| 형식 | 총 bit | 대표 구성 | 장점 | 약점 |
| --- | ---: | --- | --- | --- |
| FP8 E4M3 | 8 | sign 1, exponent 4, mantissa 3 | 저장 공간과 연산량 감소 | 표현 정밀도와 범위가 작아 scale 관리 필요 |
| BF16 | 16 | sign 1, exponent 8, mantissa 7 | FP32와 같은 exponent 폭, 학습 시 넓은 동적 범위 | FP32보다 mantissa 정밀도가 낮고 FP8보다 메모리가 큼 |

E4M3는 E5M2보다 mantissa가 한 bit 많아 상대적으로 정밀도에 유리하고 exponent가
작아 범위는 좁다. 그래서 tensor별 또는 block별 scale이 중요하다. BF16은 FP32와
같은 8-bit exponent를 가지므로 gradient와 activation의 넓은 범위를 다루기 편하지만,
7-bit mantissa 때문에 모든 실수를 정확하게 표현하지는 못한다.

# 4. BF16 폴더의 파일 구조

실제 파일 수와 shard 수는 `model.safetensors.index.json`을 기준으로 확인한다.

| 파일 | 역할 | Git 포함 여부 |
| --- | --- | --- |
| `model-xxxxx-of-yyyyy.safetensors` | BF16 weight shard | 금지 |
| `model.safetensors.index.json` | tensor 이름을 shard 파일에 연결하는 지도 | 보통 모델과 함께 보존 |
| `config.json` | 모델 architecture와 dtype 설정 | 보존 |
| `tokenizer.json`, `tokenizer_config.json` | text를 token ID로 변환하는 규칙 | 보존 |
| `chat_template.jinja` 또는 관련 template | messages를 실제 prompt 문자열로 직렬화 | 보존 |
| processor 관련 JSON | multimodal 입력 전처리 설정 | 보존 |
| `params.json` | Mistral 계열의 별도 architecture metadata | 보존하되 FP8 quantization 선언 제거 확인 |
| `conversion_manifest.json` | source revision, 변환식, tensor·shard 수와 저장 크기 | 반드시 보존 |
| `README.md`, license 관련 파일 | 사용법과 배포 조건 | 보존 |

## 왜 weight 파일이 여러 개인가

119B 모델을 파일 하나로 저장하면 복사·업로드·재시도와 병렬 I/O가 불편하다.
`safetensors` shard는 거대한 state dict를 여러 파일로 나누고, index가 각 tensor의
위치를 알려준다. shard는 모델 분할 방식일 뿐 GPU 수나 FSDP shard와 같은 개념은
아니다.

- checkpoint shard: 디스크 파일을 나누는 방식
- FSDP shard: 실행 중 parameter·gradient·optimizer state를 rank 사이에 나누는 방식
- tensor parallel: 행렬 계산 자체를 여러 GPU에 나누는 방식

세 가지를 혼동하지 않는다.

# 5. 변환기가 수행한 안전 검사

현재 변환기는 다음 조건을 확인한 뒤에만 `.incomplete`를 최종 BF16 경로로 rename한다.

1. source index에 적힌 모든 shard가 존재한다.
2. shard의 tensor key 집합과 source index가 정확히 일치한다.
3. FP8 tensor가 실제로 존재한다.
4. 모든 inverse scale이 대응 weight 변환에 사용된다.
5. 출력에 FP8 tensor와 scale tensor가 남지 않는다.
6. `config.json`과 nested `text_config`에서 `quantization_config`를 제거한다.
7. 새 BF16 shard와 `model.safetensors.index.json`을 생성한다.
8. source repository와 revision, 변환 통계를 manifest에 기록한다.

이 검사는 파일 구조와 dtype 변환의 정합성을 판정한다. 모델이 실제로 forward와
backward를 수행하고 좋은 결과를 내는지는 아직 판정하지 않는다.

# 6. 실무 검증 명령

프로젝트 root에서 실행한다.

```bash
BF16_MODEL="model/mistral-small-4-119b-2603-bf16-local"

du -sh "$BF16_MODEL"
find "$BF16_MODEL" -maxdepth 1 -type f -printf '%f\n' | sort
python -m json.tool "$BF16_MODEL/conversion_manifest.json" | less
```

index와 config의 핵심값을 읽는다.

```bash
uv run --no-sync python - <<'PY'
import json
from pathlib import Path

root = Path("model/mistral-small-4-119b-2603-bf16-local")
config = json.loads((root / "config.json").read_text())
index = json.loads((root / "model.safetensors.index.json").read_text())
manifest = json.loads((root / "conversion_manifest.json").read_text())

print("dtype:", config.get("dtype"))
print("quantization_config:", config.get("quantization_config"))
print("tensor_count:", len(index["weight_map"]))
print("shard_count:", len(set(index["weight_map"].values())))
print("stored_bytes:", index["metadata"]["total_size"])
print("source_revision:", manifest["source_revision"])
print("converted_tensor_count:", manifest["converted_tensor_count"])
PY
```

최소 기대 조건:

- `dtype == bfloat16`
- `quantization_config == None`
- manifest revision이 `.env`에 승인한 40자리 SHA와 일치
- index의 모든 shard 파일이 존재
- 변환기 출력이 `BF16 conversion PASS`로 끝남

## SHA-256 inventory

전체 shard hash는 약 240GB를 다시 읽으므로 시간이 걸리지만, 장기 재현성과 bit rot
검출을 위해 권장한다.

```bash
cd model/mistral-small-4-119b-2603-bf16-local
sha256sum \
  config.json \
  model.safetensors.index.json \
  conversion_manifest.json \
  model-*.safetensors \
  > SHA256SUMS
sha256sum --check SHA256SUMS
```

`SHA256SUMS`에는 token이나 비밀 경로를 넣지 않는다.

# 7. 학습 관점에서 얻은 것과 얻지 못한 것

## 얻은 것

- Transformers/Axolotl이 일반 BF16 weight로 읽을 수 있는 checkpoint 형식
- FP8 runtime-specific scale key가 없는 단순한 state dict
- BF16 LoRA + FSDP2 실험의 base model 후보
- 필요하면 QLoRA loader가 다시 4-bit로 양자화할 수 있는 입력 checkpoint
- source revision과 변환 방법을 추적할 수 있는 provenance

## 아직 얻지 못한 것

- 양자화 전 원본 BF16과의 완전한 수치 동일성
- 모델 load, forward, backward와 adapter save 성공
- GPU당 peak VRAM gate 통과
- finite loss와 학습 안정성
- 데이터·chat template 계약 통과
- 모델 품질 향상

특히 QLoRA는 이 BF16 근사 checkpoint를 다시 4-bit로 양자화해 base weight를 고정한다.
이는 `FP8 → 원본 BF16 복원 → 4-bit`가 아니라 `FP8 근사값 → BF16 container → 4-bit
근사값`의 흐름이다. 따라서 QLoRA와 BF16 LoRA의 품질·VRAM·저장 성공 여부는 실제
G1 canary로 비교해야 한다.

# 8. 다음 gate

```text
BF16 파일 구조 PASS
  → config·index·manifest 독립 검사
  → tokenizer·processor local load
  → dataset 전체 tokenizer preflight
  → BF16 model load-only canary
  → QLoRA/DDP 1-step
  → BF16 LoRA/FSDP2 1-step
  → VRAM·finite loss·adapter inventory 비교
```

최종 BF16 폴더가 생성된 현재 시점은 첫 번째 gate를 통과한 상태에 가깝다. 다음
단계는 장시간 학습이 아니라 metadata와 tokenizer를 읽는 저위험 검사다.

# Related Concepts

- [Mistral FP8 to BF16 변환 스크립트 오타와 사후 실패 위험](../../../errors/mistral-fp8-bf16-converter-script-typos.md)
- [Mistral PixtralProcessor TorchVision 누락](../../../errors/mistral-pixtralprocessor-torchvision-missing.md)
- [B200 Persistent Root 하위 Symlink 일괄 Broken 진단](../../../errors/b200-persistent-root-symlinks-broken-20260812.md)
- [Mistral F5-X 첫 파인튜닝 실습 워크북](../training/mistral_f5x_first_finetuning_workbook_20260809.md)
- [Transformers SFT Basics](transformers_sft_basics.md)
- [LoRA and PEFT Basics](lora_peft_basics.md)
- [Distributed Training Basics](distributed_training_basics.md)
- [AegisLM Training Libraries](../libraries/aegislm_training_libraries.md)

# Citations

- [Mistral Small 4 119B 공식 모델](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603)
- [Mistral 공식 FP8 descale 예제](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/blob/3b76d234c932e78dc989731bfc4c3b12c0a87918/README.md)
- [Hugging Face safetensors state-dict serialization](https://huggingface.co/docs/huggingface_hub/main/package_reference/serialization)
- [FP8 Formats for Deep Learning](https://arxiv.org/abs/2209.05433)
- [A Study of BFLOAT16 for Deep Learning Training](https://arxiv.org/abs/1905.12322)
- [PyTorch tensor dtype attributes](https://docs.pytorch.org/docs/stable/tensor_attributes.html)
