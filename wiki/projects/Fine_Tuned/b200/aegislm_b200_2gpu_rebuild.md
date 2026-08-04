---
type: Project
title: AegisLM-B200 2-GPU 재구축
description: Qwen3-Coder-Next 80B를 B200 2장과 400GiB cgroup 환경에서 학습하기 위한 저장소·환경·데이터·모델·체크포인트 준비 기록
tags: [aegislm, b200, llamafactory, qwen3-coder-next, fine-tuning]
timestamp: 2026-07-20
status: ready
---

# Goal

최신 AegisLM `main`과 과거 B200 실험 코드를 선별 통합하여, B200 2장 환경에서 `Qwen/Qwen3-Coder-Next` 80B LoRA 학습을 재현 가능하게 준비한다.

# Current Status

- Private 저장소: [Malicious-code-detection-project/AegisLM-B200](https://github.com/Malicious-code-detection-project/AegisLM-B200)
- Draft PR: [#1 Rebuild two-GPU B200 training profile](https://github.com/Malicious-code-detection-project/AegisLM-B200/pull/1)
- 서버 코드: `${AEGISLM_B200_ROOT}`
- 서버 커밋: `c90de3bd19d74417be4d7d67e639392c223a12e5`
- stable profile: ready
- fast profile: `nvcc` 부재로 blocked
- 실제 80B model load와 training: 시작하지 않음

# Structure

| 구분 | 경로 |
| --- | --- |
| 코드·venv | `${AEGISLM_B200_ROOT}` |
| 모델 | `${MODEL_ROOT}` |
| 데이터 | `${DATA_ROOT}` |
| 로그·checkpoint | `${TRAINING_ARTIFACTS_ROOT}` |

프로젝트의 `model`과 `data`는 persistent 경로를 가리키는 symlink다. 관련 개념은 [Symlink](../../../infra/symlink.md)를 참고한다.

# Verified Environment

- GPU: NVIDIA B200 2장, 각 183,359MiB
- effective cgroup `memory.max`: 400.0GiB
- LlamaFactory: v0.9.5 submodule
- Python 3.12, Torch 2.12.1, Transformers 5.6.0
- datasets 4.0.0, DeepSpeed 0.19.2, PEFT 0.18.1
- DeepSpeed ZeRO-3 mixed dtype patch 적용·확인
- Linux 검증: pytest 100 passed, Ruff·mypy 통과
- `.env`: mode 600, HF/W&B 설정 존재 확인, 값은 기록하지 않음

MIG Mode의 `Disabled`는 GPU를 분할하지 않고 전체 B200을 쓰는 현재 구성에서 정상이다. Persistence Mode는 `On`, Compute Mode는 `Default`로 확인했다.

# Dataset

`hf-full-v1`은 seed 42, split 0.8/0.1/0.1로 생성했다.

| Source | Converted | Skipped |
| --- | ---: | ---: |
| Cybersecurity QA | 709 | 0 |
| DiverseVul | 264,392 | 0 |
| BigVul | 150,908 | 0 |

| Split | Records |
| --- | ---: |
| Train | 332,807 |
| Validation | 41,600 |
| Test | 41,602 |

HF revision과 split별 SHA256은 서버의 `data/processed/hf-full-v1/dataset_manifest.json`에 기록했다. 로컬 CTF/ZIP corpus는 첫 profile에서 `not_available`이다. 데이터 정책과 변환 방식은 [Security Datasets](../data/security_datasets.md)를 참고한다.

전처리 첫 실행은 record마다 schema를 중복 검증하고 split 후 전체를 다시 검증해 1시간 이상 소요됐다. precompiled validator를 재사용하고 split label 변경 뒤 중복 전수 검증을 제거한 뒤 약 7분에 완료됐다.

# Model

- Model ID: `Qwen/Qwen3-Coder-Next`
- Revision: `a7fbcb5c0e12d62a448eaa0e260346bf5dcc0feb`
- Safetensors: 148.41GiB, 40 shards
- Missing shards: 0
- Manifest: `model/base/qwen3-coder-next/aegislm_model_manifest.json`

# Checkpoint Policy

- `save_steps: 500`
- `save_total_limit: 1`
- `save_only_model: false`
- 로컬 최신 checkpoint 실파일 1개 유지
- persistent 최신 checkpoint 실파일 1개 atomic mirror
- mirror 실패는 trainer에 signal을 보내지 않고 로그만 남김
- `auto` resume에서 로컬과 persistent step이 다르면 자동 선택하지 않음

dummy `checkpoint-500`으로 mirror와 `auto` resume 선택을 검증했다. 이전 checkpoint 유실 사례는 [LLaMA-Factory Checkpoint Save Failed Because Model Symlink Target Disappeared](../../../errors/llamafactory-checkpoint-save-broken-model-symlink.md)와 연결된다.

# How to Run

실행 전:

```bash
cd ${AEGISLM_B200_ROOT}
set -a
. ./.env
set +a

.venv/bin/python scripts/check_environment.py \
  --profile stable \
  --require-model \
  --require-data \
  --require-secrets
```

최초 학습은 사용자가 foreground에서 직접 시작한다.

```bash
bash scripts/run_train_qwen3_coder_next_full.sh \
  --profile stable \
  --resume fresh
```

재개:

```bash
bash scripts/run_train_qwen3_coder_next_full.sh \
  --profile stable \
  --resume auto
```

global batch는 `per_device 1 × GPU 2 × accumulation 16 = 32`다. W&B 해석은 [W&B Training Metrics Guide](../training/wandb_training_metrics_guide.md)를 참고한다.

# Key Decisions

- smoke가 아니라 full dataset real training config를 준비한다.
- setup 단계에서는 실제 model load/training을 자동 시작하지 않는다.
- memory watcher는 observe-only이며 trainer를 종료하지 않는다.
- fast kernel profile은 stable 환경과 분리하고 `nvcc`가 준비되기 전까지 blocked로 둔다.

# Issues

- 조직 정책으로 repository deploy key 등록이 비활성화돼 있다.
- 현재 `gh` token에는 서버 사용자 SSH key 등록에 필요한 `admin:public_key` scope가 없다.
- 초기 서버 배포는 검증된 Git bundle로 완료했다. 향후 private 저장소 pull 전에는 서버 Git 인증을 별도로 설정해야 한다.

# Next Actions

1. Draft PR #1을 리뷰하고 병합한다.
2. 서버 Git SSH 인증을 설정한다.
3. 사용자가 full training 명령을 foreground에서 실행한다.
4. W&B, training log, cgroup telemetry, checkpoint mirror를 함께 관측한다.

# Related Concepts

- [B200 Full-Size Training Queue](b200_full_size_training_queue.md)
- [LLaMA-Factory + W&B Fine-Tuning](../training/llamafactory_wandb_finetuning.md)
- [DeepSpeed ZeRO Basics](../fundamentals/deepspeed_zero_basics.md)
- [Distributed Training Basics](../fundamentals/distributed_training_basics.md)
