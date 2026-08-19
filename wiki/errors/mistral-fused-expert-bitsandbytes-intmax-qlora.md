---
type: Error Note
title: Mistral Fused Expert가 bitsandbytes INT_MAX를 초과해 QLoRA 실패
description: Mistral Small 4의 gate_up_proj 단일 tensor가 2^31개 원소라 bitsandbytes 4-bit CUDA kernel의 32-bit 크기 한계를 넘은 사건
tags: [error, mistral, qlora, bitsandbytes, moe, cuda]
timestamp: 2026-08-18
status: solved
---

# Situation

local BF16으로 변환한 Mistral Small 4 119B를 Axolotl 0.17.0과
bitsandbytes 0.49.1로 QLoRA 1-step 학습하려 했다. 두 B200은 유휴 상태였고 CUDA
13.0, 작은 NF4 quantization과 dataset preflight는 모두 정상인 상태였다.

QLoRA 설정은 `load_in_4bit: true`, `quantize_moe_experts: true`를 사용하고 fused MoE
parameter인 `mlp.experts.gate_up_proj`와 `mlp.experts.down_proj`를 LoRA target으로
지정했다.

# Error Message

```text
Error invalid argument at line 54 in file /src/csrc/ops.cu
torch.distributed.elastic.multiprocessing.errors.ChildFailedError
```

rank 0의 CUDA C++ kernel이 먼저 종료된 뒤 torchrun이 다른 rank에 SIGTERM을 보내서
정리했다. 따라서 `ChildFailedError`는 최초 원인이 아니라 분산 launcher의 후속 요약이다.

# Cause

safetensors header에서 첫 번째 layer의 fused expert parameter를 읽은 결과는 다음과
같았다.

```text
shape: [128, 4096, 4096]
numel: 2147483648
INT_MAX: 2147483647
exceeds: True
```

수식으로는 다음과 같다.

```text
128 experts × (2 × 2,048 MoE intermediate) × 4,096 hidden
= 2,147,483,648
= 2^31
= INT_MAX + 1
```

bitsandbytes 0.49.1의 blockwise CUDA quantization interface는 전체 원소 수 `n`을
32-bit C++ `int`로 전달한다. `gate_up_proj`는 이 범위를 정확히 한 원소 초과하므로
단일 fused tensor를 NF4로 양자화하는 kernel launch가 invalid argument로 실패한다.

다음 작은 tensor 검사가 통과해 B200·CUDA 13.0·bitsandbytes 조합 자체의 일반적인
NF4 지원 문제는 배제했다.

```text
input: torch.Size([1024, 1024]) torch.bfloat16
quantized: torch.Size([524288, 1]) torch.uint8
restored: torch.Size([1024, 1024]) torch.bfloat16
finite: True
BITSANDBYTES SMALL NF4 PASS
```

# Solution

G1 QLoRA run은 upstream tensor-size 제한으로 `BLOCK` 처리한다. 실패한 run directory와
GPU monitor·train log는 재사용하거나 삭제하지 않고 증거로 보존한다.

임의로 tensor를 잘라 quantization state와 PEFT parameter layout을 다시 조립하는 local
patch는 학습 의미와 save/reload 호환성을 함께 검증해야 하므로 현재 입문 실험 범위를
넘는다. 공식 BF16 checkpoint를 이미 준비했고 B200 두 장이 있으므로 승인된 대안인
BF16 LoRA + FSDP2 1-step으로 전환한다.

이 판정은 QLoRA 방법 전체가 불가능하다는 뜻이 아니다. Axolotl 또는 bitsandbytes가
거대 fused parameter를 chunk 단위로 안전하게 처리하고 adapter save/reload까지 지원하는
pin이 생기면 새 Work Order에서 다시 검사할 수 있다.

# Prevention

- fused MoE parameter는 dtype과 이름뿐 아니라 `shape`와 `numel`도 header에서 검사한다.
- `numel > INT_MAX`이면 bitsandbytes 단일-tensor quantization을 실제 model load 전에
  차단한다.
- 작은 kernel probe로 GPU/runtime 전체 문제와 model-specific shape 문제를 분리한다.
- torchrun 마지막 `ChildFailedError`보다 최초 CUDA·Python 오류를 먼저 찾는다.
- 실패한 run ID와 output directory를 다시 사용하지 않는다.

# Related Concepts

- [Mistral 공식 FP8 체크포인트의 로컬 BF16 변환 이해](../projects/Fine_Tuned/fundamentals/mistral_fp8_to_bf16_checkpoint_conversion.md)
- [Mistral F5-X 첫 파인튜닝 실습 워크북](../projects/Fine_Tuned/training/mistral_f5x_first_finetuning_workbook_20260809.md)

# Citations

- [bitsandbytes: Support quantizing tensors when numel() > INT_MAX](https://github.com/bitsandbytes-foundation/bitsandbytes/issues/1785)
- [bitsandbytes 0.49.1 CUDA ops](https://github.com/bitsandbytes-foundation/bitsandbytes/blob/0.49.1/csrc/ops.cu)
- [Axolotl MoE Expert Quantization](https://docs.axolotl.ai/docs/expert_quantization.html)
