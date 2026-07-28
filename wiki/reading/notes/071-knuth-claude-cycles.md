---
type: Paper Note
title: "Knuth의 Claude's Cycles"
description: "Claude Opus 4.6이 방향 그래프의 홀수 차수 해밀토니안 순환 분해를 탐색하고 사람이 검증·증명한 사례"
resource: https://news.hada.io/topic?id=27183
notion: https://app.notion.com/p/4571a73cf20b82e38d4901e1375cae75
tags: [paper, mathematics, llm-reasoning, human-ai-collaboration]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

Claude가 실패한 탐색을 문서화하며 31번의 실험 끝에 모든 홀수 `m`에 적용되는 구성 프로그램을 발견했고, Filip Stappers의 계산 검증과 Donald Knuth의 수학적 증명이 이를 완성한 인간·AI 협업 사례다.

# 문제

꼭짓점이 `m^3`개인 방향 그래프에서 각 꼭짓점은 세 좌표 중 하나를 1씩 증가시키는 세 간선을 갖는다. 목표는 모든 간선을 길이 `m^3`인 세 개의 방향성 Hamiltonian cycle로 나누는 일반 구성을 찾는 것이다. Knuth는 `m=3`을 풀었고 Stappers는 여러 작은 `m`에서 해를 찾았지만 일반식은 없었다.

# 탐색 과정

Claude는 문제를 각 꼭짓점에서 세 방향을 cycle별로 배정하는 permutation 문제로 바꿨다. 선형·이차 규칙, DFS, 2D와 3D serpentine pattern, Gray code, 특정 hyperplane 수정 등을 시도했지만 실패했다. 이후 `s=(i+j+k) mod m`으로 그래프를 층화하는 fiber decomposition을 도입하고 simulated annealing의 작은 해에서 규칙을 찾았다.

31번째 탐색에서 fiber와 한 좌표의 경계값만으로 방향을 고르는 Python 프로그램을 만들었고 `m=3,5,7,9,11`에서 동작했다. Stappers는 홀수 `m=3`부터 `101`까지 확인했고, Knuth는 이를 C로 단순화한 뒤 각 cycle이 모든 꼭짓점을 정확히 한 번 지난다는 증명을 제시했다.

# 의미와 한계

결과는 모델 단독의 완결된 수학 증명보다 탐색 에이전트, 실행 피드백, 진행 문서와 인간 증명의 결합이다. `plan.md`를 매 실험 직후 갱신하라는 지시가 실패를 누적 가능한 연구 기록으로 만들었다. 짝수 `m`의 일반 구성은 글의 개정 시점에도 미해결이며, 계산 검증은 증명을 대신하지 않는다.

# 출처

- [Donald Knuth 원문 PDF](https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf)
- [GeekNews 한국어 소개와 토론](https://news.hada.io/topic?id=27183)
- [Notion 원본 항목](https://app.notion.com/p/4571a73cf20b82e38d4901e1375cae75)

