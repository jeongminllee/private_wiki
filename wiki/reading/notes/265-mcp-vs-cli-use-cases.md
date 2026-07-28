---
type: Reference
title: "MCP와 CLI는 대체 관계가 아니라 운영 범위가 다른 tool interface"
description: "개인 local 작업과 조직용 remote tool distribution에서 CLI·MCP의 trade-off를 나눈 글"
resource: https://news.hada.io/topic?id=27530
notion: https://app.notion.com/p/27c1a73cf20b82b5b73101b19a70f87b
tags: [reading, mcp, cli, agent-tools]
timestamp: 2026-07-24
status: summarized
---

# 논지

“MCP는 죽고 CLI가 이긴다”는 주장은 서로 다른 배포 문제를 하나로 묶는다. 글은 local `stdio` MCP와 remote Streamable HTTP MCP를 구분하고, 개인 개발자의 local tool에는 CLI가 단순할 수 있지만 조직의 중앙 tool·knowledge 배포에는 MCP의 가치가 남는다고 주장한다.

# CLI가 잘 맞는 경우

- 이미 안정적인 command와 structured output이 있음
- 한 사람 또는 한 repository 안에서 local execution
- Shell pipeline, debugging과 version pinning이 중요함
- Agent 전용 server를 운영할 이유가 적음

# Remote MCP가 주는 것

- OAuth로 사용자 identity를 확인하고 backend secret을 감춤
- 중앙 server에서 rate limit, audit와 OpenTelemetry 수집
- Client를 일일이 update하지 않고 tool behavior를 배포
- Prompts와 Resources로 현재 조직 지식·문서를 동적으로 제공
- 여러 agent frontend에 동일한 contract를 제공

# 선택 기준

Protocol 이름보다 trust boundary와 lifecycle을 먼저 그려야 한다. Local process를 감싸는 MCP가 단순 CLI보다 불필요한 overhead일 수 있고, 반대로 모든 개발자에게 API key를 나눠주는 CLI wrapper는 enterprise 보안에 불리할 수 있다.

MCP를 쓴다고 authentication, schema 품질이나 observability가 자동으로 생기는 것은 아니다. CLI도 remote execution service 안에 배치하면 비슷한 중앙 통제를 만들 수 있다. Distribution, compatibility, permission과 telemetry 비용을 비교해 더 작은 운영면을 선택하는 것이 핵심이다.

# 출처

- [GeekNews 요약과 토론](https://news.hada.io/topic?id=27530)

