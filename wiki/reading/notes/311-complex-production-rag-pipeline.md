---
type: Study Note
title: "복합 RAG 파이프라인: 검색·계획·재계획·평가를 연결하는 실습"
description: "LangChain, LangGraph와 RAGAS로 다중 retriever, hallucination 검사와 plan-execute loop를 구성한 단계별 예제"
resource: "https://github.com/FareedKhan-dev/complex-RAG-guide?source=post_page-----36a66d663c5c---------------------------------------"
notion: "https://app.notion.com/p/9171a73cf20b82e9a3048161f2cf665f"
tags: [reading, rag, langgraph, evaluation]
timestamp: 2026-07-24
status: summarized
---

# 전체 흐름

단순한 `retrieve → generate`를 넘어 데이터 정리, 여러 검색 표현, 계획·재계획과 답변 평가를 묶은 RAG 실습 저장소다. LangChain으로 document와 retriever를 구성하고 LangGraph로 상태 전이를 연결하며 RAGAS로 최종 답변의 관련성과 근거 충실도를 평가한다.

질문의 고유명사를 placeholder로 바꾸는 anonymization부터 시작한다. Planner가 상위 계획을 만들고 원래 이름을 복원한 뒤 구체적인 task로 나눈다. Task handler는 인용문, 일반 chunk, chapter summary 검색 또는 직접 답변 중 하나를 고른다. 검색 결과가 들어올 때마다 replanner가 남은 계획을 수정하고, 충분한 근거가 모이면 최종 답변을 만든다.

# 데이터와 검색 설계

예제는 한 소설 PDF를 chapter, 50자 이상의 quote, 1,000자·200자 overlap의 일반 chunk로 각각 분해한다. 문자를 정리하고 chapter summary도 만들어 세 종류의 FAISS index를 구성한다. 질문의 성격에 따라 서로 다른 granularity를 검색한다는 점이 핵심이다.

# 실무에서 조심할 점

예제 저장소에는 저작권이 있는 소설 PDF가 포함돼 있어 데이터 파일을 재배포하거나 업무 corpus로 재사용하면 안 된다. 코드 라이선스는 Apache-2.0이지만 포함 데이터의 권리까지 해결하는 것은 아니다.

Anonymization이 항상 hallucination을 줄인다고 단정할 수도 없다. 중요한 entity 의미를 잃거나 de-anonymization 오류가 생길 수 있다. RAGAS와 LLM judge 역시 독립적인 사실 검증이 아니므로 retrieval recall, citation correctness, latency와 비용을 고정된 평가 세트에서 함께 측정해야 한다. 저장소는 세 개 commit의 교육용 구현이므로 production-ready라는 제목보다 학습용 reference로 보는 것이 안전하다.

# 출처

- [Complex RAG Guide 저장소](https://github.com/FareedKhan-dev/complex-RAG-guide)
