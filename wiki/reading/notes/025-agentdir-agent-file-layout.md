---
type: Reference
title: "agentdir: 원본과 에이전트용 파일 구조 분리하기"
description: "원본 파일을 옮기지 않고 작업 목적에 맞는 읽기 전용 가상 트리를 만들어 에이전트의 탐색 비용과 수정 위험을 줄이는 도구"
resource: https://tech.brain-crew.com/engineering/agentdir-agent-file-layout
notion: https://app.notion.com/p/38a1a73cf20b81058d35f67182cf618a
tags: [reading, ai-agent, filesystem, context-engineering]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

사람이 익숙한 폴더 구조와 에이전트가 일하기 좋은 구조는 다를 수 있다. `agentdir`는 원본을 실제로 이동하거나 이름을 바꾸지 않고, 작업에 필요한 파일만 목적 중심으로 재배치한 별도의 가상 파일 트리를 만든다. 가상 뷰를 읽기 전용으로 제공해 탐색 잡음과 우발적 원본 수정을 줄이는 것이 핵심이다.

# 동작 방식

- `Catalog`가 가상 경로와 실제 원본 경로의 매핑을 관리한다.
- `Materializer`가 reflink, hardlink, symlink, 일반 복사 중 환경에 맞는 전략으로 뷰를 만든다.
- APFS, Btrfs, XFS처럼 CoW를 지원하는 파일시스템에서는 같은 대용량 파일을 여러 레이아웃에 보여도 블록을 공유해 추가 공간을 줄일 수 있다.
- materialize된 파일은 일반적으로 `0o444`, Windows에서는 읽기 전용 속성으로 설정된다. 단, symlink 전략은 같은 보장을 하지 않는다.
- `Reconciler`는 기본적으로 수정 시간과 크기를 비교하고, 필요하면 SHA-256 검증으로 원본 변경을 반영한다.
- 상태 파일은 임시 파일 작성, `fsync`, 이름 변경 순서로 갱신해 중간에 깨진 manifest가 남을 가능성을 낮춘다.

글의 소규모 APFS 데모에서는 300MB 데이터셋을 다섯 레이아웃에 노출하면서 reflink를 사용해 실제 추가 디스크를 거의 쓰지 않았고, 뷰 경로 쓰기와 스냅샷 변경 전파가 차단되는 것을 확인했다. 이는 제한된 데모 결과이며 실제 에이전트의 토큰 절감이나 동시 실행 안전성까지 증명한 것은 아니다.

# 어디에 유용한가

문서, PDF, 이미지, 고객 자료, 데이터셋처럼 원본 보존이 중요한 작업에서 특히 유용하다. 예를 들어 이 wiki의 `raw/`는 그대로 두고, 특정 OCR 교정 작업에 필요한 페이지만 `workspace/reference`, `workspace/target`, `workspace/check`처럼 노출할 수 있다. 에이전트가 전체 저장소를 뒤지는 대신 작업에 필요한 경로부터 보게 하는 컨텍스트 설계 도구다.

# 한계와 안전성

읽기 전용 보장은 가상 뷰에만 적용된다. 에이전트가 원본 절대 경로에도 접근할 수 있다면 별도 sandbox와 권한 제한이 필요하다. NTFS나 ext4 등 reflink가 작동하지 않는 환경에서는 일반 복사로 폴백해 디스크 이점이 사라질 수 있다. 이 도구는 검색, 파싱, 인덱싱, 최적 레이아웃 결정을 대신하지 않는다.

# 출처

- [Braincrew Tech 소개 및 검증 글](https://tech.brain-crew.com/engineering/agentdir-agent-file-layout)
- [NomaDamas/agentdir](https://github.com/NomaDamas/agentdir)

