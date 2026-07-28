---
type: Reference
title: "Hermes Agent: 사용 경험을 skill로 축적하는 개인 AI 에이전트"
description: "Nous Research Hermes Agent의 학습 loop, 배포 형태와 장기 기억을 검토한 정리"
resource: https://github.com/nousresearch/hermes-agent
notion: https://app.notion.com/p/1e51a73cf20b834b9d0901db9e62160e
tags: [reading, ai-agent, memory, open-source]
timestamp: 2026-07-24
status: summarized
---

# 핵심 아이디어

Nous Research의 Hermes Agent는 단발성 chat보다 사용자와 함께 장기간 쓰이는 personal agent를 목표로 한다. 작업 중 얻은 절차를 skill로 만들고, 과거 대화를 검색하며, 세션을 넘어 사용자에 대한 model을 축적하는 built-in learning loop가 특징이다.

# 구성과 실행

저장소에는 agent loop, tool, skill, provider, gateway, cron, web UI와 terminal UI가 함께 들어 있다. optional MCP와 skill을 붙일 수 있고, Telegram 같은 message channel과 연결하거나 VPS, GPU server 및 serverless 환경에 배포할 수 있다. CJK 검색을 위한 SQLite FTS5 관련 구성도 포함되어 있다.

# “자기 개선”의 실제 의미

여기서 개선은 model weight를 계속 재학습한다는 뜻이라기보다, 성공한 workflow를 재사용 가능한 skill과 memory로 외부화하는 데 가깝다. agent가 과거 경험을 찾고 다음 작업에 적용하면 반복 setup을 줄일 수 있지만, 잘못 학습한 절차도 함께 고착될 수 있다.

# 운영할 때 볼 것

- 생성된 skill을 누가 검토하고 versioning하는가
- memory에 개인정보·secret이 들어갈 때 retention과 삭제가 가능한가
- Telegram·gateway·cron의 authentication과 external action 권한이 충분히 제한되는가
- remote model provider로 전송되는 context의 범위가 무엇인가
- update 후 기존 skill과 tool contract가 계속 호환되는가

항상 실행되는 agent는 편의성만큼 권한 관리가 중요하다. 처음에는 isolated account와 제한된 tool set으로 운영하고, skill·memory diff를 검토하는 방식이 적절하다.

# 출처

- [NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent)

