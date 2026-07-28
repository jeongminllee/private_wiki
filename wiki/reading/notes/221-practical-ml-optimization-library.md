---
type: Reference
title: "Practical ML: PyTorch 모델 압축과 성능 최적화 실습 모음"
description: "profiling, kernel fusion, pruning, quantization, distillation과 low-rank factorization을 코드로 다루는 블로그"
resource: https://arikpoz.github.io/
notion: https://app.notion.com/p/ac41a73cf20b83d8a59b819ac0ea6632
tags: [reading, pytorch, model-optimization, ml-engineering]
timestamp: 2026-07-24
status: summarized
---

# 자료의 성격

Practical ML은 Arik Poznanski가 machine learning과 software engineering의 접점을 실습 중심으로 정리한 블로그다. 2025년 글들은 neural network를 더 작고 빠르게 만드는 과정을 하나의 학습 경로로 묶는다.

# 추천 읽기 순서

1. 전체 최적화 기법 개요로 병목의 종류를 구분한다.
2. pruning, quantization, knowledge distillation, low-rank factorization을 각각 실습한다.
3. graph·kernel fusion으로 memory access와 kernel launch overhead를 이해한다.
4. NVIDIA Nsight Systems로 실제 training trace를 보고 CPU-GPU synchronization과 data transfer 병목을 제거한다.

# 건질 수 있는 원칙

최적화는 기법 이름부터 고르는 일이 아니라 profiler로 병목을 확인한 뒤 목표 metric에 맞춰 적용하는 일이다. 글의 사례는 3.2배 training 가속, quantization으로 75% 저장 공간 절감, pruning으로 5.5배 inference 가속 등을 보고하지만 특정 model·hardware의 실험값이다. 자신의 환경에서는 latency, throughput, memory와 accuracy를 같은 benchmark로 다시 측정해야 한다.

# 출처

- [Practical ML](https://arikpoz.github.io/)

