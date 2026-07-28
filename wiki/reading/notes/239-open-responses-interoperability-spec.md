---
type: Reference
title: "Open Responses: 여러 LLM의 메시지·도구·stream을 잇는 공통 규격"
description: "OpenAI Responses API 형태를 바탕으로 provider 간 agent request와 event lifecycle을 표준화하는 schema"
resource: https://news.hada.io/topic?id=25898
notion: https://app.notion.com/p/59f1a73cf20b83dca74601791612ba2b
tags: [reading, llm-api, interoperability, ai-agents]
timestamp: 2026-07-24
status: summarized
---

# 해결하려는 문제

LLM provider는 message, multimodal input, tool call과 streaming을 비슷하게 지원하지만 payload와 event 표현이 다르다. Open Responses는 공통 request·response schema로 provider 전환과 agent framework의 중복 adapter를 줄이려 한다.

# 주요 설계

- message, reasoning state와 tool call을 모두 `item` 단위로 표현한다.
- response와 item에 `in_progress`, `completed`, `failed`, `incomplete` lifecycle을 둔다.
- streaming을 text delta뿐 아니라 item added·delta·done 같은 semantic event로 정의한다.
- 외부 실행 tool과 provider-hosted tool을 구분하고 `allowed_tools`로 범위를 제한한다.
- 공통화하기 어려운 기능은 provider prefix extension으로 남긴다.
- structured error와 failed event로 stream 중 실패도 기록한다.

# 기대와 한계

공통 schema는 logging, replay, model routing과 vendor 교체를 쉽게 하지만 provider 고유 기능을 완전히 동일하게 만들지는 못한다. reasoning visibility, server-side state, token accounting와 hosted tool semantics가 다르면 adapter와 capability negotiation이 여전히 필요하다. specification version을 고정하고 round-trip test를 마련해야 한다.

# 출처

- [GeekNews 정리](https://news.hada.io/topic?id=25898)

