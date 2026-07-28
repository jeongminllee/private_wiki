---
type: Study Note
title: "모두를 위한 친절한 LLM 학습 가이드"
description: "언어 모델의 학습 원리부터 분산 학습, LoRA, 양자화, 추론 서빙까지 연결한 Devfest 발표"
resource: https://speakerdeck.com/beomi/devfest-incheon-2025-modureul-wihan-cinjeolhan-eoneomodel-llm-hagseub-gaideu?slide=9
notion: https://app.notion.com/p/b8c1a73cf20b8385829d81d5f1f8564b
tags: [reading, slides, llm, training]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Devfest Incheon 2025에서 Beomi가 발표한 40장 분량의 슬라이드다. LLM을 직접 만든다는 것이 데이터, 사전학습, 후속학습, 분산 시스템, 메모리 최적화, 서빙을 모두 포함한다는 점을 큰 그림으로 설명한다.

# 학습 흐름

1. 데이터를 수집하고 품질과 중복을 필터링한다.
2. tokenizer와 embedding을 거쳐 Transformer가 다음 토큰을 예측하도록 사전학습한다.
3. 목적에 맞는 instruction fine-tuning과 RLHF/RLVR로 행동을 조정한다.
4. LoRA 같은 PEFT로 전체 가중치를 갱신하지 않고 적응시킨다.
5. 양자화와 서빙 엔진으로 실제 지연 시간과 메모리 사용량을 줄인다.

# 시스템 관점

- GPU 메모리에는 가중치뿐 아니라 optimizer state, activation, KV cache가 들어간다.
- 데이터 병렬화(DP), 텐서 병렬화(TP), 파이프라인 병렬화(PP), 시퀀스·전문가 병렬화를 문제에 맞게 조합한다.
- FP32에서 BF16, FP8, FP4로 정밀도를 낮출수록 메모리와 처리량은 개선되지만 품질 검증이 필요하다.
- 개인 추론에는 Ollama·llama.cpp, 고처리량 서버에는 vLLM·SGLang 같은 선택지가 있다.

# 실무 의사결정

일반 기능은 API와 RAG를 먼저 검토하고, 도메인 행동이나 출력 형식을 반복적으로 바꿔야 할 때 파인튜닝을 고려하는 편이 좋다. 처음부터 사전학습할 이유는 독자적 데이터·언어·연구 목표와 이를 감당할 인프라가 있을 때로 제한된다.

# 출처

- [Devfest Incheon 2025 발표 자료](https://speakerdeck.com/beomi/devfest-incheon-2025-modureul-wihan-cinjeolhan-eoneomodel-llm-hagseub-gaideu)

