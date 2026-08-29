---
type: Concept
title: "3D 형상 재구성 (3D Reconstruction)"
description: "포인트 클라우드, 복셀 격자, TSDF 및 메시(Mesh)를 활용한 3차원 표면 및 볼륨 재구성 기법을 다룹니다."
tags: [computer-vision, 3d-reconstruction, point-cloud, tsdf, marching-cubes, mesh]
timestamp: 2026-08-24
status: active
---

# Summary
다중 시점 깊이 맵이나 센서 데이터로부터 실세계 물체와 환경의 완전한 3차원 기하 구조(Surface & Volume)를 디지털 데이터로 복원하는 알고리즘을 다룹니다.

# Key Ideas
* **포인트 클라우드 처리 (Point Cloud Processing)**: ICP(Iterative Closest Point) 알고리즘을 이용한 3D 포인트 클라우드 정합, 노이즈 필터링, 법선 벡터(Normal) 추정.
* **TSDF (Truncated Signed Distance Function)**: 연속된 깊이 프레임을 실시간으로 복셀 볼륨에 누적 융합 (KinectFusion).
* **메시 추출 (Marching Cubes Algorithm)**: 3D 스칼라 장(TSDF 볼륨)에서 등가 표면(Isosurface)을 찾아 삼각형 메시(Triangle Mesh)를 고속 생성.
* **포아송 표면 재구성 (Poisson Surface Reconstruction)**: 방향성 점 구름으로부터 연속적인 지시 함수(Indicator Function)를 편미분 방정식으로 풀어 완벽한 닫힌 방수(Watertight) 메시 표면 복원.

# Related Concepts
* [Stereo Matching & Depth](11-depth-estimation-stereo.md)
* [Image-Based & Neural Rendering](13-image-based-neural-rendering.md)
