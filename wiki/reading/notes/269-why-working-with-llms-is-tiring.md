---
type: Reference
title: "LLM 협업 피로는 느린 feedback loop와 불명확한 성공 기준에서 커진다"
description: "긴 context와 반복 수정이 만드는 인지 피로를 줄이는 짧은 실험·휴식·검증 기준"
resource: https://news.hada.io/topic?id=27565
notion: https://app.notion.com/p/2e41a73cf20b8276803301fdaaf8e698
tags: [reading, ai-coding, productivity, feedback-loop]
timestamp: 2026-07-24
status: summarized
---

# 피로가 생기는 loop

작업이 길어지면 사람은 핵심 context를 빠뜨린 prompt를 보내고, 불만족한 결과에 중간 개입과 수정을 반복한다. Model context도 커져 latency가 늘고 최근 실험이 묻히면서 결과가 더 나빠진다. 다음 판단을 위해 다시 긴 output을 읽어야 하므로 사람의 review 부하도 커진다.

# 글의 제안

- 목표 결과를 구체적으로 상상할 수 없을 때는 즉시 prompt를 보내지 않는다.
- 긴 작업을 빠르게 재현 가능한 작은 failure case로 줄인다.
- “5분 안에 실패를 재현한다”처럼 feedback-loop 시간도 acceptance criterion으로 둔다.
- Context가 포화되면 새 session에 verified state만 전달한다.
- Prompt 작성이 거칠어지고 판단력이 떨어졌다면 휴식한다.

이 방식은 TDD와 비슷하다. Agent가 바꾼 code를 짧은 test로 곧바로 검증할수록 실패 원인을 좁히기 쉽고 context 소비도 줄어든다.

# 덧붙일 관점

글은 개인 경험을 일반화한 essay이며 “좋은 prompt를 쓰면 피로가 해결된다”는 실험 연구는 아니다. 피로는 skill뿐 아니라 model latency, tool reliability, review 가능한 diff 크기와 조직의 과도한 workload에서도 생긴다.

실무에서는 session당 목표 하나, deterministic test, 작은 diff, 중간 checkpoint와 human stop rule을 함께 두는 편이 낫다. 생산성은 생성 token 수가 아니라 검증된 결과까지 걸린 시간과 수정 횟수로 측정해야 한다.

# 출처

- [GeekNews 요약](https://news.hada.io/topic?id=27565)

