---
type: Reference
title: "Q-learning이 아직 장기 문제에 확장되기 어려운 이유"
description: "100단계 이상의 의미 있는 의사결정이 필요한 long-horizon task에서 value 기반 RL의 병목을 짚은 글"
resource: https://seohong.me/blog/q-learning-is-not-yet-scalable/
notion: https://app.notion.com/p/d351a73cf20b82b1bd420185d6a1c426
tags: [reading, reinforcement-learning, q-learning, long-horizon]
timestamp: 2026-07-24
status: summarized
---

# 핵심 주장

글은 현재 Q-learning 계열이 수백 단계의 의미 있는 결정을 요구하는 long-horizon 문제에 아직 쉽게 확장되지 않는다고 주장한다. 큰 neural network와 많은 compute만 더하는 것으로는 bootstrapping error와 exploration 문제를 해결하기 어렵다는 관점이다.

# 왜 어려운가

Q-learning은 다음 상태의 추정값으로 현재 값을 갱신한다. horizon이 길면 작은 value error가 여러 단계를 거쳐 전파되고, 아직 방문하지 않은 상태의 과대 추정이 정책을 잘못된 방향으로 이끌 수 있다. 보상이 마지막에만 주어지는 문제에서는 어느 행동이 결과를 만들었는지 credit assignment가 더 어려워진다.

또한 최적 행동을 찾으려면 긴 action sequence를 탐색해야 한다. 무작위 탐색으로 의미 있는 성공 trajectory를 발견할 확률은 단계가 늘수록 급격히 낮아진다. offline data를 쓰더라도 dataset 밖 행동의 value를 신뢰하기 어렵다.

# 실용적 함의

장기 agent task에 Q-learning을 적용할 때는 전체 문제를 하나의 MDP로 밀어 넣기보다 hierarchy, subgoal, model-based planning, imitation data와 verifier를 결합하는 편이 현실적이다. 짧은 horizon benchmark의 성공을 실제 장기 업무 자동화로 일반화해서는 안 된다.

# 출처

- [Q-learning is not yet scalable](https://seohong.me/blog/q-learning-is-not-yet-scalable/)

