---
type: Reference
title: "Gumini 1B·1.5B 한국어-영어 Base LLM"
description: "Qwen2.5에서 층을 상속해 확장한 소형 이중언어 기반 모델의 구조, 라이선스와 한계"
resource: https://huggingface.co/GuminiResearch/Gumini-1.5B-Base
notion: https://app.notion.com/p/45b1a73cf20b82e9beff010fca606767
tags: [reading, llm, korean-language-model, open-model]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Gumini는 한국어와 영어를 대상으로 계속 사전학습한 base model 계열이다. 지시를 따르도록 튜닝한 챗봇 모델이 아니며, 연구·추가 학습용 기반 모델로 보는 것이 맞다.

# 모델 구조

- `Gumini-1.5B-Base`: 약 15.4억 parameter, 16 layers, hidden size 2,048, 16 attention heads와 2 KV heads를 사용한다.
- Qwen2.5-3B의 일부 층을 상속하고 progressive layer growing 방식인 Inheritune을 적용했다고 설명한다.
- 약 31.4억 token을 한국어 80%, 영어 20% 비율로 계속 학습했다.
- `Gumini-1B-Base`는 Qwen2.5-3B의 앞쪽 10개 층을 상속한 약 10.8억 parameter 모델이며 학습량은 약 3.93억 token으로 더 작다.

# 성능을 읽는 법

모델 카드에서 1.5B의 한국어 perplexity가 Qwen2.5-1.5B보다 소폭 낮다고 보고하지만, 이는 제작자가 공개한 특정 평가 결과다. 대화 품질, 사실성, 장문 추론이나 안전성을 직접 보장하지 않는다. 목적에 맞는 downstream benchmark와 실제 corpus로 별도 비교해야 한다.

# 사용 전 주의

Qwen Research License 기반의 비상업 조건을 확인해야 한다. 반복 생성, 오래되거나 틀린 정보, 안전 정렬 부재가 명시되어 있으므로 공개 서비스에 바로 연결하기보다 fine-tuning과 평가, 출력 제한을 먼저 설계한다.

# 출처

- [Gumini-1.5B-Base 모델 카드](https://huggingface.co/GuminiResearch/Gumini-1.5B-Base)
- [Gumini-1B-Base 모델 카드](https://huggingface.co/GuminiResearch/Gumini-1B-Base)
- [Notion 원본 항목](https://app.notion.com/p/45b1a73cf20b82e9beff010fca606767)
