---
type: Reference
title: "Codex Goals: 긴 작업의 지속 목표"
description: "여러 번의 자동 계속 실행에서도 목표, 완료 증거와 제약을 유지하는 Codex의 persistent goal 기능"
resource: https://news.hada.io/topic?id=29639
notion: https://app.notion.com/p/3681a73cf20b81dd9a33ddaa19dede13
tags: [reading, codex, ai-agent, workflow]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Goal은 한 번의 응답으로 끝내기 어려운 작업에서 Codex가 지속적으로 추적할 목적을 설정하는 기능이다. 일반 대화의 최근 요청만 따르는 대신 목표, 검증 기준, 제약과 중단 조건을 유지하면서 여러 차례 작업을 이어간다. 현재 이 읽기 자료 전체 처리도 같은 방식으로 운영할 수 있는 사례다.

# 좋은 목표의 구성

- **결과**: 무엇이 실제로 만들어지거나 바뀌어야 하는가
- **완료 증거**: 어떤 테스트, 수치, 파일 또는 화면으로 끝을 판단하는가
- **제약**: 건드리지 않을 자료, 비용, 보안과 품질 기준은 무엇인가
- **작업 경계**: 포함·제외 범위와 사용자 확인이 필요한 행동은 무엇인가
- **막힘 처리**: 어떤 실패를 기록하고 언제 사람에게 넘길 것인가

ChatGPT 데스크톱 앱, Codex CLI와 IDE 확장에서는 `/goal`로 목표를 설정하거나 보고, `/goal edit`, `/goal pause`, `/goal resume`, `/goal clear`로 상태를 관리한다. UI와 명령은 제품 버전에 따라 바뀔 수 있으므로 현재 매뉴얼을 기준으로 한다.

# 적합한 작업

대규모 마이그레이션, 성능 프로파일링과 반복 최적화, flaky test 조사, 여러 문서의 일괄 수집처럼 진행 상태와 완료 기준을 계속 유지해야 하는 일에 적합하다. 한 번의 파일 수정이나 단순 질의에는 목표 관리 비용이 더 클 수 있다.

# 주의할 점

지속 실행은 무제한 자율 실행을 뜻하지 않는다. 완료했다고 주장하는 문장보다 테스트와 산출물을 확인해야 하며, 권한 변경·배포·삭제 같은 중요한 행동은 별도 승인 경계를 둔다. 같은 장애가 반복되면 이유와 필요한 외부 입력을 기록하고 멈추게 해야 한다.

# 출처

- [Codex 공식 매뉴얼](https://developers.openai.com/codex/codex-manual.md)
- [GeekNews 한국어 소개](https://news.hada.io/topic?id=29639)
- [Notion 원본 항목](https://app.notion.com/p/3681a73cf20b81dd9a33ddaa19dede13)

