---
type: Concept
title: "Claude Code의 지속 학습을 Skills로 구현하기"
description: "회고 결과와 실패 패턴을 plain-text skill에 축적해 다음 coding session에 재사용하는 외부 기억 workflow"
resource: "https://www.youtube.com/watch?v=sWbsD-cP4rI"
notion: "https://app.notion.com/p/de71a73cf20b83d5964001c1ff6c1cc0"
tags: [reading, claude-code, skills, continual-learning, workflow]
timestamp: 2026-07-24
status: summarized
---

# 핵심 아이디어

여기서 continual learning은 model weight를 계속 학습하는 방식이 아니다. Session에서 얻은 규칙, 성공 사례와 실패 패턴을 plain-text Skills로 저장해 다음 작업 때 선택적으로 불러오는 외부 기억 방식이다. 파일이므로 사람이 읽고 수정하며 version control과 공유를 할 수 있다.

# 동작 방식

Skill은 처음부터 모든 내용을 context에 넣지 않는다. 이름과 description만 노출하고 관련 요청이 들어오면 본문, script와 reference를 progressive disclosure로 읽는다. 작업 후 retrospective에서 무엇이 성공·실패했는지 분석하고 기존 skill을 찾은 뒤, 재사용할 규칙과 guardrail을 갱신한다.

성공 사례만 저장하면 조건이 조금 바뀌었을 때 같은 실패를 반복할 수 있다. 실패 원인과 피해야 할 anti-pattern도 함께 기록하면 비결정적인 agent의 탐색 범위를 줄일 수 있다. 개인 skill은 개인 환경에, project skill은 `.claude/skills/`에, 조직 공통 규칙은 shared plugin에 둘 수 있다.

# 주의

외부 기억은 틀린 결론이나 오래된 명령도 증폭한다. 자동으로 작성된 skill을 바로 신뢰하지 말고 review, test, source와 timestamp를 붙여야 한다. 진짜 online learning이나 모델 자체의 능력 향상과 구분해서 평가한다.

# 출처

- [Continual Learning in Claude Code](https://www.youtube.com/watch?v=sWbsD-cP4rI)
- [Companion article](https://developersdigest.tech/continual-learning-in-claude-code/)
