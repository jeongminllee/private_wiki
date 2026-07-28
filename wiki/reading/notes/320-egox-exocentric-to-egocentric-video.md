---
type: Paper Note
title: "EgoX: 한 개의 3인칭 영상에서 일관된 1인칭 영상을 생성하기"
description: "3D prior와 geometry-guided attention을 video diffusion model에 결합한 exocentric-to-egocentric 변환 연구"
resource: "https://keh0t0.github.io/EgoX/"
notion: "https://app.notion.com/p/dbc1a73cf20b83698843017c329e3678"
tags: [reading, paper, computer-vision, video-generation]
timestamp: 2026-07-24
status: summarized
---

# 문제

3인칭(exocentric) 카메라 영상을 등장인물의 1인칭(egocentric) 시점 영상으로 바꾸는 과제다. 두 카메라의 위치와 방향 차이가 크고 공통으로 보이는 영역이 적어, 원본에 보이는 내용을 보존하면서 가려진 영역을 기하학적으로 일관되게 생성해야 한다.

# 방법

EgoX는 먼저 입력 영상을 3D point cloud로 올리고 목표 1인칭 시점에서 render해 거친 egocentric prior video를 만든다. 깨끗한 exocentric latent와 prior latent를 width 방향과 channel 방향으로 결합해 pretrained video diffusion model에 넣는다. 전체 모델을 다시 학습하는 대신 LoRA로 가볍게 적응한다.

Geometry-guided self-attention은 1인칭 query와 3인칭 key의 3D 방향 유사도를 attention bias로 더한다. 목표 시점에서 실제로 대응할 가능성이 높은 영역에 attention을 모으고, 보이지 않는 다른 위치의 사건이 잘못 생성되는 것을 줄인다.

# 결과와 활용

프로젝트는 다양한 exo-to-ego benchmark에서 기존 방법보다 큰 폭으로 개선됐고, 영화·스포츠·일상 장면 같은 학습 밖 영상에도 확장된다고 보고한다. immersive video, embodied AI 학습 자료와 시점 변환 콘텐츠에 응용할 수 있다.

# 한계

3D reconstruction과 camera pose가 틀리면 prior와 attention guidance도 함께 틀어진다. 원본 한 시점에 없는 영역은 결국 생성 모델의 추정이므로 사실 기록이나 안전 판단에 실제 관측처럼 사용하면 안 된다. 빠른 움직임, 반사, 가림과 scene change에서 시간적 일관성을 별도로 확인해야 한다. 이 작업은 CVPR 2026 발표 자료이며 정량 결과는 저자 보고이므로 code와 benchmark protocol을 이용한 재현이 필요하다.

# 출처

- [EgoX 프로젝트 페이지](https://keh0t0.github.io/EgoX/)
