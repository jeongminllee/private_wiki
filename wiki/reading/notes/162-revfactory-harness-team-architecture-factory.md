---
type: Reference
title: "Harness: Claude Code 팀 아키텍처 생성기"
description: "도메인 설명에서 에이전트와 스킬로 구성된 Claude Code 하네스를 생성하고 검증하는 프로젝트"
resource: https://github.com/revfactory/harness/blob/main/README_KO.md
notion: https://app.notion.com/p/bc21a73cf20b827daa5b01071e59591e
tags: [reading, ai-agents, harness, claude-code]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Harness는 업무 도메인을 설명하면 `.claude/agents/`와 `.claude/skills/`로 구성된 에이전트 팀 아키텍처를 만들어 주는 오픈소스 프로젝트다. 한 번의 프롬프트보다 역할, 전달 형식, 검증 절차를 반복 가능한 실행 구조로 만드는 데 초점을 둔다.

# 지원하는 협업 패턴

- **Pipeline**: 앞 단계의 결과를 다음 단계가 이어받는다.
- **Fan-out/Fan-in**: 여러 에이전트가 병렬 조사한 결과를 하나로 합친다.
- **Expert pool**: 문제에 맞는 전문가 역할을 선택한다.
- **Generator-verifier**: 생성과 검증을 분리한다.
- **Supervisor**: 관리 에이전트가 작업 배정과 결과 통합을 맡는다.
- **Hierarchical delegation**: 여러 단계의 위임 구조를 만든다.

# 생성과 검증

도메인 분석, 아키텍처 선택, 에이전트·스킬 생성, 오케스트레이션, 검증 순서로 진행한다. 스킬은 필요한 순간에만 상세 지침을 읽는 progressive disclosure를 사용하며, trigger 검사와 dry run, 스킬 적용 전후 비교 테스트를 지원한다. `/harness:evolve`는 초기 하네스와 실제 완료 상태의 차이를 다음 버전에 반영한다.

# 평가할 때 주의할 점

저자는 15개 과제의 자체 A/B 평가에서 점수가 49.5에서 79.3으로 올랐다고 보고한다. 흥미로운 신호지만 독립 평가가 아니고 표본도 작으므로 일반적인 성능 향상으로 단정할 수 없다. 현재 공식 실행 환경도 Claude Code에 한정된다.

# 관련 문서

- [HarnessX](036-harnessx-agent-harness-foundry.md)
- [oh-my-claude-sisyphus](151-oh-my-claude-sisyphus.md)
- [oh-my-agent](152-oh-my-agent-process-harness.md)

# 출처

- [revfactory/harness README 한국어판](https://github.com/revfactory/harness/blob/main/README_KO.md)
