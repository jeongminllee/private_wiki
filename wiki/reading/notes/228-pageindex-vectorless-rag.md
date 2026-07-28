---
type: Reference
title: "PageIndex: 문서 구조를 따라 탐색하는 Vectorless RAG"
description: "문서를 계층형 tree index로 만들고 LLM이 목차처럼 탐색해 관련 section을 찾는 reasoning-based retrieval"
resource: https://discuss.pytorch.kr/t/pageindex-db-llm-rag/9579
notion: https://app.notion.com/p/1601a73cf20b83acb8bb017e8a0a2aa3
tags: [reading, rag, information-retrieval, long-documents]
timestamp: 2026-07-24
status: summarized
---

# 접근 방식

PageIndex는 고정 크기 chunk와 embedding similarity 대신 문서의 section·subsection을 계층형 tree로 만든다. 질문이 들어오면 LLM이 목차를 읽듯 node를 선택하고 아래로 내려가 필요한 원문 구간을 찾는다.

# 장점

- section 경계와 상하위 문맥을 보존한다.
- 어떤 node를 거쳤는지 retrieval path를 설명하기 쉽다.
- 금융 보고서, 법률 문서와 논문처럼 구조가 명확한 긴 문서에 잘 맞는다.
- vector DB와 embedding model 운영이 필요 없다.

# 비용과 한계

vector search의 빠른 근사 검색을 LLM 판단으로 바꾸므로 index 생성과 query당 model call 비용이 커질 수 있다. 목차가 불명확한 문서, 여러 문서에 흩어진 표현 변형과 exact keyword 검색은 hybrid retrieval이 더 유리할 수 있다. 프로젝트는 FinanceBench 98.7%를 보고하지만 dataset 구성, answer grading과 비교 baseline을 확인한 뒤 해석해야 한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/pageindex-db-llm-rag/9579)
- [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex)

