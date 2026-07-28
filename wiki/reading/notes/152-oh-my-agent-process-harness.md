---
type: Reference
title: "oh-my-agent: 프롬프트보다 프로세스로 제어하는 에이전트 하네스"
description: "실수 기록, 명확화 부채, 단계별 품질 게이트를 통해 여러 AI IDE를 공통 운영하는 방식"
resource: https://news.hada.io/topic?id=27560
notion: https://app.notion.com/p/db81a73cf20b82e591b481154192a666
tags: [reading, ai-agents, harness, quality-assurance]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`oh-my-agent`는 에이전트의 역할을 길게 설명하는 대신 요구사항 명확화, 작업 범위, 검증, 실패 학습을 프로세스로 강제하는 범용 AI IDE 하네스다. Antigravity, Claude Code, Codex CLI, Cursor 등에서 공통으로 쓰는 `.agents/` 구조를 단일 진실 공급원으로 둔다.

# 핵심 메커니즘

- 요구사항 오해, 재작업, 범위 밖 수정에 Clarification Debt 점수를 부여한다.
- 임계치를 넘으면 원인 분석을 의무화하거나 세션을 중단한다.
- 실패에서 얻은 교훈을 `lessons-learned.md`에 남겨 다음 실행에 반영한다.
- 모호도와 작업 난이도에 따라 질문과 검증의 깊이를 조절한다.
- PM, QA, 프런트엔드, 백엔드, DB, 인프라 같은 역할을 필요에 따라 구성한다.

# 두 실행 모드

`/coordinate`는 빠른 분해·실행 뒤 QA가 주요 이슈를 잡는 비교적 가벼운 흐름이다. `/ultrawork`는 계획, 구현, 검증, 개선, 배포 단계마다 게이트를 두고 통과하지 못하면 다음 단계로 가지 않는 품질 중심 흐름이다.

# 내 관점

점수의 구체적인 숫자보다 “실패를 관찰 가능한 사건으로 만들고 재발 방지 규칙으로 환류한다”는 발상이 중요하다. 저장소에 도입한다면 삭제·이동 같은 위험 명령, 허용된 쓰기 경로, 검증 명령을 먼저 프로젝트 규칙으로 고정해야 한다.

# 관련 문서

- [HarnessX](036-harnessx-agent-harness-foundry.md)
- [에이전트 하네스와 반복 검증](20-agent-harness-loop-engineering.md)

# 출처

- [GeekNews 소개와 토론](https://news.hada.io/topic?id=27560)
- [oh-my-agent GitHub](https://github.com/first-fluke/oh-my-agent)

