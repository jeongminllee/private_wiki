---
type: Concept
title: "CodeSpeak: 코드를 생성물로 두는 명세 중심 AI 프로그래밍"
description: "자연어에 가까운 specification을 유지하고 변경분으로 구현 code를 생성·검증하는 Kotlin 창시자의 실험적 도구"
resource: "https://news.hada.io/topic?id=27476"
notion: "https://app.notion.com/p/13d1a73cf20b82c8bb9381c9be3e12a4"
tags: [reading, ai-coding, specification, code-generation]
timestamp: 2026-07-24
status: summarized
---

# 개념

CodeSpeak는 개발자가 generated code보다 specification을 주요 편집 대상으로 삼게 한다. `codespeak build`가 spec diff를 해석해 code diff를 만들며, 직접 작성한 code와 생성된 code를 한 project에서 섞을 수 있다. 기존 code를 spec으로 흡수하는 takeover workflow도 계획돼 있다.

# 보고된 사례

Project는 yt-dlp 일부를 255줄 spec 38줄, Faker 165줄을 21줄, Beautiful Soup 826줄을 141줄, markitdown 139줄을 14줄로 표현하며 약 5~10배 축약을 주장한다. 기존 test를 유지하거나 보강해 생성 결과의 동작을 확인했다고 설명한다.

# 실무적 의미

이를 deterministic programming language라기보다 specification과 구현 사이를 AI가 번역하는 workflow로 보는 편이 정확하다. Spec은 의도와 제약을 담고 test와 formal invariant는 실행 가능한 계약 역할을 해야 한다. 생성 결과도 code review, security scan과 reproducible build 대상이다.

# 한계

행동을 빠짐없이 적다 보면 specification이 다시 code만큼 복잡해지는 역설이 생길 수 있다. Model update에 따른 비결정성, spec-code drift, 작은 수정마다 다시 생성해야 하는 비용도 검증해야 한다. 줄 수 감소는 유지보수성이나 결함률 향상을 직접 증명하지 않는다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27476)
