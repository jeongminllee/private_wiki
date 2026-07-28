---
type: Reference
title: "Agent Lattice: 코드와 문서를 잇는 지식 그래프"
description: "Markdown 섹션, 코드 심볼, 테스트 명세를 양방향 링크로 연결하고 참조 무결성을 검사"
resource: https://discuss.pytorch.kr/t/lat-md-agent-lattice-ai/10095
notion: https://app.notion.com/p/3611a73cf20b818c90a8d5edbb7ae690
tags: [reading, ai-agents, knowledge-graph, documentation]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`lat.md` 또는 Agent Lattice는 코드베이스의 설계 결정과 도메인 지식을 Markdown 섹션으로 저장하고, 코드 심볼과 양방향으로 연결하는 도구다. 하나의 거대한 `AGENTS.md`에 모든 맥락을 넣는 대신 검색하고 검증할 수 있는 작은 지식 그래프를 만든다.

# 연결 방식

- 문서끼리 `[[file#Section]]` 위키 링크로 연결한다.
- 문서에서 `[[src/auth.ts#validateToken]]`처럼 코드 심볼을 가리킨다.
- 코드에는 `// @lat: [[section-id]]` 주석으로 문서 백링크를 둔다.
- 테스트 명세에 코드 언급을 필수로 설정해 문서와 테스트의 연결 누락을 검사할 수 있다.

# 주요 명령

- `lat init`: 디렉터리와 에이전트 지침을 만든다.
- `lat check`: 깨진 문서 링크와 코드 참조를 검사한다.
- `lat search`: 임베딩 기반 의미 검색을 수행한다.
- `lat section`, `lat refs`: 본문과 정·역방향 참조를 조회한다.
- `lat expand`: 프롬프트의 참조를 실제 문맥으로 펼친다.
- `lat mcp`: MCP 서버로 에디터·에이전트에 연결한다.

# 내 wiki에 주는 아이디어

현재 wiki에도 깨진 링크 검사와 작은 개념 문서 원칙이 있다. 추가로 “문서가 설명하는 실제 코드나 설정 파일”을 기계적으로 검증할 수 있는 참조를 도입하면 설명과 구현의 불일치를 더 일찍 찾을 수 있다.

# 주의

코드 주석에 링크를 많이 넣으면 리팩터링 비용이 커질 수 있다. 모든 심볼을 연결하기보다 아키텍처 결정, 보안 경계, 회귀 테스트처럼 오래 유지할 지식부터 시작하는 편이 낫다.

# 관련 문서

- [llm-wiki 지식 그래프 방식](033-llm-wiki-knowledge-graph-skill.md)
- [CodeGraph](052-codegraph-code-knowledge-graph.md)

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/lat-md-agent-lattice-ai/10095)
- [lat.md GitHub](https://github.com/1st1/lat.md)

