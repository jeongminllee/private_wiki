---
type: Reference
title: "Mantic: 파일 구조와 symbol을 활용하는 agent용 code search"
description: "Git metadata, structural scoring과 optional semantic reranking으로 관련 code를 찾는 local-first 도구"
resource: https://news.hada.io/topic?id=25942
notion: https://app.notion.com/p/e931a73cf20b8343ac5f813fb4e6ced7
tags: [reading, code-search, ai-agent, mcp]
timestamp: 2026-07-24
status: summarized
---

# 무엇인가

Mantic은 agent가 repository 전체를 무작정 읽기 전에 관련 file을 좁히는 local-first code search engine이다. `git ls-files`, path, filename, extension과 project 구조를 deterministic하게 scoring해 결과 file과 token estimate를 반환한다.

# 검색 방식

- CamelCase 분해, word boundary와 연속 path component matching
- Exact filename과 business-logic file 가중치, boilerplate penalty
- code·test·config filter와 `--path` scope
- symbol definition·reference, dependency와 impact analysis
- session에서 본 file과 성공한 search pattern을 local memory로 재사용
- CLI, VS Code·Cursor와 MCP server 제공

`ripgrep`은 exact text를 가장 빠르게 찾는 데 강하고, Mantic은 “payment 처리 code가 어디인가”처럼 의도와 구조가 중요한 질문의 ranking을 목표로 한다. 공식 benchmark도 raw speed에서는 `ripgrep`이 더 빠르며 Mantic의 장점은 relevance라고 정리한다.

# 저장 당시와 현재의 차이

저장된 소개는 embedding이나 vector DB 없이 동작한다고 설명했다. 2026-07-24 공식 저장소의 v1.0.25에는 기본 structural search 외에 `transformers.js` local embedding을 쓰는 optional `--semantic` reranking이 추가됐다. 따라서 “embedding을 전혀 쓰지 않는다”는 설명은 현재 모든 mode에 해당하지 않는다.

# 검증할 것

저장소 저자가 제시한 최대 63% token 절감과 benchmark는 independent result가 아니다. 실제 codebase에서 known-answer query, symbol language coverage, generated file 처리와 indexing latency를 `rg`, language server와 비교해야 한다. Local execution도 `npx ...@latest` 공급망과 MCP tool permission 검토는 필요하다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=25942)
- [Mantic.sh 저장소](https://github.com/marcoaapfortes/Mantic.sh)

