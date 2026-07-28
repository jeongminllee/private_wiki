---
type: Study Note
title: "Claude Code 실전 팁 70가지 한국어 가이드"
description: "설정·context·Git·MCP·hook·sandbox·검증 workflow를 한데 모은 54쪽 분량의 2차 편집 자료"
resource: "https://news.hada.io/topic?id=26526"
notion: "https://app.notion.com/p/02e1a73cf20b82ee9ff4013e06839ef2"
tags: [reading, claude-code, guide, ai-coding]
timestamp: 2026-07-24
status: summarized
---

# 구성

54쪽 PDF는 ykdojo의 tips repository와 Ado Kukic의 `Advent of Claude`를 한국어로 번역·재구성한 70개 팁 모음이다. Mindset와 문제 분해, `CLAUDE.md`와 session 설정, context 관리, Git·worktree·review, MCP·hook·skill·agent·plugin, headless 실행과 최적화, container·sandbox, browser·Playwright, TDD와 output verification, SDK·team과 학습 roadmap을 13개 부분으로 다룬다.

# 재사용할 원칙

복잡한 작업은 plan을 먼저 만들고, context가 흐려지기 전에 compaction과 상태 기록을 한다. Worktree로 병렬 변경을 분리하고 formatting·lint는 deterministic hook에 둔다. 위험 작업은 sandbox와 permission audit로 통제한다. 생성된 code는 test, browser 또는 실제 output으로 검증하는 loop를 갖춘다.

# 읽는 방법

70가지를 전부 적용하기보다 현재 반복되는 마찰 한두 개를 골라 project 규칙으로 시험한다. 효과와 부작용을 기록한 뒤 유지할 tip만 `CLAUDE.md`나 skill로 승격한다.

# 주의

이 문서는 공식 manual이 아니라 여러 자료를 합친 secondary compilation이다. PDF 날짜에는 원 출처 시점과 맞지 않는 2025년 1월 표기가 있어 생성·편집 과정의 typo 가능성이 지적됐다. Command, product 기능과 권한 방식은 빠르게 바뀌므로 최신 공식 문서 및 원 출처와 대조한다.

# 출처

- [GeekNews 소개 및 PDF](https://news.hada.io/topic?id=26526)
