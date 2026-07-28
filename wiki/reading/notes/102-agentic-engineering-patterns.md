---
type: Reference
title: "에이전틱 엔지니어링 패턴"
description: "코딩 에이전트와 일할 때 테스트, 검토, 이해와 재사용 자산을 중심에 두는 개발 습관"
resource: https://news.hada.io/topic?id=27206
notion: https://app.notion.com/p/4151a73cf20b8209b909817f2bac0794
tags: [reading, coding-agent, software-engineering, testing]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Simon Willison이 계속 갱신하는 코딩 에이전트 협업 가이드다. 초안 코드의 생산 비용은 낮아졌지만, 요구를 충족하고 이해 가능하며 테스트된 좋은 코드의 비용은 여전히 크다는 전제에서 출발한다.

# 핵심 패턴

- 이미 해결해 본 작은 예제와 검증된 명령을 모아 에이전트에게 줄 재사용 자산으로 만든다.
- 작업 전 기존 테스트를 실행해 기준선을 확인하고 red/green TDD로 종료 조건을 고정한다.
- 생성된 코드는 선형 walkthrough와 대화형 설명을 통해 사람이 실제 흐름을 이해한다.
- 유용했던 prompt와 후속 수정 과정을 주석과 함께 보관한다.
- 리뷰하지 않은 코드나 AI가 만든 PR 설명을 동료에게 그대로 넘기지 않는다.

# 적용 메모

요청에는 목표, 제약, 관련 파일, 검증 명령과 완료 조건을 함께 준다. 결과를 받은 뒤 diff, 테스트, 정적 분석과 실제 동작을 확인하고, 되돌릴 수 없는 변경에는 인간 검토 지점을 둔다. 에이전트가 만든 테스트도 구현에 맞춘 자기충족적 테스트인지 의도적인 mutation으로 확인할 수 있다.

# 비판적으로 볼 점

많은 항목은 TDD, 작은 모듈, 코드 리뷰처럼 기존의 좋은 공학 습관이다. 새 이름보다 중요한 것은 코드 생성량이 늘어난 환경에서 검증 병목과 책임을 어떻게 운영할지다. 패턴의 효과는 코드베이스 품질과 자동화 수준에 크게 좌우된다.

# 출처

- [Agentic Engineering Patterns 원문](https://simonwillison.net/guides/agentic-engineering-patterns/)
- [GeekNews 한국어 정리와 토론](https://news.hada.io/topic?id=27206)
- [Notion 원본 항목](https://app.notion.com/p/4151a73cf20b8209b909817f2bac0794)
