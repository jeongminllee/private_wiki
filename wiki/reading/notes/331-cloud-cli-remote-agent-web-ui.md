---
type: Project
title: "Cloud CLI: coding agent를 원격에서 관리하는 Web UI"
description: "Claude Code·Cursor CLI·Codex session에 chat, terminal, file, Git UI를 제공하는 open-source PWA"
resource: "https://news.hada.io/topic?id=26379"
notion: "https://app.notion.com/p/27b1a73cf20b826486c601df2d39db0e"
tags: [reading, ai-agent, remote-development, security, open-source]
timestamp: 2026-07-24
status: summarized
---

# 무엇인가

siteboon의 Cloud CLI는 desktop과 mobile browser에서 Claude Code, Cursor CLI와 Codex session을 관리하는 GPL-3.0 project다. React·Vite frontend와 Node·Express backend를 사용하며 PWA로 설치할 수 있다.

# 기능

Chat과 WebSocket 실시간 응답, shell terminal, file explorer와 CodeMirror editor, Git staging·commit·branch UI, session history와 동시 session을 제공한다. MCP와 TaskMaster AI를 선택적으로 연결할 수 있다. Claude Code 도구는 기본적으로 모두 비활성화되어 사용자가 허용 범위를 정한다.

# 보안 판단

이 UI는 편의 도구인 동시에 shell, source code, Git credential과 agent 권한을 network에 노출할 수 있는 관리 surface다. Public internet에 그대로 열지 말고 강한 인증, TLS, private network/VPN, origin·CSRF 방어, session 만료, audit log와 least privilege를 적용한다. 실행 account도 host의 중요 credential과 분리한다.

# 활용

긴 agent 작업을 mobile에서 확인하거나 여러 session을 한곳에서 관리할 때 유용하다. 도입 전에는 project의 인증 구현, update 속도, command authorization과 장애 시 session 복구를 직접 시험한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=26379)
