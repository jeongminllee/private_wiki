---
type: Decision Note
title: AegisLM Binary Model-Ready Target Gate 결정
description: Binary target 반복 실패, strict v7 공급 차단, ARVO 200건 patch gate FAIL EARLY를 연결한 학습 불승인 기록
tags: [aegislm, phase-f, binary-analysis, dataset-quality, manual-review]
timestamp: 2026-07-31
status: active
---

# Summary

Phase F F7의 compile·decompile·relation 공급 성공은 곧바로 학습 승인을
뜻하지 않는다. model-ready target v1은 자동 gate를 통과했지만 고정
100건 수동 검토에서 여섯 번째 명백한 evidence 오류에 도달해
`FAIL EARLY`로 판정했다. 이후 v2·v3·v4도 새로운 고정 100건에서 각각
같은 중단 기준에 도달했다. strict v5는 recovery r4·r5로 자동 공급
2,450쌍을 확보했지만 fixed remediation과 constrained sink를 함께
인용하지 못한 오류 6건으로 수동 gate에 다시 실패했다.

v6는 두 역할을 모두 요구해 공급 `2,123/2,450`으로 실패했다. 탈락
pseudo-C 감사에서 Ghidra 표현을 놓친 false reject가 확인되어, 동일
보안 근거를 정규화한 `decompiler-normalized-role-evidence-v7`을
도입했다. recovery r6 뒤 v7은 자동 공급을 통과했지만 수동 연결 오류가
발견됐다. v8 동일 변수 연결은 공급 실패, v9 memory write→read 연결은
자동 PASS 뒤 수동 evidence 오류 6건으로 실패했다. 다음 결정은 flat
evidence를 role-structured contract로 교체하는 것이다.

# Why it matters

자동 검사는 JSON Schema, prompt 누출, split, duplicate, tokenizer
cutoff처럼 기계적으로 판정 가능한 오류를 차단한다. 그러나 finding이
실제 CWE 관계를 가르치는지는 별도 수동 검토가 필요하다.

예를 들어 다음 출력은 schema가 유효해도 학습 target으로는 실패다.

- CWE-23에 buffer NUL 초기화만 인용하고 `fgets → open`을 누락
- CWE-401 fixed에 `malloc`만 인용하고 `free`를 누락
- CWE-121에 source size만 인용하고 작은 destination으로의 copy를 누락
- CWE-762 fixed 함수가 최적화되어 `return;`만 남았는데 정상 근거로 사용
- CWE-127 decompile 결과에서 underread boundary가 사라졌는데 label을 유지

# Gate Separation

| Gate | 질문 | 현재 결과 |
| --- | --- | --- |
| infrastructure | compile·decompile·function link가 가능한가 | PASS |
| relation | present/fixed 구분이 pseudo-C에 남아 있는가 | 2,510쌍 |
| automatic target | schema·semantic·token·누출 조건을 지키는가 | v2–v4 PASS |
| manual target | finding이 target CWE 관계를 실제로 설명하는가 | v1–v5 FAIL |
| strict supply | remediation과 sink가 모두 관찰되는가 | v6 2,123/2,450 FAIL |
| normalized supply | 동일 근거의 Ghidra 표현을 정규화했는가 | v7 2,450/2,468 |
| linked supply | 같은 변수·memory base의 write/read를 연결했는가 | v9 2,450/2,498 |
| final manual target | capacity·bound·guard·offset 역할이 보존되는가 | v9 6-error FAIL |
| training approval | 위 gate를 모두 통과했는가 | `false` |

# Target Iterations

| 버전 | 핵심 변경 | 판정 |
| --- | --- | --- |
| v1 | 단일 record의 target-like line 선택 | 수동 6-error 조기 FAIL |
| v2 | present/fixed pair contrast | 수동 6-error 조기 FAIL |
| v3 | source→sink와 remediation 관계 | 수동 6-error 조기 FAIL |
| v4 | CWE별 source-size·guard·release·fixed assignment | 수동 6-error 조기 FAIL |
| v5 | 근거 불충분 pair를 fallback 없이 제외 | 자동 PASS, 수동 6-error FAIL |
| v6 | fixed remediation과 constrained sink 모두 요구 | 공급 2,123/2,450 FAIL |
| v7 | Ghidra 이름·최적화·capacity 표현 정규화 | 기존 공급 2,329/2,450 |
| v8 | 초기화 변수와 같은 sink만 연결 | 공급 2,326/2,450 FAIL |
| v9 | 같은 memory base의 write→read 연결 | 자동 PASS, 수동 6-error FAIL |

각 실패 artifact와 hash-bound operator decision은 삭제하거나 정상으로
덮어쓰지 않는다.

# Strict v5 Policy

- present evidence는 CWE별 최소 target-operation 강도를 만족해야 한다.
- fixed evidence는 강한 remediation line 또는 pair-unique 안전 operation이
  있어야 한다.
