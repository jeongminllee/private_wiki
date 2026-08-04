---
type: Concept
title: "GLM 모델 로컬 서빙"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-06-30)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-06-30
status: active
---

# GLM 모델 로컬 서빙

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-30

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
로컬 환경에서 glm 이라는 모델을 돌려보고싶어. 지금 현재 b200 5장을 이용할 수 있는 환경이고 최대한 많이 써보면서 감각을 끌어올리고싶어 왜냐하면 곧 5장 반납해야되거든. 그리ㅗㄱ 이후에는 4장으로 써야될수도 있어서 그래. 
서빙 프레임워크는 vllm 쓸 예정인데 로컬 환경에 모델을 두고 필요할때마다 꺼내쓰려고 해. 그리고 마지막으로 파인튜닝할꺼야. 4장인 환경에서 가능할까?

### 💡 답변 (Assistant)
좋아요. 이건 “돌릴 수 있나?”보다 **어떤 GLM 계열을, vLLM에서 어떤 병렬 전략으로, 5장/4장 각각 어디까지 실험할지**가 핵심입니다. 최신 모델 스펙과 vLLM 지원 상태를 확인해서 기준선을 잡아보겠습니다.

---

### 💡 답변 (Assistant)
확인해보니 “GLM”도 세대별로 판단이 완전히 다릅니다. 지금은 **GLM-4.5/Air는 4장 실험에 매우 적합**, **GLM-5.2는 8장 기준 모델이라 5장/4장에서는 까다롭거나 비추천** 쪽으로 정리됩니다.

---

### 💡 답변 (Assistant)
결론부터 말하면 **4×B200 환경에서도 충분히 가능합니다.** 다만 대상 모델을 잘 골라야 합니다.

제가 추천하는 현실적인 기준은 이겁니다.

| 목적 | 추천 모델 | 4×B200 가능성 | 판단 |
|---|---:|---:|---|
| vLLM 로컬 서빙 감각 익히기 | **GLM-4.5-Air-FP8** | 매우 가능 | 가장 추천 |
| 고성능 서빙 실험 | **GLM-4.5-Air-BF16** | 가능 | VRAM 여유 있음 |
| 큰 모델 서빙 감각 | **GLM-4.5-FP8** | 가능성 높음 | context/concurrency 줄여 시작 |
| 풀스케일 최신 GLM | **GLM-5.2-FP8** | 4장/5장 비추천 | 공식 레시피가 8장 기준 |
| 파인튜닝 | **GLM-4.5-Air LoRA** | 가능 | 4장 환경에서 가장 현실적 |
| GLM-4.5 풀모델 LoRA | GLM-4.5 | 4장 비추천 | 공식 기준 H100 16장 |
| full fine-tuning | GLM-4.5/Air | 거의 비현실적 | LoRA/QLoRA로 가야 함 |

B200은 DGX B200 기준 8장 합산 GPU 메모리가 1,440GB라서 장당 약 180GB로 보면 됩니다. 따라서 5장은 약 900GB, 4장은 약 720GB 수준입니다. citeturn839846view3

중요한 포인트는 GLM-4.5 계열이 **MoE 모델**이라는 점입니다. GLM-4.5는 총 355B, active 32B이고, GLM-4.5-Air는 총 106B, active 12B입니다. 하지만 서빙할 때는 active parameter만 VRAM에 올라가는 게 아니라 **전체 expert weight를 들고 있어야 해서 VRAM 계산은 total parameter 기준**으로 보는 게 안전합니다. citeturn839846view5

---

## 제일 추천하는 운영 방식

지금 5장을 잠깐 쓸 수 있다면, **억지로 5장을 하나의 vLLM 인스턴스에 묶으려고 하지 않는 게 좋습니다.** `tensor_parallel_size=5`는 모델의 attention head, hidden dimension, MoE shard 구조와 안 맞을 가능성이 있고, 실무에서도 2/4/8 단위가 훨씬 안정적입니다.

추천은 이렇게입니다.

```bash
GPU 0,1,2,3  → GLM-4.5-Air 또는 GLM-4.5-FP8 vLLM 서빙
GPU 4        → 다른 실험용: 작은 모델, 벤치마크, LoRA 테스트, 데이터 전처리
```

즉, **4장을 기준으로 실험 환경을 만들고**, 5번째 GPU는 “추가 실험 슬롯”으로 쓰는 게 나중에 4장만 남았을 때도 그대로 이어가기 좋습니다.

---

## 1순위: GLM-4.5-Air-FP8

이게 가장 좋습니다. GLM-4.5-Air-FP8은 106B-A12B 모델이고, 공식 문서상 GLM-4.5-Air FP8은 H100 2장/H200 1장 수준에서도 실행 가능하다고 되어 있습니다. full 128K context는 H100 4장/H200 2장 기준으로 제시됩니다. citeturn839846view7

4×B200이면 이 모델은 꽤 여유롭게 돌릴 수 있습니다.

예시:

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3

vllm serve /models/GLM-4.5-Air-FP8 \
  --tensor-parallel-size 4 \
  --served-model-name glm-4.5-air-fp8 \
  --reasoning-parser glm45 \
  --tool-call-parser glm45 \
  --enable-auto-tool-choice \
  --kv-cache-dtype fp8_e4m3 \
  --gpu-memory-utilization 0.90 \
  --max-model-len 131072 \
  --max-num-seqs 8
```

처음에는 `--max-num-seqs 4`나 `8`로 시작하고, 안정화되면 올리면 됩니다. long context를 테스트할 때 OOM이 나면 `--max-model-len`을 `65536` 또는 `32768`로 낮추면 됩니다.

---

## 2순위: GLM-4.5-FP8

5장/4장 환경에서 “큰 모델을 만져봤다”는 감각을 얻고 싶으면 **GLM-4.5-FP8**이 좋습니다. GLM-4.5는 355B-A32B이고 FP8 버전이 공개되어 있습니다. 공식 표에서 GLM-4.5 FP8은 H100 8장/H200 4장으로 실행 가능하다고 제시되어 있습니다. 다만 full 128K context는 H100 16장/H200 8장 기준이라, 4×B200에서는 context/concurrency를 낮춰 시작하는 게 안전합니다. citeturn839846view5

예시:

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3

vllm serve /models/GLM-4.5-FP8 \
  --tensor-parallel-size 4 \
  --served-model-name glm-4.5-fp8 \
  --reasoning-parser glm45 \
  --tool-call-parser glm45 \
  --enable-auto-tool-choice \
  --kv-cache-dtype fp8_e4m3 \
  --gpu-memory-utilization 0.90 \
  --max-model-len 32768 \
  --max-num-seqs 2
```

이걸 먼저 성공시키고 나서:

```bash
--max-model-len 65536
--max-num-seqs 4
```

