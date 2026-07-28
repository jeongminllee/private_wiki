---
type: Decision Note
title: AegisLM 데이터 축소와 통제된 무작위화 결정
description: 33만 건 full SFT가 낮은 loss에도 500건 절대평가에 실패한 뒤, 1–2만 건 고품질 데이터와 재현 가능한 입력 다양화로 전환한 연구 결정
tags: [aegislm, fine-tuning, dataset, evaluation, b200]
timestamp: 2026-07-28
status: active
---

# Summary

2026-07-28 AegisLM Qwen3-Coder-Next 80B LoRA 실험은 약 33만 건을 1 epoch 학습하는 데 7일 이상 걸렸고, loss는 매우 빠르게 0에 가까워졌다. 그러나 500건 label-blind 절대평가에서 실제 코드 취약점 분석 능력은 기준에 크게 미달했다.

다음 실험은 기존 33만 건을 그대로 재사용하지 않는다. model-visible label과 source metadata를 제거하고, 코드별 근거를 갖춘 **1–2만 건 규모의 고품질 학습 데이터**로 줄인다. 여기에 정답 의미를 바꾸지 않는 **통제된 무작위화(controlled randomization)**를 적용한다.

# Why this decision was made

## 비용과 학습 효율

- Train record: `332,807`
- Update step: `10,401`
- 학습 시간: `7일 34분 41초`
- 마지막 loss: 약 `1.5e-6`
- full validation 1회: 약 3시간 30분

loss가 빠르게 감소한 뒤에도 대규모 데이터를 계속 학습하면서 GPU 임대 시간을 소모했다. 낮은 loss가 실제 성능으로 이어졌는지 조기에 확인하는 label-blind gate가 없었던 것이 가장 큰 운영상 문제였다.

## 실제 품질

500건 절대평가 결과:

| 항목 | 결과 |
| --- | ---: |
| TP / FP / TN / FN | `84 / 116 / 0 / 166` |
| Precision | `0.420` |
| Recall | `0.336` |
| FPR | `0.464` |
| Abstention | `0.598` |
| JSON parse | `0.556` |
| Schema | `0.530` |

정상 코드 250건 중 유효한 `low` 판정이 한 건도 없었다. 222건은 JSON parse에 실패했고, 다수 출력이 반복 루프에 들어가 1,024-token 상한에서 잘렸다.

## 데이터 설계 원인

확인된 train 구성:

- DiverseVul `211,333`건
- BigVul `120,897`건
- Cybersecurity QA `577`건

DiverseVul 전 record의 model-visible prompt에 dataset label, target, provenance가 포함돼 있었다. assistant target은 전체 JSON 기준 약 20개 형태로 집중됐다. BigVul은 취약한 `before` 코드만 입력으로 사용하고 모든 target을 `high`로 만들었다.

따라서 loss 수렴은 raw code 분석보다 노출된 label과 반복 target을 재현하는 과제에 수렴한 결과로 해석한다.

# Decision

## 기존 데이터 처리

기존 `hf-full-v1`과 현재 adapter는 삭제하거나 덮어쓰지 않는다. 실패 원인과 재현성을 위한 artifact로 동결한다.

다음 학습에서는:

- 기존 33만 건 export를 학습 대상에서 제외한다.
- Cybersecurity QA는 코드 취약점 판별 SFT에서 제외하고 RAG 또는 별도 보안 지식 task 후보로 분리한다.
- DiverseVul은 raw code와 숨겨진 gold label로 다시 변환한다.
- BigVul은 `func_before=취약`, `func_after=정상` pair로 재구성한다.
- code hash와 유사도 기준으로 중복·준중복을 제거한다.

## 첫 v2 train 규모

`10,000–20,000` train record를 목표 범위로 사용한다. 정확한 건수보다 class/source/template 균형과 근거 품질을 우선한다.

권장 시작 구성:

| 구성 | 권장량 | 목적 |
| --- | ---: | --- |
| DiverseVul vulnerable | 약 `5,000` | raw C/C++ 취약 사례 |
| DiverseVul benign | 약 `5,000` | 동일 source의 정상 대조 |
| BigVul before/after | `2,000–5,000 pair` | 같은 코드베이스 안의 취약/수정 hard negative |
| Cybersecurity QA | `0` | 현재 code-analysis SFT 범위에서 제외 |

BigVul pair는 pair당 before/after 두 record가 되므로 전체 train 수가 1–2만 건 범위를 넘지 않도록 최종 quota를 조정한다.

# Controlled Randomization

무작위화의 목적은 같은 의미를 다양한 입력 표현에서 인식하게 하고, dataset/template shortcut을 줄이는 것이다. 정답을 흐리거나 무작위 label noise를 추가하는 것이 아니다.

## 허용

- class와 source별 quota 안에서 고정 seed로 record를 무작위 추출
- positive/negative에 동일 비율로 prompt 표현 variant를 배정
- 같은 output contract를 요구하는 3–5개의 의미 동등한 user instruction variant
- 취약 근거 위치가 보존되는 범위에서 code window의 앞뒤 context 길이 변화
- 학습 record 순서 shuffle
- code hash와 seed로 template variant를 결정하는 재현 가능한 배정

권장 variant 배정:

```text
variant_id = sha256(code_sha256 + build_seed) % template_count
```

