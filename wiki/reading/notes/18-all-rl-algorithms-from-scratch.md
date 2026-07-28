---
type: Reference
title: All RL Algorithms from Scratch
description: 강화학습 알고리즘 18가지를 기본 라이브러리로 직접 구현하며 배우는 교육용 저장소
resource: https://discuss.pytorch.kr/t/all-rl-algorithms-from-scratch-18/11093
notion: https://app.notion.com/p/3941a73cf20b8160b058f2a68b0daf5e
tags: [reading, repository, reinforcement-learning, education]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

복잡한 강화학습 라이브러리의 추상화를 걷어내고 NumPy, Matplotlib, PyTorch로 18개 알고리즘을 구현한 교육용 저장소다. 속도와 완성도보다 핵심 업데이트 식과 학습 과정이 코드에서 보이도록 하는 데 목적이 있다.

# 핵심 내용

- 가치 기반에는 Q-Learning, SARSA, Expected SARSA, DQN 등이 포함된다.
- 정책 기반과 액터-크리틱에는 REINFORCE, TRPO, A2C, A3C, PPO, DDPG, SAC 등이 있다.
- 계획·모델 기반 방법과 다중 에이전트 학습까지 단계적으로 확장한다.
- 보상·손실 곡선, Q 값 히트맵, 정책 화살표 같은 시각화로 학습 변화를 확인한다.
- 별도 치트시트가 주요 알고리즘의 개념과 업데이트 식을 한눈에 정리한다.

# 왜 읽을 만한가

Stable-Baselines 같은 라이브러리로 바로 실험할 때 가려지는 상태 전이, 탐험, 타깃 계산과 정책 갱신을 직접 볼 수 있다. 알고리즘 간 차이를 수식과 코드로 연결하기 좋은 실습 자료다.

# 추천 학습 순서

1. 단순 환경과 Q-Learning으로 가치 갱신을 이해한다.
2. SARSA 계열로 온폴리시와 오프폴리시 차이를 비교한다.
3. REINFORCE와 A2C로 정책 경사와 분산 감소를 본다.
4. DQN과 PPO를 작은 환경에서 재현한다.
5. 모델 기반과 다중 에이전트는 앞 단계의 평가 코드를 재사용해 비교한다.

# 주의할 점

저자도 교육 목적의 단순화와 일부 복잡한 노트북의 버그 가능성을 알린다. A3C는 멀티프로세싱 때문에 노트북 밖에서 실행해야 하며, 이 구현을 프로덕션 기준 코드로 사용해서는 안 된다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/all-rl-algorithms-from-scratch-18/11093)
- [GitHub 저장소](https://github.com/fareedkhan-dev/all-rl-algorithms)
- [Notion 원본 항목](https://app.notion.com/p/3941a73cf20b8160b058f2a68b0daf5e)