이런 식으로 올려보면 됩니다. 여기서 얻을 수 있는 감각은 꽤 큽니다. 특히 vLLM에서 MoE 모델의 메모리, KV cache, tensor parallel, prefill/decode 병목을 체감하기 좋습니다.

---

## GLM-5.2는 지금 환경에서는 비추천

GLM-5.2는 훨씬 큽니다. vLLM recipe 기준으로 GLM-5.2는 약 743B total / 39B active MoE이고, FP8 checkpoint 기준으로도 표준 single-node 실행은 8×H200/H20, full 1M context는 8×B200 기준입니다. citeturn610009view0

즉, **5×B200이나 4×B200으로 GLM-5.2를 제대로 로컬 서빙하려는 건 시간 대비 리스크가 큽니다.** 모델이 일부 quantized variant로 겨우 올라갈 가능성은 있어도, vLLM에서 안정적인 실험을 하기에는 8장 기준으로 설계된 쪽입니다. GLM-5.2를 꼭 찍먹하고 싶다면 `nvidia/GLM-5.2-NVFP4` 같은 Blackwell용 quantized variant가 있지만, 공식 레시피도 `tensor-parallel-size 8`을 전제로 제시합니다. citeturn610009view4

지금처럼 GPU 반납 전 감각을 끌어올리는 목적이면 **GLM-5.2에 시간 쓰기보다 GLM-4.5-FP8과 GLM-4.5-Air fine-tuning에 집중하는 게 낫습니다.**

---

## 로컬에 모델 저장해두고 필요할 때 꺼내 쓰는 방식

이 구조가 좋습니다.

```bash
/models/
  glm/
    GLM-4.5-Air-FP8/
    GLM-4.5-Air/
    GLM-4.5-FP8/
  adapters/
    glm-4.5-air-lora-mydata/
```

다운로드는 예를 들면:

```bash
pip install -U "huggingface_hub[cli]"

hf download zai-org/GLM-4.5-Air-FP8 \
  --local-dir /models/glm/GLM-4.5-Air-FP8

hf download zai-org/GLM-4.5-FP8 \
  --local-dir /models/glm/GLM-4.5-FP8
```

그리고 vLLM은 Hugging Face repo name 대신 로컬 경로를 주면 됩니다.

```bash
vllm serve /models/glm/GLM-4.5-Air-FP8 ...
```

---

## 파인튜닝은 4장으로 가능할까?

**가능합니다. 단, GLM-4.5-Air LoRA 기준입니다.**

공식 모델 카드에서도 GLM-4.5-Air는 LLaMA-Factory 기준 H100 4장으로 LoRA fine-tuning 가능하다고 제시되어 있습니다. 반면 GLM-4.5 풀모델 LoRA는 H100 16장 기준입니다. citeturn839846view5

따라서 4×B200이면:

```text
GLM-4.5-Air LoRA       가능
GLM-4.5-Air QLoRA      가능성 높음
GLM-4.5-Air full SFT   비추천
GLM-4.5 full LoRA      비추천
GLM-5.2 fine-tuning    비추천
```

파인튜닝 전략은 이렇게 잡는 게 좋습니다.

```text
1단계: GLM-4.5-Air-FP8 vLLM 서빙
2단계: GLM-4.5-Air BF16으로 LoRA fine-tuning
3단계: LoRA adapter 저장
4단계: vLLM에서 base model + LoRA adapter 로딩
5단계: 원본 모델 vs LoRA 모델 응답 비교
```

처음 fine-tuning 설정은 보수적으로 잡으세요.

```text
sequence length: 4096 또는 8192
per_device_train_batch_size: 1
gradient_accumulation_steps: 8~32
bf16: true
gradient_checkpointing: true
LoRA rank: 8, 16, 32 중 시작은 16
target modules: q_proj, k_proj, v_proj, o_proj, gate/up/down 계열
```

---

## 지금 바로 할 실험 순서

제가 보기에는 이 순서가 가장 실전적입니다.

### Day 1: vLLM 서빙 감각

```text
GLM-4.5-Air-FP8
TP=1, TP=2, TP=4 비교
max_model_len 32K → 64K → 128K
max_num_seqs 1 → 4 → 8 → 16
prefill/decode 속도 측정
```

### Day 2: 큰 모델 감각

```text
GLM-4.5-FP8
TP=4
max_model_len 32K부터 시작
OOM 기준점 확인
긴 prompt 넣었을 때 prefill 병목 확인
동시 요청 수 올렸을 때 KV cache 압박 확인
```

### Day 3: fine-tuning

```text
GLM-4.5-Air BF16 또는 가능하면 training-friendly checkpoint
LoRA SFT
작은 instruction dataset 1천~1만 개
학습 후 adapter 저장
```

### Day 4: adapter serving

```text
vLLM base model 서빙
LoRA adapter 붙여보기
원본/튜닝 모델 비교
latency, VRAM, 품질 차이 기록
```

---

## 최종 판단

**4×B200 환경에서는 GLM-4.5-Air는 서빙과 LoRA fine-tuning 모두 현실적입니다.** GLM-4.5-FP8도 큰 모델 서빙 실험용으로 충분히 도전할 만합니다. 반대로 GLM-5.2는 8×B200/H200 기준으로 보는 게 맞아서, 지금 5장/4장 환경에서 핵심 목표로 잡기에는 비효율적입니다.

가장 좋은 선택은:

```text
메인 서빙 모델: GLM-4.5-Air-FP8
고성능 실험 모델: GLM-4.5-FP8
파인튜닝 모델: GLM-4.5-Air BF16 + LoRA
운영 기준 GPU 수: 4장
5번째 GPU: 별도 실험/비교/예비 슬롯
```

이렇게 잡으면 지금 5장을 최대한 활용하면서도, 나중에 4장만 남았을 때 그대로 운영 가능한 구조가 됩니다.

---

### ❓ 질문 (User)
나는 극한에 도전해보고싶어. 그리고 서버로 올리다보니까 token 을 올려두기엔 좀 그런데 다른 방법 없을까?

### 💡 답변 (Assistant)
좋습니다. “극한”이면 목표를 **안정 운영**이 아니라 **OOM 직전까지 밀어붙여서 한계선을 찾는 벤치마크**로 잡으면 됩니다. 그리고 서버에 토큰을 남기지 않는 방식도 꽤 깔끔하게 만들 수 있습니다.

---

### ❓ 질문 (User)
아 그리고 꼭 glm 아니어도 괜찮아 허깅페이스에 있는 모델 중에 적합한거 몇개 추천해줘

### 💡 답변 (Assistant)
좋습니다. 그러면 방향을 이렇게 바꾸는 게 맞습니다.

