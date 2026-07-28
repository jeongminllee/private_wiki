---
type: Paper Note
title: "PaperOrchestra: 실험 자료에서 학회 논문 초안까지"
description: "문헌 조사·시각화·section 작성·검토 agent를 조율해 비정형 연구 자료를 LaTeX 원고로 바꾸는 framework"
resource: https://yiwen-song.github.io/paper_orchestra/
notion: https://app.notion.com/p/5161a73cf20b83fa97ae01d45abbace4
tags: [reading, paper, ai-agents, scientific-writing]
timestamp: 2026-07-24
status: summarized
---

# 문제

기존 autonomous scientist는 특정 실험 pipeline에 강하게 묶이거나 문헌 조사가 피상적이다. PaperOrchestra는 sparse idea summary와 raw experimental log처럼 형식이 일정하지 않은 자료를 입력받아 venue template에 맞는 full manuscript를 작성하는 문제를 분리해 다룬다.

# 방법

Outline Agent가 구조를 만들고 Plotting Agent가 figure를 생성한다. Literature Review Agent는 web에서 후보를 찾은 뒤 Semantic Scholar API로 실제 존재와 관련성을 확인해 citation graph를 만든다. Section Writing Agent가 LaTeX 본문을 쓰고 Content Refinement Agent가 simulated review로 반복 수정한다.

# 평가

PaperWritingBench는 CVPR 2025와 ICLR 2025 논문 각 100편에서 idea summary, 숫자 중심 experimental log, template과 guideline을 역구성한 200개 사례다. 11명의 AI 연구자가 blind side-by-side로 평가했으며, 연구진은 baseline 대비 literature review에서 50~68%p, 전체 원고에서 14~38%p의 win-rate margin을 보고한다. 사람 원고와는 여전히 품질 차이가 남았다.

# 한계

API로 citation 존재를 확인하는 것과 인용이 주장에 적합한지는 다르다. benchmark도 이미 완성된 성공 논문에서 원재료를 역구성했으므로 실패한 연구 기록이나 불완전한 실험에 대한 일반화는 제한적이다. 최종 사실성, 독창성, 저자 자격과 연구 윤리는 사람이 책임져야 한다.

# 출처

- [PaperOrchestra project](https://yiwen-song.github.io/paper_orchestra/)

