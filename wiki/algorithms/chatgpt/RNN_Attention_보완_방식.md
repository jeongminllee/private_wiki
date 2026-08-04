---
type: Concept
title: "RNN Attention 보완 방식"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-08-21)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-08-21
status: active
---

# RNN Attention 보완 방식

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-08-21

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
좋은 질문이에요 👍  
RNN(Recurrent Neural Network)의 구조는 순차 데이터를 처리하는 데 강점이 있지만, 몇 가지 뚜렷한 단점이 있었어요. **Attention** 메커니즘은 이런 단점을 크게 보완해 줬습니다. 정리해드릴게요.

---

## 📌 RNN의 주요 단점
1. **장기 의존성(Long-term dependency) 문제**  
   - RNN은 순차적으로 정보를 업데이트하기 때문에, 입력 시퀀스가 길어질수록 앞부분의 정보가 뒤로 갈수록 희미해짐(Gradient Vanishing/Exploding 문제).
   - 예: 긴 문장에서 맨 앞 단어의 의미를 맨 끝에서 활용하기 어려움.

2. **병렬화 불가**  
   - RNN은 시퀀스를 한 단계씩(time-step) 계산해야 해서 학습 속도가 느림.

3. **정보 압축 문제**  
   - 전통적인 Seq2Seq(RNN encoder-decoder) 구조에서는 입력 문장 전체를 **하나의 고정 길이 벡터(context vector)**로 요약해야 함 → 긴 문장의 정보 손실이 심각.

---

## 📌 Attention이 보완한 방식
1. **장기 의존성 해결**  
   - Attention은 입력 전체 시퀀스를 **가중합(weighted sum)** 으로 다시 바라보게 함.  
   - 즉, 출력 시점마다 필요한 입력 부분에 **직접 집중(Attend)** → 앞의 정보가 멀리 있어도 바로 참조 가능.  
   - → Gradient 소실 문제 완화.

2. **정보 압축 문제 완화**  
   - 단일 벡터로 전체 문장을 압축하지 않고, 각 디코딩 단계에서 입력 시퀀스 전체를 참고.  
   - 중요한 단어에는 높은 가중치를, 덜 중요한 단어에는 낮은 가중치를 부여 → 정보 손실 줄임.

3. **해석 가능성(Interpretability)**  
   - Attention 가중치를 시각화하면 모델이 어떤 입력에 집중했는지 알 수 있음.  
   - RNN 단독 사용보다 직관적인 해석 가능.

4. **성능 향상**  
   - 기계 번역, 요약 등 다양한 NLP 태스크에서 성능이 크게 향상됨.  
   - 특히 긴 문장일수록 개선 효과가 큼.

---

## 📌 간단한 그림 비유
- **RNN만 사용**: 전체 책을 읽고 나서 머릿속에 한 문장으로 요약한 뒤 그걸로 질문에 답하는 것. (정보 손실 큼)
- **RNN + Attention**: 질문할 때마다 책의 각 페이지를 직접 다시 보면서 필요한 부분을 찾아 답하는 것. (정보 활용 극대화)

---

👉 요약하면, **RNN+Attention은 장기 의존성 문제와 정보 압축의 한계를 극복**해서 더 긴 문맥을 다루고, 성능과 해석력을 높였다고 볼 수 있어요.

---

원하시면, 제가 **수식/구현 관점**에서 RNN+Attention 구조(예: Bahdanau Attention, Luong Attention)를 비교 설명해 드릴 수도 있어요. 혹시 원하시나요?

---

### ❓ 질문 (User)
RNN + attention 구조가 RNN의 단점 보완을 했다고 해. 여기에서 단점 보완을 어떻게 했는지 궁금해

### 💡 답변 (Assistant)
좋습니다 👍 딥러닝을 기초부터 체계적으로 공부하고 싶으시다면, **수학 → 머신러닝 기초 → 딥러닝 이론/실습** 순서로 학습하는 게 좋아요. 아래에 **서적 + 강의**를 단계별로 추천해드릴게요.

---

# 📚 서적 추천