**목표:**  
4×B200 기준으로 나중에도 재현 가능하게 만들되, 지금 5장이 있을 때는 **극한 서빙 실험 + OOM 경계선 찾기 + benchmark 기록**까지 해보는 구조가 좋습니다. DGX B200은 8장 기준 총 GPU 메모리 1,440GB라서 B200 한 장을 약 180GB로 보면 되고, 4장은 약 720GB, 5장은 약 900GB입니다. citeturn467470search0

그리고 Hugging Face token은 **서버에 남기지 않는 방식**으로 충분히 운영할 수 있습니다.

---

## 1. Token을 서버에 안 올리는 가장 좋은 방법

가장 깔끔한 방식은 이겁니다.

```text
개인 PC / 안전한 다운로드 노드에서 Hugging Face 모델 다운로드
→ 모델 폴더만 서버로 rsync/scp
→ vLLM은 Hugging Face repo name이 아니라 local path로 실행
→ 서버에는 HF token 없음
```

즉 서버에서는 이렇게만 실행합니다.

```bash
vllm serve /models/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  --tensor-parallel-size 4
```

이러면 서버는 Hugging Face Hub에 인증할 필요가 없습니다.

다운로드 노드에서는 token을 영구 저장하지 말고 one-shot으로만 씁니다. Hugging Face 문서상 `HF_TOKEN` 환경변수는 저장된 토큰보다 우선 적용되고, 토큰 파일 기본 위치는 `"$HF_HOME/token"`입니다. 또한 HF CLI 문서도 보안상 token을 환경변수로 전달하는 방식을 권장합니다. citeturn891063view0turn108353search1

```bash
# 다운로드 노드에서만 실행
mkdir -p /mnt/models

read -s HF_TOKEN
export HF_TOKEN

hf download Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  --local-dir /mnt/models/Qwen3-Coder-480B-A35B-Instruct-FP8

unset HF_TOKEN
rm -f ~/.cache/huggingface/token
```

그다음 서버로 전송합니다.

```bash
rsync -ah --info=progress2 \
  /mnt/models/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  user@server:/models/
```

서버에서는 아예 offline mode를 켜도 됩니다. `HF_HUB_OFFLINE=1`은 Hub로 HTTP 호출을 하지 않고 local cache/path만 사용하게 합니다. citeturn891063view0

```bash
export HF_HUB_OFFLINE=1
export CUDA_VISIBLE_DEVICES=0,1,2,3

vllm serve /models/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  --tensor-parallel-size 4
```

**핵심:** `huggingface-cli login`을 서버에서 하지 마세요. 모델은 artifact처럼 옮기고, 서버는 local path만 보게 만드는 게 제일 안전합니다.

---

## 2. 5장 사용 전략: 5-way TP는 비추천

극한 도전이라고 해도 `tensor_parallel_size=5`는 별로 추천하지 않습니다. 많은 모델이 attention head 수, expert 수, hidden dimension이 2/4/8 단위로 잘 나뉘고, 5는 모양이 안 맞을 가능성이 큽니다.

대신 이렇게 가세요.

```text
GPU 0,1,2,3 → 메인 초대형 vLLM 서빙
GPU 4       → benchmark client / 작은 비교 모델 / LoRA 실험 / 모니터링
```

또는:

```text
GPU 0,1,2,3 → Qwen3-Coder-480B / GLM-4.5 / DeepSeek 계열
GPU 4       → gpt-oss-120b 단독 서빙 or fine-tuning 실험
```

이렇게 하면 나중에 4장만 남아도 환경이 그대로 유지됩니다.

---

## 3. Hugging Face 모델 추천

### 1순위: Qwen3-Coder-480B-A35B-Instruct-FP8

이게 지금 목적에 제일 잘 맞습니다. **극한에 가깝고, vLLM 지원이 명시되어 있고, 4×B200에서 도전 가치가 큽니다.** Qwen3-Coder-480B-A35B는 480B total / 35B active MoE 모델이고, native context length가 262,144 tokens입니다. FP8 checkpoint는 `transformers`, `sglang`, `vllm`에서 사용할 수 있다고 명시되어 있습니다. citeturn391197search0turn391197search3

4×B200에서는 이 모델부터 추천합니다.

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export HF_HUB_OFFLINE=1

vllm serve /models/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  --served-model-name qwen3-coder-480b-fp8 \
  --tensor-parallel-size 4 \
  --enable-expert-parallel \
  --gpu-memory-utilization 0.94 \
  --max-model-len 32768 \
  --max-num-seqs 1 \
  --trust-remote-code
```

처음부터 262K를 걸지 말고 이렇게 올리세요.

```text
32K → 64K → 128K → 262K
max_num_seqs 1 → 2 → 4
gpu_memory_utilization 0.90 → 0.94 → 0.97
```

이 모델이 좋은 이유는 **OOM 경계선, MoE expert parallel, long-context KV cache 압박, agentic coding latency**를 한 번에 체험할 수 있기 때문입니다.

---

### 2순위: GLM-4.5-FP8

GLM도 여전히 좋은 선택입니다. GLM-4.5는 355B total / 32B active, GLM-4.5-Air는 106B total / 12B active MoE 모델이고, FP8 버전도 공개되어 있습니다. GLM-4.5 계열은 reasoning, coding, agent 능력을 통합한 모델로 소개되어 있습니다. citeturn170004search0turn170004search2

4×B200에서는 `GLM-4.5-FP8`이 “큰 모델 서빙 감각”을 얻기에 좋고, `GLM-4.5-Air`는 나중에 fine-tuning 후보로 좋습니다.

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export HF_HUB_OFFLINE=1

vllm serve /models/GLM-4.5-FP8 \
  --served-model-name glm-4.5-fp8 \
  --tensor-parallel-size 4 \
  --enable-expert-parallel \
  --reasoning-parser glm45 \
  --tool-call-parser glm45 \
  --enable-auto-tool-choice \
  --kv-cache-dtype fp8_e4m3 \
  --gpu-memory-utilization 0.94 \
  --max-model-len 65536 \
  --max-num-seqs 2
```

GLM은 “코딩 + 에이전트 + reasoning” 실험용으로 좋고, Qwen3-Coder는 “repo-scale coding / agentic coding” 극한 실험용으로 더 좋습니다.

---

### 3순위: DeepSeek-V3 / DeepSeek-R1 계열

진짜 극한을 보고 싶으면 DeepSeek 계열입니다. DeepSeek-V3는 671B total / 37B active MoE 모델로 공개되어 있고, DeepSeek-R1도 vLLM 쪽 대형 서빙 사례에서 671B total / 37B active 구조로 언급됩니다. citeturn615247search9turn615247search19

다만 4×B200의 720GB에서는 **FP8 weight만으로도 상당히 빡빡하고 KV cache 여유가 작습니다.** 5×B200은 총 메모리는 더 크지만 TP=5가 애매해서 오히려 깔끔하지 않을 수 있습니다.

