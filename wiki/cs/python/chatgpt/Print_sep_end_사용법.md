---
type: Concept
title: "Print sep end 사용법"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2024-07-20)"
tags: [cs, chatgpt-export]
timestamp: 2024-07-20
status: active
---

# Print sep end 사용법

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-07-20

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
파이썬에서 print() 할 때 sep, end 사용법 알려줘

### 💡 답변 (Assistant)
파이썬의 `print()` 함수는 기본적으로 콘솔에 텍스트를 출력하는 데 사용됩니다. 이 함수는 `sep`와 `end`라는 두 가지 중요한 매개변수를 제공하여 출력 형식을 제어할 수 있습니다.

### `sep` 매개변수
- `sep`는 여러 항목을 출력할 때 항목 사이에 삽입할 문자열을 지정합니다.
- 기본값은 공백 문자열 (`' '`)입니다.
- 예를 들어, 콤마를 구분자로 사용하고 싶다면 `sep`에 콤마를 지정할 수 있습니다.

```python
print('Hello', 'World', 'Python', sep=', ')
```
출력:
```
Hello, World, Python
```

### `end` 매개변수
- `end`는 출력이 끝난 후에 삽입할 문자열을 지정합니다.
- 기본값은 새 줄 문자 (`'\n'`)입니다.
- 예를 들어, 출력 후에 줄을 바꾸지 않고 공백을 추가하고 싶다면 `end`에 공백을 지정할 수 있습니다.

```python
print('Hello', end=' ')
print('World')
```
출력:
```
Hello World
```

### 예제들

#### 1. 기본 출력
```python
print('Hello', 'World')
```
출력:
```
Hello World
```

#### 2. `sep` 사용 예시
```python
print('Apple', 'Banana', 'Cherry', sep=' - ')
```
출력:
```
Apple - Banana - Cherry
```

#### 3. `end` 사용 예시
```python
print('Hello', end=' ')
print('World')
```
출력:
```
Hello World
```

#### 4. `sep`와 `end`를 함께 사용
```python
print('One', 'Two', 'Three', sep=' | ', end='.\n')
```
출력:
```
One | Two | Three.
```

이와 같이 `sep`와 `end`를 사용하여 `print()` 함수의 출력을 원하는 형식으로 쉽게 조정할 수 있습니다.

---

### ❓ 질문 (User)
python 에서 dict 함수 중 setdefault 와 get 의 차이점이 뭐야?

### 💡 답변 (Assistant)
파이썬의 사전(dict) 자료형에서 `setdefault`와 `get` 메서드는 모두 키를 기반으로 값을 검색하는 기능을 제공합니다. 그러나 이 두 메서드는 몇 가지 중요한 차이점이 있습니다.

### `get` 메서드
- `get` 메서드는 사전에서 주어진 키에 대응하는 값을 반환합니다.
- 만약 키가 사전에 존재하지 않으면, 기본값(default)을 반환합니다. 기본값을 지정하지 않으면 `None`을 반환합니다.
- 사전의 내용을 변경하지 않습니다.

#### 예제
```python
# 사전 초기화
my_dict = {'a': 1, 'b': 2}

# 키 'a'의 값 반환
value_a = my_dict.get('a')  # 결과: 1

# 존재하지 않는 키 'c'의 값 반환 (기본값 사용)
value_c = my_dict.get('c', 3)  # 결과: 3

# 기본값을 지정하지 않으면 None 반환
value_d = my_dict.get('d')  # 결과: None
```

### `setdefault` 메서드
- `setdefault` 메서드는 사전에서 주어진 키에 대응하는 값을 반환합니다.
- 만약 키가 사전에 존재하지 않으면, 주어진 키와 기본값(default)을 사전에 추가하고 그 기본값을 반환합니다.
- 기본값을 지정하지 않으면 기본값은 `None`입니다.
- 사전의 내용을 변경할 수 있습니다.

#### 예제
```python
# 사전 초기화
my_dict = {'a': 1, 'b': 2}

# 키 'a'의 값 반환 (사전 변경 없음)
value_a = my_dict.setdefault('a')  # 결과: 1

# 존재하지 않는 키 'c'의 값 반환 (사전에 추가됨)
value_c = my_dict.setdefault('c', 3)  # 결과: 3

# 기본값을 지정하지 않으면 None이 추가됨
value_d = my_dict.setdefault('d')  # 결과: None

print(my_dict)  # 결과: {'a': 1, 'b': 2, 'c': 3, 'd': None}
```

### 주요 차이점 요약
1. **사전 변경 여부**:
   - `get`: 사전의 내용을 변경하지 않습니다.
   - `setdefault`: 키가 사전에 존재하지 않으면, 해당 키와 기본값을 사전에 추가합니다.

2. **기본값 처리**:
   - `get`: 키가 존재하지 않으면 지정된 기본값을 반환하며, 기본값을 지정하지 않으면 `None`을 반환합니다.
   - `setdefault`: 키가 존재하지 않으면 지정된 기본값을 사전에 추가하고 반환하며, 기본값을 지정하지 않으면 `None`을 사전에 추가하고 반환합니다.

이러한 차이로 인해, `get`은 단순히 값을 조회할 때 유용하고, `setdefault`는 키가 존재하지 않을 경우 기본값으로 초기화하고 추가하는 데 유용합니다.

---
