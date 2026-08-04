---
type: Concept
title: "Shallowcopy vs Deepcopy"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2024-06-28)"
tags: [cs, chatgpt-export]
timestamp: 2024-06-28
status: active
---

# Shallowcopy vs Deepcopy

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-06-28

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
shallowcopy와 deepcopy의 차이점을 설명해줘

### 💡 답변 (Assistant)
`shallowcopy`와 `deepcopy`는 모두 객체를 복사하는 방법이지만, 복사의 깊이에 따라 다르게 동작합니다. 이 둘의 차이점을 설명하겠습니다.

### `shallowcopy`
- **개념**: 얕은 복사는 객체의 최상위 레벨만 복사합니다. 즉, 원본 객체의 복사본을 만들지만, 객체가 참조하는 내부의 다른 객체들까지는 복사하지 않습니다.
- **구현**: Python의 `copy` 모듈을 사용하여 `shallowcopy`를 수행할 수 있습니다.
- **예시**:
  ```python
  import copy

  original = [1, 2, [3, 4]]
  shallow_copy = copy.copy(original)
  
  shallow_copy[0] = 10
  shallow_copy[2][0] = 30
  
  print("Original:", original)  # Output: [1, 2, [30, 4]]
  print("Shallow Copy:", shallow_copy)  # Output: [10, 2, [30, 4]]
  ```
  여기서, `shallow_copy`에서 최상위 레벨의 요소를 변경하면 원본에는 영향을 미치지 않지만, 내부의 리스트를 변경하면 원본 객체에도 영향을 미칩니다. 이는 내부 리스트가 원본과 복사본 모두에서 동일한 참조를 가리키기 때문입니다.

### `deepcopy`
- **개념**: 깊은 복사는 객체와 객체가 참조하는 모든 객체를 재귀적으로 복사합니다. 즉, 원본 객체의 완전한 복사본을 만듭니다.
- **구현**: Python의 `copy` 모듈을 사용하여 `deepcopy`를 수행할 수 있습니다.
- **예시**:
  ```python
  import copy

  original = [1, 2, [3, 4]]
  deep_copy = copy.deepcopy(original)
  
  deep_copy[0] = 10
  deep_copy[2][0] = 30
  
  print("Original:", original)  # Output: [1, 2, [3, 4]]
  print("Deep Copy:", deep_copy)  # Output: [10, 2, [30, 4]]
  ```
  여기서, `deep_copy`에서 최상위 레벨의 요소뿐만 아니라 내부 리스트의 요소를 변경해도 원본 객체는 영향을 받지 않습니다. 이는 내부 리스트까지 모두 새로운 객체로 복사되었기 때문입니다.

### 요약
- **shallowcopy**: 객체의 최상위 레벨만 복사하고, 내부의 참조는 원본 객체와 공유합니다.
- **deepcopy**: 객체와 객체가 참조하는 모든 객체를 재귀적으로 복사하여 완전한 복사본을 만듭니다.

이 두 가지 복사 방법은 객체를 복사할 때 어떤 방식이 더 적합한지에 따라 선택적으로 사용됩니다. 객체가 참조하는 데이터가 변경되어도 원본 객체에 영향을 미치지 않게 하려면 `deepcopy`를 사용하는 것이 좋습니다. 반면, 메모리 사용량을 줄이고 싶고, 내부 객체가 변경될 필요가 없는 경우 `shallowcopy`를 사용할 수 있습니다.

---
