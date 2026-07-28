---
type: Command Note
title: "gws: Google Workspace 통합 CLI"
description: "Drive, Gmail, Calendar 등 Google Workspace API를 한 CLI와 구조화된 JSON 출력으로 다루는 도구"
resource: https://news.hada.io/topic?id=27209
notion: https://app.notion.com/p/73d1a73cf20b835d8ecf0165c4577c55
tags: [reading, cli, google-workspace, automation]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`gws`는 Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin 등 Google Workspace 서비스를 하나의 명령줄 인터페이스에서 다루는 도구다. 사람의 대화형 사용뿐 아니라 에이전트와 자동화 파이프라인이 읽기 쉬운 JSON 입출력을 지향한다.

# 특징

- Google Discovery Service를 읽어 명령을 동적으로 구성하므로 새 API 엔드포인트를 비교적 빠르게 반영한다.
- 100개가 넘는 에이전트 스킬과 구조화된 JSON 출력을 제공한다.
- 사용자 OAuth, 서비스 계정, CI 환경 인증을 지원한다.
- 응답 보안을 위해 Google Model Armor와 연결할 수 있다.

# 활용 예

캘린더 일정 조회, Drive 파일 탐색, Gmail 검색, Sheets 데이터 수정처럼 여러 Workspace API를 오가는 작업을 하나의 자동화 흐름으로 묶을 수 있다. 에이전트가 실행할 때는 사람이 쓰는 계정 전체를 넘기지 말고 작업별 최소 권한, 별도 서비스 계정, 쓰기 작업의 승인 경계를 먼저 설계해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27209)
- [googleworkspace/cli](https://github.com/googleworkspace/cli)

