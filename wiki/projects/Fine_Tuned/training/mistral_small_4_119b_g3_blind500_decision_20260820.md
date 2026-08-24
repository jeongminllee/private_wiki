---
type: Decision Note
title: Mistral Small 4 119B G3 Blind 500 Source Decision PASS
description: BF16 LoRA FSDP2 100-step adapter가 fresh blind decision 500건에서 모든 자동 gate를 통과한 결과와 적용 범위를 기록
tags: [mistral, phase-f, lora, fsdp2, blind-evaluation, source-security]
timestamp: 2026-08-20
status: active
---

# Summary

Mistral Small 4 119B local BF16 checkpoint에 BF16 LoRA + FSDP2로 학습한 G3
100-step adapter가 `phase-f-source-fresh-blind-500-v1`의 decision contract 500건
절대평가를 통과했다. scorer exit code는 0이고 precision, recall, parse, schema가
모두 1.0이며 FPR과 abstention은 0이다.

이 판정은 **source decision-only contract PASS**다. 실제 evidence line 선택 능력은
이번 adapter가 출력하지 않으므로 평가하지 않았고, evidence adapter·merge·full epoch를
자동 승인하지 않는다.

# Training and Lifecycle Evidence

- profile: BF16 LoRA + FSDP2
- optimizer step: 100/100
- runtime: 271.3초
- train loss: 0.04073
- Trainer device reserved: 154.2 GiB
- final adapter save: PASS
- artifact SHA-256 inventory: PASS
- G2 새 process reload·단일 inference: PASS

loss는 hardware·lifecycle 신호일 뿐 품질 판정에는 사용하지 않았다.

# Blind Boundary

- source: `phase-f-source-fresh-blind-500-v1`
- contract: decision-only
- challenge/gold: 500/500
- label balance: present/not_observed 250/250
- challenge ID: 500개 모두 고유
- model-visible roles: `system → user`
- source·contract SHA256SUMS: PASS
- prediction process: challenge만 읽고 gold 경로를 포함하지 않음
- prediction을 500행과 SHA-256으로 동결한 뒤 별도 scorer process가 gold를 읽음

이 blind는 결과 확인으로 gold가 열린 평가 artifact이므로 향후 model selection이나
threshold 조정에 재사용하지 않는다.

# Automatic Gate Results

| Metric | Result | Gate |
| --- | ---: | ---: |
| TP / TN / FP / FN | 250 / 250 / 0 / 0 | PASS |
| Precision | 1.0000 | ≥0.90 |
| Recall | 1.0000 | ≥0.95 |
| FPR | 0.0000 | ≤0.05 |
| Abstention | 0.0000 | ≤0.05 |
| Parse success | 1.0000 | ≥0.99 |
| Schema pass | 1.0000 | ≥0.99 |
| Missing / extra | 0 / 0 | PASS |
| Latency p50 / p95 | 2,395.3907 / 3,354.4281 ms | 기록 |
| Overall | **PASS** | 모든 gate true |

모든 raw output이 `assessment` 하나만 포함하는 decision schema를 통과했으므로 이번
contract 범위에서는 free-text unsafe guidance와 근거 가장(evidence fabrication) surface가
없었다. 이는 evidence correctness를 측정했다는 뜻이 아니다.

# Evidence Hashes

- predictions: `305e178b62534e8f9ec5b6ad99b01e7d2e45bc3ddd6c76730df20e9c00cf8d85`
- summary: `0d443195bdcd199a42bd8d2f72feb11639eb131a93f896944a673cfb4b584a63`
- scorer log: `751efdf14b89bc8cda83467787ccca005fec1a7e1bcb888f23868727de4c99aa`
- evaluation `SHA256SUMS`: `4476d2e758d96e47a6ab602da3f6b8cf7e760bc4d2952e2398572a1ca35d7958`

# Decision

1. Mistral G3 source decision adapter를 scope-limited PASS 후보로 동결한다.
2. 같은 blind 500을 후속 선택·튜닝에 재사용하지 않는다.
3. merge, evidence adapter와 full epoch는 별도 연구 결정과 승인 전까지 실행하지 않는다.
4. 실제 repository, 다른 언어, binary·pseudo-code와 evidence line 품질은 증명되지 않았다.

# Related Concepts

- [Mistral Small 4 B200 vLLM 0.26 서빙 트러블슈팅](../../../errors/mistral-small4-b200-vllm-serving-troubleshooting-20260820.md)
- [Mistral F5-X 첫 파인튜닝 실습 워크북](mistral_f5x_first_finetuning_workbook_20260809.md)
- [Mistral F5-X 통합 설정 v2 인계서](../handoffs/mistral_f5x_unified_config_v2_handoff_20260805.md)
- [AegisLM Q1R11 신규 Blind 500 PASS](aegislm_q1r11_fresh_blind_pass_decision_20260730.md)
