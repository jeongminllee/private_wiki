---
type: Decision Note
title: AegisLM CVEfixes Patch-label 공급 Gate 결정
description: CVEfixes v1.0.8 무결성·SQLite·6,248쌍 공급 감사와 200쌍 수동 gate 대기 기록
tags: [aegislm, phase-f, cvefixes, dataset-quality, manual-review]
timestamp: 2026-07-31
status: active
---

# Summary

CVEfixes v1.0.8 official archive를 검증해 방어적으로 SQLite DB로
가져왔고, read-only 감사에서 C/C++ exact before/after 후보 6,248쌍을
확인했다. 숫자형 CWE만 허용한 200쌍 catalog와 함수 전·후 review queue의
자동 구조 gate는 통과했다. 그러나 patch↔CWE 수동 판단 200건과 원
repository code license 검토가 남아 있어 학습은 승인하지 않는다.

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

현재 상태는 `manual_review_ready / training=false`다. 각 pair에서 같은
기능 단위인지, 수정 operation과 target CWE가 직접 연결되는지,
구체적인 다른 CWE가 맞는지, 문맥 부족으로 불확실한지를 검토한다.
오류·불확실이 `10/200`을 초과하면 `FAIL EARLY`로 종료한다.

CVEfixes database의 CC BY 4.0을 원 repository source code license로
간주하지 않는다. 수동 품질 gate를 통과하더라도 repository code license
검토가 끝나기 전에는 bulk materialization과 training을 허용하지 않는다.

# Next Actions

1. 200쌍 수동 patch↔CWE review를 완료한다.
2. 오류 유형과 CWE별 실패 분포를 기록한다.
3. 품질 PASS일 때만 repository license를 감사한다.
4. 두 gate가 모두 통과해야 binary-derived build feasibility로 이동한다.

# Related Concepts

- [Phase F 구현 계획](../repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [Patch-label 공급 결정 원문](../repos/AegisLM-B200/docs/PHASE_F_PATCH_LABEL_SUPPLY_DECISION_20260731.md)
- [Binary Model-Ready Target Gate](aegislm_binary_model_ready_target_gate_decision_20260731.md)

# Citations

- [CVEfixes official repository](https://github.com/secureIT-project/CVEfixes)
- [CVEfixes v1.0.8 Zenodo record](https://zenodo.org/records/13118970)
- [MegaVul official repository](https://github.com/Icyrockton/MegaVul)
