---
type: Reference
title: "AI Engineering Stack의 세 계층과 역할 경계"
description: "AI application, model development, infrastructure를 나누고 AI engineer·ML engineer·full-stack engineer의 책임을 비교한 번역 글"
resource: "https://blogbyash.com/translation/ai-engineering-stack/"
notion: "https://app.notion.com/p/9e41a73cf20b83b4b2f981d27f4e1e96"
tags: [reading, ai-engineering, ml-engineering, infrastructure, career]
timestamp: 2026-07-24
status: summarized
---

# 세 계층

AI engineering stack은 크게 application development, model development, infrastructure로 나눌 수 있다. Application 계층은 foundation model을 API나 open weight로 사용해 context, retrieval, agent, evaluation과 user feedback loop를 제품으로 만든다. Model 계층은 fine-tuning, data curation, training과 model evaluation을 다룬다. Infrastructure는 compute, serving, storage, observability, latency와 cost를 책임진다.

# 직무 비교

AI engineer는 대개 model을 처음부터 훈련하기보다 기존 model을 조합해 유용하고 신뢰할 수 있는 application을 만든다. Prompt와 RAG뿐 아니라 nondeterministic output 평가, provider 변화, safety, latency와 token 비용까지 소유한다.

ML engineer는 전통적으로 task-specific model의 training·deployment와 feature·data pipeline에 더 가깝다. Full-stack engineer는 UI, API, database와 deterministic application behavior를 맡지만 AI 기능을 넣으면 evaluation과 model lifecycle까지 경계가 넓어진다.

# 읽을 때 주의할 점

실제 조직의 직함은 이 분류와 일치하지 않는다. “AI engineer”라는 이름보다 누가 data quality, model adaptation, production reliability와 사용자 성과를 책임지는지로 역할을 정의해야 한다. 작은 team에서는 한 사람이 세 계층을 모두 다룰 수도 있다.

이 page는 Chip Huyen의 책 《AI Engineering》 일부를 번역·발췌한 글이다. 원문의 전체 논지를 대신하지 않으며, 인용과 세부 맥락은 저자의 책과 공식 자료에서 확인해야 한다.

# 출처

- [번역 글](https://blogbyash.com/translation/ai-engineering-stack/)
- [AI Engineering 저자 공식 페이지](https://huyenchip.com/ai-engineering-book/)
