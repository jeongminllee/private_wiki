---
type: Reference
title: "Titans와 MIRAS: Test-time 장기 기억 연구"
description: "긴 문맥을 모두 attention에 넣는 대신 실행 중 neural memory를 갱신하는 Google Research 접근"
resource: https://www.aitimes.kr/news/articleView.html?idxno=37597
notion: https://app.notion.com/p/b771a73cf20b833e8f7c815650032825
tags: [reading, long-context, neural-memory, machine-learning]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Titans는 현재 context에 attention을 쓰면서 과거 정보는 별도의 neural long-term memory에 압축해 저장하는 sequence architecture다. MIRAS는 online optimization, associative memory와 architecture design을 하나의 관점으로 설명하는 이론적 framework다.

# 작동 아이디어

- attention은 정확하지만 sequence 길이에 따른 compute·memory 비용이 크다.
- recurrent state는 효율적이지만 고정된 작은 상태에 정보를 압축해야 한다.
- Titans는 들어오는 정보의 `surprise`를 기준으로 neural memory를 test time에 갱신한다.
- short-term context, 학습되는 long-term memory와 training으로 고정된 persistent memory를 나눈다.

# 의미

“실시간으로 똑똑해진다”는 제목보다, 별도 offline retraining 없이 현재 sequence에서 기억할 표현을 갱신하는 test-time memorization 연구로 이해해야 한다. 개인 사용자 지식을 영구 보존하거나 model 전체가 지속 학습한다는 의미는 아니다.

# 한계

논문 benchmark에서 Transformer와 최신 recurrent model보다 좋은 결과를 보고했지만 아직 연구 architecture다. memory pollution, privacy, 장기 안정성, parallel training·serving 비용과 실제 제품 통합을 검증해야 한다. “무한 기억”이나 Transformer의 완전한 대체라는 표현은 과장이다.

# 출처

- [Google Research 공식 설명](https://www.research.google/blog/titans-miras-helping-ai-have-long-term-memory/)
- [Titans 논문](https://arxiv.org/abs/2501.00663)
- [AI타임스코리아 원문](https://www.aitimes.kr/news/articleView.html?idxno=37597)
- [Notion 원본 항목](https://app.notion.com/p/b771a73cf20b833e8f7c815650032825)
