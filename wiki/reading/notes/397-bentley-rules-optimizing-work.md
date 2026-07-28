---
type: Study Note
title: "Bentley Rules로 program work 줄이기"
description: "Packing, precomputation, loop transformation, short-circuit와 fast path로 실행 연산량을 줄이는 MIT 6.172 강의"
resource: "https://www.youtube.com/watch?v=H-1-X9bkop8"
notion: "https://app.notion.com/p/7811a73cf20b82b2af99815efd7ca101"
tags: [reading, video, performance, optimization, algorithm]
timestamp: 2026-07-24
status: summarized
---

# Work의 의미

강의에서 program의 `work`는 특정 input에 대해 실행한 operation의 총량이다. 더 나은 algorithm으로 asymptotic complexity를 낮추는 것이 가장 큰 개선이지만, 같은 algorithm 안에서도 불필요한 작업을 줄일 수 있다. 다만 work 감소가 cache, vectorization, branch prediction과 instruction parallelism 때문에 실제 wall-clock 감소와 항상 같지는 않으므로 측정이 필요하다.

# Bentley Rules

- `Packing and encoding`: 더 조밀한 representation으로 여러 value를 한 operation에 처리하고 memory traffic을 줄인다.
- `Precomputation`: runtime에 반복할 계산을 compile time이나 table 생성 단계로 옮긴다.
- `Compile-time initialization`: 변하지 않는 값을 실행 때 만들지 않는다.
- `Loop unrolling`: loop control overhead를 줄이고 compiler optimization 기회를 늘린다.
- `Short-circuiting`: 결과가 이미 결정됐으면 나머지 계산을 건너뛴다.
- `Common-case fast path`: 빈번하고 단순한 case를 먼저 빠르게 처리하고 복잡한 fallback을 분리한다.
- `Combining tests`: 여러 pass나 조건 검사를 한 번의 traversal로 합친다.

# 적용 순서

먼저 profiler와 benchmark로 hotspot과 input distribution을 확인한다. Correctness test를 고정한 뒤 한 규칙씩 적용하고 instruction count, cache miss와 elapsed time을 전후 측정한다. Readability를 크게 해치는 micro-optimization은 실제 gain이 작으면 되돌린다.

# 출처

- [YouTube 강의](https://www.youtube.com/watch?v=H-1-X9bkop8)
- [MIT OpenCourseWare 강의와 transcript](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/resources/lecture-2-bentley-rules-for-optimizing-work/)
