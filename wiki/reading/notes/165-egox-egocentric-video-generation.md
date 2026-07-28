---
type: Paper Note
title: "EgoX: 외부 시점 영상에서 1인칭 영상 생성"
description: "단일 3인칭 영상을 조건으로 일관된 1인칭 영상을 생성하는 비디오 확산 모델 연구"
resource: https://arxiv.org/pdf/2512.08269
notion: https://app.notion.com/p/5d31a73cf20b82cb8c1501aa7adf4750
tags: [reading, paper, computer-vision, video-generation]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

EgoX는 한 대의 외부 카메라로 촬영한 3인칭 영상에서 같은 장면의 1인칭 영상을 생성하려는 비디오 확산 모델이다.

# 문제

외부 시점과 1인칭 시점은 자세 변화가 크고 겹쳐 보이는 영역이 적다. 3인칭 영상에 나오지 않은 영역도 만들어야 하므로 단순한 시점 변환만으로는 시간적·기하학적 일관성을 유지하기 어렵다.

# 방법

- 사전 학습된 비디오 확산 모델을 기반으로 경량 LoRA만 학습한다.
- 외부 시점과 1인칭 시점의 조건을 폭 또는 채널 방향으로 결합한다.
- geometry-guided self-attention으로 두 시점 사이의 대응과 움직임을 유도한다.

# 결과와 한계

저자들은 실험 자료와 야외 영상에서 기존 방법보다 현실적이고 일관된 결과를 보고한다. 다만 생성된 1인칭 영상은 실제 관찰 기록이 아니라 모델의 추정이다. 로봇 학습이나 안전 분석에 사용할 때는 보이지 않던 물체와 접촉 관계가 정확한지 별도로 검증해야 한다.

# 출처

- [EgoX 논문](https://arxiv.org/abs/2512.08269)