- 중복 evidence line은 제거한다.
- `return;`만 남은 fixed representation은 제외한다.
- underread·underwrite boundary처럼 CWE 핵심 관계가 사라지면 제외한다.
- raw payload와 object 실행은 계속 0으로 유지한다.
- 공급이 부족하면 기준을 낮추지 않고 frozen queue에서 복구한다.

# Recovery r4–r6

| 항목 | 결과 |
| --- | ---: |
| frozen queue 선택 | 400 pair |
| queue SHA-256 | `858145ffa4ce779d9146a00281e911bfc584906b3fa07f3281f69f6491d8b9fb` |
| compile / symbol link | `1,600/1,600` |
| compile summary SHA-256 | `32a6140dd8589c6c6e58b4efd8d14b87d82e413ea9b6fbf3536fe5691f341ee0` |
| object 실행 | `0` |
| r4 relation 추가 | `253 pair` |
| r5 queue / relation 추가 | `64 / 45 pair` |
| v5 최종 공급 | `2,450/2,477`; 자동 PASS |
| v5 수동 판정 | evidence error 6건; `FAIL EARLY` |
| v6 공급 | `2,123/2,450`; 327 부족 |
| v7 기존 공급 | `2,329/2,450`; 121 부족 |
| r6 queue / SHA-256 | `260 pair` / `a7a8bab1…6350` |
| r6 compile / symbol / 실행 | `1,040/1,040` / `1,040/1,040` / `0` |
| r6 decompile / function link | `1,040/1,040` / `1,040/1,040` |
| r6 relation-qualified | `176/260` |
| v7 최종 공급 | `2,450/2,468`; 자동 PASS, 수동 연결 오류 |
| v8 공급 | `2,326/2,450`; FAIL |
| v9 공급 | `2,450/2,498`; 자동 PASS |
| v9 수동 판정 | evidence error `6/100`; `FAIL EARLY` |

v5 최종 tokenizer gate SHA-256은
`ed561365cf46bbd95d347b3d745278aedb7f8baa181097be5800f9758d3ead2d`다.

# Decision

1. v9와 이전 실패 artifact를 그대로 보존한다.
2. flat evidence array를 `source / control / sink / bound / remediation`
   role과 관계가 명시된 versioned contract로 교체한다.
3. 새 계약으로 model-ready dataset과 고정 100건을 다시 생성한다.
4. 수동 label/evidence 오류율 `≤0.05` 전에는 Qwen 80B binary canary를
   학습하지 않는다.
5. contract 재설계 뒤에도 공급이 부족하면 신규 원천 데이터 확보 또는
   승인 규모 축소를 별도 연구 결정으로 다룬다.

첫 구현으로 `aegislm.binary-role-assessment-output.v2` schema와 semantic
validator를 추가했다. evidence마다 exact span과
`source/control/sink/bound/remediation` role을 요구하고, relation이
role과 호환되며 실제 sink에 연결되는지 검사한다. 기존 v1 artifact는
변경하지 않으며 다음 작업은 v2 target builder다.

# Role Target v2 실행 결과

v2 r1과 r2는 pair 기반 target builder, v2 전용 prompt, 실제 Qwen
tokenizer gate, 고정 seed 100건 검토까지 실행했다.

| Iteration | 자동 공급 | Gate SHA | 수동 판정 |
|---|---:|---|---:|
| v2 r1 | `2,450/2,479` | `9b48a00c…577a` | `6/100 FAIL EARLY` |
| v2 r2 | `2,450/2,485` | `bf910417…f703` | `6/100 FAIL EARLY` |

r1의 buffer/format/numeric source 오연결은 r2에서 교정했지만, r2에서는
path construction, unbounded work, missing release, initialization,
invalid pointer origin, untrusted loop bound가 identifier-overlap만으로
잘못 연결됐다.

따라서 “2,450쌍 확보”는 target 품질을 증명하지 못한다. 다음 iteration은
generic fallback을 폐기하고 CWE별 완전한 role extractor가 있는 범주만
eligible로 다시 집계한다. 공급이 줄면 실제 수량에 맞춰 dataset 규모를
축소하며 새 100건 gate 통과 전에는 materialization과 GPU 학습을 하지
않는다.

후속 strict v3는 generic fallback을 완전히 제거해 `1,301/2,924` pair를
확보했다. original quota는 실패했지만 review 가능한 규모였고, 고정
100건에서 CWE-124/127/457/690 extractor 오류 6건으로 다시
`FAIL EARLY`했다. 네 CWE는 quarantine하며 남은 extractor도 새 gate 전에는
학습에 사용하지 않는다.

# Strict v4–v7 최종 판정

실패 CWE만 iteration별로 추가 격리해 extractor 범위를 좁혔다.

| Iteration | 적격 pair | 수동 판정 | 추가 격리 |
|---|---:|---:|---|
| strict v4 | `1,228` | `6/100 FAIL EARLY` | CWE-121 |
| strict v5 | `928` | `6/100 FAIL EARLY` | CWE-122 |
| strict v6 | `661` | `6/100 FAIL EARLY` | CWE-126 |
| strict v7 | `644` | `1/100 PASS` | 없음 |

