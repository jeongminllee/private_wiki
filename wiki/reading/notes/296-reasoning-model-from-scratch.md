---
type: Reference
title: "Build a Reasoning Model From Scratch: Qwen3 위에 추론 기법을 단계별로 구현하기"
description: "평가, inference-time scaling, self-refinement, GRPO 계열 RL과 distillation을 PyTorch notebook으로 배우는 교재 code"
resource: https://github.com/rasbt/reasoning-from-scratch
notion: https://app.notion.com/p/5bb1a73cf20b824aa17001d63976433d
tags: [reading, reasoning-models, pytorch, learning]
timestamp: 2026-07-24
status: summarized
---

# 학습 목표

Sebastian Raschka의 repository는 *Build a Reasoning Model (From Scratch)*의 공식 code다. Transformer pre-training 전체를 다시 하는 것이 아니라 pretrained open-source Qwen3 base model에서 시작해 작은 기능성 reasoning model을 만드는 교육 과정이다. 기존 pretrained weight를 불러오는 code도 제공한다.

# 진행 순서

1장은 reasoning model의 의미를 정리하고, 2장은 pretrained LLM의 text generation을 구현한다. 3장에서 reasoning을 평가한 뒤 4장은 여러 sample·compute를 쓰는 inference-time scaling, 5장은 self-refinement를 다룬다. 6~7장은 reinforcement learning과 GRPO 개선, 8장은 큰 reasoning model의 지식을 더 효율적인 model로 distill하는 방법으로 이어진다.

부록에는 Qwen3 source code, 더 큰 model 사용, batching·throughput, 일반적인 LLM evaluation과 chat interface가 있다. 각 장에 main notebook과 exercise solution이 있어 수식을 읽은 뒤 바로 작은 실험으로 연결하기 좋다.

# 무엇을 “from scratch”라고 부르는가

여기서 from scratch는 reasoning 기법을 library 한 줄로 숨기지 않고 단계별 code로 구현한다는 뜻이다. Base LLM의 pre-training data와 weight까지 처음부터 만드는 과정은 아니다. DeepSeek-R1이나 상용 thinking model과 비슷한 원리를 교육 규모에서 따라가지만, 같은 compute·data·성능을 재현한다고 주장하지 않는다.

# 추천 실습

먼저 고정된 작은 evaluation set과 base score를 저장한다. Inference-time scaling은 sample 수와 latency, RL은 reward hacking과 train instability, distillation은 teacher contamination과 평가 누수를 함께 기록한다. Notebook이 실행되는 것보다 같은 prompt에서 정확도·token·wall time이 어떻게 바뀌는지 표로 남기는 것이 학습 효과가 크다.

# 출처

- [reasoning-from-scratch 저장소](https://github.com/rasbt/reasoning-from-scratch)

