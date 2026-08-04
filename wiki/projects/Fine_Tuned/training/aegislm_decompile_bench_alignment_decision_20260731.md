---
type: Decision Note
title: AegisLM Decompile-Bench Alignment·Provenance Gate 결정
description: source–assembly 정렬 96/100 PASS와 불완전한 provenance·build metadata로 reference-only 사용을 결정한 기록
tags: [aegislm, phase-f, decompile-bench, binary, provenance]
timestamp: 2026-07-31
status: active
---

# Summary

Decompile-Bench 고정 revision의 첫 Arrow shard에서 source–assembly 정렬
100건을 수동 검토했다. 96건이 같은 함수와 의미를 유지해 정렬 품질
gate는 통과했다. 그러나 전체 행의 repository provenance가 완전하지 않고
repository별 license, compiler, optimization metadata가 없어 binary
adapter 학습에는 승인하지 않는다.

# Why it matters

source와 assembly가 잘 맞는다는 사실은 표현 학습 가능성을 보여주지만,
상용화 가능한 학습 데이터의 출처·라이선스와 compiler variant 강건성을
자동으로 보장하지 않는다. 정렬 품질과 학습 적격성을 분리해야 좋은
benchmark를 근거 없는 학습 데이터로 확대 해석하는 일을 막을 수 있다.

# Verified Input

- dataset: `LLM4Binary/decompile-bench`
- revision: `4b708c2211cd7d4af403675db56322aa4ed7050c`
- shard: `data-00000-of-00017.arrow`
- bytes: `489,618,088`
- shard SHA-256:
  `2a68cfda840f0c1aa1b6846b78fa9cce961cd2da42be5043579c53c1f69332b5`
- rows: `131,359`
- exact duplicate rows: `1,298`
- raw binary·executable 실행: `0`

# Alignment Result

- review seed / size: `20260731 / 100`
- passed / error / unfinished: `96 / 4 / 0`
- 허용 오류 예산: 최대 `5/100`
- 오류 4건: 모두 `different_function + semantic_mismatch`
- review result SHA-256:
  `87104c7b9225820b2f0f935dcdd71ecf6a8cb0ad612908517ef70243c9bc2795`

# Provenance Result

- 명시 repository 행: `111,206 / 131,359` (`84.6581%`)
- 미복원 행: `20,153`
- 고유 명시 repository: `1,066`
- repository별 license evidence: 없음
- compiler·optimization metadata: 없음
- vulnerability label·patch ground truth: 없음
- provenance audit SHA-256:
  `68b4b51d3968a53bd711886e3d75ea02d9de5c8794c6eef733bb5b06c5525c36`

dataset card의 `CC0-1.0`과 “permissively licensed repositories” 설명을
개별 원본 repository의 행별 license 증거로 대체하지 않는다.

# Decision

최종 disposition은 `alignment_reference_only`다.

- source–assembly 정렬 회귀·representation 참고: 승인
- vulnerability label 공급: 불승인
- binary adapter 학습: 불승인
- `approved_for_training=false`

# Next Actions

1. 다음 공급 후보로 Assemblage metadata를 감사한다.
2. repository license, compiler, optimization, architecture가 행 단위로
   추적 가능한지 먼저 확인한다.
3. 전체 PE/ELF corpus나 executable은 다운로드·실행하지 않는다.
4. metadata gate가 통과한 뒤에만 필요한 소규모 함수 subset을 검토한다.
5. 취약점 label은 SARD/Juliet 또는 별도로 검증된 patch/CWE 근거에서만
   공급한다.

# Related Concepts

- [Phase F 구현 계획](aegislm_phase_f_experiment_plan_20260728.md)
- [Decompile-Bench 결정 원문](aegislm_decompile_bench_alignment_decision_20260731.md)
- [CVEfixes Patch-label 공급 Gate](aegislm_cvefixes_supply_gate_decision_20260731.md)
- [Binary Model-Ready Target Gate](aegislm_binary_model_ready_target_gate_decision_20260731.md)

# Citations

- [Decompile-Bench dataset card](https://huggingface.co/datasets/LLM4Binary/decompile-bench)
- [LLM4Decompile Decompile-Bench documentation](https://github.com/albertan017/LLM4Decompile/tree/main/decompile-bench)
- [Decompile-Bench paper](https://arxiv.org/abs/2505.12668)
