---
type: Reference
title: "Knowledge Graph로 agent의 API 선택 순서까지 찾는 DeepLearning.AI 과정"
description: "API specification과 business process를 graph로 연결해 tool discovery·execution을 구현하는 74분 과정"
resource: https://learn.deeplearning.ai/courses/knowledge-graphs-for-ai-agent-api-discovery/lesson/536du6/api-knowledge-graph-construction
notion: https://app.notion.com/p/4b81a73cf20b82668a778139e0884985
tags: [reading, knowledge-graph, ai-agent, api]
timestamp: 2026-07-24
status: summarized
---

# 해결하는 문제

기업에는 수천 개 API가 있어 semantic search만으로 비슷한 endpoint를 찾더라도 prerequisite와 호출 순서를 알기 어렵다. 이 과정은 API specification을 knowledge graph로 만들고 business-process edge를 추가해 agent가 필요한 API 집합과 실행 순서를 함께 찾게 한다.

# 학습 흐름

1. API service와 endpoint metadata를 graph node·edge로 변환
2. Business process data로 서로 고립된 API와 dependency 연결
3. Semantic retrieval로 후보 API를 좁힘
4. Graph의 process edge를 따라 누락된 prerequisite와 순서 확장
5. Discovery, GET data와 POST data tool을 가진 agent로 실제 business task 실행

Course는 7개 video lesson과 4개 code example, quiz로 구성되고 총 1시간 14분이다. API graph construction, business-process integration, graph discovery와 business-process agent가 주요 실습이다. SAP Business AI의 Pavithra G K와 Lars Heling이 강의한다.

# 핵심 아이디어

Vector retrieval은 query와 endpoint 설명의 유사성을 찾지만 “계정을 만든 뒤 주문을 제출해야 한다” 같은 절차 제약을 직접 표현하기 어렵다. Knowledge graph는 endpoint, property, navigation과 business step의 관계를 명시해 retrieval 결과를 executable plan으로 확장한다.

# 적용 전 확인

Graph schema와 process data가 오래되면 agent가 틀린 순서를 자신 있게 실행한다. OpenAPI 변화 감지, provenance, write API approval, idempotency와 rollback을 별도로 설계해야 한다. Intermediate course이며 기본 Python 지식이 필요하다.

# 출처

- [저장된 lesson](https://learn.deeplearning.ai/courses/knowledge-graphs-for-ai-agent-api-discovery/lesson/536du6/api-knowledge-graph-construction)
- [Course 소개](https://www.deeplearning.ai/alpha/short-courses/knowledge-graphs-for-ai-agent-api-discovery/)

