---
type: Reference
title: "9개 Claude 역할로 구성한 소프트웨어 개발 시스템"
description: "요구 분석부터 문서화까지 전문 agent를 tmux와 file IPC로 연결한 공개 multi-agent prototype"
resource: "https://news.hada.io/topic?id=26013"
notion: "https://app.notion.com/p/4bb1a73cf20b821fa58b8137c08d81ae"
tags: [reading, multi-agent, claude-code, software-engineering, prototype]
timestamp: 2026-07-24
status: summarized
---

# 구조

`Claude-Multi-Agent-System`은 orchestrator 아래에 requirement analyst, UX designer, tech architect, planner, test designer, developer, reviewer와 documenter를 둔다. 각 역할은 독립 tmux session의 Claude Code로 실행되고 file-based IPC signal로 상태를 전달한다.

Workflow는 요구 분석, 설계, 계획, test 작성, 구현, review와 문서화를 순서대로 거친다. Terminal과 web dashboard mode가 있고 agent별 model도 설정할 수 있다. TDD 단계와 별도 reviewer를 구조에 포함한 점은 한 context에서 모든 일을 처리할 때 생기는 역할 혼선을 줄이려는 시도다.

# 한계와 위험

역할 수가 많다고 독립적인 전문성이 생기지는 않는다. 같은 model과 비슷한 prompt를 쓰면 오류가 여러 단계에서 그대로 승인될 수 있고, orchestrator의 요약 과정에서 중요한 맥락이 사라질 수 있다. 토론에서도 생성량이 사람이 따라갈 수 있는 review 속도를 넘어서는 문제가 지적됐다.

Repository는 release가 없는 초기 prototype이며 성능·비용 benchmark가 없다. Auto mode는 `--dangerously-skip-permissions`로 file 생성·수정·삭제와 command를 승인 없이 수행하므로 격리된 disposable workspace에서만 시험해야 한다. 가격과 plan 추천도 저장 당시 정보일 뿐 현재 subscription 조건을 보장하지 않는다.

# 출처

- [GeekNews 소개와 토론](https://news.hada.io/topic?id=26013)
- [GitHub repository](https://github.com/Kuneosu/Claude-Multi-Agent-System)
