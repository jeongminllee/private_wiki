---
type: Error Note
title: Mistral 전수 Preflight의 잘못된 Empty Target 판정
description: Transformers 5.x Mistral chat template 반환 객체에서 input_ids를 꺼내지 않아 정상 assistant target을 빈 값으로 오판한 문제
tags: [error, mistral, transformers, tokenizer, preflight]
timestamp: 2026-08-18
status: solved
---

# Situation

Mistral Small 4 119B의 train 10,000건과 validation 1,000건을 실제 local tokenizer로
검사하는 `scripts/preflight_dataset.py`를 실행했다. 앞선 sample 검사는 train 첫 행의
assistant target을 10 token으로 확인했지만, 전수 검사는 같은 첫 행을 빈 target으로
판정했다.

# Error Message

```text
[load] local Mistral processor
[start] train
RuntimeError: train:1: empty target
```

# Cause

`tokenizer.apply_chat_template(..., tokenize=True)`의 반환값을 다음 helper가 처리했다.

```python
def to_input_ids(value: Any) -> list[int]:
    if isinstance(value, dict):
        value = value["input_ids"]
    ...
    return list(value)
```

Transformers 5.x의 Mistral tokenizer는 tokenized chat을 `.input_ids` attribute를 가진
객체로 반환할 수 있다. 이 객체가 일반 `dict` 검사에 걸리지 않으면 helper는 token ID가
아닌 객체 자체를 `list()`로 변환한다. 그 결과 `full_ids`와 `prompt_ids`가 모두 빈
리스트가 되어 prefix 검사는 우연히 통과하고, 뒤의 `empty target` 검사가 실패했다.

따라서 이 오류는 데이터의 assistant content가 빈 것이 아니라 반환형 정규화 오류였다.
앞선 sample의 content 29자·target 10 token 관찰과도 일치한다.

# Solution

일반 `dict` 처리보다 먼저 `.input_ids`를 명시적으로 꺼내고, 최종 결과가 정수 token ID
리스트인지 검증했다.

```python
def to_input_ids(value: Any) -> list[int]:
    if hasattr(value, "input_ids"):
        value = value.input_ids
    elif isinstance(value, dict):
        value = value["input_ids"]

    if hasattr(value, "tolist"):
        value = value.tolist()

    if not isinstance(value, list):
        raise TypeError(
            f"Unsupported tokenized output type: {type(value).__name__}"
        )

    if value and isinstance(value[0], list):
        value = value[0]

    if not all(isinstance(token_id, int) for token_id in value):
        raise TypeError("Tokenized output contains non-integer token IDs")

    return cast(list[int], value)
```

수정 후 train 10,000건과 validation 1,000건이 모두 통과했다. 고유 ID는 11,000개,
2,048 token 초과와 THINK marker는 모두 0건이었다. train 최대 길이는 1,505 token,
validation 최대 길이는 1,497 token이었다.

# Prevention

- tokenizer API의 반환형을 단순 `list`나 `dict` 하나로 가정하지 않는다.
- `input_ids` attribute, mapping, tensor/list 변환을 명시적으로 정규화한다.
- 빈 리스트가 들어오면 prefix equality가 참이 되는 점을 고려해, 경계 검사 전에
  `full_ids`와 `prompt_ids` 자체가 비어 있지 않은지도 검증한다.
- sample gate와 전수 gate가 같은 레코드에서 충돌하면 데이터를 수정하기 전에 검사
  코드의 API boundary를 먼저 확인한다.

# Related Concepts

- [Mistral 공식 FP8 체크포인트의 로컬 BF16 변환 이해](../projects/Fine_Tuned/fundamentals/mistral_fp8_to_bf16_checkpoint_conversion.md)
- [Mistral F5-X 첫 파인튜닝 실습 워크북](../projects/Fine_Tuned/training/mistral_f5x_first_finetuning_workbook_20260809.md)
- [Mistral PixtralProcessor TorchVision 누락](mistral-pixtralprocessor-torchvision-missing.md)

# Citations

- [Hugging Face Transformers Mistral tokenizer tests](https://github.com/huggingface/transformers/blob/main/tests/test_tokenization_mistral_common.py)
- [Hugging Face chat templates](https://huggingface.co/docs/transformers/v5.0.0/chat_templating)
