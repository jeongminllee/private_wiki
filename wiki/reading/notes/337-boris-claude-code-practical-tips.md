---
type: Study Note
title: "Boris Cherny의 Claude Code 실전 팁 10가지"
description: "병렬 worktree, 계획 검토, skill 축적, 검증 loop와 도구 연결을 중심으로 한 후속 실무 팁"
resource: "https://news.hada.io/topic?id=26330"
notion: "https://app.notion.com/p/2ac1a73cf20b839bb92801dc7b3624cb"
tags: [reading, claude-code, workflow, ai-coding]
timestamp: 2026-07-24
status: summarized
---

# 핵심 습관

1. 이름 붙인 Git worktree 3~5개로 독립 작업을 병렬화한다.
2. 복잡한 일은 plan mode에서 시작하고 다른 Claude에게 계획을 review시킨다. 진행이 어긋나면 다시 계획한다.
3. 실수와 PR review에서 얻은 규칙을 `CLAUDE.md`에 계속 반영한다.
4. 매일 반복하는 동작은 version control되는 skill이나 slash command로 만든다.
5. Slack thread, log와 CI failure를 직접 제공해 진단 근거를 넓힌다.
6. “동작함을 증명하라”, main과 feature를 비교하라는 acceptance request를 준다.
7. Status line, tmux와 notification으로 병렬 session의 context를 관리한다.
8. Subagent로 조사·검증을 분리해 main context를 보존한다.
9. BigQuery, MCP와 CLI를 통해 실제 data를 분석하게 한다.
10. 설명·diagram·spaced repetition을 요청해 작업을 학습으로 바꾼다.

# 적용 시 주의

이는 한 개발팀의 업무 방식이지 모든 project의 정답은 아니다. 병렬 session이 많아지면 비용, merge conflict와 인지 부하도 늘어난다. 권한 hook이나 command allowlist는 model의 판단만으로 자동 승인하지 말고 위험도와 실행 환경에 맞춰 제한한다.

# 관련 문서

- [Boris Cherny의 복리형 Claude Code workflow](338-boris-claude-code-compounding-workflow.md)

# 출처

- [GeekNews 요약](https://news.hada.io/topic?id=26330)
