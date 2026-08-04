---
type: Decision Note
title: AegisLM CVEfixes Patch-label 공급 Gate 결정
description: CVEfixes v1.0.8 공급량 PASS 뒤 patch↔CWE 수동 11/28 FAIL EARLY와 direct-label 학습 거부 기록
tags: [aegislm, phase-f, cvefixes, dataset-quality, manual-review]
timestamp: 2026-07-31
status: active
---

# Summary

CVEfixes v1.0.8 official archive를 검증해 방어적으로 SQLite DB로
가져왔고, read-only 감사에서 C/C++ exact before/after 후보 6,248쌍을
확인했다. 숫자형 CWE만 허용한 200쌍 catalog와 함수 전·후 review queue의
자동 구조 gate는 통과했다. 그러나 patch↔CWE 수동 검토는 28건에서
오류·불확실 11건으로 예산 10건을 초과해 `FAIL EARLY`했다. 남은
172건은 미검토이며 학습은 승인하지 않는다.

# Why it matters

commit-level CVE/CWE가 붙어 있다는 사실만으로 특정 함수 변경이 해당
취약점을 수정했다는 뜻은 아니다. 자동 pair 연결과 수량 PASS를 실제
학습 label 품질 PASS로 오해하면 ARVO에서 확인한 오류를 반복하게 된다.

# Verified Lifecycle

- official archive: `12,708,711,268` bytes
- archive MD5: `4586a358977acfa4c60b1a2cdd096221`
- archive SHA-256:
  `6acd55aaeb7ffcfc20fdcebf7df88d206f9892ef64b0f2a2e06864d5b44b3a83`
- ZIP inventory: 15 members, unsafe 계수 0
- gzip CRC와 51.8 GB 정적 SQL 감사: PASS
- imported DB: 51.7 GB, `quick_check=ok`
- DB SHA-256:
  `4cfba1ef46e363f702f4e72a7ca36e9afc70493a3adb798816f02e24ca60e84a`
- source code·PoC·object 실행: 0

# Supply Result

- exact before/after method pairs: 78,963
- single-CWE pairs: 70,589
- C/C++ 후보: 6,248
- actionable 숫자형 CWE 후보: 5,569
- final sample: C 150, C++ 50, commit group 200개, CWE 56개
- 선택 함수 materialization: 200/200, 구조 오류 0, 동일 pair 0
- review queue SHA-256:
  `8e73ac22f02127a14279d383d4ff529fa750f947355844240776486854429b2a`

# Decision

현재 상태는 `manual_review_fail_early / training=false`다.

- reviewed / passed / error / unfinished: `28 / 17 / 11 / 172`
- CWE mismatch: 7
- CWE too broad: 6
- insufficient context: 5
- patch unrelated: 1
- operator decisions SHA-256:
  `08aed98de897f8081cd8871d795d6f8480f6e810b4f97b263b71259496a969a1`
- final result SHA-256:
  `ed099b23b6cf619b5ea717ff4b52119c7149b87165a8c57b26ee11a4bb6172be`

CVEfixes database의 CC BY 4.0을 원 repository source code license로
간주하지 않는다. 이번에는 품질 gate가 먼저 실패했으므로 repository
license gate에도 착수하지 않는다.

# Next Actions

1. CVEfixes commit-level CWE를 direct training label로 사용하지 않는다.
2. 재사용하려면 code-local operation 기반 label contract를 새로 만든다.
3. 새 contract는 새로운 고정 sample로 자동·수동 gate를 다시 시작한다.
4. vulnerability label 공급과 source–binary alignment 공급을 계속 분리한다.

# Related Concepts

- [Phase F 구현 계획](../repos/AegisLM-B200/docs/experiments/plans/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [Patch-label 공급 결정 원문](../repos/AegisLM-B200/docs/experiments/decisions/phase-f/PHASE_F_PATCH_LABEL_SUPPLY_DECISION_20260731.md)
- [Binary Model-Ready Target Gate](aegislm_binary_model_ready_target_gate_decision_20260731.md)

# Citations

- [CVEfixes official repository](https://github.com/secureIT-project/CVEfixes)
- [CVEfixes v1.0.8 Zenodo record](https://zenodo.org/records/13118970)
- [MegaVul official repository](https://github.com/Icyrockton/MegaVul)
