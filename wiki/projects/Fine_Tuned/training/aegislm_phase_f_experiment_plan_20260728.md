---
type: Project
title: AegisLM Phase F 데이터 재설계와 Qwen 재학습
description: Phase E 품질 실패를 F0~F9에서 분리 진단하고 source target, Qwen 80B 신규 학습, binary-derived adapter와 NuriLab 연결을 순차 검증하는 계획
tags: [aegislm, phase-f, fine-tuning, qwen, dataset, binary-analysis, evaluation]
timestamp: 2026-07-29
status: active
---

# Goal

Phase E에서 검증한 학습·저장·merge·서빙·평가 인프라는 보존하되,
label·provenance 누출, 반복 target, 근거 없는 정답과 token 절단을 제거한
데이터로 Qwen3-Coder-Next 80B LoRA를 base에서 새로 학습한다.

Phase F의 질문:

1. 코드 근거와 tokenizer 예산을 갖춘 source data를 만들 수 있는가?
2. 그 데이터로 새로 학습한 Qwen 80B adapter가 절대 gate를 통과하는가?
3. binary-derived 별도 adapter도 독립 gate를 통과하는가?

# Current Status

| 단계 | 상태 | 현재 근거 |
| --- | --- | --- |
| F0 Phase E 동결 | `Complete` | infrastructure PASS / quality FAIL |
| F1 Raw Catalog·범주화·감사 | `Complete` | r2 group-first pool·taxonomy·reserve·cross-dataset 재현성 감사 통과 |
| F2 Source task·target | `Running — 기존 설계 Fail` | 반복·근거·schema·token 문제 확인 |
| F3 Source 승인 데이터 | `Blocked by F2` | F2 gate를 적용한 `phase-f-source-v3` 생성 필요 |
| F4 Qwen base·legacy 평가 | `Blocked` | F3 승인 challenge 필요 |
| F5 Qwen 신규 학습 | `Blocked` | F3/F4와 전용 runner 필요 |
| F6-A Binary 조사 | `Ready` | GPU 없이 병행 가능 |
| F6-B Binary B0 | `Blocked` | F5 판정 필요 |
| F7 Binary adapter | `Blocked` | B0 통과 필요 |
| F8 NuriLab handoff | `Blocked` | source/binary 결과 필요 |
| F9 최종 결정 | `Not Started` | 앞 단계 결과 필요 |

F1 분류·분할은 완료했습니다. 현재 다음 작업은 학습이 아니라 F2의
source 전용 contract, code-grounded target, tokenizer cutoff 수정입니다.

# Structure

## F0 — Phase E 종료와 증거 동결

기존 80B adapter, merged model, 10,401-step log, 5건·500건 prediction과
평가 결과를 실패 기준선으로 보존한다. 새 학습은 이 checkpoint를
resume하지 않는다.

## F1 — Raw Catalog와 감사

- DiverseVul 330,492건, BigVul 188,636건, PrimeVul paired canonical 9,408건
- raw catalog 537,304건
- eligible/quarantine/reject 284,804/158,251/94,249
- selected/reserve 11,900/272,904
- train/validation/blind 10,000/1,000/500, 각 label 1:1
- BigVul·PrimeVul cross-dataset test 각 200건, 각 완전한 pair 100개
- group/content leakage 0
- model-visible label/provenance leakage 0
- 동일 seed artifact 19개 SHA-256 불일치 0

`phase-f-source-v2-r2`는 F1 구조·범주화·분할 완료본이며 학습 승인본은
아니다. category-stratified sampling과 group-first split을 적용했으며,
F2 target·token gate를 통과한 다음 승인본을 별도로 만든다.

F1 taxonomy:

- `task_family`: source vulnerability, patch analysis, malware behavior,
  binary-derived
- `weakness_family`: memory safety, injection, access control,
  resource/lifetime, concurrency, numeric, crypto, information exposure,
  error handling, other
- `evidence_level`: label-only, CWE-scoped, patch-localized,
  code-span-grounded, analyzer-grounded
- `representation`: source, pseudo-C, assembly, static features
- `pair_type`: unpaired, vulnerable-before, fixed-after
- `length_bucket`
- `label`과 `label_confidence`

Language는 taxonomy, sampling quota, model prompt, 품질 gate에서 제외한다.
원본 dataset이 제공한 값만 provenance 감사용으로 보존하고, 누락된 언어를
코드 문법으로 추정하지 않는다. `unknown`은 정상 입력이다. 목표는 언어명을
맞히는 것이 아니라 언어 정보 없이 위험한 연산·데이터 흐름·API·악성 행위
패턴을 근거로 판단하는 것이다.

## F2 — Source Task·Target 재설계

재감사 결과:

- 10,000개 target 중 exact unique 939개
- 상위 4개 target 5,000건
- summary 8종
- positive evidence generic 문장 사실상 1종
- Qwen 2,048 token 초과 train/validation/challenge
  927/121/46건
- 초과 train은 positive 781, negative 146으로 편향
- CTI/malware용 output schema를 CWE source 판별에 잘못 재사용

수정 방향:

- `present / not_observed / uncertain` source vulnerability contract
- 실제 code span·operation·patch에 연결된 finding
- DiverseVul은 근거 수준에 맞는 분류 후보
- BigVul verified before/after·patch는 설명 근거 후보
- 근거 없는 rich target 생성 금지
- tokenizer total 2,048 이하만 승인

