---
type: Reference
title: "Claude Code용 community skill·plugin 7선"
description: "계획, memory, 도구 탐색, UI, Obsidian, n8n과 project workflow를 보완하는 community 확장 목록"
resource: "https://generativeai.pub/7-claude-code-skills-every-developer-needs-in-2026-52b15ae68685?gi=89602564636c"
notion: "https://app.notion.com/p/2021a73cf20b8390991681c4765149c6"
tags: [reading, claude-code, skills, plugin, security]
timestamp: 2026-07-24
status: summarized
---

# 소개된 도구

- `Superpowers`: brainstorming, plan, TDD와 review 순서를 강제하는 workflow
- `Claude Mem`: session에서 얻은 context와 결정을 압축해 다음 session에 재주입
- `Awesome Claude Code`: skill, plugin, hook와 tool을 찾는 curated directory
- `UI/UX Pro Max`: frontend style·palette·typography reference를 제공하는 skill
- `Obsidian Skills`: WikiLink, Canvas와 Bases 등 Obsidian 형식을 다루는 지침
- `n8n-MCP`: n8n node schema와 parameter를 MCP로 조회
- `GSD`: 질문, research, requirement, roadmap와 subagent 실행을 단계화

# 목록을 쓰는 법

이 일곱 항목은 모두 같은 종류의 “skill”이 아니다. Plugin, memory service, directory, MCP server와 workflow package가 섞여 있다. 먼저 현재 문제가 context 손실인지, planning 부재인지, domain schema 부족인지 확인하고 하나씩 도입해야 효과와 부작용을 분리할 수 있다.

# 보안과 검증

Community 확장은 prompt와 command, local file 또는 network access를 포함할 수 있다. Star 수는 안전성이나 유지보수의 보증이 아니다. Install 전에 source와 manifest를 읽고 version을 고정하며, 필요한 directory와 command만 허용한다. Memory tool에는 secret과 개인정보가 장기 저장되지 않는지도 확인한다.

Article의 star 수, install command와 제품 호환성은 2026년 3월의 snapshot이다. 실행 전 각 repository의 최신 README와 Claude Code 공식 extension 방식을 다시 확인해야 한다.

# 출처

- [저장된 Medium article](https://generativeai.pub/7-claude-code-skills-every-developer-needs-in-2026-52b15ae68685?gi=89602564636c)
- [공개 mirror](https://www.hubwiz.com/blog/top7-claude-code-skills-for-developers/)