이 방식은 빌드를 다시 실행해도 같은 코드가 같은 variant를 사용하게 한다.

## 금지

- vulnerability label 또는 risk level 무작위 변경
- 근거 없는 CWE·ATT&CK·행위 설명 임의 생성
- 취약 연산을 제거하거나 의미를 바꾸는 code 변형
- positive에 특정 template, negative에 다른 template를 배정하는 class-template 상관
- JSON field 누락, 형식 변화, 자유로운 prose target으로 output contract를 흔드는 방식
- seed와 manifest를 남기지 않는 비재현성 shuffle

JSON target 형식은 다양화하지 않는다. 출력 schema와 key type은 고정하고, 입력 표현과 표본 구성만 통제된 범위에서 다양화한다.

# Target quality rules

- label만 있고 코드별 취약 근거를 만들 수 없는 record는 설명형 SFT에서 제외한다.
- 취약 record는 함수·연산·data flow 또는 patch 변화에 근거한 설명을 포함한다.
- 정상 record는 단순히 `low`만 출력하지 않고, 왜 제공된 범위에서 취약 근거가 부족한지 기록한다.
- ATT&CK 근거가 없으면 `attack_mapping: []`를 사용한다.
- 정형 target 고유 수, 상위 template 점유율, 동일 output hash 비율을 manifest에 기록한다.
- source명, split, label, target, 평가 metadata는 model-visible prompt에 넣지 않는다.

# Experiment gates

```text
dataset audit
→ 100-step training
→ 50–100건 label-blind diagnostic
→ 필요할 때 500/1,000 step
→ 500건 절대평가
→ 재현성 평가
```

다음 조건이면 full training을 시작하지 않는다.

- 100-step 이후 loss만 감소하고 blind precision/recall이 개선되지 않음
- 정상 표본에서 `low`가 나오지 않음
- 반복 출력이나 length 종료가 반복됨
- prompt와 label/source/template 사이 상관이 발견됨
- code-specific evidence target 비율이 정한 기준에 미달함

100건 평가는 빠른 중단을 위한 진단이며 최종 채택 근거가 아니다. 최종 판정은 독립 500건 절대평가로 수행한다.

# Phase F implementation

이 결정은 AegisLM-B200의 Phase F로 구체화했다.

- Phase E는 `infrastructure PASS / model quality FAIL`로 종료한다.
- Phase F source profile은 5,000 positive + 5,000 benchmark-negative,
  validation 1,000, blind test 500으로 고정한다.
- 데이터는 raw catalog Parquet, eligible manifest Parquet, materialized
  JSONL의 세 계층으로 분리한다.
- 기존 model-visible source, metadata, target, label은 prompt formatter에서
  제거한다.
- `openai/gpt-oss-20b` 100-step canary가 진단 gate를 통과한 뒤에만
  Qwen3-Coder-Next 80B 재학습을 허용한다.
- source와 binary-derived adapter를 별도로 평가하고 둘 다 통과한 뒤에만
  NuriLab/RAG/MCP 연결을 검증한다.
- binary는 raw byte가 아니라 pseudo-C, 정적 특징, 제한된 assembly
  evidence를 사용한다.

BigVul의 현재 canonical record에는 fixed code body와 충분한 CWE·수정
위치가 없으므로 자동 보강하지 않고 `quarantine`으로 둔다. B0에서
build 가능한 before/after 100 pair를 확보하고 compile/decompile/pair
보존 gate를 통과한 뒤에만 binary adapter dataset을 만든다.

# Research story

1. **가설**: 33만 건 보안 데이터로 SFT하면 코드 보안 분석 능력이 향상될 것이다.
2. **관측**: loss는 빠르게 거의 0에 수렴했지만 학습은 7일 이상 지속됐다.
3. **실제 검증**: 500건 label-blind 평가에서 TN 0, 낮은 precision/recall, 반복 JSON 실패가 확인됐다.
4. **원인 해석**: 데이터 크기보다 target leakage, source shortcut, 반복 target이 학습을 지배했다.
5. **다음 가설**: 1–2만 건의 근거 중심 데이터와 통제된 입력 무작위화가 더 짧은 시간에 실제 blind 성능을 높일 수 있다.
6. **반증 조건**: 수정 데이터로도 blind gate가 개선되지 않으면 데이터가 아니라 base model 또는 fine-tuning task 자체를 재검토한다.

# Related Concepts

- [Qwen3-Coder-Next 80B B200 2-GPU 실행 기록](qwen3_coder_next_80b_2gpu_run_20260720.md)
- [AegisLM Phase F 연구 계획](aegislm_phase_f_experiment_plan_20260728.md)
- [Security Datasets](../data/security_datasets.md)
- [AegisLM 수동 파인튜닝 검증 워크북](../repos/AegisLM-B200/docs/FINETUNING_TEST_WORKBOOK.md)
- [Phase F 데이터 재설계 및 바이너리 분석 실험 계획](../repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [LLM 생명주기 환경 설계](../../../infra/llm-lifecycle-environment-design.md)

# Citations

- AegisLM-B200 run `aegislm-qwen3next-20260728T100259-operator`의 training artifact, 500건 prediction, absolute summary와 report
- `data/processed/hf-full-v1/dataset_manifest.json`
- `aegislm/datasets/security_builder.py`
