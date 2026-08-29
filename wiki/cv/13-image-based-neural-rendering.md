---
type: Concept
title: "영상 기반 및 신경 렌더링 (Image-Based & Neural Rendering)"
description: "광선장(Light Field) 이론부터 NeRF(Neural Radiance Fields), 3D Gaussian Splatting(3D-GS)에 이르는 차세대 시점 합성(Novel View Synthesis) 및 3D 렌더링 기술을 다룹니다."
tags: [computer-vision, neural-rendering, nerf, 3d-gaussian-splatting, view-synthesis, radiance-fields]
timestamp: 2026-08-24
status: active
---

# Summary
다양한 각도에서 촬영된 2D 사진들로부터 새로운 시점(Novel View)에서의 사실적인 고해상도 영상을 실시간으로 렌더링하는 영상 기반 렌더링(IBR)과 신경 렌더링(Neural Rendering) 기술을 다룹니다. 전통적인 광선장(Light Field) 및 텍스처 매핑부터 볼륨 렌더링 기반 NeRF(Neural Radiance Fields), 격자 가속 기법(Instant-NGP), 그리고 미분 가능한 래스터라이제이션 기반의 3D Gaussian Splatting(3D-GS)을 포괄합니다.

# Why it matters
* **실감형 3D 콘텐츠 제작 혁신**: 복잡한 수작업 3D 모델링 없이 실사 사진 수십 장만으로 영화급 3D 에셋 및 가상 공간 생성.
* **디지털 트윈 및 VR/AR**: 물리적 현실 환경을 그대로 복제하여 실시간 탐색 가능한 초사실적 공간 렌더링 제공.

# Key Ideas

## 1. 광선장 및 전통 IBR (Light Fields & Image-Based Rendering)
공간 내의 모든 위치 $(x, y, z)$에서 모든 방향 $(\theta, \phi)$으로 이동하는 빛의 강도를 5D 플레놉틱 함수(Plenoptic Function)로 모델링하고, 자유 공간에서 4D Light Field ($L(u, v, s, t)$)로 축소하여 새로운 시점 합성.

## 2. NeRF (Neural Radiance Fields)
3차원 연속 공간을 MLP(다층 퍼셉트론) 가중치 $\Theta$로 표현:

$$
F_\Theta : (\mathbf{x}, \mathbf{d}) \rightarrow (\mathbf{c}, \sigma)
$$
* $\mathbf{x} = (x, y, z)$: 3D 공간 위치
* $\mathbf{d} = (\theta, \phi)$: 시선 방향 (Viewing direction)
* $\mathbf{c} = (r, g, b)$: 방출 색상
* $\sigma$: 볼륨 밀도 (Volume density, 투과도)

### 볼륨 렌더링 방정식 (Volume Rendering Equation)
카메라 광선 $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$을 따라 누적 투과율 $T(t)$와 볼륨 렌더링 적분을 수행하여 픽셀 색상 $C(\mathbf{r})$을 합성:

$$
C(\mathbf{r}) = \int_{t_n}^{t_f} T(t) \sigma(\mathbf{r}(t)) \mathbf{c}(\mathbf{r}(t), \mathbf{d}) dt, \quad \text{where } T(t) = \exp\left(-\int_{t_n}^{t} \sigma(\mathbf{r}(s)) ds\right)
$$

* **Positional Encoding (위치 인코딩)**: 고주파 디테일(선명한 에지, 질감)을 학습하기 위해 푸리에 특성 함수 $\gamma(p) = [\sin(2^k \pi p), \cos(2^k \pi p)]$ 매핑 적용.
* **가속화 기법**: Instant-NGP(다해상도 해시 그리드 인코딩), TensoRF, Zip-NeRF.

## 3. 3D Gaussian Splatting (3D-GS)
NeRF의 느린 렌더링 속도(광선당 수백 번 MLP 호출)를 해결하기 위해, 장면을 수백만 개의 **3차원 비등방성 가우시안 타원체(3D Gaussians)**로 표현하고 하드웨어 가속 미분 가능 타일 래스터라이저를 통해 **실시간 100+ FPS** 렌더링 달성.

각 3D 가우시안 $G(\mathbf{x})$의 파라미터:
* **위치 (Position $\mu$)**: 3D 중심점
* **공분산 행렬 (Covariance $\Sigma = R S S^T R^T$)**: 회전 쿼터니언 $q$, 스케일 벡터 $s$
* **불투명도 (Opacity $\alpha$)**: 0~1 값
* **색상 (Spherical Harmonics, SH)**: 시점 의존적 색상 표현을 위한 구면 조화 함수 계수

# Related Concepts
* [Image Formation](01-image-formation.md) - 카메라 투영 및 광선 생성
* [SfM & Visual SLAM](10-sfm-and-slam.md) - COLMAP을 통한 카메라 포즈 전처리
* [3D Reconstruction](12-3d-reconstruction.md) - 메시 및 볼륨 표현 기법

# Citations
* Richard Szeliski, *Computer Vision: Algorithms and Applications (2nd Edition)*, Chapter 14: Image-based rendering.
* Mildenhall et al., *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*, ECCV 2020.
* Kerbl et al., *3D Gaussian Splatting for Real-Time Radiance Field Rendering*, SIGGRAPH 2023.
