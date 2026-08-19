---
type: Concept
title: "12. 지도학습 분류 분석 (Classification Algorithms)"
description: "로지스틱 회귀, 의사결정나무(지니/엔트로피), 나이브 베이즈, 서포트 벡터 머신(SVM), KNN 분류 알고리즘을 분석합니다."
tags: [machine-learning, classification, logistic-regression, decision-tree, naive-bayes, svm, knn]
timestamp: 2026-08-19
status: active
---

# Summary
분류 분석(Classification Analysis)은 지도학습(Supervised Learning)의 대표적인 형태로, 입력 데이터의 독립변수 특징들을 기반으로 사전에 정의된 이산형 범주 레이블(Class)을 예측하는 알고리즘 집합이다.

---

# Key Ideas

## 1. 로지스틱 회귀 (Logistic Regression)
- 종속변수가 0 또는 1인 이항 범주일 때, **승산비(Odds Ratio)**와 **시그모이드 함수(Sigmoid Function)**를 적용하여 특정 클래스에 속할 확률 $P(Y=1|X)$을 추정.
  $$P = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X)}}$$

## 2. 의사결정나무 (Decision Tree)
- 데이터를 특정 분기 기준에 따라 나무 구조로 반복 분할하는 직관적인 화이트박스 모델.
- **분할 기준 불순도(Impurity) 지표**:
  - **지니 지수 (Gini Index, CART)**: $Gini = 1 - \sum_{i=1}^c p_i^2$ (지니지수가 작을수록 순도가 높음)
  - **엔트로피 (Entropy / Information Gain, C4.5)**: $Entropy = -\sum_{i=1}^c p_i \log_2 p_i$

## 3. 기타 핵심 분류 알고리즘
- **나이브 베이즈 (Naive Bayes)**: 베이즈 정리(Bayes' Theorem)와 모든 특성이 상호 독립이라는 가정을 기반으로 사후확률을 계산. 텍스트 스팸 필터링에 강력.
- **서포트 벡터 머신 (SVM)**: 클래스를 구분하는 **최대 마진(Margin)을 갖는 초평면(Hyperplane)**을 찾고, 비선형 분류를 위해 커널 트릭(Kernel Trick, RBF 등)을 활용.
- **K-최근접 이웃 (KNN)**: 새로운 데이터가 들어왔을 때 가장 가까운 $K$개의 이웃 레이블을 다수결로 판정하는 게으른 학습(Lazy Learner).

---

# Related Concepts
- [13. 앙상블 학습](13-ensemble-learning.md) - 의사결정나무를 확장한 랜덤포레스트/부스팅
- [15. 모델 평가 지표](15-model-evaluation-and-optimization.md) - 혼동행렬, ROC-AUC 평가

---

# Citations
- `raw/notes/Bigdata_analysis/빅분기자료/4과목_5_분류분석의 개요.pdf`
