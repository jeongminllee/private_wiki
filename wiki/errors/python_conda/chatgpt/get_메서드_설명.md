---
type: Error Note
title: "get 메서드 설명"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2025-04-05)"
tags: [errors, chatgpt-export]
timestamp: 2025-04-05
status: active
---

# get 메서드 설명

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-04-05

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
`adj_list.get(node, [])`는 파이썬 딕셔너리의 `get` 메서드를 이용해 `node`라는 키에 대응하는 값을 가져오되, 만약 `node` 키가 딕셔너리에 없으면 기본값으로 빈 리스트(`[]`)를 반환하도록 하는 코드입니다.

### 딕셔너리의 `get` 메서드란?
- **역할:**  
  딕셔너리에서 특정 키에 대응하는 값을 조회할 때, 해당 키가 존재하면 그 값을 반환하고, 존재하지 않으면 기본값(default)을 반환합니다.
  
- **기본 구문:**  
  ```python
  value = dictionary.get(key, default_value)
  ```
  여기서:
  - `key`: 조회하려는 키
  - `default_value`: 해당 키가 없을 경우 반환할 값

- **장점:**  
  - **예외 처리:** 키가 없을 때 `KeyError`를 발생시키지 않고 안전하게 값을 가져올 수 있습니다.
  - **유연성:** 기본값을 지정할 수 있어, 키가 없을 때 원하는 타입이나 초기값을 쉽게 설정할 수 있습니다.

### 예시
```python
# 일반 딕셔너리 사용 예시
person = {"name": "Alice", "age": 25}

# "name" 키가 존재하므로 "Alice" 반환
print(person.get("name", "Unknown"))  # 출력: Alice

# "address" 키가 없으므로 기본값 "Unknown" 반환
print(person.get("address", "Unknown"))  # 출력: Unknown
```

### defaultdict와의 차이
`defaultdict(list)`는 만약 키가 존재하지 않으면 자동으로 빈 리스트(`list()`)를 생성하여 딕셔너리에 저장합니다. 그러나 `get` 메서드를 사용하면 기본값을 반환할 뿐, 딕셔너리에 해당 키-값 쌍이 추가되지는 않습니다.

예를 들어:
```python
from collections import defaultdict

adj_list = defaultdict(list)

# 인덱스 연산은 키가 없으면 새 항목을 생성
print(adj_list["node1"])  # 출력: []

# get 메서드는 기본값을 반환하지만, 실제로 딕셔너리에 추가하지 않음
print(adj_list.get("node2", []))  # 출력: []
print("node2" in adj_list)  # 출력: False
```

이처럼 `get(node, [])`는 `node` 키가 없을 경우 안전하게 빈 리스트를 반환하여 이후 연산에서 에러 없이 활용할 수 있도록 도와줍니다.

---

### ❓ 질문 (User)
```
adj_list = defaultdict(list)
adj_list.get(node, []) 
```
이때 get(node, []) 가 의미하는 것을 알려줘. 
그리고 딕셔너리에서 get 메서드가 하는 역할과 기본적인 활용법을 알려줘
