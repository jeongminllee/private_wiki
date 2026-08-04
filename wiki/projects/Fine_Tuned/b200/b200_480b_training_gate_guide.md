---
type: Setup Guide
title: B200 Qwen3-Coder 480B FP8 Training Gate Guide
description: Qwen3-Coder 480B FP8 full training before-run gates, monitoring points, and recording rules for MalwareAnalysisLLM.
tags: [project, finetuning, b200, qwen3-coder, llamafactory, deepspeed, wandb]
timestamp: 2026-07-03
status: active
---

# Summary

이 문서는 `${MALWARE_ANALYSIS_LLM_ROOT}`에서 `Qwen3-Coder-480B-A35B-Instruct-FP8` 실제 학습으로 넘어가기 전 확인해야 하는 0~4단계 게이트를 정리한다.

핵심 원칙은 다음과 같다.

- 사용자가 직접 학습과 모니터링을 수행한다.
- 에이전트는 명령어, 로그 해석, 문서화, 다음 조정안을 지원한다.
- 480B full 1 epoch run은 바로 시작하지 않고, 0~4단계가 통과된 뒤에만 승격한다.
- telemetry watcher는 observe-only다. 학습 process에 signal을 보내지 않는다.
- 실패도 결과다. 각 단계의 실패 지점과 telemetry를 남겨야 다음 판단이 가능하다.

# Current Context

현재 기준 환경:

```text
project: ${MALWARE_ANALYSIS_LLM_ROOT}
branch: experiment/b200-qwen3-coder-480b
target model: Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8
local model dir: model/base/qwen3-coder-480b-a35b-instruct-fp8
framework: LLaMA-Factory + DeepSpeed + PEFT LoRA
logging: W&B online
telemetry: scripts/check_memory_budget.py observe-only watcher
```

분리해서 봐야 하는 문제:

- 480B: 과거 checkpoint loading 중 `SIGKILL(-9)`가 발생했다. container cgroup memory limit, loader/rank별 RSS, external kill 가능성을 계속 분리해서 본다.
- 30B/72B: ZeRO-3 첫 optimizer step에서 dtype mismatch가 발생했다. DeepSpeed PR #8073 방식의 patch로 regression을 먼저 확인한다.
- 30B/72B ZeRO-2: 이미 1-step smoke가 통과했으므로 dataset, W&B, LLaMA-Factory 기본 경로는 정상으로 본다.

# Common Preparation

모든 단계 시작 전에 같은 shell에서 환경변수를 주입한다.

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}
set -a
. ./.env
set +a
export CUDA_VISIBLE_DEVICES=0,1,2,3
export WANDB_PROJECT=malware-analysis-llm
export WANDB_LOG_MODEL=false
export WANDB_WATCH=false
```

`uv run python`은 현재 프로젝트에서 `.venv/bin/python3`로 해석되므로 Python helper script 실행에 사용해도 된다. 실제 LLaMA-Factory 학습은 준비된 `bash scripts/...sh` runner로 실행한다.

# Stage 0: DeepSpeed ZeRO-3 Patch Check

## Purpose

30B/72B가 ZeRO-3에서 실패했던 `TypeError: output tensor must have the same type as input tensor` 문제가 patch된 상태인지 확인한다.

이 단계는 480B 메모리 문제를 해결하는 단계가 아니다. 480B full run에서 ZeRO-3를 사용할 것이므로, 먼저 optimizer/all-gather dtype mismatch 문제가 남아 있지 않은지 확인하는 gate다.

## Command

```bash
uv run python scripts/patch_deepspeed_zero3_dtype.py check
```

필요할 때만 patch를 적용한다.

```bash
uv run python scripts/patch_deepspeed_zero3_dtype.py patch
uv run python scripts/patch_deepspeed_zero3_dtype.py check
```

## What To Check

성공 기준:

- `bug_blocks: 0`
- `patch_blocks: 2`
- `patched: true`
- `needs_patch: false`

기록할 값:

- 실행 시각
- DeepSpeed file path
- backup file path
- `bug_blocks`
- `patch_blocks`
- `patched`
- `needs_patch`

## Decision

- 통과: Stage 1로 진행한다.
- 실패: 30B/72B ZeRO-3 regression을 돌리지 않는다. patch 상태부터 복구한다.

# Stage 1: Full Dataset Export And Registration

## Purpose

smoke용 100건 dataset과 full training dataset을 분리한다. 현재 목표는 full train 332,807건과 validation 41,600건을 LLaMA-Factory에 별도 dataset name으로 등록하는 것이다.

이 단계는 GPU 학습이 아니라 데이터 준비 단계다. 여기서 실패하면 학습 config가 아무리 좋아도 full run을 시작할 수 없다.

## Commands

```bash
uv run python scripts/export_llamafactory_dataset.py \
  --input data/processed/aegislm_security_train.jsonl \
  --output LLaMA-Factory/data/aegislm_security_sft_train_full.json \
  --dataset-name aegislm_security_sft_train_full \
  --ignore-errors

