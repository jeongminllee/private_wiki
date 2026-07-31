---
type: Decision Note
title: AegisLM Binary 엄격 Target Evidence 재감사 결정
description: F7 두 차례 500-pair 확대와 과거 B0·pilot에 동일한 target-evidence 기준을 적용해 누적 공급 gate를 다시 계산한 기록
tags: [aegislm, phase-f, binary-analysis, dataset-quality, evaluation]
timestamp: 2026-07-30
status: active
---

# Summary

Phase F F7 첫 500-pair 확대 배치는 컴파일과 디컴파일 인프라는 통과했지만
target-preservation 품질 gate에는 실패했다. 더 중요한 발견은
`CWE-476`과 `CWE-563`처럼 최적화 후 핵심 취약 연산이 사라진 사례가
과거 검토에서는 PASS와 FAIL로 섞여 있었다는 점이다.

이에 `strict-target-evidence-v1`을 새 정본으로 정하고 과거 B0 145쌍,
pilot 250쌍, 현재 500쌍에 동일하게 적용했다. 과거 결과는 삭제하지 않고
새 strict summary가 이전 결론을 supersede한다.

# Why it matters

compile, function link, decompile 성공은 분석 가능한 입력을 얻었다는
인프라 증거다. 이것만으로 target CWE가 binary-derived representation에
남아 있다고 결론 내릴 수 없다.

특히 최적화가 취약 연산을 제거한 뒤 generic control flow만 남은 표본을
학습에 넣으면 모델은 실제 취약 근거가 아니라 함수명, CWE 분포 또는
주변 패턴을 외울 위험이 있다. 따라서 수량을 줄이더라도 네 compiler
variant 모두에서 target-specific evidence가 관찰되는 pair만 사용한다.

# Strict Policy

- 대상 variant: GCC·Clang × `O0/O2`
- 모든 variant에서 target operation 또는 target에 특이적인
  present/not_observed contrast가 관찰되어야 한다.
- generic control flow 차이만으로 PASS를 부여하지 않는다.
- 최적화 후 target operation이 사라지면 FAIL이다.
- `CWE-476` null dereference와 `CWE-563` unused assignment처럼
  현 toolchain에서 O2가 핵심 연산을 제거한 범주는 현재 공급에서 제외한다.
- decompile 또는 target-function link가 하나라도 실패하면 pair 전체를
  제외한다.
- 검토 대상 pair ID와 CWE 목록의 SHA-256을 decision config에 고정한다.

# Corrected Results

| 범위 | 이전 판정 | strict 재감사 |
| --- | ---: | ---: |
| B0 145 pair | PASS 100 / FAIL 45 | PASS 99 / FAIL 46 |
| F7 pilot 250 pair | PASS 206 / FAIL 44 | PASS 198 / FAIL 52 |
| 과거 누적 | PASS 306 / 395 | PASS 297 / 395 |

정정된 9쌍은 과거 PASS 중 O2에서 `CWE-476` 또는 `CWE-563`의
target-specific operation이 사라진 사례다. 과거 FAIL은 보수적으로
유지했다.

# First 500-pair Scale Batch

| 항목 | 결과 |
| --- | ---: |
| compile | `2,000/2,000` |
| decompile·function link | `1,997/2,000` |
| target-preservation | `420/500`, `0.840` |
| batch gate `≥0.90` | `FAIL — replace 80 pairs` |
| raw payload·object 실행 | `0` |

탈락 80쌍 중 `CWE-476` 18쌍과 `CWE-563` 19쌍은 범주 전체가
최적화 소실로 제외됐다. 나머지는 개별 compiler variant에서 target
operation 또는 pair contrast가 보존되지 않은 사례다.

# Second 500-pair Scale Batch

| 항목 | 결과 |
| --- | ---: |
| compile | `2,000/2,000` |
| decompile·function link | `1,997/2,000` |
| target-preservation | `394/500`, `0.788` |
| batch gate `≥0.90` | `FAIL — replace 106 pairs` |
| raw payload·object 실행 | `0` |

탈락 106쌍에는 `CWE-476` 5쌍과 `CWE-563` 23쌍이 포함됐다. 나머지는
네 variant 중 하나에서 buffer operation, allocation과 release의 차이,
unchecked dereference 또는 mismatched deallocation이 사라진 사례다.
GCC O2에서 target function을 연결하지 못한 CWE-126 세 쌍도 보수적으로
pair 전체를 제외했다.

# Third 500-pair Scale Batch

