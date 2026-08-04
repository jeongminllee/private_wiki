---
type: Error Note
title: "nonlocal vs global 차이"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2025-04-12)"
tags: [errors, chatgpt-export]
timestamp: 2025-04-12
status: active
---

# nonlocal vs global 차이

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-04-12

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
파이썬에서 nonlocal과 global 이 두 메소드가 헷갈려. 각 메소드마다 특징을 알려주고 차이점에 대해서 설명해줘

### 💡 답변 (Assistant)
좋은 질문이야! `nonlocal`과 `global`은 **함수 내부에서 변수의 범위(scope)**를 제어할 때 사용하는 키워드야. 자주 헷갈릴 수 있는데, 아래에 정리해줄게.

---

### 🔹 `global` 키워드
`global`은 **전역 변수(global variable)**를 함수 안에서 수정하고 싶을 때 사용해.

#### ✅ 특징
- 함수 내부에서 `global`을 선언하면, 그 변수는 **전역 공간의 변수**를 가리켜.
- 함수 내부에서 새로 값을 할당해도, 전역 변수 자체가 변경돼.

#### 📌 예제:
```python
x = 10

def change_global():
    global x
    x = 20

change_global()
print(x)  # 출력: 20
```

---

### 🔹 `nonlocal` 키워드
`nonlocal`은 **바로 바깥쪽(상위) 함수의 지역 변수**를 수정할 때 사용해.

#### ✅ 특징
- 중첩 함수(nested function)에서 **바깥 함수의 지역 변수**를 참조하거나 수정하고 싶을 때 사용.
- 전역 변수가 아니라 **로컬(지역) 변수**를 대상으로 함.

#### 📌 예제:
```python
def outer():
    x = 10
    def inner():
        nonlocal x
        x = 20
    inner()
    print(x)

outer()  # 출력: 20
```

---

### 🔄 `global` vs `nonlocal` 차이점 정리

| 항목         | `global`                       | `nonlocal`                            |
|--------------|----------------------------------|----------------------------------------|
| 작용 대상    | 전역 변수 (Global Scope)       | 바깥 함수의 지역 변수 (Enclosing Scope) |
| 사용 위치    | 함수 내부                      | 중첩 함수 내부 (nested function)       |
| 사용 목적    | 전역 변수 수정                 | 상위 함수의 지역 변수 수정            |
| 없는 변수에 사용 시 | 새 전역 변수 생성 가능          | `SyntaxError` 발생 (존재해야 함)         |

---

### 💡 요약 한 줄
- `global`은 **전역 변수를 수정할 때**,
- `nonlocal`은 **바깥 함수의 지역 변수를 수정할 때** 사용해.

---

필요하다면 그림이나 예제 더 추가해줄게! 어떤 부분이 더 헷갈리는지도 말해줘 :)

---
