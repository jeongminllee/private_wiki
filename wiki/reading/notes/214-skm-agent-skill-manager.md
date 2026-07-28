---
type: Reference
title: "SKM: 여러 AI 에이전트의 skill을 한 설정으로 관리하기"
description: "Git repository와 local skill을 감지해 Claude, Codex, OpenClaw 등의 디렉터리에 연결하는 선언형 CLI"
resource: https://discuss.pytorch.kr/t/skm-skill-manager-ai-skill/9193
notion: https://app.notion.com/p/6f01a73cf20b827892398142e2777b21
tags: [reading, ai-agents, developer-tools, skills]
timestamp: 2026-07-24
status: summarized
---

# 해결하는 문제

SKM은 여러 repository에 흩어진 `SKILL.md` 묶음을 한곳에서 설치·업데이트하고 Claude, Codex, OpenClaw 등 각 에이전트의 skill directory에 symbolic link로 배포하는 CLI다. project마다 file을 복사하는 대신 사용자 전역의 선언적 상태를 유지한다.

# 동작 방식

`~/.config/skm/skills.yaml`에 Git repository 또는 `local_path`와 적용할 skill·agent를 선언한다. `skm install`은 source를 store로 가져오고 유효한 `SKILL.md`를 찾아 link를 만들며 lock file을 갱신한다. 설정에서 빠진 오래된 link는 제거하지만 SKM이 만들지 않은 file은 건드리지 않는다.

지원 기본 경로는 `~/.agents/skills/`, `~/.claude/skills/`, `~/.codex/skills/`, `~/.openclaw/skills/`다. `list`, `view`, `check-updates`, `update` 명령으로 설치 상태와 update를 관리한다.

# 적용 전 확인

외부 skill은 agent에게 command와 data access를 유도할 수 있는 실행 지침이다. version을 lock하고 `SKILL.md`와 동봉 script를 review한 뒤 설치해야 한다. Windows에서는 symbolic link 권한과 path 처리, 서로 다른 agent가 기대하는 frontmatter·directory 규칙의 호환성을 확인할 필요가 있다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/skm-skill-manager-ai-skill/9193)
- [reorx/skm](https://github.com/reorx/skm)

