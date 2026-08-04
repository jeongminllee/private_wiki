---
type: Decision Note
title: B200 Full-Size Training Queue
description: Qwen2/72B를 제외하고 Qwen3-Coder-Next 80B부터 full dataset real training으로 전환하는 실행 큐
tags: [b200, finetuning, qwen, deepseek, glm, training]
timestamp: 2026-07-06
status: active
---

# Summary

`MalwareAnalysisLLM` B200 학습은 smoke 중심 검증을 멈추고 full dataset 기반 real training으로 전환한다.

핵심 결정:

- Qwen2/Qwen2.5 72B 계열은 active training queue에서 제외한다.
- `Qwen/Qwen3-Coder-Next` 80B를 첫 real training target으로 둔다.
- 취소됐던 DeepSeek 다운로드는 `model/base/deepseek-v4-flash` 같은 경로로 재개한다.
- 480B FP8은 LLaMA-Factory 직행 full training 후보가 아니라 loader 구조 개선 후보로 별도 관리한다.

# Server Changes

원격 프로젝트 `${MALWARE_ANALYSIS_LLM_ROOT}`에 다음 변경을 추가했다.

- `scripts/download_hf_model.py`: `deepseek-v4-flash`, `deepseek-v4-flash-base`, `qwen3-coder-next`, `glm45-air-fp8`, `glm45-full-fp8` variant alias 추가
- `configs/llamafactory/b200/qwen3_coder_next_lora_full.yaml`: Qwen3-Coder-Next 80B full dataset LoRA SFT config 추가
- `scripts/run_train_qwen3_coder_next_full.sh`: observe-only memory watcher와 함께 full training을 실행하는 runner 추가
- `docs/FULL_SIZE_TRAINING_QUEUE.md`: 서버 실행 큐와 명령어 기록

# Commands

DeepSeek Flash 다운로드 재개:

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}
set -a
. ./.env
set +a
export HF_HOME=model/cache/huggingface

uv run python scripts/download_hf_model.py \
  --variant deepseek-v4-flash \
  --cache-dir model/cache/huggingface \
  --max-download-gib 360
```

DeepSeek Flash Base가 필요할 때:

```bash
uv run python scripts/download_hf_model.py \
  --variant deepseek-v4-flash-base \
  --cache-dir model/cache/huggingface \
  --max-download-gib 420
```

Qwen3-Coder-Next 80B 다운로드:

```bash
uv run python scripts/download_hf_model.py \
  --variant qwen3-coder-next \
  --cache-dir model/cache/huggingface \
  --max-download-gib 220
```

Qwen3-Coder-Next 80B full training:

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export WANDB_PROJECT=malware-analysis-llm
export WANDB_LOG_MODEL=false
export WANDB_WATCH=false
export B200_MEMORY_WATCH_INTERVAL_SECONDS=2

bash scripts/run_train_qwen3_coder_next_full.sh
```

# Candidate Order

1. `Qwen/Qwen3-Coder-Next` 80B real training
2. `zai-org/GLM-4.5-Air-FP8` real training compatibility
3. `deepseek-ai/DeepSeek-V4-Flash` compatibility 또는 real training
4. `zai-org/GLM-4.5-FP8` load/training 한계 확인
5. `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8`는 Axolotl FSDP2, HF/TRL loader baseline, NeMo/Megatron 경로로 별도 설계

# 480B Direction

480B의 현재 병목은 학습 hyperparameter보다 checkpoint loading 구조다. batch size, cutoff length, LoRA rank를 줄이는 것보다 먼저 다음을 비교해야 한다.

- Axolotl FSDP2의 CPU-RAM-efficient loading
- HF/TRL 순수 loader baseline
- NeMo/Megatron tensor/pipeline/expert parallelism

# Related Concepts

- [MalwareAnalysisLLM LLM Candidate Matrix](llm_candidate_matrix_20260703.md)
- [B200 Model Limit Load-Only Probes](b200_model_limit_load_only_probes.md)
- [B200 Fine-Tuning Troubleshooting Report](b200_finetuning_troubleshooting_report_20260703.md)
- [B200 Qwen3-Coder 480B Training Gate Guide](b200_480b_training_gate_guide.md)
- [Full Size Training Queue Mirror](../repos/AegisLM/docs/FULL_SIZE_TRAINING_QUEUE.md)
