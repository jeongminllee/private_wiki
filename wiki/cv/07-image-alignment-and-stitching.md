---
type: Concept
title: "영상 정합 및 파노라마 스티칭 (Image Alignment & Stitching)"
description: "호모그래피 변환 추정, RANSAC 이상치 제거 및 매끄러운 파노라마 영상 모자이킹 기술을 다룹니다."
tags: [computer-vision, alignment, stitching, homography, ransac, panorama]
timestamp: 2026-08-24
status: active
---

# Summary
여러 장의 겹치는 영상들을 하나의 연속된 고해상도 파노라마(Panorama) 영상으로 합성하는 전 과정을 다룹니다. 특징점 매칭 기반 호모그래피 추정, RANSAC 강건 모델 피팅, 카메라 회전 전역 정합, 시임 카빙(Seam Carving) 및 멀티밴드 블렌딩(Multiband Blending)을 포함합니다.

# Key Ideas
* **RANSAC (Random Sample Consensus)**: 수많은 오매칭(Outliers)이 존재하는 상황에서 최소 표본(호모그래피의 경우 4점)을 무작위 추출하여 인라이어(Inliers)가 최대가 되는 최적 변환 모델을 추정.
* **원통형/구면 투영 (Cylindrical / Spherical Warping)**: 360도 전방향 파노라마를 위해 평면 투영 대신 원통형 좌표계로 좌표 변환.
* **멀티밴드 블렌딩 (Multiband Blending)**: 라플라시안 피라미드를 이용해 저주파 성분(명암 차이)은 넓게 블렌딩하고 고주파 성분(디테일)은 좁게 합성하여 접합부 경계선(Seam)과 고스팅(Ghosting) 현상을 완벽히 제거.

# Related Concepts
* [Feature Detection & Matching](06-feature-detection-and-matching.md)
* [Image Processing](02-image-processing.md) - 피라미드 기반 영상 합성
