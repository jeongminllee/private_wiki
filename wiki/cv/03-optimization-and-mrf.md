---
type: Concept
title: "모델 피팅 및 최적화 (Model Fitting & Optimization)"
description: "불연속적 시각 문제를 확률적으로 모델링하고 전역 최적해를 구하는 변분법, 마르코프 랜덤 필드(MRF), 그래프 컷 기법을 다룹니다."
tags: [computer-vision, optimization, mrf, graph-cuts, energy-minimization]
timestamp: 2026-08-24
status: active
---

# Summary
세그멘테이션, 스테레오 매칭, 옵티컬 플로우와 같은 컴퓨터 비전의 역문제(Inverse Problems)를 에너지 최소화 문제로 정식화하고 해결하는 최적화 기법을 다룹니다.

# Key Ideas
* **에너지 함수 정식화**: $E(f) = E_{data}(f) + \lambda E_{smooth}(f)$ (데이터 적합도 항 + 평활화 정규화 항).
* **Markov Random Fields (MRF)**: 픽셀 간 국소적 상호의존성을 그래프 모델로 표현.
* **그래프 컷 (Graph Cuts)**: 최대 유량/최소 컷(Max-Flow/Min-Cut) 알고리즘을 이용해 비볼록(Non-convex) 2진 레이블링 문제의 전역 최적해를 다항 시간에 계산 ($s-t$ Cut). GrabCut 영상 분할의 핵심 원리.
* **신념 전파 (Belief Propagation)**: 트리 및 일반 그래프에서 주변 확률 분포를 메시지 전달 방식으로 근사 추론.

# Related Concepts
* [Stereo Matching & Depth](11-depth-estimation-stereo.md) - SGM 및 MRF 기반 스테레오 최적화
* [Motion Estimation](08-motion-and-optical-flow.md) - 전역 광학 흐름 정규화
