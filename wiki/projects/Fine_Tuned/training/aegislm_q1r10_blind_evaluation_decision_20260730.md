---
type: Decision Note
title: AegisLM Q1R10 Blind 평가와 Evidence 보정 결정
description: Q1R10 decision adapter의 절대평가 통과와 Q1R9 evidence adapter의 strict renderer 실패를 분리하고 다음 Q1R11 실험을 결정한 기록
tags: [aegislm, phase-f, qwen, blind-evaluation, evidence]
timestamp: 2026-07-30
status: active
---

# Summary

Qwen3-Coder-Next 80B의 Q1R10 decision-only adapter는 미노출 480건
절대평가를 통과했다. 그러나 Q1R9 evidence-only adapter는 malformed line
range 3건 때문에 deterministic renderer `1.00` 조건을 만족하지 못했다.

따라서 source two-stage 전체 판정은 `FAIL`이다. Decision 모델은 동결하고
추가 250-step 학습을 하지 않는다. 다음 실험은 미사용 SARD pair로 새
blind를 먼저 만든 뒤 evidence-only 100-step Q1R11을 수행한다.

# Confirmed Facts

## Q1R10 Decision

- 학습: base-start 100 steps
- adapter SHA-256:
  `3dee2eb1d1555b90ff0a680d15b53e6fc3ed21f3be18b74f344fc304fbf23dd4`
- dev100: TP/TN/FP/FN `49/50/0/1`
- blind 480: TP/TN/FP/FN `239/236/4/1`
- blind precision/recall/FPR: `0.9835/0.9958/0.0167`
- parse/schema: `1.00/1.00`
- 판정: `PASS`

## Q1R9 Evidence

- blind evidence precision/recall/F1: `0.7855/0.8056/0.7954`
- parse/schema: `1.0000/0.9938`
- deterministic renderer: `0.9938`, 즉 `477/480`
- 판정: `FAIL`

처음 확인된 renderer 실패 5건 중 2건은 서로 다른 유효 line이 동일한
문자열을 포함할 때 exact span을 중복 생성하는 resolver 구현 문제였다.
동일 텍스트만 결정적으로 중복 제거한 뒤에도 다음 모델 오류 3건이 남았다.

- `sard-82a5750b899aa72e-present`: 역순 range `13 → 7`
- `sard-1ee5ed456f983a10-not_observed`: 동일 range 중복
- `sard-8beb1c673aac344e-present`: 역순 range `80 → 77`

모델 오류를 숨기지 않기 위해 역순이나 중복 range는 자동 교정하지 않았다.

# Decision

1. Q1R10 decision adapter를 현재 decision 채택 후보로 동결한다.
2. Q1R9 evidence adapter는 최종 source pipeline에 채택하지 않는다.
3. Decision 250-step은 실행하지 않는다. 100-step에서 이미 절대 gate를
   통과했고 남은 오류는 evidence objective에 있기 때문이다.
4. 사용한 blind 480은 연구 증거로만 보존하고 후속 모델의 최종 blind로
   재사용하지 않는다.
5. 현재 extractor에서 기존 group ID와 code hash를 모두 제외한 뒤 확인한
   unique complete pair `2,217`개를 이용해 기존 split과 겹치지 않는 새
   blind를 먼저 동결한다.
6. Q1R11은 decision 데이터나 threshold를 바꾸지 않고 evidence-only
   100-step으로 수행한다.
7. Q1R11은 dev100을 먼저 통과해야 하며, 새 blind는 최종 단계에서 한 번만
   연다.
8. Source 전체 gate를 통과하기 전에는 binary adapter, NuriLab, RAG/MCP로
   진행하지 않는다.

# Why

이번 결과는 “모델이 대체로 잘했으니 통과”가 아니라 사전에 고정한
절대평가를 적용한 결과다. 3/480은 작은 비율이지만 renderer `1.00`은
production contract가 항상 유효한 보고서를 생성하는지 확인하는 hard
gate다.

또한 blind gold를 본 뒤 같은 480건에 맞춰 재학습하고 다시 최종 점수로
사용하면 data snooping이 된다. 새 group에서 평가해야 Q1R11의 개선이 실제
일반화인지 판단할 수 있다.

# Next Actions

1. 미사용 SARD group 기반 새 blind builder와 overlap 감사를 구현한다.
   (`완료`: 500건, group/code overlap `0/0`)
2. 새 challenge/gold/private records를 분리하고 hash를 동결한다.
   (`완료`: source·contract 독립 재빌드 hash 일치)
3. Q1R11 evidence-only 100-step config와 preflight를 만든다.
   (`완료`: 2026-07-30 preflight PASS, 학습 시작)
4. dev100의 parse/schema/renderer/evidence gate를 확인한다.
5. dev100 통과 시 새 blind에서 Q1R10→Q1R11 two-stage를 한 번 평가한다.
6. 최종 PASS일 때만 source adapter 결론과 다음 Phase F 분기를 결정한다.

위 4–6번은 2026-07-30에 완료됐다. 신규 blind 500건 전체 gate가
PASS했으며 후속 결정은
[Q1R11 신규 Blind 500 PASS와 Source 후보 동결](aegislm_q1r11_fresh_blind_pass_decision_20260730.md)에
기록했다.

# Related Concepts

- [AegisLM Phase F 실행 계획](aegislm_phase_f_experiment_plan_20260728.md)
- [파인튜닝 실행 기록](qwen3_coder_next_80b_2gpu_run_20260720.md)
- [절대평가 계획](aegislm_phase_f_experiment_plan_20260728.md)
- [데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md)
- [LLM 생명주기 환경 설계](../../../infra/llm-lifecycle-environment-design.md)

# Evidence

- Blind summary:
  `artifacts/evaluation/phase-f-source-untouched-blind-480-v1/q1r10-q1r9-two-stage/summary.json`
- 최종 summary SHA-256:
  `aa555516f827b46c11bab12f63a8bc4d8a7573941fcb9a8e1883857eefb3b4d7`
- 수정 전 summary SHA-256:
  `28837d1b65080fe4f2ef984e0f58f62b065f6595284839a1160deeb53f36b8f4`
- Decision predictions SHA-256:
  `bb377ce766704b187535e08946f8bdd74274b207bade2084430a2ca5a2e2154a`
- Evidence predictions SHA-256:
  `215a577ece07e5ac9a6a5ab702115b0982959d125e64dd5a73cfab4072313118`
