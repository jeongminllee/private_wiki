---
type: Reference
title: "OpenCode 입문과 현재 설정에서 확인할 점"
description: "OpenCode 설치, provider 연결, plan mode, LSP·MCP·GitHub 연동을 설명하고 오래된 설정 예제를 바로잡은 안내"
resource: "https://help.apiyi.com/ko/opencode-ai-coding-agent-beginner-guide-2026-ko.html"
notion: "https://app.notion.com/p/15f1a73cf20b83d2ad050149338d732f"
tags: [reading, opencode, coding-agent, cli, setup]
timestamp: 2026-07-24
status: summarized
---

# 기본 workflow

OpenCode는 terminal에서 repository를 읽고 code를 수정하는 open-source coding agent다. 설치 후 project directory에서 실행하고 `/connect`로 model provider credential을 연결한다. `/init`으로 project instruction을 만들고, 불확실한 작업은 plan agent로 먼저 읽기·분석한 뒤 build 단계로 넘긴다.

관련 file을 명시하고 큰 refactor를 작은 단계로 나누며, 각 단계에서 test와 diff를 확인하는 방식이 안전하다. LSP diagnostic으로 언어별 오류를 받고 MCP server로 외부 tool을 확장할 수 있다. GitHub integration은 issue나 PR에서 작업을 시작하고 Actions runner에서 수행하는 흐름을 제공한다.

# 원문 예제의 시점 문제

Article의 `config.json`, `providers` 복수 field와 특정 model name은 현재 공식 schema와 다를 수 있다. 2026년 7월 공식 문서는 `opencode.json`, 단수 `provider`, `options.baseURL`, `models` 구조를 사용한다. Legacy `tools` boolean도 `permission`으로 통합되었다.

Third-party API proxy 예제는 편리하지만 source code와 prompt가 외부 endpoint로 전송된다. Credential은 config에 직접 쓰지 말고 environment reference나 credential store를 사용하고, provider의 privacy·retention과 model identity를 확인해야 한다.

# 출처

- [저장된 한국어 가이드](https://help.apiyi.com/ko/opencode-ai-coding-agent-beginner-guide-2026-ko.html)
- [OpenCode 공식 provider 문서](https://opencode.ai/docs/providers)
- [OpenCode 공식 agent·permission 문서](https://opencode.ai/docs/agents/)
