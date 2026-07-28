---
type: Reference
title: "How I Claude Code: 긴 agent 작업의 성능을 좌우하는 context 관리"
description: "플랜 모드, 서브에이전트, 중간 문서, skill과 MCP CLI로 탐색·설계·구현의 context를 분리하는 2시간 38분 강의"
resource: https://www.youtube.com/live/wDP91skrk5M
notion: https://app.notion.com/p/32c1a73cf20b82c29a248119abe9ad7e
tags: [reading, claude-code, context-engineering, ai-agents]
timestamp: 2026-07-24
status: summarized
---

# 중심 생각

발표자는 짧은 bug fix는 최신 model이 이미 잘 처리하므로, 긴 작업에서 coding agent를 잘 쓰는 능력은 특별한 prompt 문구보다 context를 관리하는 능력에 가깝다고 본다. 탐색 결과, 요구사항, 긴 tool output과 구현 대화를 한 context에 계속 쌓으면 정작 code를 만들 때 중요한 정보가 묻힌다.

# 사용 흐름

먼저 plan mode에서 codebase를 탐색하고 여러 내장 subagent가 서로 다른 관점으로 조사하게 한다. 탐색과 설계를 마치면 결과를 Markdown 계획서로 저장하고, 구현은 그 문서를 입력으로 새 context에서 시작한다. 단계 사이의 중간 산출물이 handoff contract가 되어 앞선 대화 전체를 가져오지 않아도 된다.

Skill은 매번 모든 지식을 넣지 않고 필요한 순간에 지침을 불러오는 장치로 설명한다. MCP를 직접 호출해 대량 data를 context에 넣기보다 MCP CLI나 code가 중간에서 query·filter하고 최종 결과만 agent에 돌려주면 token과 주의력을 아낄 수 있다. IDE diagnostic처럼 이미 구조화된 오류 정보도 전체 build log보다 좁은 feedback에 유리하다.

발표 중 frontend 예시는 reference site의 image와 design 요소를 먼저 수집하고 checklist를 만든 뒤 component 단위로 구현한다. 바뀔 가능성이 큰 절차는 고정 code보다 수정하기 쉬운 prompt·skill로 두고, browser를 무작정 눈으로 조작시키기보다 재현 가능한 test script를 선호한다.

# 적용 기준

Subagent의 사용량은 main context에 그대로 쌓이지 않아도 전체 token·비용은 발생한다. 여러 agent를 부르는 것이 정확성을 자동 보장하지 않으므로 조사 질문, 반환 형식과 종료 조건을 좁혀야 한다. 발표자의 요금제·도구 선호는 2025년 말 당시의 개인 경험이며 현재 가격과 기능 비교로 읽어서는 안 된다.

이 영상은 한국어 자동 자막을 바탕으로 확인했다. 자막에 반복과 일부 오인식이 있어 특정 command 철자보다 workflow의 구조를 중심으로 정리했다.

# 출처

- [YouTube 강의](https://www.youtube.com/live/wDP91skrk5M)

