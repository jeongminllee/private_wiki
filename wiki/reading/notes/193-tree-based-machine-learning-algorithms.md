---
type: Concept
title: "트리 기반 머신러닝 알고리즘 비교"
description: "결정 트리, 랜덤 포레스트, Gradient Boosting, XGBoost의 학습 방식과 선택 기준"
resource: https://www.geeksforgeeks.org/machine-learning/tree-based-machine-learning-algorithms/
notion: https://app.notion.com/p/6bf1a73cf20b82afac6c0143e3c84ab5
tags: [reading, machine-learning, decision-tree, ensemble]
timestamp: 2026-07-24
status: summarized
---

# 기본 원리

트리는 특성에 대한 조건으로 데이터를 반복 분할한다. 내부 노드는 질문, 가지는 조건 결과, 잎은 분류 레이블이나 회귀 평균값이다. 분류에서는 Gini impurity나 entropy, 회귀에서는 분산 감소 같은 기준으로 분할을 고른다.

# 알고리즘 비교

| 방법 | 학습 방식 | 장점 | 주의점 |
| --- | --- | --- | --- |
| Decision Tree | 한 트리를 재귀 분할 | 규칙을 설명하기 쉽고 전처리가 적음 | 깊어지면 과적합과 불안정성이 큼 |
| Random Forest | bootstrap 표본과 무작위 특성으로 여러 트리를 독립 학습 | 분산을 낮추고 튜닝이 비교적 쉬움 | 큰 모델, 느린 추론, 개별 규칙 해석 어려움 |
| Gradient Boosting | 앞 트리의 잔차를 다음 얕은 트리가 순차 보정 | 표 형식 데이터에서 높은 정확도 | 학습률·트리 수·깊이에 민감함 |
| XGBoost | 정규화와 시스템 최적화를 더한 boosting | 결측 처리, 병렬화, 강한 성능 | 설정이 많고 잘못된 검증에서는 쉽게 과적합 |

# 선택 기준

해석 가능한 기준선에는 작은 결정 트리, 안정적인 기본 성능에는 랜덤 포레스트, 충분한 튜닝과 최고 성능이 필요하면 XGBoost·LightGBM·CatBoost 같은 boosting 계열이 적합하다. 범주형 특성, 결측치, 불균형, 데이터 크기에 따라 구현체를 고른다.

# 평가할 때

시계열이나 사용자 데이터는 무작위 분할이 누수를 만들 수 있으므로 실제 배포 단위에 맞게 나눈다. 정확도 하나가 아니라 불균형 분류의 PR-AUC, calibration, 추론 지연, 모델 크기, feature importance의 안정성을 함께 본다.

# 출처

- [Tree Based Machine Learning Algorithms](https://www.geeksforgeeks.org/machine-learning/tree-based-machine-learning-algorithms/)

