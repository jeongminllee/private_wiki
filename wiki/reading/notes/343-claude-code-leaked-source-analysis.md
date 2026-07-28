---
type: Reference
title: "Claude Code 노출 소스 기반 구조 분석서"
description: "2026년 3월 말 노출된 것으로 알려진 bundle을 바탕으로 query loop, tool, permission과 context 구조를 설명한 2차 분석"
resource: "https://news.hada.io/topic?id=28080"
notion: "https://app.notion.com/p/7781a73cf20b828ea78b8166cba02da7"
tags: [reading, claude-code, architecture, security, source-analysis]
timestamp: 2026-07-24
status: summarized
---

# 분석서의 범위

작성자는 2026년 3월 31일 시점의 TypeScript·React file 약 1,884개를 분석했다고 밝힌다. 노출된 source code 자체는 한 줄도 싣지 않고 구조와 동작 흐름만 설명한다. 핵심은 `사용자 요청 → API streaming → tool use 감지 → 입력·권한 검사 → 실행 → 결과를 model에 반환`하는 query loop다.

# 설명하는 구조

초기화 단계가 인증, model, 설정, feature gate, Git 상태와 `CLAUDE.md`를 모은 뒤 REPL 또는 headless mode를 시작한다. Query loop는 context 축소, streaming API, 복구 가능한 error의 retry, tool 실행과 Stop hook을 반복한다. Read 계열은 병렬화하고 Edit·Bash 같은 변경 tool은 순차 실행한다는 분석도 담겨 있다.

Tool은 schema, 실행 함수, permission check, semantic validation, concurrency·read-only 속성과 result size 제한을 공통 interface로 가진다. Headless `QueryEngine`, coordinator, local-cloud bridge 같은 mode와 transcript persistence, usage budget도 별도 계층으로 설명한다.

# 읽을 때의 주의

이 문서는 공식 architecture specification이 아니며 출처가 된 code의 취득·공개 경위에 윤리적·법적 논쟁이 있다. 분석서의 내부 이름, file 크기와 hidden feature는 release마다 쉽게 바뀌고 오독 가능성도 있다. 구현을 복제하는 자료가 아니라 공개 product behavior를 이해하는 보조 자료로만 사용하고, 현재 기능은 공식 문서와 실제 version에서 검증한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=28080)
- [WikiDocs 분석서](https://wikidocs.net/338204)
