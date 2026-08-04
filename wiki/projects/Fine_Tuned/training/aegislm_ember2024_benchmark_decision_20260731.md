---
type: Decision Note
title: AegisLM EMBER2024 ELF Static-Feature Benchmark Gate 결정
description: ELF test 12,000행의 중복을 감사하고 6,000개 temporal observation으로 제한해 독립 malware benchmark를 승인한 기록
tags: [aegislm, phase-f, ember2024, binary, benchmark]
timestamp: 2026-07-31
status: active
---

# Summary

EMBER2024의 고정 ELF test artifact는 archive·schema·feature-shape gate를
통과했다. 다만 원본 12,000행에는 동일 `(week_id, sha256)` 중복 6,000행이
있으므로 6,000개의 temporal observation으로 중복 제거한 독립 malware
benchmark만 승인한다.

# Verified Results

- artifact: `ELF_test.zip`, 16,763,975 bytes
- fixed revision: `3d23efef7c0f0b702c5024400cfff4c3744a3832`
- archive members: weekly JSONL 12개
- raw / post-dedup records: `12,000 / 6,000`
- primary labels: benign `6,000`, malware `6,000`
- invalid JSON·schema·feature shape: 0
- primary label conflict: 0
- static-feature conflict: 0
- raw executable read / execution: `0 / 0`

동일 관측치의 완전한 record는 1,268개 group에서 달랐다. 차이는
CAPS/MBC/TTP 보조 annotation이 한쪽 duplicate에만 채워진 형태였으며,
static feature와 primary malware label은 같았다.

# Decision

최종 disposition은
`independent_benchmark_with_required_dedup`이다.

- benchmark materialization: true
- dedup key: `(week_id, sha256)`
- Qwen SFT 혼합: false
- raw executable download: false
- auxiliary label evaluation: merge 계약 전까지 false

원본 12,000행을 그대로 사용한 점수는 중복 표본에 의한 편향이 있으므로
유효한 결과로 인정하지 않는다. 여러 주차에 다시 등장한 동일 file hash는
시간별 관측치로 유지하되 hash-level aggregate도 같이 기록한다.

# Evidence

- archive inventory SHA-256:
  `99ca5beccd2e5bcab32b3714cb635bc6b528faa458500190adc995d66ce96e9c`
- benchmark audit SHA-256:
  `f37ae45b619ad2274827ebba2d37c9a06f8448406b4dc9e4c6cba639ca618a8e`

# Next Actions

1. [완료] train 26,000·test 6,000관측치 deterministic materializer
2. [완료] malware classifier용 별도 absolute gate
3. [실패] 자체 temporal LightGBM과 공식 공개 모델 절대평가
4. [차단] NuriLab static-feature 연결과 AegisLM 근거 입력
5. [다음] FP 집중 주차의 label-blind feature drift 감사

# Related Concepts

- [EMBER2024 Classifier 절대평가](aegislm_ember2024_classifier_baseline_decision_20260731.md)
- [Phase F 구현 계획](aegislm_phase_f_experiment_plan_20260728.md)
- [EMBER2024 결정 원문](aegislm_ember2024_benchmark_decision_20260731.md)
- [BinKit Metadata Gate](aegislm_binkit_metadata_decision_20260731.md)
- [Assemblage Metadata Gate](aegislm_assemblage_metadata_decision_20260731.md)

# Citations

- [EMBER2024 repository](https://github.com/FutureComputing4AI/EMBER2024)
- [EMBER2024 dataset](https://huggingface.co/datasets/joyce8/EMBER2024)
- [EMBER2024 paper](https://arxiv.org/abs/2506.05074)
