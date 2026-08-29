---
type: Concept
title: "모션 추정 및 옵티컬 플로우 (Motion Estimation & Optical Flow)"
description: "연속된 영상 프레임 간의 픽셀 단위 2차원 겉보기 움직임 벡터장(Optical Flow) 추정 알고리즘을 다룹니다."
tags: [computer-vision, optical-flow, motion-estimation, lucas-kanade, raft]
timestamp: 2026-08-24
status: active
---

# Summary
비디오 프레임 사이에서 픽셀들의 순간적인 속도 벡터 $(u, v)$를 추정하는 고전적 및 딥러닝 기반 옵티컬 플로우 기법을 다룹니다.

# Key Ideas
* **밝기 항수성 가정 (Brightness Constancy Constraint)**:
  $$I(x, y, t) = I(x + \Delta x, y + \Delta y, t + \Delta t) \implies I_x u + I_y v + I_t = 0$$
  * 단일 픽셀 식 1개로 미지수 2개 $(u, v)$를 구할 수 없는 **구경 문제(Aperture Problem)** 발생.
* **루카스-카나데 (Lucas-Kanade, 로컬 기법)**: 작은 윈도우 내의 모든 픽셀이 동일한 모션을 가진다고 가정하고 최소제곱법으로 $(u, v)$ 해결.
* **혼-셩크 (Horn-Schunck, 전역 기법)**: 전역 평활화 정규화 항을 추가하여 변분법으로 전체 영상의 매끄러운 플로우 장 계산.
* **RAFT (Recurrent All-Pairs Field Transforms)**: 모든 픽셀 쌍의 4D 상관관계 볼륨(Correlation Volume)을 생성하고 GRU 기반 반복 갱신을 통해 고정밀 옵티컬 플로우를 예측하는 현대 SOTA 딥러닝 모델.

# Related Concepts
* [Optimization & MRF](03-optimization-and-mrf.md)
* [SfM & Visual SLAM](10-sfm-and-slam.md)
