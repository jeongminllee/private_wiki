---
type: Reference
title: RAG From Scratch
description: 기본 RAG에서 질의 변환, 라우팅, 색인 전략과 적응형 RAG까지 구현하는 장시간 강의 노트
resource: https://www.youtube.com/watch?v=sVcwVQRHIc8
notion: https://app.notion.com/p/3961a73cf20b81378faaf38b7ebc2fab
tags: [reading, video, rag, langchain]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

LangChain 엔지니어 Lance Martin이 약 2시간 33분 동안 RAG의 색인·검색·생성 기본 흐름부터 고급 검색 전략까지 코드로 설명하는 강의다. 동반 GitHub 노트북이 있어 개념을 직접 실행하며 따라가기 좋다.

# 핵심 내용

- 기본 파이프라인은 문서를 분할하고 임베딩해 벡터 저장소에 넣은 뒤, 질문과 가까운 문맥을 검색해 답변 생성에 사용한다.
- 질의 변환에서는 multi-query, RAG Fusion, 질문 분해, step-back prompting, HyDE를 다룬다.
- 라우팅은 질문에 따라 검색 소스나 처리 흐름을 선택하고, query construction은 자연어 질문을 구조화된 필터로 바꾼다.
- multi-representation indexing과 RAPTOR는 원문 조각 외에 요약·계층 표현을 함께 색인한다.
- CRAG와 Adaptive RAG는 검색 결과의 품질을 평가하고 필요에 따라 재검색, 웹 검색, 생성 단계를 조정한다.

# 왜 읽을 만한가

RAG를 벡터 검색 한 번으로 끝내지 않고 질의 해석, 검색 품질 평가, 흐름 제어의 조합으로 이해하게 한다. 어떤 고급 기법이 어떤 실패를 해결하는지 비교하며 배울 수 있다.

# 추천 학습법

1. 기본 RAG 노트북을 작은 한국어 문서로 재현한다.
2. 검색 실패 사례를 모은 뒤 질의 변환 기법 하나만 추가한다.
3. 검색 recall, 근거 정확성, 답변 품질과 지연 시간을 함께 비교한다.
4. 마지막에 LangGraph 기반 적응형 흐름을 붙여 복잡성 증가가 실제 개선으로 이어지는지 본다.

# 주의할 점

강의와 코드가 만들어진 뒤 LangChain API가 바뀌었을 수 있다. 최신 패키지에서 그대로 실행되지 않으면 개념과 구현을 분리해 보고, 버전을 고정한 뒤 수정 내역을 기록해야 한다.

# 출처

- [freeCodeCamp 영상](https://www.youtube.com/watch?v=sVcwVQRHIc8)
- [동반 GitHub 저장소](https://github.com/langchain-ai/rag-from-scratch)
- [Notion 원본 항목](https://app.notion.com/p/3961a73cf20b81378faaf38b7ebc2fab)
