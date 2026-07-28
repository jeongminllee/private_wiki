---
type: Project
title: Qwen3-Coder-Next 80B B200 2-GPU Real Training Run
description: B200 2장과 400GiB cgroup에서 Qwen3-Coder-Next 80B LoRA 실제 학습의 로딩, 메모리, 속도, loss, checkpoint를 추적하는 실행 기록
tags: [finetuning, qwen3-coder-next, b200, deepspeed, zero3, wandb]
timestamp: 2026-07-20
status: active
---

# Goal

이번 실행을 이후 모델 선택과 독립 실행을 위한 기준선으로 남긴다. 모델 로딩과 실제 학습을 분리해 CPU RAM, GPU VRAM, 처리 속도, loss, evaluation, checkpoint 저장 상태를 추적한다.

# Run Configuration

| 항목 | 값 |
| --- | --- |
| Model | `Qwen/Qwen3-Coder-Next` BF16, 전체 약 79.7B / 활성 약 3B |
| GPUs | NVIDIA B200 2장, GPU당 약 179GiB |
| Container memory | 400GiB cgroup limit |
| Framework | LLaMA-Factory v0.9.5 |
| Distributed runtime | DeepSpeed ZeRO-3 |
| Fine-tuning | LoRA rank 8 / alpha 16 |
| Dataset | `hf-full-v1`, train 332,807건 |
| Sequence length | 2,048 |
| Micro batch | GPU당 1 |
| Gradient accumulation | 16 |
| Global batch | 32 |
| Epoch / update steps | 1 epoch / 10,401 steps |
| Logging / eval / save | 5 / 500 / 500 steps |

# Timeline

## Model Loading

- `DeepSpeed zero.init()`에서 ZeRO-3 parameter partitioning을 시작했다.
- FLA와 `causal-conv1d`가 없어 Torch fallback을 사용했다. 이는 비치명적 성능 경고다.
- cgroup memory가 `400.0GiB`에 도달했고 `memory.events.max`가 증가했지만, `oom`과 `oom_kill`은 증가하지 않았다.
- GPU memory는 로딩 중 GPU당 약 `80.6GiB`까지 올라갔다.
- 로딩을 통과한 뒤 CPU RAM이 크게 반환되고 실제 training loop에 진입했다.

## Early Training

2026-07-20 19:29 KST, 약 step 281에서 확인한 값이다.

| 지표 | 관측값 |
| --- | --- |
| GPU memory | GPU당 약 `90.7GiB` |
| GPU utilization | 순간 `0~100%`, 확인 시 대체로 `60~70%` |
| cgroup current | 약 `22.3GiB` |
| cgroup peak | `400.0GiB` |
| cgroup OOM / OOM kill | `0 / 0` |
| Step time | 약 `32~33초` |
| Step 5 loss | `2.117` |
| Step 10 loss | `2.119` |
| Step 260 loss | `0.01023` |
| Step 280 loss | `0.008331` |

사용자가 화면에서 약 `70GB`를 관측했지만 어떤 memory metric인지 확정되지 않았다. 같은 시점대 telemetry에서는 GPU memory가 약 `90.7GiB`로 유지되고 GPU utilization이 약 `60~70%`였다. 이후 비교에서는 VRAM allocated, GPU utilization, cgroup current를 구분해 기록한다.

# Interpretation

- GPU memory와 GPU utilization은 다른 값이다. 가중치가 GPU에 상주하면 utilization이 낮은 순간에도 VRAM은 유지된다.
- 로딩 peak와 training steady state도 다르다. 현재 경로의 우선 병목은 학습 중 VRAM보다 ZeRO-3 로딩 순간의 400GiB CPU RAM이다.
- 초반 loss가 `2.1`에서 `0.01` 부근으로 빠르게 하락했다. 이를 성능 향상으로 단정하지 않고 step 500 validation loss와 출력 품질로 과적합, 반복적인 target, 쉬운 label 구조 여부를 확인한다.
- 동일 모델을 다시 실행할 때는 현재 수치를 기준으로 config 변경 전후를 비교한다.

## Step 500-1,500 Evaluation Observations

2026-07-21 14:00 KST 기준 step 1,500 이후 세 번째 full validation이 진행 중이다.

