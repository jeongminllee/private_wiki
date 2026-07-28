---
type: Reference
title: "OpenCode에서 로컬·저가 LLM을 섞어 쓰는 비용 절감 전략"
description: "Ollama, Qwen, GLM, DeepSeek와 MiniMax를 작업 난도에 따라 전환하는 설정·비용·hardware guide"
resource: https://goddaehee.tistory.com/488
notion: https://app.notion.com/p/df51a73cf20b83a4bb1081154755bd82
tags: [reading, local-llm, opencode, cost-optimization]
timestamp: 2026-07-24
status: summarized
---

# 핵심 전략

모든 coding task에 가장 비싼 model을 쓰지 않고 local·저가 model을 기본으로 두며 어려운 refactoring과 final review에만 stronger hosted model을 사용한다. OpenCode처럼 provider 전환이 쉬운 harness는 task별 routing으로 비용, privacy와 vendor dependence를 조절할 수 있다.

# 선택 기준

- boilerplate, 검색, format과 작은 수정은 빠르고 저렴한 model
- architecture, 복잡한 debug와 security review는 강한 model
- 민감 code는 local inference 또는 enterprise data policy가 확인된 endpoint
- offline 작업은 Ollama 등 local runtime

local model도 hardware 구매, 전력, setup, update와 느린 prompt processing 비용이 있다. “무료”는 API bill이 없다는 뜻이지 총비용이 0이라는 뜻은 아니다.

# 가격표와 설정을 읽는 법

글은 Qwen3, GLM-4.7, DeepSeek, MiniMax M2.1과 여러 plan의 당시 가격·무료 quota를 비교한다. 가격, model 이름, context와 rate limit은 자주 변하므로 문서의 숫자를 현재 견적으로 사용하면 안 된다. provider 공식 price page에서 input·cached input·output을 다시 확인하고 실제 repository의 token trace로 월 비용을 계산해야 한다.

# 품질 관리

model별 동일 task set으로 test pass rate, edit churn, latency, hallucinated API와 비용을 기록한다. 작은 model의 결과를 그대로 merge하기보다 deterministic test와 선택적 stronger-model review를 결합하는 것이 현실적이다.

# 출처

- [Open Code 리뷰(3)](https://goddaehee.tistory.com/488)

