---
type: Project
title: B200 Fine-Tuning Troubleshooting Report
description: MalwareAnalysisLLM B200 서버 fine-tuning 준비 중 발생한 데이터셋, LLaMA-Factory, DeepSpeed, dependency, memory/cgroup 문제와 해결 내역 정리
tags: [project, llm, finetuning, b200, troubleshooting, llamafactory, deepspeed]
timestamp: 2026-07-03
status: active
---

# Goal

`${MALWARE_ANALYSIS_LLM_ROOT}`에서 `Qwen3-Coder` 계열 모델을 LLaMA-Factory 기반으로 fine-tuning하기 위해 진행한 작업 중 발생한 문제, 원인, 해결 방법, 현재 남은 리스크를 팀원이 재현 가능한 형태로 정리한다.

이 문서는 "무엇이 터졌는가"보다 "어디까지 해결됐고, 다음에는 무엇을 먼저 확인해야 하는가"를 기준으로 읽는다.

# Current Status

## 확인된 정상 경로

- AegisLM 데이터셋 build/export/register 경로는 동작한다.
- W&B online logging 경로는 동작한다.
- DeepSpeed ZeRO-3 dtype patch 적용 후 30B/72B 1-step regression은 통과했다.
- `pyproject.toml`에 LLaMA-Factory training dependency group을 추가했고, `uv sync --group training`으로 `.venv/bin/llamafactory-cli`와 학습 runtime을 재구성할 수 있다.
- `datasets==4.0.0` 범위를 project dependency에 고정해 LLaMA-Factory dependency check가 통과한다.

## 남은 주요 문제

- `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8`는 4-rank LLaMA-Factory/DeepSpeed 경로에서 checkpoint loading 약 40% 지점에 `SIGKILL(-9)`로 종료된다.
- 최신 관측에서는 GPU OOM이 아니라, container cgroup `memory.max=800GiB`에 도달한 시점에 `memory.events.oom_kill`이 증가했다.
- 따라서 480B full training은 아직 시작 조건을 만족하지 못했다.

# Incident Summary

| No | 문제 | 대표 증상 | 원인 또는 가장 강한 가설 | 해결/조치 | 현재 상태 |
| --- | --- | --- | --- | --- | --- |
| 1 | 데이터셋 build 결과 0건 | `Wrote 0 train records` | include flag 없이 실행되어 source가 선택되지 않음 | `--include-hf`, source별 flag, local dir flag 사용 | 해결 |
| 2 | `rezaduty/cybersecurity-qa-v2` 로딩 실패 | `An error occurred while generating the dataset` | `datasets.load_dataset()` parquet 경로에서 row/materialization 문제 | HF Hub JSONL 직접 로더와 fallback 추가 | 해결 |
| 3 | DiverseVul secret-like row 중단 | `SafetyPolicyViolationError` | 공개 데이터셋의 `password=`, `api_key=` 형태 코드가 safety validator에 걸림 | row 전체 폐기 대신 secret-like value redaction 후 포함 | 해결 |
| 4 | 전체 데이터셋 수집 옵션 부족 | `--max-per-source`가 int 제한 | smoke와 full build를 같은 옵션으로 표현하기 어려움 | `--max-per-source -1`을 전체 수집 의미로 확장 | 해결 |
| 5 | 480B 자체 soft-stop 혼선 | 700GiB 근처에서 조기 종료 | 우리가 추가한 watcher soft-limit가 학습 process에 signal을 보냄 | `--soft-limit-gib`, `--terminate-pgid`, `--exit-on-soft-limit`, `os.killpg` 경로 제거 | 해결 |
| 6 | 30B/72B ZeRO-3 첫 optimizer step 실패 | `output tensor must have the same type as input tensor` | DeepSpeed 0.19.2 ZeRO-3 + PEFT LoRA + bf16 mixed dtype all-gather bug | ZeRO-2 diagnostic, upstream PR #8073 방식 patch helper, ZeRO-3 regression 재검증 | 해결됨으로 판단 |
| 7 | LLaMA-Factory 시작 즉시 실패 | `datasets>=2.16.0,<=4.0.0 is required ... found datasets==4.8.5` | `.venv`의 `datasets==4.8.5`가 LLaMA-Factory 0.9.6.dev0 요구 범위를 벗어남 | `uv pip install "datasets==4.0.0"` | 해결, 단 `uv run` 주의 |
| 8 | LLaMA-Factory CLI 누락 | `.venv/bin/llamafactory-cli: No such file or directory` | root `pyproject.toml`이 local `LLaMA-Factory/`와 training stack을 dependency로 관리하지 못함 | `training` dependency group과 editable `llamafactory` source 추가, `uv sync --group training` | 해결 |
| 9 | 480B FP8 calibration SIGKILL | `Loading weights: 40%`, rank `SIGKILL(-9)` | 4 ranks가 checkpoint loading 중 각각 약 200GiB RSS를 사용해 cgroup 800GiB에 도달 | observe-only telemetry로 확인. 아직 구조적 해결 필요 | 미해결 |