| 관측 지점 | 결과 |
| --- | --- |
| Step 500 evaluation | `eval_loss=0.004252`, runtime 약 12,610초(약 3시간 30분) |
| Step 500 checkpoint | 저장 및 persistent mirror 성공 |
| Step 1,000 evaluation | `eval_loss=0.0003558`, runtime 약 12,640초(약 3시간 31분) |
| Step 1,000 checkpoint | 저장 및 persistent mirror 성공, 약 201MiB |
| Step 1,500 evaluation | 2026-07-21 13:34 KST 시작, 관측 시 진행 중 |
| Evaluation GPU memory | GPU당 약 `106~108GiB`, 약 90분 동안 평탄하게 유지 |
| Evaluation GPU free memory | GPU당 약 `70~72GiB` |
| Evaluation throughput | 약 `1.65 step/s`, validation batch 총 20,800개 |

Evaluation에서 VRAM이 training steady state의 약 90.7GiB보다 15~17GiB 증가했지만 지속 증가하는 leak 패턴은 관측되지 않았다. 총 VRAM 179GiB 대비 약 40%가 남아 있어 현재 모델의 즉시 OOM 위험은 낮다.

반면 full validation 1회가 약 3시간 30분 걸리고 `eval_steps=500`이므로, 1 epoch에서 약 20회의 evaluation이 실행될 수 있다. 현재 설정을 끝까지 유지하면 evaluation만 약 70시간을 차지할 수 있다. 현재 run은 재현 가능한 기준선을 위해 변경하지 않되, 다음 run에서는 evaluation frequency와 validation subset 정책을 별도 결정한다.

# Next Observation Gates

1. Step 1,500 evaluation 완료와 checkpoint mirror 성공을 확인한다.
2. checkpoint local/persistent 최신본이 각각 하나인지 확인한다.
3. checkpoint 저장 중 일시적인 RAM, VRAM, step time 증가를 기록한다.
4. Step 2,000 이후 training/evaluation 합산 ETA를 다시 계산한다.
5. 종료 시 total runtime, 최종 loss/eval loss, peak memory, resume 검증 결과를 추가한다.

# Post-Run Outcome — 2026-07-28

학습은 `10,401 / 10,401 step`, 1 epoch를 완료했고 총 `7일 34분 41초`가 걸렸다. 마지막 loss는 약 `1.5e-6`까지 감소했다. LoRA adapter를 base model에 병합한 BF16 checkpoint는 vLLM `0.26.0` TP2로 정상 서빙됐다.

그러나 250개 취약·250개 정상 label-blind challenge에서 TP/FP/TN/FN은 `84/116/0/166`, precision `0.420`, recall `0.336`, JSON parse `0.556`이었다. 정상 코드 250건 중 유효한 `low` 판정은 0건이었다.

train 데이터를 감사한 결과 DiverseVul 211,333건 전부의 model-visible prompt에 label과 target이 있었고 expected output은 전체 JSON 기준 약 20개 형태로 집중됐다. BigVul 120,897건도 취약 코드라는 정보를 입력에 노출하고 모두 `high`로 학습했다.

따라서 초반 loss 급락은 실제 코드 분석 능력 향상보다 target leakage와 반복 target 학습의 조기 신호였다고 재해석한다. 다음 실험은 기존 33만 건 full run을 반복하지 않고, [1–2만 건 데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md)을 적용한다.

# Monitoring Paths

```text
/NHNHOME/WORKSPACE/26moel002_ex07/LLM/TrainingArtifacts/runs/qwen3-coder-next/lora/full/training-stable.log
/NHNHOME/WORKSPACE/26moel002_ex07/LLM/TrainingArtifacts/runs/qwen3-coder-next/lora/full/memory/*.jsonl
/NHNHOME/WORKSPACE/26moel002_ex07/LLM/TrainingArtifacts/runs/qwen3-coder-next/lora/full/memory/*.csv
/NHNHOME/WORKSPACE/26moel002_ex07/LLM/TrainingArtifacts/wandb/
```

# Related Concepts

- [LLM 생명주기 환경 설계](../../../infra/llm-lifecycle-environment-design.md)
- [W&B Training Metrics Guide](wandb_training_metrics_guide.md)
- [LLaMA-Factory and W&B Fine-Tuning](llamafactory_wandb_finetuning.md)
- [AegisLM 데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md)
- [AegisLM-B200 2-GPU Rebuild](../b200/aegislm_b200_2gpu_rebuild.md)
- [DeepSpeed ZeRO Basics](../fundamentals/deepspeed_zero_basics.md)
