---
type: Reference
title: "Qwen3 Hybrid Thinking: 같은 모델에서 추론을 켜고 끄는 방법"
description: "요청의 난도와 latency 요구에 따라 thinking과 direct answer를 전환하는 Qwen3 제어 방식"
resource: https://devocean.sk.com/blog/techBoardDetail.do?ID=167448&boardType=techBlog
notion: https://app.notion.com/p/c0f1a73cf20b8218ac9001af11820ad8
tags: [reading, llm, reasoning, qwen]
timestamp: 2026-07-24
status: summarized
---

# 핵심 아이디어

Qwen3의 Hybrid Thinking mode는 어려운 문제에는 test-time reasoning을 사용하고 빠른 응답이 중요한 요청에는 이를 생략하도록 같은 model의 동작을 전환한다. 별도 reasoning model과 일반 model을 운영하는 대신 품질·latency·token 비용을 요청별로 조절할 수 있다.

# 제어 방법

대화에서는 `/think`와 `/no_think` 지시로 전환하고, API나 library에서는 `enable_thinking` parameter를 사용한다. reasoning이 필요한 수학, planning과 검증 작업에는 thinking을 켜고, 간단한 분류·추출·형식 변환에는 끄는 식으로 routing할 수 있다.

# 모델군과 해석

글은 Qwen3가 MoE와 dense 크기로 공개됐고 큰 model에서 작은 model로 strong-to-weak distillation을 사용했다고 설명한다. 다만 공개 당시 technical report가 없어 pruning 등 세부 학습 방식에 대한 일부 내용은 작성자의 추정이다. 확인된 발표 내용과 추론을 구분해 읽어야 한다.

# 적용 포인트

운영에서는 사용자가 직접 toggle하게 두기보다 질문 복잡도, 허용 latency와 예산으로 router를 만들고, 어려운 질문에서만 thinking을 허용하는 방식이 유용하다. 정확도뿐 아니라 총 token, 응답 시간, 불필요한 장황함과 reasoning loop 빈도를 함께 측정해야 한다.

# 출처

- [DEVOCEAN 글](https://devocean.sk.com/blog/techBoardDetail.do?ID=167448&boardType=techBlog)

