---
type: Concept
title: "15. 머신러닝 모델 평가 지표 및 최적화 (Model Evaluation & Optimization)"
description: "혼동행렬(Confusion Matrix), 정밀도/재현율/F1, ROC-AUC 곡선, K-Fold 교차검증 및 하이퍼파라미터 튜닝 기법을 정리합니다."
tags: [machine-learning, evaluation, confusion-matrix, roc-auc, f1-score, cross-validation, grid-search]
timestamp: 2026-08-19
status: active
---

# Summary
머신러닝 모델의 실무 유효성을 검증하기 위해서는 단순 정확도(Accuracy)를 넘어 불균형 데이터에 강건한 **혼동행렬(Confusion Matrix)** 기반 지표(정밀도, 재현율, F1-Score, ROC-AUC)를 종합적으로 평가해야 한다. 또한 과적합을 방지하기 위한 **K-Fold 교차검증**과 최적 파라미터를 탐색하는 **Grid/Random Search** 최적화 기법을 적용한다.

---

# Key Ideas

## 1. 혼동행렬 (Confusion Matrix)과 4대 평가지표

```
                 [ 실제 실제값 (Actual) ]
                    Positive (1)        Negative (0)
[ 예측 예측값 ] ──────────────────────────────────────────
Positive (1)   │   TP (True Positive)   │   FP (False Positive)
Negative (0)   │   FN (False Negative)  │   TN (True Negative)
```

- **정확도 (Accuracy)**: $\frac{TP + TN}{TP + FP + FN + TN}$ (전체 중 맞춘 비율)
- **정밀도 (Precision)**: $\frac{TP}{TP + FP}$ (Positive로 예측한 것 중 실제 Positive 비율 - 스팸 필터링에 중요)
- **재현율 (Recall / Sensitivity)**: $\frac{TP}{TP + FN}$ (실제 Positive 중 올바르게 감지한 비율 - 암 진단, 불량품 검출에 중요)
- **F1-Score**: 정밀도와 재현율의 조화평균 (불균형 데이터 평가에 최적)
  $$F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

## 2. ROC 곡선과 AUC (Area Under Curve)
- **ROC 곡선**: 분류 임계값(Threshold)을 변화시키며 x축에 **FPR (False Positive Rate, $1 - \text{특이도}$)**, y축에 **TPR (True Positive Rate, 재현율)**을 그린 곡선.
- **AUC**: ROC 곡선 아래 면적 ($0.5 \le AUC \le 1$). 1에 가까울수록 우수한 분류기.

## 3. 교차검증 및 하이퍼파라미터 튜닝
- **K-Fold 교차검증 (Cross Validation)**: 전체 데이터를 $K$개의 폴드로 나누어 $K-1$개로 훈련하고 1개로 검증하는 과정을 $K$회 반복하여 일반화 성능 평가.
- **Grid Search vs Random Search**: 파라미터 조합의 전수 조사(Grid) vs 지정된 분포 내 무작위 샘플링(Random)을 통한 최적 모델 도출.

---

# Related Concepts
- [12. 지도학습 분류](12-classification-algorithms.md) - 분류 모델 학습
- [13. 앙상블 학습](13-ensemble-learning.md) - 앙상블 튜닝

---

# Citations
- `raw/notes/Bigdata_analysis/빅분기자료/4과목_통계 분석 문제 풀이.pdf`
- `raw/notes/Bigdata_analysis/빅데이터분석기사_모든것_ocr.pdf`
