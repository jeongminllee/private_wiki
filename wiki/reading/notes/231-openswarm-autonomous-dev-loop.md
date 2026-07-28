---
type: Reference
title: "OpenSwarm: issue에서 PR·CI 수정까지 이어가는 자율 개발 loop"
description: "Claude Code worker·reviewer를 조율하고 project memory와 code graph를 결합한 초기 단계 개발 pipeline"
resource: https://news.hada.io/topic?id=27216
notion: https://app.notion.com/p/1ba1a73cf20b832fb74c8188198131db
tags: [reading, ai-agents, ai-coding, orchestration]
timestamp: 2026-07-24
status: summarized
---

# 작업 흐름

OpenSwarm은 Linear issue를 가져와 Worker, Reviewer, 선택적 Tester·Documenter 순서로 처리하고 code change, PR, CI 수정과 issue 상태 update까지 이어가는 Claude Code orchestration pipeline이다.

# 상태와 context

- LanceDB와 multilingual-e5로 이전 작업 맥락을 검색한다.
- codebase scan 결과로 dependency와 change impact graph를 만든다.
- Discord에서 dispatch·schedule·log·pair session을 제어한다.
- web dashboard에서 pipeline과 PR processor를 관찰한다.
- CI failure와 merge conflict를 재시도해 PR이 통과할 때까지 loop를 이어간다.

# 운영 위험

자동 commit과 무한 재시도는 잘못된 변경, 비용 폭증과 issue 상태 왜곡을 만들 수 있다. branch isolation, 최대 시도·비용, required test, human merge gate와 rollback이 필요하다. 소개 당시 초기 project였으므로 memory가 쌓일수록 실제 품질이 좋아진다는 주장은 장기 평가로 확인해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27216)

