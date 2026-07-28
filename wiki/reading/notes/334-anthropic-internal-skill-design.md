---
type: Concept
title: "Anthropic 내부 사례에서 뽑은 Agent Skill 설계 원칙"
description: "문서·script·asset과 progressive disclosure를 결합해 반복 업무를 재사용 가능한 skill로 만드는 방법"
resource: "https://news.hada.io/topic?id=27640"
notion: "https://app.notion.com/p/d5b1a73cf20b833d91e2819656adf687"
tags: [reading, ai-agent, skills, claude-code, workflow]
timestamp: 2026-07-24
status: summarized
---

# Skill이 적합한 일

내부 사례는 library·API reference, product verification, data fetch·analysis, business automation, scaffold·template, quality review, CI/CD, runbook과 infrastructure operation으로 나뉜다. 반복되며 project 고유 맥락이나 deterministic helper가 필요한 작업이 좋은 후보이고, model이 이미 아는 일반 상식은 되풀이하지 않는다.

# 설계 원칙

- Description은 언제 자동으로 불러야 하는지 판단하는 trigger hint로 쓴다.
- 본문을 작게 유지하고 세부 reference, data와 script는 필요할 때만 읽는 progressive disclosure를 사용한다.
- 반복되는 실패는 `Gotchas`에 추가한다.
- 정확성이 필요한 parsing·검사는 설명 대신 bundled script로 고정한다.
- Setup에서 필요한 값을 묻고 stable data는 `${CLAUDE_PLUGIN_DATA}` 같은 정해진 위치에 보관한다.
- 위험 작업은 `/careful`, `/freeze` 같은 on-demand hook으로 추가 통제한다.

# 운영

작은 팀은 repository에 함께 commit하고 큰 조직은 내부 plugin marketplace와 curator를 둘 수 있다. Native dependency management가 부족하므로 prerequisite와 version을 명시하고, hook으로 사용량과 실패를 관찰한다. 좋은 skill은 처음부터 거대하게 설계하기보다 실제 edge case를 겪으며 자란다.

# 주의

Skill도 실행 가능한 supply-chain 자산이다. Script 권한, secret 접근과 외부 입력을 review하고, 오래된 workflow를 정기적으로 폐기해야 한다. 자동 trigger가 너무 넓으면 불필요한 context와 행동을 유발한다.

# 출처

- [GeekNews 요약](https://news.hada.io/topic?id=27640)
