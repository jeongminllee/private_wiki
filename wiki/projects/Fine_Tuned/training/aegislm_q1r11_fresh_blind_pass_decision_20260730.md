---
type: Decision Note
title: AegisLM Q1R11 신규 Blind 500 PASS와 Source 후보 동결
description: Q1R10/Q1R11 신규 500건과 BF16 merge·vLLM lifecycle PASS, F6 binary B0 100-pair PASS를 기록
tags: [aegislm, phase-f, qwen, blind-evaluation, source-security]
timestamp: 2026-07-30
status: active
---

# Summary

> **2026-07-30 정정:** 이 문서의 F6-B 100-pair PASS는 최초 판정이다.
> F7 엄격 정책을 소급 적용한 결과 CWE-563 1쌍을 추가 격리해 B0는
> 99/145로 정정됐다. 이후 binary 공급 계산은
> [Binary 엄격 Target Evidence 재감사 결정](aegislm_binary_strict_target_evidence_decision_20260730.md)을
> 따른다.

Qwen3-Coder-Next 80B의 Q1R10 decision 100-step과 Q1R11 evidence
100-step을 순차 실행한 source pipeline이 신규 blind 500건의 고정 절대
gate를 모두 통과했다.

이 결과로 두 adapter를 source model-only 채택 후보로 동결했다. 추가
250-step이나 313-step 학습은 수행하지 않는다. 두 adapter의 개별 BF16
merge와 vLLM TP2 F5-M1도 완료했으며, evidence endpoint는 guided JSON
Schema와 semantic validator를 필수조건으로 사용할 때 전체 gate를
통과했다.

# Confirmed Facts

## Data boundary

- 평가 자료: `phase-f-source-fresh-blind-500-v1`
- 수량: 250 pair, 500 records, `present/not_observed=250/250`
- 기존 학습·validation·평가 group overlap: `0`
- 기존 code hash overlap: `0`
- model-visible label leakage: `0`
- 최대 Qwen token: `1,442/2,048`
- Q1R11 dev100 gate 전에는 challenge를 모델에 전달하지 않음
- 독립 재빌드에서 source와 contract hash inventory가 byte-identical

## Q1R11 training

- base-start 100 optimizer steps, global batch `32`, resume 없음
- train/validation: `9,975/996`
- runtime: `2,969.24초`
- train loss: `0.1035507`
- aggregate GPU peak: `209,624 MiB`
- adapter SHA-256:
  `c68c4af73248a2f2b3da52cb6be18573cced78d17a108a146cfab938457451e0`
- 저장·외부 mirror·재로드·HF API: PASS

## Blind 500 automatic gates

| 항목 | 결과 |
| --- | --- |
| decision TP/TN/FP/FN | `250/247/3/0` |
| decision precision/recall/FPR | `0.9881/1.0000/0.0120` |
| decision parse/schema/abstention | `1.0000/1.0000/0` |
| evidence precision/recall/F1 | `0.9001/0.9229/0.9114` |
| evidence parse/schema/renderer | `1.0000/1.0000/1.0000` |
| pipeline latency p50/p95 | `4,239.48/5,330.96 ms` |
| HTTP | decision `500×200`, evidence `500×200`, non-200 `0` |
| final result | **PASS** |

평가 artifact `SHA256SUMS`의 SHA-256은
`c460afcf76ef845cd23113d8f0820a2d6d667cbd68994af8e810381bf706eef1`이다.

# Error Audit

Decision false positive는 3건이고 false negative는 0건이다.

1. `sard-ed213928edf7351c-not_observed`, `CWE-690`
   - allocation 뒤 null guard가 있지만 `present`로 과판정했다.
2. `sard-2b4b6c5b89f8d61e-not_observed`, `CWE-789`
   - network-derived size를 사용하지만 allocation 조건이 `<100`으로
     제한됐는데 `present`로 과판정했다.
3. `sard-ed879b9acd94a217-not_observed`, `CWE-122`
   - 100-wide destination과 99-character null-terminated source의
     경계를 `present`로 과판정했다.

Evidence는 모든 record에서 gold line과 최소 한 줄 이상 겹쳤다.
`present` 조건의 line P/R은 `0.9234/0.9145`,
`not_observed` 조건은 `0.8765/0.9322`였다. Schema와 renderer 실패는
없었다.

# Manual Review

