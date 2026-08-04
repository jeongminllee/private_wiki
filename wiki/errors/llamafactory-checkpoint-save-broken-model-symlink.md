---
type: Error Note
title: LLaMA-Factory Checkpoint Save Failed Because Model Symlink Target Disappeared
description: Qwen3-Coder-Next 80B full training이 4500 step 이후 checkpoint 저장 단계에서 model/adapters 경로를 만들지 못해 중단된 사건 분석
tags: [error, b200, llamafactory, checkpoint, symlink, storage]
timestamp: 2026-07-08
status: active
---

# Situation

`${MALWARE_ANALYSIS_LLM_ROOT}`에서 `Qwen/Qwen3-Coder-Next` 80B LoRA full training을 실행했다.

학습은 model loading과 실제 training loop를 통과했고, W&B에는 `train/global_step = 4500`, `train/epoch ~= 0.4327`까지 기록되었다. `eval_steps: 250` 기준 evaluation도 실행되었고, `eval_loss`가 기록된 뒤 checkpoint 저장 단계에서 중단되었다.

# Error Message

```text
FileNotFoundError: [Errno 2] No such file or directory: 'model/adapters'
```

traceback 위치:

```text
transformers/trainer.py
_maybe_log_save_evaluate
_save_checkpoint
save_model
_save
os.makedirs(output_dir, exist_ok=True)
```

# Confirmed Facts

- 학습 process는 종료되었고 GPU memory는 모두 해제되었다.
- W&B 최신 summary:
  - `train/global_step`: `4500`
  - `train/epoch`: `0.43268190668493545`
  - `train/loss`: 약 `3.69e-06`
  - `eval/loss`: 약 `1.39e-05`
  - `eval/runtime`: 약 `6389.55s`
- 실패 시점은 model loading이나 optimizer step이 아니라 checkpoint save 단계다.
- 프로젝트의 `model` 경로는 실제 디렉터리가 아니라 symlink였다.

```text
model -> ${TRAINING_STORAGE_ROOT}/Model/MalwareAnalysis/
```

- 확인 시점에는 symlink target의 중간 경로 `${TRAINING_STORAGE_ROOT}` 자체가 존재하지 않았다.
- `${TRAINING_STORAGE_PARENT}` 아래에는 `DAEJEON`, `GANGSEO`만 존재했다.
- 프로젝트와 `/NHNHOME`에서 `checkpoint-*`, `adapter_model.safetensors`, `qwen3-coder-next`를 검색했지만 현재 보이는 checkpoint/adapters는 없었다.
- W&B local directory에서도 `adapter_model.safetensors`, `adapter_config.json`, `trainer_state.json` 같은 model artifact는 발견되지 않았다.
- `output.log`에는 `checkpoint-250`, `checkpoint-500`, `checkpoint-3750`, `checkpoint-4000`, `checkpoint-4250` 저장 루틴 진입 로그가 있다.
- 그러나 현재 접근 가능한 filesystem에는 해당 checkpoint directory/file이 없다.
- `${TRAINING_STORAGE_PARENT}/.gc` 로그 기준 2026-07-08 17:01~17:03 KST에 `CHEONGJU-MOBILITY` 컨테이너 재생성 흔적이 있으며, 새 container mount는 `${CONTAINER_MOUNT_ROOT}/CHEONGJU`, `${CONTAINER_MOUNT_ROOT}/GANGSEO` 중심으로 구성되어 있었다.

# Cause

가장 강한 원인은 checkpoint output path의 root인 `model/` symlink가 학습 도중 또는 저장 시점에 깨진 것이다.

LLaMA-Factory config의 output path는 다음과 같았다.

```yaml
output_dir: model/adapters/qwen3-coder-next/lora/full
logging_dir: model/runs/qwen3-coder-next/lora/full
save_steps: 250
eval_steps: 250
```

`model`이 깨진 symlink가 되면 `os.makedirs("model/adapters/...", exist_ok=True)`는 parent path를 만들 수 없고 `FileNotFoundError`로 실패한다.

이 문제는 GPU OOM, cgroup memory limit, DeepSpeed dtype mismatch와 별개다. 학습은 상당히 진행되었고, evaluation 이후 save checkpoint 단계에서 파일시스템 경로 문제로 중단되었다.

추가 관측상, 학습 중 또는 학습 직후 컨테이너/스토리지 마운트가 재구성되면서 이전 `DAEGU` 경로가 현재 컨테이너에서 보이지 않게 되었을 가능성이 있다. 이 경우 checkpoint가 실제로 잠깐 생성되었더라도 현재 컨테이너에서는 접근할 수 없거나, scratch 영역 정리와 함께 사라졌을 수 있다.

# Solution

재실행 전에 먼저 artifact root를 안정적인 실제 디렉터리로 고정해야 한다.

현재 기준으로는 resume 가능한 checkpoint가 확인되지 않았다. 이전 컨테이너 또는 이전 mount namespace에서 `${TRAINING_STORAGE_ROOT}/Model/MalwareAnalysis/model/adapters/qwen3-coder-next/lora/full/checkpoint-*`를 복구할 수 있는지 운영/스토리지 레벨에서 확인해야 한다.

확인 명령:

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}
readlink model
readlink -f model
ls -ld model model/base model/adapters model/runs
```

`model` symlink target이 없으면 다음 중 하나를 결정한다.

1. 올바른 shared storage 경로로 symlink를 다시 만든다.
2. 프로젝트 내부 실제 디렉터리 또는 안정적인 mounted path를 `model/`로 사용한다.
3. base model과 adapter/checkpoint output root를 분리한다.

예:

```text
model/base        -> 대형 base model storage
model/adapters    -> 안정적인 checkpoint/adapters storage
model/runs        -> local or shared run logs
model/wandb       -> W&B local files
```

중요: checkpoint 저장 경로는 학습 중 사라질 수 있는 symlink나 재구성되는 shared path에 두면 안 된다.

# Prevention

학습 시작 전 preflight에 다음 항목을 추가한다.

```bash
test -d model/base/qwen3-coder-next
mkdir -p model/adapters/.write_test model/runs/.write_test model/wandb/.write_test
rmdir model/adapters/.write_test model/runs/.write_test model/wandb/.write_test
```

그리고 실제 output path도 미리 만든다.

```bash
mkdir -p model/adapters/qwen3-coder-next/lora/full
mkdir -p model/runs/qwen3-coder-next/lora/full
```

장시간 학습 전에는 `save_steps` 첫 checkpoint 이전이 아니라, 시작 직전에 write test를 반드시 통과해야 한다.

# Related Concepts

- [B200 Fine-Tuning Troubleshooting Report](../projects/Fine_Tuned/b200/b200_finetuning_troubleshooting_report_20260703.md)
- [B200 Full-Size Training Queue](../projects/Fine_Tuned/b200/b200_full_size_training_queue.md)
- [W&B Training Metrics Guide for MalwareAnalysisLLM](../projects/Fine_Tuned/training/wandb_training_metrics_guide.md)
