---
type: Decision Note
title: AegisLM BinKit 2.0 Metadata Gate 결정
description: compiler matrix는 확인했지만 고정 dataset artifact·license·schema 부재로 binary와 pickle을 보류한 기록
tags: [aegislm, phase-f, binkit, binary, metadata]
timestamp: 2026-07-31
status: active
---

# Summary

BinKit 2.0의 compiler·architecture·optimization matrix는 Phase F 강건성
실험 설계에 적합하다. 그러나 실제 precompiled dataset과 함수 pickle이
GitHub release asset이 아닌 Google Drive 링크로만 배포되고, size,
checksum, dataset license, row schema가 없어 다운로드하지 않는다.

# Verified Strengths

- release: `v2.0.0`
- commit: `82bc979122843d3f3953bc02cfc3cc359935ceb8`
- build-script license: MIT
- binaries: 371,928
- option combinations: 1,904
- architectures / compilers / optimizations: `8 / 23 / 6`
- documented missing binaries: 8

# Blockers

- GitHub release dataset asset: 0
- Google Drive artifact revision binding: 없음
- artifact size·SHA-256: 없음
- compiled dataset license: 확인 불가
- sample·source-package·function schema: 확인 불가
- pickle 안전 변환 절차: 없음

repository MIT license를 compiled GNU package와 extracted function feature의
license로 확대 적용하지 않는다. Python pickle은 로드 시 임의 코드가
실행될 수 있으므로 신뢰 전 역직렬화하지 않는다.

# Decision

최종 disposition은 `metadata_hold`다.

- binary download: false
- pickle download/deserialization: false
- processing: false
- training: false

metadata preflight SHA-256:
`285c0e514b2c958620f7b060d5b0e3817df9423133e0a7f4acd7a99974c76530`

# Next Actions

1. upstream이 versioned artifact, checksum, dataset license, row schema를
   제공하면 새 preflight를 수행한다.
2. compile matrix는 자체 build quota 설계 참고 자료로만 사용한다.
3. 다음 후보 EMBER2024를 독립 malware static-feature benchmark 관점에서
   감사한다.

# Related Concepts

- [Phase F 구현 계획](aegislm_phase_f_experiment_plan_20260728.md)
- [BinKit 결정 원문](aegislm_binkit_metadata_decision_20260731.md)
- [Assemblage Metadata Gate](aegislm_assemblage_metadata_decision_20260731.md)

# Citations

- [BinKit repository](https://github.com/SoftSec-KAIST/BinKit)
- [BinKit v2.0.0 release](https://github.com/SoftSec-KAIST/BinKit/releases/tag/v2.0.0)
