---
type: Error Note
title: LLaMA-Factory CLI Missing After Dependency Drift
description: MalwareAnalysisLLM 서버에서 .venv/bin/llamafactory-cli가 없어져 학습 runner가 시작 즉시 실패한 사건과 pyproject.toml 기반 복구 방법
tags: [error, b200, llamafactory, uv, pyproject, dependency]
timestamp: 2026-07-06
status: solved
---

# Situation

`${MALWARE_ANALYSIS_LLM_ROOT}`에서 Qwen3-Coder-Next 80B full training을 준비하던 중 runner가 시작 직후 실패했다.

이 시점의 문제는 model loading, DeepSpeed, GPU memory, dataset tokenizing 문제가 아니라 `.venv` 안에 LLaMA-Factory CLI와 training runtime dependency가 제대로 설치되어 있지 않은 환경 정합성 문제였다.

# Error Message

```text
scripts/run_observed_llamafactory_train.sh: line 45: .venv/bin/llamafactory-cli: No such file or directory
```

# Cause

확인 결과 `.venv/bin/llamafactory-cli`가 없었고, `.venv`에는 `torch`, `peft`, `accelerate`, `trl` 같은 학습 runtime dependency도 빠져 있었다.

근본 원인은 root `pyproject.toml`이 AegisLM의 데이터/유틸리티 의존성만 담고 있었고, local checkout인 `LLaMA-Factory/`와 training stack을 project dependency로 알지 못했다는 점이다. 이 상태에서는 `uv sync` 또는 환경 재정비 후 `.venv`가 학습 가능한 상태로 복원되지 않는다.

추가로 LLaMA-Factory `0.9.6.dev0`는 `datasets>=2.16.0,<=4.0.0`을 요구하므로, `datasets` version range도 project dependency에 고정되어 있어야 한다.

# Solution

`pyproject.toml`을 다음 정책으로 정리했다.

- 기본 dependency에 `datasets>=2.16.0,<=4.0.0`을 명시한다.
- `hf-transfer`를 추가해 대형 모델 shard 다운로드를 재개/가속할 수 있게 한다.
- `training` dependency group에 `accelerate`, `deepspeed`, `llamafactory`, `peft`, `trl`을 둔다.
- local `LLaMA-Factory/` checkout을 editable source로 등록한다.

핵심 구조:

```toml
[dependency-groups]
training = [
    "accelerate>=1.3.0,<=1.11.0",
    "deepspeed>=0.19.2,<0.20",
    "llamafactory",
    "peft>=0.18.0,<=0.18.1",
    "trl>=0.18.0,<=0.24.0",
]

[tool.uv.sources]
llamafactory = { path = "LLaMA-Factory", editable = true }
```

복구 명령:

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}
uv sync --group training
```

복구 후 확인:

```bash
.venv/bin/llamafactory-cli version
.venv/bin/python - <<'PY'
import torch
print(torch.__version__)
print(torch.cuda.is_available(), torch.cuda.device_count())
PY
```

확인된 결과:

```text
LLaMA Factory 0.9.6.dev0
torch 2.12.1+cu130
cuda available: True
cuda devices: 4
datasets 4.0.0
peft 0.18.1
accelerate 1.11.0
trl 0.24.0
```

주의할 점:

`uv sync --group training`이 DeepSpeed package를 다시 설치하면 site-package에 적용한 ZeRO-3 dtype patch가 원복될 수 있다. 따라서 sync 이후에는 아래 명령을 다시 확인한다.

```bash
.venv/bin/python scripts/patch_deepspeed_zero3_dtype.py check
```

필요하면 다시 적용한다.

```bash
.venv/bin/python scripts/patch_deepspeed_zero3_dtype.py patch
```

# Prevention

앞으로 학습 서버 복구는 임시 `uv pip install ...`을 우선하지 않는다. 먼저 project dependency를 기준으로 복원한다.

```bash
uv sync --group training
```

그 다음 아래를 순서대로 확인한다.

```bash
.venv/bin/llamafactory-cli version
.venv/bin/python scripts/patch_deepspeed_zero3_dtype.py check
.venv/bin/python scripts/check_environment.py
```

이 방식이면 `.venv`를 새로 만들거나 서버 컨테이너를 정리해도 LLaMA-Factory CLI와 training dependency를 반복 수동 설치하지 않아도 된다.

# Related Concepts

- [B200 Fine-Tuning Troubleshooting Report](../projects/Fine_Tuned/b200/b200_finetuning_troubleshooting_report_20260703.md)
- [LLaMA-Factory DeepSpeed ZeRO-3 LoRA BF16 Dtype Mismatch](llamafactory-deepspeed-zero3-dtype-mismatch.md)
- [B200 Full-Size Training Queue](../projects/Fine_Tuned/b200/b200_full_size_training_queue.md)

# Citations

- LLaMA-Factory local checkout: `${MALWARE_ANALYSIS_LLM_ROOT}/LLaMA-Factory`
- Project dependency file: `${MALWARE_ANALYSIS_LLM_ROOT}/pyproject.toml`
