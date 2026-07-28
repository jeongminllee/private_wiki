---
type: Paper Note
title: "FiCT: 간접 증거만으로 언어 규칙을 학습할 수 있는가"
description: "특정 언어 구문을 학습 말뭉치에서 제거하고 모델의 문법 일반화를 측정하는 연구"
resource: https://arxiv.org/pdf/2405.15750
notion: https://app.notion.com/p/5f31a73cf20b82d88e43818e862ddfdb
tags: [reading, paper, linguistics, language-model]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

Filtered Corpus Training(FiCT)은 평가할 언어 구문을 학습 데이터에서 의도적으로 제거한 뒤, 모델이 다른 문장에서 얻은 간접 증거만으로 그 규칙을 일반화하는지 시험한다.

# 연구 질문

언어 모델이 본 예문을 통계적으로 흉내 내는 것인지, 직접 보지 않은 구조까지 더 일반적인 문법 지식으로 추론하는지를 구분하기는 어렵다. FiCT는 목표 현상을 포함한 문장을 필터링해 직접 증거를 차단한다.

# 결과

연구는 여러 언어 현상에 대해 LSTM과 비슷한 규모의 Transformer를 비교한다. Transformer가 전체 perplexity에서는 더 좋았지만, 직접 보지 않은 구문에 대한 문법적 일반화는 두 구조 모두 예상보다 강했고 차이도 크지 않았다고 보고한다.

# 의미와 한계

성능이 높은 아키텍처가 반드시 더 인간다운 언어 일반화를 한다고 볼 수 없음을 보여준다. 다만 필터가 모든 간접 단서를 제거하지는 않으며, 제한된 모델 규모와 현상에서 얻은 결과를 최신 대형 모델 전체로 일반화해서는 안 된다.

# 출처

- [Generalization from Indirect Evidence in LLMs](https://arxiv.org/abs/2405.15750)

