---
type: Paper Note
title: "Mamba-3: 추론 효율을 우선한 state space sequence model"
description: "복소 상태 갱신과 MIMO 구조로 state tracking 및 decoding 효율을 개선한 Mamba-3 논문과 기사 대조"
resource: "https://www.aitimes.com/news/articleView.html?idxno=208071"
resource_aliases: ["https://share.google/hiFH3ZdTRaGM2lHAR"]
notion: "https://app.notion.com/p/8271a73cf20b83aa89b9017fa1caf57f"
tags: [reading, paper, mamba, state-space-model, inference]
timestamp: 2026-07-24
status: summarized
---

# 문제

Transformer attention은 긴 sequence에서 학습 연산량이 길이의 제곱에 비례하고, autoregressive decoding의 KV cache도 문맥과 함께 커진다. Mamba 계열은 고정 크기 state를 recurrent하게 갱신해 선형 시간·상수 decoding memory를 지향하지만, 기존 linear model은 state tracking 품질과 실제 hardware 효율 사이에서 손해를 보기도 했다.

Mamba-3는 학습 속도보다 inference 효율을 먼저 놓고 세 가지 변화를 결합한다.

- State space discretization에서 유도한 더 표현력 있는 recurrence
- 진동·주기 정보를 표현하기 위한 complex-valued state update
- 한 번의 recurrence에서 여러 input과 output을 처리해 연산 밀도를 높이는 MIMO 구조

MIMO는 decoding이 memory-bound일 때 GPU의 남는 연산 자원을 활용하면서 latency 증가를 억제하려는 설계다.

# 보고된 결과

1.5B 규모에서 기본 Mamba-3는 강한 linear baseline인 Gated DeltaNet보다 downstream 평균 정확도가 0.6%p 높고, MIMO variant가 추가로 1.2%p를 얻어 총 1.8%p 차이를 보고했다. State-size 실험에서는 Mamba-2의 절반 크기로 비슷한 perplexity를 달성했다.

AI타임스의 “메모리 절반”은 모든 GPU memory 사용량이 항상 절반이라는 뜻이 아니라, 같은 perplexity를 맞춘 비교에서 recurrent state size를 절반으로 줄였다는 논문 결과다. 기사에 나온 Transformer 대비 평균 정확도도 특정 1.5B 평가 묶음의 결과이므로 모든 규모와 작업에 일반화할 수 없다.

# 실무 판단

긴 문맥을 낮은 decoding memory로 처리하거나 batch throughput이 중요한 serving에서는 검토 가치가 있다. 반면 Transformer를 전면 대체했다고 보기는 이르다. 연구 결과는 주로 1.5B 규모와 지정된 retrieval·state-tracking·language modeling 평가에 기반하며, 대형 instruction model의 tool use, reasoning, training stability와 생태계 성숙도는 별도 검증이 필요하다.

공식 repository는 Mamba-3를 최신 source tree에서 설치하도록 안내한다. CUDA selective scan extension은 기본 설치에 포함되지 않으므로, 속도 비교 전 kernel 빌드 여부와 CUDA·PyTorch 환경을 동일하게 맞춰야 한다.

# 출처

- [AI타임스 소개 기사](https://www.aitimes.com/news/articleView.html?idxno=208071)
- [Mamba-3 논문](https://arxiv.org/abs/2603.15569)
- [Mamba 공식 repository](https://github.com/state-spaces/mamba)
- [Princeton 연구진 해설](https://pli.princeton.edu/blog/2026/mamba-3-improved-sequence-modeling-using-state-space-principles)

