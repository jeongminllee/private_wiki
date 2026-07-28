---
type: Reference
title: "Sebastian Raschka의 LLM Architecture Gallery 공식 참조법"
description: "Architecture figure, fact sheet와 source link를 model 비교표로 사용하는 공식 gallery 안내"
resource: https://sebastianraschka.com/llm-architecture-gallery
notion: https://app.notion.com/p/f8b1a73cf20b8300b05601950b28dc82
tags: [reading, llm-architecture, reference, visualization]
timestamp: 2026-07-24
status: summarized
---

# 무엇이 들어 있나

LLM Architecture Gallery는 Sebastian Raschka의 architecture 비교 글에서 model figure와 fact sheet를 모은 공식 reference다. GPT-2부터 dense, sparse MoE와 hybrid open-weight model을 같은 형식으로 살펴볼 수 있다.

각 entry에는 다음 정보가 연결된다.

- total·active parameter와 context length
- decoder type과 attention mechanism
- layer mix, KV-cache 추정과 핵심 설계
- release date와 license
- 원 분석 글, `config.json`, technical report
- 다른 model과 field 단위 비교

# 활용 순서

1. 관심 model 두 개를 compare 기능으로 고른다.
2. Total size와 active parameter를 구분한다.
3. Attention 방식과 layer 비율로 KV-cache·long-context 가설을 세운다.
4. Config와 technical report에서 정확한 dimension·routing을 확인한다.
5. Serving stack에서 memory와 throughput을 실측한다.

예를 들어 DeepSeek R1은 V3와 같은 671B/37B MoE·MLA architecture를 쓰고 주된 변화가 reasoning-oriented training recipe에 있다. 이 비교는 성능 향상을 architecture 변화로 잘못 귀속하는 일을 줄여준다.

# 갱신과 재사용

Source metadata는 [GitHub 저장소](https://github.com/rasbt/llm-architecture-gallery)에서 관리된다. Gallery 수치는 유용한 출발점이지만 model revision과 저자의 해석이 섞일 수 있으므로 공식 model card와 함께 인용해야 한다.

# 관련 자료

- [GeekNews의 구조 흐름 요약](271-llm-architecture-gallery-geeknews.md)
- [PyTorchKR 한국어 안내](272-llm-architecture-gallery-pytorchkr.md)
- [공식 gallery](https://sebastianraschka.com/llm-architecture-gallery/)

