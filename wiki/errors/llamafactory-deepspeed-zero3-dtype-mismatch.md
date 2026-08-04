---
type: Error Note
title: LLaMA-Factory DeepSpeed ZeRO-3 LoRA BF16 Dtype Mismatch
description: B200 서버에서 30B/72B LoRA smoke training이 첫 optimizer step에서 DeepSpeed ZeRO-3 all_gather dtype mismatch로 실패한 사건 분석
tags: [error, llm, finetuning, llamafactory, deepspeed, zero3, lora, bf16]
timestamp: 2026-07-03
status: investigating
---

# Situation

`${MALWARE_ANALYSIS_LLM_ROOT}`의 `experiment/b200-qwen3-coder-480b` 브랜치에서 30B/72B smoke fine-tuning을 실행했다. 두 run 모두 model loading 이후 training loop에 진입했지만, 첫 optimizer step에서 동일한 오류로 중단되었다.

이 문제는 `Qwen3-Coder-480B-A35B-Instruct-FP8`의 checkpoint loading 중 SIGKILL 문제와 분리해서 본다.

# Error Message

```text
TypeError: output tensor must have the same type as input tensor
```

traceback의 핵심 경로는 다음과 같다.

```text
deepspeed/runtime/zero/stage3.py _post_step
self.persistent_parameters[0].all_gather(self.persistent_parameters)
deepspeed/runtime/zero/partition_parameters.py _allgather_params_coalesced
torch.distributed.distributed_c10d.py all_gather_into_tensor
```

# Cause

## 확인된 사실

- 서버의 DeepSpeed 버전은 `0.19.2`이다.
- PEFT 버전은 `0.18.1`이다.
- 30B/72B 실패 시 cgroup `oom_kill` 증가는 관측되지 않았다.
- 설치된 DeepSpeed의 `_allgather_params_coalesced` 구현은 all-gather output buffer dtype을 `param_list[0].ds_tensor.dtype`으로 만든다.
- DeepSpeed upstream PR #8073은 이 구현이 mixed dtype persistent parameters에서 깨진다고 설명하며, parameter별 dtype으로 buffer를 만들도록 수정했다.

## 추정

bf16 base model parameter와 PEFT LoRA adapter parameter가 ZeRO-3 persistent parameter group 안에서 mixed dtype이 되었고, DeepSpeed 0.19.2가 첫 parameter dtype으로 모든 output buffer를 만들면서 `all_gather_into_tensor`의 dtype 검사를 통과하지 못한 것으로 보인다.

# Solution

즉시 의존성을 바꾸지 않고, ZeRO-2 diagnostic smoke run을 추가한다.

- `configs/deepspeed/ds_z2_bf16_b200.json`
- `configs/llamafactory/b200/qwen3_coder_30b_lora_smoke_z2.yaml`
- `configs/llamafactory/b200/qwen2_72b_lora_smoke_z2.yaml`
- `scripts/run_smoke_qwen3_coder_30b_z2.sh`
- `scripts/run_smoke_qwen2_72b_z2.sh`

실행 순서:

```bash
bash scripts/run_smoke_qwen3_coder_30b_z2.sh
bash scripts/run_smoke_qwen2_72b_z2.sh
```

판정 기준:

- ZeRO-2 30B가 통과하면 dataset, W&B, LLaMA-Factory, PEFT 기본 경로는 정상으로 본다.
- ZeRO-2 72B도 통과하면 30B/72B의 기존 실패 원인은 ZeRO-3 dtype bug 가능성이 매우 높다.
- ZeRO-2에서도 같은 dtype 오류가 나면 LLaMA-Factory/PEFT adapter dtype 생성 경로를 추가 조사한다.

2026-07-03 실행 결과, 30B와 72B ZeRO-2 smoke run이 모두 성공했다. 두 run 모두 첫 optimizer step을 통과했고, W&B run과 LoRA adapter/checkpoint를 생성했으며, 실행 중 cgroup `oom_kill` 증가는 없었다. 따라서 기존 30B/72B 실패는 ZeRO-3 optimizer/all-gather 경로에 강하게 격리된다.

| Model | Result | cgroup current max | oom_kill | Adapter output |
| --- | --- | --- | --- | --- |
| Qwen3-Coder-30B-A3B | Passed | 280.25 GiB | 6 -> 6 | `model/adapters/qwen3-coder-30b/lora/smoke-z2` |
| Qwen2-72B | Passed | 668.11 GiB | 6 -> 6 | `model/adapters/qwen2-72b/lora/smoke-z2` |

# Prevention

ZeRO-3를 다시 사용할 때는 다음 후보 중 하나를 실험한다.

- DeepSpeed upstream PR #8073 패치 적용
- DeepSpeed `0.19.1` downgrade
- DeepSpeed master 또는 수정 릴리스 upgrade
- LLaMA-Factory/PEFT adapter dtype 우회

# Related Concepts

- [LLaMA-Factory Qwen3-Coder 480B FP8 SIGKILL Investigation](llamafactory-qwen3-coder-480b-fp8-oom-kill.md)
- [B200 Server Fine-Tuning](../projects/Fine_Tuned/b200/B200_server.md)
- [LLaMA-Factory + W&B Fine-Tuning Integration](../projects/Fine_Tuned/training/llamafactory_wandb_finetuning.md)
- [DeepSpeed ZeRO-3 Dtype Mismatch Troubleshooting](../projects/Fine_Tuned/repos/AegisLM/docs/DEEPSPEED_ZERO3_DTYPE_MISMATCH.md)

# Citations

- DeepSpeed issue #8072: https://github.com/deepspeedai/DeepSpeed/issues/8072
- DeepSpeed PR #8073: https://github.com/deepspeedai/DeepSpeed/pull/8073
- Hugging Face forum traceback: https://discuss.huggingface.co/t/output-tensor-must-have-the-same-type-as-input-tensor/90729
- ms-swift similar issue: https://github.com/modelscope/ms-swift/issues/3235
