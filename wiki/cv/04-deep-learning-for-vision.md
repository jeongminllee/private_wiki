---
type: Concept
title: "비전을 위한 딥러닝 기초 (Deep Learning for Vision)"
description: "CNN 백본 아키텍처의 진화, Vision Transformer(ViT) 및 비전 태스크를 위한 딥러닝 최적화 기법을 정리합니다."
tags: [computer-vision, deep-learning, cnn, resnet, vit, transformer]
timestamp: 2026-08-24
status: active
---

# Summary
영상 데이터를 효율적으로 학습하기 위한 신경망 구조의 진화 과정을 다룹니다. 전통적 합성곱 신경망(LeNet, AlexNet, VGG, ResNet, ConvNeXt)부터 패치 기반 어텐션을 적용한 Vision Transformer(ViT, Swin Transformer)와 자기지도학습(MAE, DINO)을 포괄합니다.

# Key Ideas
* **ResNet과 잔차 연결 (Residual Connection)**: $y = F(x, W) + x$ 스킵 커넥션을 통해 100계층 이상의 심층 신경망에서 기울기 소실(Vanishing Gradient) 문제를 해결.
* **Vision Transformer (ViT)**: 이미지를 $16 \times 16$ 패치로 분할하여 1D 시퀀스 토큰으로 변환한 후 표준 Transformer Encoder에 통과. 대규모 데이터셋 사전학습 시 CNN을 능가하는 전역적 수용 영역(Receptive Field) 확보.
* **계층적 구조 (Swin Transformer)**: 윈도우 기반 로컬 셀프 어텐션과 패치 병합을 통해 선형 복잡도 $O(N)$ 달성 및 Dense Prediction 태스크에 최적화.

# Related Concepts
* [Recognition & VLM](05-recognition-and-vlm.md) - 비전 백본을 활용한 객체 검출 및 멀티모달 모델
