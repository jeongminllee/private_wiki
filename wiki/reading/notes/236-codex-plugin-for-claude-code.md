---
type: Reference
title: "Claude Code 안에서 Codex를 reviewer와 rescue agent로 쓰기"
description: "Codex CLI를 Claude Code slash command와 background task로 호출해 교차 review·작업 위임하는 plugin"
resource: https://news.hada.io/topic?id=28023
notion: https://app.notion.com/p/2d61a73cf20b82eda5c701af289ab95e
tags: [reading, codex, claude-code, code-review]
timestamp: 2026-07-24
status: summarized
---

# 제공하는 흐름

이 plugin은 Claude Code 안에서 local Codex CLI·app server를 호출해 같은 repository의 변경을 다른 agent에게 review시키거나 막힌 작업을 넘긴다. 별도 execution layer를 만들지 않아 기존 Codex 인증, model 설정과 session을 재사용한다.

# 주요 명령

- `/codex:review`: uncommitted change 또는 base branch와의 diff를 읽기 전용 검토
- `/codex:adversarial-review`: assumption, failure mode, security와 rollback을 압박 검토
- `/codex:rescue`: bug 조사·수정이나 이전 Codex task를 이어받기
- `/codex:status`, `result`, `cancel`: background task 관리
- `/codex:setup`: 설치와 인증 확인

review gate는 Claude가 멈추기 전에 Codex 검토를 자동 실행하고 발견된 문제가 있으면 수정 loop를 이어가게 한다.

# 활용과 주의

서로 다른 model·harness를 reviewer로 쓰면 같은 blind spot을 줄일 수 있지만 둘의 동의가 correctness를 보장하지 않는다. deterministic test와 사람이 최종 판단해야 한다. 자동 review gate는 Claude-Codex loop와 사용량 폭증을 만들 수 있으므로 최대 반복, background task 수와 비용을 제한한다.

# 출처

- [GeekNews 정리와 토론](https://news.hada.io/topic?id=28023)

