---
type: Paper Note
title: "mHC: Manifold-Constrained Hyper-Connections"
description: "Hyper-Connections의 표현력을 유지하면서 항등 사상, 학습 안정성, 확장성을 회복하려는 잔차 연결 구조"
resource: https://arxiv.org/abs/2512.24880v1
notion: https://app.notion.com/p/d251a73cf20b82ab9aa40154246ef3d7
tags: [paper, llm-architecture, residual-connections, training-stability]
timestamp: 2026-07-24
status: summarized
---

# One-line Summary

mHC는 넓어진 residual stream과 다양한 연결을 쓰는 Hyper-Connections를 특정 manifold에 투영해 잔차 연결의 항등 사상 성질을 되살리고 대규모 학습 안정성을 높이려는 구조다.

# Problem

Hyper-Connections는 residual stream 폭과 연결 패턴을 확장해 표현력을 높이지만, 전통적인 잔차 연결의 identity mapping을 훼손할 수 있다. 저자들은 이것이 학습 불안정, 확장성 제한, 추가 메모리 접근 비용으로 이어진다고 본다.

# Method

연결 공간에 수학적 제약을 두어 변환이 안정적인 manifold 위에 머물게 한다. 구조적 제약만 제안하는 데 그치지 않고 실제 대규모 학습에서 메모리 접근 비용을 줄이기 위한 구현 최적화도 함께 다룬다.

# Key Findings

저자들의 실험에서는 mHC가 규모가 커질 때 더 안정적으로 학습되고 Hyper-Connections의 성능 이점을 유지하거나 개선한다고 보고한다. 다만 이 문서가 저장한 링크는 v1이며 arXiv에는 2026년 1월 5일 v2가 올라와 있다.

# My Understanding

잔차 연결은 단순한 덧셈이 아니라 깊은 네트워크에서 신호와 기울기가 지나가는 안정적인 기본 경로다. 연결을 더 표현력 있게 만들 때도 이 기본 경로가 보존되는지를 먼저 확인해야 한다는 연구로 읽을 수 있다.

# Open Questions

- 다른 모델 규모와 데이터 분포에서도 같은 안정성 이득이 유지되는가
- 이론적 제약이 실제 학습 처리량과 메모리에 주는 비용은 얼마인가
- 일반적인 Transformer 학습 스택에서 재현 가능한 구현이 제공되는가

# Citations

- [arXiv v1](https://arxiv.org/abs/2512.24880v1)
- [arXiv 최신 버전](https://arxiv.org/abs/2512.24880)

