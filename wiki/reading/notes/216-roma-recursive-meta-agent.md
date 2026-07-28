---
type: Reference
title: "ROMA: 복잡한 일을 재귀적으로 분해하고 다시 합치는 Meta-Agent"
description: "장기 작업을 tree 형태로 분해·병렬 실행하고 결과를 상향 통합하는 DSPy 기반 multi-agent framework"
resource: https://discuss.pytorch.kr/t/roma-recursive-open-meta-agent/8691
notion: https://app.notion.com/p/eb11a73cf20b8240afa681039ff36eb5
tags: [reading, ai-agents, multi-agent, orchestration]
timestamp: 2026-07-24
status: summarized
---

# 핵심 구조

ROMA(Recursive Open Meta-Agent)는 요청을 하나의 node로 보고 바로 실행할 수 있을 때까지 재귀적으로 하위 작업으로 나눈다. leaf node의 실행 결과는 아래에서 위로 합쳐져 최종 답이 된다. 긴 chain 하나에 모든 문맥을 넣는 대신 필요한 context를 task tree 안에서 제한하려는 접근이다.

# 주요 모듈

- **Atomizer**: 요청이 atomic task인지 계획이 필요한지 판단한다.
- **Planner**: 복잡한 일을 더 작은 subtask로 분해한다.
- **Executor**: LLM과 외부 tool로 leaf task를 실행한다.
- **Aggregator**: 여러 결과를 상위 문맥에 맞게 통합한다.
- **Verifier**: 선택적으로 최종 결과가 원래 요청을 충족하는지 검사한다.

Python, Pydantic와 DSPy를 중심으로 하고 FastAPI, PostgreSQL, MinIO, MLflow와 E2B sandbox를 조합할 수 있다.

# 평가와 주의점

소개 글은 ROMA Search가 복합 web research를 평가하는 SEAL-0에서 45.6%를 기록했다고 전한다. 이 결과가 다른 종류의 coding·workflow 성능을 보장하지는 않는다. 재귀 분해는 병렬성을 높이지만 node 수, token 비용, 중복 조사와 잘못된 상위 aggregation도 늘릴 수 있으므로 최대 깊이, budget, dependency와 provenance를 명시적으로 추적해야 한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/roma-recursive-open-meta-agent/8691)
- [sentient-agi/ROMA](https://github.com/sentient-agi/ROMA)

