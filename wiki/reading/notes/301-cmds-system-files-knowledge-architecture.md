---
type: Reference
title: "CMDS System Files: 사람과 AI가 함께 쓰는 Obsidian 지식 아키텍처"
description: "10,000개가 넘는 노트를 운영하며 역할별 지침, 우선순위, 공통 규칙과 컨텍스트 복구를 분리한 시스템 파일 설계"
resource: "https://github.com/johnfkoo951/cmds-system-files"
notion: "https://app.notion.com/p/dd51a73cf20b8332b39301c28623d246"
tags: [reading, knowledge-management, ai-agents, obsidian]
timestamp: 2026-07-24
status: summarized
---

# 무엇을 공개한 저장소인가

10,000개가 넘는 Obsidian 노트를 사람과 여러 AI 에이전트가 함께 다루기 위해 만든 운영 파일 모음이다. 현재 README 기준 공개 구성은 핵심 파일 6개, 공통 규칙 8개, 아키텍처 패턴 9개다. 저장소 설명의 더 작은 숫자는 이전 상태로 보이므로 세부 목록은 README를 기준으로 보는 편이 낫다.

핵심 파일은 역할을 나눠 가진다. `CLAUDE.md`는 Claude용 기술적 실행법, `AGENTS.md`는 도구에 덜 종속적인 에이전트 규칙, `CMDS.md`는 시스템의 이유와 대상, `CMDS-Guide.md`는 운영법, `CMDS-Head-Quarter.md`는 탐색 허브, `DESIGN.md`는 시각 언어를 담당한다. `@path`는 AI 컨텍스트에 실제 내용을 넣고, `[[wikilink]]`는 사람이 Obsidian 그래프를 탐색하는 데 쓴다는 구분도 유용하다.

# 재사용할 설계

- 충돌 시 적용 순서를 문서마다 명시한다.
- 변하지 않는 규칙과 세션별 동적 정보를 나눠 캐시한다.
- 공통 규칙은 한곳에 두고 `@include` 방식으로 불러온다.
- 컨텍스트 압축 뒤 반드시 복원할 최소 정보를 별도로 둔다.
- 문서마다 필수 사용자와 선택 사용자를 표시한다.
- 메모리 종류, 예상 토큰, 변경 이력을 메타데이터로 관리한다.

작업 흐름은 Connect, Merge, Develop, Share다. 새 도구를 기존 지식 체계에 연결하고, 중복 지침을 병합하고, 실제 사용으로 개선한 뒤 재사용 가능한 부분을 공유한다. 이 저장소의 가장 큰 가치는 특정 파일을 그대로 복사하는 데 있지 않고, 지식의 의미와 에이전트 실행 규칙을 서로 다른 계층으로 분리한 데 있다.

# 주의점

공개 저장소지만 표준 라이선스 파일은 확인되지 않고 지적재산권 고지가 따로 있다. 공개됐다는 사실만으로 자유로운 재배포·수정을 가정하면 안 된다. 또한 `ANTIGRAVITY.md`, `BRAIN.md`, `BRAIN_PROMPT.md` 등 개인 파일은 배포 대상이 아니므로 공개된 구조만 참고해야 한다.

# 출처

- [CMDS System Files 저장소](https://github.com/johnfkoo951/cmds-system-files)