# Detailed Notes

## 1. 데이터셋 build가 0건으로 끝난 문제

증상:

```text
Wrote 0 train records to data/processed/aegislm_security_train.jsonl
Wrote 0 validation records to data/processed/aegislm_security_validation.jsonl
Wrote 0 test records to data/processed/aegislm_security_test.jsonl
```

원인:

- `scripts/build_security_dataset.py --output-dir data/processed`만 실행하면 입력 source가 선택되지 않는다.
- 이 경우 builder는 정상 종료하지만 수집할 source가 없어 0건 split을 만든다.

해결:

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

현재 판단:

- 0건 output 자체는 loader 장애가 아니라 command 옵션 문제였다.
- 이후 `--include-hf`는 QA/DiverseVul/BigVul alias로 확장되었다.

## 2. `rezaduty/cybersecurity-qa-v2` 다운로드 실패

증상:

```text
Failed to load rezaduty/cybersecurity-qa-v2: An error occurred while generating the dataset
```

원인:

- `datasets.load_dataset()` 경로에서 parquet/nested row generation 문제가 발생했다.
- fallback dataset만 쓰면 원래 의도한 QA source가 빠져 데이터셋 폭이 줄어든다.

해결:

- Hugging Face Hub에서 `cybersecurity_interview_qa_complete.jsonl`을 직접 읽는 우회 로더를 추가했다.
- fallback으로 `Rowden/CybersecurityQAA`를 유지했다.

현재 상태:

- `rezaduty` primary source는 직접 JSONL loader로 수집 가능하다.
- full build에서는 smoke와 달리 source별 수량 제한을 명시적으로 관리해야 한다.

## 3. DiverseVul secret-like row validation 중단

증상:

```text
aegislm.datasets.validation.SafetyPolicyViolationError:
Record diversevul-002142-92ef10dc4313 may contain sensitive credential secrets.
```

원인:

- 보안 코드 데이터셋에는 `password=`, `api_key=`, `client_secret=` 같은 패턴이 자주 등장한다.
- 초기 policy는 이런 row를 민감정보로 보고 hard fail했다.
- 사용 목적상 이런 패턴 자체가 학습에 필요하지만, 실제 secret 값은 보존하면 안 된다.

해결:

- row를 버리지 않고 secret-like assignment value를 `[REDACTED_SECRET]`로 치환한다.
- metadata/signals에 redaction count를 남긴다.
- 안전 정책은 "패턴은 보존, 실제 값은 제거"로 정리했다.

현재 상태:

- security dataset 성격에 맞게 hardcoded credential 패턴을 포함할 수 있다.
- 단, 실제 secret 값은 target/output에 보존하지 않는다.

## 4. `--max-per-source` 전체 수집 옵션

문제:

- smoke run에서는 source별 100건 제한이 필요하다.
- full run에서는 source별 전체 수집이 필요하다.
- 기존에는 int만 받았고 "전체" 의미가 명확하지 않았다.

해결:

```bash
--max-per-source -1
```

을 전체 수집으로 해석하도록 확장했다.

현재 상태:

