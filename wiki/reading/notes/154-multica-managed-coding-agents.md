---
type: Reference
title: "multica: 코딩 에이전트를 팀원처럼 운영하는 관리 플랫폼"
description: "여러 코딩 에이전트 CLI에 태스크를 할당하고 상태·블로커·재사용 스킬을 한곳에서 관리"
resource: https://news.hada.io/topic?id=28399
notion: https://app.notion.com/p/7e11a73cf20b834e9d5b01550bab0007
tags: [reading, ai-agents, project-management, self-hosting]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`multica`는 사람에게 이슈를 배정하듯 코딩 에이전트에 태스크를 할당하고, 진행 상태와 블로커를 대시보드에서 추적하는 관리형 에이전트 플랫폼이다. Claude Code, Codex, OpenCode 등의 CLI를 하나의 운영 화면에 묶는 데 초점을 둔다.

# 주요 기능

- 태스크의 대기, 할당, 시작, 완료·실패 생명주기를 관리한다.
- 실행 로그와 상태 업데이트를 WebSocket으로 실시간 표시한다.
- 배포, 마이그레이션, 코드 리뷰 절차를 재사용 가능한 팀 스킬로 축적한다.
- 워크스페이스별로 에이전트, 이슈, 설정을 격리한다.
- Docker Compose 기반 셀프호스팅을 지원한다.

# 평가 기준

도입 전에는 에이전트가 실제로 어느 권한으로 명령을 실행하는지, 비밀값을 어떻게 격리하는지, 작업 취소와 롤백이 가능한지, 실패 로그가 충분히 남는지를 확인해야 한다. 대시보드가 있어도 코드 검토와 CI를 대신하지는 않는다.

# 관련 문서

- [HarnessX](036-harnessx-agent-harness-foundry.md)
- [에이전트 하네스와 반복 검증](20-agent-harness-loop-engineering.md)

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=28399)
- [multica GitHub](https://github.com/multica-ai/multica)

