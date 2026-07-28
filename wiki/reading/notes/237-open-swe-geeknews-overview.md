---
type: Reference
title: "Open SWE 핵심 패턴: 격리·선별된 도구·풍부한 시작 맥락"
description: "사내 coding agent들이 공통으로 채택한 production architecture를 정리한 GeekNews 문서"
resource: https://news.hada.io/topic?id=27604
notion: https://app.notion.com/p/76f1a73cf20b83669cbc81f9241d3cf3
tags: [reading, ai-agents, ai-coding, internal-tools]
timestamp: 2026-07-24
status: summarized
---

# 공통 패턴

Stripe, Ramp와 Coinbase의 사내 coding agent는 독립적으로 만들어졌지만 비슷한 구조로 수렴했다. 각 task를 cloud sandbox에 격리하고, 관리되는 tool set을 주며, Slack·Linear·GitHub에서 풍부한 context를 받아 시작하고, 복잡한 일은 isolated subagent에 나눈다.

# Open SWE의 구현

Open SWE는 Deep Agents와 LangGraph 위에 이 구조를 composition한다. repository의 `AGENTS.md`와 issue·thread·PR context를 합치고, file·shell·web·PR·comment tool을 제공한다. model 판단이 필요한 orchestration과 반드시 실행돼야 하는 message injection·PR 생성 같은 middleware를 분리한다.

# 조직 도입 포인트

agent core를 fork하기보다 model, sandbox, tool, trigger, prompt와 middleware를 plugin처럼 교체해 upgrade 경로를 남긴다. “많은 tool”보다 owner와 test가 있는 curated tool이 중요하다. 자세한 원문 중심 정리는 [Open SWE 사내 coding agent framework](238-open-swe-internal-coding-agents.md)에 연결했다.

# 출처

- [GeekNews 정리와 토론](https://news.hada.io/topic?id=27604)