- smoke와 full build를 같은 CLI로 구분할 수 있다.
- full export/register는 smoke dataset과 이름을 분리해서 등록한다.

## 5. 자체 memory soft-stop 혼선

증상:

- 480B가 cgroup 800GiB 전에 700GiB 근처에서 조기 종료되는 것처럼 보였다.

원인:

- 우리가 만든 memory watcher에 soft-limit 기반 controlled stop 기능이 있었다.
- `--soft-limit-gib`, `--terminate-pgid`, `--exit-on-soft-limit` 경로가 학습 process group에 signal을 보낼 수 있었다.
- 이 때문에 "서버가 죽였는가, 우리 코드가 죽였는가" 분석이 혼탁해졌다.

해결:

- soft-stop 기능을 retired/disabled 처리했다.
- watcher는 observe-only로만 동작하게 정리했다.
- 다음 필드는 계속 기록한다.
  - cgroup `memory.current`, `memory.peak`, `memory.max`, `memory.events`
  - `cpu.stat`, pressure, pids
  - GPU memory/utilization
  - rank/process별 RSS, CPU, thread count

현재 상태:

- memory watcher는 학습을 kill하지 않는다.
- 480B 최신 실패는 우리 soft-stop이 아니라 외부 `SIGKILL`로 다시 분리되었다.

## 6. DeepSpeed ZeRO-3 dtype mismatch

증상:

```text
TypeError: output tensor must have the same type as input tensor
```

발생 위치:

```text
deepspeed/runtime/zero/stage3.py
deepspeed/runtime/zero/partition_parameters.py
torch.distributed.all_gather_into_tensor
```

확인된 환경:

```text
deepspeed 0.19.2
peft      0.18.1
torch     2.12.1+cu130
```

원인:

- DeepSpeed 0.19.2의 ZeRO-3 all-gather 경로가 mixed dtype persistent parameters를 다룰 때 output buffer dtype을 첫 parameter 기준으로 잡는다.
- PEFT LoRA adapter와 bf16 base model이 섞이면서 dtype mismatch가 발생한 것으로 판단했다.

해결 과정:

1. ZeRO-2 smoke config로 문제를 분리했다.
2. 30B/72B ZeRO-2 1-step smoke가 통과해 dataset, W&B, LLaMA-Factory, PEFT 기본 경로는 정상임을 확인했다.
3. DeepSpeed upstream PR #8073 방식의 reversible patch helper를 추가했다.
4. patch 적용 후 30B/72B ZeRO-3 regression을 다시 실행했다.

최신 결과:

| Model | Config | Result | Loss | Checkpoint |
| --- | --- | --- | ---: | --- |
| Qwen3-Coder-30B-A3B | ZeRO-3 patched | PASS | 2.379 | `model/adapters/qwen3-coder-30b/lora/smoke/checkpoint-1` |
| Qwen2-72B | ZeRO-3 patched | PASS | 2.066 | `model/adapters/qwen2-72b/lora/smoke/checkpoint-1` |

현재 상태:

- 30B/72B 기준으로는 ZeRO-3 dtype mismatch가 해결된 것으로 본다.
- 480B 실패는 이 dtype bug와 별개로 checkpoint loading/cgroup 문제로 분리한다.

관련 문서:

- [LLaMA-Factory DeepSpeed ZeRO-3 LoRA BF16 Dtype Mismatch](../../../errors/llamafactory-deepspeed-zero3-dtype-mismatch.md)
- [DeepSpeed ZeRO-3 Dtype Mismatch Troubleshooting](../repos/AegisLM/docs/DEEPSPEED_ZERO3_DTYPE_MISMATCH.md)

## 7. LLaMA-Factory dependency check 즉시 실패

증상:

```text
ImportError: datasets>=2.16.0,<=4.0.0 is required ... found datasets==4.8.5
```

확인된 환경:

```text
datasets     4.8.5
transformers 5.6.0
deepspeed    0.19.2
peft         0.18.1
torch        2.12.1
```

원인:

