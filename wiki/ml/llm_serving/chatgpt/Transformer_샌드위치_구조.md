---
type: Concept
title: "Transformer 샌드위치 구조"
description: "ML - LLM Serving & Inference - ChatGPT 대화 추출 노트 (2025-11-21)"
tags: [ml, chatgpt-export]
timestamp: 2025-11-21
status: active
---

# Transformer 샌드위치 구조

> **카테고리**: `ML - LLM Serving & Inference`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-11-21

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
이 구조에 대해서 자세하게 설명해줘

### 💡 답변 (Assistant)
아래 그림은 **“중간에 이산(바이너리) 잠재변수 Z를 끼워 넣은, 샌드위치 형태의 Transformer 디코더/인코더 구조”**로 보면 돼요.  
한 줄 요약하면:

> **과거 토큰으로 ① 아래쪽(전반부) 디코더가 표현을 만들고 → ② 인코더가 그 표현을 H비트 이산 코드(Z)로 압축/샘플링하고 → ③ 위쪽(후반부) 디코더가 그 이산 코드를 메모리처럼 참고해 다음 토큰을 예측하는 구조**입니다.

그림에 나온 블록/화살표를 아래에서 위로 차근차근 설명해볼게요.

---

## 0) 표기부터
- **T**: 시퀀스 길이(토큰 개수)
- **D**: Transformer 히든 차원
- **V**: vocab 크기
- **H**: 잠재 코드의 비트 수  
  → **H 비트면 가능한 코드 수는 2^H**  
- **L**: 디코더 Transformer 레이어 수  
  그림은 **L/2 층 + L/2 층**으로 나눠 샌드위치처럼 배치

각 텐서 크기 표기가 예를 들어 `T × D`면 “길이 T, 히든 D”라는 뜻.

---

## 1) 입력과 Embedding
### **S₁:ₜ₋₁**
- 모델이 이미 본 **과거 토큰(prefix)**.
- 다음 토큰을 예측하기 위해 입력으로 들어감.

### **Embeddings**
- 토큰 임베딩 + 위치 임베딩.
- 출력 크기: **T × D**

---

## 2) 아래쪽 디코더: Causal Transformer Block × L/2
그림 맨 아래 보라색 스택.

### 역할
- **완전한 오토리그레시브(AR) 디코더의 전반부**.
- **Causal mask**가 있어서 t번째 위치는 **1..t 까지만** 봄.
- 과거 토큰으로부터 강한 문맥 표현을 만듦.

### 출력
- 히든 상태: **h⁽low⁾ ∈ ℝ^{T×D}**

이 h⁽low⁾가 두 군데로 흘러가요:
1) **위쪽 디코더로 그대로 올라가는 주 경로**
2) **인코더의 key/value(kv)로 들어가는 경로(오른쪽으로 빠지는 굵은 라인)**

---

## 3) 인코더(추론 네트워크): Non-Causal Transformer Block
가운데 주황색 블록.

### 입력
- **q (query)**: 왼쪽의 `ζ`에서 옴.
  - `ζ`는 보통 **학습되는 쿼리 시퀀스**나  
    **latent를 뽑기 위한 기준 토큰/포지션 임베딩**이라고 보면 됨.
  - 크기 표기: **r × D** (그림엔 r로 나와 있는데, 보통 T와 같거나 T에 대응)

- **kv (key/value)**: 아래 디코더 출력 **h⁽low⁾ (T×D)**

### Non-Causal 의미
- **양방향(attend-to-all)** attention.
- causal mask가 없어서 **입력 전체 위치를 동시에 참고** 가능.
- 다만 kv가 아래쪽 causal 표현에서 왔기 때문에 **미래 토큰을 직접 보진 않음**(prefix 기반).

### 역할
- 아래 디코더가 만든 문맥을 보고  
  **각 위치의 이산 잠재코드(바이너리 코드)를 추정**.

### 출력
- **e ∈ ℝ^{T×D}**

---

## 4) Encoder read-out FC → T × H
인코더 출력 `e(T×D)`를 **H차원 로짓/확률**로 투영.

- **logit_b ∈ ℝ^{T×H}**
- 위치마다 H개의 비트(혹은 비트 로짓)를 만든다고 생각하면 됨.