이건 “성공 운영”보다는 “한계 실험”으로 보세요.

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export HF_HUB_OFFLINE=1

vllm serve /models/DeepSeek-R1 \
  --served-model-name deepseek-r1 \
  --tensor-parallel-size 4 \
  --enable-expert-parallel \
  --gpu-memory-utilization 0.97 \
  --max-model-len 8192 \
  --max-num-seqs 1 \
  --trust-remote-code
```

처음은 `8K`부터 시작하세요. 이건 실패해도 얻는 게 많습니다. 어디서 터지는지 보면 weight 메모리, KV cache, NCCL, expert parallel, tokenizer/model config 문제를 전부 보게 됩니다.

---

### 4순위: Nvidia Nemotron Ultra 253B

`nvidia/Llama-3_1-Nemotron-Ultra-253B-v1`도 괜찮습니다. 모델 카드상 253B reasoning 모델이고, RAG/tool calling/chat preference 쪽 post-training이 되어 있으며 128K context를 지원하고, inference는 single 8×H100 node에 맞는다고 설명되어 있습니다. citeturn382895search2

B200 4장에서는 weight memory 관점상 도전해볼 만합니다. 다만 dense 계열에 가까운 큰 모델은 MoE보다 decode 비용이 더 묵직하게 느껴질 수 있습니다. “MoE 극한”보다는 “dense-ish 대형 reasoning 모델 감각”에 좋습니다.

---

### 5순위: gpt-oss-120b

이건 극한용은 아니지만 꼭 한 번 돌려볼 가치가 있습니다. Hugging Face 모델 카드에 vLLM으로 OpenAI-compatible server를 띄우는 예시가 있고, `gpt-oss-120b`와 `gpt-oss-20b`는 open-weight reasoning model로 공개되어 있습니다. citeturn382895search0turn382895academia37

B200에서는 너무 쉽게 돌아갈 가능성이 높지만, **vLLM 세팅 검증, API 호환성, benchmark baseline**으로 아주 좋습니다.

```bash
export CUDA_VISIBLE_DEVICES=4

vllm serve /models/gpt-oss-120b \
  --served-model-name gpt-oss-120b \
  --gpu-memory-utilization 0.90 \
  --max-model-len 131072
```

5번째 GPU에 이걸 올려두고, 4장짜리 대형 모델과 품질/latency를 비교하면 꽤 재밌습니다.

---

### 6순위: Kimi K2는 “지금 환경에서는 너무 큼”

Kimi K2는 1T total / 32B active MoE 모델입니다. citeturn615247search5  
하지만 vLLM recipe 기준으로 Kimi-K2-Thinking은 8×H200/H20 실행을 제시하고, Kimi-K2 FP8도 128K context 기준 mainstream H800 16장 구성을 최소 단위로 설명합니다. citeturn382895search3turn382895search7

즉 4×B200이나 5×B200으로는 시간 대비 리스크가 큽니다. 극한 도전이라도 **DeepSeek나 Qwen3-Coder-480B 쪽이 더 생산적**입니다.

---

## 4. 내가 추천하는 실험 순서

### Step 1 — vLLM sanity check

```text
gpt-oss-120b 또는 GLM-4.5-Air-FP8
목표: vLLM, CUDA, NCCL, OpenAI-compatible API 정상 확인
```

### Step 2 — 실전 대형 모델

```text
Qwen3-Coder-480B-A35B-Instruct-FP8
TP=4
EP enabled
32K context부터 시작
```

### Step 3 — GLM 비교

```text
GLM-4.5-FP8
Qwen3-Coder-480B와 latency / 품질 / VRAM 비교
```

### Step 4 — 진짜 극한

```text
DeepSeek-R1 또는 DeepSeek-V3
TP=4
max_model_len=8192
max_num_seqs=1
gpu_memory_utilization=0.97
```

### Step 5 — fine-tuning 후보 분리

```text
서빙 극한: Qwen3-Coder-480B, GLM-4.5, DeepSeek
파인튜닝 현실 후보: GLM-4.5-Air, Qwen3.6-35B-A3B, gpt-oss-120b LoRA
```

서빙에서 극한을 찍는 모델과 fine-tuning할 모델은 분리하는 게 좋습니다. 480B/671B급은 fine-tuning보다 **서빙 병렬화 감각**을 얻는 용도로 쓰고, fine-tuning은 35B~120B급 또는 GLM-4.5-Air 쪽이 현실적입니다.

---

## 5. Benchmark 명령

vLLM은 `vllm bench serve`를 제공하고, random dataset에서는 input/output token 길이를 지정할 수 있습니다. citeturn457975search0turn457975search2

서버 띄운 뒤:

```bash
vllm bench serve \
  --backend openai-chat \
  --base-url http://127.0.0.1:8000 \
  --endpoint /v1/chat/completions \
  --model qwen3-coder-480b-fp8 \
  --dataset-name random \
  --num-prompts 64 \
  --max-concurrency 1 \
  --random-input-len 8192 \
  --random-output-len 1024 \
  --ignore-eos
```

그다음 이렇게 올립니다.

```text
input_len:       8K → 16K → 32K → 64K
output_len:      1K → 2K → 4K
concurrency:     1 → 2 → 4 → 8
num_prompts:    64 → 128 → 256
```

기록할 항목은 이겁니다.

```text
TTFT
TPOT
output tokens/sec
GPU memory usage
KV cache usage
OOM 발생 조건
NCCL error 여부
서버 기동 시간
첫 요청 latency
```

---

## 최종 추천 조합

제일 재밌고 실속 있는 조합은 이겁니다.

```text
1순위 극한 모델:
Qwen3-Coder-480B-A35B-Instruct-FP8

2순위 GLM 비교 모델:
GLM-4.5-FP8

3순위 한계 테스트:
DeepSeek-R1 또는 DeepSeek-V3

5번째 GPU 활용:
gpt-oss-120b 단독 서빙 / benchmark client / LoRA 실험

