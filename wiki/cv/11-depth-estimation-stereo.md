---
type: Concept
title: "스테레오 매칭 및 깊이 추정 (Stereo Matching & Depth Estimation)"
description: "양안 시차(Disparity)를 이용한 3차원 깊이 맵 생성과 준전역 매칭(SGM), 단안 깊이 추정 신경망을 다룹니다."
tags: [computer-vision, stereo-vision, disparity, sgm, depth-estimation]
timestamp: 2026-08-24
status: active
---

# Summary
두 개 이상의 보정된 카메라 영상(Stereo Pair)으로부터 시차(Disparity)를 계산하여 픽셀별 물리적 거리(Depth $Z$)를 복원하는 스테레오 비전 및 단일 영상 기반 깊이 추정 기법을 다룹니다.

# Key Ideas
* **스테레오 깊이 삼각측량 공식**:
  $$Z = \frac{f \cdot B}{d}$$
  ($f$: 초점거리, $B$: 두 카메라 중심 사이의 기선 거리 Baseline, $d = x_L - x_R$: 시차 Disparity)
* **준전역 매칭 (Semi-Global Matching, SGM)**: 2D 2차원 MRF 최적화의 높은 계산 복잡도를 해결하기 위해, 8방향 또는 16방향의 1D 동적 계획법(Dynamic Programming) 경로 비용을 합산하여 고속/고품질 깊이 지도 생성.
* **단안 깊이 추정 (Monocular Depth Estimation - MiDaS, Depth Anything)**: 단일 RGB 영상만으로 원근감, 객체 크기, 음영, 텍스처 그래디언트 등의 시각적 단서를 대규모 파운데이션 모델로 학습하여 메트릭/상대 깊이 맵 예측.

# Related Concepts
* [SfM & Visual SLAM](10-sfm-and-slam.md)
* [3D Reconstruction](12-3d-reconstruction.md)
