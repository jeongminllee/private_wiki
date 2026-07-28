---
type: Reference
title: "코드 작성 속도보다 시스템 병목을 찾아라"
description: "AI가 코드 생산량을 늘려도 요구, 리뷰, 배포와 피드백 대기열이 그대로면 전체 전달 속도는 좋아지지 않는다는 글"
resource: https://news.hada.io/topic?id=27624
notion: https://app.notion.com/p/2fb1a73cf20b8389a52b01c55794f1ef
tags: [reading, software-engineering, productivity, theory-of-constraints]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

글은 AI coding 도구가 코드 작성 단계를 빠르게 해도 제품이 사용자에게 도달하는 전체 흐름의 병목은 다른 곳에 있을 수 있다고 주장한다. Theory of Constraints 관점에서는 병목이 아닌 공정만 가속하면 처리량 대신 WIP와 대기 시간이 늘어난다.

# 흔한 실제 병목

- **문제 이해**: 사용자와 대화하지 않은 채 짧은 ticket을 구현해 잘못된 기능을 빠르게 만든다.
- **review queue**: PR 생성은 늘지만 reviewer 수와 시간이 그대로여서 형식적 승인이 늘어난다.
- **CI와 배포**: 느리고 flaky한 test, 수동 승인과 배포 window 때문에 code가 며칠씩 기다린다.
- **배포 신뢰**: 관찰과 rollback이 약해 변경을 큰 batch로 묶고 risk가 더 커진다.
- **출시 후 피드백**: 사용 여부를 측정하지 않아 다음 기능도 추측으로 만든다.
- **조정 비용**: 팀 간 API 결정, 회의와 단일 승인자가 전체 흐름을 막는다.

# 측정과 개선

기능 하나를 idea에서 production 사용까지 추적해 실제 작업 시간과 대기 시간을 나눈 value stream map을 만든다. line 수나 merged PR 수보다 commit-to-production, 사용자 피드백까지의 cycle time을 본다. 작은 PR, WIP 제한, review 시간 확보, 자동화된 test·rollback과 명확한 decision owner로 가장 큰 대기 지점부터 줄인다.

# 균형 있게 보기

모든 팀에서 코딩이 병목이 아니라는 절대 법칙은 아니다. 1인 개발, prototype과 반복 구현에서는 생성 속도가 실제 제약일 수 있다. AI 사용과 process 개선도 동시에 가능하다. 핵심은 도구를 도입하기 전에 현재 제약을 측정하고, 가속된 코드가 다음 공정에 쌓이지 않는지 보는 것이다.

# 출처

- [GeekNews 한국어 소개와 토론](https://news.hada.io/topic?id=27624)
- [원문](https://andrewmurphy.io/if-you-think-code-writing-speed-is-your-problem-you-have-bigger-problems)
- [Notion 원본 항목](https://app.notion.com/p/2fb1a73cf20b8389a52b01c55794f1ef)

