---
type: Reference
title: "로컬 RAG의 구성요소와 현실적인 평가 방법"
description: "vector DB, embedding, reranker, parser와 LLM을 모두 self-host하고 cloud 조합과 비교한 구축기"
resource: https://blog.yakkomajuri.com/blog/local-rag
notion: https://app.notion.com/p/5b41a73cf20b8398948601a2d698dfd2
tags: [reading, rag, local-llm, privacy]
timestamp: 2026-07-24
status: summarized
---

# 로컬화해야 하는 구성요소

RAG를 local로 만든다는 것은 LLM 하나를 local model로 바꾸는 일이 아니다. vector database, embedding model, reranker, document parser와 LLM 각각에서 외부 API 호출을 제거해야 한다.

글의 Skald 구성은 PostgreSQL+pgvector, Sentence Transformers embedding, cross-encoder reranker, Docling parser와 llama.cpp로 실행한 GPT-OSS 20B를 사용한다. 다국어에는 BGE-M3와 `bge-reranker-v2-m3`도 시험했다.

# 구축과 평가

전체 service 묶음은 약 8분 만에 배포했고 LLM server만 별도로 실행했다. PostHog 문서를 가져온 뒤 질문과 기대 답변 dataset을 만들고, 검색 top K를 100, reranking top K를 50으로 높여 여러 문서의 정보를 합쳐야 하는 질의를 평가했다.

비공식 소규모 평가에서 Voyage embedding·reranker와 Claude 조합은 LLM judge 평균 9.45, 같은 검색 계층과 local GPT-OSS 20B 조합은 작성자의 수동 평가에서 9.18을 받았다. judge와 평가자가 다르므로 두 숫자는 엄밀한 직접 비교가 아니다.

# 적용할 때 볼 것

privacy 요구사항과 함께 parser의 표 처리, 한국어 검색 recall, 긴 답변 latency, GPU memory, backup과 monitoring 비용을 측정해야 한다. 완전 local의 품질은 특정 model보다 각 retrieval 단계의 평가 dataset과 trace를 갖추는 데 더 크게 좌우된다.

# 출처

- [So you wanna build a local RAG?](https://blog.yakkomajuri.com/blog/local-rag)

