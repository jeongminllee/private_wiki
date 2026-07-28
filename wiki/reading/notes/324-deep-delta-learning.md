---
type: Paper Note
title: "Deep Delta Learning: 잔차 연결을 지우기와 쓰기로 일반화하기"
description: "identity addition 대신 rank-1 Delta Operator로 깊이 방향의 기억 보존·망각·반전을 조절하는 이론"
resource: "https://yifanzhang-pro.github.io/deep-delta-learning/"
notion: "https://app.notion.com/p/8d91a73cf20b82d89acd816fc0f9ef0c"
tags: [reading, paper, deep-learning, architecture, delta-rule]
timestamp: 2026-07-24
status: summarized
---

# 핵심 아이디어

표준 residual connection은 이전 표현에 새 값을 더한다. Deep Delta Learning은 이 항등·가산 구조가 항상 적합하다는 가정을 풀고, 깊이 방향으로 기존 성분을 지운 뒤 새 성분을 쓰는 Delta Operator를 제안한다.

`A = I - βkkᵀ`를 사용하면 update는 `Xₗ₊₁ = (I - βkkᵀ)Xₗ + βkvᵀ`가 된다. 이는 `Xₗ + βk(vᵀ - kᵀXₗ)` 형태의 depth-wise Delta Rule로도 볼 수 있다.

# β의 의미

Operator의 spectrum은 `{1, ..., 1, 1-β}`다. `β → 0`이면 identity에 가까워 기억을 보존하고, `β → 1`이면 특정 방향을 projection으로 제거한 뒤 새 값을 쓴다. `β → 2`이면 Householder reflection과 연결되어 음의 eigenvalue를 갖는 반전·진동 dynamics를 표현할 수 있다.

# 왜 흥미로운가

Residual stream을 계속 누적하는 대신 layer마다 어떤 feature를 유지하고 교체할지 gate로 제어한다. 시간축 sequence memory에 쓰이는 DeltaNet의 delta rule을 network depth 방향으로 옮겼다는 관점도 제공한다.

# 확인할 점

Project page는 주로 이론 구조를 설명한다. 실제 모델에서의 계산량, 학습 안정성, 기존 residual architecture 대비 품질은 논문의 전체 실험과 독립 재현으로 확인해야 한다. `β`가 큰 구간의 gradient와 진동이 장기 학습에서 어떤 영향을 주는지도 중요하다.

# 출처

- [Deep Delta Learning 프로젝트](https://yifanzhang-pro.github.io/deep-delta-learning/)
- [arXiv 논문](https://arxiv.org/abs/2601.00417)
