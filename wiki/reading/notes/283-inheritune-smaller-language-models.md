---
type: Paper Note
title: "Inheritune: 큰 모델의 초기 층을 물려받아 더 작은 언어 모델 훈련하기"
description: "깊은 decoder의 비활성 attention 층을 관찰하고 초기 transformer 층 상속·재학습·점진 확장으로 줄이는 방법"
resource: https://arxiv.org/pdf/2404.08634v2
notion: https://app.notion.com/p/bd51a73cf20b82f0ad6c018130c09ab7
tags: [reading, paper, llm, model-compression]
timestamp: 2026-07-24
status: summarized
---

# 문제

저자들은 표준 decoder LLM의 깊은 층에서 attention matrix가 한 열에 집중하는 현상을 관찰하고, 의미 있는 패턴을 배우지 못하는 이런 층을 `lazy layer`라고 부른다. 단순히 모델의 뒤쪽 층을 제거하면 계산량은 줄지만 이미 학습된 표현과 최종 성능을 잃을 수 있다.

# Inheritune

Inheritune은 큰 pretrained model의 앞쪽 transformer layer를 작은 모델의 초기값으로 물려받는다. 그 작은 모델을 다시 학습한 뒤 필요에 따라 층을 점진적으로 확장하는 과정을 반복해, 처음부터 작은 모델을 학습하거나 큰 모델을 그대로 쓰는 선택 사이의 중간 경로를 만든다.

v2 논문은 GPT-2 계열을 OpenWebText-9B와 FineWeb-Edu에서 실험한다. 대표 결과로 16-layer GPT-2 Medium 변형이 표준 24-layer GPT-2 Medium과 비슷한 성능을 보였다고 보고한다. 핵심 주장은 모든 깊은 층이 동일한 가치를 갖는 것이 아니며, 유용한 초기 representation을 상속하면 더 적은 층으로 경쟁력 있는 모델을 만들 수 있다는 것이다.

# 읽을 때의 한계

저장된 링크는 2024-10-04의 arXiv v2다. arXiv에는 2026-02-16 v4까지 올라와 있으므로 재현이나 최신 결론 인용에는 v4의 변경점을 다시 확인해야 한다. 실험도 GPT-2 규모와 정해진 dataset에 집중되어 있어 현대 MoE나 매우 큰 instruction model에 같은 비율로 적용된다고 일반화할 수 없다.

또한 attention이 단일 열에 집중한다는 관찰만으로 층 전체가 완전히 불필요하다고 단정할 수는 없다. pruning baseline, 총 학습 compute와 데이터량을 맞춘 비교, downstream task별 성능을 함께 봐야 실제 효율 이득을 판단할 수 있다.

# 출처

- [Inheritune v2](https://arxiv.org/abs/2404.08634v2)
- [최신 arXiv revision](https://arxiv.org/abs/2404.08634)

