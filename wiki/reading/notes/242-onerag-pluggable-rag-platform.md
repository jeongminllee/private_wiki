---
type: Reference
title: "OneRAG: 구성 요소를 설정으로 교체하는 한국어 RAG 플랫폼"
description: "벡터 DB, LLM, reranker와 cache를 바꿔 끼우는 OneRAG의 구조와 도입 전 검증 항목"
resource: https://news.hada.io/topic?id=26538
notion: https://app.notion.com/p/b491a73cf20b8244bb2081f00b465d64
tags: [reading, rag, llm, open-source]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

OneRAG은 RAG(Retrieval-Augmented Generation)의 주요 부품을 코드 수정 대신 설정으로 교체하도록 만든 FastAPI 기반 오픈소스 플랫폼이다. 특정 vendor 조합에 잠기지 않고 여러 retrieval·generation 구성을 비교하려는 팀에 적합하다.

# 지원하는 구성

- vector database: Weaviate, Chroma, Pinecone, Qdrant, pgvector와 MongoDB
- LLM: Gemini, OpenAI, Claude와 OpenRouter
- reranker: Jina, Cohere, Google, OpenAI와 local model
- cache: process memory, Redis와 semantic cache
- 그 밖의 기능: 한국어 처리, GraphRAG, PII masking과 agent workflow

저장소를 clone한 뒤 Docker Compose와 `make quickstart`로 기본 구성을 띄우고, provider와 backend를 설정에서 바꾸는 흐름이다. 라이선스는 MIT다.

# 실제 가치

플러그형 구조의 장점은 “최고의 RAG”를 자동으로 얻는 데 있지 않다. 같은 질문·문서 집합에서 vector DB, embedding, reranker와 model의 비용·latency·정확도를 반복 비교하기 쉬워지는 것이 핵심이다. cloud service에서 local component로 옮기거나 장애 시 provider를 바꾸는 경로도 명시적으로 만들 수 있다.

# 도입 전 확인

구성 요소가 많을수록 조합별 호환성, schema migration과 observability 부담도 늘어난다. 실제 문서로 retrieval recall, citation faithfulness, 한국어 tokenization, cold-start latency와 비용을 측정해야 한다. 설정 한 줄로 provider가 바뀌더라도 결과 품질과 API semantics까지 같아지는 것은 아니므로, 대표 조합을 integration test로 고정하는 것이 중요하다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=26538)

