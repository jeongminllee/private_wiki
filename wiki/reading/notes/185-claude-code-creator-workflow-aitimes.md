---
type: Reference
title: "Claude Code 제작자가 공개한 실제 사용 방식"
description: "Boris Cherny의 병렬 세션, 공유 지침, 계획과 검증 중심 Claude Code workflow를 전한 기사"
resource: https://www.aitimes.com/news/articleView.html?idxno=205321
notion: https://app.notion.com/p/5571a73cf20b828b85fe01c800292423
tags: [reading, claude-code, workflow, ai-agents]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

AI타임스가 Claude Code 개발 책임자 Boris Cherny의 공개 글을 소개한 기사다. 핵심은 하나의 긴 채팅에 모든 일을 맡기는 것이 아니라 작업을 병렬 세션으로 나누고, 팀 지침과 계획, 검증 루틴을 반복 가능한 개발 과정으로 만드는 것이다.

# 공개된 사용 방식

- 로컬과 웹 세션을 여러 개 열어 독립 과제를 병렬로 진행한다.
- 저장소의 `CLAUDE.md`에 빌드·테스트 명령과 반복 실수를 기록해 팀이 공유한다.
- 복잡한 작업은 Plan 단계에서 범위와 접근을 다듬은 뒤 실행한다.
- 반복 업무는 명령과 스킬로 만들고, 조사·구현·검토 역할을 분리한다.
- 결과를 그대로 믿지 않고 테스트, diff 검토, 정리 단계를 거친다.

# 해석

도구 제작자의 개인 workflow는 유용한 사례지만 모든 팀의 정답은 아니다. 병렬 세션을 늘리기 전에 파일 소유 범위, 비용 상한, 통합 시점, 실패 처리 방법을 정해야 실제 생산성 향상으로 이어진다.

# 관련 문서

- [GN#340: Claude Code를 만든 사람의 사용법](175-geeknews-340-claude-code-creator-workflow.md)

# 출처

- [AI타임스 기사](https://www.aitimes.com/news/articleView.html?idxno=205321)

