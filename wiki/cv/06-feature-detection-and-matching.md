---
type: Concept
title: "특징 검출 및 기술자 매칭 (Feature Detection & Matching)"
description: "기하학적 변화와 조명 변화에 불변인 특징점 검출(Harris, SIFT, ORB)과 특징 기술자 매칭 기법을 다룹니다."
tags: [computer-vision, feature-detection, sift, orb, harris-corner, descriptors]
timestamp: 2026-08-24
status: active
---

# Summary
서로 다른 시점이나 조명에서 촬영된 두 영상 사이의 대응 관계(Correspondence)를 찾기 위한 국소 특징점(Local Keypoints) 검출 및 기술자(Descriptors) 추출, 매칭 알고리즘을 다룹니다.

# Key Ideas
* **해리스 코너 (Harris Corner Detector)**: 2D 구조 텐서(Structure Tensor)의 두 고윳값 $\lambda_1, \lambda_2$를 평가하여 모든 방향으로 그래디언트 변화가 큰 코너 지점 탐지 ($R = \det(M) - k \cdot \text{tr}(M)^2$).
* **SIFT (Scale-Invariant Feature Transform)**:
  1. DoG(Difference of Gaussians) 피라미드에서 스케일 공간 극값 탐색 (스케일 불변성)
  2. 주요 방향 할당 (회전 불변성)
  3. $16 \times 16$ 윈도우 내 $4 \times 4$ 셀별 8방향 그래디언트 히스토그램 생성 (128차원 기술자)
* **ORB (Oriented FAST and Rotated BRIEF)**: 고속 FAST 코너 검출 + 강도 중심(Intensity Centroid) 기반 방향 계산 + 바이너리 기술자 BRIEF. 모바일 및 실시간 SLAM에 최적화.
* **기술자 매칭**: 유클리드 거리 / 해밍 거리(Hamming Distance), FLANN 고속 최근접 이웃 탐색, Lowe's Ratio Test ($d_1 / d_2 < 0.75$)를 통한 이상치 제거.

# Related Concepts
* [Image Alignment & Stitching](07-image-alignment-and-stitching.md)
* [SfM & Visual SLAM](10-sfm-and-slam.md)