고정 seed `20260730`으로 올바른 TP 10건과 TN 10건을 추출해 코드,
target CWE, decision, gold/predicted evidence line을 함께 읽었다.

- benchmark label과 decision 적합: `20/20`
- gold evidence와 overlap: `20/20`
- gold와 exact line-set 일치: `9/20`
- 과도한 공격 지침: `0/20`
- confidence: `high 20/20`

모델이 직접 생성하는 것은 decision과 line range이며 최종 설명·제약·권고는
deterministic renderer가 만든다. 현재 recommendation은 “정적 분석과
사람 검토로 재확인”이라는 일반 문구이므로 구체적인 수정 방안의 유용성은
검증되지 않았다.

# Decision

1. Q1R10 decision과 Q1R11 evidence를 source model-only 채택 후보로
   동결한다.
2. 같은 blind 500은 gold가 공개됐으므로 후속 모델 선택이나 threshold
   조정에 재사용하지 않는다.
3. Q1R10/Q1R11의 추가 학습 step은 수행하지 않는다.
4. 두 objective를 하나의 adapter로 임의 합치지 않는다.
5. 두 adapter의 개별 merge와 vLLM TP2 lifecycle은 완료했다.
6. Evidence endpoint는 guided JSON Schema와 semantic validator를
   배포 필수조건으로 둔다.
7. F6-A inventory와 사용자 영역 Clang+Ghidra toolchain 동결을 통과했고,
   F6-B 1-pair smoke 후 B0 후보 감사로 이동한다.

# Scope and Limitations

이번 PASS는 NIST SARD/Juliet 기반 C/C++ supplied-function에서 지정된
CWE의 `present / not_observed` 판단과 code line evidence 선택에 한정된다.

다음을 아직 증명하지 않는다.

- 실제 저장소와 장문·다중 함수 코드
- C/C++ 이외 언어
- 실행파일, pseudo-C, assembly, static feature 분석
- confidence calibration
- 구체적인 remediation 품질
- NuriLab, RAG, MCP 연결 효과
- production throughput와 두 endpoint 운영 구조

# Next Actions

1. target CWE가 최적화 뒤에도 보존되는 후보와 탈락 사유를 분류
2. 고정 seed로 B0 100 pair와 reserve manifest를 생성·감사
3. 승인된 manifest만 compile→decompile→normalized record로 materialize
4. B0 gate 통과 전 외부 binary corpus 다운로드 금지

# F5-M1 and F6 Preflight Update

- decision/evidence BF16 merged model은 각각 약 `149G`, shard `48/48`이다.
- merged inventory SHA-256은 decision `0c0f31ad…8fed`, evidence
  `20a4792e…86a`다.
- decision vLLM 500건은 HF raw output과 `500/500` 동일했다.
- evidence 자유 생성은 1건이 9-range를 출력해 schema/renderer
  `0.9980`으로 실패했다.
- guided JSON Schema constrained run은 parse/schema/renderer `1.00`,
  line P/R/F1 `0.8757/0.8783/0.8770`으로 확정 gate를 통과했다.
- vLLM peak는 GPU당 `171,268 MiB`, OOM/fatal/non-200은 0이었다.
- F5-M1 artifact `SHA256SUMS` SHA-256은 `fee515c5…ad1`이다.
- F6-A manifest SHA-256은 `af18ec72…ab9d`이며, SARD 원천은 승인됐다.
- 사용자 영역 Clang 18.1.3·Ghidra 12.1.2 toolchain manifest
  `0de66fb5…e502`를 동결했다.
- F6-B는 running이다. 첫 CWE-690 후보는 `O2`에서 target semantics가
  사라져 탈락했고, CWE-122 pair `eaa5bdf5be4b7f6b`는 GCC·Clang
  `O0/O2`의 8개 present/not_observed normalized record를 통과했다.
- smoke summary SHA-256은 `c9ed9183…0908`이다. 이 결과는 1-pair
  feasibility이며 B0 100-pair PASS가 아니다. 외부 payload download와
  sample execution은 0회다.
- Linux 비호환 309 pair를 제외한 candidate queue는 primary 100·reserve
  50, 37개 CWE, 최대 CWE 비중 3%이며 SHA-256은 `fcd8bbc7…198f`이다.
- 앞 10 pair compile canary는 GCC·Clang × `O0/O2` compile과
  target-symbol link `40/40`, 실행 0회로 decompile canary 조건을 통과했다.

