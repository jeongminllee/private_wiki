---
type: Concept
title: "07. 기술통계 및 확률분포 (Descriptive Statistics & Distributions)"
description: "대푯값(평균/중앙값/최빈값), 산포도(분산/표준편차/IQR), 왜도/첨도, 주요 확률분포 및 중심극한정리를 분석합니다."
tags: [statistics, descriptive-statistics, variance, skewness, normal-distribution, clt]
timestamp: 2026-08-19
status: active
---

# Summary
기술통계(Descriptive Statistics)는 수집된 데이터를 요약하고 정리하여 데이터의 전반적인 특성을 수치나 그래프로 기술하는 통계 기법이다. 데이터의 중심 위치를 나타내는 **대푯값**, 흩어진 정도를 나타내는 **산포도**, 분포의 비대칭성을 나타내는 **왜도/첨도**로 파악하며, **중심극한정리(CLT)**를 통해 표본 통계량의 정규분포 근사를 보장한다.

---

# Key Ideas

## 1. 대푯값과 산포도

### 대푯값 (Measures of Central Tendency)
- **산술평균 (Mean)**: $\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$ (이상치에 민감함)
- **중앙값 (Median)**: 데이터를 크기순 정렬했을 때 정중앙 값 (이상치에 강건/Robust)
- **최빈값 (Mode)**: 빈도수가 가장 높은 값 (범주형 데이터에 주로 활용)

### 산포도 (Measures of Dispersion)
- **표본분산 (Sample Variance)**: $s^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \bar{x})^2$ (자유도 $n-1$ 적용)
- **표본표준편차 (Standard Deviation)**: $s = \sqrt{s^2}$
- **사분위수 범위 (IQR, Interquartile Range)**: $IQR = Q_3 - Q_1$ (박스플롯 이상치 판정에 사용)

## 2. 왜도(Skewness)와 첨도(Kurtosis)
- **왜도 (Skewness)**:
  - 왜도 > 0 (오른쪽 꼬리 분포, Positive Skew): `평균 > 중앙값 > 최빈값`
  - 왜도 = 0 (대칭 분포): `평균 = 중앙값 = 최빈값`
  - 왜도 < 0 (왼쪽 꼬리 분포, Negative Skew): `최빈값 > 중앙값 > 평균`
- **첨도 (Kurtosis)**: 정규분포(첨도=3 또는 기준 0) 대비 뾰족한 정도.

## 3. 중심극한정리 (Central Limit Theorem, CLT)
- 모집단의 분포 형태와 상관없이 표본의 크기 $n$이 충분히 크다면($n \ge 30$), 표본평균 $\bar{X}$의 표본분포는 정규분포 $N(\mu, \frac{\sigma^2}{n})$에 근사한다.

---

# Related Concepts
- [08. 추론통계 및 가설검정](08-inferential-statistics-hypothesis-testing.md) - 중심극한정리에 기반한 가설 검정
- [11. 데이터마이닝 전처리](11-datamining-and-preprocessing.md) - IQR 기반 이상치 탐지

---

# Citations
- `raw/notes/Bigdata_analysis/빅분기자료/4과목_1_통계분석의 이해.pdf`
- `raw/notes/Bigdata_analysis/빅분기자료/4과목_2_기초 통계분석과 상관분석.pdf`
