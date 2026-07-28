---
type: Reference
title: "LLM Architecture Gallery를 통해 읽는 dense·MoE·hybrid 구조의 흐름"
description: "Sebastian Raschka의 시각 자료를 바탕으로 주요 open-weight LLM 구조 변화를 정리한 GeekNews 해설"
resource: https://news.hada.io/topic?id=27553
notion: https://app.notion.com/p/3f91a73cf20b83ac938e01b386dbd077
tags: [reading, llm-architecture, moe, attention]
timestamp: 2026-07-24
status: summarized
---

# 세 흐름

## Dense baseline

GPT-2의 MHA·LayerNorm·GELU 구조에서 Llama 3의 RoPE·GQA·RMSNorm, OLMo 2의 residual 내부 post-norm과 QK-Norm으로 학습 안정성과 KV cache 효율을 다듬었다.

## Sparse MoE

DeepSeek V3/R1은 671B 중 37B를 활성화하고 MLA, shared expert와 MTP를 결합했다. Llama 4, Qwen3, Kimi K2와 GLM 계열은 expert 수, shared expert, attention과 dense-prefix 조합을 달리하며 총 parameter를 늘리고 token당 compute를 제한한다.

## Hybrid sequence model

Qwen3 Next는 Gated DeltaNet과 attention, Kimi Linear는 linear attention과 MLA, Nemotron 3는 Mamba-2와 Transformer를 섞는다. 긴 context의 quadratic attention 비용을 줄이면서 일부 global attention으로 recall을 보완하려는 흐름이다.

# Gallery를 쓰는 법

각 card의 total·active parameter, decoder type, attention, layer mix, context와 license를 같은 축으로 비교한다. Model 이름이 비슷해도 reasoning variant는 architecture가 같고 training recipe만 다른 경우가 있다. DeepSeek R1과 V3가 대표적이다.

구조표만으로 품질·속도·memory를 단정하면 안 된다. Training data, post-training, quantization, serving kernel과 batch가 결과에 큰 영향을 준다. Gallery는 비교할 질문을 만드는 index이고 최종 source는 model config와 technical report다.

# 관련 자료

- [PyTorchKR의 한국어 상세 소개](272-llm-architecture-gallery-pytorchkr.md)
- [공식 gallery 정리](274-llm-architecture-gallery-official.md)
- [GeekNews 원문](https://news.hada.io/topic?id=27553)

