---
type: Reference
title: "CMDS System Files v4.9.5 기술 문서"
description: "핵심 파일 6개, shared rule 8개, slash command와 필수 metadata를 탐색 가능한 형태로 공개한 공식 문서"
resource: "https://system.cmdspace.work/docs"
notion: "https://app.notion.com/p/9ac1a73cf20b8229bbed81cab98b8702"
tags: [reading, knowledge-management, documentation, obsidian, cmds]
timestamp: 2026-07-24
status: summarized
---

# 문서 구성

이 페이지는 CMDS의 overview를 넘어 각 system file과 shared rule을 직접 읽는 reference다. v4.9.5 기준 핵심 file 6개, shared rule 8개, slash command 8개, architecture pattern 9개와 note 필수 property 7개를 안내한다.

AI 문서는 `CLAUDE.md`, `AGENTS.md`, `CMDS.md`, 인간 중심 문서는 Guide와 Head Quarter, visual output용 문서는 `DESIGN.md`로 분리된다. Shared rule은 indentation, frontmatter, file creation, wikilink, blank line, directory, Mermaid와 video project처럼 한 파일에 한 concern을 둔다.

# 재사용할 점

전체 규칙을 거대한 prompt 하나로 만들지 않고 audience와 변화 주기별로 나눈다. 공통 rule은 단일 원천에서 include하고, 문서마다 precedence와 적용 대상을 명시한다. Frontmatter description은 사람의 설명인 동시에 LLM retrieval hint가 된다.

# 주의

CMDS의 directory 번호와 property를 그대로 복사하기보다 현재 wiki의 목적과 규모에 맞게 변형한다. 문서에서 `Loading…`으로 표시되는 부분은 client-side fetch가 필요할 수 있으므로 실제 source repository의 같은 version과 대조한다.

# 관련 문서

- [공식 홈페이지 개요](350-cmds-system-files-home.md)
- [CMDS 저장소 중심 정리](301-cmds-system-files-knowledge-architecture.md)

# 출처

- [CMDS v4.9.5 Docs](https://system.cmdspace.work/docs)
