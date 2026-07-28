---
type: Reference
title: "Claude Code 입문과 실전 프로젝트"
description: "설치·에이전틱 루프·권한부터 RAG, SQL agent와 multi-agent code review까지 이어지는 WikiDocs 교재"
resource: https://wikidocs.net/book/19202
notion: https://app.notion.com/p/56c1a73cf20b82f3a38e81ddc71e3f5b
tags: [reading, claude-code, wikidocs, learning]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

판다스 스튜디오가 집필한 Claude Code 한국어 입문서다. 처음 실행과 permission 승인에서 시작해 세션·컨텍스트·`CLAUDE.md`, Git, IDE, MCP, CI/CD, skill과 hook으로 확장하고, 뒤에서는 AI application을 직접 만드는 프로젝트로 연결한다.

# 구성

## Claude Code 핵심

1~13장은 설치, 첫 변경, agentic loop, interactive mode, codebase 탐색, plan mode, memory, 권한과 sandbox, Git/worktree, IDE, MCP, headless 자동화, skill·subagent, 비용 관리를 다룬다. 각 장의 연습 문제로 명령을 읽는 데서 끝나지 않고 직접 실행하게 한다.

## 실전 프로젝트

14~17장은 LangChain과 FAISS를 이용한 RAG 문서 Q&A, 웹 검색 ReAct agent, pandas 기반 EDA 자동화, SQLite와 Streamlit을 사용한 SQL agent를 만든다. 이후 FastMCP server와 병렬 code review system까지 확장한다.

# 읽는 순서

처음 사용한다면 첫 세션, 권한과 Git 부분을 먼저 실습한다. AI application 개발 경험이 이미 있다면 세션·컨텍스트, 권한, MCP와 자동화 장을 골라 읽는다. 예제의 API key는 저장소에 넣지 않고 환경 변수나 secret store로 관리한다.

# 주의할 점

Claude Code와 LangChain은 빠르게 변한다. 책도 갱신되지만 특정 command, permission mode, package version과 UI가 현재 공식 문서와 다를 수 있다. 예제 앱은 학습용이므로 prompt injection, SQL write 제한, 문서 개인정보와 production 관찰 기능을 별도로 설계해야 한다.

# 출처

- [WikiDocs 교재](https://wikidocs.net/book/19202)
- [Claude Code 공식 문서](https://code.claude.com/docs/en/overview)
- [Notion 원본 항목](https://app.notion.com/p/56c1a73cf20b82f3a38e81ddc71e3f5b)

