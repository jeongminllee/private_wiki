---
type: Paper Note
title: "Parcae: 안정적인 반복형 언어 모델"
description: "같은 블록을 반복해 매개변수와 메모리를 크게 늘리지 않고 계산량을 확장하는 언어 모델"
resource: https://share.google/ZlAMWVVgrsKGq1Omr
resource_aliases: [https://arxiv.org/pdf/2604.12946]
notion: https://app.notion.com/p/afc1a73cf20b833897f88151a260c22c
tags: [reading, paper, language-model, architecture]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

Parcae는 동일한 신경망 블록을 여러 번 통과시키는 looped language model의 불안정성을 줄여, 매개변수 수를 고정한 채 추론 계산량을 늘릴 수 있게 한 구조다.

# 문제와 방법

기존 반복형 모델은 순환할수록 residual이 커지고 학습 손실이 급등하기 쉽다. 저자들은 이를 동역학계로 해석하고, 입력 주입 매개변수의 큰 spectral norm을 원인으로 지목한다. 음의 대각 성분을 이산화한 매개변수화로 반복 과정의 안정성을 제한한다.

# 보고된 결과

- 기존 반복형 모델보다 검증 perplexity를 최대 6.3% 낮췄다고 보고한다.
- 반복 횟수와 데이터 양을 함께 늘리는 scaling law를 제시한다.
- 1.3B 모델에서 같은 매개변수·데이터 조건의 Transformer보다 CORE 2.99점, CORE-Extended 1.18점 높았다고 보고한다.
- 저자 평가에서는 두 배 큰 Transformer 품질의 최대 87.5%에 도달한다.

# 해석

반복 계산은 모델 파일과 메모리가 제한된 환경에서 품질을 높일 후보지만 지연 시간은 늘어난다. 실제 적용에서는 메모리 절감뿐 아니라 처리량, 반복 횟수별 수익 체감, 하드웨어 활용률을 함께 측정해야 한다.

# 출처

- [Parcae 논문](https://arxiv.org/abs/2604.12946)

