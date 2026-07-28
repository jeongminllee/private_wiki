---
type: Reference
title: "Pi의 미니멀 에이전트 철학: 기능은 코드로 확장한다"
description: "네 가지 기본 도구와 tree session, hot reload를 중심으로 한 확장 가능한 coding agent 분석"
resource: https://news.hada.io/topic?id=26298
notion: https://app.notion.com/p/1c11a73cf20b82268a84014db8dde3f7
tags: [reading, ai-agents, coding-agent, pi]
timestamp: 2026-07-24
status: summarized
---

# 핵심 철학

Pi는 `read`, `write`, `edit`, `bash` 네 도구와 짧은 system prompt만 제공하고, 필요한 기능은 agent가 extension code를 작성해 추가하게 한다. 많은 protocol과 내장 기능을 넣기보다 LLM이 이미 잘하는 code 작성·실행을 확장 메커니즘으로 삼는다.

# 설계 특징

- session을 tree로 저장해 옆 branch에서 도구를 만들거나 조사한 뒤 요약만 본류로 가져온다.
- 여러 model provider를 같은 session에서 바꿔 쓸 수 있다.
- extension이 custom message와 disk state를 가질 수 있다.
- agent가 extension code를 고치면 hot reload로 즉시 시험할 수 있다.
- MCP를 core에 넣지 않고 필요할 때 CLI bridge나 직접 작성한 skill로 연결한다.

# 의미와 위험

작은 core는 context와 동작을 관찰하고 고치기 쉽다. 반면 agent가 자신의 실행 코드를 즉석에서 확장하는 방식은 supply-chain과 self-modification 위험을 키운다. extension source review, isolated workspace, command log와 version control 없이는 편의성이 통제력을 앞설 수 있다.

# 출처

- [GeekNews 정리](https://news.hada.io/topic?id=26298)

