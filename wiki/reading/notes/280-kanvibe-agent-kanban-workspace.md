---
type: Reference
title: "KanVibe: worktree와 agent terminal을 묶는 keyboard-first Kanban"
description: "병렬 coding agent의 branch·terminal·상태·diff를 한 board에서 관리하는 self-hosted workspace"
resource: https://news.hada.io/topic?id=26737
notion: https://app.notion.com/p/58a1a73cf20b8247af4a8112fee0d50a
tags: [reading, ai-coding, kanban, git-worktree]
timestamp: 2026-07-24
status: summarized
---

# 해결하는 문제

여러 coding agent를 branch와 terminal session별로 동시에 실행하면 누가 작업 중인지, 질문을 기다리는지, review가 필요한지 확인하기 어렵다. KanVibe는 task card, Git worktree와 tmux·zellij session을 하나로 묶는다.

# Workflow

Board는 `TODO → PROGRESS → PENDING → REVIEW → DONE` 다섯 상태를 쓴다. Branch 이름으로 task를 만들면 worktree와 terminal session이 생성되고, card를 열면 xterm.js 기반 terminal·metadata·chat·PR action과 code diff를 볼 수 있다.

Claude Code, Gemini CLI, Codex CLI와 OpenCode hook이 prompt 시작, approval·질문 대기와 응답 완료 event를 받아 card 상태를 바꾼다. 현재 공식 저장소는 browser뿐 아니라 Electron desktop app, keyboard search, Vim-style navigation과 여러 terminal pane layout도 제공한다.

# 주의할 동작

`DONE`으로 옮기면 branch, worktree와 terminal session을 자동 삭제한다. Review 전 자동 이동이 일어나지 않도록 permission과 confirmation을 확인하고, uncommitted file과 remote branch가 안전한지 test repository에서 먼저 검증해야 한다.

Browser terminal과 SSH support는 편리하지만 web app compromise가 shell access로 이어질 수 있다. Local bind address, authentication, WebSocket, SSH key와 reverse proxy를 점검한다. License는 AGPL-3.0이며 공식 README의 “commercial SaaS distribution 불가” 해석은 실제 license text와 필요시 법률 검토를 우선해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=26737)
- [KanVibe 저장소](https://github.com/rookedsysc/kanvibe)
