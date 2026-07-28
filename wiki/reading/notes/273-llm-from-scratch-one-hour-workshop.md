---
type: Reference
title: "한 시간짜리 LLM from Scratch: 작은 GPT의 전체 경로 직접 구현하기"
description: "문자 tokenizer부터 Transformer, training loop와 sampling까지 10M model로 배우는 workshop"
resource: https://discuss.pytorch.kr/t/llm-from-scratch-gpt/10070
notion: https://app.notion.com/p/b5e1a73cf20b820ebff3014f52f2c815
tags: [reading, llm-training, pytorch, workshop]
timestamp: 2026-07-24
status: summarized
---

# 목표

이 workshop은 pretrained model을 불러오지 않고 tokenizer, embedding, causal self-attention, Transformer block, loss, optimizer와 text generation을 직접 구현한다. Production LLM을 만드는 과정이 아니라 작은 model로 end-to-end mechanics를 눈으로 확인하는 실습이다.

# 기본 실험

- Tiny Shakespeare와 character-level tokenization
- 약 10M parameter, 6 layer·6 head·384 hidden dimension
- Cross-entropy next-character prediction
- AdamW, learning-rate schedule, gradient clipping
- Training·validation loss, checkpoint와 중간 sample 관찰
- MPS, CUDA와 CPU 자동 선택

M3 Pro 기준 medium 설정은 약 45분, 4M small model은 약 20분, 0.5M tiny model은 약 5분으로 소개된다. Hardware와 software version에 따라 시간은 달라진다.

# 학습 포인트

Character tokenizer는 작은 Shakespeare corpus에서 BPE보다 sparse vocabulary 문제가 적다. Model 크기가 커질수록 빠르게 좋은 sample을 만들지만 작은 data에 더 빨리 overfit한다. Training loss가 계속 내려가도 validation loss가 오르면 마지막 checkpoint가 아니라 best validation checkpoint를 써야 한다.

한 번 완주한 뒤에는 context length, head 수, dropout과 data size를 하나씩 바꾸고 같은 seed의 loss curve를 비교하는 것이 좋다. 생성 문장이 그럴듯하다는 인상보다 held-out loss와 memorization을 함께 본다.

# 출처

- [PyTorchKR workshop 소개](https://discuss.pytorch.kr/t/llm-from-scratch-gpt/10070)

