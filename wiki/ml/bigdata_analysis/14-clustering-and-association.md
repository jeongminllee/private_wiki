---
type: Concept
title: "14. 비지도학습 군집 및 연관 분석 (Clustering & Association Rules)"
description: "K-Means, 계층적 군집, DBSCAN, 실루엣 계수 평가 및 Apriori 알고리즘(지지도, 신뢰도, 향상도)을 다룹니다."
tags: [machine-learning, clustering, k-means, dbscan, silhouette, association-rule, apriori]
timestamp: 2026-08-19
status: active
---

# Summary
군집 분석(Clustering)과 연관 분석(Association Rules)은 정답 레이블(Target)이 없는 상태에서 데이터 자체의 유사성과 숨겨진 규칙을 탐색하는 대표적인 **비지도학습(Unsupervised Learning)** 기법이다. 군집 분석은 객체 간 거리를 기준으로 동질적 그룹을 형성하며, 연관 분석(장바구니 분석)은 항목 간 동시 구매 패턴을 도출한다.

---

# Key Ideas

## 1. 군집 분석 주요 알고리즘
- **K-평균 군집화 (K-Means)**:
  - 군집 수 $K$를 사전에 지정하고, 중심점(Centroid)을 반복 갱신하여 군집 내 오차제곱합(SSE)을 최소화.
  - 엘보우 기법(Elbow Method)으로 최적 $K$ 탐색.
- **계층적 군집화 (Hierarchical Clustering)**:
  - 개별 데이터 포인트에서 시작해 가장 가까운 군집을 점진적으로 병합해 나가는 상향식(Agglomerative) 기법.
  - 결과물을 트리 구조의 **덴드로그램(Dendrogram)**으로 시각화.
- **밀도 기반 군집화 (DBSCAN)**:
  - 반경($\epsilon$) 내에 최소 포인트 수(MinPts) 이상이 밀집된 영역을 군집으로 판정. 노이즈(이상치) 탐지에 강건하며 기하학적 형태의 군집 분할 가능.
- **군집 평가 지표 - 실루엣 계수 (Silhouette Coefficient)**:
  - 군집 내 응집도($a$)와 군집 간 분리도($b$)를 측정 ($-1 \le s \le 1$). 1에 가까울수록 군집화가 잘 됨.

## 2. 연관 분석 3대 평가지표 (Apriori Rule: $A \rightarrow B$)

| 지표 | 공식 | 의미 |
| :--- | :--- | :--- |
| **지지도 (Support)** | $P(A \cap B) = \frac{\text{A와 B 동시 거래수}}{\text{전체 거래수}}$ | 전체 거래 중 두 품목이 함께 구매될 확률 |
| **신뢰도 (Confidence)** | $P(B|A) = \frac{P(A \cap B)}{P(A)}$ | 품목 A를 구매했을 때 품목 B도 구매할 조건부 확률 |
| **향상도 (Lift)** | $\frac{P(A \cap B)}{P(A) \times P(B)} = \frac{\text{Confidence}}{P(B)}$ | A와 B가 독립적일 때 대비 동시 구매할 비율<br>• Lift = 1: 독립 (연관성 없음)<br>• Lift > 1: 양의 상관 (유의미한 규칙)<br>• Lift < 1: 음의 상관 |

---

# Related Concepts
- [11. 데이터마이닝 전처리](11-datamining-and-preprocessing.md) - 거리 계산을 위한 스케일링
- [15. 모델 평가](15-model-evaluation-and-optimization.md) - 머신러닝 평가 지표

---

# Citations
- `raw/notes/Bigdata_analysis/빅분기자료/4과목_6_군집분석.pdf`