strict v7은 CWE-134/190/191/194/195에 한해 target 근거 품질을
통과했다. 하지만 공급 목표 `2,450` pair에는 미달하므로
`quality-approved / supply-blocked` seed로 동결한다.

이는 품질 실패가 아니다. 반대로 저신뢰 CWE를 되살리지 않았기 때문에
남은 수량이 줄어든 결과다. 따라서 현 단계에서 binary materialization과
adapter 학습은 시작하지 않는다. 다음 연구는 동일 5개 CWE의 독립 공급을
확대하거나, 격리된 CWE extractor가 allocation·source length·read length를
완전하게 연결하도록 재설계하는 것이다.

최종 tokenizer gate SHA-256은
`d9305d43939e355a968217dd426f6cc7ba10426a2a51dabeebfba146216efd35`,
review manifest SHA-256은
`865789a5f15aaffc1965eb63e8d514cbe018dd53ca8dcf11f6b4d6c67bb96cde`다.

# 다음 단계: ARVO Buffer Feasibility

기존 SARD frozen queue는 모두 소진됐고 BigVul·PrimeVul의 승인 CWE
verified pair도 최대 약 281쌍이어서 strict v7 부족분을 채우지 못한다.
따라서 ARVO v3 metadata 6,138건을 확보해 격리된 CWE-121/122/126
extractor를 실제 patch 관계로 복구하는 방향으로 전환했다.

heap/stack buffer read·write에서 각 50건, 총 200건을 프로젝트 다양성
기준으로 선택했다. sanitizer crash type은 CWE gold가 아니므로 전부
quarantine이며, patch URL·fix commit과 allocation/source length/sink
관계를 사람이 확인하기 전에는 compile·decompile·학습하지 않는다.

DB SHA-256은
`331184ca807c2f136f98dac9f1df94c893f4ee2fdf9329dca517ff88e72f97ce`,
metadata audit SHA-256은
`b562ac2dc2882c6a70219d0b57bf2fd0603807064fca3c8f02ae3d60c35e8a66`다.
PoC/raw payload 읽기, Docker pull, reproducer/object 실행은 모두 0이다.

# ARVO Patch Gate 최종 판정

metadata audit 뒤 공개 GitHub 개발자 패치만 수집하는 별도 gate를
실행했다. repository+commit을 중복 제거하고 C/C++ source hunk가 있는
패치만 남겨 family별 50건, 총 200건을 다시 동결했다.

| 항목 | 결과 |
|---|---:|
| metadata 후보 | `2,675` |
| GitHub patch 후보 | `2,144` |
| 최종 고유 patch | `200/200` |
| Git binary patch 자동 제외 | `13` |
| C/C++ source hunk 없음 자동 제외 | `5` |
| 수동 오류 예산 | `10/200` |
| 확정 오류 | `11/200` |
| 최소 오류율 | `5.5%` |
| 최종 판정 | `FAIL EARLY` |
| 학습 승인 | `false` |

오류 11건이 확인된 뒤 남은 189건을 모두 정상으로 가정해도 5% gate를
회복할 수 없으므로 검토를 중단했다. 미검토 레코드는 PASS로 간주하지
않는다.

확정 오류에는 보안 수정과 무관한 spelling·numeric correction, ASAN
instrumentation 비활성화, stale-object/decode failure 처리, 주장된
heap/stack read/write와 다른 patch, 국소화되지 않은 WIP 변경이 포함됐다.
따라서 ARVO sanitizer `crash_type`을 CWE-121/122/126 gold label로
변환하지 않으며 binary compile/decompile과 adapter 학습을 계속 보류한다.

다음 공급 감사는 역할을 분리한다.

- MegaVul/CVEfixes: patch-localized CWE label 공급 후보
- Assemblage/Decompile-Bench: source–binary representation alignment 후보

alignment dataset에 vulnerability gold label이 있다고 가정하지 않는다.
세부 artifact hash와 안전 경계는
[ARVO Patch Gate 결정문](../repos/AegisLM-B200/docs/PHASE_F_ARVO_PATCH_GATE_DECISION_20260731.md)에
보존한다.

# Related Concepts

- [AegisLM Binary 엄격 Target Evidence 재감사](aegislm_binary_strict_target_evidence_decision_20260730.md)
- [AegisLM Phase F 연구 계획](aegislm_phase_f_experiment_plan_20260728.md)
- [Phase F 데이터셋 및 바이너리 실험 계획](../repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [파인튜닝 테스트 워크북](../repos/AegisLM-B200/docs/FINETUNING_TEST_WORKBOOK.md)
- [Binary Role Target v2 결정](../repos/AegisLM-B200/docs/PHASE_F_BINARY_ROLE_TARGET_DECISION_20260731.md)
- [ARVO Patch Gate 결정](../repos/AegisLM-B200/docs/PHASE_F_ARVO_PATCH_GATE_DECISION_20260731.md)

# Citations

- AegisLM-B200 로컬·원격 평가 artifact와 hash-bound manual review decision
- NIST SARD/Juliet C/C++ 1.3 source corpus
