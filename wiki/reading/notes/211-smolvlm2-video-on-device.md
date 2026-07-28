---
type: Reference
title: "SmolVLM2: 작은 기기에서 실행하는 영상 이해 모델"
description: "256M·500M·2.2B 크기로 영상 질의응답과 captioning을 지원하는 경량 vision-language model"
resource: https://huggingface.co/blog/smolvlm2
notion: https://app.notion.com/p/3971a73cf20b8352864201f988f9531a
tags: [reading, vlm, video, edge-ai]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

SmolVLM2는 영상 이해를 phone부터 server까지 가져가는 것을 목표로 한 256M, 500M, 2.2B parameter 모델군이다. Hugging Face Transformers와 Apple MLX용 Python·Swift API를 공개해 local·on-device 실험의 진입 장벽을 낮췄다.

# 크기별 역할

- **2.2B**: 영상·이미지 이해의 기본 선택지로 OCR, diagram, 수학·과학 시각 질의 성능을 강화했다.
- **500M·256M**: 정확도보다 memory와 배포 크기가 중요한 mobile·edge 실험에 초점을 둔다.
- 2.2B는 무료 Google Colab에서도 실행할 수 있을 정도의 memory 효율을 목표로 한다.

# 기술과 사용

모델은 video file과 질문을 함께 chat template에 넣어 `AutoModelForImageTextToText`로 추론할 수 있다. MLX 지원은 Apple Silicon에서 Python 또는 Swift application으로 연결할 때 유용하다. video caption, 여러 image 비교, highlight 생성과 VLC·iPhone demo도 제공된다.

# 평가 포인트

발표는 Video-MME에서 동급 크기 모델보다 좋은 효율을 보였다고 보고한다. 실제 적용에서는 sampling FPS, clip 길이, audio·subtitle 사용 여부, 작은 text OCR, temporal ordering과 hallucination을 따로 측정해야 한다. 작은 모델의 장점은 frontier API를 완전히 대체하는 것보다 privacy, offline 처리와 많은 영상을 저렴하게 1차 분류하는 데 있다.

# 출처

- [SmolVLM2 발표](https://huggingface.co/blog/smolvlm2)

