---
type: Reference
title: "Everything Claude Code: skills·hooks·subagents·rules를 운영 체계로 묶기"
description: "반복 workflow 자동화, context 절약과 제한된 작업 위임을 위해 Claude Code 설정을 모듈화한 실전 가이드"
resource: "https://discuss.pytorch.kr/t/everything-claude-code-anthropic-x-forum-ventures-claude-code/8740"
resource_aliases: [https://share.google/nSb6ctNt2pQMJU2qC]
notion: "https://app.notion.com/p/3d71a73cf20b83679ee1813edb003b0c"
tags: [reading, claude-code, ai-agents, developer-workflow]
timestamp: 2026-07-24
status: summarized
---

# 구성 원리

Claude Code를 매번 긴 prompt로 지시하지 않고 `~/.claude/` 아래 역할별 파일로 운영하는 방법을 정리한 글이다. `skills/`는 여러 단계의 재사용 workflow, `commands/`는 즉시 실행할 짧은 명령, `agents/`는 planner·security reviewer 같은 전문 역할, `rules/`는 항상 적용할 품질 기준, 설정 파일은 MCP와 tool 연결을 담당한다.

Hook은 lifecycle event에 자동 반응한다. `PreToolUse`에서 오래 걸리는 command를 tmux로 보내거나 push 전 review를 요구하고, `PostToolUse`에서 formatter와 type check를 실행하며, `Stop`에서 남은 debug log를 검사하는 식이다. 자동화는 model의 기억에 기대는 요청을 deterministic guardrail로 옮긴다는 데 의미가 있다.

# 컨텍스트 관리

Subagent는 좁은 역할과 제한된 도구만 받아 별도 context에서 일한다. 메인 agent가 모든 repository 세부를 들고 있지 않아도 되지만, 결과를 합치는 acceptance criteria는 메인 workflow에 남겨야 한다. MCP도 많이 등록하는 것보다 프로젝트당 필요한 5~6개만 켜고 전체 도구 수를 제한하는 방식을 권한다.

장기 작업은 tmux, 병렬 작업은 Git worktree, 코드 구조는 주기적으로 갱신하는 codemap으로 보조한다. 핵심은 설정을 한 번에 거대한 체계로 만드는 것이 아니라 반복되는 실패를 발견할 때마다 rule, skill 또는 hook으로 조금씩 옮기는 것이다.

# 주의점

기사 자체가 GPT 정리를 바탕으로 해 원문 의도와 다를 수 있다고 밝힌다. 예시 설정의 command 이름, plugin과 MCP 형식은 Claude Code 버전에 따라 바뀔 수 있으므로 공식 문서와 실제 schema를 확인해야 한다. Hook에 shell 권한과 secret이 집중되므로 외부 template을 그대로 설치하지 말고 command, network와 credential 접근을 검토해야 한다.

# 출처

- [PyTorchKR의 Everything Claude Code 정리](https://discuss.pytorch.kr/t/everything-claude-code-anthropic-x-forum-ventures-claude-code/8740)
