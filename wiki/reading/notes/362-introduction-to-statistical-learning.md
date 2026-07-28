---
type: Reference
title: "An Introduction to Statistical Learning 학습 안내"
description: "통계학습의 핵심 방법을 수식 부담을 낮춰 설명하고 R·Python 실습과 무료 PDF를 제공하는 공식 교재"
resource: "https://www.statlearning.com/"
notion: "https://app.notion.com/p/7641a73cf20b8287b7738163d02ba9ec"
tags: [reading, statistics, machine-learning, textbook, python, r]
timestamp: 2026-07-24
status: summarized
---

# 책의 위치

`An Introduction to Statistical Learning(ISL)`은 통계적 학습을 폭넓게 소개하되 이론 전개보다 직관과 실제 분석을 앞세운 교재다. Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani가 집필했고 Python 판에는 Jonathan Taylor가 참여했다. 공식 사이트에서 R 2판과 Python 판 PDF, 실습 자료와 공개 강의를 제공한다.

# 다루는 내용

회귀와 분류에서 시작해 resampling, model selection과 regularization, 비선형 방법, tree와 ensemble, support vector machine, deep learning, survival analysis, unsupervised learning, multiple testing으로 확장한다. 각 장의 lab은 개념을 실제 data와 연결하는 역할을 한다.

# 읽는 방법

처음부터 algorithm 목록을 외우기보다 다음 질문을 장마다 반복하는 편이 좋다.

- 어떤 prediction 또는 inference 문제인가?
- Train·validation·test를 어떻게 나누며 data leakage는 없는가?
- Bias와 variance가 어떻게 바뀌는가?
- Metric과 uncertainty가 실제 의사결정에 맞는가?
- 더 복잡한 model이 단순 baseline보다 정말 나은가?

ISL은 접근 가능한 입문서지만 “수학이 필요 없다”는 뜻은 아니다. 선형대수, 확률과 회귀 기초를 함께 복습하고, 더 엄밀한 이론이 필요할 때는 같은 저자들의 `The Elements of Statistical Learning`이나 원 논문으로 넘어가는 흐름이 좋다. 판본별 errata도 확인해야 한다.

# 출처

- [ISL 공식 사이트](https://www.statlearning.com/)
