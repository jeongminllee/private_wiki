---
type: Study Note
title: "Boris Cherny의 복리형 Claude Code 개발 workflow"
description: "병렬 session, CLAUDE.md, slash command, subagent와 자동 검증을 연결해 팀 지식을 누적하는 초기 workflow"
resource: "https://news.hada.io/topic?id=25570"
notion: "https://app.notion.com/p/3b51a73cf20b8305b78681c39f064c2e"
tags: [reading, claude-code, workflow, verification]
timestamp: 2026-07-24
status: summarized
---

# 운영 방식

작성자는 local terminal에서 약 5개, web에서 5~10개의 Claude session을 병렬로 사용하고 notification과 handoff로 상태를 관리한다. Plan mode에서 방향을 검토한 뒤 편집을 진행하고, 팀의 `CLAUDE.md`에는 실수와 PR feedback에서 얻은 규칙을 계속 추가한다.

반복 과정은 `/commit-push-pr` 같은 repository의 slash command로 고정한다. Code simplification과 application verification은 subagent에 맡기고, `PostToolUse` hook으로 formatting 같은 deterministic 작업을 실행한다. Slack, BigQuery와 Sentry를 연결해 agent가 실제 evidence를 조회하게 한다.

# 가장 중요한 원칙

Agent에게 결과를 스스로 확인할 feedback loop를 준다. Test, browser, simulator나 비교 가능한 output이 있어야 생성과 검증을 반복할 수 있다. 작성자는 이런 loop가 품질을 2~3배 높였다고 체감하지만 이는 개인 경험치이며 독립 benchmark가 아니다.

# 권한과 장기 작업

일반 환경에서 무조건 permission check를 건너뛰지 않고 알려진 command만 allowlist에 둔다. 격리 sandbox의 장기 작업에는 background verifier, Stop hook이나 반복 loop를 사용할 수 있다. 자동화가 길어질수록 비용 상한, timeout과 rollback 조건이 필요하다.

# 관련 문서

- [Boris Cherny의 Claude Code 실전 팁 10가지](337-boris-claude-code-practical-tips.md)

# 출처

- [GeekNews 요약](https://news.hada.io/topic?id=25570)
