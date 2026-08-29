---
type: Concept
title: "영상 형성과 카메라 모델 (Image Formation & Camera Models)"
description: "3차원 물리적 세계가 2차원 디지털 영상으로 투영되는 기하학적·광도학적 원리와 카메라 내부/외부 파라미터, 왜곡 모델을 다룹니다."
tags: [computer-vision, image-formation, camera-model, homography, pinhole, distortion]
timestamp: 2026-08-24
status: active
---

# Summary
3차원 세계의 점이 카메라 렌즈와 센서를 거쳐 2D 픽셀 좌표로 변환되는 수학적·물리적 모델을 정의합니다. 핀홀 카메라 모델, 내부 파라미터(Intrinsic), 외부 파라미터(Extrinsic), 투영 변환(Perspective Projection), 호모그래피(Homography), 렌즈 왜곡(Radial/Tangential Distortion) 및 광도학적 영상 형성(BRDF, 방사도, 복사도)을 다룹니다.

# Why it matters
* **3D 비전의 절대적 기반**: SLAM, 자율주행, 3D 재구성, NeRF 등 모든 3D 비전 시스템은 정확한 카메라 투영 모델과 왜곡 보정 없이는 동작할 수 없습니다.
* **센서 좌표계와 물리 좌표계의 다리**: 로봇 팔, 자율주행 차량 센서 융합에서 픽셀 단위 측정값을 실제 3차원 물리적 거리(m)로 변환하는 핵심 기준입니다.

# Key Ideas

## 1. 2D 및 3D 기하 변환 (Geometric Transformations)
동차 좌표계(Homogeneous Coordinates)를 사용하여 평행 이동, 회전, 스케일링, 아핀, 사영 변환을 일관된 행렬 곱으로 표현합니다.

$$
\tilde{\mathbf{x}} = \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}, \quad \tilde{\mathbf{x}}' = H \tilde{\mathbf{x}}
$$

* **유클리드 변환 (Isometry/Rigid)**: 회전 $R$과 평행이동 $t$ (3 DOF), 길이와 각도 보존
* **유사 변환 (Similarity)**: 회전 + 평행이동 + 등방 스케일 $s$ (4 DOF), 각도 보존
* **아핀 변환 (Affine)**: 평행선 보존 (6 DOF)
* **사영 변환 (Projective / Homography)**: 직선 보존 (8 DOF), 임의의 3D 평면 간 투영 관계

## 2. 핀홀 카메라 투영 모델 (Pinhole Camera Model)
3D 월드 좌표계 상의 점 $\mathbf{P}_w = [X_w, Y_w, Z_w, 1]^T$를 2D 픽셀 좌표 $\mathbf{p} = [u, v, 1]^T$로 변환하는 관계식:

$$
s \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \begin{bmatrix} R & \mathbf{t} \end{bmatrix} \begin{bmatrix} X_w \\ Y_w \\ Z_w \\ 1 \end{bmatrix} = P \mathbf{P}_w
$$

### 내부 파라미터 행렬 (Intrinsic Matrix $K$)
$$
K = \begin{bmatrix} f_x & s & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}
$$
* $f_x, f_y$: 초점 거리(focal length in pixel units, $f_x = f / s_x$)
* $c_x, c_y$: 주점(principal point, 센서 중심 픽셀 좌표)
* $s$: 비대칭 왜곡(skew factor, 통상 0)

### 외부 파라미터 (Extrinsic Parameters $[R | \mathbf{t}]$)
월드 좌표계를 카메라 중심 좌표계로 변환하는 3차원 회전 행렬 $R \in SO(3)$ 및 평행 이동 벡터 $\mathbf{t} \in \mathbb{R}^3$.

## 3. 렌즈 왜곡 모델 (Lens Distortion)
실제 광학 렌즈에서 발생하는 비선형 왜곡을 보정하기 위해 정규화 좌표 $(x_n, y_n)$에 왜곡 함수를 적용합니다 ($r^2 = x_n^2 + y_n^2$):

* **방사 왜곡 (Radial Distortion)**: 렌즈 형상으로 인해 외곽으로 갈수록 휘어지는 현상 (배럴/핀쿠션 왜곡)
  $$x_{distorted} = x_n (1 + k_1 r^2 + k_2 r^4 + k_3 r^6)$$
  $$y_{distorted} = y_n (1 + k_1 r^2 + k_2 r^4 + k_3 r^6)$$
* **접선 왜곡 (Tangential Distortion)**: 렌즈와 센서 평면이 완벽히 평행하지 않아 발생
  $$x_{distorted} = x_{distorted} + [2 p_1 x_n y_n + p_2 (r^2 + 2 x_n^2)]$$
  $$y_{distorted} = y_{distorted} + [p_1 (r^2 + 2 y_n^2) + 2 p_2 x_n y_n]$$

## 4. 광도학적 형성 (Photometric Image Formation)
* **복사도(Radiance)와 조도(Irradiance)**: 광원에서 방출된 빛이 물체 표면에 도달하여 반사되고, 카메라 센서에 맺히는 광량 전달 물리식.
* **BRDF (Bidirectional Reflectance Distribution Function)**: 입사각 $(\theta_i, \phi_i)$에 따른 반사 방향 $(\theta_r, \phi_r)$으로의 반사 비율을 모델링 (람베르시안 난반사 vs 거울면 정반사).

# Examples

```python
import cv2
import numpy as np

# 카메라 내부 행렬 및 왜곡 계수 예제
K = np.array([[800, 0, 320],
              [0, 800, 240],
              [0,   0,   1]], dtype=np.float32)
dist_coeffs = np.array([-0.2, 0.05, 0, 0, 0], dtype=np.float32)

# 이미지 왜곡 보정 (Undistortion)
# undistorted_img = cv2.undistort(img, K, dist_coeffs)
```

# Related Concepts
* [Image Processing](02-image-processing.md) - 왜곡 보정 이후 영상 필터링 및 전처리
* [Feature Detection & Matching](06-feature-detection-and-matching.md) - 영상 정합을 위한 기하학적 제약 조건
* [SfM & Visual SLAM](10-sfm-and-slam.md) - 카메라 파라미터 기반 3D 궤적 추정

# Citations
* Richard Szeliski, *Computer Vision: Algorithms and Applications (2nd Edition)*, Chapter 2: Image formation.
