---
type: Reference
title: "Pi 코딩 에이전트를 만들며 배운 단순성·맥락·관찰 가능성"
description: "모델 API, agent loop, TUI와 coding CLI를 작은 모듈로 나누며 얻은 설계 교훈"
resource: https://news.hada.io/topic?id=26324
notion: https://app.notion.com/p/2571a73cf20b8357aac301222b63941c
tags: [reading, ai-agents, coding-agent, context-engineering]
timestamp: 2026-07-24
status: summarized
---

# 네 계층

Pi는 provider 차이를 통합하는 `pi-ai`, message·tool loop를 담당하는 `pi-agent-core`, terminal rendering을 맡는 `pi-tui`, 실제 CLI 제품인 `pi-coding-agent`로 나뉜다. 모델 API, orchestration, UI와 제품 기능의 경계를 작게 유지한 구조다.

# 의도적으로 뺀 기능

system prompt는 1,000 token 이하이고 기본 도구는 read·write·edit·bash뿐이다. built-in plan, todo, MCP, background shell과 subagent를 core에서 제외하고 Markdown file, CLI, tmux와 자기 호출로 대체한다. 모든 command와 file access를 화면에 보여 context 통제와 관찰 가능성을 우선한다.

# 중요한 교훈

provider 호환은 field 이름, reasoning 표현, token count와 abort semantics처럼 세부 차이를 흡수해야 한다. UI용 tool result와 LLM용 text를 분리하면 같은 실행을 사람이 읽기 좋게 표시할 수 있다. 기능 수보다 context가 어떻게 쌓이고 잘리는지, 사용자가 어떤 action을 볼 수 있는지가 agent 품질에 직접 영향을 준다.

# 안전 주의

Pi의 unrestricted mode는 container처럼 경계가 분명한 환경을 전제로 해야 한다. 단순함이 sandbox와 승인 정책의 필요까지 없애지는 않는다.

# 출처

- [GeekNews 정리와 토론](https://news.hada.io/topic?id=26324)

