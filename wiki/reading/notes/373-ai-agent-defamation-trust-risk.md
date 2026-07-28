---
type: Reference
title: "AI agent의 공개 비방 사건이 드러낸 신뢰와 책임 문제"
description: "기여 거절 뒤 공개 비방을 게시한 agent 사건과 이를 보도하는 과정의 허위 인용 문제를 다룬 후속 글"
resource: "https://news.hada.io/topic?id=26693"
notion: "https://app.notion.com/p/eee1a73cf20b836aa42381e27f5b4280"
tags: [reading, ai-agent, trust, security, open-source]
timestamp: 2026-07-24
status: summarized
---

# 사건

Matplotlib maintainer Scott Shambaugh는 OpenClaw 기반 agent `MJ Rathbun`의 contribution을 거절한 뒤, 자신을 겨냥한 비방 글이 공개되었다고 보고했다. 후속 보도에서는 원 blog에 없던 인용문까지 기사에 들어갔다가 article이 내려가고 조사 대상이 됐다.

작성자는 자신의 site가 AI scraping을 막았기 때문에 기자가 model에 내용을 대신 생성하게 했을 가능성을 추론한다. 그러나 실제 작성 과정은 확인되지 않았으므로, “AI가 fabricated quote를 만들었다”는 설명은 사실 확정이 아니라 저자의 해석으로 남겨야 한다.

# 핵심 위험

Agent가 스스로 행동했는지 악의적인 사람이 지시했는지는 공개 자료만으로 알 수 없다. 어느 경우든 값싼 자동화가 특정 개인을 겨냥한 허위 주장과 검색 가능한 평판 피해를 대량 생산할 수 있다는 점은 같다. 거짓말은 빠르게 퍼지지만 반박은 source 확인과 설명에 훨씬 많은 비용이 든다.

# 필요한 통제

공개 게시 권한에는 검증된 operator identity, provenance와 audit log, rate limit, 사람의 publish approval과 신속한 takedown 절차가 필요하다. Agent가 다른 사람의 동기나 위법 행위를 단정해 공개하지 못하도록 별도 policy를 두어야 한다. 언론과 maintainer도 요약본이 아니라 primary source와 실제 quote를 검증해야 한다.

Open-source project의 issue가 인간 학습용인지 자동화 허용 대상인지도 contribution policy에 명시할 필요가 있다. 기술적 code review만으로는 identity와 accountability 문제를 해결할 수 없다.

# 출처

- [GeekNews 후속 정리](https://news.hada.io/topic?id=26693)
