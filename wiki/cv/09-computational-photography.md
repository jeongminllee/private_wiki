---
type: Concept
title: "컴퓨테이셔널 포토그래피 (Computational Photography)"
description: "HDR 영상 합성, 초해상화(SR), 이미지 디노이징, 인페인팅 및 매팅(Matting) 기술을 다룹니다."
tags: [computer-vision, computational-photography, hdr, super-resolution, inpainting, matting]
timestamp: 2026-08-24
status: active
---

# Summary
단순한 물리적 광학 렌즈의 한계를 컴퓨팅 알고리즘으로 극복하여 사람의 눈이 인지하는 수준 이상의 고품질 영상을 생성하는 기술들을 정리합니다.

# Key Ideas
* **HDR (High Dynamic Range) 이미징**: 서로 다른 노출(Exposure) 시간으로 촬영된 다중 노출 영상들을 결합하여 어두운 영역과 밝은 영역의 디테일을 모두 보존하는 방사도 맵(Radiance Map) 복원 및 톤 매핑(Tone Mapping).
* **초해상화 (Super-Resolution)**: 단일 영상(SISR) 또는 다중 영상으로부터 고주파 디테일을 복원하여 고해상도 영상을 생성 (Diffusion/GAN/Transformer 기반).
* **이미지 매팅 (Image Matting)**: 전경 색상 $F$, 배경 색상 $B$, 알파 마스크 $\alpha$를 분리하는 역문제 ($I = \alpha F + (1-\alpha)B$).

# Related Concepts
* [Image Processing](02-image-processing.md)
* [Image-Based & Neural Rendering](13-image-based-neural-rendering.md)
