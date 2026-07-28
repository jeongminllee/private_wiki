---
type: Paper Note
title: "StreamingVLM: 끝나지 않는 영상을 실시간으로 이해하기"
description: "제한된 KV cache와 짧은 중첩 구간 학습으로 장시간 video stream을 안정적으로 처리하는 VLM"
resource: https://arxiv.org/abs/2510.09608
notion: https://app.notion.com/p/2201a73cf20b83df871881671050bc8a
tags: [reading, paper, vlm, video, streaming]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

StreamingVLM은 전체 video token을 계속 보관하지 않고 attention sink, 최근 vision token의 짧은 window, 최근 text token의 긴 window만 유지해 무한에 가까운 video stream을 일정한 memory와 latency로 처리한다.

# 방법

추론 시 사용할 제한된 attention pattern을 학습에서도 재현한다. 매우 긴 영상을 그대로 학습하는 대신 짧고 서로 겹치는 video chunk에 full attention SFT를 적용해 이전 구간의 문맥을 이어받는 streaming 동작을 익힌다.

# 평가

연구진은 평균 길이가 두 시간을 넘고 frame과 text를 초 단위로 맞춰야 하는 `Inf-Streams-Eval`을 만들었다. 논문은 이 평가에서 GPT-4o mini 대비 66.18% win rate, NVIDIA H100 한 장에서 최대 8 FPS의 안정적 실시간 처리를 보고한다. 별도 VQA fine-tuning 없이 LongVideoBench는 4.30점, OVOBench Realtime은 5.96점 향상됐다고 한다.

# 의미와 한계

핵심은 긴 context를 무작정 확장하는 대신 “지금 필요한 시각 정보”와 “더 오래 남겨야 할 언어 기억”의 보존 기간을 다르게 둔 점이다. 다만 H100 기준 처리량이 edge device의 실시간성을 보장하지는 않으며, 오래전에 등장한 시각 세부를 다시 묻는 질의에서 손실이 얼마나 큰지 별도 확인해야 한다.

# 출처

- [StreamingVLM 논문](https://arxiv.org/abs/2510.09608)
- [공식 코드](https://github.com/mit-han-lab/streaming-vlm)

