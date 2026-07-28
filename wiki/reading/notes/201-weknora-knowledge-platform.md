---
type: Reference
title: "WeKnora: 문서를 RAG·Agent·Wiki로 바꾸는 지식 플랫폼"
description: "여러 형식의 문서를 검색형 질의응답, ReAct 에이전트와 연결형 Wiki로 제공하는 오픈소스 지식 플랫폼"
resource: https://github.com/Tencent/WeKnora
notion: https://app.notion.com/p/1f91a73cf20b826a8c6881a189bfbc1c
tags: [reading, rag, ai-agents, knowledge-base]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

WeKnora는 PDF, Word, 이미지, 표와 외부 지식 서비스를 한곳에 가져와 RAG 질의응답, ReAct 에이전트, 상호 연결된 Markdown Wiki로 제공하는 오픈소스 플랫폼이다. 단순한 벡터 검색 UI보다 수집, 파싱, 검색, 생성, 권한과 관측 가능성을 함께 운영하려는 제품에 가깝다.

# 핵심 기능

- BM25, dense retrieval, GraphRAG, parent-child retrieval을 조합한다.
- Feishu, Notion, Yuque, RSS와 여러 문서 형식의 가져오기·동기화를 지원한다.
- Wiki Mode는 자료를 주제별 문서와 링크 구조로 재구성하고 지식 그래프로 보여준다.
- 여러 LLM 제공자, vector DB, 저장소와 메신저 채널을 교체할 수 있다.
- RBAC, 감사 log, 범위가 제한된 API key, secret 암호화, SSRF 방어와 sandbox를 포함한다.
- Langfuse 관측, worker queue, parsing trace, CLI와 MCP를 제공한다.

# 시작과 평가 포인트

기본 설치는 저장소를 clone하고 `.env.example`을 `.env`로 복사한 뒤 `docker compose up -d`로 실행한다. 실제 도입 전에는 한국어 문서와 표의 parsing 품질, 답변 인용 정확도, Wiki 자동 갱신 시 기존 수기 문서 보존 여부를 작은 자료 묶음으로 검증해야 한다. 기능 폭이 넓은 만큼 구성 요소와 운영 부담도 함께 평가할 필요가 있다.

# 출처

- [Tencent/WeKnora](https://github.com/Tencent/WeKnora)

