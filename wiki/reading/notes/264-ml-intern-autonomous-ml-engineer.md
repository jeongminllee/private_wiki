---
type: Reference
title: "ML Intern: 논문 조사부터 학습·배포까지 수행하는 Hugging Face 에이전트"
description: "Hugging Face 도구와 compute를 연결한 autonomous ML workflow, 승인 경계와 trace privacy"
resource: https://discuss.pytorch.kr/t/ml-intern-hugging-face-ml/10192
notion: https://app.notion.com/p/3611a73cf20b81a48a8af16dc1c0327c
tags: [reading, ai-agent, machine-learning, hugging-face]
timestamp: 2026-07-24
status: summarized
---

# 역할

ML Intern은 자연어로 받은 ML task를 조사하고 code를 작성해 model을 학습·평가·배포하는 오픈소스 agent다. Hugging Face의 docs, paper, model, dataset, Hub repository와 cloud compute를 tool로 연결한다.

# 실행 구조

Agent loop는 model이 tool call을 만들면 approval 여부를 확인하고, `ToolRouter`가 실행한 결과를 context에 넣어 다음 판단을 반복한다. 반복된 tool pattern을 감지하는 doom-loop detector와 context manager가 포함된다.

Hosted model은 Hugging Face Inference Providers를 통해 쓰고, Ollama·vLLM·LM Studio·llama.cpp 같은 OpenAI-compatible local endpoint도 LiteLLM으로 연결한다. 기본 local tool runtime은 현재 filesystem에서 `bash`, read, write와 edit를 실행하며 `--sandbox-tools`를 주면 private HF Space sandbox를 사용한다. License는 Apache-2.0이다.

# 설치와 사용

```bash
git clone git@github.com:huggingface/ml-intern.git
cd ml-intern
uv sync
uv tool install -e .
ml-intern "fine-tune llama on my dataset"
```

Hub 작업에는 `HF_TOKEN`, GitHub 작업에는 제한된 `GITHUB_TOKEN`이 필요하다.

# 운영상 중요한 점

Headless mode는 tool 실행을 자동 승인할 수 있으므로 처음부터 중요한 repository나 고비용 GPU job에 연결하면 안 된다. Budget, iteration limit, sandbox, dataset license와 model evaluation gate를 먼저 둬야 한다.

Session trace는 기본적으로 사용자 소유의 private Hugging Face dataset에 upload된다. `share_traces: false`로 끌 수 있지만, 민감 prompt·path·data가 들어가는 환경에서는 시작 전에 설정과 telemetry를 확인해야 한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/ml-intern-hugging-face-ml/10192)
- [공식 저장소](https://github.com/huggingface/ml-intern)

