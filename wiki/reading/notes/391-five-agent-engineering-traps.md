---
type: Reference
title: "전통적 개발 습관이 AI agent 설계를 막는 다섯 지점"
description: "자연어 state, model 주도 control flow, error recovery, eval과 agent 친화 API를 강조하는 agent engineering 관점"
resource: "https://aisparkup.com/posts/7049"
notion: "https://app.notion.com/p/fb61a73cf20b837ead5b81e1e25c53f8"
tags: [reading, ai-agent, architecture, evaluation, api-design]
timestamp: 2026-07-24
status: summarized
---

# 다섯 가지 전환

1. 복잡한 사용자 의도와 preference를 boolean field로 지나치게 압축하지 말고 원래 text를 state로 보존한다.
2. 모든 branch를 code로 hard-code하기보다 model이 현재 context와 tool을 보고 다음 action을 고르게 한다.
3. Tool error를 즉시 전체 실패로 만들지 말고 agent가 읽어 retry, 수정 또는 사용자 질문으로 복구할 수 있는 observation으로 돌려준다.
4. 하나의 정답이 없는 behavior는 unit test만으로 평가하지 말고 여러 run의 reliability, quality rubric과 intermediate trace를 본다.
5. Agent가 쓰는 API에는 모호한 `id`보다 의미 있는 field name, 상세 docstring, 명시적 error와 permission을 제공한다.

# 균형 있게 적용하기

글의 “제어권을 넘겨라”는 safety constraint까지 없애라는 뜻으로 적용하면 위험하다. 결제, 삭제, 권한 변경과 규제 판단은 deterministic policy와 human approval로 감싸야 한다. 자연어 state도 검색·감사·schema migration이 필요한 핵심 record를 모두 대체하지 않는다.

Unit test와 eval 역시 대체 관계가 아니다. Deterministic tool code는 unit·integration test로, model behavior는 fixed evaluation set, repeated trial과 human rubric으로 검증한다. Error recovery에는 retry budget, idempotency와 escalation 조건이 필요하다.

# 출처

- [AI Sparkup 한국어 정리](https://aisparkup.com/posts/7049)
- [Philipp Schmid 원문](https://www.philschmid.de/why-engineers-struggle-to-build-ai-agents)