파인튜닝 후보:
GLM-4.5-Air 또는 Qwen3.6-35B-A3B 계열
```

그리고 token 문제는 **서버에서 HF login 하지 말고, 모델을 미리 다운로드한 뒤 local path로 vLLM을 띄우는 방식**이 가장 깔끔합니다. 이 구조면 서버에는 HF token이 없어도 되고, 나중에 4장만 남아도 그대로 재현 가능합니다.

---

### ❓ 질문 (User)
지금 작성한 글들 잘 모아서 제안서 형태로 작성해. 문체는 15년차 베테랑 머신러닝 엔지니어가 작성했고, 잘 다듬어진 문체로 작성해서 나한테 줘.

### 💡 답변 (Assistant)
이전 논의를 하나의 실행 가능한 제안서로 정리하겠습니다. 모델 스펙·vLLM 옵션·GPU 메모리 기준은 공개 문서 기준으로 다시 확인해, 의사결정에 바로 쓰기 좋게 다듬겠습니다.

---

### 💡 답변 (Assistant)
DeepSeek은 4×B200 FP4 레시피가 있어 극한 실험 후보로 더 강하게 반영하고, Kimi K2는 이번 주력 범위에서 제외하겠습니다.

---

### 💡 답변 (Assistant)
# B200 기반 대형 언어 모델 로컬 서빙 및 파인튜닝 실험 제안서

## 1. 제안 개요

현재 사용 가능한 환경은 **B200 GPU 5장**이며, 가까운 시점에 1장을 반납하고 **B200 GPU 4장 체계로 전환될 가능성**이 있다. 따라서 이번 실험의 핵심 목적은 단순히 모델 하나를 구동하는 것이 아니라, 짧은 기간 동안 고성능 GPU 자원을 최대한 활용해 다음 세 가지 감각을 확보하는 데 있다.

첫째, **vLLM 기반 대형 모델 서빙의 한계 지점**을 직접 확인한다.  
둘째, 향후 4장 환경에서도 재현 가능한 운영 구조를 만든다.  
셋째, 최종적으로 로컬 모델을 대상으로 **LoRA/QLoRA 기반 파인튜닝 가능성**까지 검증한다.

이번 실험은 “안정적인 운영”만을 목표로 하지 않는다. 사용 가능한 자원이 B200급인 만큼, 일반적인 70B 또는 120B급 모델에서 멈추기보다는 **480B, 671B급 MoE 모델까지 도전하면서 OOM 경계, KV cache 압박, tensor parallel, expert parallel, long-context serving의 병목을 체감하는 것**을 목표로 한다.

다만 중요한 운영 원칙은 명확하다.

**실제 운영 기준은 4×B200으로 잡고, 현재의 5번째 GPU는 극한 실험, 비교 모델, 벤치마크 클라이언트, 파인튜닝 테스트 슬롯으로 활용한다.**

이 방식이 가장 실용적이다. 5장을 기준으로 구조를 설계하면 나중에 4장으로 축소될 때 다시 튜닝해야 한다. 반면 처음부터 4장 기준으로 모델을 띄우고, 5번째 GPU를 별도 실험용으로 쓰면 이후 환경 변화에도 운영 구조가 흔들리지 않는다.

---

## 2. 현재 환경과 제약 조건

### 2.1 하드웨어 전제

현재 가용 자원은 다음과 같이 본다.

```text
현재 환경: B200 GPU 5장
향후 환경: B200 GPU 4장 가능성 높음
운영 기준: 4×B200
임시 활용 자원: 5번째 B200
```

B200은 장당 GPU 메모리가 매우 큰 축에 속하므로, 4장 환경에서도 일반적인 대형 dense 모델뿐 아니라 상당수의 MoE 모델을 실험할 수 있다. 다만 480B, 671B, 1T급 모델은 weight memory뿐 아니라 KV cache, NCCL 통신, vLLM 내부 병렬화 전략, context length 설정이 모두 영향을 주므로 단순히 “총 파라미터 수 × dtype”만 보고 판단하면 안 된다.

특히 MoE 모델은 active parameter 수가 작더라도, 서빙 시에는 전체 expert weight를 분산 적재해야 한다. 따라서 VRAM 계산은 **active parameter가 아니라 total parameter 기준**으로 보수적으로 접근해야 한다.

---

### 2.2 소프트웨어 전제

서빙 프레임워크는 **vLLM**을 사용한다.

```text
Serving framework: vLLM
Serving API: OpenAI-compatible API
Model source: Hugging Face checkpoint
Model loading: local path 기반
운영 방식: 필요 시 로컬 모델 디렉터리에서 기동
```

서버에 직접 Hugging Face token을 남기는 것은 지양한다. 모델은 별도 다운로드 노드 또는 개인 PC에서 받은 뒤 서버로 전송하고, 서버에서는 local path만 사용해 vLLM을 실행하는 구조가 바람직하다.

---

## 3. 핵심 운영 전략

### 3.1 5장 전체를 하나의 tensor parallel 그룹으로 묶지 않는다

극한 실험을 하더라도 `tensor_parallel_size=5`는 권장하지 않는다.

대부분의 대형 모델은 hidden dimension, attention head, KV head, expert partitioning 등이 2, 4, 8 단위로 나누어지도록 설계되어 있다. 5-way tensor parallel은 모델 구조와 잘 맞지 않을 가능성이 높고, 맞더라도 성능이나 안정성 면에서 이점이 크지 않다.

따라서 기본 전략은 다음과 같다.

```text
GPU 0,1,2,3 → 메인 대형 모델 vLLM 서빙
GPU 4       → 별도 실험 슬롯
```

5번째 GPU의 활용 방식은 다음 중 하나가 적합하다.

```text
1. 벤치마크 클라이언트 전용
2. gpt-oss-120b 같은 비교 모델 단독 서빙
3. GLM-4.5-Air 또는 Qwen 계열 LoRA 실험
4. 데이터 전처리 및 평가 작업
5. 모니터링/프로파일링 보조 작업
```

이 구성의 장점은 명확하다.

현재 5장 환경을 충분히 활용하면서도, 나중에 4장만 남았을 때 메인 서빙 구조를 그대로 유지할 수 있다. 즉, “반납 전 실험”과 “반납 후 운영”이 분리되지 않는다.

---

## 4. Hugging Face Token 보안 운영 방안

서버에 Hugging Face token을 올려두는 것은 피하는 것이 좋다. 특히 여러 사람이 접근할 수 있는 서버이거나, 운영 서버에 가까운 환경이라면 `huggingface-cli login`을 직접 수행해 token을 cache에 남기는 방식은 바람직하지 않다.

권장 방식은 다음과 같다.

```text
개인 PC 또는 별도 다운로드 노드에서 모델 다운로드
→ 모델 디렉터리만 서버로 전송
→ 서버에서는 HF token 없이 local path로 vLLM 실행
→ 필요 시 HF_HUB_OFFLINE=1 설정
```

### 4.1 다운로드 노드에서 모델 받기

```bash
mkdir -p /mnt/models

read -s HF_TOKEN
export HF_TOKEN

hf download Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  --local-dir /mnt/models/Qwen3-Coder-480B-A35B-Instruct-FP8

unset HF_TOKEN
rm -f ~/.cache/huggingface/token
```

이 방식은 token을 shell session 안에서만 사용하고, 다운로드가 끝난 뒤 즉시 제거한다.

---

### 4.2 서버로 모델 전송

```bash
rsync -ah --info=progress2 \
  /mnt/models/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  user@server:/models/
