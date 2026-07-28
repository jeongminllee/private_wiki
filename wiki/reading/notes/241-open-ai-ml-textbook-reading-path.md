---
type: Reference
title: "오픈 AI·ML 교재 11권을 단계별로 읽는 경로"
description: "머신러닝 기초부터 시스템, 강화학습, 공정성과 확률 모델까지 공개 교재를 목적별로 고르는 안내"
resource: https://cs.nyu.edu/~mohri/mlbook/
notion: https://app.notion.com/p/4691a73cf20b835b90da81ade593c906
tags: [reading, machine-learning, textbook, learning-path]
timestamp: 2026-07-24
status: summarized
---

# 목록을 읽는 법

저장된 글은 서로 난도와 목적이 다른 공개 AI·ML 교재 11권을 한데 모은다. 전부 처음부터 읽기보다 현재 목표에 맞는 한 갈래를 정하고, 수학적 기초가 부족할 때 앞 단계로 돌아가는 편이 효율적이다.

# 추천 경로

## 머신러닝과 딥러닝 기초

1. [Foundations of Machine Learning](https://cs.nyu.edu/~mohri/mlbook/)은 일반화, 복잡도와 학습 이론을 수학적으로 다룬다.
2. [Understanding Deep Learning](https://udlbook.github.io/udlbook/)은 현대 딥러닝을 직관과 이론으로 연결한다.
3. [Deep Learning](https://www.deeplearningbook.org/)은 최적화, 신경망과 생성 모델의 고전적 기준점이다.
4. [Algorithms for Machine Learning](https://algorithmsbook.com/)은 학습 문제를 알고리즘 설계 관점에서 정리한다.

이론보다 구현을 먼저 익히려면 2번을 중심으로 읽고, 증명과 일반화가 궁금할 때 1번으로 확장하는 순서가 자연스럽다.

## 시스템과 운영

[Introduction to Machine Learning Systems](https://mlsysbook.ai/book/)은 모델 자체보다 데이터, 학습 파이프라인, 배포, 모니터링과 운영상의 trade-off를 다룬다. 실제 서비스를 만들려는 독자라면 이론서와 병행할 가치가 크다.

## 강화학습과 에이전트

- [Reinforcement Learning: An Introduction](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf): value function, temporal-difference와 policy-gradient의 표준 입문서
- [Distributional Reinforcement Learning](https://direct.mit.edu/books/oa-monograph-pdf/2111075/book_9780262374026.pdf): 기대 보상이 아니라 return distribution을 모델링하는 고급 주제
- [Multi-Agent Reinforcement Learning](https://marl-book.com/): 여러 agent의 협력·경쟁과 game-theoretic 관점
- [Agents in the Long Game of AI](https://direct.mit.edu/books/oa-monograph-pdf/2471103/book_9780262380355.pdf): 장기적 agent 설계와 AI 연구의 큰 그림

# 책임성과 확률 모델

[Fairness and Machine Learning](https://fairmlbook.org/)은 공정성 정의가 서로 충돌할 수 있다는 점과 측정·의사결정의 사회적 맥락을 다룬다. Kevin Murphy의 [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html)과 [Advanced Topics](https://probml.github.io/pml-book/book2.html)은 확률 모델, 추론과 현대 ML을 폭넓게 참조할 수 있는 두 권짜리 자료다.

# 주의할 점

“Open Access”가 곧 자유로운 재배포·수정을 뜻하지는 않는다. 예를 들어 *Foundations of Machine Learning* 공개본은 별도 저작권·라이선스 조건이 있으므로 각 사이트의 이용 조건을 확인해야 한다. 링크 모음은 독서 지도이지, 모든 책을 순서대로 완독해야 하는 curriculum은 아니다.

