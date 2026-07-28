---
type: Paper Note
title: "Adaptive Chunking for RAG"
description: "문서 특성을 측정해 고정 크기, 페이지, LLM 기반 분할 중 적합한 청킹 전략을 문서별로 고르는 연구"
resource: https://discuss.pytorch.kr/t/adaptive-chunking-rag/10478
notion: https://app.notion.com/p/3741a73cf20b81359f43f67140726e37
tags: [paper, rag, chunking, document-ai]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

모든 문서를 같은 길이로 자르는 대신 문서마다 여러 청킹 후보를 만들고, 참조 보존·블록 무결성·응집도·문맥 일관성·크기 적합성을 평가해 전략을 고르는 방법이다.

# 방법

연구는 재귀적 길이 기반 분할, 페이지 기반 분할, LLM이 문서 앞부분에서 구분 정규식을 생성하는 분할을 후보로 둔다. 각 결과는 다섯 지표로 비교한다.

- **References Completeness**: 각 청크가 참조 대상을 충분히 포함하는가
- **Block Integrity**: 표, 목록, 코드와 문단 같은 블록이 불필요하게 갈라지지 않는가
- **Intrachunk Cohesion**: 한 청크 안의 내용이 같은 주제를 다루는가
- **Document Contextual Coherence**: 청크가 전체 문서 맥락과 연결되는가
- **Size Compliance**: 검색과 모델 입력에 적절한 크기인가

재귀 방식은 먼저 나눈 뒤 작은 조각을 다시 합치는 split-then-merge 구조를 쓴다. LLM 방식은 문서 전체를 매번 생성형으로 자르지 않고, 앞부분에서 하나의 separator 정규식을 만든 뒤 결정적으로 적용해 비용과 재현성을 조절한다.

# 결과와 활용

논문 환경에서는 답변 점수가 약 62~64에서 72 수준으로 오르고 성공한 질문 수도 49에서 65로 증가했다고 보고한다. 실무에서는 문서 유형별 고정 규칙을 바로 정하기 전에 소수의 대표 문서에서 후보 전략을 평가하는 선택기로 활용할 수 있다.

# 한계

References Completeness 구현은 영어와 특정 모델에 의존한다. 내재 지표가 높아도 실제 검색·답변 품질이 항상 좋아지는 것은 아니며, 후보를 여러 번 계산하는 비용도 든다. 최종 선택은 자체 질문 세트의 retrieval recall과 answer accuracy로 검증해야 한다.

# 출처

- [Adaptive Chunking 논문](https://arxiv.org/abs/2603.25333)
- [공식 코드 저장소](https://github.com/ekimetrics/adaptive-chunking)
- [저장된 PyTorchKR 해설](https://discuss.pytorch.kr/t/adaptive-chunking-rag/10478)
- [Notion 원본 항목](https://app.notion.com/p/3741a73cf20b81359f43f67140726e37)

