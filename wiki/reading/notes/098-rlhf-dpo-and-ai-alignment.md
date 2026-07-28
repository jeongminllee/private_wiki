---
type: Reference
title: "RLHF와 DPO로 보는 LLM 선호 정렬의 구조와 한계"
description: "인간 선호 데이터로 모델 행동을 조정하는 RLHF·DPO 과정, 평가와 편향 문제"
resource: https://www.youtube.com/watch?v=0aryjbfkL0k
notion: https://app.notion.com/p/dd01a73cf20b826eba4281d5d446b872
tags: [reading, llm-alignment, rlhf, dpo, ai-safety]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

정렬(alignment)은 모델의 행동이 인간의 의도·선호와 안전 요구에 더 잘 맞도록 만드는 문제다. RLHF와 DPO는 모두 비교 선호 데이터를 활용하지만 학습 절차가 다르며, 어느 쪽도 “윤리적 AI”를 자동으로 완성하지 않는다.

# RLHF

대표적인 InstructGPT 방식은 세 단계다.

1. 사람이 작성한 좋은 응답으로 pretrained model을 supervised fine-tuning한다.
2. 같은 prompt의 여러 응답을 사람이 비교한 순위로 reward model을 학습한다.
3. policy model이 reward를 높이되 reference model에서 너무 멀어지지 않도록 KL penalty를 두고 PPO 등으로 최적화한다.

복잡하고 reward hacking, 불안정성과 비용 문제가 있지만 online sampling과 별도 reward model을 활용할 수 있다.

# DPO

DPO는 preferred response와 rejected response가 reference model에 비해 얼마나 더 가능성이 높아졌는지를 직접 classification loss로 최적화한다. 별도 reward model과 PPO loop가 없어 구현과 학습이 단순하다. 그러나 선호 dataset의 coverage, reference model, hyperparameter와 distribution shift에 여전히 민감하며 모든 task에서 RLHF보다 우월하다는 뜻은 아니다.

# 평가와 윤리의 한계

helpfulness·harmlessness·truthfulness, jailbreak와 toxicity를 따로 평가하고 red-team 결과와 실제 사용자 feedback을 본다. RLAIF나 Constitutional AI는 human label 비용을 줄일 수 있지만 AI judge와 constitution에 든 가치·편향을 확대할 수 있다. 다수의 선호를 최적화하는 것과 소수자 보호, 사실성, 법적 책임은 동일한 목표가 아니다.

# 실무 체크

선호 수집자의 구성과 지침을 기록하고 disagreement를 지우지 않는다. aggregate benchmark 외에 언어·문화·고위험 domain별 failure를 분석하며, 학습 뒤에도 monitoring, incident response와 human escalation을 둔다.

# 출처

- [YouTube 원본 영상](https://www.youtube.com/watch?v=0aryjbfkL0k)
- [InstructGPT 논문](https://arxiv.org/abs/2203.02155)
- [DPO 논문](https://arxiv.org/abs/2305.18290)
- [Constitutional AI 논문](https://arxiv.org/abs/2212.08073)
- [Notion 원본 항목](https://app.notion.com/p/dd01a73cf20b826eba4281d5d446b872)
