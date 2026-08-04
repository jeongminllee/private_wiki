---
type: Reference
title: 사이버 보안 LLM 파인튜닝 데이터셋 추출·전처리·분리 가이드
description: AegisLM과 Project NuriLab 목적에 맞게 공개 보안 데이터셋과 로컬 CTF/source corpus를 안전한 canonical JSONL로 변환하고 train/validation/test로 분리하는 실행 가이드
tags: [security, dataset, fine-tuning, llm, preprocessing]
timestamp: 2026-07-01
status: active
---

# Summary

이 문서는 AegisLM 보안 파인튜닝 데이터셋의 정본 흐름을 기록한다. 목표는 보안 지식을 많이 외우는 모델이 아니라, **Project NuriLab의 정적 분석 결과를 방어적으로 설명하고 JSON 보고서로 구조화하는 adapter**를 만드는 것이다.

데이터는 LLaMA-Factory의 `instruction/input/output`으로 바로 만들지 않는다. 먼저 AegisLM canonical JSONL로 정규화하고, schema/safety validation과 split을 거친 뒤 LLaMA-Factory dataset으로 export한다.

```text
raw / legacy dataset
-> extraction
-> AegisLM canonical preprocessing
-> train/validation/test split
-> LLaMA-Factory export
-> SFT LoRA training
```

# Dataset Sources

v1 구현 범위는 처음 작성한 전처리 코드의 5갈래를 안전 변환 방식으로 복원하는 것이다.

| Source | CLI flag | 처리 방식 |
| --- | --- | --- |
| Cybersecurity QA | `--include-cybersecurity-qa` 또는 `--include-hf` | `rezaduty/cybersecurity-qa-v2`는 parquet 변환 경로가 pyarrow nested column 문제로 실패하므로, 작은 원본 `cybersecurity_interview_qa_complete.jsonl`을 HF Hub에서 직접 받아 읽는다. 이 경로가 실패하면 `Rowden/CybersecurityQAA`를 fallback으로 사용한다. 원본 answer는 bounded context로만 쓰고 target output에는 복사하지 않는다. |
| DiverseVul | `--include-diversevul` 또는 `--include-hf` | `func`, `target`을 사용해 취약 label과 정적 signal 설명 record로 변환한다. |
| BigVul | `--include-bigvul` 또는 `--include-hf` | `func_before`는 redacted context로 쓰고 `func_after` 전체 패치 코드는 target output에 넣지 않는다. fixed pair 존재와 hash metadata만 남긴다. |
| CTF write-up Markdown | `--ctf-writeups-dir` | 제목, 상대 경로, 짧은 redacted excerpt만 사용한다. write-up 전문, payload, exploit procedure는 supervised target에 넣지 않는다. |
| ZIP/source corpus | `--zip-source-dir`, `--local-source-dir` | ZIP은 path traversal 방어 후 `data/extracted/security_archives/`에 풀고 source file만 local source corpus record로 변환한다. |

`--include-hf`는 하위 호환 alias이며 Cybersecurity QA, DiverseVul, BigVul 세 HF source를 모두 포함한다.

# Canonical Record

AegisLM의 1차 저장 포맷은 JSONL이며, 각 줄은 다음 구조를 따른다.

```json
{
  "id": "string",
  "source": {
    "type": "public_security_dataset",
    "name": "string",
    "url": "string|null",
    "license_or_terms": "string|null",
    "retrieved_at": "YYYY-MM-DD|null"
  },
  "input": {
    "task": "string",
    "context": "string",
    "signals": {}
  },
  "expected_output": {
    "summary": "string",
    "behavior_explanation": "string",
    "risk_level": "low|medium|high|critical|unknown",
    "malware_like_behaviors": [],
    "attack_mapping": [],
    "recommendations": [],
    "limitations": []
  },
  "metadata": {
    "split": "train|validation|test|fixture",
    "safety_level": "metadata_only|synthetic|redacted|restricted",
    "contains_executable_payload": false,
    "notes": []
  }
}
```

# Build Commands

Smoke 100 build:

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}

uv run python scripts/build_security_dataset.py \
  --include-hf \
  --ctf-writeups-dir ./dataset/ctf_raw_writeups \
  --zip-source-dir ./dataset \
  --max-per-source 100 \
  --output-dir data/processed \
  --split-ratios 0.8,0.1,0.1 \
  --seed 42
