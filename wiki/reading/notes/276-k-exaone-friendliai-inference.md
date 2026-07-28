---
type: Reference
title: "K-EXAONE 236B-A23B를 hosted·self-hosted inference로 쓰는 기준"
description: "FriendliAI endpoint와 공식 model card에서 확인한 K-EXAONE의 규모, reasoning·tool use와 배포 요구"
resource: https://friendli.ai/model/LGAI-EXAONE/K-EXAONE-236B-A23B
notion: https://app.notion.com/p/ee01a73cf20b8376ae9f01163994a9a3
tags: [reading, k-exaone, inference, llm]
timestamp: 2026-07-24
status: summarized
---

# 모델

LG AI Research의 K-EXAONE은 236B 전체 parameter 중 inference마다 23B가 활성화되는 multilingual MoE model이다. Reasoning·non-reasoning mode, long context와 OpenAI·Hugging Face 형식의 tool calling을 지원한다.

# 두 사용 경로

저장된 FriendliAI page는 model을 직접 운영하지 않고 low-latency hosted API와 dedicated endpoint로 쓰는 경로다. Hardware provisioning, autoscaling과 serving update를 provider가 맡는 대신 price, data policy, region과 rate limit을 확인해야 한다.

직접 배포할 때는 FP8 model과 vLLM 0.14 이상을 사용할 수 있다. 공식 card의 예시는 256K context를 tensor parallel 2개의 H200에서 serving하며, SGLang 경로는 4개 H200 예시를 든다. 이는 권장 예시이지 모든 context·batch에서 필요한 최소 hardware를 보장하는 수치는 아니다.

# 실행 특성

- `enable_thinking=True`가 기본 reasoning mode
- Latency가 중요하면 `enable_thinking=False`
- 권장 sampling은 `temperature=1.0`, `top_p=0.95`
- MTP weight를 활용한 speculative decoding 경로
- TensorRT-LLM, vLLM과 SGLang 지원

# 검토할 점

FriendliAI의 marketing 성능 표현과 model benchmark는 실제 Korean task set에서 재검증해야 한다. Hosted와 self-hosted를 비교할 때 token 가격만 보지 말고 concurrency, time-to-first-token, data retention, GPU utilization과 운영 인력을 포함한다. Model은 별도의 K-EXAONE AI Model License를 쓰므로 MIT 같은 일반 open-source license로 가정하면 안 된다.

# 출처

- [FriendliAI model endpoint](https://friendli.ai/models/LGAI-EXAONE/K-EXAONE-236B-A23B)
- [공식 FP8 model card](https://huggingface.co/LGAI-EXAONE/K-EXAONE-236B-A23B-FP8)

