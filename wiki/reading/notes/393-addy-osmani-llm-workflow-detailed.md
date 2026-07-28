---
type: Reference
title: "2026년을 대비한 LLM 코딩 workflow 상세 정리"
description: "계획, context, 작은 반복, 여러 model, test와 version control을 개발 전 과정에 배치하는 Addy Osmani의 경험"
resource: "https://news.hada.io/topic?id=25755"
notion: "https://app.notion.com/p/f831a73cf20b83cc8bc801f54dcb0b94"
tags: [reading, ai-coding, workflow, testing, software-engineering]
timestamp: 2026-07-24
status: summarized
---

# 시작은 대화와 명세

새 project에서는 AI가 먼저 요구사항과 edge case를 질문하게 하고, 확정된 내용을 `spec.md`로 만든다. Architecture decision, data model, test strategy와 명시적 범위를 담은 뒤 reasoning model이 이를 작은 task로 분해하게 한다. 이 단계가 재작업과 서로 맞지 않는 module을 줄인다.

# 구현 loop

한 번에 큰 feature를 맡기지 않고 review 가능한 increment로 진행한다. 현재 task에 필요한 file, API와 constraint를 주고, 변경 뒤 test, lint와 diff를 확인한다. Context가 길어져 방향을 잃으면 현재 결정과 남은 작업을 문서로 저장하고 새 session에서 다시 시작한다.

Model은 강점에 따라 나눠 쓸 수 있다. 구현, debugging, UI critique와 code review를 서로 다른 model에 맡기되 최종 판단은 사람이 한다. AI가 작성한 code를 이해하지 못한 채 merge하면 속도 이득이 미래 debugging 비용으로 돌아온다.

# 수치를 읽는 법

원문에 인용된 조직별 AI 작성 code 비율은 측정 정의와 시점이 다르며 품질이나 생산성의 직접 지표가 아니다. 중요한 것은 accepted change까지의 cycle time, escaped defect, review 부담과 유지보수성이다.

# 관련 문서

- [같은 원문의 핵심판](392-addy-osmani-llm-workflow-condensed.md)

# 출처

- [GeekNews 상세 정리](https://news.hada.io/topic?id=25755)
- [Addy Osmani 원문](https://addyosmani.com/blog/ai-coding-workflow/)
