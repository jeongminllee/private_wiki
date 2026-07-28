---
type: Reference
title: "Mistral Vibe: plan·subagent·skill·MCP를 갖춘 open-source coding CLI"
description: "Mistral model로 codebase 탐색·수정·shell 실행을 수행하고 권한 수준을 agent profile로 분리하는 도구"
resource: https://github.com/mistralai/mistral-vibe
notion: https://app.notion.com/p/0fa1a73cf20b820ab5c7818380389398
tags: [reading, ai-coding, cli, mistral]
timestamp: 2026-07-24
status: summarized
---

# 기능

Mistral Vibe는 Mistral이 공개한 command-line coding assistant다. 자연어 대화에서 file read·write·patch, shell, recursive code search, todo와 git 작업을 실행한다. Project tree와 Git status를 읽어 context를 만들고 image attachment, slash command, session, custom system prompt와 MCP server를 지원한다.

복잡한 탐색은 독립 context의 `explore` subagent에 위임할 수 있다. Skill은 project 또는 user directory에 재사용 지침과 custom command를 두는 방식이다. Tool 실행 중 요구사항이 불명확하면 선택지를 제시하는 interactive question 기능도 갖는다.

# 권한 profile

`default`는 tool 실행마다 승인을 요구하고, `plan`은 read-only 탐색, `accept-edits`는 file edit만 자동 승인한다. `auto-approve`는 모든 tool을 허용하므로 격리된 disposable workspace가 아니라면 피해야 한다. Folder trust와 tool permission은 단순 UI 옵션이 아니라 repository의 credential과 shell 권한 경계다.

# 설치와 선택 기준

`uv tool install mistral-vibe` 또는 `pip install`로 설치하며 Apache-2.0 license다. Windows에서도 동작하지만 공식 target과 지원 우선순위는 UNIX 환경이라고 명시한다. Windows에서는 path, shell command와 PTY 동작을 작은 repository에서 먼저 확인한다.

장점은 Mistral model을 중심으로 agent harness 전체를 공개 code로 검토할 수 있다는 점이다. 다만 “open source CLI”와 사용하는 model endpoint·비용·data policy는 별개다. `config.toml`의 provider, API key storage, telemetry·data collection 설정과 실제 outbound request를 확인해야 한다.

# 출처

- [Mistral Vibe 저장소](https://github.com/mistralai/mistral-vibe)

