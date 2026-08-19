---
type: Error Note
title: Mistral PixtralProcessor TorchVision 누락
description: Mistral Small 4의 local AutoProcessor 검사가 TorchVision 누락으로 실패한 원인과 PyTorch CUDA build를 맞춘 해결 기록
tags: [error, mistral, pixtral, torchvision, pytorch, cuda]
timestamp: 2026-08-11
status: solved
---

# Situation

FP8에서 변환한 local BF16 checkpoint의 config, tokenizer와 chat template를 weight
load 없이 검사했다. 데이터는 text-only이지만 모델은 vision encoder를 포함한
multimodal architecture다.

# Error Message

```text
ImportError:
PixtralProcessor requires the Torchvision library but it was not found in your environment.
```

# Cause

`AutoProcessor`는 text tokenizer만 읽는 것이 아니라 `PixtralProcessor`의 image
전처리 component도 구성한다. 따라서 text-only SFT를 계획해도 processor import
시점에는 TorchVision이 필요하다.

TorchVision은 PyTorch와 함께 동작하는 compiled operator를 포함하므로 임의 버전을
설치하면 안 된다. 당시 runtime은 `torch==2.12.1+cu130`이었고 이에 대응하는 공식
조합은 `torchvision==0.27.1+cu130`이다.

# Solution

`torchvision==0.27.1`을 project dependency에 추가하고 `torch`와 같은 explicit
PyTorch CUDA 13.0 index에서 받도록 source를 고정했다.

```toml
[tool.uv.sources]
torch = { index = "pytorch-cu130" }
torchvision = { index = "pytorch-cu130" }

[[tool.uv.index]]
name = "pytorch-cu130"
url = "https://download.pytorch.org/whl/cu130"
explicit = true
```

검사 결과:

```text
torch: 2.12.1+cu130
torchvision: 0.27.1+cu130
torch CUDA: 13.0
CUDA available: True
GPU count: 2
```

이후 `Mistral3Config`, `PixtralProcessor`, vocabulary 131,072와
`reasoning_effort=none` chat template를 local-only로 정상 로드했다.

# Prevention

- multimodal model은 text-only 학습이어도 processor의 vision dependency를 검사한다.
- PyTorch ecosystem package는 torch version과 CUDA local version suffix를 함께 맞춘다.
- `torch`와 `torchvision`을 같은 explicit uv index에 고정한다.
- 설치 직후 package version, `torch.version.cuda`, CUDA availability와 GPU 수를 확인한다.
- full weight load 전에 `AutoConfig`·`AutoProcessor` local-only smoke test를 수행한다.

# Related Concepts

- [Mistral 공식 FP8 체크포인트의 로컬 BF16 변환 이해](../projects/Fine_Tuned/fundamentals/mistral_fp8_to_bf16_checkpoint_conversion.md)
- [AegisLM Training Libraries](../projects/Fine_Tuned/libraries/aegislm_training_libraries.md)

# Citations

- [PyTorch 공식 과거 버전 조합](https://pytorch.org/get-started/previous-versions/)
- [uv의 PyTorch index 구성](https://docs.astral.sh/uv/guides/integration/pytorch/)

