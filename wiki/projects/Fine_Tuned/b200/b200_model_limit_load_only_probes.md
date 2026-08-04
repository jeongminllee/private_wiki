---
type: Project
title: B200 Model Limit Load-Only Probes
description: B200 4-GPU 서버의 800GiB container RAM 조건에서 후보 LLM의 로딩 가능 한계를 측정하는 load-only 테스트 계획과 구현 기록
tags: [project, b200, llm, vllm, sglang, telemetry]
timestamp: 2026-07-03
status: active
---

# Goal

B200 서버의 현재 container RAM 약 800GiB 조건에서 어떤 모델까지 “로딩 가능”한지 확인한다.

이번 1차 범위는 fine-tuning, optimizer step, serving benchmark가 아니라 **load-only**다. 즉, 모델 서버가 뜨고 `/v1/models` readiness에 도달하는지 또는 어떤 지점에서 실패하는지만 본다.

# Candidate List

| Key | HF model id | 1차 목적 | dry-run 예상 크기 |
| --- | --- | --- | ---: |
| `qwen3_coder_next` | `Qwen/Qwen3-Coder-Next` | 80B coder instruct/posttrain 계열 | 148.43 GiB |
| `qwen3_coder_next_base` | `Qwen/Qwen3-Coder-Next-Base` | 80B coder base 계열 | 148.43 GiB |
| `glm45_air_fp8` | `zai-org/GLM-4.5-Air-FP8` | GLM Air FP8 경량 기준 | 104.85 GiB |
| `deepseek_v4_flash` | `deepseek-ai/DeepSeek-V4-Flash` | DeepSeek Flash instruct 계열 | 148.67 GiB |
| `deepseek_v4_flash_base` | `deepseek-ai/DeepSeek-V4-Flash-Base` | DeepSeek Flash base 계열 | 274.45 GiB |
| `glm45_full_fp8` | `zai-org/GLM-4.5-FP8` | Full GLM FP8 한계 후보 | 336.50 GiB |

근거:

- GLM-4.5 collection은 GLM-4.5 full/Air와 FP8 variants를 제공한다. GLM-4.5는 355B total / 32B active, GLM-4.5-Air는 106B total / 12B active로 설명된다.
- Qwen3-Coder-Next는 80B total / 3B activated 모델로 공개되어 있다.
- DeepSeek-V4 collection과 Flash/Base 모델 페이지가 Hugging Face에 공개되어 있다.

# Implemented Files

원격 프로젝트 `${MALWARE_ANALYSIS_LLM_ROOT}`의 B200 실험 브랜치에 다음 파일을 추가했다.

- `experiments/model_limits/candidates.json`
- `aegislm/experiments/model_limits.py`
- `scripts/run_model_limit_probe.py`
- `docs/MODEL_LIMIT_PROBES.md`
- `tests/test_model_limits.py`

`docs/README.md`에는 `MODEL_LIMIT_PROBES.md` 링크를 추가했다.

# Probe Phases

```bash
cd ${MALWARE_ANALYSIS_LLM_ROOT}

.venv/bin/python scripts/run_model_limit_probe.py --phase summary
.venv/bin/python scripts/run_model_limit_probe.py --phase dry-run-files --all
.venv/bin/python scripts/run_model_limit_probe.py --phase inspect-local --all
.venv/bin/python scripts/run_model_limit_probe.py --phase config-only --all
```

실제 heavy load-only는 후보 하나씩 실행한다.

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
export HF_HUB_OFFLINE=1

.venv/bin/python scripts/run_model_limit_probe.py \
  --phase load-only \
  --candidate qwen3_coder_next \
  --backend vllm \
  --allow-heavy
```

`--allow-heavy`가 없으면 load-only 서버 프로세스를 시작하지 않는다. 다운로드도 `--download`가 있을 때만 수행한다.

# Telemetry

load-only 실행 중에는 기존 observe-only memory watcher를 재사용한다.

출력 위치:

```text
model/runs/model_limits/<timestamp>/
```

기록 항목:

- `results.jsonl`
- `summary.md`
- backend stdout/stderr log tail
- cgroup `memory.current`, `memory.peak`, `memory.events`
- host `MemAvailable`
- GPU memory/utilization
- top process RSS/thread count

중요한 점: watcher는 관측 전용이다. 메모리 기준으로 학습/로드 프로세스를 중단시키지 않는다.

# 2026-07-03 Dry Checks

검증 결과:

- `summary`: 후보 6개 정상 출력.
- `inspect-local --all`: 6개 후보 모두 `not_downloaded`.
- `dry-run-files --all`: 6개 후보 모두 Hugging Face 파일 목록과 예상 크기 조회 성공. 실제 다운로드는 수행하지 않음.
- `pytest tests/test_model_limits.py`: 6 passed.
- `ruff check aegislm/experiments/model_limits.py scripts/run_model_limit_probe.py tests/test_model_limits.py`: passed.
- `ruff format --check ...`: passed after formatting.
- `mypy aegislm/experiments/model_limits.py tests/test_model_limits.py`: passed.

# Current Status

아직 6개 신규 후보는 서버 `model/base/...`에 다운로드되어 있지 않다.

다음 단계는 사용자가 명시적으로 선택한 후보부터 `--download` 또는 기존 로컬 모델 배치를 진행한 뒤, `config-only -> load-only` 순서로 관측하는 것이다.

# Related Concepts

- [MalwareAnalysisLLM LLM Candidate Matrix](llm_candidate_matrix_20260703.md)
- [B200 Fine-Tuning Troubleshooting Report](b200_finetuning_troubleshooting_report_20260703.md)
- [W&B and Telemetry Basics](../fundamentals/wandb_telemetry_basics.md)
- [B200 Qwen3-Coder 480B Training Gate Guide](b200_480b_training_gate_guide.md)

# Citations

- [GLM-4.5 collection](https://huggingface.co/collections/zai-org/glm-45)
- [GLM-4.5-FP8](https://huggingface.co/zai-org/GLM-4.5-FP8)
- [GLM-4.5-Air-FP8](https://huggingface.co/zai-org/GLM-4.5-Air-FP8)
- [Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next)
- [Qwen3-Coder-Next-Base](https://huggingface.co/Qwen/Qwen3-Coder-Next-Base)
- [DeepSeek-V4 collection](https://huggingface.co/collections/deepseek-ai/deepseek-v4)
- [DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)
- [DeepSeek-V4-Flash-Base](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base)
