---
type: Project
title: "claude-recall: 병렬 Claude Code 세션의 목적을 보여주는 statusline"
description: "세션 목적, branch, turn, context와 비용을 터미널 HUD에 표시해 여러 작업의 맥락 복구를 돕는 plugin"
resource: "https://news.hada.io/topic?id=27525"
notion: "https://app.notion.com/p/22c1a73cf20b8339ba3c81bf603e8860"
tags: [reading, claude-code, plugin, statusline, productivity]
timestamp: 2026-07-24
status: summarized
---

# 해결하려는 문제

Claude Code를 여러 terminal에서 실행하면 tab을 바꿀 때마다 각 session이 무슨 일을 하던 중인지 다시 읽어야 한다. `claude-recall`은 prompt 아래 statusline에 session의 목적과 진행 정보를 표시해 이 전환 비용을 줄인다.

# 동작

GeekNews에 처음 소개될 때는 첫 prompt와 `/purpose` 명령으로 목적을 정하고 `SessionStart`, `UserPromptSubmit`, `SessionEnd` hook이 JSON 상태를 저장했다. 현재 repository는 background Haiku 호출이 transcript 언어로 focus label을 자동 보정하는 방식으로 발전했다.

현재 HUD는 최대 세 줄에 focus, directory·branch 색상, turn과 elapsed time, context·cost·rate limit, Git 상태와 model metadata를 조합한다. Claude Code의 native statusline JSON과 plugin 상태를 함께 사용하며 `/compact`, `/clear`, `/resume` 같은 session 명령과 역할을 나눈다.

# 비용과 주의

Focus 자동 보정에는 긴 session당 약 0.01달러의 background LLM 호출이 발생하며 끄는 option이 없다고 README가 밝힌다. Transcript 일부가 model 호출에 쓰인다는 점을 고려해 민감한 project에서는 설치 전 data flow를 검토한다. Statusline은 맥락을 상기시키지만 실제 완료 여부는 test와 변경 결과로 확인해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27525)
- [claude-recall 저장소](https://github.com/dkstm95/claude-recall)
