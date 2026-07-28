---
type: Reference
title: "GN#340: Claude Code를 만든 사람의 사용법"
description: "병렬 세션, 공유 지침, 계획과 검증 루틴을 중심으로 정리한 Claude Code 작업 방식"
resource: https://news.hada.io/weekly/202602
notion: https://app.notion.com/p/2381a73cf20b8216aade01c097ece057
tags: [reading, newsletter, claude-code, workflow]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

2026년 1월 5일부터 11일까지의 GeekNews 위클리다. 중심 글은 Claude Code를 이끄는 Boris Cherny가 공개한 실제 사용 방식이며, AI 코딩 도구를 한 번의 대화가 아니라 병렬 작업과 검증 시스템으로 운영하는 방법을 보여준다.

# 작업 방식

- 로컬과 웹에서 5~10개 세션을 병렬로 운영하되 작업 단위를 분리한다.
- 팀이 `CLAUDE.md`를 공유해 반복되는 실수와 저장소 규칙을 명시한다.
- Plan 단계에서 구현 방향을 충분히 다듬은 다음 실행 범위를 넓힌다.
- 반복 작업은 slash command로 만들고, 독립 조사와 검토는 subagent에 맡긴다.
- 구현, 검증, 정리 루틴을 분리해 결과를 다시 확인한다.

# 이동 중 작업

같은 호에서는 스마트폰에서 원격으로 Claude Code를 쓰는 두 방식도 비교한다. 하나는 전용 VM, 알림, 비동기 작업을 포함한 환경이고 다른 하나는 항상 켜진 개인 컴퓨터에 Tailscale로 접속하는 가벼운 방식이다. 편의성만큼 계정 인증, 비밀정보, 원격 명령 권한을 좁히는 일이 중요하다.

# 적용할 점

병렬 세션 수 자체가 생산성을 보장하지 않는다. 파일 소유 범위와 완료 조건을 먼저 나누고, 공통 검증 명령과 Git diff를 마지막 합류 지점으로 두어야 충돌과 중복 작업을 줄일 수 있다.

# 출처

- [GeekNews Weekly GN#340](https://news.hada.io/weekly/202602)

