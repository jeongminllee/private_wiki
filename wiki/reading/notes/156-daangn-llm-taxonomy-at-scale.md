---
type: Reference
title: "당근의 2조 토큰 LLM 카테고리 분류 운영기"
description: "1,400개에서 10,000개까지 확장하는 택소노미 분류 파이프라인의 정확도·비용·운영 설계"
resource: https://medium.com/daangn/2%EC%A1%B0-%ED%86%A0%ED%81%B0%EC%9D%84-%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC-%EB%B6%84%EB%A5%98%EC%97%90-%EC%93%B0%EB%A9%B4%EC%84%9C-%EC%95%8C%EA%B2%8C%EB%90%9C-%EA%B2%83%EB%93%A4-f619f1db6b7b
notion: https://app.notion.com/p/efe1a73cf20b83cd8d2781af8d67f8e0
tags: [reading, llm, taxonomy, data-pipeline, evaluation]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

당근 Taxonomy 팀이 중고거래와 모임 게시글을 대규모 카테고리 체계에 자동 분류하기 위해 LLM을 운영한 사례다. 택소노미는 검색, 추천, 광고, 분석이 공유하는 공통 언어이므로 모델 정확도뿐 아니라 카테고리 변경과 데이터 적재까지 안정적으로 관리해야 한다.

# 시스템 구성

- Kafka에서 입력을 받고 Dataflow/Apache Beam으로 병렬 추론한다.
- 결과는 BigQuery에 적재해 서비스와 분석에서 사용한다.
- 택소노미 정의를 YAML로 중앙 관리한다.
- Gemini와 GPT 계열 등 여러 LLM과 프롬프트 전략을 교체 가능하게 구성한다.
- 임베딩과 BM25를 결합해 후보 카테고리를 먼저 좁힌다.
- 트리를 단계적으로 탐색하는 two-stage 방식으로 전체 후보를 매번 보는 비용을 줄인다.

# 평가와 최적화

- Ground Truth를 기준으로 LLM-as-a-Judge 평가를 운영한다.
- 프롬프트 캐싱과 이미지 해상도 조절로 토큰·비전 비용을 낮춘다.
- 카테고리와 속성의 일관성, 다국어 분류까지 같은 관리 체계에 넣는다.
- 약 1,400개 3-depth 체계에서 10,000개 6-depth 규모까지 확장 가능한 구조를 지향한다.

# 배울 점

LLM 분류의 핵심은 모델 한 번의 정답률이 아니라 택소노미 버전, 후보 생성, 평가셋, 비용, 재처리를 함께 운영하는 것이다. 계층 분류에서는 전체 라벨을 한 프롬프트에 넣기보다 검색과 트리 탐색으로 문제 공간을 줄이는 편이 합리적이다.

# 관련 문서

- [온톨로지 설계 원칙](12-ontology-design-principles.md)
- [ML 목적함수와 비즈니스 지표](099-ml-objective-and-business-metric.md)

# 출처

- [당근 기술 블로그 원문](https://medium.com/daangn/2%EC%A1%B0-%ED%86%A0%ED%81%B0%EC%9D%84-%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC-%EB%B6%84%EB%A5%98%EC%97%90-%EC%93%B0%EB%A9%B4%EC%84%9C-%EC%95%8C%EA%B2%8C%EB%90%9C-%EA%B2%83%EB%93%A4-f619f1db6b7b)

