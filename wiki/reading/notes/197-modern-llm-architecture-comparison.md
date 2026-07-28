---
type: Concept
title: "현대 LLM 아키텍처 비교: 공통 기반과 효율화 패턴"
description: "DeepSeek V3부터 GLM-5와 Gemma 4까지 attention, MoE, normalization, 위치 표현의 변화를 비교"
resource: https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison
notion: https://app.notion.com/p/cc01a73cf20b83f2b0af813a8720e0b7
tags: [reading, llm, architecture, transformer]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Sebastian Raschka가 현대 공개 가중치 LLM의 텍스트 아키텍처를 나란히 비교한 장문 자료다. GPT-2 이후 기본 Transformer 골격은 크게 남아 있지만, KV cache·FFN 계산·긴 문맥·학습 안정성을 개선하는 여러 조합이 축적됐다.

# 반복해서 나타나는 변화

- **MHA에서 GQA·MLA로**: key/value head를 공유하거나 낮은 차원으로 압축해 KV cache를 줄인다.
- **Dense에서 MoE로**: 많은 expert 중 일부만 토큰마다 활성화해 전체 용량과 토큰당 계산량을 분리한다.
- **GELU에서 SwiGLU로**: FFN의 표현력과 학습 효율을 높이는 gated activation이 표준에 가까워졌다.
- **LayerNorm에서 RMSNorm·QK-Norm으로**: 계산을 단순화하고 attention logit과 학습 안정성을 관리한다.
- **Global과 local attention 혼합**: Gemma 계열처럼 sliding-window layer 사이에 global layer를 배치해 긴 문맥 비용을 줄인다.
- **RoPE 변형과 NoPE**: 위치 정보를 부분적으로 적용하거나 일부 layer에서 제거해 길이 일반화와 위치 잡음을 조절한다.

# 모델별 눈에 띄는 선택

- DeepSeek V3/R1은 MLA와 세분화된 MoE를 결합한다.
- OLMo 2는 투명한 학습 공개와 함께 normalization 위치, QK-Norm을 실험한다.
- Gemma 3·4는 local/global hybrid attention과 pre·post normalization을 유지한다.
- SmolLM3는 일부 layer의 NoPE로 작은 모델의 긴 문맥을 탐색한다.
- GLM-5는 744B MoE와 MLA, sparse attention을 사용하면서 토큰당 활성 매개변수는 약 40B로 제한한다.

# 비교할 때의 함정

아키텍처만으로 모델 품질을 설명할 수 없다. 데이터, tokenizer, optimizer, 학습·후속학습 예산, 평가 오염이 서로 다르다. 이 글도 benchmark 순위보다 설계 선택을 이해하기 위한 지도에 가깝다.

# 출처

- [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)

