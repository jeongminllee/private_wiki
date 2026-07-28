---
type: Reference
title: "Ollama 비판과 대안: 편의성 뒤의 attribution·호환성·cloud 경계"
description: "llama.cpp 의존 역사, model naming과 registry 설계를 비판하고 직접 engine과 다른 local LLM 도구를 제안한 의견 글"
resource: "https://sleepingrobots.com/dreams/stop-using-ollama/"
notion: "https://app.notion.com/p/44f1a73cf20b82ea96dd8126e4a70f6c"
tags: [reading, local-llm, ollama, open-source]
timestamp: 2026-07-24
status: summarized
---

# 글의 주장

이 글은 Ollama가 `llama.cpp`를 쉽게 쓰게 만든 공로는 있지만, upstream attribution, backend 품질, model naming, closed-source GUI와 cloud 전환에서 신뢰를 잃었다고 강하게 비판한다. 초기 binary의 MIT notice와 README 인정을 늦게 처리했고, 이후 `ggml` 위에 자체 backend를 만들면서 structured output, vision과 새 tensor type 관련 문제가 다시 생겼다는 사례를 든다.

또 `deepseek-r1` 같은 짧은 이름이 실제 671B 원본이 아니라 작은 distill model을 받아 오게 해 사용자가 무엇을 실행하는지 혼동한다고 지적한다. GGUF에 이미 chat template과 metadata가 있는데 별도 Modelfile과 registry를 끼워 넣어 template 변환, quantization 선택과 파일 재사용이 불편해졌다는 비판도 한다.

# 대안

- `llama.cpp`: GGUF를 직접 실행하며 OpenAI 호환 `llama-server`와 web UI를 제공한다.
- `llamafile`: 모델과 runtime을 하나의 실행 파일로 묶는다.
- `llama-swap`과 LiteLLM: 여러 local model의 load·unload와 endpoint routing을 분리한다.
- Jan, KoboldCpp: source가 공개된 desktop·web UI 대안이다.
- LM Studio, Msty: proprietary이지만 편리한 GUI를 제공한다.
- RamaLama: container 중심 model runner다.

# 균형 있게 적용하기

이 글은 중립 비교 보고서가 아니라 “Ollama를 쓰지 말라”는 입장이 분명한 의견 글이다. 인용된 성능 차이도 서로 다른 community 환경에 기반하므로 같은 hardware, model file, context와 batch에서 재측정해야 한다. Ollama의 단일 명령 UX, 넓은 integration과 팀의 기존 자동화 비용도 실제 선택 기준이다.

다만 local이라고 믿은 요청이 cloud로 가는지, 정확히 어떤 model·quantization을 실행하는지, upstream license notice가 유지되는지는 도구와 무관하게 반드시 확인할 좋은 체크리스트다.

# 출처

- [Friends Don't Let Friends Use Ollama](https://sleepingrobots.com/dreams/stop-using-ollama/)
