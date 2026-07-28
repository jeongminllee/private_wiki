---
type: Study Note
title: "Claude Agent SDK 전체 워크숍: Bash, 파일시스템과 검증 loop"
description: "Thariq Shihipar가 agent 정의, tool 설계, context, security와 verification을 live coding으로 설명한 112분 강의"
resource: "https://www.youtube.com/watch?v=TqC1qOfiVcQ"
notion: "https://app.notion.com/p/8f61a73cf20b824ca1a60111deea1172"
tags: [reading, claude-agent-sdk, ai-agent, security, workshop]
timestamp: 2026-07-24
status: summarized
---

# Agent를 보는 관점

워크숍은 사람이 미리 경로를 정한 workflow와 model이 스스로 context와 실행 경로를 만드는 agent를 구분한다. Agent loop는 `context 수집 → 행동 → 결과 관찰·검증`이며, 좋은 domain은 행동 결과를 test나 규칙으로 확인할 수 있어야 한다.

# Bash is all you need

Bash와 filesystem은 이미 composable한 tool ecosystem과 persistent state를 제공한다. Agent가 필요할 때 code를 생성해 data를 가공하면 모든 operation을 별도 tool schema로 만들지 않아도 된다. 다만 shell 하나에 무제한 권한을 주라는 뜻이 아니라 sandbox, command policy와 permission을 함께 설계하라는 주장이다.

# Context와 subagent

큰 dataset이나 광범위한 search는 subagent가 처리하고 main agent에는 최종 결과만 돌려 context pollution을 줄인다. 비판적 검토 subagent는 원 작업의 context를 그대로 fork하기보다 독립 context에서 시작하는 편이 낫다. Skill은 반복 절차와 domain 지식을 재사용하는 역할을 한다.

# 검증과 보안

가능한 검증은 model judge보다 compiler, lint, schema, threshold와 state invariant 같은 deterministic rule로 먼저 만든다. 마지막뿐 아니라 읽기·쓰기·실행 사이의 모든 경계에서 즉시 feedback을 주면 agent가 수정할 수 있다.

Security는 model alignment, tool permission, sandbox와 application guardrail을 여러 겹으로 두는 `Swiss cheese defense`로 설명한다. 한 계층이 모든 공격을 막는다고 가정하지 않는다. Claude Code에서 prototype한 뒤 SDK application으로 옮길 때도 budget, audit log, timeout과 human approval을 명시해야 한다.

# 출처

- [Claude Agent SDK Full Workshop](https://www.youtube.com/watch?v=TqC1qOfiVcQ)
- [검색 가능한 transcript](https://youtube-distilled.com/watch/TqC1qOfiVcQ)
