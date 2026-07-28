---
type: Reference
title: "실용적인 Agent 구축 원칙: 단일 loop와 평가부터 시작하기"
description: "model·tool·instruction으로 agent를 구성하고 적합한 workflow, guardrail과 확장 순서를 판단하는 guide"
resource: https://news.hada.io/topic?id=27459
notion: https://app.notion.com/p/f751a73cf20b8350b0728145c5faf9b1
tags: [reading, ai-agents, architecture, guardrails]
timestamp: 2026-07-24
status: summarized
---

# Agent가 필요한 경우

Agent는 LLM이 workflow의 다음 행동과 완료 여부를 판단하고 tool로 외부 system을 바꾸는 application이다. 단순 chat이나 한 번의 classification은 agent가 아니다. 복잡한 예외 판단, 유지보수하기 어려운 rule set, 비정형 문서·대화가 핵심인 업무에서 특히 가치가 있다. 그렇지 않으면 deterministic automation이 더 낫다.

# 세 구성요소

- **Model**: reasoning과 decision을 담당한다.
- **Tools**: API와 function으로 실제 행동한다.
- **Instructions**: 정책, 절차와 경계를 명시한다.

처음에는 강한 model로 quality baseline을 만들고 eval을 통과하는 범위에서 작은 model로 교체해 cost와 latency를 줄인다.

# 구축 순서

단일 agent와 작은 tool set으로 시작해 실제 task completion과 failure를 측정한다. domain이 뚜렷하게 나뉘거나 tool 선택이 지나치게 복잡해질 때만 manager·specialist 구조로 확장한다. privacy, content safety, permission, human handoff와 stop condition은 여러 guardrail layer로 둔다.

# 핵심 원칙

Agent의 성공은 demo의 자연스러운 답변보다 완료율, 잘못된 action, escalation, latency와 비용으로 판단해야 한다. 실패를 감지했을 때 멈추고 사용자에게 제어권을 돌려주는 것도 핵심 기능이다.

# 출처

- [GeekNews 정리](https://news.hada.io/topic?id=27459)

