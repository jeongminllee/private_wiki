---
type: Reference
title: "MiniMind: 64M GPT를 처음부터 학습하며 LLM pipeline 익히기"
description: "Tokenizer부터 pretraining, SFT와 preference optimization까지 작은 모델로 실습하는 교육용 프로젝트"
resource: https://discuss.pytorch.kr/t/minimind-3-2-64m-gpt/9460
notion: https://app.notion.com/p/eeb1a73cf20b829d80db81222a86809a
tags: [reading, llm-training, pytorch, education]
timestamp: 2026-07-24
status: summarized
---

# 목적

MiniMind는 거대한 production model을 만드는 대신 작은 language model의 전체 학습 pipeline을 한 GPU에서 직접 경험하게 하는 PyTorch 중심 교육용 프로젝트다. 핵심 구현을 framework 뒤에 숨기지 않아 data, loss와 training stage의 관계를 추적하기 쉽다.

# 다루는 범위

- 64M dense model과 198M/A64M MoE variant
- custom tokenizer와 최대 32K context
- pretraining, full SFT와 LoRA
- DPO, RLAIF 기반 PPO·GRPO·CISPO
- knowledge distillation, adaptive thinking과 YaRN
- Transformers, TRL, PEFT 및 llama.cpp·vLLM·Ollama 연동

기본 흐름은 저장소를 clone하고 dependency를 설치한 뒤 `train_pretrain`과 `train_full_sft` 단계로 진행한다. 각 단계의 dataset format, checkpoint와 evaluation 결과를 기록하면 end-to-end 구조를 이해하는 작은 실험실로 쓸 수 있다.

# 비용 주장 해석

“RTX 3090 한 장에서 2시간, 3달러” 같은 수치는 특정 model 크기, dataset, sequence length와 cloud 요금 조건의 예시다. 전체 기능과 충분한 품질을 그 비용에 얻는다는 보장은 아니다. Hardware, mixed precision, batch와 data volume을 고정해 재현해야 한다.

# 적절한 기대치

64M model은 training mechanics와 code를 배우기에는 좋지만, 일반적인 production assistant 품질을 기대할 규모는 아니다. Evaluation은 loss뿐 아니라 held-out prompt, memorization, tokenizer coverage와 stage별 behavior 변화를 포함해야 한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/minimind-3-2-64m-gpt/9460)

