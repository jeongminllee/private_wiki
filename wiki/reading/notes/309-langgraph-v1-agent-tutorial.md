---
type: Study Note
title: "LangGraph 1.0 에이전트 튜토리얼: 쇼핑 고객지원으로 배우는 핵심 구성"
description: "ReAct agent, tool, runtime context, 구조화 응답, memory와 human-in-the-loop를 한 프로젝트에서 익히는 한국어 실습"
resource: "https://github.com/IHAGI-c/langgraph-agent-tutorial"
notion: "https://app.notion.com/p/a801a73cf20b8275a42e81458f1d0a22"
tags: [reading, langgraph, tutorial, ai-agents]
timestamp: 2026-07-24
status: summarized
---

# 학습 범위

LangGraph 1.0으로 전자상거래 고객지원 에이전트를 만드는 한국어 교육 프로젝트다. 상품 검색·추천, 배송 상태 조회와 고객 프로필 기반 개인화를 구현하면서 다음 요소를 단계적으로 다룬다.

- `create_react_agent`로 ReAct 스타일 에이전트 생성
- `@tool`로 외부 기능 정의
- `ToolRuntime`과 `context_schema`로 실행 환경 전달
- Pydantic 기반 구조화 응답
- `InMemorySaver`와 `thread_id`로 대화 이력 유지
- middleware를 이용한 human-in-the-loop 승인

Jupyter notebook은 개념 실습용이고 `src/shopping_agent/`는 배포 가능한 형태로 agent, tool, data와 prompt를 나눈다. `langgraph.json`을 이용해 `uv run langgraph dev`로 개발 서버를 띄우고 별도 Agent Chat UI에서 시험할 수 있다.

# 실행 환경

Python 3.11 이상과 `uv`가 필요하다. Azure OpenAI key는 필수이고 LangSmith tracing과 Tavily 검색은 선택이다. `uv.lock`을 이용해 환경을 고정하고 Jupyter kernel을 별도로 등록한다. README의 Windows 활성화 명령에는 렌더링상 공백이 섞여 있으므로 실제 경로는 `.venv\Scripts\activate`로 해석해야 한다.

# 학습 후 보완할 점

`InMemorySaver`는 프로세스 종료 뒤 상태를 보존하지 않으므로 실제 서비스에서는 durable checkpoint store가 필요하다. 도구의 권한, 재시도, idempotency, 개인정보 마스킹과 승인 timeout도 예제 바깥에서 설계해야 한다. 저장소는 교육 목적이며 무단 배포 금지 고지가 있으므로 자료를 그대로 재배포하지 않고 개념과 코드 구조만 참고한다.

# 출처

- [LangGraph Agent Tutorial](https://github.com/IHAGI-c/langgraph-agent-tutorial)
