---
type: Reference
title: "LangChain Skills: domain 지침을 필요한 순간에 불러오고 평가하는 방법"
description: "LangChain·LangSmith coding task 성능을 높인 skill 구성과 benchmark를 일반화할 때의 주의점"
resource: https://news.hada.io/topic?id=27359
notion: https://app.notion.com/p/cb61a73cf20b835b945181b07d0780b7
tags: [reading, agent-skills, langchain, evaluation]
timestamp: 2026-07-24
status: summarized
---

# 무엇을 공개했나

LangChain은 coding agent가 LangChain, LangGraph, Deep Agents와 LangSmith 작업을 수행할 때 참고하는 Markdown 지침·script·resource 묶음을 공개했다. 모든 내용을 system prompt에 넣는 대신 관련 task에서만 skill을 불러오는 progressive disclosure를 사용한다.

- LangChain skill 11종: agent loop, durable execution, human-in-the-loop 등
- LangSmith skill 3종: tracing, dataset 구축과 agent evaluation
- LangSmith CLI: terminal에서 trace, dataset과 experiment 관리

# 평가 결과

공식 LangChain skill eval set에서는 Claude Code 성능이 29%에서 95%로 올랐다고 보고한다. 별도의 skill 평가 실험에서는 task completion이 skill 사용 82%, 미사용 9%였다. 기사에 등장하는 25%→95%, 17%→92% 등은 LangChain·LangSmith task set과 metric이 다른 결과이므로 하나의 보편적 점수로 합치면 안 된다.

# 중요한 교훈

Skill 자체도 prompt software이므로 test가 필요하다. Docker 같은 고정 환경에서 baseline과 skill-enabled run을 반복하고 artifact correctness를 deterministic test로 확인한다. 관련 skill 호출률이 낮으면 `AGENTS.md`나 `CLAUDE.md`에 언제 쓸지 짧게 안내할 수 있다.

Skill이 너무 많거나 유사하면 routing이 나빠질 수 있다. 소개된 실험에서도 20개보다 12개로 줄였을 때 선택 정확도가 좋아졌다. 따라서 task taxonomy, trigger description, 최소 context와 regression suite를 함께 versioning해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27359)
- [LangChain Skills](https://www.langchain.com/blog/langchain-skills)
- [Evaluating Skills](https://www.langchain.com/blog/evaluating-skills)

