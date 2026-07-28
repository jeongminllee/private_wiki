---
type: Reference
title: "Linus Torvalds와 DHH의 AI 코딩 사용 사례"
description: "유명 개발자들의 제한된 AI 활용을 과장된 전향 서사와 분리해 살펴본 영상"
resource: https://www.youtube.com/watch?v=75y-8iBwJsk
notion: https://app.notion.com/p/24c1a73cf20b83f794e40128393fa00b
tags: [reading, ai-coding, open-source, software-engineering]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

영상은 직접 코딩과 엄격한 코드 관리를 중시하던 Linus Torvalds와 DHH도 agentic coding을 쓰기 시작했다는 사례를 소개한다. 중요한 맥락은 두 사람이 핵심 시스템을 검토 없이 AI에 넘겼다는 뜻이 아니라, 자신에게 유용한 경계에서 도구를 채택했다는 점이다.

# Linus Torvalds 사례

Torvalds는 개인 취미 프로젝트 `AudioNoise`의 Python 시각화 도구를 Google Antigravity로 생성했다고 밝혔다. 이는 Linux kernel이나 Git의 핵심 코드를 바이브 코딩했다는 사례가 아니다. 익숙하지 않은 보조 영역에서 생성 도구를 쓰고 결과를 소유한 작은 실험으로 보는 편이 정확하다.

# DHH 사례

DHH는 editor autocomplete에는 큰 흥미가 없었지만 OpenCode에서 여러 agent를 팀처럼 사용하고, bug fix와 초안을 감독하는 경험을 긍정적으로 썼다. 직접 만드는 즐거움을 포기한다기보다 반복 작업과 탐색을 위임하고 선택·검토에 집중하는 변화다.

# 적용 메모

유명 개발자의 사용 여부는 도구의 품질 증명이 아니다. 작업의 위험도, code ownership, test와 review 능력에 따라 위임 범위를 정한다. “AI 사용”과 “생성된 코드를 이해하지 않고 배포”하는 바이브 코딩을 구분한다.

# 출처

- [YouTube 원본 영상](https://www.youtube.com/watch?v=75y-8iBwJsk)
- [DHH: Promoting AI agents](https://world.hey.com/dhh/promoting-ai-agents-3ee04945)
- [Torvalds 사례의 맥락](https://arstechnica.com/ai/2026/01/hobby-github-repo-shows-linus-torvalds-vibe-codes-sometimes/)
- [Notion 원본 항목](https://app.notion.com/p/24c1a73cf20b83f794e40128393fa00b)
