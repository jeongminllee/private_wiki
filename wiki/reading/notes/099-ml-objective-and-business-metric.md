---
type: Reference
title: "배포 효과로 이어지는 ML 학습 목표와 평가 지표 설계"
description: "교란을 줄인 randomized data, item-wise ranking과 conversion-rate lift로 offline 평가를 business impact에 연결한 사례"
resource: https://hyperconnect.github.io/2025/11/28/how-to-set-ml-objective.html
notion: https://app.notion.com/p/9a41a73cf20b822392d181f95d8d2b2c
tags: [reading, machine-learning, ranking, experimentation, causal-inference]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

좋은 offline metric이 실제 배포 성과를 보장하지 않는 이유는 학습 data의 생성 과정과 business 질문이 어긋날 수 있기 때문이다. Hyperconnect 사례는 아이템의 대표 속성을 골라 전환율을 높이는 문제에서 confounder를 줄인 data를 만들고, business lift와 직접 연결되는 평가 지표를 설계한다.

# 문제 정의

단순히 “전환된 속성을 맞히는” supervised learning은 인기 item, 노출 사용자와 기존 선택 정책의 영향을 함께 학습할 수 있다. 같은 item 안에서도 시간이나 추천 logic이 사용자 분포와 속성 노출에 동시에 영향을 주면 비교가 왜곡된다.

이를 줄이기 위해 item의 후보 속성을 무작위로 노출한 `attribute shuffle` data를 사용한다. 같은 item의 두 속성 중 관찰 전환율이 높은 쪽이 더 큰 score를 갖도록 pairwise dataset을 만들고 ranking loss를 최소화한다.

# 평가 지표

Mean Spearman correlation과 Top-1 accuracy는 순서를 비교하지만 전환율 차이의 크기와 business impact를 직접 나타내지 못한다. 관찰 전환율은 binomial noise를 포함해 표본 수가 적을수록 순위 자체도 불확실하다.

대신 사람이 고른 대표 속성 대비 모델이 고른 속성의 평균 전환율 상승을 `relative mean CR lift`로 계산한다. `+5%`라면 offline data에서 기존 선택 대비 평균 전환율이 5% 높을 것으로 추정한다는 의미여서 배포 판단과 연결하기 쉽다.

# 중요한 보정

같은 data에서 관찰 전환율이 가장 높은 속성을 고르고 그 값으로 상한을 계산하면 maximization bias가 생긴다. 한 data split에서 최선 후보를 고르고 다른 split에서 그 후보의 성과를 측정해 편향을 줄인다.

# 한계와 적용

Offline lift는 online A/B test의 대체물이 아니다. 미래 분포, 사용자 간 상호작용과 capacity constraint가 달라질 수 있다. 이 사례의 핵심은 특정 loss를 복사하는 것이 아니라 목표 지표에서 역으로 data 생성 과정, confounder, baseline과 evaluation unit을 설계하는 것이다.

# 출처

- [Hyperconnect 기술 블로그 원문](https://hyperconnect.github.io/2025/11/28/how-to-set-ml-objective.html)
- [Notion 원본 항목](https://app.notion.com/p/9a41a73cf20b822392d181f95d8d2b2c)