| 항목 | 결과 |
| --- | ---: |
| compile | `2,000/2,000` |
| decompile·function link | `1,996/2,000` |
| target-preservation | `410/500`, `0.820` |
| batch gate `≥0.90` | `FAIL — replace 90 pairs` |
| raw payload·object 실행 | `0` |

탈락 90쌍은 `CWE-563` 전체 13쌍과 개별 O2 변형에서 target evidence가
사라진 77쌍이다. 원래 함수 호출이 직접 load/store로 낮아졌더라도
할당·객체 경계와 초과 접근 관계가 pseudo-C에 남으면 승인했다. 반면
상수 대입이나 출력만 남아 경계 관계를 복원할 수 없는 변형은
보수적으로 pair 전체를 제외했다. CWE-126 네 쌍은 GCC O2 target
function decompile/link 실패로 제외했다.

# Supply Decision

strict 재감사와 네 확대 배치를 합친 결과는 다음과 같다.

네 번째 500-pair 확대는 compile `2,000/2,000`,
decompile·function link `1,996/2,000`, target-preservation
`419/500`을 기록했다. 81쌍은 O2 target evidence 소실로 교체한다.
이를 포함한 최신 누적은 다음과 같다.

| 항목 | 결과 |
| --- | ---: |
| 구조 적격 전체 공급 | `4,643 pairs` |
| 누적 검토 / 승인 / 탈락 | `2,395 / 1,940 / 455` |
| 관측 승인률 | `0.81002` |
| Wilson 95% 승인률 하한 | `0.79382` |
| 목표 | `2,450 accepted pairs` |
| 추가 필요 승인 | `510` |
| 하한 기준 예상 추가 검토 | `643` |
| 남은 구조 공급 | `2,248` |
| 보수적 공급 margin | `1,605` |
| 결정 | `PASS — fifth 500-pair batch authorized` |

개별 batch의 90% gate 실패와 전체 공급 gate PASS는 다른 판정이다.
실패 pair는 버리되, 남은 후보만으로 목표 수량을 보수적으로 확보할 수
있으므로 다음 500-pair batch를 진행한다.

# Next Actions

1. SHA-256 `7d0fdaf0…996f`의 다섯 번째 500-pair queue를 동결한다.
2. 같은 toolchain과 strict policy로 compile→decompile→명시 검토한다.
3. batch 뒤 Wilson 하한과 공급 margin을 다시 계산한다.
4. 승인 pair가 2,450개에 도달하기 전에는 binary adapter를 학습하지 않는다.
5. 최종 materialization에서 strict 재감사 탈락 pair를 모두 제외한다.

# Related Concepts

- [Phase F 실행 계획](../repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [수동 파인튜닝 검증 워크북](../repos/AegisLM-B200/docs/FINETUNING_TEST_WORKBOOK.md)
- [Q1R11 신규 Blind 500 PASS 결정](aegislm_q1r11_fresh_blind_pass_decision_20260730.md)
- [데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md)

# Evidence

- Draft PR: [AegisLM-B200 #3](https://github.com/Malicious-code-detection-project/AegisLM-B200/pull/3)
- B0 strict summary SHA-256:
  `fde1e20b257806eef96fc859010b74fd0c3b9fadfcd6168bd3422790cbb4db9f`
- pilot strict summary SHA-256:
  `26eb2d76f6d8bde2ac5cfa9df064dff7ec10989abe72b1cea6985fc9ccc8b223`
- first 500-pair summary SHA-256:
  `2c0d09ae26f94610ef28450a973d3112197e61c723c87b062ffdb98d17c0d06d`
- second 500-pair summary SHA-256:
  `ad4e87f2e0b519c216a0533a6388cc3b2cba6dde9d87d36e4db666b0803eaa30`
- third 500-pair compile summary SHA-256:
  `e556e746346839aa2181cebf3e621de19937bad67671aec48edd662943041422`
- third 500-pair decompile summary SHA-256:
  `bfdff41c7ce3e9df59936bed1f0643b6ca30075dbc53e9d0b99e727b8a529587`
- third 500-pair summary SHA-256:
  `11ab07b6106096f069e96b60f6311761a20d3fadbaca35b547c1786688b716d0`
- cumulative supply summary SHA-256:
  `4426bcdcc0a4b6cb694150ec87ad68f5f502c246e7ffaba30ef5829ffdfa5403`
- next queue SHA-256:
  `7d0fdaf011b815f116f65cb0f7794d1a4e5bc110243a00eff2e129cfd895996f`
