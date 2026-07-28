---
type: Study Note
title: "2026 LLM 실무 종합 4시간 강의"
description: "sLLM 파인튜닝, 사내 문서 처리, GraphRAG를 세 부분으로 묶은 실무 강의의 목차 기반 정리"
resource: https://www.youtube.com/watch?v=XOhDCjg3LsI
notion: https://app.notion.com/p/3611a73cf20b81b69749c92eb0ee0d4d
tags: [reading, video, llm, fine-tuning, rag]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

메타코드M이 공개한 약 4시간 분량의 강의로, 로컬 sLLM 파인튜닝부터 사내 비정형 문서 처리와 GraphRAG까지 한 흐름으로 다룬다. 아래 내용은 영상 설명과 공개된 챕터를 기준으로 정리했다.

# 1부: 로컬 sLLM 파인튜닝

- sLLM과 LLM의 차이, 개발 환경, 데이터셋 구성
- 학습 파라미터와 QLoRA
- GPU 메모리 제약에 맞춘 설정
- 학습 결과의 테스트와 추론

# 2부: 사내 데이터와 sLLM

- OCR과 PDF 같은 비정형 자료에서 정보 추출
- 임베딩과 벡터 데이터베이스
- 사내 데이터에 맞춘 소형 모델과 자동화
- 챗봇 구축 이후의 기업 환경 운영

# 3부: 환각과 GraphRAG

- 환각이 생기는 이유와 일반 RAG의 한계
- 지식 그래프의 엔터티와 관계
- 그래프 탐색을 활용한 사내 GraphRAG
- 도구를 사용하는 에이전트로의 확장

# 활용 순서

먼저 검색·평가 가능한 RAG 기준선을 만들고, 모델의 행동이나 전문 용어 적응이 부족할 때 파인튜닝을 검토하는 편이 비용을 통제하기 쉽다. GraphRAG 역시 그래프 구축 자체보다 엔터티 추출 정확도와 근거 인용 평가가 먼저다.

# 확인 범위

전체 자막을 대조한 전문 요약이 아니라 공개 목차 기반 개요다. 설명란에는 교육 과정 홍보도 포함되어 있으므로 기술 내용과 판매 주장은 분리해서 볼 필요가 있다.

# 출처

- [2026 LLM 실무 4시간 풀강의](https://www.youtube.com/watch?v=XOhDCjg3LsI)