- 설치된 LLaMA-Factory `0.9.6.dev0`는 `datasets>=2.16.0,<=4.0.0`을 요구한다.
- 서버 `.venv`에는 `datasets==4.8.5`가 들어 있었다.
- 따라서 model loading이나 DeepSpeed 이전에 LLaMA-Factory 자체 version guard에서 바로 실패했다.

해결:

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}
uv pip install "datasets==4.0.0"
```

확인:

```text
datasets     4.0.0
transformers 5.6.0
deepspeed    0.19.2
peft         0.18.1
torch        2.12.1
```

현재 상태:

- `pyproject.toml`에 `datasets>=2.16.0,<=4.0.0` 범위를 반영했다.
- `uv.lock`도 이 정책을 기준으로 갱신했다.
- 이 문제 때문에 실패한 run은 30B/72B/480B 공통으로 "시작 직후 실패"처럼 보였지만, model 문제는 아니었다.

## 7-1. LLaMA-Factory CLI 누락과 training group 복구

증상:

```text
scripts/run_observed_llamafactory_train.sh: line 45: .venv/bin/llamafactory-cli: No such file or directory
```

원인:

- `.venv` 안에 `llamafactory-cli`가 없었다.
- `torch`, `peft`, `accelerate`, `trl`도 학습 runtime으로 설치되어 있지 않은 상태였다.
- root `pyproject.toml`이 local `LLaMA-Factory/` checkout을 dependency로 등록하지 않았기 때문에 `.venv` 재구성 시 학습 환경이 복원되지 않았다.

해결:

`pyproject.toml`에 training group과 editable local source를 추가했다.

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

검증 결과:

```text
LLaMA Factory 0.9.6.dev0
torch 2.12.1+cu130
CUDA available: True
CUDA devices: 4
datasets 4.0.0
peft 0.18.1
accelerate 1.11.0
trl 0.24.0
```

주의:

- `uv sync --group training` 이후에는 DeepSpeed site-package patch가 원복될 수 있다.
- 따라서 sync 후에는 반드시 `.venv/bin/python scripts/patch_deepspeed_zero3_dtype.py check`를 실행한다.

관련 문서:

- [LLaMA-Factory CLI Missing After Dependency Drift](../../../errors/llamafactory-cli-missing-after-uv-sync.md)

## 8. 480B FP8 checkpoint loading `SIGKILL`

증상:

```text
Loading weights: 40%|████      | 276/685
Root Cause:
rank 3 (local_rank: 3)
exitcode: -9
traceback: Signal 9 (SIGKILL)
```

최신 관측:

```text
experiment_id: qwen3-coder-480b-fp8-lora-calibration-10-z3-patched
time: 2026-07-03T03:05:40 -> 2026-07-03T03:18:27 UTC
cgroup limit: 800 GiB
cgroup current max: 800 GiB
memory.events oom: 196 -> 246
memory.events oom_kill: 7 -> 8
max GPU memory used: 1688 MiB
rank RSS: 약 200 GiB x 4
```

해석:

- GPU memory는 거의 쓰기 전이므로 CUDA OOM이 아니다.
- host 전체 RAM은 충분해도 container cgroup limit이 800GiB이면 프로세스는 그 이상 사용할 수 없다.
- 4개 rank가 checkpoint loading 중 각각 약 200GiB RSS를 사용하면서 총량이 cgroup limit에 닿은 것으로 보인다.
- `torchrun` 로그에서 나머지 rank의 `SIGTERM(-15)`은 root cause가 아니라, 한 rank가 `SIGKILL(-9)`된 뒤 torchrun이 sibling rank를 정리한 결과다.

현재 상태:

- 480B는 10-step calibration도 training step까지 도달하지 못했다.
- 문제 지점은 optimizer, W&B, dataset이 아니라 checkpoint loading이다.

가능한 다음 선택지:

1. 같은 LLaMA-Factory 경로에서 `nproc=1/2/4` load-only RSS를 비교한다.
2. container cgroup `memory.max`를 800GiB보다 높인 뒤 같은 calibration을 재실행한다.
3. LLaMA-Factory/DeepSpeed 대신 Megatron/NeMo 계열처럼 480B급 model parallelism에 더 가까운 framework로 전환한다.
4. 작은 모델로 pipeline 검증을 계속하고, 480B는 별도 large-model loading strategy를 세운다.

관련 문서:

- [LLaMA-Factory Qwen3-Coder 480B FP8 SIGKILL Investigation](../../../errors/llamafactory-qwen3-coder-480b-fp8-oom-kill.md)
- [B200 Qwen3-Coder 480B SIGKILL Analysis Process](../repos/AegisLM/docs/B200_QWEN3_480B_MEMORY_PROCESS.md)
- [B200 Qwen3-Coder 480B Training Gate Guide](b200_480b_training_gate_guide.md)

# Stable Runbook

## 환경 복구 확인

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}
uv pip show datasets transformers deepspeed peft torch
```

