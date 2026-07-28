---
type: Reference
title: "Opentology: 코드와 개발 세션을 RDF 지식 그래프로 보존하기"
description: "symbol dependency, 변경 영향과 session memory를 embedded Oxigraph에 저장하는 coding assistant 보조 도구"
resource: https://news.hada.io/topic?id=28489
notion: https://app.notion.com/p/dd11a73cf20b83fa91e70185cfcfe4d4
tags: [reading, knowledge-graph, ai-coding, rdf]
timestamp: 2026-07-24
status: summarized
---

# 무엇을 저장하는가

Opentology는 codebase의 symbol·module dependency, 작업 중 얻은 지식과 이전 session을 RDF graph로 저장한다. LLM이 매번 repository를 처음부터 탐색하는 대신 필요한 관계와 과거 맥락을 명시적으로 불러오게 한다.

# 주요 명령

- `context-scan`: symbol과 module dependency를 graph로 만든다.
- `context-impact`: 변경할 symbol의 blast radius를 계산한다.
- `context-load`: project와 이전 session 정보를 시작 context에 넣는다.
- `context-save`: 현재 session에서 얻은 정보를 보존한다.
- `context-graph`: graph visualization을 연다.

Oxigraph WASM을 embedded로 사용해 별도 graph server 없이 실행할 수 있다.

# 평가할 점

RDF는 관계를 질의하고 provenance를 붙이기 좋지만 source 변경 뒤 stale edge를 제거하는 증분 indexing이 정확해야 한다. 정적 dependency만으로 runtime behavior를 모두 알 수 없으며, LLM이 저장한 “지식”은 사실과 추론을 구분해야 한다. 소개 시점은 0.4 pre-release이므로 large monorepo 성능과 language 지원을 직접 검증할 필요가 있다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=28489)

