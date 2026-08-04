---
type: Concept
title: "Triton 커널 JIT 경고"
description: "ML - LLM Serving & Inference - ChatGPT 대화 추출 노트 (2026-05-22)"
tags: [ml, chatgpt-export]
timestamp: 2026-05-22
status: active
---

# Triton 커널 JIT 경고

> **카테고리**: `ML - LLM Serving & Inference`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-22

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
(EngineCore pid=9738) WARNING 05-22 12:30:11 [jit_monitor.py:103] Triton kernel JIT compilation during inference: _compute_slot_mapping_kernel. This causes a latency spike; consider extending warmup to cover this shape/config.
(APIServer pid=9446) INFO:     127.0.0.1:53002 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=9446) INFO 05-22 12:30:17 [loggers.py:271] Engine 000: Avg prompt throughput: 253.9 tokens/s, Avg generation throughput: 32.6 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
(APIServer pid=9446) INFO 05-22 12:30:27 [loggers.py:271] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%

### 💡 답변 (Assistant)
이 로그는 **정상 동작에 가깝습니다.** 에러라기보다는 vLLM/서빙 엔진이 “첫 요청에서 특정 커널을 JIT 컴파일하느라 순간 지연이 있었다”고 알려주는 경고입니다.

핵심은 이 부분입니다.

```text
WARNING ... Triton kernel JIT compilation during inference:
_compute_slot_mapping_kernel.
This causes a latency spike; consider extending warmup to cover this shape/config.
```

의미는 다음과 같습니다.

vLLM 내부에서 **Triton 커널**을 사용합니다. Triton 커널은 GPU에서 빠르게 실행되도록 컴파일되는 작은 연산 코드라고 보면 됩니다. 그런데 어떤 입력 길이, batch 크기, KV cache 구성 같은 **특정 shape/config**가 처음 등장하면, 이미 컴파일된 커널이 없어서 추론 중에 즉석으로 컴파일합니다.

그래서 첫 요청 또는 새로운 형태의 요청에서 잠깐 느려질 수 있습니다.

```text
POST /v1/chat/completions HTTP/1.1" 200 OK
```

이건 요청이 정상적으로 처리됐다는 뜻입니다. HTTP 200이므로 API 응답은 성공했습니다.

아래 로그도 정상입니다.

```text
Avg prompt throughput: 253.9 tokens/s
Avg generation throughput: 32.6 tokens/s
Running: 0 reqs, Waiting: 0 reqs
GPU KV cache usage: 0.0%
Prefix cache hit rate: 0.0%
```

해석하면:

| 항목 | 의미 |
|---|---|
| Avg prompt throughput: 253.9 tokens/s | 프롬프트 입력 처리 속도 |
| Avg generation throughput: 32.6 tokens/s | 답변 생성 속도 |
| Running: 0 reqs | 현재 처리 중인 요청 없음 |
| Waiting: 0 reqs | 대기 중인 요청 없음 |
| GPU KV cache usage: 0.0% | 현재 KV cache를 점유한 활성 요청 없음 |
| Prefix cache hit rate: 0.0% | 재사용된 프롬프트 prefix cache 없음 |

마지막 로그에서 throughput이 0으로 나오는 것도 정상입니다.

```text
Avg prompt throughput: 0.0 tokens/s
Avg generation throughput: 0.0 tokens/s
Running: 0 reqs
Waiting: 0 reqs
```

이건 **그 시간 구간에 요청이 없었다**는 뜻입니다. GPU가 계속 일을 안 하는 것처럼 보이는 이유도 이 때문입니다. LLM 서버는 요청이 들어올 때만 GPU를 쓰고, 요청이 끝나면 대기 상태가 됩니다.

정리하면:

```text
문제 없음.
첫 요청/새로운 입력 형태에서 Triton JIT 컴파일 때문에 순간 지연 발생.
API 응답은 정상 성공.
이후 요청이 없어서 throughput과 KV cache 사용량이 0으로 표시됨.
```

줄이고 싶다면 서버 시작 후에 **warmup 요청**을 몇 번 날리면 됩니다. 예를 들어 실제로 자주 쓸 입력 길이와 max_tokens 설정으로 미리 호출해두면, 실사용 첫 요청에서 JIT 지연이 덜합니다.

예시:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "사용중인_모델명",
    "messages": [
      {"role": "user", "content": "warmup test"}
    ],
    "max_tokens": 128
  }'
```

긴 프롬프트도 자주 쓴다면 이런 식으로 한 번 더 워밍업하는 게 좋습니다.

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "사용중인_모델명",
    "messages": [
      {"role": "user", "content": "다음은 긴 입력에 대한 warmup입니다. 이 문장을 여러 번 반복해서 실제 사용 길이와 비슷하게 만듭니다."}
    ],
    "max_tokens": 512
  }'
```

즉, 지금 로그는 **“서버가 잘 돌고 있고, 첫 추론에서 GPU 커널 컴파일이 발생했다”** 정도로 보면 됩니다.

---
