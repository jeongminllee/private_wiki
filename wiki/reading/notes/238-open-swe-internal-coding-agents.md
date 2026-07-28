---
type: Reference
title: "Open SWE: 사내 Coding Agent를 기존 업무 흐름에 넣는 Framework"
description: "Deep Agents, persistent sandbox와 middleware로 Slack·Linear·GitHub 기반 coding workflow를 구성하는 방법"
resource: https://www.langchain.com/blog/open-swe-an-open-source-framework-for-internal-coding-agents
notion: https://app.notion.com/p/72c1a73cf20b82bdb35f81f1f35f2e8c
tags: [reading, ai-agents, ai-coding, langgraph]
timestamp: 2026-07-24
status: summarized
---

# Architecture

Open SWE는 완성된 coding product보다 조직별 agent를 만들기 위한 composable base다. Deep Agents의 planning, file-based context와 subagent를 사용하고 LangGraph의 stateful orchestration을 결합한다.

# 실행 경계

각 conversation thread는 repository를 clone한 persistent cloud sandbox를 갖는다. sandbox 내부에서는 shell 전체 권한을 주되 production system과 다른 task의 blast radius는 격리한다. Modal, Daytona, Runloop와 LangSmith backend를 지원하고 자체 backend도 구현할 수 있다.

# Context와 tool

root `AGENTS.md`에는 convention, test와 architecture decision을 넣고, Linear issue나 Slack thread의 전체 내용을 task context로 제공한다. 기본 tool은 file edit, shell, web fetch, HTTP, PR 생성과 comment처럼 명확한 목적만 갖는다. 후속 message 주입, tool error 처리와 “agent가 놓친 PR 열기”는 deterministic middleware가 보완한다.

# 적용 기준

Slack 호출이 편리해도 sender identity, repository authorization과 secret scope가 연결되어야 한다. task별 clean branch, required CI, human merge gate, sandbox image provenance, trace와 비용 budget을 운영 설계에 포함해야 한다. framework adoption 자체보다 조직의 acceptance test와 tool ownership이 성패를 가른다.

# 출처

- [LangChain 공식 소개](https://www.langchain.com/blog/open-swe-an-open-source-framework-for-internal-coding-agents)

