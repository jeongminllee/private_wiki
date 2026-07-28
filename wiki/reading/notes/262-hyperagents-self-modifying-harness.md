---
type: Paper Note
title: "Hyperagents: 에이전트가 작업 방식과 개선 방식까지 수정하는 실험"
description: "DGM-H가 task agent와 meta agent를 하나의 편집 가능한 프로그램으로 묶는 이유와 한계"
resource: https://news.hada.io/topic?id=28430
resource_aliases: [https://arxiv.org/abs/2603.19461]
notion: https://app.notion.com/p/8e01a73cf20b8266a0a1012670f91599
tags: [paper, ai-agent, self-improvement, harness]
timestamp: 2026-07-24
status: summarized
---

# 문제

기존 self-improving agent는 task를 푸는 code는 바꿔도 “다음 개선안을 만드는 방법”은 사람이 고정해 두는 경우가 많다. Hyperagents는 task agent와 이를 수정하는 meta agent를 하나의 편집 가능한 program으로 합쳐, 개선 절차 자체도 개선 대상으로 만든다.

# DGM-H loop

1. 현재 agent가 task를 수행하고 평가 점수를 얻는다.
2. Meta agent가 현재 code와 과거 성능을 읽고 변형본을 만든다.
3. 변형본을 다시 평가해 archive에 보존한다.
4. Archive에서 다음 parent를 고르고 반복한다.

이 구조는 Darwin Gödel Machine을 coding 밖으로 확장한 DGM-Hyperagents(DGM-H)다. Coding, paper review, robotics reward design, Olympiad math grading 등에서 self-improvement가 없는 baseline과 prior system보다 성능이 개선됐다고 저자들은 보고한다.

# 흥미로운 관찰

반복 과정에서 persistent memory, generation별 performance tracking, checklist와 multi-stage verification, threshold rule, domain knowledge base와 retry logic가 나타났다. 이는 production agent harness에서 사람이 넣는 구성과 닮아 있다. Meta-level improvement 일부가 domain 사이에 전이된 결과도 제시된다.

# 신중하게 볼 점

이 결과가 harness architecture의 필연적 수렴을 증명하지는 않는다. Base model이 이미 공개된 agent pattern을 학습했거나 검색으로 접했다면 “독립 발명”과 pattern 재조합을 구분하기 어렵다. Evaluation contamination, 많은 반복에 든 compute, 실패 변형의 안전성과 사람이 설정한 task·metric의 영향도 확인해야 한다.

Self-modifying agent에서는 회귀 test, immutable policy boundary, sandbox와 human approval가 더 중요해진다. 개선 목표가 불완전하면 agent는 잘못된 metric을 더 효율적으로 최적화할 수 있다.

# 출처

- [GeekNews 해설](https://news.hada.io/topic?id=28430)
- [Hyperagents 논문](https://arxiv.org/abs/2603.19461)

