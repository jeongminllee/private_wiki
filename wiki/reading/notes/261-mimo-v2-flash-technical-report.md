---
type: Paper Note
title: "MiMo-V2-Flash: 15B 활성 파라미터로 속도와 추론을 맞춘 309B MoE"
description: "Hybrid attention, MTP와 multi-teacher on-policy distillation을 결합한 Xiaomi 모델의 구조와 주장"
resource: https://arxiv.org/abs/2601.02780
notion: https://app.notion.com/p/4c91a73cf20b83fe94cc01969149d753
tags: [paper, llm, mixture-of-experts, speculative-decoding]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

MiMo-V2-Flash는 309B 전체 parameter 중 token마다 15B를 활성화하는 MoE model로, 짧은 sliding-window attention과 드문 global attention, multi-token prediction을 결합해 long context와 빠른 agentic inference를 함께 노린다.

# 구조

- Sliding Window Attention(SWA)과 global attention을 5:1로 교차 배치
- SWA window는 128 token이며 attention sink bias를 학습
- Native 32K context로 pretraining한 뒤 256K까지 확장
- 27조 token pretraining과 Multi-Token Prediction(MTP)
- 총 309B, 활성 15B parameter

짧은 local window를 대부분의 layer에 쓰면 KV cache를 줄일 수 있고, global layer가 멀리 떨어진 token 사이의 정보를 보완한다. MTP module은 다음 한 token만이 아니라 여러 미래 token을 예측하도록 학습하며, inference 때 draft model로 재사용해 speculative decoding을 수행한다.

# Post-training

논문은 Multi-Teacher On-Policy Distillation(MOPD)을 제안한다. 수학·coding·agent처럼 영역별로 강화학습된 teacher가 student의 현재 rollout에 dense reward와 token-level feedback을 주어 여러 전문성을 하나의 model로 옮긴다.

# 결과 해석

저자들은 3개 MTP layer를 사용할 때 최대 3.6 token의 acceptance length와 2.6배 decoding speedup을 보고하고, 더 큰 open-weight MoE와 경쟁하는 benchmark 결과를 제시한다. 이 수치는 저자 환경의 serving stack, batch와 task에 따른 결과이므로 실제 hardware에서 같은 속도를 보장하지 않는다.

Weight와 3-layer MTP weight는 MIT license로 공개됐다. 309B 전체 weight를 올려야 하므로 활성 parameter가 작다고 해도 memory·network와 expert parallelism 요구가 가벼운 model은 아니다.

# 출처

- [Technical report](https://arxiv.org/abs/2601.02780)
- [공식 model card](https://huggingface.co/XiaomiMiMo/MiMo-V2-Flash)

