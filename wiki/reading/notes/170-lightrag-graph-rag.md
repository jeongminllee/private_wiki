---
type: Paper Note
title: "LightRAG: 그래프와 벡터 검색을 결합한 RAG"
description: "엔터티 관계 그래프와 저수준·고수준 이중 검색으로 검색 증강 생성을 구성하는 방법"
resource: https://short.oursophy.com/nb4PEu
resource_aliases: [https://arxiv.org/abs/2410.05779]
notion: https://app.notion.com/p/0c01a73cf20b8310878081d5e400b02d
tags: [reading, paper, rag, knowledge-graph]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

LightRAG는 문서에서 엔터티와 관계를 추출해 그래프를 만들고 벡터 검색과 함께 사용함으로써, 구체적인 사실 질문과 전체 맥락 질문을 모두 다루려는 RAG 구조다.

# 핵심 구조

- 텍스트 청크에서 엔터티와 관계를 추출해 그래프 인덱스를 만든다.
- **Low-level retrieval**은 특정 엔터티와 세부 사실을 찾는다.
- **High-level retrieval**은 여러 문서에 걸친 주제와 관계를 찾는다.
- 새 문서를 전체 재색인 없이 추가하는 incremental update를 지원한다.

# 기대 효과

벡터 유사도만으로는 멀리 떨어진 사실의 관계를 놓치기 쉽다. 그래프 탐색을 함께 쓰면 “누가 무엇과 어떻게 연결되는가”를 명시적으로 따라갈 수 있다. 저자들은 여러 질의에서 기존 RAG 기준선보다 검색 품질과 효율이 개선됐다고 보고한다.

# 적용할 때의 주의

엔터티·관계 추출 오류가 그래프 전체로 전파될 수 있고, 모호한 이름의 병합과 출처 추적이 어렵다. 그래프를 만들었다는 사실만으로 답변이 정확해지는 것은 아니므로 인용 근거, 원문 청크, 검색 평가셋을 함께 유지해야 한다.

# 관련 문서

- [RAG 밑바닥부터 구현하기](16-rag-from-scratch.md)
- [로컬 RAG 구축](125-building-a-local-rag.md)

# 출처

- [LightRAG 논문](https://arxiv.org/abs/2410.05779)
- [LightRAG GitHub](https://github.com/HKUDS/LightRAG)
