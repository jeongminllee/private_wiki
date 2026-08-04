---
type: Error Note
title: LLaMA-Factory Qwen3-Coder 480B FP8 SIGKILL Investigation
description: B200 4-GPU 컨테이너에서 Qwen3-Coder-480B-A35B-Instruct-FP8 LoRA smoke fine-tuning이 checkpoint loading 약 40% 지점에서 SIGKILL된 사건 분석
tags: [error, llm, finetuning, llamafactory, deepspeed, b200]
timestamp: 2026-07-02
status: active
---

# Situation

`${MALWARE_ANALYSIS_LLM_ROOT}`의 `experiment/b200-qwen3-coder-480b` 브랜치에서 LLaMA-Factory와 DeepSpeed ZeRO-3를 사용해 `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8` LoRA smoke SFT를 실행했다.

데이터셋 export, tokenizer/preprocessing 단계는 통과했지만, 모델 checkpoint weight loading 약 39-40% 지점에서 반복적으로 종료되었다.

# Error Message

대표 로그:

```text
Loading weights: 40%|...
failed (exitcode: -9) local_rank: 0
traceback : Signal 9 (SIGKILL) received by PID ...
```

다른 rank의 `SIGTERM`은 root cause가 아니다. 하나의 rank가 `SIGKILL`된 뒤 `torchrun`이 나머지 rank를 정리하면서 보낸 종료 신호다.

# Additional Observation: 2026-07-02 15:44 KST

두 번째 관측에서는 torchrun 로그와 `scripts/check_memory_budget.py --watch` JSONL 마지막 4개 샘플을 함께 확인했다.

torchrun 관측:

- rank 0, local rank 0, PID `258460`이 `SIGKILL(-9)`로 먼저 종료되었다.
- rank 1-3은 각각 `SIGTERM(-15)`을 받았다.
- Python traceback이나 `CUDA out of memory` 메시지는 없었다.

memory watcher 관측:

| KST time | cgroup current | cgroup limit | oom | oom_kill | train ranks | rank RSS |
|---|---:|---:|---:|---:|---:|---|
| 15:44:42 | 800.00 GiB | 800.00 GiB | 109 | 4 | 4 | 약 200 GiB x 4 |
| 15:44:47 | 792.88 GiB | 800.00 GiB | 156 | 5 | 3 | 약 199 GiB x 3 |
| 15:44:52 | 517.43 GiB | 800.00 GiB | 156 | 5 | 0 | worker 사라짐 |
| 15:44:57 | 109.46 GiB | 800.00 GiB | 156 | 5 | 0 | worker 사라짐 |

# Current Interpretation

확정할 수 있는 사실:

- torchrun 로그 단독으로는 왜 `SIGKILL`이 발생했는지 알 수 없다.
- `SIGKILL(-9)`은 Python 예외가 아니라 외부 kill 신호다.
- GPU memory는 각 GPU 약 1.6 GiB 수준이어서 GPU OOM으로 보기 어렵다.
- host `MemAvailable`은 1.4-2.0 TiB 수준으로 남아 있어 host 전체 RAM 고갈로 보기 어렵다.
- Docker/container cgroup effective `memory.max`는 800 GiB였고, watcher는 `memory.current`가 이 값에 닿은 시점을 기록했다.
- 같은 구간에서 `memory.events`의 `oom_kill` 값이 4에서 5로 증가했다.

주의할 점:

- 이 문서는 원인을 "OOM으로 확정"하지 않는다.
- 다만 현재까지의 증거는 "컨테이너 cgroup memory limit에 의한 kill" 가설을 가장 강하게 지지한다.
- host RAM 2.2 TiB 중 800 GiB만 쓴 것처럼 보여도, 해당 컨테이너가 800 GiB cgroup limit 안에 있으면 프로세스는 나머지 host RAM을 사용할 수 없다.

# PID, CPU Core, Rank 구분

관측된 4개의 PID는 CPU core 4개를 의미하지 않는다. `torchrun --nproc_per_node 4`가 만든 4개의 distributed rank 프로세스다.

- 일반적으로 4 GPU 학습에서는 GPU 1장당 rank 1개를 둔다.
- 각 rank 프로세스는 내부적으로 여러 CPU thread를 사용할 수 있다.
- PID/rank를 더 늘리는 것은 CPU core를 더 "할당"하는 것과 다르다.
- checkpoint loading 단계에서 각 rank가 모델 shard를 중복으로 읽거나 펼친다면, rank를 늘릴수록 총 RSS가 더 커질 수 있다.

따라서 "CPU에서 터진 문제인지"는 별도 실험으로 확인해야 하지만, 단순히 PID/rank 수를 늘리는 것은 현재 증상에 대한 안전한 해결책으로 보기 어렵다.

# Investigation Direction

다음 단계에서는 CPU, RAM, cgroup, loader 경로를 분리해서 확인한다.

1. `nproc=1`, `2`, `4`별 model load-only RSS를 측정한다.
2. 각 rank의 CPU 사용률, thread 수, RSS, VSZ를 함께 기록한다.
3. cgroup `memory.events`뿐 아니라 `cpu.stat`, `pids.current`, `pids.max`, `memory.pressure`, `cpu.pressure`도 함께 확인한다.
4. 순수 `transformers.from_pretrained` 경로와 LLaMA-Factory launcher 경로를 비교한다.
5. DeepSpeed ZeRO 설정이 checkpoint loading 시점에 실제로 어떤 영향을 주는지 확인한다.
6. 컨테이너 memory limit을 변경할 수 있다면, 같은 실험을 반복해 40% 지점 SIGKILL이 사라지는지 확인한다.

# Prevention

- 480B급 모델에서는 training config 실행 전 "model load only" preflight를 먼저 수행한다.
- `free -h`만 보지 않고 Docker/cgroup ancestor의 `memory.max`, `memory.peak`, `memory.events`를 함께 확인한다.
- GPU memory만 보지 않고 cgroup event, CPU stat, pids stat, rank별 RSS/thread 수를 함께 기록한다.
- `SIGKILL`/exit code `-9`는 Python exception이 아니므로 마지막 traceback보다 system/cgroup telemetry를 먼저 확인한다.
- B200 전용 실행에서는 memory watcher JSONL/CSV를 기본 분석 자료로 남긴다.

# Related Concepts

- [LLaMA-Factory + W&B Fine-Tuning Integration](../projects/Fine_Tuned/training/llamafactory_wandb_finetuning.md)
- [B200 Server Fine-Tuning](../projects/Fine_Tuned/b200/B200_server.md)
- [Security Datasets](../projects/Fine_Tuned/data/security_datasets.md)
- [2026-07-02 15:44 raw failure log](../../raw/error-logs/b200-qwen3-480b-fp8-sigkill-20260702-1544.md)

# Citations

- Local server log: `${MALWARE_ANALYSIS_LLM_ROOT}/model/runs/qwen3-coder-480b-fp8/lora/smoke/train_fp8_ds_20260702_050414.log`
- Raw sanitized record: [B200 Qwen3-Coder 480B FP8 SIGKILL at 2026-07-02 15:44 KST](../../raw/error-logs/b200-qwen3-480b-fp8-sigkill-20260702-1544.md)
- Local cgroup counters checked on 2026-07-02.
