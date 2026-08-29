---
type: Reference
title: "Computer Vision Study Dashboard (컴퓨터 비전 종합 지식 대시보드)"
description: "Richard Szeliski의 《Computer Vision: Algorithms and Applications (2nd Edition)》을 기반으로 전통 영상 처리, 기하학적 3D 비전, 딥러닝 인식 및 신경 렌더링까지 체계화한 컴퓨터 비전 종합 지식 대시보드입니다."
tags: [computer-vision, deep-learning, image-processing, 3d-vision, slam, vlm, nerf, index, reference]
timestamp: 2026-08-24
status: active
---

# Computer Vision Study Dashboard

Richard Szeliski의 컴퓨터 비전 표준 교과서인 **《Computer Vision: Algorithms and Applications (2nd Edition)》**의 핵심 이론과 수식, 최신 딥러닝·VLM 및 3D 기하·렌더링 기법을 총망라한 지식 대시보드입니다.

---

## 📚 챕터별 핵심 지식 문서

### Part 1. 영상 형성 및 기초 신호 처리 (Foundations)
- **[01. 영상 형성과 카메라 모델 (Image Formation & Camera Models)](01-image-formation.md)** - 2D/3D 기하 변환(Homography), 광도학적 형성, 핀홀/원근 카메라 투영 행렬($P = K[R|t]$), 렌즈 왜곡
- **[02. 영상 처리 및 주파수 변환 (Image Processing & Frequency Transforms)](02-image-processing.md)** - 공간 필터링(가우시안, 미분 필터), 2D 푸리에 변환, 가우시안/라플라시안 이미지 피라미드, 웨이블릿

### Part 2. 최적화 및 딥러닝 기반 시각 인식 (Optimization & Recognition)
- **[03. 모델 피팅 및 최적화 (Model Fitting & Optimization)](03-optimization-and-mrf.md)** - 변분법, 마르코프 랜덤 필드(MRF), 그래프 컷(Graph Cuts), 에너지 최소화 기법
- **[04. 비전을 위한 딥러닝 기초 (Deep Learning for Vision)](04-deep-learning-for-vision.md)** - CNN 아키텍처(ResNet, ConvNeXt), Vision Transformer(ViT), 손실 함수 및 최적화
- **[05. 시각 인식 및 비전-언어 모델 (Recognition & Vision-Language Models)](05-recognition-and-vlm.md)** - 객체 검출(Faster R-CNN, YOLO, DETR), 시맨틱/인스턴스 분할, 비디오 이해, **Vision-Language Model(VLM / LMM)**

### Part 3. 특징 추출, 정합 및 모션 분석 (Features & Motion)
- **[06. 특징 검출 및 기술자 매칭 (Feature Detection & Matching)](06-feature-detection-and-matching.md)** - 해리스 코너(Harris Corner), SIFT, ORB, 에지/외곽선 검출(Canny), 특징 기술자 매칭
- **[07. 영상 정합 및 파노라마 스티칭 (Image Alignment & Stitching)](07-image-alignment-and-stitching.md)** - 호모그래피 추정, RANSAC 강건 추정, 전역 정합, 이미지 블렌딩 및 모자이킹
- **[08. 모션 추정 및 옵티컬 플로우 (Motion Estimation & Optical Flow)](08-motion-and-optical-flow.md)** - 루카스-카나데(Lucas-Kanade), 혼-셩크(Horn-Schunck), 계층적 모션, 딥러닝 기반 Optical Flow(RAFT)

### Part 4. 3D 기하 비전 및 재구성 (3D Vision, Geometry & SLAM)
- **[09. 컴퓨테이셔널 포토그래피 (Computational Photography)](09-computational-photography.md)** - HDR 이미징, 초해상화(Super-Resolution), 디노이징, 인페인팅, 이미지 매팅(Matting)
- **[10. SfM 및 시각 SLAM (Structure from Motion & Visual SLAM)](10-sfm-and-slam.md)** - 에피폴라 기하(Epipolar Geometry), 본질/기초 행렬($E, F$), 2-뷰/다중뷰 SfM, 번들 조정(Bundle Adjustment), Visual SLAM(ORB-SLAM)
- **[11. 스테레오 매칭 및 깊이 추정 (Stereo Matching & Depth Estimation)](11-depth-estimation-stereo.md)** - 스테레오 시차(Disparity), 준전역 매칭(SGM), 다중뷰 스테레오(MVS), 단안 깊이 추정(Monocular Depth)
- **[12. 3D 형상 재구성 (3D Reconstruction)](12-3d-reconstruction.md)** - Shape from X, 포인트 클라우드, 복셀/TSDF 기반 볼륨 재구성, 메시(Mesh) 생성(Marching Cubes)
- **[13. 영상 기반 및 신경 렌더링 (Image-Based & Neural Rendering)](13-image-based-neural-rendering.md)** - 광선장(Light Field), 신경 방사 휘도장(NeRF - Neural Radiance Fields), 3D 가우시안 스플래팅(3D-GS)

---

## 🔗 관련 인덱스 및 지식 연결
- [ML Study Dashboard](../ml/index.md) - 머신러닝 & 딥러닝 종합 지식 대시보드
- [Algorithms Dashboard](../algorithms/index.md) - 자료구조 & 알고리즘
- [Root Wiki Index](../../index.md) - 전체 지식베이스 루트 인덱스
