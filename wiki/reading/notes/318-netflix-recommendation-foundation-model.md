---
type: Reference
title: "Netflix 추천 파운데이션 모델: 여러 개인화 모델의 선호 학습을 중앙화하기"
description: "긴 사용자 상호작용을 autoregressive sequence로 학습해 예측 head, embedding과 fine-tuning 기반을 함께 제공하는 추천 모델"
resource: "https://netflixtechblog.com/foundation-model-for-personalized-recommendation-1a0bd8e02d39?gi=cce3166ad8eb"
resource_aliases: [https://netflixtechblog.com/foundation-model-for-personalized-recommendation-1a0bd8e02d39]
notion: "https://app.notion.com/p/7831a73cf20b82bf9e5881292401c93d"
tags: [reading, recommender-systems, foundation-models, netflix]
timestamp: 2026-07-24
status: summarized
---

# 전환의 이유

Netflix의 개인화 시스템에는 Continue Watching, Today's Top Picks처럼 목적별 모델이 많다. 서로 비슷한 interaction data를 별도로 학습하므로 유지비가 크고 한 모델의 개선을 다른 모델로 옮기기 어렵다. 이 글은 member preference learning을 큰 foundation model에 중앙화하고, downstream model이 weight나 embedding을 공유하도록 바꾸는 방향을 설명한다.

# 추천을 언어처럼 학습하기

사용자의 재생·탐색 같은 interaction event를 token sequence로 보고 다음 interaction을 autoregressive하게 예측한다. 각 token에는 item ID뿐 아니라 locale, time, duration, device, genre와 출시 국가 같은 이질적 feature가 들어간다. 예측 시점에 아는 request-time feature와 이전 행동 뒤 알게 된 post-action feature를 구분해 leakage를 막는다.

수백 개 event의 긴 이력을 처리하기 위해 low-rank compression을 포함한 sparse attention과 겹치는 sliding-window sampling을 사용한다. 모든 행동의 가치가 같지 않으므로 하나의 다음 token만 맞히는 목적을 넘어 여러 미래 token과 장기 만족을 고려한다.

# 추천 시스템 고유 문제

새 title은 interaction이 없어 embedding을 배울 수 없는 cold start가 생긴다. 이전 모델을 warm-start하면서 새 item parameter를 추가하고, 보지 못한 entity도 metadata로 추론할 수 있게 설계한다. 재학습마다 embedding 좌표계가 임의로 회전하면 downstream 소비자가 깨질 수 있어 orthogonal low-rank transformation으로 공간을 안정화한다.

# 활용과 한계

Foundation model은 직접 prediction head로 쓰거나 user·title embedding을 batch로 만들거나, 특정 화면용 데이터로 fine-tuning할 수 있다. 하지만 거대한 공통 모델은 장애와 편향의 영향 범위도 키운다. Offline metric뿐 아니라 다양성, 장기 만족, cold-start와 presentation bias를 online experiment로 검증하고, 민감한 시청 이력의 privacy와 retention을 관리해야 한다.

# 출처

- [Netflix TechBlog 원문](https://netflixtechblog.com/foundation-model-for-personalized-recommendation-1a0bd8e02d39)
