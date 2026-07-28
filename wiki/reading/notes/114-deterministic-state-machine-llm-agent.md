---
type: Reference
title: "상태머신 기반 결정론적 LLM 에이전트"
description: "LLM은 의도 분류에만 쓰고 상태 전이와 실행을 규칙으로 통제하는 실험적 에이전트 구조"
resource: https://news.hada.io/topic?id=25710
notion: https://app.notion.com/p/b711a73cf20b828ca708813de184f784
tags: [reading, llm-agent, state-machine, deterministic-system]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

이 데모는 LLM이 직접 상태를 바꾸거나 행동을 실행하지 않게 제한한다. LLM은 사용자 입력을 정해진 intent로 분류하고, 실제 전이는 state machine의 규칙이 결정한다. 생성 모델의 유연한 언어 이해와 결정론적 실행 경계를 분리하려는 실험이다.

# 구조

- 사용자 상태는 서버 대신 browser IndexedDB에 저장한다.
- intent와 현재 state가 허용된 transition을 만족할 때만 동작한다.
- memory는 ant colony algorithm에서 착안한 reinforcement와 decay로 기억과 망각을 표현한다.
- 기본 server 호출 외에 사용자의 API key나 Ollama 같은 local model을 선택할 수 있다.

# 장점

허용된 상태와 전이를 audit하기 쉽고, LLM의 임의 tool call 범위를 줄인다. 동일한 state와 intent에서 같은 결과를 기대할 수 있어 테스트가 명확해진다. 중요한 업무에서는 `LLM 판단 -> 검증된 command` 경계를 설계하는 참고 사례가 된다.

# 한계와 보완

intent classification 자체는 여전히 틀릴 수 있고, IndexedDB는 backup·동기화·암호화를 자동 보장하지 않는다. 외부 side effect에는 idempotency key, authorization, transaction과 rollback이 필요하다. 현재는 소규모 연구·데모이므로 복잡한 장기 workflow의 동시성, migration과 recovery를 별도로 검증해야 한다.

# 출처

- [GeekNews 프로젝트 소개](https://news.hada.io/topic?id=25710)
- [백서 저장소](https://github.com/manifesto-ai/mind-protocol-whitepaper)
- [Notion 원본 항목](https://app.notion.com/p/b711a73cf20b828ca708813de184f784)
