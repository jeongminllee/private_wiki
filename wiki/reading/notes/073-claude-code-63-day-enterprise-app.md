---
type: Reference
title: "Claude Code와 63일간 만든 AHP 웹앱"
description: "PM이 목표·구조·검증을 맡고 AI가 구현·문서·디버깅을 수행한 장시간 집중 개발 사례"
resource: https://yozm.wishket.com/magazine/detail/3469/
notion: https://app.notion.com/p/2141a73cf20b8296812f01cb7bc29434
tags: [reading, claude-code, case-study, web-development]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

연구자를 위한 AHP(Analytic Hierarchy Process) 플랫폼을 혼자 개발하며 Claude Code를 사용한 회고다. 발표자는 63일 연속, 총 950시간가량 작업하며 9개 저장소에 2,900개 이상의 commit을 남겼다고 보고한다. 단순 프롬프트 한 번이 아니라 사람이 PM과 architect 역할을 맡은 고강도 프로젝트다.

# 역할 분담

사람은 요구사항, 우선순위, 전체 구조, 개발 규칙과 최종 검증을 담당했다. AI는 코드와 문서 생성, 반복 구현, 디버깅을 수행했다. 개발 일지, 평가 보고서, 저장소별 역할과 history를 계속 남겨 긴 세션의 방향을 유지했다.

글은 첫 시도 성공률 78%, 자동 생성률 85%, 평균 버그 해결 18분, 일반 개발자 대비 5배 생산성 등을 제시한다. 기존 시스템 대비 99.9% 성능 향상이라는 표현도 15명 이상 tester의 평가를 근거로 든다.

# 해석

가장 재사용 가능한 교훈은 생산성 숫자보다 작업의 구조다. 63일 동안 하루 평균 15시간 수준의 노동, 풍부한 도메인 지식과 웹 개발 경험이 결합됐다. 사람이 방향과 평가를 계속 제공했고, 작은 commit과 백업 저장소로 회귀 비용을 낮췄다. 이를 “비개발자 한 명이 AI에게 맡겨 4~5명 팀을 대체했다”로 단순화하면 중요한 조건이 사라진다.

# 주의할 점

수치는 저자의 자체 측정이며 동일 요구사항을 인간 팀과 비교한 통제 실험이 아니다. commit 수는 가치나 품질 지표가 아니고, 950시간의 집중 노동은 지속 가능한 일반 작업 방식도 아니다. 보안, 운영 장애, 장기 유지보수와 독립 code review가 어느 정도였는지는 별도로 확인해야 한다.

# 출처

- [요즘IT 원문](https://yozm.wishket.com/magazine/detail/3469/)
- [Notion 원본 항목](https://app.notion.com/p/2141a73cf20b8296812f01cb7bc29434)