---

## 5) Binary mapper → Z (T × 2^H)
점선 박스.

### 역할
- `T×H` 로짓을 **이산 코드로 바꾸는 단계**.
- H비트 조합은 2^H가지니까
  - **각 위치마다 2^H개 중 하나를 고르는(one-hot) 분포**를 만들거나
  - **H개의 Bernoulli 비트 샘플**을 뽑아 코드화함.

### 학습 때
이산 샘플은 미분이 안 되니까 보통
- **Straight-Through estimator**
- **Gumbel-Softmax / Relaxed Bernoulli**
- **vector quantization(VQ)**
같은 기법으로 “샘플은 이산처럼, 그래디언트는 연속처럼” 흘려요.

### 결과: **Z**
- **Z ∈ ℝ^{T×2^H}** (각 위치의 이산 코드 one-hot)
  - 또는 내부적으로는 T×H 바이너리 비트로 보관해도 동일 의미.

---

## 6) Post-sampler FC → T × D
Z를 다시 디코더가 쓰기 좋게 **연속 벡터 메모리**로 변환.

- **m = FC(Z) ∈ ℝ^{T×D}**
- 이 m이 위쪽 디코더의 **cross-attention 메모리(kv)**가 됨.

---

## 7) 위쪽 디코더: Causal Transformer Block × L/2
맨 위의 보라색 스택.

### 입력
- **주 경로(hidden)**: 아래 디코더에서 올라온 **h⁽low⁾**
- **cross-attention kv**: post-sampler에서 온 **m(T×D)**

그림에서 q는 위로 올라오는 디코더 히든,  
kv는 Z에서 복원한 메모리로 들어가죠.

### 역할
- 아래쪽 디코더만으로는 얻기 어려운 정보를
  **이산 잠재코드 Z를 통해 보강**해서 더 좋은 다음 토큰 예측을 하게 함.
- 구조적으로는 **Encoder-Decoder Transformer의 cross-attention**을  
  **AR 디코더의 후반부에만 붙인 느낌**.

### 출력
- 최종 디코더 히든: **h⁽up⁾ ∈ ℝ^{T×D}**

---

## 8) Decoder read-out FC → Logits S₂:ₜ (T × V)
- 마지막 선형층이 vocab 차원 V로 투영.
- **다음 토큰 분포(logits)** 출력:
  - **S₂:ₜ** 라는 표기는 “2번째~T번째 토큰(정답)의 로짓”이라는 뜻.

---

## 9) 왜 L을 반으로 쪼갰을까? (샌드위치 이유)
이 구조의 핵심 의도는 보통 이거예요:

1) **아래쪽 AR 표현(h⁽low⁾)**은  
   *“과거만 보고도 만들 수 있는, 추론/생성 공용 기반 표현”*.

2) 그 기반을 이용해 인코더가  
   **정보를 H비트 이산 코드로 압축(Z)**.

3) 위쪽 디코더는  
   **압축된 요약본(Z-memory)**을 보면서  
   더 강력한 예측을 수행.

→ 즉, **모델 내부에 ‘이산 요약/계획/압축 채널’을 하나 둔 AR LM**이라고 보면 됩니다.

---

## 10) 전체 데이터 흐름(한 번에 보기)
1. **prefix S₁:ₜ₋₁ → Embedding**
2. **아래 Causal Decoder(L/2) → h⁽low⁾**
3. **Encoder(Non-Causal) + ζ queries, kv=h⁽low⁾ → e**
4. **Readout FC → 비트 로짓(T×H)**
5. **Binary mapper → 이산 latent Z**
6. **Post-sampler FC → 메모리 m(T×D)**
7. **위 Causal Decoder(L/2), cross-attend to m → h⁽up⁾**
8. **Readout FC → 다음 토큰 logits S₂:ₜ**

---

원하면,
- 이 구조가 어떤 논문/모델 계열에서 나왔는지 추정해서 맥락까지 연결해주거나,
- “Binary mapper를 실제로 어떻게 학습/샘플링하는지” 수식/의사코드로 더 깊게 풀어줄 수도 있어요.

---
