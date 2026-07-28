---
type: Setup Guide
title: "iTerm2와 tmux에서 Claude Code Agent Teams 운영하기"
description: "팀 lead·teammate·공유 task와 mailbox를 이용해 여러 coding agent를 병렬 운영하는 실전 가이드"
resource: "https://www.fullstackfamily.com/@urstory/posts/14067"
notion: "https://app.notion.com/p/5a51a73cf20b83038692814bd866d391"
tags: [reading, claude-code, agent-teams, tmux, iterm2]
timestamp: 2026-07-24
status: summarized
---

# Agent Teams와 subagent

Subagent는 main agent가 일을 위임하고 결과를 돌려받는 구조이며 서로 직접 대화하지 않는다. Agent Teams는 lead와 여러 teammate가 shared task list와 file-based mailbox를 사용해 직접 message를 주고받는다. 독립된 역할이 실제로 병렬화될 때 적합하다.

# 운영 흐름

실험 기능을 활성화하고 macOS의 iTerm2 또는 tmux에서 pane별 teammate를 실행한다. 역할, 소유 directory와 완료 조건을 명시하고 task dependency를 shared list에 둔다. Code 변경 전에 계획 승인을 요구할 수 있으며, 역할별로 다른 model을 선택해 비용을 조절한다. Native pane integration이 필요하면 iTerm2 Python API와 `it2` CLI를 사용할 수 있다.

# 충돌 방지

각 agent가 다른 file·directory를 맡게 하고 같은 file 수정은 순서를 정한다. 큰 변경은 Git worktree로 분리한 뒤 test를 통과한 commit만 통합한다. Team 기능을 쓰지 않아도 tmux pane에서 여러 `claude -p` process를 제한된 `--allowedTools`로 수동 운영할 수 있다.

# 한계와 보안

가이드 시점의 experimental 기능은 session resume 시 실행 중 teammate가 복구되지 않고 nested team도 지원하지 않는다. 일반적으로 3~5명 이후에는 coordination 비용이 빠르게 커진다. Remote shell, source와 key 접근 권한을 role별로 최소화하고 공식 문서에서 최신 기능과 option을 다시 확인한다.

# 출처

- [Claude Code Agent Teams 완벽 가이드](https://www.fullstackfamily.com/@urstory/posts/14067)
