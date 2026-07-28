---
type: Reference
title: "일러스트로 이해하는 원형 Transformer"
description: "encoder-decoder 구조, self-attention, multi-head attention과 positional encoding의 계산 흐름"
resource: https://news.hada.io/topic?id=25272
notion: https://app.notion.com/p/4951a73cf20b838ea72c81d0d872167d
tags: [reading, transformer, attention, deep-learning]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Jay Alammar의 대표 입문 글은 2017년 원형 Transformer를 번역 모델의 입력부터 다음 token 확률까지 그림으로 설명한다. 현대 decoder-only LLM의 모든 세부 구현을 설명하는 자료는 아니지만 attention의 기본 계산과 tensor 흐름을 익히기에 좋다.

# 계산 흐름

1. token을 embedding vector로 만들고 위치 정보를 더한다.
2. 각 위치의 입력에서 Query, Key, Value vector를 만든다.
3. Query와 모든 Key의 내적으로 관련 점수를 구하고 차원 크기의 제곱근으로 scale한다.
4. softmax weight로 Value를 가중 합해 문맥이 반영된 표현을 만든다.
5. 여러 head가 서로 다른 projection 공간에서 이 과정을 수행하고 결과를 연결한다.
6. attention과 feed-forward sublayer마다 residual connection과 layer normalization을 적용한다.

decoder는 미래 token을 보지 못하도록 masked self-attention을 사용하고, 원형 encoder-decoder 구조에서는 encoder output을 참조하는 cross-attention도 수행한다. 마지막 linear와 softmax가 다음 token의 확률 분포를 만든다.

# 무엇을 구분해야 하나

글의 기본 예시는 512차원 embedding, 8개 head, sinusoidal positional encoding과 post-normalization에 가깝다. 현대 LLM은 RoPE, RMSNorm, grouped-query attention, mixture-of-experts와 decoder-only 구조 등을 사용할 수 있다. 따라서 이 글은 공통 뼈대이고 특정 최신 모델의 정확한 설계도는 model paper와 configuration에서 확인해야 한다.

# 읽는 순서

먼저 그림으로 한 token의 Q/K/V 흐름을 따라간 뒤, 작은 행렬을 손으로 계산한다. 그다음 PyTorch 구현에서 tensor shape을 출력하면 공식만 외울 때보다 attention mask와 head 분할을 오래 기억할 수 있다.

# 출처

- [GeekNews 한국어 정리](https://news.hada.io/topic?id=25272)
- [The Illustrated Transformer 원문](https://jalammar.github.io/illustrated-transformer/)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Notion 원본 항목](https://app.notion.com/p/4951a73cf20b838ea72c81d0d872167d)