기대값:

```text
datasets 4.0.0
deepspeed 0.19.2
peft 0.18.1
torch 2.12.1
transformers 5.6.0
```

## 실행 전 환경변수

```bash
set -a
. ./.env
set +a

export CUDA_VISIBLE_DEVICES=0,1,2,3
export WANDB_PROJECT=malware-analysis-llm
export WANDB_LOG_MODEL=false
export WANDB_WATCH=false
```

## 검증 순서

```bash
bash scripts/run_smoke_qwen3_coder_30b.sh
bash scripts/run_smoke_qwen2_72b.sh
bash scripts/run_calibrate_qwen3_coder_480b_fp8_10_z3_patched.sh
```

주의:

- 현재는 `uv run python ...`을 장시간 학습 실행에 쓰지 않는다.
- runner script는 PATH/PYTHONPATH와 watcher 실행을 함께 잡아주므로 직접 `llamafactory-cli train ...`보다 안전하다.
- 480B는 30B/72B가 통과한 뒤에만 재시도한다.

# Decisions

- `model/` 아래 base model, adapter, checkpoint, run log를 모으고 Git에는 올리지 않는다.
- W&B secret과 HF token은 `.env` 또는 shell env로만 주입한다.
- memory watcher는 observe-only다. 학습 프로세스를 직접 kill하지 않는다.
- 30B/72B는 LLaMA-Factory/DeepSpeed/PEFT/W&B 경로의 기준선으로 사용한다.
- 480B는 cgroup memory limit 또는 framework/model-parallelism 문제를 해결하기 전 full training으로 넘어가지 않는다.

# Next Actions

1. tokenizing/export가 끝나면 Qwen3-Coder-Next 80B full training을 runner script로 시작한다.
2. `uv sync --group training`을 다시 실행한 경우 DeepSpeed ZeRO-3 dtype patch 상태를 재확인한다.
3. 480B `nproc=1`, `2`, `4` load-only probe로 rank 수와 RSS 증가가 선형인지 확인한다.
4. container `memory.max`를 조정할 수 있는지 서버 운영 측면에서 확인한다.
5. cgroup limit 증설이 어렵거나 LLaMA-Factory loader가 계속 중복 로딩하면 Megatron/NeMo 계열 실험으로 전환한다.
6. 480B calibration 결과는 매번 `model/runs/logs/`와 `model/runs/memory/`의 timestamp를 짝지어 기록한다.

# Related Concepts

- [B200 Server Fine-Tuning](B200_server.md)
- [Security Datasets](../data/security_datasets.md)
- [LLaMA-Factory + W&B Fine-Tuning Integration](../training/llamafactory_wandb_finetuning.md)
- [B200 Qwen3-Coder 480B Training Gate Guide](b200_480b_training_gate_guide.md)
- [LLaMA-Factory Qwen3-Coder 480B FP8 SIGKILL Investigation](../../../errors/llamafactory-qwen3-coder-480b-fp8-oom-kill.md)
- [LLaMA-Factory DeepSpeed ZeRO-3 LoRA BF16 Dtype Mismatch](../../../errors/llamafactory-deepspeed-zero3-dtype-mismatch.md)
- [LLaMA-Factory CLI Missing After Dependency Drift](../../../errors/llamafactory-cli-missing-after-uv-sync.md)
