---
type: Reference
title: "LLM 엔지니어링 도구 지도"
description: "훈련, 미세 조정, RAG, 평가, 서빙 단계별로 도구를 선택하는 기준"
resource: https://m.bikorea.net/news/articleView.html?idxno=44938
notion: https://app.notion.com/p/37d1a73cf20b82e499f701d484ed7d29
tags: [reading, llm-engineering, rag, serving, evaluation]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

LLM 개발은 하나의 프레임워크로 끝나지 않는다. 데이터와 훈련, 미세 조정, 응용 조립, 평가, 배포가 서로 다른 문제이므로 단계별 도구를 목적에 맞게 조합해야 한다.

# 단계별 지도

| 단계 | 대표 선택지 | 먼저 물을 질문 |
| --- | --- | --- |
| 모델 활용·훈련 | PyTorch, Hugging Face Transformers | 새 모델 훈련이 정말 필요한가 |
| 분산 훈련 | FSDP, DeepSpeed | 메모리와 통신 병목은 어디인가 |
| 효율적 미세 조정 | PEFT, LoRA, QLoRA | 전체 가중치를 바꿀 이유가 있는가 |
| RAG·에이전트 | LlamaIndex, LangChain/LangGraph | 검색과 실행 흐름을 어떻게 평가할 것인가 |
| 평가 | 과업별 데이터셋, LLM judge, 사람 평가 | 실패를 재현할 테스트셋이 있는가 |
| 고성능 서빙 | vLLM, TensorRT-LLM | 처리량, 지연 시간, 하드웨어 제약은 무엇인가 |
| 로컬·엣지 실행 | llama.cpp와 GGUF | 품질 손실과 메모리 예산을 감당할 수 있는가 |

# 도구보다 중요한 것

새 도구를 모두 따라가는 것보다 프로젝트의 제약을 먼저 명시해야 한다. 한국어 품질, 데이터 보안, 응답 지연, GPU 예산, 평가 가능성을 기준으로 작은 실험을 하고 교체 비용을 낮추는 편이 지속 가능하다.

# 주의

원문은 생태계 지도를 빠르게 소개하는 기사이므로 일부 명칭과 설명이 엄밀하지 않을 수 있다. 실제 도입 시에는 각 프로젝트의 공식 문서, 라이선스, 최근 릴리스를 다시 확인해야 한다.

# 관련 문서

- [로컬 RAG 구축](125-building-a-local-rag.md)
- [RAG를 바닥부터 이해하기](16-rag-from-scratch.md)
- [AI 개발자 취업 준비](128-ai-developer-job-preparation.md)

# 출처

- [BI KOREA 기사](https://m.bikorea.net/news/articleView.html?idxno=44938)

