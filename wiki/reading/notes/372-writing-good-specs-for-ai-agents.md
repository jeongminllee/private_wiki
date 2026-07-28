---
type: Reference
title: "AI coding agent가 따를 수 있는 좋은 명세 작성법"
description: "무엇과 왜에서 시작해 plan·task·implementation으로 내려가고 command, test, boundary를 명시하는 specification workflow"
resource: "https://news.hada.io/topic?id=25949"
notion: "https://app.notion.com/p/2131a73cf20b830c8eff81d67634a7ed"
tags: [reading, specification, ai-coding, agent, software-engineering]
timestamp: 2026-07-24
status: summarized
---

# 명세의 역할

좋은 명세는 code를 길게 묘사하는 문서가 아니라 agent가 판단해야 할 모호함을 줄이는 shared contract다. 먼저 높은 수준의 `무엇을`과 `왜`를 적고, agent에게 read-only plan을 만들게 해 빠진 질문과 제약을 드러낸다. 합의된 뒤 `Specify -> Plan -> Tasks -> Implement` 순서로 내려간다.

# 포함할 내용

여러 repository의 agent instruction에서 반복되는 항목은 실행 command, testing, project structure, code style, git workflow와 boundaries다. 정확한 version, 실제 command와 좋은 예제를 적고, 행동은 `항상`, `먼저 물어보기`, `절대 하지 않기`로 구분하면 권한 경계가 선명해진다.

큰 문서는 목차와 module별 하위 문서로 나눈다. 지금 task에 필요한 context만 불러오고, 완료 조건을 test·lint·build·conformance suite처럼 실행 가능한 형태로 둔다. 주관적 품질에 LLM judge를 쓸 수 있지만 결정론적 test를 대체해서는 안 된다.

# 운영 원칙

명세는 실패를 통해 갱신되는 living document다. Agent가 잘못 이해한 지점이 요구사항의 빈칸인지, codebase의 숨은 규칙인지 확인하고 수정한다. 반대로 사소한 작업까지 과도하게 규정하면 오래된 지침과 충돌이 늘어난다. Domain edge case와 최종 승인 책임은 여전히 사람에게 있다.

# 출처

- [GeekNews 요약](https://news.hada.io/topic?id=25949)
- [Addy Osmani 원문](https://addyosmani.com/blog/good-spec/)
