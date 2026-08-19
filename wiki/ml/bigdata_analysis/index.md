---
type: Reference
title: "Big Data Analysis & Data Science Study Dashboard (빅데이터 분석 학습 대시보드)"
description: "빅데이터 기획, 통계적 가설 검정, 회귀분석, 머신러닝/데이터마이닝 분류·군집·앙상블 모델 및 평가 지표를 포괄하는 종합 학습 인덱스입니다."
tags: [bigdata, data-science, statistics, machine-learning, datamining, index, reference]
timestamp: 2026-08-19
status: active
---

# Big Data Analysis & Data Science Study Dashboard

빅데이터의 기초 개념과 전략적 인사이트부터 분석 기획 방법론(KDD, CRISP-DM), 기초/추론 통계(가설검정, ANOVA, 회귀분석), 머신러닝 데이터마이닝 기법(분류, 앙상블, 군집, 연관분석) 및 모델 평가 지표에 이르는 빅데이터 분석 종합 지식 대시보드입니다.

---

## 📚 주제별 지식 문서 목록

### Part 1. 빅데이터 이해 및 전략적 기획
- **[01. 데이터와 정보 (Data & Information)](01-data-and-information.md)** - DIKW 피라미드, 정형/반정형/비정형 데이터, 데이터베이스 및 데이터웨어하우스/데이터레이크
- **[02. 빅데이터의 특성과 가치 (Big Data Value & Impact)](02-bigdata-characteristics-value.md)** - 3V~5V 특성, 출현 배경, 데이터 경제 및 비즈니스 가치 창출 패러다임
- **[03. 전략적 인사이트와 데이터 사이언스 (Data Science Strategy)](03-bigdata-strategy-insights.md)** - 데이터 사이언티스트 핵심 역량(Analytics + IT + Domain), 인문학적 소양과 가치 전환

### Part 2. 분석 방법론 및 거버넌스
- **[04. 분석 기획 및 과제 발굴 (Analysis Planning & Discovery)](04-analysis-planning-directions.md)** - 하향식(Top-Down) vs 상향식(Bottom-Up) 과제 발굴, 디자인 씽킹, 최적화·통찰·솔루션 매트릭스
- **[05. 데이터 분석 방법론 (Analysis Methodologies)](05-data-analysis-methodology.md)** - KDD 5단계, CRISP-DM 6단계, 빅데이터 분석 5단계 생명주기(기획-준비-개발-테스트-전개)
- **[06. 분석 마스터플랜 및 거버넌스 (Master Plan & Governance)](06-analysis-masterplan-governance.md)** - 과제 우선순위 평가(시급성 vs 난이도), 분석 준비도/성숙도 진단 4분면, 데이터 거버넌스 체계

### Part 3. 기초 통계 및 가설 검정
- **[07. 기술통계 및 확률분포 (Descriptive Statistics & Distributions)](07-descriptive-statistics-distributions.md)** - 대푯값(평균/중앙값/최빈값), 산포도(분산/표준편차/IQR), 왜도와 첨도, 정규분포/이항분포/포아송분포, 중심극한정리
- **[08. 추론통계 및 가설검정 (Inferential Statistics & Hypothesis Testing)](08-inferential-statistics-hypothesis-testing.md)** - 점추정/구간추정, 귀무가설($H_0$)과 대립가설($H_1$), 1종·2종 오류, p-value 판정 기준, 단일표본/독립표본/대응표본 t-검정
- **[09. 분산분석 및 교차/카이제곱 검정 (ANOVA & Chi-Square Test)](09-anova-and-chi-square.md)** - 일원/이원 분산분석, F-검정 통계량, 사후검정(Scheffe, Tukey), 적합도/독립성/동질성 카이제곱 검정($\chi^2$)
- **[10. 상관분석 및 선형 회귀분석 (Correlation & Linear Regression)](10-correlation-and-regression.md)** - 피어슨/스피어만 상관계수, 단순/다중 선형회귀(OLS), 결정계수($R^2$), 다중공선성(VIF), 회귀 잔차 4대 가정(선형성, 독립성, 등분산성, 정규성)

### Part 4. 데이터마이닝, 머신러닝 및 모델 평가
- **[11. 데이터마이닝 및 전처리 (Data Preprocessing & Mining)](11-datamining-and-preprocessing.md)** - 결측치 처리, 이상치 탐지(IQR, Z-score), 정규화/표준화 스케일링, 주성분 분석(PCA) 차원축소
- **[12. 지도학습 분류 분석 (Classification Algorithms)](12-classification-algorithms.md)** - 로지스틱 회귀(Odds Ratio/Sigmoid), 의사결정나무(지니지수/엔트로피), 나이브 베이즈, 서포트 벡터 머신(SVM), KNN
- **[13. 앙상블 학습 기법 (Ensemble Methods)](13-ensemble-learning.md)** - 배깅(Bagging) & Random Forest, 부스팅(Boosting - AdaBoost, GBM, XGBoost, LightGBM), 보팅 및 스태킹
- **[14. 군집 분석 및 연관 분석 (Clustering & Association Rules)](14-clustering-and-association.md)** - K-Means, 계층적 군집(덴드로그램), DBSCAN, 실루엣 계수 평가, Apriori 알고리즘(지지도, 신뢰도, 향상도)
- **[15. 모델 평가 지표 및 최적화 (Model Evaluation & Tuning)](15-model-evaluation-and-optimization.md)** - 혼동행렬(Confusion Matrix), 정확도/정밀도/재현율/F1-score, ROC-AUC 곡선, K-Fold 교차검증, 하이퍼파라미터 튜닝

---

## 🔗 관련 문서 및 상위 인덱스
- [ML Study Index](../index.md) - 머신러닝 학습 대시보드
- [MML Study](../mml/index.md) - 머신러닝을 위한 수학 기초
- [CS Study Index](../../cs/index.md) - 컴퓨터 과학 핵심 개념 인덱스
- [Root Wiki Index](../../../index.md) - 전체 지식베이스 루트 인덱스
