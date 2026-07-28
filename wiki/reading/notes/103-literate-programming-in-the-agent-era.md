---
type: Reference
title: "에이전트 시대의 문학적 프로그래밍"
description: "실행 가능한 코드와 설명을 한 문서에 두고 에이전트로 동기화 비용을 줄이는 접근"
resource: https://news.hada.io/topic?id=27383
notion: https://app.notion.com/p/7d21a73cf20b82908f6501baed2bce3a
tags: [reading, literate-programming, coding-agent, documentation]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

문학적 프로그래밍(literate programming)은 코드와 자연어 설명을 독자가 이야기처럼 따라갈 수 있게 엮는 방식이다. 과거에는 코드와 설명이라는 두 서사를 함께 유지하고 tangling 결과를 관리하는 비용이 컸지만, 에이전트가 양쪽을 동기화하면 runbook과 수동 검증 문서에서 다시 실용적일 수 있다는 제안이다.

# 제안하는 흐름

1. Org Mode의 `org-babel` 같은 실행 가능한 문서에 의도와 명령을 함께 적는다.
2. 사람이 설명과 실행 순서를 검토한 뒤 코드 블록을 하나씩 또는 전체로 실행한다.
3. 결과를 문서 안에 남겨 실행 기록과 설명을 동시에 얻는다.
4. 에이전트에게 코드 수정 시 설명도 갱신하고 실행 전 tangle하도록 지시한다.
5. `AGENTS.md`에는 어떤 문서가 source of truth인지 명확히 적는다.

# 어디에 유용한가

인프라 runbook, 재현 가능한 실험, 수동 QA, 개인 설정과 장애 대응 절차에 특히 잘 맞는다. 코드 실행과 기록을 같은 행위로 묶으면 “나중에 문서화”가 빠지는 문제를 줄일 수 있다.

# 한계

저자는 큰 프로덕션 코드베이스에서는 아직 검증하지 않았다고 밝힌다. 원본 문서와 추출된 코드가 모두 수정되면 source of truth가 충돌하고, AI가 만든 설명이 장황하거나 사실과 어긋날 수 있다. 따라서 CI에서 tangle 결과의 차이를 검사하고 실행 권한을 제한해야 한다.

# 출처

- [원문](https://silly.business/blog/we-should-revisit-literate-programming-in-the-agent-era/)
- [GeekNews 한국어 정리](https://news.hada.io/topic?id=27383)
- [Notion 원본 항목](https://app.notion.com/p/7d21a73cf20b82908f6501baed2bce3a)