## 1. **수학/기초 다지기**
- 《밑바닥부터 시작하는 딥러닝》 (사이토 고키)  
  - 파이썬 코드로 신경망을 직접 구현해보면서 원리를 이해할 수 있음.
- 《Deep Learning 수학》 (이시이 히사시)  
  - 선형대수, 미적분, 확률/통계 등 딥러닝에 필요한 수학을 직관적으로 설명.

## 2. **머신러닝 기초**
- 《Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow》 (Aurélien Géron)  
  - 머신러닝과 딥러닝을 실무 예제와 함께 학습 가능. (국내 번역: 《핸즈온 머신러닝》)
- 《파이썬 머신러닝 완벽 가이드》 (권철민)  
  - 국내 저자의 책으로, Kaggle 데이터셋 예제를 많이 다룸.

## 3. **딥러닝 본격 학습**
- 《Deep Learning》 (Ian Goodfellow, Yoshua Bengio, Aaron Courville)  
  - 딥러닝 "바이블". 이론적으로 깊이 들어가고 싶다면 필수.
- 《Dive into Deep Learning》(Aston Zhang 외) [무료 온라인 교재]  
  - 코드와 이론을 동시에 학습 가능. (PyTorch, MXNet 기반)

---

# 🎥 강의 추천

## 1. **입문**
- **Andrew Ng – Machine Learning (Coursera)**  
  - 전통적인 머신러닝 기초. (수학적 직관과 기본 개념 잡기 좋음)
- **Andrew Ng – Deep Learning Specialization (Coursera)**  
  - 딥러닝의 기본 구조(MLP, CNN, RNN, Optimization 등)를 다룸.

## 2. **실습 위주**
- **Fast.ai – Practical Deep Learning for Coders** (무료)  
  - "이론보다 먼저 실습" 접근법. 실제 모델을 만들면서 감각을 익힐 수 있음.
- **PyTorch 공식 튜토리얼**  
  - 프레임워크 사용법을 빠르게 익히는 데 유용.

## 3. **이론 심화**
- **CS231n: Convolutional Neural Networks for Visual Recognition (Stanford)**  
  - CNN, 딥러닝 핵심 이론과 최신 기법을 다룸. 강의 노트가 교재급.
- **MIT 6.S191: Introduction to Deep Learning**  
  - 딥러닝 전반을 한 학기 수준으로 다루는 강의.

---

# 🚀 학습 순서 제안
1. **Python + Numpy**로 기본 프로그래밍 연습  
2. 《밑바닥부터 시작하는 딥러닝》으로 **신경망 원리** 이해  
3. Andrew Ng ML 강의 → 핸즈온 머신러닝 책으로 **ML/DL 기초**  
4. Fast.ai / PyTorch 튜토리얼로 **실습 감각** 익히기  
5. Ian Goodfellow 《Deep Learning》 + CS231n 강의로 **이론 심화**

---

👉 혹시 원하시는 방향이 **실무(빠르게 모델 만들기)** 쪽인지, 아니면 **이론(수학·논문 이해)** 쪽인지 알려주시면 더 맞춤형 로드맵을 짜드릴 수 있어요.  
어느 쪽을 원하시나요?

---

### ❓ 질문 (User)
딥러닝을 기초부터 공부하고 싶은데 서적이나 강의를 추천해줘.

### 💡 답변 (Assistant)
좋은 질문이에요 👍  
**Query / Key / Value (Q, K, V)**는 Attention 메커니즘의 핵심인데, 이 세 가지가 어디서 나와서 어떻게 작용하는지 정확히 짚고 갈게요.

---

## 📌 1. Query, Key, Value의 직관적 의미
- **Query (Q)** : “무엇을 찾고 싶은가?” → 현재 시점의 **질의(검색 요청)**
- **Key (K)** : “내가 가진 정보의 이름표” → 입력 시퀀스 각 요소의 **특징(주소/인덱스)**
- **Value (V)** : “실제 정보” → 그 요소가 가진 **내용(값)**

👉 즉, **Query가 Key와 얼마나 잘 맞는지**를 보고, 그 가중치로 **Value를 섞어서 새로운 표현**을 만듭니다.

