---
type: Reference
title: "Canine Remotion Slide: Markdown 기반 발표·영상 도구"
description: "하나의 Markdown에서 presenter, 16:9 slide 영상, shorts와 PDF를 만드는 MIT 프로젝트"
resource: https://www.youtube.com/watch?v=_9VdOHhlRAk
notion: https://app.notion.com/p/2111a73cf20b82179eae01533a475486
tags: [reading, presentation, markdown, remotion, open-source]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Canine Remotion Slide는 Markdown 하나를 원본으로 browser presenter, Remotion slide 영상, 세로 shorts와 PDF를 만드는 프로젝트다. AI coding agent가 초안을 만들고 editor에서 다듬은 뒤 presenter와 영상 출력에 같은 내용을 재사용하는 workflow를 목표로 한다.

# 주요 기능

- Markdown의 제목, bullet, image와 marker를 보고 slide type을 자동 선택한다.
- title, image, split, keyword, steps, compare, quote, stat와 evolution-flow 등을 지원한다.
- `dark`, `blue`, `orange`, `yellow`, `black`, `parchment`, `figma`의 기본 theme가 있다.
- 같은 폴더의 `DESIGN.md`로 custom theme를 만들 수 있다.
- browser presenter, Remotion Studio preview, MP4, shorts와 PDF command를 제공한다.

# 기본 흐름

repository를 clone하고 `npm install`한 뒤 `markdowns/<topic>/<topic>.md`를 만든다. `npm run slides:present -- <file>`로 빠르게 확인하고, 내용과 이미지 경로를 다듬은 뒤 render 또는 PDF command를 실행한다. 내장 agent skill은 초안 생성과 slide type 변경에 활용할 수 있다.

# 주의할 점

Markdown이 source of truth라도 layout, 긴 텍스트, font와 asset license는 실제 desktop·projector·video에서 확인해야 한다. AI가 만든 발표문과 시각 자료는 사실성, 저작권과 읽기 속도를 사람이 검토한다. 저장소는 MIT License다.

# 출처

- [YouTube 발표 영상](https://www.youtube.com/watch?v=_9VdOHhlRAk)
- [GitHub 저장소와 사용법](https://github.com/Canine89/canine-remotion-slide)
- [Notion 원본 항목](https://app.notion.com/p/2111a73cf20b82179eae01533a475486)