## F6-B B0 100-pair 후속 판정

F6-B는 1-pair feasibility에서 멈추지 않고 B0 절대 gate까지 완료했다.
SARD/Juliet 후보 145 pair를 GCC·Clang × `O0/O2`로 compile·decompile한
뒤 target CWE 보존을 명시적으로 검토했다. 최적화 후 근거가 사라진
45 pair를 제외하고 최종 100 pair·400 variant를 승인했다.

- compile·decompile·source-function link: 승인 variant `400/400`
- normalized record: `800`, present/not_observed 각 `400`
- pseudo-C·bounded assembly·static feature linkage: 각각 `1.00`
- prompt provenance·gold label·source symbol 누출: `0`
- raw executable payload·object 실행: `0`
- B0 gate summary SHA-256:
  `73ade0fbf0970d7176e2d3ef7d069c243d2657ee9d6e86b4c226ef72a825b8dd`
- normalized records SHA-256:
  `737a9e399ca5004681e38739ca87e71f1dff19f9ea8e5de691d5f483041fe18c`

따라서 F7 차단 조건은 해제한다. 다음 단계는 binary adapter 학습 자체가
아니라 최대 2,000 pair의 검증 가능 공급량 감사, group-first split,
`O3 + stripped` robustness holdout과 validation/blind set 동결이다.
수량이 부족하면 저신뢰 pair로 채우지 않는다.

## F7 250-pair 공급 Pilot 후속 판정

구조 적격 4,643 pair queue를 동결한 뒤 별도 250 pair를 GCC·Clang ×
`O0/O2`로 처리했다. compile·symbol link는 `1,000/1,000`,
decompile·function link는 `999/1,000`이었다. 모든 pair를 명시적으로
검토해 206 pair를 승인하고, 최적화 variant에서 target 차이가 보존되지
않은 44 pair를 제외했다.

250-pair batch의 target-preservation rate `0.824`는 개별 batch 기준
`0.90`에 미달한다. 이 판정은 44 pair를 저신뢰 후보로 버린다는 뜻이며
F7 공급 전체가 실패했다는 뜻은 아니다. 과거 B0를 포함한 누적 결과는
검토 395, 승인 306, 탈락 89 pair다. Wilson 95% 하한 승인률
`0.73095`로 계산해도 추가 2,144개의 승인을 위해 2,934 pair 검토가
예상되고, 남은 구조 공급 4,248 pair 대비 1,314 pair의 여유가 있다.

따라서 공급 gate는 PASS로 판정하고 다음 500-pair queue를 승인한다.
각 500-pair batch 뒤 승인률과 Wilson 하한 margin을 다시 계산하며,
탈락 후보를 수량 충족 목적으로 복구하지 않는다. 250-pair pilot의
병렬 decompile은 약 23.1분, 중복 merged artifact 포함 약 106.9 MB였다.

- pilot review summary SHA-256:
  `9bd9d026224cce6347a8497bfbe2cf345fc514b4cdfb98dbeb36129d500d6e60`
- 누적 supply outcome SHA-256:
  `d58a5aad633b5180e0377e1354f96eef9bad911eda430beb6262098038be6bed`
- 다음 500-pair queue SHA-256:
  `20d1af8262634288992be7e3e663b0c0f2895d6e12de13258a4b2d79f07318bd`

# Related Concepts

- [Phase F 실행 계획](../repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [수동 파인튜닝 검증 워크북](../repos/AegisLM-B200/docs/FINETUNING_TEST_WORKBOOK.md)
- [절대평가 계획](../repos/AegisLM-B200/docs/EVALUATION_PLAN.md)
- [Q1R10 Blind 평가와 Evidence 보정 결정](aegislm_q1r10_blind_evaluation_decision_20260730.md)
- [데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md)

# Evidence

- Evaluation root:
  `artifacts/evaluation/phase-f-source-fresh-blind-500-v1/q1r10-q1r11-two-stage`
- Decision predictions SHA-256:
  `f1920618e0732c685573f09621e87292ae8bee68160cfb184eab3d52e8b02a9c`
- Evidence predictions SHA-256:
  `2806780d99a771e64f2c8b3a1cd2d64250b76d5c5a276be1ff1077c86d55f757`
- Final summary SHA-256:
  `2de686657c65e06625781fd6487493b832b1fb772bb33889ffdb606abf62fedc`
