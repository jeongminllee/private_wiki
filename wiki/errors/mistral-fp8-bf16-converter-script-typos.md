---
type: Error Note
title: Mistral FP8 to BF16 변환 스크립트 오타와 사후 실패 위험
description: 공식 Mistral FP8 descale 스크립트를 수동 작성하면서 집합 변수, config 검증과 params 저장 오타로 장시간 변환이 사후 실패할 뻔한 문제
tags: [error, mistral, fp8, bf16, python, checkpoint]
timestamp: 2026-08-11
status: solved
---

# Situation

공식 `Mistral-Small-4-119B-2603` FP8 checkpoint를 local BF16 checkpoint로
변환하기 위해 Mistral의 공개 descale 식을 구현했다. 119B 모델 변환은 100GB가 넘는
원본을 읽고 약 239GB를 저장하므로, 뒤쪽 코드의 오타도 몇 시간 작업을 낭비하게
만들 수 있다.

# Error Message

초기 실행에서는 `uv`의 experimental option 경고만 보였고, 변환기 출력이 즉시
나타나지 않았다. 첨부된 실제 script를 감사한 결과 다음 결함을 발견했다.

```python
unused_scale_keys = scale_key - used_scale_keys
for key in scale_key | activation_scale_keys:
json.dumps(config, ...)  # params.json 저장 위치
if "quantizaiton_config" in config:
```

`scale_key`는 loop 안의 단일 문자열 또는 `None`이고 `scale_keys`는 전체 집합이다.
따라서 변환 후 검증 단계에서 type error 또는 잘못된 key 제거가 발생할 수 있었다.

# Cause

- 긴 script를 수동으로 다시 입력하면서 복수형 `scale_keys`가 단수형으로 바뀌었다.
- `params.json` rewrite에서 수정된 `params` 대신 `config`를 직렬화했다.
- `quantization_config` 검사 문자열에 오타가 있어 잔여 config를 놓칠 수 있었다.
- `parse_args`, verify log label에도 비기능적 오타가 있었다.
- Python 문법 검사는 이런 이름·논리 오류를 탐지하지 못한다.

# Solution

다음처럼 전체 inverse-scale 집합을 사용하고 올바른 객체와 key를 검증하도록 수정했다.

```python
unused_scale_keys = scale_keys - used_scale_keys

for key in scale_keys | activation_scale_keys:
    del state_dict[key]

params_path.write_text(json.dumps(params, ...))

if "quantization_config" in config:
    raise RuntimeError(...)
```

수정 후 `py_compile`, `--help`, 실제 변환과 독립 safetensors header 검사를 수행했다.
최종 결과는 BF16 tensor 765개, shard 35개, 누락 shard·FP8·scale tensor 각 0개로
PASS했다.

# Prevention

- 대형 변환 전 `py_compile`과 `--help`를 실행한다.
- 119B 전체 실행 전에 작은 synthetic state dict로 scale 사용·제거 unit test를 만든다.
- output은 `.incomplete`에 저장하고 모든 검증 뒤 final path로 rename한다.
- 모든 scale key가 정확히 한 번 사용됐는지 집합 차이로 검사한다.
- 저장된 shard header를 다시 열어 FP8·scale key가 0개인지 독립 확인한다.
- 수동 재입력보다 version-controlled script와 diff review를 사용한다.

# Related Concepts

- [Mistral 공식 FP8 체크포인트의 로컬 BF16 변환 이해](../projects/Fine_Tuned/fundamentals/mistral_fp8_to_bf16_checkpoint_conversion.md)
- [Mistral F5-X 첫 파인튜닝 실습 워크북](../projects/Fine_Tuned/training/mistral_f5x_first_finetuning_workbook_20260809.md)

# Citations

- [Mistral 공식 FP8 descale 예제](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/blob/3b76d234c932e78dc989731bfc4c3b12c0a87918/README.md)

