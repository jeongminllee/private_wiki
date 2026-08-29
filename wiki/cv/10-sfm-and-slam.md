---
type: Concept
title: "SfM 및 시각 SLAM (Structure from Motion & Visual SLAM)"
description: "다중 시점 영상으로부터 카메라의 3차원 자세(동작)와 장면의 3차원 구조를 동시에 복원하는 SfM과 실시간 Visual SLAM 알고리즘을 다룹니다."
tags: [computer-vision, sfm, slam, epipolar-geometry, bundle-adjustment, 3d-vision]
timestamp: 2026-08-24
status: active
---

# Summary
연속된 2D 영상들로부터 카메라의 6자유도 자세(6-DoF Pose)와 3D 공간상의 점들의 위치를 동시에 복원하는 Structure from Motion(SfM) 및 실시간 동시적 위치추정 및 지도작성(Visual SLAM)의 수학적 기초를 다룹니다. 에피폴라 기하(Epipolar Geometry), 기초 행렬($F$), 본질 행렬($E$), 삼각측량(Triangulation), PnP(Perspective-n-Point), 번들 조정(Bundle Adjustment) 및 루프 클로징(Loop Closing)을 포괄합니다.

# Why it matters
* **자율주행 및 로봇 내비게이션**: GPS 음영 구역(실내, 터널 등)에서 정밀한 자가 위치 추정의 핵심 기술입니다.
* **AR/VR 및 메타버스**: 공간 트래킹 및 가상 객체의 물리적 정렬을 위한 공간 컴퓨팅의 뼈대입니다.
* **3D 맵핑 및 재구성 파이프라인(NeRF/3D-GS)의 전처리**: NeRF 학습에 필요한 카메라 포즈를 COLMAP 등의 SfM으로 계산합니다.

# Key Ideas

## 1. 2-뷰 에피폴라 기하 (Epipolar Geometry)
두 시점 $C_1, C_2$에서 동일한 3D 점 $\mathbf{P}$를 관측할 때 성립하는 기하학적 제약 조건:

$$
\mathbf{x}_2^T E \mathbf{x}_1 = 0 \quad (정규화 좌표계)
$$
$$
\mathbf{p}_2^T F \mathbf{p}_1 = 0 \quad (픽셀 좌표계, F = K_2^{-T} E K_1^{-1})
$$

* **본질 행렬 (Essential Matrix $E = [\mathbf{t}]_\times R$)**: 5 DOF (회전 3 + 평행이동 방향 2). 5-점 알고리즘 또는 8-점 알고리즘으로 추정.
* **기초 행렬 (Fundamental Matrix $F$)**: 카메라 내부 파라미터를 모를 때 픽셀 좌표 매칭점 8개로 추정 (8-point algorithm).

## 2. 3D 점 복원: 삼각측량 (Triangulation)
두 카메라 포즈 $P_1, P_2$와 대응점 $\mathbf{p}_1, \mathbf{p}_2$가 주어졌을 때 DLT(Direct Linear Transformation) 또는 최적 재투영 오차 최소화를 통해 3D 점 $\mathbf{P}$를 계산.

## 3. 새로운 프레임 포즈 추정: PnP (Perspective-n-Point)
이미 3D 좌표가 알려진 $n$개의 점과 현재 영상의 2D 대응점 간의 관계로부터 카메라의 자세 $(R, \mathbf{t})$를 계산 (EPnP, P3P + RANSAC).

## 4. 전역 최적화: 번들 조정 (Bundle Adjustment, BA)
모든 3D 점 $\mathbf{X}_j$와 모든 카메라 포즈 $C_i$에 대해 관측된 픽셀 좌표 $\mathbf{x}_{ij}$와의 재투영 오차(Reprojection Error)를 비선형 최소제곱법(Levenberg-Marquardt, Ceres Solver)으로 전역 최적화:

$$
\min_{C_i, \mathbf{X}_j} \sum_{i} \sum_{j} \rho\left( \| \mathbf{x}_{ij} - \pi(C_i, \mathbf{X}_j) \|^2 \right)
$$

## 5. Visual SLAM 아키텍처 (ORB-SLAM 계열)
* **Tracking**: 프레임 단위 특징점 추출 및 PnP 기반 실시간 카메라 포즈 추적
* **Local Mapping**: 로컬 키프레임들 간의 Local Bundle Adjustment 및 3D 점 지도 확장
* **Loop Closing**: DBoW(Bag of Words) 기반 과거 방문 장소 인식 $\rightarrow$ Sim(3) 정합 $\rightarrow$ 누적 오차 교정(Pose Graph Optimization)

# Related Concepts
* [Image Formation](01-image-formation.md) - 카메라 투영 행렬 $P = K[R|t]$
* [Feature Detection & Matching](06-feature-detection-and-matching.md) - ORB/SIFT 특징점 매칭
* [Depth Estimation](11-depth-estimation-stereo.md) - 깊이 지도 및 MVS
* [Neural Rendering](13-image-based-neural-rendering.md) - NeRF/3D-GS를 위한 포즈 입력

# Citations
* Richard Szeliski, *Computer Vision: Algorithms and Applications (2nd Edition)*, Chapter 11: Structure from motion and SLAM.