```

서버에는 다음과 같은 구조로 모델을 둔다.

```text
/models/
  qwen/
    Qwen3-Coder-480B-A35B-Instruct-FP8/
  glm/
    GLM-4.5-FP8/
    GLM-4.5-Air-FP8/
    GLM-4.5-Air/
  deepseek/
    DeepSeek-R1/
    DeepSeek-V3/
  openai/
    gpt-oss-120b/
  adapters/
    glm-4.5-air-lora-mydata/
    qwen-lora-mydata/
```

---

### 4.3 서버에서는 offline mode로 실행

```bash
export HF_HUB_OFFLINE=1
export CUDA_VISIBLE_DEVICES=0,1,2,3

vllm serve /models/qwen/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  --served-model-name qwen3-coder-480b-fp8 \
  --tensor-parallel-size 4
```

이 구조에서는 서버가 Hugging Face Hub에 인증할 필요가 없다. 모델 checkpoint, tokenizer, config, generation config 등이 local path에 모두 존재해야 한다.

---

## 5. 추천 모델 후보군

이번 실험의 목적은 크게 두 갈래다.

하나는 **극한 서빙 실험**이고, 다른 하나는 **향후 파인튜닝까지 고려한 현실적인 운영 모델 확보**다.

따라서 모델을 하나만 고르기보다, 역할별로 모델을 나누는 것이 좋다.

---

## 5.1 1순위 극한 서빙 모델: Qwen3-Coder-480B-A35B-Instruct-FP8

### 선정 이유

`Qwen3-Coder-480B-A35B-Instruct-FP8`은 이번 환경에서 가장 먼저 도전해볼 만한 모델이다.

이 모델은 480B급 MoE 구조이며, active parameter는 상대적으로 작지만 전체 weight 규모가 매우 크다. 따라서 4×B200에서 vLLM으로 구동하면 다음 요소를 한 번에 실험할 수 있다.

```text
1. FP8 대형 MoE 모델 로딩
2. tensor parallel 4-way 구성
3. expert parallel 사용 여부
4. long-context serving
5. KV cache 압박
6. prefill latency와 decode throughput 차이
7. coding/agentic workload에서의 실사용성
```

코딩 특화 모델이라는 점도 장점이다. 단순 질의응답보다 repo-scale 코드 분석, 긴 context 기반 reasoning, tool-use 시나리오에서 GPU와 서빙 프레임워크의 한계를 더 잘 드러낸다.

### 권장 실행 예시

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export HF_HUB_OFFLINE=1

vllm serve /models/qwen/Qwen3-Coder-480B-A35B-Instruct-FP8 \
  --served-model-name qwen3-coder-480b-fp8 \
  --tensor-parallel-size 4 \
  --enable-expert-parallel \
  --gpu-memory-utilization 0.94 \
  --max-model-len 32768 \
  --max-num-seqs 1 \
  --trust-remote-code
```

처음부터 긴 context를 최대로 열지 않는다. 다음 순서로 올리는 것이 안전하다.

```text
max_model_len: 32K → 64K → 128K → 262K
max_num_seqs: 1 → 2 → 4
gpu_memory_utilization: 0.90 → 0.94 → 0.97
```

이 모델의 목표는 안정 운영 이전에 “어디서부터 무너지는지”를 확인하는 것이다. 즉, 성공 여부만 중요한 것이 아니라 실패 로그 자체가 중요한 산출물이다.

---

## 5.2 2순위 비교 모델: GLM-4.5-FP8

### 선정 이유

GLM 계열은 여전히 좋은 후보군이다. 특히 `GLM-4.5-FP8`은 reasoning, coding, agent workload를 두루 실험하기 좋고, Qwen3-Coder와 비교했을 때 모델 응답 스타일과 서빙 특성이 다르게 나타날 가능성이 높다.

Qwen3-Coder가 코딩 특화 극한 모델이라면, GLM-4.5는 더 범용적인 reasoning/agent 모델로 보는 것이 좋다.

### 권장 실행 예시

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export HF_HUB_OFFLINE=1

vllm serve /models/glm/GLM-4.5-FP8 \
  --served-model-name glm-4.5-fp8 \
  --tensor-parallel-size 4 \
  --enable-expert-parallel \
  --reasoning-parser glm45 \
  --tool-call-parser glm45 \
  --enable-auto-tool-choice \
  --kv-cache-dtype fp8_e4m3 \
  --gpu-memory-utilization 0.94 \
  --max-model-len 65536 \
  --max-num-seqs 2
```

GLM-4.5-FP8은 4×B200에서 충분히 도전할 가치가 있다. 다만 full long-context와 높은 concurrency를 동시에 욕심내면 KV cache에서 병목이 발생할 수 있으므로, context length와 동시 요청 수를 분리해서 실험해야 한다.

---

## 5.3 3순위 한계 테스트 모델: DeepSeek-R1 또는 DeepSeek-V3 계열

### 선정 이유

DeepSeek 계열은 이번 실험에서 “극한 테스트” 역할에 적합하다.

671B급 MoE 모델은 4×B200에서 상당히 빡빡하다. 따라서 이 모델은 안정적인 서비스 후보라기보다는 다음을 확인하기 위한 모델로 보는 편이 맞다.

```text
1. 4×B200에서 671B급 MoE checkpoint가 어느 정도까지 로딩 가능한가
2. FP8 또는 저정밀 checkpoint 사용 시 실질적인 KV cache 여유가 얼마나 남는가
3. vLLM의 expert parallel, tensor parallel 조합이 어디서 병목을 보이는가
4. NCCL, CUDA graph, memory fragmentation 이슈가 발생하는가
5. 짧은 context라도 실제 decode가 가능한가
```

### 권장 실행 예시

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export HF_HUB_OFFLINE=1

vllm serve /models/deepseek/DeepSeek-R1 \
  --served-model-name deepseek-r1 \
  --tensor-parallel-size 4 \
  --enable-expert-parallel \
  --gpu-memory-utilization 0.97 \
  --max-model-len 8192 \
  --max-num-seqs 1 \
  --trust-remote-code
```

처음은 반드시 보수적으로 시작한다.

```text
max_model_len: 8K
max_num_seqs: 1
gpu_memory_utilization: 0.95~0.97
```

이 모델은 실패 가능성이 있다. 하지만 실패해도 충분히 가치가 있다. 특히 OOM 위치, 로딩 시간, weight shard 분산, KV cache 예약량, NCCL 오류 여부를 확인하면 이후 어떤 규모의 모델까지 운영 가능한지 판단할 수 있다.

---

## 5.4 안정성 검증 및 기준 모델: gpt-oss-120b

### 선정 이유

`gpt-oss-120b`는 극한 모델은 아니지만, vLLM 환경 검증용으로 매우 유용하다.

