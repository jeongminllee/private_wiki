---
type: Reference
title: "OpenJarvis: 로컬 우선 개인 AI 플랫폼"
description: "모델·추론 엔진·에이전트·도구·메모리·학습을 교체 가능한 층으로 구성한 오픈소스 시스템"
resource: https://openjarvis.stanford.edu/
notion: https://app.notion.com/p/0d31a73cf20b821c873e01abe2bd2f65
tags: [reading, local-ai, ai-agent, open-source]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

OpenJarvis는 개인 AI를 특정 모델이나 클라우드 API에 묶지 않고 로컬 하드웨어에서 운영할 수 있게 만든 오픈소스 플랫폼이다. `Intelligence`, `Engine`, `Agents`, `Tools & Memory`, `Learning`의 다섯 primitive를 교체 가능한 층으로 나눈다.

# 구성

- Ollama, vLLM, SGLang, llama.cpp와 cloud backend를 선택할 수 있다.
- Apple Silicon, NVIDIA·AMD GPU, NPU와 CPU 등 여러 하드웨어를 대상으로 한다.
- agent가 web, code, retrieval와 MCP tool을 사용하고 장기 memory를 연결할 수 있다.
- workload와 장치 조건에 맞는 model·engine 조합을 찾는 specification search를 제안한다.

# 논문의 주장

논문은 cloud model을 단순히 local model로 바꾸면 평가 점수가 25~39 percentage point 하락할 수 있다고 보고한다. 반면 조합을 탐색하면 8개 benchmark 중 4개에서 cloud baseline과 같거나 높고, 평균 차이는 3.2 point 이내였으며 API 비용과 latency도 크게 줄었다고 주장한다. 이 수치는 해당 benchmark와 설정 안의 결과이지 모든 업무에 그대로 적용되는 보장은 아니다.

# 운영 시 주의

`local-first`가 자동으로 `local-only`를 뜻하지 않는다. cloud backend, web tool이나 외부 MCP를 쓰면 데이터가 장치 밖으로 나갈 수 있다. tool 권한, secret 저장, prompt injection, sandbox, model license와 hardware별 재현성을 별도로 점검한다.

# 출처

- [OpenJarvis 공식 사이트](https://openjarvis.stanford.edu/)
- [GitHub 저장소](https://github.com/open-jarvis/OpenJarvis)
- [논문](https://arxiv.org/abs/2605.17172)
- [Notion 원본 항목](https://app.notion.com/p/0d31a73cf20b821c873e01abe2bd2f65)
