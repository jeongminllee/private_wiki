---
type: Concept
title: "New chat"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2023-12-05)"
tags: [algorithms, chatgpt-export]
timestamp: 2023-12-05
status: active
---

# New chat

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-12-05

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
Foundation models, now powering most of the exciting applications in deep learning, are almost universally based on the Transformer architecture and its core attention module. Many subquadratic-time architectures such as linear attention, gated convolution and recurrent models, and structured state space models (SSMs) have been developed to address Transformers’ computational ineﬃciency on long sequences, but they have not performed as well as attention on important modalities such as language. We identify that a key weakness of such models is their inability to perform content-based reasoning, and make several improvements. First, simply letting the SSM parameters be functions of the input addresses their weakness with discrete modalities, allowing the model to selectively propagate or forget information along the sequence length dimension depending on the current token. Second, even though this change prevents the use of eﬃcient convolutions, we design a hardware-aware parallel algorithm in recurrent mode. We integrate these selective SSMs into a simpliﬁed end-to-end neural network architecture without attention or even MLP blocks (Mamba). Mamba enjoys fast inference (5× higher throughput than Transformers) and linear scaling in sequence length, and its performance improves on real data up to million-length sequences. As a general sequence model backbone, Mamba achieves state-of-the-art performance across several modalities such as language, audio, and genomics. On language modeling, our Mamba-3B model outperforms Transformers of the same size and matches Transformers twice its size, both in pretraining and downstream evaluation.
한국어로 번역해줘

### 💡 답변 (Assistant)
제가 이해한 바로는, Transformer 아키텍처와 그 핵심 attention 모듈을 기반으로 하는 대부분의 딥 러닝 응용 프로그램이 최근에 많이 나오고 있지만, Transformer의 계산 효율성 부족으로 인해, 선형 어텐션, 게이트드 컨볼루션 및 순환 모델, 구조화된 상태 공간 모델(SSM)과 같은 서브-이차 시간 아키텍처들이 개발되었지만, 이러한 모델들은 언어와 같은 중요한 모달리티에서 어텐션만큼 잘 작동하지 않았다고 합니다. 이러한 모델들의 주요 약점은 콘텐츠 기반 추론(content-based reasoning)을 수행할 수 없다는 것입니다. 그래서 입력에 따라 SSM 매개변수가 함수로 작용하게 함으로써 이들 모델의 약점을 해결하였고, 이를 통해 모델이 현재 토큰에 따라 시퀀스 길이 차원을 따라 정보를 선택적으로 전파하거나 잊을 수 있게 되었다고 합니다. 또한, 이러한 변경으로 효율적인 컨볼루션 사용이 불가능해지지만, 병렬 하드웨어에 적합한 알고리즘을 설계하여 순환 모드에서 통합시켰다고 합니다. 이 선택적 SSM을 attention이나 MLP 블록 없이 단순화된 end-to-end 신경망 아키텍처에 통합하여 Mamba를 만들었습니다. Mamba는 빠른 추론(Transformer보다 5배 높은 처리량)과 시퀀스 길이에 대한 선형 스케일링을 갖추고 있으며, 백만 길이의 시퀀스에서 실제 데이터에서 성능이 향상되었다고 합니다. 일반적인 시퀀스 모델 백본으로서, Mamba는 언어, 오디오, 유전체

---
