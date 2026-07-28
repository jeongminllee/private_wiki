---
type: Paper Note
title: "Nested Learning: 모델과 optimizer를 여러 시간 척도의 학습 문제로 보기"
description: "NeurIPS 2025 논문이 제안한 nested optimization, continuum memory와 Hope model의 의미"
resource: https://openreview.net/challenge?redirect=%2Fforum%3Fid%3DnbMeRvNb7A
resource_aliases: [https://openreview.net/forum?id=nbMeRvNb7A]
notion: https://app.notion.com/p/4061a73cf20b831986d1814ff9dc1521
tags: [paper, optimization, continual-learning, memory]
timestamp: 2026-07-24
status: summarized
---

# 문제의식

논문은 deep-learning architecture와 optimizer를 서로 분리된 것으로 보는 통상적 설명을 재검토한다. 둘 다 context를 압축해 parameter를 갱신하는 associative memory이며, 서로 다른 update rate와 information flow를 가진 여러 optimization problem이 중첩돼 있다는 관점을 제시한다.

# Nested Learning

저자들은 model을 여러 수준의 병렬·중첩 optimization으로 표현한다. 빠르게 변하는 activation이나 short-term state와 느리게 갱신되는 weight를 하나의 continuum 안에서 보고, 각 memory module이 어느 context를 어떤 update frequency로 저장하는지 분석한다.

이 관점에서는 optimizer도 단순한 외부 계산 규칙이 아니다. Gradient history를 기억하고 update를 만드는 학습 module로 해석할 수 있다. 이를 바탕으로 더 표현력 있는 optimizer와 self-modifying sequence model을 설계한다.

# Hope와 continuum memory

Proof-of-concept인 Hope는 여러 시간 척도의 memory를 결합해 long-context 처리와 continual learning을 개선하려는 model이다. 하나의 고정된 short/long-term 구분 대신 update frequency가 다른 memory 층을 연속적으로 배치한다는 점이 핵심이다.

# 평가할 때

Nested Learning은 architecture, memory와 optimization을 함께 설계하는 유용한 framework이지만 continual learning이 일반적으로 해결됐다는 증명은 아니다. 기존 Transformer와 같은 parameter·data·compute에서의 비교, forgetting 측정, 긴 sequence 비용과 independent reproduction을 확인해야 한다.

# 출처

- [OpenReview](https://openreview.net/forum?id=nbMeRvNb7A)
- [arXiv 2512.24695](https://arxiv.org/abs/2512.24695)

