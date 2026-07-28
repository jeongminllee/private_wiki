---
type: Reference
title: 최신 LLM 구조의 기본기 - GQA
description: Attention과 Multi-Head Attention에서 Grouped-Query Attention으로 이어지는 직관을 설명한 영상 노트
resource: https://www.youtube.com/watch?v=vEKhXxSlclY
notion: https://app.notion.com/p/39f1a73cf20b81878db7eaa73a8824b9
tags: [reading, video, llm, attention]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

임커밋의 9분짜리 영상으로, 기본 Attention의 가중합에서 Multi-Head Attention(MHA), Grouped-Query Attention(GQA)까지 모양과 의도를 이어 설명한다. GQA의 핵심은 Query head 수보다 Key/Value head 수를 줄이고 여러 Query head가 같은 Key/Value head를 공유하는 것이다.

# 핵심 내용

- Attention은 Query와 Key의 내적으로 관련도 점수를 만들고, softmax를 거친 가중치로 Value의 가중합을 계산한다.
- MHA는 벡터를 여러 head로 나누어 서로 다른 관점의 관련도를 동시에 학습한다.
- GQA에서는 Query head를 여러 개 유지하면서 Key/Value head를 더 적게 둔다.
- 예를 들어 Query head 두 개가 하나의 Key/Value head를 공유하면 서로 다른 질의 표현이 같은 정보 관점을 여러 방식으로 살핀다.
- Key/Value head가 줄어 KV cache가 작아지므로 메모리를 아끼면서 MHA에 가까운 성능을 노릴 수 있다.

# 왜 읽을 만한가

GQA를 단순한 최적화 이름으로 외우지 않고 MHA와 Multi-Query Attention 사이의 설계 선택으로 이해하게 해 준다. LLM 추론에서 KV cache가 왜 중요한지도 자연스럽게 연결된다.

# 적용 아이디어

- 모델 명세를 볼 때 attention head 수와 함께 `num_key_value_heads`를 확인한다.
- 긴 컨텍스트 서빙에서는 파라미터 수뿐 아니라 KV cache의 메모리 비용을 계산한다.
- 다음 학습 주제로 MQA와 MLA를 비교해 압축 방식과 성능 손실의 차이를 정리한다.

# 주의할 점

직관 중심 영상이라 GQA의 원 논문 실험, 학습 변환 방식과 실제 모델별 구현 차이는 별도로 확인해야 한다.

# 출처

- [YouTube 영상](https://www.youtube.com/watch?v=vEKhXxSlclY)
- [Notion 원본 항목](https://app.notion.com/p/39f1a73cf20b81878db7eaa73a8824b9)
