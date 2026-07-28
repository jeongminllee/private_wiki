---
type: Paper Note
title: "SIMA 2: Gemini 기반 범용 embodied agent"
description: "여러 3D 가상환경에서 보고, 추론하고, 키보드·마우스로 행동하며 자기 경험으로 개선되는 Google DeepMind 연구"
resource: "https://www.linkedin.com/feed/update/urn:li:activity:7404656173028925440"
notion: "https://app.notion.com/p/4041a73cf20b82c7848601fc6e8fa13f"
tags: [reading, embodied-agent, sima, gemini, reinforcement-learning]
timestamp: 2026-07-24
status: summarized
---

# 핵심

SIMA 2는 특정 게임의 내부 API나 상태값을 직접 읽지 않고 화면을 관찰한 뒤 가상 키보드와 마우스로 행동하는 범용 embodied agent다. SIMA 1의 단순 지시 수행에 Gemini의 추론 능력을 결합해, 추상적인 목표를 해석하고 사용자와 대화하며 여러 단계의 행동을 설명하도록 확장했다.

학습에는 언어 설명이 붙은 사람의 시연 영상과 Gemini가 생성한 label을 함께 사용한다. 언어뿐 아니라 이미지·스케치·emoji로 주어진 지시를 이해하고, 한 게임에서 익힌 채굴 같은 개념을 보지 못한 게임의 수확 행동에 전이하는 것이 핵심 평가 대상이다.

# 일반화와 자기 개선

연구진은 학습에 포함되지 않은 `ASKA`, `MineDojo`와 Genie 3가 생성한 새로운 세계에서도 목표 지향적 행동이 가능했다고 보고한다. 초기 인간 시연 이후에는 Gemini가 새 과제를 만들고 행동에 reward를 부여하며, SIMA 2가 자기 play에서 모은 경험을 다음 세대 학습에 다시 사용하는 loop도 실험했다.

LinkedIn 글은 확장 평가에서 성공률이 SIMA 1 약 31%, SIMA 2 약 62%, 사람 약 71%라고 요약한다. 다만 공식 blog가 강조하듯 SIMA 1 수치는 더 많은 환경과 어려운 지시를 포함한 새 평가 기준의 결과이므로, 예전 SIMA 1 benchmark와 그대로 비교하면 안 된다.

# 해석과 한계

이 결과는 곧바로 범용 로봇을 완성했다는 뜻이 아니다. SIMA 2는 제한된 research preview이고, 긴 시간에 걸친 목표 검증, 짧은 interaction memory, 정밀한 저수준 조작과 복잡한 장면 인식에 여전히 약하다. 게임에서 얻은 행동 능력이 물리적 로봇으로 전이되려면 안전성, 접촉 dynamics, sensor noise와 실제 행동 비용을 별도로 해결해야 한다.

그럼에도 하나의 policy가 다양한 시각 환경에서 언어·추론·행동을 연결하고, 생성된 환경에서 경험을 축적하는 구조는 embodied agent 연구의 중요한 방향이다. 실제 적용을 볼 때는 평균 성공률뿐 아니라 보지 못한 환경, 긴 task horizon, 실패 복구와 사람 개입 횟수를 함께 봐야 한다.

# 출처

- [HaYeJin Kang의 LinkedIn 소개 글](https://www.linkedin.com/feed/update/urn:li:activity:7404656173028925440)
- [Google DeepMind 공식 소개](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/)
- [SIMA 2 technical report](https://arxiv.org/abs/2512.04797)

