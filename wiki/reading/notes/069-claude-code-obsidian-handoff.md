---
type: Reference
title: "Obsidian 인수인계로 Claude Code 맥락 유지하기"
description: "프로젝트 기록, 설계, 구현과 세션 인수인계를 Markdown으로 연결하는 개인 워크플로"
resource: https://news.hada.io/topic?id=27614
notion: https://app.notion.com/p/ead1a73cf20b8368b736016282578cda
tags: [reading, claude-code, obsidian, knowledge-management]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

글은 바이브 코딩 프로젝트가 반복해서 무너지는 병목을 코드 생성보다 기억의 유실로 본다. 사람과 AI 모두 며칠 뒤 목표, 결정과 실패를 잊기 때문에 Obsidian을 장기 기억으로 두고 “기록 → 설계 → 구현 → 기록” 순환을 만든 사례다.

# 역할 분리

- **Obsidian**: 기획, 설계, 세션 로그, 오류와 결정을 Markdown으로 보존한다.
- **Claude Desktop + MCP**: 노트를 읽고 요구와 구조를 논의하는 지휘자 역할을 맡는다.
- **Claude Code + MCP**: 합의된 설계를 저장소에서 구현하고 테스트한다.
- **`날짜_handoff.md`**: 세션 종료 시 현재 상태, 결정, 막힌 점과 다음 행동을 기록한다.

새 세션은 전체 대화를 다시 넣는 대신 최신 handoff와 필요한 설계 문서부터 읽는다. AI의 자동 메모리는 모델이 다음 행동을 고르는 데 유용하고, 사람이 읽는 프로젝트 기록은 책임과 재개를 위해 필요하므로 서로 대체하지 않는다는 관점이다.

# 간단한 템플릿

인수인계에는 목표, 이번 세션에서 바뀐 파일, 확정한 결정과 이유, 실행한 검증, 남은 오류, 다음 한 가지 행동을 둔다. 코드와 문서가 어긋나지 않도록 큰 결정은 저장소 안의 문서에도 반영한다.

# 주의할 점

10개 이상 프로젝트를 동시에 운영했다는 결과는 개인 경험이지 비교 실험이 아니다. MCP와 별도 Obsidian vault가 항상 필요한 것도 아니다. 작은 프로젝트는 저장소 안의 `docs/`, issue와 Git history만으로 충분할 수 있으며 기록 유지 비용이 실제 복구 시간보다 커지지 않게 해야 한다.

# 출처

- [GeekNews 원문과 토론](https://news.hada.io/topic?id=27614)
- [공개된 WikiDocs 가이드북](https://wikidocs.net/book/19307)
- [Notion 원본 항목](https://app.notion.com/p/ead1a73cf20b8368b736016282578cda)

