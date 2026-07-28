---
type: Reference
title: "Kanana LLM의 Two-stage Pre-training"
description: "제한된 compute에서 데이터 품질과 단계별 학습으로 한국어·영어 base model을 만든 과정"
resource: https://tech.kakao.com/posts/661
notion: https://app.notion.com/p/d211a73cf20b82b5ab4c81a3c7b26b15
tags: [reading, llm, pretraining, kanana]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

카카오가 Kanana Essence와 Nano base model을 학습한 데이터·학습 전략을 설명한다. 구조의 참신함보다 제한된 compute budget에서 corpus 품질과 혼합 비율, scaling law와 단계별 학습을 조정한 과정에 초점이 있다.

# 데이터 전략

웹, code, 다국어·한국어와 수학 등 여러 domain을 수집하고 중복, 품질과 개인정보를 전처리한다. 공개 Wikipedia 자료에서 수식이 손실되는 문제를 발견해 한국어·영어 자료를 다시 수집한 사례처럼, token 수보다 원문 보존과 domain coverage가 중요하다. 평가에서 약한 수치 계산 영역은 Common Crawl에서 수학 자료를 추가 수집해 보강한다.

# 학습 전략

- Kanana Essence는 총 3T token을 `2.7T + 0.3T` 두 단계로 학습했다.
- Llama 계열과 유사한 GQA·RoPE 구조와 8K context를 사용했다.
- scaling law로 learning rate와 batch size를 정하고 multi-step learning-rate scheduler를 선택했다.
- 초경량 Kanana Nano는 먼저 from-scratch baseline을 만들고 pruning·distillation의 비교 기준으로 삼았다.

# 읽을 때 주의

영어 성능은 비슷하고 한국어는 우수하다는 평가는 공개된 특정 benchmark와 shot 설정의 자체 보고다. 데이터 구성, contamination, 실제 서비스 latency와 post-training 결과를 함께 봐야 한다. Base model의 지식과 instruct model의 사용자 지시 수행 능력도 구분한다.

# 출처

- [카카오 기술 블로그 원문](https://tech.kakao.com/posts/661)
- [이어지는 Post-training 글](https://tech.kakao.com/posts/662)
- [Notion 원본 항목](https://app.notion.com/p/d211a73cf20b82b5ab4c81a3c7b26b15)
