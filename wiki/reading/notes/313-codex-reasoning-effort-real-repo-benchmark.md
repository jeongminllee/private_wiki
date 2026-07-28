---
type: Reference
title: "Codex 추론 강도 비교: 테스트 통과보다 의미적 동등성과 리뷰 품질이 갈렸다"
description: "실제 GraphQL 저장소 작업 26개에서 low부터 xhigh까지 비용, 시간, 패치 동등성과 리뷰 가능성을 비교한 실험"
resource: "https://news.hada.io/topic?id=29316"
resource_aliases: [https://share.google/8hdO1IxIm0jBWJnS0]
notion: "https://app.notion.com/p/5941a73cf20b82c480a201824b856942"
tags: [reading, coding-agents, evaluation, codex]
timestamp: 2026-07-24
status: summarized
---

# 실험과 결과

GPT-5.5 Codex를 Go 기반 `GraphQL-go-tools`의 실제 병합 작업 26개에 low, medium, high, xhigh 추론 강도로 각각 한 번 실행한 비교다. 고정 snapshot과 prompt를 사용하고 Docker 안에서 task별 test를 실행했다. 이후 사람 patch와의 의미적 동등성, code review 통과 가능성, 변경 footprint와 코드 제작·규율을 별도로 평가했다.

테스트 통과는 low 21/26, medium 21/26, high 25/26, xhigh 24/26이었다. 반면 사람 patch와 의미적으로 동등한 결과는 4/26, 11/26, 18/26, 23/26, review 통과는 3/26, 5/26, 10/26, 18/26으로 더 크게 벌어졌다. 평균 비용은 $2.65, $3.13, $4.49, $9.77이고 평균 시간은 약 287초, 411초, 579초, 753초였다.

# 해석

테스트가 통과해도 빠진 요구사항, 잘못된 domain model이나 유지보수 위험이 남을 수 있다. 이 실험에서 high는 medium보다 비용이 1.43배였지만 세 주요 지표가 모두 좋아져 일상적인 기본값 후보였다. xhigh는 의미와 review 품질은 더 높았지만 비용이 high의 2.18배이고 test·fixture까지 더 넓게 바꾸는 경향이 있었다.

추론 강도 효과는 단조롭지 않았다. 일부 작업에서는 high가 xhigh보다 정확했고, 높은 설정이 더 그럴듯하지만 잘못된 구현을 만들기도 했다. 모호하거나 concurrency가 중요한 작업에는 xhigh가 도움이 될 수 있지만 전역 기본값으로 복사할 결과는 아니다.

# 한계와 적용

작업당 seed가 한 번뿐이고 한 Go 저장소의 26개 작업에 한정됐다. 판정자도 GPT-5.4이며 별도 인간 calibration이 없다. 절대 수치보다 방향성을 참고하고, 실제 팀에서는 과거 병합 작업으로 자체 harness를 만들어 test, semantic acceptance, review와 비용을 함께 측정해야 한다.

# 출처

- [GeekNews 정리와 원문 링크](https://news.hada.io/topic?id=29316)