uv run python scripts/export_llamafactory_dataset.py \
  --input data/processed/aegislm_security_validation.jsonl \
  --output LLaMA-Factory/data/aegislm_security_sft_validation_full.json \
  --dataset-name aegislm_security_sft_validation_full \
  --ignore-errors

uv run python scripts/prepare_llamafactory_data.py \
  --train-file aegislm_security_sft_train_full.json \
  --validation-file aegislm_security_sft_validation_full.json \
  --train-name aegislm_security_sft_train_full \
  --validation-name aegislm_security_sft_validation_full
```

건수 확인:

```bash
uv run python - <<'PY'
import json
from pathlib import Path

for p in [
    "LLaMA-Factory/data/aegislm_security_sft_train_full.json",
    "LLaMA-Factory/data/aegislm_security_sft_validation_full.json",
]:
    data = json.loads(Path(p).read_text())
    print(p, len(data), f"{Path(p).stat().st_size / 1024**2:.1f} MiB")
PY
```

## What To Check

성공 기준:

- train full JSON이 생성된다.
- validation full JSON이 생성된다.
- `LLaMA-Factory/data/dataset_info.json`에 두 dataset name이 등록된다.
- train count는 약 332,807건이어야 한다.
- validation count는 약 41,600건이어야 한다.

기록할 값:

- train export count
- validation export count
- skipped/ignored error count가 있다면 그 수와 대표 사유
- output file size
- dataset_info 등록명

## Decision

- 통과: Stage 2로 진행한다.
- 실패: full training을 시작하지 않는다. dataset export error부터 고친다.

# Stage 2: 30B/72B ZeRO-3 Regression

## Purpose

DeepSpeed patch가 실제 LLaMA-Factory + PEFT LoRA 경로에서 작동하는지 확인한다.

30B/72B는 480B보다 가볍기 때문에, 여기서 ZeRO-3 optimizer step이 실패하면 480B full run은 의미가 없다. 반대로 여기서 통과하면 dtype mismatch 문제는 어느 정도 제거됐다고 볼 수 있다.

## Commands

```bash
bash scripts/run_smoke_qwen3_coder_30b.sh
bash scripts/run_smoke_qwen2_72b.sh
```

## What To Check

성공 기준:

- model loading 성공
- 첫 forward/backward 진입
- 첫 optimizer step 통과
- `TypeError: output tensor must have the same type as input tensor` 미발생
- W&B loss logging 확인
- adapter/checkpoint 생성 확인
- memory watcher에서 새 `oom_kill` 증가 없음

기록할 값:

- model name
- config file
- run script
- W&B run name
- 첫 step 성공 여부
- peak cgroup current
- `memory.events`의 `oom`, `oom_kill`
- adapter/checkpoint output path
- 실패 시 traceback 첫 원인

## Decision

- 30B와 72B 모두 통과: Stage 3으로 진행한다.
- 둘 중 하나라도 dtype mismatch 재발: DeepSpeed patch, PEFT adapter dtype, LLaMA-Factory config를 다시 본다.
- dtype mismatch가 아닌 memory 문제 발생: batch size, cutoff length, offload config를 먼저 본다.

# Stage 3: 480B FP8 10-Step Calibration

## Purpose

480B FP8가 full dataset config 기반으로 최소한 model load, 첫 train step, W&B logging, checkpoint save까지 갈 수 있는지 확인한다.

10-step은 학습 품질을 보는 단계가 아니다. 자연 종료 지점과 telemetry를 확보하고, full run을 시작해도 되는지 판단하는 가장 작은 480B gate다.

## Command

```bash
bash scripts/run_calibrate_qwen3_coder_480b_fp8_10_z3_patched.sh
```

## Live Monitoring

GPU:

```bash
watch -n 2 nvidia-smi
```

memory watcher:

```bash
tail -f "$(ls -t model/runs/memory/memory_watch_*.jsonl | head -n 1)"
```

cgroup events는 현재 container path에 따라 달라질 수 있다. 정확한 path는 `scripts/check_memory_budget.py` 출력의 cgroup path를 우선 사용한다.

## What To Check

성공 기준:

- checkpoint shard loading이 끝난다.
- 첫 optimizer step까지 도달한다.
- W&B에 loss가 찍힌다.
- adapter/checkpoint가 생성된다.
- run이 `max_steps: 10`까지 완료된다.
- watcher가 학습 process를 종료시키지 않는다.

중요 관찰값:

- checkpoint loading 진행률과 시각
- cgroup `memory.current`, `memory.peak`, `memory.max`
- `memory.events.oom`, `memory.events.oom_kill`
- rank별 RSS와 thread count
- GPU memory used
- GPU utilization
- `SIGKILL`, `SIGTERM`, Python exception 중 무엇으로 끝났는지

## Decision

- 통과: Stage 4로 진행한다.
- loading 중 `SIGKILL(-9)`: torchrun 로그만으로 단정하지 않고 cgroup events, process RSS, external kill 가능성을 함께 본다.
- 첫 optimizer step에서 dtype mismatch: Stage 0/2 patch 검증 결과와 DeepSpeed path를 다시 본다.
- GPU OOM: batch, cutoff, gradient checkpointing, ZeRO config를 조정한다.

# Stage 4: 480B FP8 100-Step Calibration

## Purpose

10-step이 단순 생존 확인이라면, 100-step은 짧은 실제 학습 안정성 확인이다. loss logging, checkpoint save/resume 가능성, step time, ETA, memory drift를 본다.

여기서 통과해야 full 1 epoch run으로 승격할 근거가 생긴다.

## Command

```bash
bash scripts/run_calibrate_qwen3_coder_480b_fp8_100_z3_patched.sh
```

## What To Check

성공 기준:

- 100 step 완료
- W&B loss curve가 정상적으로 이어진다.
- `save_steps` 기준 checkpoint가 생성된다.
- `oom_kill` 증가 없음
- cgroup memory가 계속 상승하는 leak 양상을 보이지 않는다.
- 평균 step time과 tokens/sec를 추정할 수 있다.

기록할 값:

- total elapsed time
- average step time
- W&B loss logging interval
- checkpoint save time
- peak cgroup current
- peak GPU memory
- rank별 RSS 최대값
- full 1 epoch 예상 step 수와 ETA
- resume test 여부

## Decision

- 통과: full 1 epoch run을 시작할 수 있다.
- checkpoint save에서 실패: disk path, permission, file count, checkpoint size를 확인한다.
- 시간이 지나며 memory가 계속 증가: dataloader/cache/checkpoint/eval strategy를 조정한다.
- 100-step은 통과하지만 ETA가 과도함: cutoff length, gradient accumulation, eval/save interval을 재조정한다.

# Promotion: Full 1 Epoch Run

0~4단계가 통과된 뒤에만 full run을 시작한다.

```bash
bash scripts/run_train_qwen3_coder_480b_fp8_full_z3_patched.sh
```

full run 기록 항목:

- start time
- config path
- dataset count
- expected update steps
- W&B run name
- checkpoint interval
- eval interval
- peak cgroup memory
- peak GPU memory
- average step time
- latest checkpoint
- interruption reason, if any
- resume command, if any

# Failure Log Template

실패가 발생하면 아래 항목을 우선 남긴다.

```text
time:
stage:
command:
config:
last visible progress:
torchrun root cause rank:
exitcode:
signal:
python exception:
memory.current:
memory.peak:
memory.max:
memory.events oom:
memory.events oom_kill:
rank rss:
gpu memory:
wandb run:
checkpoint path:
interpretation:
next action:
```

# Related Concepts

- [B200 Qwen3-Coder 480B SIGKILL Analysis Process](../repos/AegisLM/docs/B200_QWEN3_480B_MEMORY_PROCESS.md)
- [B200 Qwen3-Coder 480B Memory Observation Report](../repos/AegisLM/docs/B200_MEMORY_CONTROL_REPORT.md)
- [DeepSpeed ZeRO-3 Dtype Mismatch Troubleshooting](../repos/AegisLM/docs/DEEPSPEED_ZERO3_DTYPE_MISMATCH.md)
- [LLaMA-Factory Qwen3-Coder 480B FP8 SIGKILL Investigation](../../../errors/llamafactory-qwen3-coder-480b-fp8-oom-kill.md)
- [LLaMA-Factory DeepSpeed ZeRO-3 LoRA BF16 Dtype Mismatch](../../../errors/llamafactory-deepspeed-zero3-dtype-mismatch.md)
