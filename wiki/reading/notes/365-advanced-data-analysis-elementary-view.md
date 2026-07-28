---
type: Reference
title: "Advanced Data Analysis from an Elementary Point of View"
description: "회귀의 가정부터 비모수·고차원 분석까지 모델을 비판적으로 사용하는 법을 다루는 Cosma Shalizi의 공개 초고"
resource: "https://stat.cmu.edu/~cshalizi/ADAfaEPoV"
notion: "https://app.notion.com/p/d471a73cf20b838b9a8081bdfdfd994f"
tags: [reading, statistics, data-analysis, textbook, regression]
timestamp: 2026-07-24
status: summarized
---

# 책의 성격

Cosma Rohilla Shalizi가 고급 학부 한 학기 수업을 위해 쓰는 통계 data analysis 초고다. 제목의 `elementary`는 초심자용이라는 뜻보다, 이미 배운 probability, mathematical statistics와 linear regression을 출발점으로 더 현대적인 분석을 구축한다는 의미에 가깝다.

# 중심 관점

Data에 선형 model을 바로 맞추는 cookbook 방식보다, 왜 그 model이 적절한지와 가정이 깨졌을 때 무엇을 할지를 묻는다. Smoothing과 nonparametric regression은 선형성을 기본값으로 두지 않고 관계의 형태를 data에서 확인하는 수단이다. Model evaluation, resampling, additive model, tree, density estimation과 clustering 같은 주제도 “기법 목록”보다 예측·추론 목적과 검증을 중심으로 연결된다.

# 학습 방법과 제한

각 장을 읽을 때 가정, estimator, uncertainty, diagnostic, 대안 model을 한 묶음으로 정리하고 R exercise를 직접 재현하는 편이 좋다. 동일 data에 단순 baseline과 유연한 model을 모두 적용해 out-of-sample error와 해석 가능성을 비교하면 책의 관점이 선명해진다.

공개본은 계속 바뀌는 draft이므로 page나 표현을 인용할 때 version을 적어야 한다. 저자는 허가 없는 재배포를 금지하고 있으므로 PDF를 wiki에 복제하지 않고 공식 page만 연결한다.

# 출처

- [저자 공식 교재 페이지](https://stat.cmu.edu/~cshalizi/ADAfaEPoV/)
