---
type: Paper Note
title: HugRAG
description: 계층형 지식 그래프와 인과 게이트로 Graph RAG의 recall과 precision 문제를 함께 다루는 논문 리뷰
resource: https://arxiv.org/abs/2602.05143
notion: https://app.notion.com/p/3941a73cf20b81339c67fb4ae131bdb9
tags: [reading, paper, rag, knowledge-graph, causal-reasoning]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

HugRAG는 Graph RAG가 지역 커뮤니티 안에 갇혀 멀리 있는 근거를 놓치는 문제와, 가까이 있지만 인과적으로 무관한 노드를 가져오는 문제를 함께 다룬다. 계층형 그래프를 만들고 모듈 사이에 인과 게이트를 두어 검색 범위와 정밀도를 조절한다.

# 문제

- 그래프의 모듈성이 강하면 관련 증거가 다른 커뮤니티에 있어도 제한된 hop 검색으로 도달하지 못한다.
- 단순한 유사도나 이웃 확장은 상관관계를 인과관계로 오인해 불필요한 근거를 섞을 수 있다.

# 방법

- 오프라인 단계에서 기본 지식 그래프를 만들고 Leiden partition으로 계층적 모듈을 구성한다.
- LLM이 모듈 사이의 인과 관련성을 평가해 계층을 가로지르는 게이트를 만든다.
- 온라인 검색은 여러 수준에서 seed를 찾고, 우선순위 확장 중 인과 게이트를 이용해 멀리 있는 관련 모듈로 이동한다.
- 검색된 후보에서 인과 경로를 다시 골라 표면적 연관만 있는 노드를 제거하고, 남은 근거로 답변을 생성한다.

# 핵심 결과

논문과 영상은 여러 QA 데이터셋에서 경쟁 Graph RAG보다 좋은 성능과 근거 품질을 보고한다. ablation에서는 계층 구조, 인과 게이트, 경로 정제가 recall과 precision의 균형에 각각 기여한다고 설명한다.

# 내가 어떻게 써먹을 수 있는가

wiki의 cross-link 검색이 같은 폴더나 가까운 문서에만 머무를 때 상위 주제와 원인·결과 관계를 이용해 다른 영역으로 확장하는 방식으로 응용할 수 있다. 다만 처음부터 전체 인과 그래프를 만들기보다 질문 유형이 다중 hop을 요구하는지부터 측정하는 편이 낫다.

# 주의할 점

인과 게이트는 관측 데이터로 인과를 발견하는 전통적 인과 추론이라기보다 LLM의 판단으로 관계를 분류하는 방식이다. 게이트의 오류, 구축 비용과 도메인 이동 시 성능을 독립적으로 검증해야 한다.

# 출처

- [arXiv 논문](https://arxiv.org/abs/2602.05143)
- [DSBA Paper Review 영상](https://www.youtube.com/watch?v=AUiyrm2R_iA)
- [Notion 원본 항목](https://app.notion.com/p/3941a73cf20b81339c67fb4ae131bdb9)
