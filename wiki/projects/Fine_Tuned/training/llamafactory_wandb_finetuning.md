---
type: Project
title: LLaMA-Factory + W&B 기반 AegisLM 보안 파인튜닝 연동
description: B200 서버에서 AegisLM 데이터 빌더, LLaMA-Factory, DeepSpeed ZeRO-3, W&B logging을 사용해 Qwen3-Coder smoke LoRA SFT를 실행하는 가이드
tags: [project, fine-tuning, llamafactory, wandb, aegislm, nurilab, b200]
timestamp: 2026-07-01
status: active
---

# Goal

Project NuriLab은 정적 분석과 보고서 생성을 담당하고, AegisLM은 보안 분석 설명에 특화된 adapter 개발을 담당한다. 학습 프레임워크는 B200 4장 환경에서 LLaMA-Factory를 기본으로 사용한다.

# Current Status

서버 기준 작업 위치:

```text
${MALWARE_ANALYSIS_LLM_ROOT}
```

주요 구성:

- `.venv`: 프로젝트 Python 환경
- `LLaMA-Factory/`: 서버 로컬 checkout
- `aegislm/`: canonical dataset/schema/formatting/evaluation helper
- `scripts/build_security_dataset.py`: HF/CTF/ZIP/source corpus 전처리
- `scripts/export_llamafactory_dataset.py`: LLaMA-Factory Alpaca-style export
- `scripts/prepare_llamafactory_data.py`: `dataset_info.json` 등록
- `scripts/check_environment.py`: 서버 preflight 점검
- `configs/llamafactory/qwen3_coder_480b_fp8_lora_smoke.yaml`
- `configs/llamafactory/qwen3_coder_480b_lora_smoke.yaml`

# Environment

비밀값은 Git에 넣지 않는다. 서버에서는 `.env.example`을 참고해서 shell에 직접 export한다.

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export WANDB_PROJECT=malware-analysis-llm
export WANDB_API_KEY="<secret>"
export HF_TOKEN="<optional>"
```

환경 점검:

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}
uv run python scripts/check_environment.py
```

`WANDB_API_KEY`, `HF_TOKEN`, `DATASET_OUTPUT_DIR`은 상황에 따라 warning일 수 있다. 실제 online W&B training 전에는 `WANDB_API_KEY`가 반드시 필요하다.

# How to Run

1. Smoke dataset 생성:

```bash
uv run python scripts/build_security_dataset.py \
  --include-hf \
  --ctf-writeups-dir ./dataset/ctf_raw_writeups \
  --zip-source-dir ./dataset \
  --max-per-source 100 \
  --output-dir data/processed \
  --split-ratios 0.8,0.1,0.1 \
  --seed 42
```

전체 source를 제한 없이 수집하려면 `--max-per-source -1`을 사용한다. 단, DiverseVul/BigVul은 대형 데이터셋이므로 먼저 smoke run을 통과한 뒤 실행한다.

2. LLaMA-Factory dataset export:

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

3. FP8 smoke training:

```bash
export WANDB_API_KEY="<secret>"
bash scripts/run_smoke_qwen3_coder_480b_fp8.sh
```

4. Non-FP8 comparison smoke:

```bash
bash scripts/run_smoke_qwen3_coder_480b.sh
```

# Key Decisions

- `--include-hf`는 Cybersecurity QA, DiverseVul, BigVul을 모두 포함하는 alias다.
- CTF write-up과 BigVul patch code는 supervised target output에 전문을 넣지 않는다.
- `.env.example`은 실행값의 문서 역할만 하며 실제 `.env`와 token은 Git 밖에 둔다.
- `data/`, `outputs/`, `runs/`, `wandb/`, `checkpoints/`, `adapters/`, `models/`, `saves/`는 Git 추적 대상이 아니다.
- W&B에는 loss 등 metric을 기록하되 raw dataset이나 secret을 업로드하지 않는다.

# Verification

```bash
uv run pytest tests/
uv run ruff check .
uv run ruff format --check .
uv run mypy aegislm/ tests/
.venv/bin/llamafactory-cli version
.venv/bin/python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.device_count())"
```

# 2026-07-02 B200 FP8 Smoke Result

`Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8` smoke run은 dataset export, tokenizer/preprocessing, distributed launch까지 통과했지만 checkpoint weight loading 약 39~40% 지점에서 반복적으로 실패했다.

실패 원인은 GPU OOM이나 호스트 전체 RAM 고갈이 아니라 Docker/container cgroup memory limit OOM으로 확인했다. 호스트에는 2.2TiB RAM이 보였지만 상위 Docker cgroup의 `memory.max`는 `858993459200` bytes, 즉 약 800GiB였고, 실패 시 `memory.peak`가 이 값에 도달했다. torchrun 로그의 실제 root cause는 rank 프로세스의 `SIGKILL(exitcode -9)`이다.

이 결과는 LLaMA-Factory + DeepSpeed ZeRO-3 조합이 학습 중 shard는 가능하더라도, 480B FP8 checkpoint loading 단계에서 rank별 CPU memory 피크를 충분히 낮추지 못한다는 증거로 기록한다. 자세한 분석은 [Qwen3-Coder 480B FP8 OOM Kill Error Note](../../../errors/llamafactory-qwen3-coder-480b-fp8-oom-kill.md)를 참조한다.

다음 실행 방향은 480B fine-tuning을 계속 밀어붙이기보다, 더 작은 Qwen3-Coder 계열 모델로 pipeline smoke를 먼저 성공시키고 480B는 별도의 sharded loading/FSDP/Megatron/vLLM serving 검증으로 분리하는 것이다.

# Memory Guard

`experiment/b200-qwen3-coder-480b` 브랜치에는 `scripts/check_memory_budget.py`를 추가했다. 기본 FP8 run script는 훈련 시작 전에 이 guard를 실행하고, 현재처럼 800GiB container limit에서 Qwen3-Coder 480B FP8 + 4 ranks 조합이 감지되면 fail-fast로 중단한다.

```bash
.venv/bin/python scripts/check_memory_budget.py \
  --model-dir model/base/qwen3-coder-480b-a35b-instruct-fp8 \
  --nproc 4
```

사용자가 직접 지켜보며 강행할 때만 다음처럼 실행한다.

```bash
B200_MEMORY_GUARD_MODE=monitor \
B200_MEMORY_ALLOW_KNOWN_RISK=1 \
bash scripts/run_smoke_qwen3_coder_480b_fp8.sh
```

팀 실행 절차와 체크리스트는 [B200 Qwen3-Coder 480B Memory Process](../repos/AegisLM/docs/B200_QWEN3_480B_MEMORY_PROCESS.md)에 기록한다.

# Related Concepts

- [사이버 보안 LLM 파인튜닝 데이터셋 추출·전처리·분리 가이드](../data/security_datasets.md)
- [B200 기반 대형 언어 모델 로컬 서빙 및 파인튜닝 실험 제안](../b200/B200_server.md)
- [Project NuriLab LLaMA-Factory integration](../repos/project_Nurilab/docs/LLAMA_FACTORY_AEGISLM_INTEGRATION.md)
