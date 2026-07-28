---
type: Reference
title: "Addy Osmani의 LLM 코딩 workflow 핵심판"
description: "Spec-first, 작은 task, 충분한 context, model 교차 검증과 human review를 요약한 짧은 GeekNews 항목"
resource: "https://news.hada.io/topic?id=26566"
notion: "https://app.notion.com/p/ccf1a73cf20b83d0b55e819fa5ab2647"
tags: [reading, ai-coding, workflow, specification, code-review]
timestamp: 2026-07-24
status: summarized
---

# 핵심 원칙

Code를 생성하기 전에 `spec.md`에서 요구사항, architecture, data model과 test 전략을 정한다. Osmani는 이 짧고 구조화된 준비 단계를 “15분 waterfall”에 비유한다. 이후 구현을 feature, function과 bug 단위로 작게 나눠 한 단계씩 검증한다.

관련 code와 API 문서, 제약 조건을 충분히 제공하되 repository 전체를 무작정 넣지 않는다. 한 model이 막히면 다른 model에게 대안을 묻거나, 한 model의 구현을 다른 model이 비판하게 해 blind spot을 찾는다.

# 책임 경계

LLM은 자신감은 높지만 실수가 잦은 junior pair programmer처럼 다룬다. 사람이 모든 변경을 이해하고 test·review하며, 설명할 수 없는 code는 commit하지 않는다는 기준이 핵심이다. Model끼리 교차 review해도 independent test와 domain owner의 승인을 대체하지 않는다.

# 관련 문서

- [같은 원문의 상세 GeekNews 정리](393-addy-osmani-llm-workflow-detailed.md)
- [AI coding agent 명세 작성법](372-writing-good-specs-for-ai-agents.md)

# 출처

- [GeekNews 짧은 정리](https://news.hada.io/topic?id=26566)
- [Addy Osmani 원문](https://addyosmani.com/blog/ai-coding-workflow/)
