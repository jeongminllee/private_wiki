---
type: Reference
title: "출판 에디터의 Claude Code·Obsidian·Zotero 자동화"
description: "로컬 노트와 서지 자료를 연결해 뉴스·논문 수집을 자동화한 비개발 직군 사례"
resource: https://yozm.wishket.com/magazine/detail/3555/
notion: https://app.notion.com/p/e4e1a73cf20b83c3a27e01937fab31d5
tags: [reading, claude-code, obsidian, zotero, workflow-automation]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

컴퓨터 전공 기초가 있는 출판 에디터가 terminal 기반 Claude Code를 편집 업무에 적용한 사례다. local Markdown을 쓰는 Obsidian은 agent가 파일을 직접 읽고 수정하기 쉬웠고, Zotero는 MCP로 연결해 논문 metadata와 자료를 노트 흐름에 가져왔다.

# 만든 흐름

1. 뉴스 수집과 요약 command를 만들고 지정한 Obsidian 경로에 Markdown으로 저장한다.
2. `cron`으로 매일 아침 실행해 읽을 자료를 자동 축적한다.
3. Zotero MCP에서 논문 자료를 읽어 요약하고 Obsidian note와 연결한다.
4. 사람이 빠진 정보, 잘못된 인용과 문체를 마지막에 검토한다.

# 이 wiki에 적용할 점

원문과 생성된 wiki note를 분리하고 source URL, 확인일과 실패 상태를 frontmatter에 남긴다. 자동 ingest는 inbox까지만 맡기고, 중요한 요약과 기존 문서 통합은 사람 또는 별도 review 단계가 승인한다. file write 범위와 MCP permission도 필요한 vault·collection으로 제한한다.

# 한계

글은 짧은 세미나 요약이자 전자책 소개이며 비용·오류율·장기 유지보수 수치는 없다. 자동 실행은 편리하지만 오래된 prompt, 중복 자료와 잘못된 요약을 매일 누적할 수 있어 monitoring과 deduplication이 필요하다.

# 출처

- [요즘IT 원문](https://yozm.wishket.com/magazine/detail/3555/)
- [Notion 원본 항목](https://app.notion.com/p/e4e1a73cf20b83c3a27e01937fab31d5)