---

## 📌 2. RNN + Attention (Seq2Seq)에서 Q, K, V의 위치
### (1) Encoder
- 입력 시퀀스(예: 영어 문장)를 RNN, LSTM, GRU로 인코딩해서 **hidden states** \(h_1, h_2, ..., h_T\)를 얻습니다.  
- 이 hidden states가 Attention에서 **Key와 Value** 역할을 합니다.  
  - \( K = [h_1, h_2, ..., h_T] \)  
  - \( V = [h_1, h_2, ..., h_T] \)  (대개 Key와 Value는 같은 벡터를 씀)

### (2) Decoder
- 디코더의 현재 시점 hidden state \(s_t\)가 **Query**가 됩니다.  
  - \( Q = s_t \)

---

## 📌 3. 작용 과정 (Bahdanau / Luong Attention 예시)
1. **유사도 측정 (Q vs K)**  
   - Query와 Key의 유사도를 계산해 "어느 입력 단어에 집중할지"를 정함.  
   - 점수 함수(score function) 사용:  
     \[
     score(Q, K_i) = Q^T W K_i
     \]
   - 이 점수를 소프트맥스(Softmax)로 변환해서 **Attention 가중치 α**를 얻음.

2. **Value 결합 (Weighted Sum)**  
   - Attention 가중치 α를 Value에 곱해서 합산:  
     \[
     context = \sum_i \alpha_i V_i
     \]

3. **출력 생성**  
   - 이 context vector를 디코더 출력에 반영 → 원하는 위치에서 필요한 정보만 뽑아 씀.

---

## 📌 4. Transformer Self-Attention과 비교
- **Seq2Seq (RNN+Attention)**  
  - Query = 디코더 hidden state  
  - Key, Value = 인코더 hidden states  
- **Self-Attention (Transformer)**  
  - Query, Key, Value 모두 같은 시퀀스(hidden state)에서 선형 변환으로 뽑음.  
  - 즉, 모든 단어가 서로를 참고 가능.

---

## 🔑 요약
- **Query (Q)** → “현재 내가 집중하고 싶은 것” (디코더 hidden state)  
- **Key (K)** → “각 입력 단어의 인덱스/특징” (인코더 hidden state)  
- **Value (V)** → “그 단어가 가진 실제 정보” (인코더 hidden state)  
- Attention은 **Q와 K의 유사도를 기반으로 V를 가중합**해 context를 만드는 과정.

---

혹시 원하시면, 제가 **수식 없이 그림/직관 비유**로 “Q/K/V가 서로 대화하는 과정”을 설명드릴 수도 있는데, 좀 더 직관적으로 보시겠어요?

---

### ❓ 질문 (User)
쿼리 키 밸류가 어텐션 에서 어디에서 작용하는거야?

### ❓ 질문 (User)
transformers 구조에 대해서 자세하게 설명해줘

### 💡 답변 (Assistant)
좋아요! 한 번에 전체 그림이 잡히도록, **Transformer**를 “부품 → 블록 → 전체 아키텍처 → 학습/추론 → 변형/최적화” 순서로 정리해볼게요. (수학/구현 관점도 함께 담았습니다.)

---

# 1) 큰 그림: 세 가지 계열
- **Encoder-only** (예: BERT): 입력 이해/분류·추출 등 **이해(understanding)** 중심.
- **Decoder-only** (예: GPT): 한 토큰씩 이어 쓰는 **생성(generation)** 중심.
- **Encoder–Decoder** (예: T5, 원형 Transformer): 입력을 인코딩 후 디코더가 **조건부 생성**(번역/요약 등).

---

# 2) 토큰화 & 임베딩 & 위치정보
1) **토큰화**: BPE/SentencePiece 등으로 텍스트 → 토큰 ID.  
2) **임베딩**: 토큰 ID → \(d_\text{model}\) 차원 벡터. (입력 임베딩, 출력 임베딩; 종종 가중치 공유)  
3) **위치정보(Positional Encoding)**: 순서를 모르는 self-attention에 **순서**를 주입.
   - **Sinusoidal**(원 논문): 학습 불필요, 길이 외삽 안정.
   - **Learned**: 위치 임베딩을 학습.
   - **상대/회전형**: **RoPE**, **ALiBi** 등. 긴 문맥 일반화/확장에 유리.

