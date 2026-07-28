---
type: Reference
title: "로컬 RAG 구축 구성요소와 평가"
description: "vector DB부터 parser·reranker·LLM까지 외부 API를 로컬 구성으로 바꾸고 비교한 사례"
resource: https://news.hada.io/topic?id=24712
notion: https://app.notion.com/p/1211a73cf20b83f0972781d175730909
tags: [reading, rag, local-ai, retrieval]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

완전한 local RAG는 LLM 하나만 내려받는 일이 아니다. vector database, embedding, reranker, document parser와 generation model 전부에서 외부 전송 경로를 제거하고, 언어와 질의 유형에 맞는 retrieval 품질을 평가해야 한다.

# 예시 stack

- Vector DB: PostgreSQL + pgvector. 기존 운영 DB를 재사용하며 수십만 문서 규모까지 먼저 검증한다.
- Embedding: 영어 중심 `all-MiniLM-L6-v2`, 다국어가 필요하면 `bge-m3` 등으로 비교한다.
- Reranker: sentence-transformers cross-encoder 또는 다국어 모델을 사용한다.
- Parser: Docling과 `docling-serve`로 PDF·문서를 처리한다.
- LLM: GPT-OSS 20B를 llama.cpp server로 별도 운영한 사례다.

# 글의 실험 결과

약 2천 문서와 작은 질문셋에서 cloud 조합은 9.45, local LLM만 바꾼 조합은 작성자 평가 9.18, 기본 local English 모델 조합은 7.10, 다국어 조합은 8.63을 받았다. point query는 잘했지만 여러 문서의 정보를 모으는 aggregation, 모호한 질문과 비영어 질의에서 약했다.

# 비판적으로 볼 점

질문셋이 작고 저자가 답을 잘 아는 corpus이며 일부 점수는 직접 매긴 비과학적 실험이다. 제품 선택 근거로 쓰기보다 `retrieval recall`, citation faithfulness, latency, memory, ingestion 오류와 언어별 실패를 자체 데이터로 측정하는 출발점으로 사용한다.

# 출처

- [원문](https://blog.yakkomajuri.com/blog/local-rag)
- [GeekNews 한국어 정리와 토론](https://news.hada.io/topic?id=24712)
- [Notion 원본 항목](https://app.notion.com/p/1211a73cf20b83f0972781d175730909)
