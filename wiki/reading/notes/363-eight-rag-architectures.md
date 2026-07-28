---
type: Reference
title: "RAG 아키텍처 8종을 실패 유형별로 선택하기"
description: "Naive, multimodal, HyDE, corrective, graph, hybrid, adaptive, agentic RAG의 차이와 선택 기준"
resource: "https://x.com/akshay_pachaar/status/2004892550335967412?s=20"
notion: "https://app.notion.com/p/23e1a73cf20b83e4a65c813b53ade649"
tags: [reading, rag, retrieval, llm, architecture]
timestamp: 2026-07-24
status: summarized
---

# 여덟 가지 형태

원문은 RAG를 다음과 같이 분류한다.

- `Naive RAG`: 질문 embedding과 vector similarity로 문서를 찾는다.
- `Multimodal RAG`: text뿐 아니라 image, table, audio 같은 자료를 함께 검색한다.
- `HyDE`: 가상의 답변을 먼저 만든 뒤 그 embedding으로 관련 문서를 찾는다.
- `Corrective RAG`: 검색 결과의 관련성을 검사하고 부족하면 query 수정이나 외부 검색을 수행한다.
- `Graph RAG`: entity와 relation을 이용해 여러 문서에 걸친 연결을 탐색한다.
- `Hybrid RAG`: 서로 다른 retrieval 신호를 조합한다.
- `Adaptive RAG`: 질문 난도에 따라 단순 검색, query 분해, 다단계 검색을 고른다.
- `Agentic RAG`: agent가 계획, 도구 호출, memory와 반복 검색을 조정한다.

# 분류를 그대로 믿으면 안 되는 이유

이 명칭들은 표준화된 상호 배타적 계층이 아니다. Hybrid는 흔히 sparse와 dense retrieval 결합을 뜻하지만 원문은 dense와 graph 조합으로 설명한다. Corrective, adaptive와 agentic RAG도 실제 system에서는 겹친다. Graph RAG가 모든 문서를 graph로 바꿔야 하는 것도 아니며, corrective loop가 사실성을 자동 보장하지도 않는다.

# 선택 기준

Architecture 이름보다 현재 실패를 먼저 측정한다. 용어 불일치면 hybrid retrieval, 가상의 표현과 실제 문서 표현의 간극이면 HyDE, 관계 추론이면 graph, 질문 유형이 다양하면 adaptive routing, 여러 source와 tool을 순차적으로 써야 하면 agentic orchestration이 후보가 된다.

각 후보는 동일 evaluation set에서 retrieval recall, answer faithfulness, latency, token·index 비용과 운영 복잡도를 함께 비교해야 한다. 단순 RAG가 충분한데 agent를 넣으면 비용과 failure mode만 늘 수 있다.

# 관련 문서

- [LangChain·LangGraph·RAGAS 기반 복합 RAG](358-langchain-langgraph-ragas-complex-rag-article.md)

# 출처

- [Akshay Pachaar의 X 게시물](https://x.com/akshay_pachaar/status/2004892550335967412?s=20)
- [공개 X mirror metadata](https://api.vxtwitter.com/akshay_pachaar/status/2004892550335967412)