> 최종 입력: `x = token_embedding + positional_encoding` (또는 RoPE로 Q/K에 직접 적용).

---

# 3) 핵심 부품: Scaled Dot-Product Attention
입력 행렬 \(X \in \mathbb{R}^{T \times d_\text{model}}\)에서 선형 변환으로
\[
Q = XW_Q,\quad K = XW_K,\quad V = XW_V
\]
(각 \(W_\*\in \mathbb{R}^{d_\text{model}\times d_k}\), 보통 \(d_k=d_v=d_\text{model}/h\))

**유사도 → 가중치 → 합산**:
\[
\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}} + \text{mask}\right) V
\]

- **mask**:
  - **Padding mask**: 패딩 토큰을 보지 않게  \(-\infty\) 가산.
  - **Causal mask**(디코더/생성): 미래 토큰 차단(상삼각에 \(-\infty\)).
- **스케일링** \(1/\sqrt{d_k}\): 내적 분산 안정화.

---

# 4) Multi-Head Attention (MHA)
- \(h\)개의 head로 \(Q,K,V\)를 분할(혹은 독립 투사)해 **여러 서브공간에서 병렬로** 어텐션.
- 각 head의 출력을 concat 후 \(W_O\)로 다시 투사:
\[
\text{MHA}(X) = \text{Concat}(\text{head}_1,\dots,\text{head}_h) W_O
\]
- 효과: 서로 다른 관계(구문/의미/장거리/근거리)를 **동시에 포착**.

---

# 5) Position-wise FFN (비선형 변환)
각 토큰 위치별로 동일한 2층 MLP:
\[
\text{FFN}(x) = W_2\, \sigma(W_1 x + b_1) + b_2
\]
- 보통 **차원 확장**: \(d_\text{ff} \approx 4 \times d_\text{model}\)
- 활성함수: ReLU, GELU, 또는 **게이팅(GEGLU/Swish-Gated)** 변형.

---

# 6) 잔차 연결 & 정규화
- 각 서브레이어(MHA, FFN) 앞뒤로 **Residual + LayerNorm**.
- **Pre-LN**(현대 표준): `x ← x + Sublayer(LN(x))` → 깊은 네트워크 안정.
- **Dropout**, **학습 스케줄러**, **가중치 초기화**가 함께 안정성에 기여.

---

# 7) 블록 구성도

## (A) Encoder Block
1) \(y = x + \text{MHA}(\text{LN}(x))\)  
2) \(z = y + \text{FFN}(\text{LN}(y))\)  
- **Self-Attention**: 입력 토큰끼리 서로를 자유롭게 참조.

## (B) Decoder Block
1) \(y = x + \text{MHA}_\text{masked}(\text{LN}(x))\)  (Causal mask)  
2) \(z = y + \text{CrossAttn}(\text{LN}(y), K,V\!=\text{EncoderOut})\)  
3) \(u = z + \text{FFN}(\text{LN}(z))\)  
- **Masked Self-Attn**: 미래 차단.
- **Cross-Attn**: 디코더가 인코더 출력을 **조회(Q=디코더, K/V=인코더)**.

---

# 8) 전체 아키텍처별 데이터 흐름

### Encoder-only (BERT류)
- 입력 \(\to\) N×EncoderBlock \(\to\) [CLS] 토큰 등으로 **이해/분류/추출**.
- **목표**: MLM(마스크 언어모델), NSP(초기 BERT), 다음문장/문장쌍 판단 등.

### Decoder-only (GPT류)
- 입력(프롬프트) \(\to\) N×DecoderBlock(마스크된 self-attn만) \(\to\) 다음 토큰 확률.
- **목표**: Causal LM(다음 토큰 예측).  
- **생성 루프**: 한 토큰 생성 → 입력에 붙여 다음 토큰 생성.

### Encoder–Decoder (T5류)
- 인코더가 입력을 **압축/정리**, 디코더가 **조건부 생성**.
- **목표**: span corruption(텍스트-투-텍스트), 번역·요약에 강함.

