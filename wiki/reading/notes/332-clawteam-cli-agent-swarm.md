---
type: Project
title: "ClawTeam: CLI와 Git worktree 기반 agent swarm"
description: "별도 queue infrastructure 없이 leader와 worker agent를 조직해 병렬 작업하는 open-source orchestration"
resource: "https://news.hada.io/topic?id=27609"
notion: "https://app.notion.com/p/5861a73cf20b8363b7b101fc1d061461"
tags: [reading, multi-agent, orchestration, git-worktree, open-source]
timestamp: 2026-07-24
status: summarized
---

# 구조

HKUDS의 ClawTeam은 leader agent가 worker를 생성하고 역할과 작업을 나누는 multi-agent orchestration project다. Agent끼리 직접 message를 보내고 leader가 progress를 관찰해 전략을 바꿀 수 있다. CLI, filesystem, tmux와 Git worktree를 이용해 Redis 같은 별도 queue infrastructure 없이 실행하는 것이 특징이다.

# 제시된 활용

Project는 GPU 8개와 agent 8개로 2,000회 이상의 ML experiment를 수행한 사례, frontend·backend·test 역할을 나눈 full-stack 개발, 투자·데이터 분석 사례를 제시한다. Worktree는 code 변경 영역을 분리하고, task graph와 message는 coordination을 돕는다.

# 운영 원칙

Agent마다 소유 file과 acceptance criteria를 명시하고 shared file 수정은 순서를 정한다. Leader가 단순 진행률뿐 아니라 test result, artifact와 merge conflict를 확인해야 한다. 비용·token·실행 시간을 agent별로 측정하고 병렬화 이득이 없는 작업은 단일 agent로 돌린다.

# 한계

Agent 수가 늘면 중복 조사, 충돌, 잘못된 공유 상태와 검토 비용도 증가한다. 소개된 대규모 수치는 project 측 사례이지 일반 성능 보장이 아니다. 동일 benchmark를 단일 agent와 비교하고 최종 산출물은 사람이 review해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27609)
