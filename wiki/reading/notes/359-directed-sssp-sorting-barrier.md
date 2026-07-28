---
type: Paper Note
title: "Directed SSSP에서 Dijkstra의 sorting barrier 깨기"
description: "음이 아닌 실수 가중치 directed graph의 single-source shortest paths를 O(m log^(2/3) n)에 푸는 STOC 2025 알고리즘"
resource: "https://arxiv.org/abs/2504.17033v2"
notion: "https://app.notion.com/p/7fe1a73cf20b8343b9f281578ac6b3e2"
tags: [reading, paper, algorithm, graph, shortest-path]
timestamp: 2026-07-24
status: summarized
---

# 결과

Dijkstra와 고급 heap은 directed graph의 SSSP를 `O(m + n log n)`에 푼다. 이 논문은 comparison-addition model에서 음이 아닌 실수 edge weight를 가진 directed graph의 거리만 `O(m log^(2/3) n)`에 계산하는 deterministic algorithm을 제시한다. Sparse graph에서 처음으로 Dijkstra의 bound를 asymptotically 개선했다.

# 핵심 아이디어

Dijkstra가 매번 최소 거리 vertex를 뽑으며 전체 distance ordering을 만드는 비용을 피한다. 대신 아직 완료되지 않은 frontier를 정렬하지 않은 채 bounded multi-source shortest path(BMSSP) subproblem으로 묶는다.

Bellman-Ford식 relaxation으로 큰 shortest-path subtree를 대표하는 pivot을 찾고, boundary 아래에서 진전 가능한 vertex batch를 처리한다. Vertex set을 재귀적으로 partition하며 level별 data structure가 작은 거리 범위를 반환한다. 완전한 순서가 아니라 거리만 요구한다는 조건이 sorting barrier를 피하는 핵심이다.

# 한계와 의미

음수 weight에는 적용되지 않고 comparison-addition model의 이론 결과다. Constant-degree 변환과 복잡한 recursive structure의 상수 비용 때문에 일반 workload에서 binary-heap Dijkstra보다 바로 빠르다는 뜻은 아니다. 구현 난도, graph density와 cache behavior를 포함한 benchmark가 별도로 필요하다.

# 출처

- [arXiv v2](https://arxiv.org/abs/2504.17033v2)
- [STOC 2025 공개본](https://doi.org/10.1145/3717823.3718179)
