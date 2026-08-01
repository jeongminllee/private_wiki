---
type: Decision Note
title: AegisLM Assemblage LinuxELF Metadata Gate 결정
description: artifact와 schema는 통과했지만 strict complete metadata가 0건이라 raw ELF와 학습을 거부한 기록
tags: [aegislm, phase-f, assemblage, binary, provenance]
timestamp: 2026-07-31
status: active
---

# Summary

Assemblage LinuxELF의 고정 compressed DuckDB metadata를 검증하고 read-only
schema·집계 감사를 수행했다. artifact와 5개 table schema는 통과했지만
repository license, architecture, build trace를 같은 행에서 모두 만족하는
strict complete row가 0건이어서 raw ELF 다운로드와 학습을 승인하지
않는다.

# Why it matters

metadata 컬럼이 존재한다는 사실과 학습에 필요한 provenance가 완전하다는
사실은 다르다. 서로 다른 schema 세대의 행을 섞은 채 dataset-level
설명으로 결손을 추정하면 compiler-robustness 실험의 원인을 통제할 수
없다.

# Verified Artifact

- revision: `5d58b08b500ea279a9880f80fd4b217e1897035a`
- compressed bytes: `21,971,861,569`
- compressed SHA-256:
  `a5b12c3353cd0f653c9543e78343b45dca4207f072a7d5d17b2ab07a4540eb5e`
- decompressed bytes: `136,143,712,256`
- DuckDB SHA-256:
  `767b69efe0443827167f152a86ee04a04ab494cd186404503e3e64f9d25449ef`
- DuckDB client: `1.5.5`, read-only
- raw ELF 다운로드·실행: `0`

# Field Result

- binary rows: `249,121`
- repository URL: 100%
- actionable license 상한: 70.9069%
- compiler: 99.8772%
- optimization: 100%
- architecture: 68.8404%
- binary format·repo commit·build mode: 약 31.15%
- build trace without architecture: `63,031`
- architecture without complete trace: `113,329`
- strict complete rows: `0`

`other/Other/unknown`을 제외한 license 비율도 법적 허용 목록이 아니라
추가 검토 가능한 최대 상한이다.

# Decision

최종 disposition은 `metadata_reference_only`다.

- schema·provenance 연구 참고: 승인
- raw ELF archive 다운로드: 불승인
- binary subset materialization: 불승인
- training: 불승인

# Next Actions

1. Assemblage upstream이 동일 행에 architecture와 build trace를 제공하는
   새 snapshot을 내면 새 revision으로 재감사한다.
2. 현재 raw ELF archive는 받지 않는다.
3. 다음 후보 BinKit 2.0의 compiler·architecture·optimization metadata
   계약을 먼저 감사한다.
4. BinKit도 metadata gate 전에는 binary package를 다운로드·실행하지
   않는다.

# Related Concepts

- [Phase F 구현 계획](../repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [Assemblage 결정 원문](../repos/AegisLM-B200/docs/PHASE_F_ASSEMBLAGE_METADATA_DECISION_20260731.md)
- [Decompile-Bench Alignment·Provenance Gate](aegislm_decompile_bench_alignment_decision_20260731.md)

# Citations

- [Assemblage LinuxELF dataset card](https://huggingface.co/datasets/changliu8541/Assemblage_LinuxELF)
- [Assemblage dataset access documentation](https://assemblagedocs.readthedocs.io/en/latest/dataset.html)
- [Assemblage dataset site](https://assemblage-dataset.net/)
