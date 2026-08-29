---
type: Concept
title: "영상 처리 및 주파수 변환 (Image Processing & Frequency Transforms)"
description: "픽셀 점 연산, 공간 도메인 선형 필터링, 푸리에 변환 및 다해상도 피라미드 기법을 다룹니다."
tags: [computer-vision, image-processing, filtering, fourier, pyramid, wavelets]
timestamp: 2026-08-24
status: active
---

# Summary
영상 신호의 화질 개선, 노이즈 제거, 에지 검출 및 다해상도 표현을 위한 핵심 영상 처리 기법을 정리합니다. 점 연산(히스토그램 평활화, 감마 보정), 공간 선형 필터링(가우시안, 소벨, 라플라시안, 양방향 필터), 2D 이산 푸리에 변환(DFT), 그리고 가우시안/라플라시안 이미지 피라미드를 다룹니다.

# Key Ideas
* **공간 필터링과 컨볼루션**: 가우시안 블러를 통한 고주파 노이즈 제거, Sobel/Prewitt 마스크를 통한 1차 미분 그래디언트 계산, Laplacian of Gaussian(LoG)을 통한 2차 미분 제로 크로싱.
* **양방향 필터 (Bilateral Filter)**: 공간 거리 가중치 + 픽셀 밝기 차이 가중치를 동시에 적용하여 에지를 보존하면서 노이즈를 제거.
* **주파수 도메인 분석 (2D Fourier Transform)**: 영상의 공간 주파수 성분 분해 및 저주파/고주파 통과 필터링. 컨볼루션 정리 ($f * g \iff F \cdot G$).
* **이미지 피라미드 (Image Pyramids)**:
  * **가우시안 피라미드**: 블러링 후 다운샘플링 (다해상도 스케일 스페이스 생성)
  * **라플라시안 피라미드**: 가우시안 피라미드 레벨 간 차분 영상 (대역 통과 표현, 이미지 압축 및 블렌딩에 활용)

# Related Concepts
* [Image Formation](01-image-formation.md)
* [Feature Detection & Matching](06-feature-detection-and-matching.md) - DoG(Difference of Gaussians) 기반 SIFT 특징점 검출