## F3 — Source 승인 데이터 동결

기존 v2는 덮어쓰지 않고
`data/processed/phase-f-source-v3`에 생성한다.

- train 최대 10,000, class 1:1
- validation 1,000
- blind challenge/gold 500
- 저신뢰 record로 quota를 채우지 않음
- target/code-grounding/token audit와 수동 100건 검토
- 모든 hash 동결

## F4 — Qwen Base와 Legacy Adapter

- Q0-B: Qwen base 20건 smoke 후 500건
- Q0-E: Phase E merged adapter 같은 20건·500건

각각 절대평가한다. 상대순위는 채택 기준이 아니다. Contract/evaluator
오류가 없으면 base·legacy 품질 실패 자체는 F5 신규 학습을 막지 않는다.

## F5 — Qwen 80B 신규 학습

```text
Q1 base에서 신규 LoRA 100 step
→ Q2 Q1만 resume, 총 250 step
→ Q3 개선 지속 시 Q2만 resume, 총 313 step
→ M1 채택 후보만 merge·vLLM
```

Phase E YAML과 runner는 old dataset/output/checkpoint root가 고정돼 있으므로
Phase F 전용 config와 namespace guard를 먼저 구현한다.

Q1 진단 gate:

- 누락 0
- parse/schema 0.99
- safety 1.00
- precision/recall 0.75
- FPR 0.20
- abstention 0.10
- 양쪽 class prediction 존재
- 반복 0.01 이하

최종 gate:

- precision 0.90
- recall 0.95
- FPR 0.05
- abstention 0.05
- parse/schema 0.99
- safety 1.00
- evidence linkage 0.90

GPT-OSS-20B는 Qwen 결론 이후의 선택적 이식성 실험이며 선행 gate가 아니다.

## F6 — Binary 조사와 B0

F6-A는 현재 BigVul patch evidence 복구와 NIST SARD/Juliet 자체 컴파일을
우선한다. 그 다음 Assemblage·Decompile-Bench의 소규모 aligned subset,
BinKit compiler 강건성 subset, EMBER2024 static-feature 평가 subset을
검토한다. 전체 raw binary corpus와 malware payload는 받지 않는다.

F6-B는 source 판정 후 before/after 100 pair를 GCC·Clang, O0/O2로
컴파일·디컴파일한다. compile/decompile 0.90, pair 연결 0.95와 raw
payload·provenance 누출 0을 요구한다.

## F7 — Binary Adapter

검증된 pair 최대 2,000, train 최대 4,000, validation 400, blind 500으로
별도 adapter를 학습한다. O3+stripped와 compiler consistency를 추가
평가한다.

## F8 — NuriLab Handoff

NuriLab/offline extractor가 pseudo-C, 제한된 assembly, static features,
function hash와 extraction warning을 normalized record로 전달한다.
AegisLM은 source → binary → normalized signals → multitask → RAG →
RAG/MCP 순서로 독립 gate를 적용한다.

## F9 — 최종 결정

`채택 / Source만 채택 / 데이터 수정 후 재학습 / 모델 변경 /
파인튜닝 중단 / Phase G 진입` 중 하나를 증거로 확정한다.

# Key Decisions

- Loss는 관찰값이며 gate가 아니다.
- 기존 33만 건을 다시 학습하지 않는다.
- 현재 v2 구조 통과를 학습 승인으로 해석하지 않는다.
- Qwen 신규 학습은 base에서 시작한다.
- GPT-OSS는 Qwen 선행 조건이 아니다.
- source와 binary adapter는 독립 검증한다.
- language는 분류·quota·prompt·gate에서 제외하고 감사 metadata로만 둔다.
- raw/live malware와 byte-level 연구는 Phase G로 보류한다.

# Issues

- Source vulnerability 전용 schema·prompt·evaluator 미구현
- code-grounded target builder와 token audit 미구현
- Phase F 전용 Qwen YAML·checkpoint namespace guard 미구현
- BigVul pair와 원 코드 license 추가 검토 필요
- 재감사 시 Phase E merged vLLM이 port 8000에서 계속 실행 중

# Next Actions

1. Source vulnerability contract와 evaluator를 구현한다.
2. Code-grounded target builder와 Qwen token audit를 구현한다.
3. F2 gate를 적용한 `phase-f-source-v3`을 생성해 수동 100건까지 통과시킨다.
4. SARD/Juliet function-level good/bad extractor를 설계하고 raw-only 상태를 해제할지 판단한다.
5. Phase F Qwen 100/250/313-step config와 resume guard를 구현한다.
6. Q0-B/Q0-E와 Q1을 실행하고 gate에 따라 Q2/Q3를 진행한다.
7. 최종 후보만 merge·vLLM 검증한다.

# Related Concepts

- [Phase F 구현·실험 SSOT](../repos/AegisLM-B200/docs/experiments/plans/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [AegisLM 수동 검증 워크북](../repos/AegisLM-B200/docs/operations/b200/FINETUNING_TEST_WORKBOOK.md)
- [데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md)
- [Qwen3-Coder-Next 80B 실행 기록](qwen3_coder_next_80b_2gpu_run_20260720.md)
- [LLM 생명주기 환경 설계](../../../infra/llm-lifecycle-environment-design.md)
