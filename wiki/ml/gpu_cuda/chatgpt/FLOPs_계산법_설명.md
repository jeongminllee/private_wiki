---
type: Concept
title: "FLOPs 계산법 설명"
description: "ML - GPU & CUDA 가속 - ChatGPT 대화 추출 노트 (2026-06-09)"
tags: [ml, chatgpt-export]
timestamp: 2026-06-09
status: active
---

# FLOPs 계산법 설명

> **카테고리**: `ML - GPU & CUDA 가속`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-09

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
FLOPs = 6 x 70e9 x 15e12 이거 스탠포드 대학 LLM 강의할때 가르쳐주던 수식인데 70B parameter 모델을 15T tokens로 학습시키기 위해 얼마나 시간이 드냐. 가용 GPU는 1024 * H100 이거든? 저기서 6이 왜 나온거야?

### 💡 답변 (Assistant)
좋은 질문이야. 저 식에서 **6**은 Transformer 계열 dense LLM을 학습할 때 자주 쓰는 근사식인

\[
\text{training FLOPs} \approx 6 \times N \times D
\]

에서 나온 상수야.

여기서

\[
N = \text{모델 파라미터 수}
\]

\[
D = \text{학습 토큰 수}
\]

이므로 70B 모델을 15T 토큰으로 학습하면

\[
6 \times 70 \times 10^9 \times 15 \times 10^{12}
\]

이 되는 거야.

---

## 왜 6인가?

핵심은 **각 파라미터가 토큰 하나를 처리할 때 대략 6 FLOPs 정도의 학습 비용을 만든다**는 근사야.

학습은 크게 세 단계로 나눌 수 있어.

\[
\text{Forward pass}
\]

\[
\text{Backward pass: activation gradient}
\]

\[
\text{Backward pass: weight gradient}
\]

각각을 아주 거칠게 보면:

| 단계 | 비용 |
|---|---:|
| Forward pass | 약 \(2ND\) |
| Backward pass, activation gradients | 약 \(2ND\) |
| Backward pass, parameter gradients | 약 \(2ND\) |
| 합계 | 약 \(6ND\) |

그래서 전체 학습 FLOPs를

\[
\boxed{6ND}
\]

로 잡는 거야.

---

## 왜 forward가 \(2ND\)인가?

행렬곱에서 곱셈과 덧셈을 둘 다 FLOP으로 세면, 하나의 weight를 한 번 사용하는 데 대략

\[
1 \text{ multiply} + 1 \text{ add} = 2 \text{ FLOPs}
\]

가 들어가.

Transformer의 대부분 계산은 Linear layer, Attention projection, MLP projection 같은 행렬곱에서 발생해. 그래서 파라미터 \(N\)개가 토큰 \(D\)개에 대해 사용된다고 보면 forward 비용을 대략

\[
2ND
\]

로 근사할 수 있어.

---

## backward가 왜 forward보다 약 2배인가?

Linear layer를 예로 들면 forward는

\[
Y = XW
\]

이고 backward에서는 보통 두 가지 gradient를 계산해야 해.

첫 번째는 입력 쪽 gradient:

\[
\frac{\partial L}{\partial X}
\]

두 번째는 weight 쪽 gradient:

\[
\frac{\partial L}{\partial W}
\]

이 둘 다 행렬곱으로 계산돼.

그래서 backward는 대략 forward의 2배 비용이 들어가고,

\[
\text{forward} \approx 2ND
\]

\[
\text{backward} \approx 4ND
\]

따라서

\[
\text{total} \approx 2ND + 4ND = 6ND
\]

가 돼.

---

## 중요한 점: 이건 “정확한 물리 법칙”이 아니라 근사식

\[
6ND
\]

는 LLM 학습 비용을 빠르게 추정하기 위한 경험적 근사야.

실제로는 다음 요소 때문에 달라져.

