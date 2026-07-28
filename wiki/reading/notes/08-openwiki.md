---
type: Reference
title: OpenWiki
description: 개인 자료와 코드 저장소를 에이전트 친화적인 OKF 위키로 만드는 오픈소스 도구
resource: https://news.hada.io/topic?id=31594
notion: https://app.notion.com/p/3a31a73cf20b81a1a81cee19a1e79e55
tags: [reading, repository, knowledge-base, okf]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

OpenWiki는 로컬 저장소와 외부 지식 소스를 모아 사람과 AI 에이전트가 함께 읽을 수 있는 Markdown 위키로 변환한다. 출력이 YAML frontmatter와 Markdown 링크를 사용하는 Google OKF v0.1 번들이라는 점에서 이 저장소의 운영 방식과 매우 가깝다.

# 핵심 내용

- 개인 모드는 로컬 저장소, Gmail, Notion, 웹 검색, Hacker News, X 등의 자료를 `~/.openwiki/wiki`에 모은다.
- 코드 모드는 저장소를 분석해 `openwiki/` 아래에 구조화된 문서를 만든다.
- CI와 연결하면 코드 변화에 맞춘 문서 갱신 PR을 자동 생성할 수 있다.
- 연결된 문서를 단순 저장하지 않고 에이전트가 탐색하기 좋은 링크 구조로 만든다.

# 왜 읽을 만한가

현재 wiki의 Notion 가져오기와 가장 직접적으로 비교할 수 있는 프로젝트다. 수집, 구조화, 링크 생성, 갱신 자동화를 어디까지 도구에 맡기고 어디부터 사람이 검토할지 판단하는 기준이 된다.

# 적용 아이디어

- 별도 테스트 디렉터리에서 동일한 Notion 자료 일부를 OpenWiki로 가져와 현재 결과와 비교한다.
- 문서 제목, frontmatter, cross-link, 증분 갱신, 원문 보존 여부를 평가 항목으로 둔다.
- 자동 생성 결과를 바로 본 wiki에 합치지 말고 diff와 출처 추적을 먼저 검증한다.

# 주의할 점

Gmail과 Notion 같은 개인 소스를 연결하면 생성물에 민감 정보가 섞일 수 있다. 커넥터 권한, 로컬 저장 범위, Git 추적 여부를 먼저 확인해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=31594)
- [Notion 원본 항목](https://app.notion.com/p/3a31a73cf20b81a1a81cee19a1e79e55)