---

# 9) 학습 목표(Objectives)
- **MLM**: 일부 토큰 마스킹 후 복원(양방향 문맥 활용).
- **Causal LM**: 왼쪽 문맥만으로 다음 토큰 예측(오토리그레시브).
- **Seq2Seq**: 입력→출력 매핑(번역/요약/질의응답 등).

추가로 최근엔 **Instruction Tuning**(명령 데이터로 미세조정), **RLHF/DPO**(사람 선호 반영)로 사용성을 높입니다.

---

# 10) 복잡도 & 최적화 포인트
- **표준 Attention**: 시간/메모리 \(O(T^2)\) (T = 시퀀스 길이).
- **디코더 추론**: KV-Cache로 한 토큰당 비용을 \(O(T)\to O(1)\) 수준으로 절감(과거 K,V 재사용).
- **메모리/속도 최적화**: FlashAttention(정확한 소프트맥스 유지하며 IO 감소), 혼합정밀도(FP16/BF16), 시퀀스 병렬화, 텐서 병렬/파이프라인 병렬 등.
- **롱컨텍스트**: RoPE/ALiBi 스케일링, 위치보간, 선형/저랭크/국소 어텐션(단, 정확도 트레이드오프).

---

# 11) 언제 무엇을 쓰나?
- **분류/추출/NER/질의응답(추출형)**: Encoder-only가 간결·강력.
- **개방형 생성(작문/코딩/챗봇)**: Decoder-only가 표준.
- **조건부 생성(번역/추상 요약)**: Encoder–Decoder가 여전히 강력.

---

# 12) 형태/차원 감각(예시)
- \(d_\text{model}=768,\ h=12 \Rightarrow d_k=d_v=64\)  
- 입력 배치: \((B, T)\) → 임베딩 \((B, T, d_\text{model})\)  
- 한 head: \(Q,K,V\in \mathbb{R}^{B\times T\times d_k}\)  
- 어텐션 가중치: \(A=\text{softmax}(QK^\top/\sqrt{d_k})\in \mathbb{R}^{B\times T\times T}\)  
- 헤드 concat: \((B, T, h\cdot d_v)=(B,T,d_\text{model})\)

---

# 13) PyTorch 스타일 의사코드(단일 MHA)
```python
def mha(X, mask=None):                      # X: (B,T,d_model)
    Q = X @ W_Q   # (B,T,d_k*h)
    K = X @ W_K
    V = X @ W_V
    Q,K,V = split_heads(Q), split_heads(K), split_heads(V)  # -> (B,h,T,d_k)

    attn_scores = Q @ K.transpose(-1, -2) / math.sqrt(d_k) # (B,h,T,T)
    if mask is not None:
        attn_scores += mask  # padding/causal: very negative on blocked positions
    attn_probs = softmax(attn_scores, dim=-1)              # (B,h,T,T)

    context = attn_probs @ V                               # (B,h,T,d_k)
    context = combine_heads(context)                       # (B,T,d_model)
    return context @ W_O                                   # (B,T,d_model)
```

---

# 14) 핵심 요약(치트시트)
- **Self-Attention**: 모든 토큰이 서로를 **직접** 참조 → 장기 의존성 해결.
- **Multi-Head**: 다양한 관점의 관계를 **병렬** 포착.
- **Pre-LN + Residual**: 안정적 학습의 표준.
- **마스킹**: 패딩/미래 차단.
- **아키텍처 선택**: 이해=Encoder / 생성=Decoder / 조건부생성=Encoder–Decoder.
- **한계/해결**: \(O(T^2)\) → KV-Cache, FlashAttention, 롱컨텍스트 기법.

---

필요하시면, **BERT vs GPT vs T5를 표로 비교**하거나, **Attention 마스킹/로프(RoPE) 적용 예시**, **학습 하이퍼파라미터(학습률 스케줄/Dropout/Weight Decay) 튜닝 가이드**도 이어서 정리해 드릴게요. 어느 부분을 더 깊게 보고 싶으세요?

---
