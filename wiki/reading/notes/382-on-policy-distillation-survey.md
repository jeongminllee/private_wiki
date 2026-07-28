---
type: Paper Note
title: "On-Policy Distillation for LLM Survey"
description: "학생 모델이 실제 생성한 trajectory에 교사 feedback을 주어 긴 reasoning의 exposure bias를 줄이는 증류 방법 survey"
resource: "https://arxiv.org/abs/2604.00626"
notion: "https://app.notion.com/p/2c51a73cf20b8369aa2e81ddaf1384ea"
tags: [reading, paper, distillation, llm, reinforcement-learning]
timestamp: 2026-07-24
status: summarized
---

# 문제

전통적 knowledge distillation은 교사가 만든 완성도 높은 text를 학생이 정적으로 모방한다. 학습 때는 늘 올바른 teacher prefix를 보지만 inference에서는 자신의 token을 이어가므로, 작은 오류 뒤의 상태를 복구하는 법을 배우지 못한다. Sequence가 길고 reasoning이 복잡할수록 이 exposure bias가 누적된다.

# On-Policy Distillation

On-policy distillation(OPD)은 학생이 현재 policy로 만든 trajectory 위에서 교사가 feedback을 제공하도록 training loop를 바꾼다. 학생이 실제로 방문하는 잘못된 중간 상태를 보고 correction을 학습하므로, 단일 pass imitation보다 iterative correction에 가깝다.

Survey는 OPD를 student-sampled trajectory 위의 `f-divergence` 최소화로 formalize하고 세 축으로 정리한다. 무엇을 optimize하는지, signal이 teacher distribution·reward·self-play 중 어디서 오는지, training을 어떻게 stabilize하는지가 그 축이다. 이 관점에서 OPD와 KL-constrained reinforcement learning의 경계도 연결한다.

# 실무 의미와 열린 문제

긴 chain-of-thought나 agent trajectory를 작은 model에 옮길 때 final answer만 복제하는 것보다 recovery behavior를 학습할 가능성이 있다. 반면 on-policy sample 생성과 teacher feedback은 비용이 크고, 불완전한 teacher의 오류를 반복 강화할 수 있다. Reward hacking, distribution drift와 mode collapse도 별도 검증해야 한다.

저자들은 distillation scaling law, uncertainty-aware feedback, agent-level distillation과 RL·distillation의 통합을 열린 문제로 둔다. 현재 문서는 `Ongoing Work`로 표시된 survey이므로 revision에 따라 taxonomy와 결론이 달라질 수 있다.

# 출처

- [arXiv 최신 revision](https://arxiv.org/abs/2604.00626)
