---
type: Reference
title: "OpenKB: 원문을 누적형 Markdown Wiki로 컴파일하기"
description: "여러 문서 형식을 요약·개념·교차 링크로 합성하고 query, lint와 watch workflow를 제공하는 CLI"
resource: https://discuss.pytorch.kr/t/openkb-llm/10058
notion: https://app.notion.com/p/54a1a73cf20b8238a15d01e8f0b81584
tags: [reading, knowledge-base, llm-wiki, rag]
timestamp: 2026-07-24
status: summarized
---

# RAG와 다른 목표

OpenKB는 질문할 때마다 관련 chunk를 찾고 버리는 대신 분석 결과를 Markdown Wiki로 계속 축적한다. 새 문서가 들어오면 기존 concept를 갱신하거나 새 page를 만들고 index, log와 cross-link를 함께 관리한다.

# 처리 구조

PDF, Word, Markdown, PowerPoint, HTML과 Excel을 `markitdown`으로 읽는다. 짧은 문서는 전체 text를 사용하고 20쪽 이상의 긴 PDF는 PageIndex tree로 구조를 먼저 압축한다. 출력에는 source 변환본, 문서별 summary, 여러 문서를 합친 concept, 저장한 exploration과 lint report가 포함된다.

# 사용 흐름

`openkb add`로 문서를 넣고 `query`·`chat`으로 질문한다. `--save`는 결과를 Wiki에 남기고 `lint`는 모순, 공백, orphan과 오래된 page를 찾는다. `watch`는 raw directory의 새 file을 감지해 갱신한다. LiteLLM을 통해 여러 model provider를 쓸 수 있다.

# 적용 시 주의

한 문서가 여러 concept를 자동 수정하면 잘못된 요약의 영향 범위도 커진다. raw source 불변성, page별 citation, diff review, conflict 표시와 rollback이 필수다. 한국어 Wiki는 CJK tokenization과 검색 품질도 별도 검증해야 한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/openkb-llm/10058)
- [VectifyAI/OpenKB](https://github.com/VectifyAI/OpenKB)