| 요소 | 영향 |
|---|---|
| Attention 계산 | sequence length가 길면 추가 비용 증가 |
| Embedding / LM head | vocab 크기에 따라 영향 |
| MoE 모델 | 전체 파라미터 수와 활성 파라미터 수가 달라짐 |
| Activation checkpointing | 메모리 절약 대신 재계산 FLOPs 증가 |
| Optimizer | AdamW 업데이트 비용 추가 |
| Precision | BF16/FP16/FP8 등에 따라 실제 처리량 차이 |
| Parallelism overhead | tensor/pipeline/data parallel 통신 비용 |
| MFU | 이론 FLOPs 대비 실제 활용률 |

그래도 dense Transformer LLM에서는 대략적인 학습량 추정에

\[
\boxed{\text{FLOPs} \approx 6 \times \text{parameters} \times \text{tokens}}
\]

를 많이 써.

---

## 네 예시로 다시 보면

\[
N = 70 \times 10^9
\]

\[
D = 15 \times 10^{12}
\]

\[
\text{FLOPs} = 6 \times 70 \times 10^9 \times 15 \times 10^{12}
\]

\[
= 6300 \times 10^{21}
\]

\[
= 6.3 \times 10^{24} \text{ FLOPs}
\]

즉 70B 모델을 15T 토큰으로 학습하는 데 필요한 총 연산량은 대략

\[
\boxed{6.3 \times 10^{24} \text{ FLOPs}}
\]

야.

요약하면, **6은 forward 1번 + backward에서 gradient 2종류를 계산하는 비용까지 합쳐서 나온 학습 FLOPs 근사 계수**라고 보면 돼.

---

### ❓ 질문 (User)
MoE는 달라?

### 💡 답변 (Assistant)
응, **MoE는 달라.**  
Dense 모델에서 쓰는

\[
\text{Training FLOPs} \approx 6 \times N \times D
\]

를 **그대로 전체 파라미터 수 \(N\)** 에 적용하면 MoE에서는 보통 **과대평가**가 돼.

핵심은 이거야.

\[
\boxed{\text{MoE는 전체 파라미터 수가 아니라 “토큰당 활성화되는 파라미터 수”가 중요하다}}
\]

---

## Dense 모델은 모든 파라미터를 매 토큰마다 사용함

Dense Transformer에서는 토큰 하나가 들어오면 모델의 거의 모든 layer를 지나고, 대부분의 파라미터가 계산에 참여해.

그래서 70B dense 모델이면 대략

\[
6 \times 70B \times D
\]

로 계산해도 된다.

---

## MoE는 일부 expert만 사용함

MoE, Mixture of Experts 모델은 보통 FFN/MLP 부분을 여러 expert로 나눠놓고, 각 토큰마다 그중 일부 expert만 선택해서 사용해.

예를 들어 expert가 8개 있고, top-2 routing을 쓴다고 하자.

\[
\text{전체 expert 수} = 8
\]

\[
\text{토큰당 사용하는 expert 수} = 2
\]

그러면 FFN expert 부분에서는 전체 expert 파라미터의 전부가 아니라

\[
\frac{2}{8} = 25\%
\]

정도만 활성화돼.

즉 전체 파라미터 수는 커도, 토큰당 계산량은 훨씬 작아진다.

---

## MoE FLOPs 근사는 이렇게 봐야 함

Dense 모델:

\[
\text{FLOPs} \approx 6 \times N_{\text{total}} \times D
\]

MoE 모델:

\[
\text{FLOPs} \approx 6 \times N_{\text{active}} \times D
\]

여기서

\[
N_{\text{active}} = \text{토큰 하나를 처리할 때 실제로 사용되는 파라미터 수}
\]

야.

그래서 MoE에서는 전체 파라미터 수보다 **active parameters per token**이 훨씬 중요해.

---

## 예시: Mixtral 8x7B 느낌으로 보면

예를 들어 단순화해서 어떤 MoE 모델이 있다고 하자.

