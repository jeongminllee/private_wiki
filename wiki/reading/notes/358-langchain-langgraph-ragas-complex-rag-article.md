---
type: Study Note
title: "LangChain·LangGraph·RAGAS 복합 RAG 원문 해설"
description: "logical chunking, 다중 retriever, plan-execute-replan graph와 RAG evaluation을 단계별로 엮은 장문 tutorial"
resource: "https://levelup.gitconnected.com/building-a-complex-production-ready-rag-system-with-langchain-langgraph-and-ragas-36a66d663c5c?gi=07b64e53c7b5"
notion: "https://app.notion.com/p/1491a73cf20b83fabd3d0128cb2ed0ca"
tags: [reading, rag, langchain, langgraph, ragas]
timestamp: 2026-07-24
status: summarized
---

# Pipeline

글은 먼저 text를 정리하고 logical·fixed chunking을 비교한다. 질문의 entity를 placeholder로 anonymize한 뒤 planner가 계획을 만들고 원래 entity를 복원해 task로 나눈다. Handler는 quote, 일반 chunk, chapter summary retriever 또는 direct answer 중 하나를 선택한다.

각 task 뒤 replanner가 지금까지의 evidence와 남은 계획을 갱신한다. 충분한 context가 모이면 answer를 만들고 RAGAS와 custom metric으로 relevance와 faithfulness를 평가한다. LangChain은 document·retriever, LangGraph는 state transition, RAGAS는 evaluation을 맡는다.

# 실무적 판단

여러 agent와 index는 단순 RAG보다 latency, 비용과 failure point를 늘린다. 먼저 retrieval miss 유형을 측정하고 필요한 granularity만 추가한다. Anonymization이 중요한 의미를 제거하는지, de-anonymization이 틀리는지 별도 test한다. LLM judge는 citation correctness와 ground truth evaluation을 대체하지 않는다.

제목의 `production-ready`와 달리 companion repository는 작은 교육용 구현이다. 포함된 소설 PDF의 저작권과 code license를 구분해야 한다.

# 관련 문서

- [같은 글의 companion repository 정리](311-complex-production-rag-pipeline.md)

# 출처

- [원문](https://levelup.gitconnected.com/building-a-complex-production-ready-rag-system-with-langchain-langgraph-and-ragas-36a66d663c5c)
- [Complex RAG Guide](https://github.com/FareedKhan-dev/complex-RAG-guide)
