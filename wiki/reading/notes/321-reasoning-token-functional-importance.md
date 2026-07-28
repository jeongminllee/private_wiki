---
type: Paper Note
title: "추론 토큰의 기능적 중요도를 LLM이 내부적으로 구분하는가"
description: "추론 과정에서 제거해도 되는 토큰과 보존해야 하는 토큰을 likelihood 기반 pruning으로 분석한 ACL 2026 연구"
resource: "https://arxiv.org/abs/2601.03066"
notion: "https://app.notion.com/p/6cd1a73cf20b8306a1de01ed3fdc1e44"
tags: [reading, paper, llm, reasoning, distillation]
timestamp: 2026-07-24
status: summarized
---

# 문제

긴 chain-of-thought는 정답률을 높일 수 있지만 추론 비용이 크고, 어떤 토큰이 실제 계산에 필요한지 알기 어렵다. 이 연구는 reasoning token을 하나씩 제거했을 때 모델의 likelihood가 얼마나 변하는지를 이용해 토큰의 기능적 중요도를 측정한다.

# 방법

Greedy pruning은 매 단계에서 지정한 목적함수의 likelihood를 가장 적게 훼손하는 reasoning token을 지운다. 이 과정을 반복하면 원하는 길이의 압축된 추론 사슬을 만들 수 있다. 저자들은 이 사슬로 student model을 distillation하고, attention score와 greedy pruning 순위의 관계도 분석했다.

# 결과

같은 reasoning 길이에서 pruning한 사슬로 학습한 student가 frontier model이 직접 압축한 사슬로 학습한 경우보다 좋은 성능을 보였다고 보고한다. 특정 토큰이 반복적으로 먼저 또는 나중에 제거되고 attention score가 제거 순위를 예측한다는 결과는, 모델 내부 표현에 토큰별 기능 차이가 일부 담겨 있음을 시사한다.

# 해석과 한계

이 방법은 추론 사슬을 진단하고 distillation 데이터를 줄이는 데 유용하다. 다만 토큰을 반복 삭제하며 likelihood를 다시 계산하므로 실제 요청의 즉시 비용 절감 기법으로는 비쌀 수 있다. Likelihood 보존은 사람이 이해하기 쉬운 설명이나 인과적 중요도와 같지 않으며, 결과는 저자 실험 범위에서 재현해야 한다.

# 출처

- [Do LLMs Encode Functional Importance of Reasoning Tokens?](https://arxiv.org/abs/2601.03066)
