---
type: Reference
title: "Act Operator: LangGraph 프로젝트의 규칙을 실행 가능한 하네스로 만들기"
description: "프로젝트 구조, 에이전트 스킬, 패턴과 CLAUDE.md 피드백 루프를 함께 생성하는 LangGraph 1.0+ 스캐폴더"
resource: "https://github.com/Proact0/act-operator"
notion: "https://app.notion.com/p/9a61a73cf20b8337b698811bc06f88ce"
tags: [reading, langgraph, ai-agents, scaffolding]
timestamp: 2026-07-24
status: summarized
---

# 해결하려는 문제

에이전트 프로젝트의 중요한 관례가 대화와 사람의 머릿속에만 남으면 새 세션마다 다시 설명해야 한다. Act Operator는 이 context gap을 줄이기 위해 LangGraph 1.0+ 프로젝트의 구조와 작업 규칙을 함께 생성하는 production-oriented harness다. Python 3.11 이상에서 `uvx --from act-operator act new`로 시작한다.

# 세 계층

1. Scaffolding이 state, node, agent, tool, middleware, test와 CI가 들어갈 프로젝트 골격을 만든다.
2. Act Template, 역할별 skill과 Drawkit 문서가 실행 가능한 단일 지식 원천 역할을 한다.
3. 프로젝트 루트와 하위 단위의 `CLAUDE.md`가 실제 개발에서 발견한 관례를 에이전트에게 다시 전달한다.

Act는 전체 프로젝트와 하네스이고 Cast는 하나의 `StateGraph` 실행 단위다. 한 monorepo에 여러 Cast를 둘 수 있다. `architecting-act`, `developing-cast`, `engineering-act`, `testing-cast` 같은 skill과 50개가 넘는 패턴을 제공해 설계·개발·시험의 컨텍스트를 나눈다.

# 적용 판단

스캐폴딩은 팀의 암묵지를 파일로 바꾸고 새 에이전트가 구조를 빨리 파악하도록 돕는다. 하지만 생성된 구조가 곧 production 품질을 보장하지는 않는다. state persistence, retry와 idempotency, 인증·비밀 관리, 관측성, 배포 topology는 서비스 요구에 맞게 검토해야 한다. 프로젝트가 작다면 많은 패턴이 오히려 유지비가 될 수 있으므로 필요한 Cast와 skill부터 도입하는 편이 낫다. 라이선스는 Apache-2.0이다.

# 출처

- [Act Operator 저장소](https://github.com/Proact0/act-operator)