```

`--max-per-source`는 source별 변환 record 개수 제한이다. `-1`을 주면 해당 source의 전체 record를 받는다.

예: HF source 전체 수집

```bash
uv run python scripts/build_security_dataset.py \
  --include-hf \
  --max-per-source -1 \
  --output-dir data/processed \
  --split-ratios 0.8,0.1,0.1 \
  --seed 42
```

HF source만 따로 지정할 수도 있다.

```bash
uv run python scripts/build_security_dataset.py \
  --include-cybersecurity-qa \
  --include-diversevul \
  --include-bigvul \
  --max-per-source 100 \
  --output-dir data/processed \
  --split-ratios 0.8,0.1,0.1 \
  --seed 42
```

로컬 source corpus만 변환할 때:

```bash
uv run python scripts/build_security_dataset.py \
  --local-source-dir ./dataset/source_corpus \
  --max-per-source 3000 \
  --output-dir data/processed \
  --split-ratios 0.8,0.1,0.1 \
  --seed 42
```

생성 결과:

```text
data/processed/aegislm_security_train.jsonl
data/processed/aegislm_security_validation.jsonl
data/processed/aegislm_security_test.jsonl
```

# LLaMA-Factory Export

`test` split은 training dataset으로 export하지 않고 학습 후 held-out 평가에 사용한다.

```bash
uv run python scripts/export_llamafactory_dataset.py \
  --input data/processed/aegislm_security_train.jsonl \
  --output LLaMA-Factory/data/aegislm_security_sft_train.json \
  --dataset-name aegislm_security_sft_train \
  --ignore-errors

uv run python scripts/export_llamafactory_dataset.py \
  --input data/processed/aegislm_security_validation.jsonl \
  --output LLaMA-Factory/data/aegislm_security_sft_validation.json \
  --dataset-name aegislm_security_sft_validation \
  --ignore-errors

uv run python scripts/prepare_llamafactory_data.py
```

# Quality Checks

코드 변경 후:

```bash
uv run pytest tests/
uv run ruff check .
uv run ruff format --check .
uv run mypy aegislm/ tests/
uv run python scripts/check_environment.py
```

데이터셋 생성 후 확인할 것:

- JSONL 각 줄이 JSON object인지
- `metadata.split`이 파일명과 일치하는지
- `contains_executable_payload`가 항상 `false`인지
- BigVul `func_after`, CTF write-up 전문, exploit procedure가 target output에 없는지
- `password=`, `api_key=`, `client_secret=` 같은 민감정보 의심 assignment는 값을 `[REDACTED_SECRET]`으로 마스킹하고, `signals.redacted_secret_like_assignments`에 개수를 남기는지
- train/validation/test count가 기대 비율과 맞는지
- W&B run이나 adapter artifact에 raw dataset이 업로드되지 않는지

# 2026-07-28 Post-Run Data Policy

`hf-full-v1` 332,807건으로 수행한 Qwen3-Coder-Next 80B LoRA 학습은 loss가 약 `1.5e-6`까지 감소했지만 500건 label-blind 절대평가를 통과하지 못했다. 기존 full export는 실패 재현 artifact로 동결하고 다음 학습 입력으로 재사용하지 않는다.

다음 dataset revision은 다음을 필수로 한다.

- train 규모를 우선 `10,000–20,000`건으로 제한
- DiverseVul input에서 dataset명, label, target 제거
- BigVul의 vulnerable `before`와 fixed `after`를 positive/negative pair로 사용
- Cybersecurity QA를 코드 취약점 판별 SFT에서 분리
- code hash와 유사도 기반 중복 제거
- class/source/template별 quota와 상관관계 검사
- 고정 seed와 code hash로 3–5개 입력 prompt variant를 재현 가능하게 배정
- label, risk, JSON schema는 무작위화하지 않음
- 100-step 학습 후 label-blind diagnostic을 통과하기 전 full epoch 금지

세부 근거와 허용·금지 무작위화 규칙은 [AegisLM 데이터 축소와 통제된 무작위화 결정](../training/aegislm_dataset_reduction_randomization_decision_20260728.md)을 따른다.

# Related Concepts

- [B200 기반 대형 언어 모델 로컬 서빙 및 파인튜닝 실험 제안](../b200/B200_server.md)
- [LLaMA-Factory + W&B 기반 AegisLM 보안 파인튜닝 연동](../training/llamafactory_wandb_finetuning.md)
- [AegisLM 데이터 축소와 통제된 무작위화 결정](../training/aegislm_dataset_reduction_randomization_decision_20260728.md)
- [AegisLM LLaMA-Factory B200 W&B guide](../repos/AegisLM/docs/LLAMA_FACTORY_B200_WANDB.md)
