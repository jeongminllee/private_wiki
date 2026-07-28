---
type: Reference
title: "2025년 주목받은 Python library 지도"
description: "개발 도구와 AI·ML·data 분야의 신규 Python library를 문제 영역별로 정리한 Tryolabs 연례 목록"
resource: "https://news.hada.io/topic?id=25458"
notion: "https://app.notion.com/p/f201a73cf20b83e0a59381240c15b5de"
tags: [reading, python, library, developer-tools, ai]
timestamp: 2026-07-24
status: summarized
---

# 일반 개발 도구

목록에는 Rust 기반 type checker `ty`, cognitive complexity 측정기 `complexipy`, 여러 문서 형식을 처리하는 `Kreuzberg`, rate limiter `throttled-py`, HTTP 단계별 timing을 보는 `httptap`, FastAPI security middleware와 dead-code·위험 pattern 분석 도구, 여러 framework에 OpenAPI를 붙이는 `FastOpenAPI` 등이 포함된다.

# AI·ML·Data

`MCP Python SDK`와 `FastMCP`는 tool protocol, `TOON`은 LLM 입력용 compact notation, `Deep Agents`와 `smolagents`는 agent workflow와 code execution, `LlamaIndex Workflows`는 event 기반 orchestration을 다룬다. 이 밖에 multi-provider batch API `Batchata`, document-to-Markdown `MarkItDown`, visualization tool `Data Formulator`, 근거 위치를 보존하는 extraction library `LangExtract`, geospatial AI용 `GeoAI`가 선정됐다.

# 목록을 활용하는 법

연례 “주목” 목록은 maturity 순위가 아니다. 실제 도입 전 release cadence, maintainer 수, license, dependency와 security advisory, benchmark 재현 여부를 확인한다. 기존 stack이 해결하는 문제를 새 library가 얼마나 줄이는지 작은 spike에서 비교하고, lockfile과 rollback plan을 둔다.

특히 agent와 document parser는 untrusted input과 code execution을 다루므로 sandbox, file size limit와 prompt injection 방어가 필요하다. Article의 속도와 token 절감 수치는 각 project의 주장으로 보고 workload에서 다시 측정해야 한다.

# 출처

- [GeekNews 상세 정리](https://news.hada.io/topic?id=25458)
- [Tryolabs 원문](https://tryolabs.com/blog/2025/12/23/top-python-libraries-2025)
