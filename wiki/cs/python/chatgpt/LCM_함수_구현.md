---
type: Concept
title: "LCM 함수 구현"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2025-02-06)"
tags: [cs, chatgpt-export]
timestamp: 2025-02-06
status: active
---

# LCM 함수 구현

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-02-06

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
최소 공배수를 구하는 함수를 파이썬 코드로 구현해줘

### 💡 답변 (Assistant)
파이썬에서 최소 공배수(LCM, Least Common Multiple)를 구하는 함수는 최대 공약수(GCD, Greatest Common Divisor)를 활용하면 쉽게 구현할 수 있습니다. `math` 모듈의 `gcd` 함수를 사용하면 간결하게 구현할 수 있습니다.  

```python
import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

# 사용 예시
print(lcm(12, 18))  # 출력: 36
```

이 함수는 두 수의 곱을 최대 공약수로 나누어 최소 공배수를 구합니다.  
여러 개의 숫자에 대해 최소 공배수를 구하려면 `functools.reduce`를 사용할 수 있습니다.

```python
import math
from functools import reduce

def lcm_multiple(numbers):
    return reduce(lcm, numbers)

# 사용 예시
print(lcm_multiple([12, 18, 24]))  # 출력: 72
```

필요한 경우 응용해서 사용할 수 있도록 작성했어요. 원하는 방식이 있으면 말해줘! 😊

---

### ❓ 질문 (User)
최대 공약수를 구하는 함수를 구현해줘

### 💡 답변 (Assistant)
최대 공약수(GCD, Greatest Common Divisor)를 구하는 함수는 유클리드 호제법을 이용하면 효율적으로 구현할 수 있습니다. 파이썬에서는 `math.gcd` 함수를 사용할 수도 있지만, 직접 구현하려면 다음과 같이 작성할 수 있습니다.

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 사용 예시
print(gcd(48, 18))  # 출력: 6
```

### 여러 개의 숫자에 대한 최대 공약수 구하기
여러 개의 숫자에 대해 최대 공약수를 구하려면 `functools.reduce`를 활용할 수 있습니다.

```python
from functools import reduce

def gcd_multiple(numbers):
    return reduce(gcd, numbers)

# 사용 예시
print(gcd_multiple([48, 18, 30]))  # 출력: 6
```

필요한 방식이 있다면 말해줘! 😊

---