B200 1장 또는 소수 GPU에서 비교적 수월하게 구동될 가능성이 높기 때문에, 다음 용도로 적합하다.

```text
1. vLLM 설치 및 OpenAI-compatible API 정상 동작 확인
2. benchmark pipeline 검증
3. request/response logging 확인
4. client SDK 호환성 확인
5. 5번째 GPU 단독 활용
6. 대형 MoE 모델과 품질/속도 비교
```

### 권장 실행 예시

```bash
export CUDA_VISIBLE_DEVICES=4
export HF_HUB_OFFLINE=1

vllm serve /models/openai/gpt-oss-120b \
  --served-model-name gpt-oss-120b \
  --gpu-memory-utilization 0.90 \
  --max-model-len 131072
```

이 모델은 “메인 타깃”이라기보다 기준선이다. Qwen3-Coder-480B나 GLM-4.5-FP8이 느리거나 불안정할 때, gpt-oss-120b를 통해 vLLM 자체 문제인지 모델 규모 문제인지 분리할 수 있다.

---

## 5.5 파인튜닝 후보: GLM-4.5-Air 또는 중형 Qwen 계열

파인튜닝은 서빙 극한 실험과 분리해야 한다.

480B, 671B급 모델은 서빙 실험 대상으로는 훌륭하지만, 4×B200 환경에서 파인튜닝 대상으로 삼기에는 시간, 메모리, 디버깅 비용이 지나치게 크다. 특히 full fine-tuning은 현실적이지 않다.

파인튜닝 후보는 다음 기준으로 고르는 것이 좋다.

```text
1. 4×B200에서 LoRA/QLoRA가 안정적으로 가능한가
2. vLLM에서 base model + adapter serving이 가능한가
3. tokenizer/chat template이 복잡하지 않은가
4. 학습 후 평가와 배포가 단순한가
5. 모델 크기가 실험 반복에 적합한가
```

가장 현실적인 후보는 다음과 같다.

```text
1. GLM-4.5-Air
2. GLM-4.5-Air-FP8은 서빙용, BF16 또는 training-friendly checkpoint는 학습용
3. Qwen 중형/대형 Instruct 계열
4. gpt-oss-120b LoRA 실험
```

파인튜닝은 처음부터 고난도 설정으로 들어가지 않는다. 먼저 작은 instruction dataset으로 end-to-end loop를 확인한다.

```text
데이터 규모: 1천~1만 샘플
sequence length: 4K 또는 8K
batch size: per device 1
gradient accumulation: 8~32
precision: bf16
gradient checkpointing: enabled
LoRA rank: 8, 16, 32 중 16부터 시작
```

---

## 6. 권장 실험 계획

## 6.1 1단계: vLLM 환경 검증

먼저 작은 비교 모델 또는 GLM-4.5-Air-FP8로 vLLM 기본 환경을 검증한다.

목표는 다음과 같다.

```text
1. CUDA/NCCL 정상 동작 확인
2. vLLM serve 정상 기동 확인
3. OpenAI-compatible API 응답 확인
4. tokenizer/chat template 문제 확인
5. benchmark client 동작 확인
```

이 단계에서 바로 480B 모델로 들어가면 문제 원인을 분리하기 어렵다. 먼저 기준 모델로 API path와 serving stack을 검증한 뒤 대형 모델로 넘어가는 편이 안정적이다.

---

## 6.2 2단계: Qwen3-Coder-480B FP8 서빙

두 번째 단계에서 메인 극한 모델을 구동한다.

초기 설정은 보수적으로 잡는다.

```text
tensor_parallel_size: 4
expert_parallel: enabled
max_model_len: 32K
max_num_seqs: 1
gpu_memory_utilization: 0.90~0.94
```

이후 다음 항목을 단계적으로 올린다.

```text
1. max_model_len
2. max_num_seqs
3. random input length
4. random output length
5. benchmark concurrency
6. gpu_memory_utilization
```

이 단계의 핵심 산출물은 단순 성공 여부가 아니다.

```text
1. 최대 안정 context length
2. 최대 안정 concurrency
3. OOM 발생 조건
4. TTFT
5. TPOT
6. output tokens/sec
7. GPU별 memory balance
8. NCCL 오류 여부
9. 첫 요청 latency
10. 장시간 구동 안정성
```

---

## 6.3 3단계: GLM-4.5-FP8 비교

Qwen3-Coder-480B가 코딩 특화 극한 모델이라면, GLM-4.5-FP8은 reasoning/agent 성향 비교 모델로 둔다.

같은 benchmark 조건에서 비교한다.

```text
input length: 8K, 16K, 32K, 64K
output length: 1K, 2K, 4K
concurrency: 1, 2, 4
```

비교 항목은 다음과 같다.

```text
1. 모델 기동 시간
2. VRAM 사용량
3. TTFT
4. TPOT
5. 긴 context에서의 안정성
6. 코딩 태스크 품질
7. reasoning 태스크 품질
8. tool-call parser 사용성
9. vLLM 옵션 호환성
```

이 비교를 통해 최종적으로 어떤 모델을 메인 로컬 서빙 모델로 둘지 판단한다.

---

## 6.4 4단계: DeepSeek 계열 한계 테스트

DeepSeek-R1 또는 DeepSeek-V3는 안정 운영 후보라기보다, 4×B200의 상한선을 확인하기 위한 모델이다.

처음부터 긴 context를 시도하지 않는다.

```text
max_model_len: 8K
max_num_seqs: 1
concurrency: 1
```

이 단계에서 확인할 것은 다음이다.

```text
1. 모델 weight 로딩 가능 여부
2. vLLM 초기화 성공 여부
3. 첫 응답 생성 가능 여부
4. memory fragmentation 발생 여부
5. expert parallel 관련 오류 여부
6. GPU별 메모리 편차
7. 짧은 context에서의 decode 가능성
```

이 모델은 실패 가능성을 전제로 둔다. 하지만 이 실패는 의미 있는 실패다. 어디서 막히는지 알면, 이후 4×B200 환경에서 어떤 규모의 모델을 안정권으로 볼 수 있는지 판단할 수 있다.

---

## 6.5 5단계: LoRA/QLoRA 파인튜닝

파인튜닝은 GLM-4.5-Air 또는 중형 Qwen 계열로 시작한다.

권장 순서는 다음과 같다.

```text
1. base model 로컬 저장
2. 학습 데이터 chat format 정리
3. LoRA SFT 수행
4. adapter 저장
5. vLLM에서 base model + LoRA adapter 로딩
6. 원본 모델과 adapter 모델 응답 비교
7. latency 및 VRAM 변화 측정
```

초기 학습 설정은 다음처럼 잡는다.

```text
sequence length: 4096 또는 8192
per_device_train_batch_size: 1
gradient_accumulation_steps: 8~32
bf16: true
gradient_checkpointing: true
LoRA rank: 16
LoRA alpha: 32 또는 64
LoRA dropout: 0.05
```

