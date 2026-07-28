---
type: Reference
title: "LinkedIn의 PyTorch 기반 초대규모 선형계획 최적화"
description: "CPU 중심 DuaLip을 희소 텐서와 멀티 GPU 기반 DuaLip-PyTorch로 재설계한 사례"
resource: https://pytorch.kr/blog/2026/how-linkedin-uses-pytorch-extreme-scale-optimization/
notion: https://app.notion.com/p/3891a73cf20b81d6a18ff7e152a09907
tags: [reading, pytorch, optimization, gpu, linear-programming]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

LinkedIn의 추천, 구직자-채용 공고 매칭, 이메일 발송량 같은 의사결정은 참여도·매출을 높이면서 예산·공정성·빈도 제한을 지켜야 하는 선형계획 문제로 표현할 수 있다. 규모가 수조 개 결정 변수까지 커지면 고전적 simplex나 interior-point 방식의 행렬 분해 비용을 감당하기 어렵다. 이 사례는 기존 Scala/Spark 기반 DuaLip 솔버를 GPU 친화적인 PyTorch 실행 엔진으로 다시 만든 과정을 설명한다.

# 접근법

DuaLip은 ridge-regularized dual ascent와 1차 최적화에 기반한 분산 솔버다. 비싼 행렬 분해 대신 희소 행렬-벡터 곱, 가속 변화도 갱신, projection을 반복한다. 원래 구현은 CPU와 스키마 중심 인터페이스에 묶여 새 문제를 추가하기 어려웠다.

DuaLip-PyTorch는 태스크 수준의 “솔버 호출” API보다 연산자 수준의 텐서 프로그래밍 모델을 택했다.

- 핫 패스를 희소 행렬-벡터 연산과 블록 단위 projection의 명시적 데이터 흐름으로 표현한다.
- 수십억~수조 변수는 희소 텐서와 배치 projection 커널로 GPU에서 처리한다.
- 변수는 여러 GPU에 분할하고 dual 변수는 `all-reduce`와 `broadcast`로 복제·동기화한다.
- 행 정규화와 스케일링, regularization continuation, AGD와 FISTA 계열 방법으로 조건과 수렴 속도를 개선한다.

# 결과와 의미

글은 CPU 시스템 대비 자릿수 단위 속도 향상, 단일 GPU에서 멀티 GPU로의 효율적 확장, 더 유연한 LP 정식화, ML과 최적화 실행 스택의 통합을 장점으로 제시한다. 제시된 비교에서는 8 GPU PyTorch 솔버가 반복당 벽시계 시간에서 Scala 구현보다 75배 빠른 사례를 보인다.

이 사례의 큰 교훈은 PyTorch가 신경망에만 쓰이는 것이 아니라, 계산을 텐서 연산으로 표현하고 GPU·분산 통신을 이용할 수 있는 범용 수치 실행 계층이 될 수 있다는 점이다.

# 주의할 점

75배 수치는 특정 문제, 하드웨어, 반복당 시간 비교다. 전체 데이터 준비, 통신, 수렴까지 포함한 종단 성능과 해의 허용 오차를 함께 확인해야 한다. 1차 방법은 매우 큰 문제에서 실용적인 근사해를 빠르게 얻는 대신 문제 조건과 정확도 요구에 민감할 수 있다.

# 출처

- [PyTorch Korea 번역 글](https://pytorch.kr/blog/2026/how-linkedin-uses-pytorch-extreme-scale-optimization/)
- [DuaLip-GPU 기술 보고서](https://arxiv.org/abs/2603.04621)
- [LinkedIn DuaLip 코드](https://github.com/linkedin/DuaLip)

