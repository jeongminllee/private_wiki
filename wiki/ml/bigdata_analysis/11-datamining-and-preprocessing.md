---
type: Concept
title: "11. 데이터마이닝 및 전처리 기법 (Data Preprocessing & Mining)"
description: "결측치 처리(대체법), 이상치 탐지(IQR/Z-score), 특성 스케일링 및 주성분 분석(PCA) 차원 축소를 설명합니다."
tags: [datamining, preprocessing, imputation, outlier, scaling, pca, dimension-reduction]
timestamp: 2026-08-19
status: active
---

# Summary
데이터 전처리(Data Preprocessing)는 원천 데이터의 결측치, 이상치, 노이즈를 정제하고, 단위와 분포를 스케일링하며, 차원의 저주를 극복하기 위해 특징을 변환하는 머신러닝의 필수 기초 단계이다. 데이터의 품질이 머신러닝 모델의 성능 상한선을 결정한다(Garbage In, Garbage Out).

---

# Key Ideas

## 1. 결측치(Missing Value) 및 이상치(Outlier) 처리
- **결측치 처리 기법**:
  - 완전 삭제 (Listwise Deletion): 결측 포함 행 전체 제거 (데이터 손실 주의).
  - 평균/중앙값/최빈값 대치 (Simple Imputation).
  - 회귀대치법 및 KNN/MICE 다중대치법: 다른 변수들의 관계를 모델링하여 결측치 예측 대치.
- **이상치 탐지 기법**:
  - **IQR 방식**: $Q_1 - 1.5 \times IQR$ 미만 또는 $Q_3 + 1.5 \times IQR$ 초과인 값을 이상치로 판정.
  - **Z-score (표준점수)**: $|Z| > 3$ 인 경우 이상치로 판정.

## 2. 피처 스케일링 (Feature Scaling)
- **Min-Max 정규화 (Normalization)**: 데이터를 $[0, 1]$ 범위로 선형 변환.
  $$x_{\text{norm}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$
- **표준화 (Standardization / Z-score)**: 평균 0, 표준편차 1인 표준정규분포로 변환.
  $$z = \frac{x - \mu}{\sigma}$$

## 3. 주성분 분석 (PCA, Principal Component Analysis)
- 고차원 데이터의 분산(Variance)을 최대한 보존하는 직교하는 새로운 주성분(Principal Components) 축을 찾아 저차원으로 투영하는 대표적 비지도 차원 축소 알고리즘.
- 데이터의 공분산 행렬로부터 고유값(Eigenvalue)과 고유벡터(Eigenvector)를 계산하여 차원 축소 수행.

---

# Related Concepts
- [10. 상관분석 및 회귀분석](10-correlation-and-regression.md) - 다중공선성 해소를 위한 PCA
- [12. 분류 분석](12-classification-algorithms.md) - 전처리된 데이터 기반 모델 학습

---

# Citations
- `raw/notes/Bigdata_analysis/빅분기자료/4과목_5_데이터마이닝개요.pdf`