처음부터 full fine-tuning은 하지 않는다. 이 환경에서 중요한 것은 “학습을 끝까지 한 번 돌리는 것”과 “학습된 adapter를 실제 vLLM serving에 붙여보는 것”이다.

---

## 7. 벤치마크 계획

vLLM의 `vllm bench serve`를 활용해 serving 성능을 측정한다.

기본 예시는 다음과 같다.

```bash
vllm bench serve \
  --backend openai-chat \
  --base-url http://127.0.0.1:8000 \
  --endpoint /v1/chat/completions \
  --model qwen3-coder-480b-fp8 \
  --dataset-name random \
  --num-prompts 64 \
  --max-concurrency 1 \
  --random-input-len 8192 \
  --random-output-len 1024 \
  --ignore-eos
```

벤치마크는 다음 순서로 올린다.

```text
input_len:    8K → 16K → 32K → 64K → 128K
output_len:   1K → 2K → 4K
concurrency:  1 → 2 → 4 → 8
num_prompts: 64 → 128 → 256
```

측정해야 할 핵심 지표는 다음과 같다.

```text
1. TTFT, Time To First Token
2. TPOT, Time Per Output Token
3. output tokens/sec
4. request throughput
5. GPU memory usage
6. KV cache usage
7. OOM 발생 조건
8. NCCL error 여부
9. server startup time
10. first request latency
11. long-running stability
```

벤치마크 결과는 모델별로 동일한 형식으로 남긴다.

```text
model_name
checkpoint_dtype
tensor_parallel_size
expert_parallel_enabled
max_model_len
max_num_seqs
gpu_memory_utilization
input_len
output_len
concurrency
TTFT
TPOT
tokens/sec
peak_memory_per_gpu
failure_condition
notes
```

이렇게 남겨야 나중에 5장 반납 후 4장 환경에서도 같은 조건을 재현할 수 있다.

---

## 8. 리스크와 대응 방안

### 8.1 OOM 리스크

대형 MoE 모델은 weight loading은 성공해도 실제 요청 시 KV cache에서 OOM이 발생할 수 있다.

대응 방안은 다음과 같다.

```text
1. max_model_len을 낮춘다
2. max_num_seqs를 낮춘다
3. concurrency를 낮춘다
4. kv-cache-dtype을 FP8로 설정한다
5. gpu_memory_utilization을 보수적으로 조정한다
6. 먼저 짧은 context에서 decode 가능 여부를 확인한다
```

---

### 8.2 5-way TP 비효율 리스크

5장을 하나의 tensor parallel group으로 묶으면 모델 구조와 맞지 않아 실패하거나 비효율이 발생할 수 있다.

대응 방안은 명확하다.

```text
메인 서빙은 TP=4로 고정
5번째 GPU는 독립 실험용으로 사용
```

---

### 8.3 Token 노출 리스크

서버에 Hugging Face token을 저장하면 보안상 부담이 생긴다.

대응 방안은 다음과 같다.

```text
1. 서버에서 huggingface-cli login 금지
2. 다운로드 노드에서만 HF_TOKEN 사용
3. 다운로드 후 token 제거
4. 서버에는 모델 artifact만 전송
5. 서버는 HF_HUB_OFFLINE=1로 실행
```

---

### 8.4 파인튜닝 대상 과대 설정 리스크

480B 또는 671B 모델을 바로 파인튜닝 대상으로 삼으면 실험 반복 속도가 지나치게 느려지고 디버깅 비용이 커진다.

대응 방안은 다음과 같다.

```text
서빙 극한 모델과 파인튜닝 모델을 분리한다.
서빙 극한: Qwen3-Coder-480B, GLM-4.5-FP8, DeepSeek 계열
파인튜닝: GLM-4.5-Air, 중형 Qwen 계열, gpt-oss-120b
```

---

## 9. 최종 권장 구성

가장 균형 잡힌 구성은 다음과 같다.

```text
메인 극한 서빙 모델:
Qwen3-Coder-480B-A35B-Instruct-FP8

비교 서빙 모델:
GLM-4.5-FP8

한계 테스트 모델:
DeepSeek-R1 또는 DeepSeek-V3

기준선/검증 모델:
gpt-oss-120b

파인튜닝 후보:
GLM-4.5-Air 또는 중형 Qwen 계열
```

GPU 구성은 다음을 권장한다.

```text
GPU 0,1,2,3:
대형 모델 vLLM serving

GPU 4:
benchmark client
또는 gpt-oss-120b 단독 serving
또는 LoRA fine-tuning 실험
```

운영 기준은 4장이다. 5번째 GPU는 메인 구조에 편입하지 않고, 실험 가속과 비교 평가에 사용한다. 이 방식이 향후 4장 환경으로 축소되었을 때 가장 손실이 적다.

---

## 10. 결론

이번 환경은 일반적인 로컬 LLM 실험 환경이 아니다. B200 5장을 사용할 수 있는 시점은 짧더라도, 이 기간 동안 얻을 수 있는 경험치는 상당히 크다. 따라서 70B급 안정 운영에 머무르기보다, 4×B200 기준에서 재현 가능한 구조를 만들고, 5번째 GPU를 활용해 대형 MoE 모델의 실질적인 한계선을 확인하는 편이 낫다.

가장 추천하는 진행 방향은 다음과 같다.

```text
1. 서버에는 Hugging Face token을 남기지 않는다.
2. 모델은 별도 환경에서 다운로드 후 /models 경로로 전송한다.
3. vLLM은 local path 기반으로 실행한다.
4. 메인 서빙 구조는 4×B200, TP=4로 고정한다.
5. Qwen3-Coder-480B-A35B-Instruct-FP8을 1순위 극한 모델로 실험한다.
6. GLM-4.5-FP8로 reasoning/agent 성향을 비교한다.
7. DeepSeek 계열로 4×B200의 상한선을 확인한다.
8. 파인튜닝은 GLM-4.5-Air 또는 중형 Qwen 계열 LoRA로 별도 진행한다.
9. 모든 실험은 context length, concurrency, TTFT, TPOT, OOM 조건을 기록한다.
```

최종적으로 이 제안의 핵심은 하나다.

**지금 5장을 “운영 구조”에 묶지 말고, 4장 기준의 재현 가능한 서빙 체계를 만든 뒤 5번째 GPU로 극한 실험과 비교 실험을 병렬 수행해야 한다.**

이렇게 접근하면 GPU를 반납하기 전에는 대형 모델 서빙의 한계를 충분히 밀어붙일 수 있고, 반납 이후에는 4×B200 환경에서 바로 이어갈 수 있는 실전형 로컬 LLM 운영 체계를 확보할 수 있다.

---
