---
type: Reference
title: "oh-my-claude-sisyphus 멀티 에이전트 오케스트레이션"
description: "Claude Code에서 계획·구현·검증을 전문 역할로 나누고 완료까지 반복하는 에이전트 하네스"
resource: https://discuss.pytorch.kr/t/oh-my-claude-sisyphus-ai-claude-code-feat-oh-my-opencode/8642
notion: https://app.notion.com/p/7791a73cf20b83e8a93801f8e7ffe559
tags: [reading, ai-agents, claude-code, orchestration]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`oh-my-claude-sisyphus`는 Claude Code 위에서 여러 전문 에이전트를 조율해 요구사항 분석부터 구현, 테스트, 검토까지 반복 수행하도록 만든 오케스트레이션 프로젝트다. `oh-my-opencode`의 역할 분담과 완료 지향 루프를 Claude Code 환경에 옮기는 것이 목표다.

# 구성

- 기획: 요구사항을 구체화하고 계획의 허점을 검토한다.
- 실행: 아키텍처, 구현, 프런트엔드 작업 등을 담당한다.
- 지원: 코드 탐색, 공식 문서 조사, 문서화, 이미지 분석을 맡는다.
- 조정: 전체 작업을 나누고 상태와 검증 결과를 추적한다.

`/plan`, `/review`, `/deepsearch`, `/orchestrator`, `/ultrawork`처럼 행동 모드를 명시하는 명령을 제공한다. LSP와 AST 기반 검색을 활용해 단순 문자열 검색보다 구조적인 코드 변경을 지향한다.

# 배울 점

좋은 멀티 에이전트 시스템의 핵심은 역할 이름이 아니라 책임 범위, 완료 조건, 검증 루프다. 작은 작업에서는 조정 비용이 더 클 수 있으므로 복잡도에 따라 역할 수와 검토 단계를 줄여야 한다.

# 주의

이 문서는 커뮤니티의 프로젝트 소개 글을 바탕으로 한다. 설치 전 저장소의 현재 유지보수 상태, 실행되는 훅과 셸 명령, 외부 서비스로 전송되는 코드 범위, 라이선스를 직접 확인해야 한다.

# 관련 문서

- [에이전트 하네스와 반복 검증](20-agent-harness-loop-engineering.md)
- [Agentic Engineering Patterns](102-agentic-engineering-patterns.md)

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/oh-my-claude-sisyphus-ai-claude-code-feat-oh-my-opencode/8642)