| 항목 | 값 |
|---|---:|
| 전체 파라미터 | 47B |
| 토큰당 활성 파라미터 | 약 13B |
| 토큰 수 | \(D\) |

그러면 학습 FLOPs는 전체 47B 기준이 아니라 대략

\[
6 \times 13B \times D
\]

에 가깝게 잡는 게 맞아.

전체 파라미터 47B라고 해서

\[
6 \times 47B \times D
\]

로 계산하면 실제 계산량보다 훨씬 크게 잡게 돼.

---

## 하지만 완전히 단순하지는 않음

MoE에서도 항상 전체 파라미터가 무시되는 건 아니야.

학습 중에는 선택된 expert만 forward/backward에 참여하므로 계산량은 active parameter 기준에 가깝지만, 다음 비용들이 추가로 들어간다.

| 요소 | 설명 |
|---|---|
| Router 계산 | 토큰마다 어떤 expert로 보낼지 계산 |
| Expert dispatch/combine | 토큰을 expert별로 보내고 다시 모으는 통신 비용 |
| Load balancing loss | expert 사용량 균형을 맞추기 위한 보조 loss |
| Communication overhead | 여러 GPU에 expert가 나뉘어 있으면 all-to-all 통신 발생 |
| Capacity factor | 특정 expert에 토큰이 몰릴 때 여유 용량 설정 필요 |
| Expert imbalance | expert별 부하 불균형으로 일부 GPU가 놀거나 병목 발생 |

그래서 순수 FLOPs만 보면 MoE가 싸 보이지만, 실제 wall-clock time은 **통신과 라우팅 오버헤드** 때문에 생각보다 복잡해져.

---

## Dense 70B vs MoE 70B는 같은 70B가 아님

중요한 비교 포인트는 이거야.

### Dense 70B

\[
N_{\text{total}} = N_{\text{active}} = 70B
\]

그래서

\[
\text{FLOPs} \approx 6 \times 70B \times D
\]

---

### MoE 70B

전체 파라미터가 70B여도 토큰당 활성 파라미터가 예를 들어 12B라면

\[
N_{\text{total}} = 70B
\]

\[
N_{\text{active}} = 12B
\]

그래서

\[
\text{FLOPs} \approx 6 \times 12B \times D
\]

에 가까워진다.

즉 MoE 70B는 계산량 기준으로는 dense 70B가 아니라 **dense 10B~20B급에 가까운 경우**가 많아.

---

## 그럼 MoE는 왜 쓰나?

MoE의 장점은 이거야.

\[
\boxed{\text{계산량은 작게 유지하면서, 전체 파라미터 용량은 크게 만든다}}
\]

즉,

| 관점 | Dense | MoE |
|---|---|---|
| 전체 파라미터 | 계산량과 강하게 연결됨 | 크게 늘릴 수 있음 |
| 토큰당 계산량 | 전체 모델 크기에 비례 | 활성 expert 수에 비례 |
| 메모리 | 전체 파라미터 저장 필요 | 전체 expert 저장 필요 |
| FLOPs | 큼 | 상대적으로 작음 |
| 통신 복잡도 | 상대적으로 단순 | 더 복잡 |
| 학습 안정성 | 비교적 단순 | 라우팅/부하균형 이슈 있음 |

---

## 결론

MoE에서는

\[
6 \times N \times D
\]

의 \(N\)에 **전체 파라미터 수**를 넣으면 안 되고, 보통은

\[
\boxed{N = \text{active parameters per token}}
\]

을 넣어야 해.

따라서 MoE 학습 FLOPs는 대략

\[
\boxed{\text{FLOPs} \approx 6 \times N_{\text{active}} \times D}
\]

로 보는 게 맞아.

단, 실제 학습 시간은 FLOPs만으로 결정되지 않고, **expert parallelism, all-to-all 통신, load balancing, routing overhead, GPU utilization**에 크게 좌우돼.

---
