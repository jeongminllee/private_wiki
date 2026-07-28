---
type: Study Note
title: "노트북에서 소형 언어 모델을 처음부터 학습하는 워크숍"
description: "문자 토크나이저부터 Transformer, 학습 루프와 샘플링까지 직접 구현하는 약 10M 모델 실습"
resource: https://news.hada.io/topic?id=29218
notion: https://app.notion.com/p/0311a73cf20b8290879301109e023a0f
tags: [reading, llm, pytorch, study]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

약 1MB의 Shakespeare 텍스트로 10M 매개변수 GPT를 노트북에서 1시간 안에 학습하도록 만든 실습 워크숍이다. 대규모 성능보다 토크나이저, self-attention, loss, optimizer, 생성이 어떻게 연결되는지 직접 확인하는 것이 목적이다.

# 직접 만드는 부분

- 문자 단위 tokenizer와 `vocab_size=65`
- token·position embedding
- causal self-attention, LayerNorm, MLP가 포함된 Transformer block
- cross-entropy loss, AdamW, gradient clipping, learning-rate scheduling
- temperature와 top-k를 이용한 다음 토큰 샘플링
- `model.py`, `train.py`, `generate.py`

# 제공 규모

- Tiny 약 0.5M: M3 Pro 기준 약 5분
- Small 약 4M: 약 20분
- Medium 약 10M: 약 45분
- 공통 `block_size=256`

Mac의 MPS, NVIDIA CUDA, CPU를 자동 선택하며 로컬에서는 `uv sync`, 대안으로 Colab을 안내한다.

# “처음부터”의 범위

PyTorch의 tensor와 autograd를 사용하므로 수치 연산, 역전파, GPU kernel까지 직접 구현하는 과정은 아니다. “대형” 모델을 만드는 자료라기보다 Transformer 학습 파이프라인을 작은 규모로 재구성하는 입문 실습이라고 보는 것이 정확하다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=29218)
- [Train Your Own LLM From Scratch](https://github.com/angelos-p/llm-from-scratch)

