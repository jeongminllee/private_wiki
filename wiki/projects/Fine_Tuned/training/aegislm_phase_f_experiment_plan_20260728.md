---
type: Project
title: AegisLM Phase F 데이터 재설계와 바이너리 분석 실험
description: 80B SFT 품질 실패 이후 source 데이터 재구축, binary-derived 별도 adapter, 절대평가와 NuriLab 연결 순서를 고정한 실행 계획
tags: [aegislm, phase-f, fine-tuning, dataset, binary-analysis, evaluation]
timestamp: 2026-07-28
status: active
---

# Goal

Phase E에서 검증한 학습·저장·merge·서빙·평가 인프라를 유지하면서,
과도한 중복과 label·provenance 누출을 제거한 소규모 데이터로 실제 보안
분석 품질을 다시 검증한다.

Phase F가 답할 질문은 두 가지다.

1. 정제된 1만~1.2만 건 source data로 500건 절대 보안 gate를 통과할 수 있는가?
2. 실행파일에서 추출한 pseudo-C, 정적 특징, 제한된 assembly를 학습한
   별도 adapter가 binary-derived 분석 gate를 통과할 수 있는가?

# Current Status

- Phase E infrastructure: `PASS`
- Phase E model quality: `FAIL`
- Phase F 구현: `Ready`
- 416,009건 catalog 실제 생성: `Not Started`
- 20B 100-step canary: `Not Started`
- 80B 재학습: `Blocked` — 20B 진단 gate 통과 필요
- binary B0 feasibility: `Blocked` — source adapter 판정 후 진행
- NuriLab/RAG/MCP 연결: `Blocked` — 독립 adapter gate 통과 필요

# Structure

## F0 — 실패 기준선 동결

기존 80B adapter, merged model, 500건 prediction과 평가 결과를 삭제하지
않고 실패 기준선으로 보존한다.

## F1 — Source Dataset v2

```text
raw_catalog.parquet
→ eligible_manifest.parquet
→ train/validation/challenge/gold JSONL
```

- train: DiverseVul positive 5,000 + benchmark-negative 5,000
- validation: 500 + 500
- blind test: 250 + 250
- BigVul: before/after, CWE, 수정 위치가 검증된 pair만 최대 2,000
- seed: `20260728`
- prompt variant: 의미가 같은 네 종류
- split: repository/function/patch/compiler group 단위

Dataset 이름, source, split, target, label, expected output은 model-visible
prompt에 넣지 않는다. `target=0`과 patch 후 코드는 프로그램 전체가
안전하다는 의미로 사용하지 않는다.

## F2 — Source Adapter

```text
S0 base 500건
→ S1 gpt-oss-20b 100-step
→ S2 20B 최대 1 epoch
→ S3 Qwen3-Coder-Next 80B 100-step
→ S4 80B 최대 1 epoch
```

100-step 진단은 parse/schema 0.99, safety 1.00, precision·recall 0.75,
FPR 0.20, abstention 0.10을 진행 기준으로 사용한다.

최종 채택은 500건에서 precision 0.90, recall 0.95, FPR 0.05,
abstention 0.05, parse/schema 0.99, safety 1.00, evidence 0.90을 모두
통과해야 한다.

## F3 — Binary-derived Adapter

Raw executable byte를 LLM 데이터에 직접 넣지 않는다. 다음 파생 표현만
사용한다.

- pseudo-C/decompiler output
- imports, sections, strings, symbols
- 근거에 필요한 제한된 assembly
- format, architecture, compiler, optimization, stripped 정보

B0는 build 가능한 before/after 100 pair로 compile/decompile 성공률과
source–binary–function 연결을 검증한다. B0를 통과한 경우에만 최대
2,000 patch pair, 4,000 train record로 B1을 구성한다.

Binary 최종 평가에는 source absolute gate와 함께 compiler variant
일치율 0.95를 요구한다.

## F4 — NuriLab과 후속 연결

```text
source adapter
→ binary-derived adapter
→ NuriLab normalized signal
→ source+binary multitask
→ signals+RAG
→ signals+RAG/MCP
```

앞 단계의 절대 gate 실패를 뒤 단계의 도구 연결로 가리지 않는다.

# How to Run

원격 B200 서버에서 F1을 시작할 때:

```bash
uv run python scripts/build_phase_f_source_dataset.py \
  --input /approved/data/hf-full-v1/train.jsonl \
  --input /approved/data/hf-full-v1/validation.jsonl \
  --input /approved/data/hf-full-v1/test.jsonl \
  --output-dir /approved/data/phase-f-source-v2
```

실제 경로, manifest·challenge·gold SHA-256, record 수와 분포는 수동
워크북에 기록한다.

# Key Decisions

- loss는 관찰 지표이며 모델 채택 기준이 아니다.
- 33만 건 전체를 다시 학습하지 않는다.
- quota보다 label·근거 신뢰도를 우선하며 부족분을 저신뢰 데이터로 채우지 않는다.
- source와 binary adapter는 독립적으로 학습하고 평가한다.
- raw/live malware와 byte-level model 연구는 Phase G로 보류한다.
- EMBER2024는 초기 SFT 혼합 데이터가 아니라 별도 metadata benchmark로 둔다.
- 실제 binary compiler/decompiler pipeline은 NuriLab 또는 승인된 offline
  extractor가 담당한다.

# Issues

- 현재 canonical BigVul에는 fixed body와 충분한 CWE·수정 위치가 없어
  기본적으로 `quarantine`된다.
- 원격 416,009건에 대한 catalog와 실제 eligible 수는 아직 생성하지 않았다.
- 20B와 80B의 실제 lifecycle preflight 시간·VRAM은 다음 run에서 기록해야 한다.
- B0가 요구하는 build 가능한 patch pair 100쌍을 확보할 수 있는지 확인이 필요하다.

# Next Actions

1. 원격 기존 dataset으로 F1 catalog와 manifest를 생성한다.
2. eligible/quarantine/reject, 중복, leakage, 언어·CWE 분포를 확인한다.
3. source-v2 JSONL과 challenge/gold hash를 동결한다.
4. S0 base 500건을 다시 측정한다.
5. gpt-oss-20b 100-step canary와 save/reload/serve를 실행한다.
6. 진단 gate를 통과한 경우에만 20B 한 epoch와 80B로 진행한다.
7. Source 결과가 확정된 후 binary B0 100 pair feasibility를 시작한다.

# Related Concepts

- [AegisLM 데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md)
- [Phase F 구현·실험 SSOT](../repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)
- [AegisLM 수동 파인튜닝 검증 워크북](../repos/AegisLM-B200/docs/FINETUNING_TEST_WORKBOOK.md)
- [Qwen3-Coder-Next 80B 실행 기록](qwen3_coder_next_80b_2gpu_run_20260720.md)
- [LLM 생명주기 환경 설계](../../../infra/llm-lifecycle-environment-design.md)
