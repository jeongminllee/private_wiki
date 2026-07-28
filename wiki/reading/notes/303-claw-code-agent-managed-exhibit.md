---
type: Reference
title: "Claw Code: 에이전트가 유지하는 코딩 CLI 실험 전시물"
description: "Rust 기반 코딩 에이전트 하네스를 AI가 스스로 관리하게 한 공개 실험이자 비프로덕션 프로젝트"
resource: "https://github.com/ultraworkers/claw-code"
resource_aliases: [https://github.com/instructkr/claw-code]
notion: "https://app.notion.com/p/9d81a73cf20b82b788a9013d19c27f59"
tags: [reading, ai-agents, coding-agents, rust]
timestamp: 2026-07-24
status: summarized
---

# 프로젝트의 성격

`claw`라는 CLI 코딩 에이전트 하네스를 공개한 Rust 프로젝트다. 저장소가 `instructkr`에서 `ultraworkers`로 이동했다. 핵심은 기능 자체보다 “에이전트가 에이전트용 도구를 계속 유지하면 어떤 결과가 생기는가”를 관찰하는 데 있다. README도 이를 진지한 프로덕션 도구가 아닌 agent-managed museum exhibit라고 명시하며, 실제 업무에는 LazyCodex나 Gajae-Code를 권한다.

실행의 기준 구현은 `rust/`에 있고 Python 코드는 동반 참고 작업공간에 가깝다. 공개 저장소가 자동화된 유지보수 실험의 기록 역할을 하므로, 일반 제품처럼 안정된 로드맵이나 호환성을 기대하기보다 커밋과 에이전트 의사결정의 흔적을 살펴보는 자료로 읽는 편이 맞다.

# 설치와 기능상 함정

`cargo install claw-code`는 이름이 비슷한 오래된 다른 stub을 설치한다. 현재 저장소는 소스에서 빌드하거나 upstream binary 이름인 `agent-code`를 설치해야 한다. ACP/Zed daemon도 구현된 상태가 아니며 `claw acp serve`는 상태 확인과 발견성을 위한 alias일 뿐 실제 서버를 띄우지 않는다.

따라서 이름이나 명령만 보고 완성된 IDE 통합을 기대하면 안 된다. 자동으로 생성·수정된 코드는 사람이 소유권, 보안과 회귀를 검토해야 하고, 프로젝트가 스스로 밝힌 실험적 지위를 그대로 받아들여야 한다. 라이선스는 MIT다.

# 읽을 가치

장기 실행 에이전트가 자기 도구를 관리할 때 문서, 릴리스, 명명과 실제 동작이 어떻게 어긋날 수 있는지 보여준다. “자율 유지보수”는 유지비를 없애는 것이 아니라 검증 기준과 인간의 책임 범위를 새로 설계하는 문제라는 점이 핵심이다.

# 출처

- [Claw Code 저장소](https://github.com/ultraworkers/claw-code)
