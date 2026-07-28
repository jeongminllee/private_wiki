---
type: Reference
title: "Hatchet의 터미널 UI 개발 사례"
description: "Charm 스택과 tmux 기반 자동 검증으로 개발자용 TUI를 이틀 만에 만든 사례"
resource: https://news.hada.io/topic?id=26694
notion: https://app.notion.com/p/6651a73cf20b839081fb8120d260934e
tags: [reading, tui, golang, ai-coding]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Hatchet 팀은 IDE와 터미널에서 일하는 사용자가 웹 대시보드로 이동하지 않고 workflow를 보고 실행하도록 TUI를 만들었다. Go의 Charm 스택과 기존 OpenAPI client, Claude Code가 다루기 쉬운 텍스트 출력 검증을 결합해 약 이틀 만에 첫 버전을 만들었다는 사례다.

# 기술 구성

- Bubble Tea: 상태 업데이트와 렌더링을 관리하는 TUI framework
- Lip Gloss: 레이아웃과 색, 테두리 등 스타일링
- Huh: form과 입력 구성 요소
- 기존 REST client와 OpenAPI 명세: 웹 UI와 같은 backend 계약 재사용
- `tmux capture-pane`: 실제 터미널 화면을 캡처해 에이전트가 결과를 읽고 반복 수정

가장 어려운 부분은 DAG를 ASCII로 표현하는 렌더러였다. 기존 `mermaid-ascii` 구현을 참고해 완벽한 그래프보다 사용 가능한 첫 버전을 만들었다.

# 왜 에이전트와 잘 맞았나

렌더링 결과가 텍스트이므로 브라우저의 시각 좌표보다 캡처·비교가 쉽고, 테스트 명령과 피드백 루프가 짧았다. 기존 웹 구현과 API 명세가 명확한 참고 답안 역할을 한 것도 중요하다. 생산성은 LLM 하나보다 모듈화, 재사용 가능한 계약과 관찰 가능한 출력에서 나왔다.

# 주의할 점

TUI가 항상 GUI보다 빠르거나 접근성이 좋은 것은 아니다. 복잡한 시각화, 마우스 탐색과 화면 읽기 도구에서는 GUI가 적합할 수 있다. “이틀 완성”은 숙련된 팀, 기존 backend와 제한된 범위가 있는 사례이며 유지보수 비용을 포함한 비교는 아니다.

# 출처

- [GeekNews 한국어 소개와 토론](https://news.hada.io/topic?id=26694)
- [Hatchet 원문](https://hatchet.run/blog/tuis-are-easy-now)
- [Notion 원본 항목](https://app.notion.com/p/6651a73cf20b839081fb8120d260934e)

