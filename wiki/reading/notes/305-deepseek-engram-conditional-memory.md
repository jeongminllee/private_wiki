---
type: Paper Note
title: "DeepSeek Engram: 계산 희소성에 정적 기억 희소성을 더하는 언어 모델"
description: "현대화한 N-gram lookup으로 정적 패턴을 O(1)에 불러오고 신경망의 동적 추론 용량을 보존하는 조건부 메모리 연구"
resource: "https://github.com/deepseek-ai/Engram"
resource_aliases: [https://share.google/6ByyZlyDWn3rPmN1G]
notion: "https://app.notion.com/p/e221a73cf20b83d88eb7812f620c949e"
tags: [reading, paper, llm-architecture, memory]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

MoE가 입력에 따라 일부 신경망 계산만 활성화하는 conditional computation이라면, Engram은 입력 N-gram으로 거대한 정적 메모리 일부를 결정론적으로 조회하는 conditional memory다.

# 방법

현대화한 N-gram embedding을 O(1) lookup으로 가져와 현재 hidden state와 결합한다. 자주 반복되는 철자·구문·지역 패턴을 초기 Transformer layer가 매번 다시 구성하지 않아도 되므로, 동적 신경망 계산을 문맥 추론에 더 쓸 수 있다는 발상이다. 주소가 결정론적이어서 큰 메모리 표를 host memory로 옮기고 필요한 항목만 가져오는 구성도 가능하다고 설명한다.

연구진은 총 parameter와 FLOPs 예산이 고정됐을 때 MoE 계산 용량과 Engram 정적 메모리 사이에 최적 배분점이 생기는 U자형 scaling law를 보고한다. Engram-27B는 같은 parameter·연산량 조건의 MoE 기준선보다 지식, 추론, 코드와 수학 평가에서 개선됐다고 제시한다.

# 해석

이 결과는 “모든 지식을 가중치 계산으로 표현할 필요가 있는가”라는 질문을 던진다. 정적인 국소 패턴은 lookup에 맡기고, 깊은 layer는 조합과 추론에 집중시키는 역할 분담이다. 특히 host memory offload가 실제 지연을 크게 늘리지 않는다면 GPU 메모리와 시스템 RAM을 함께 쓰는 새로운 scaling 축이 된다.

# 한계와 재현

저장소의 `engram_demo_v1.py`는 Attention, MoE와 mHC를 단순화한 데모이며 전체 학습 코드는 아니다. 논문의 성능과 offload 비용은 저자 실험 조건에서 나온 결과이므로 독립 재현이 필요하다. 코드 표시는 Apache-2.0이지만 모델 사용은 각 모델 라이선스를 따로 확인해야 한다.

# 출처

- [DeepSeek Engram 저장소와 논문](https://github.com/deepseek-ai/Engram)
