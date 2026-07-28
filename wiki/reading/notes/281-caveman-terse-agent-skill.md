---
type: Reference
title: "Caveman: 코딩 에이전트의 출력만 짧게 만드는 응답 압축 skill"
description: "코드·명령·오류는 보존하면서 설명의 군더더기를 줄이는 다중 에이전트용 skill과 실제 절감 범위"
resource: https://github.com/JuliusBrussee/caveman
notion: https://app.notion.com/p/11d1a73cf20b839c8f62010c7a9cd1b0
tags: [reading, ai-agents, token-efficiency, agent-skills]
timestamp: 2026-07-24
status: summarized
---

# 무엇을 하는가

Caveman은 Claude Code, Codex, Gemini CLI, Cursor 등 30개 이상의 coding agent가 답변을 짧고 전보문처럼 쓰게 만드는 skill·plugin이다. 모델의 추론이나 도구 사용 능력을 줄이는 것이 아니라 최종 설명의 완곡한 표현과 반복을 걷어낸다. 코드, command, path와 error message는 원문 그대로 유지하도록 지시한다.

`lite`, `full`, `ultra`, `wenyan` 강도를 고를 수 있고 commit message, PR review, session token 통계, memory file 압축과 MCP tool description 압축 기능도 포함한다. `caveman-compress`는 `CLAUDE.md` 같은 매번 입력되는 문서를 줄여 출력뿐 아니라 이후 session의 input도 절약하려는 별도 기능이다.

# 숫자를 읽는 법

저장소 benchmark는 10개 prompt에서 기본 응답보다 output token이 평균 65% 감소했다고 보고한다. 작업별 범위는 22~87%이고 memory file 예시는 평균 46% 감소했다. 다만 이는 프로젝트가 준비한 prompt와 비교 조건에서 얻은 수치이지 모든 업무의 품질 보증은 아니다.

더 중요한 제한은 skill 자체가 매 turn 약 1,000~1,500 input token을 추가하고 reasoning token은 줄이지 않는다는 점이다. 원래부터 짧게 답하는 agent나 짧은 session에서는 총비용이 오히려 늘 수 있다. 따라서 장문의 설명을 자주 읽는 workflow에서 가독성과 응답 속도를 개선하는 도구로 보고, 실제 비용은 `/caveman-stats`나 provider usage로 측정하는 편이 맞다.

# 도입할 때

원격 script를 `curl | bash` 또는 `irm | iex`로 바로 실행하는 설치법이 제시되지만, production 장비에서는 script를 먼저 내려받아 검토하고 revision을 고정한다. 지나친 축약은 가정, 위험, 대안과 근거를 없앨 수 있으므로 architecture 결정이나 보안 review에는 `lite`를 쓰고 결과 형식을 명시적으로 요구하는 편이 안전하다.

# 출처

- [Caveman 저장소](https://github.com/JuliusBrussee/caveman)

