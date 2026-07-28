---
type: Reference
title: "AI agent 구성 요소: Rules, Skills, Commands, Subagents"
description: "Claude Code를 예로 들어 상시 규칙, 재사용 지식, 명시적 동작과 격리된 실행 주체를 구분하는 설계 가이드"
resource: "https://yozm.wishket.com/magazine/detail/3646/"
notion: "https://app.notion.com/p/3c61a73cf20b82908d3501981a94c17e"
tags: [reading, ai-agent, claude-code, skills, subagents]
timestamp: 2026-07-24
status: summarized
---

# 네 구성 요소

`Rules`는 coding convention, 금지 사항, 필수 검증처럼 매 작업에 적용되는 invariant다. 항상 context에 들어가므로 짧고 안정적이어야 한다.

`Skills`는 특정 workflow에 필요한 지식과 절차를 folder와 `SKILL.md` 형태로 묶는다. 이름과 설명만 먼저 보여주고 실제 내용은 관련 task에서 불러오는 progressive disclosure가 context를 아낀다.

`Commands`는 사용자가 명시적으로 실행하는 예측 가능한 action이다. 반복되는 release, check, migration처럼 입력과 출력 형태가 안정된 작업에 맞는다.

`Subagents`는 별도 context, model, tools와 permission을 가진 실행 주체다. 단순히 지식이 다른 것이 아니라 탐색 범위, 권한 또는 작업 방식이 독립적일 때 사용한다.

# 조합 원칙

Team 전체 invariant는 rule, 필요할 때만 읽을 domain playbook은 skill, 사람이 시작하는 deterministic operation은 command, 병렬 조사나 권한 격리가 필요한 일은 subagent로 둔다. 같은 내용을 네 곳에 복제하면 충돌과 context 낭비가 생긴다.

Skill의 description과 trigger가 모호하면 필요한 순간에 불리지 않고, 너무 넓으면 매번 불필요한 내용을 주입한다. 실제 실패 log를 보고 metadata와 scope를 조정해야 한다. Claude Code의 directory와 호출 semantics는 version에 따라 달라질 수 있으므로 article의 개념과 현재 공식 동작을 구분해서 적용한다.

# 출처

- [요즘IT 원문](https://yozm.wishket.com/magazine/detail/3646/)
