---
type: Concept
title: "pow 함수 구현하기"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-11-21)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-11-21
status: active
---

# pow 함수 구현하기

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-11-21

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
Implement pow(x, n), which calculates x raised to the power n (i.e., xn).

무슨 말일까

### 💡 답변 (Assistant)
문장 그대로 해석하면:

> `pow(x, n)` 함수를 직접 구현해라.  
> 이 함수는 **x를 n번 곱한 값**, 즉 \(x^n\) 을 계산해서 반환해야 한다.

예를 들어
- `pow(2, 3)` → \(2^3 = 8\)
- `pow(5, 0)` → \(5^0 = 1\) (0제곱은 항상 1)
- `pow(2, -2)` → \(2^{-2} = 1 / 2^2 = 1/4\)

보통 이 문제는 **그냥 n번 곱하는 방식(O(n)) 말고 더 빠르게(O(log n))** 하라는 의도가 있어요.  
그래서 자주 쓰는 풀이가 **빠른 거듭제곱(Exponentiation by Squaring)** 입니다.

핵심 아이디어:
- \(x^n\)에서 n이 짝수면  
  \(x^n = (x^{n/2})^2\)
- n이 홀수면  
  \(x^n = x \cdot (x^{\lfloor n/2 \rfloor})^2\)

이걸 재귀나 반복으로 하면 곱셈 횟수가 확 줄어요.

추가로 신경쓸 것:
1. `n == 0`이면 무조건 1
2. `n < 0`이면  
   \(x^n = 1 / x^{-n}\) 로 바꿔서 계산

즉, 문제의 요지는  
**“내장 pow 쓰지 말고, x^n을 효율적으로 계산하는 함수를 만들어봐라”**  
라고 이해하면 됩니다.

---

### ❓ 질문 (User)
그니까 파이썬으로 구현하면
```
class Solution :
    def myPow(x: float, n: int) :
        return x ** n 
```
이런 식으로가 아니라 쭉 풀어서 제곱을 처음 배우는 학생에게 설명하듯 구현하라는거지?

### 💡 답변 (Assistant)
맞아! 그 의도가 거의 확실해. 😊

이 문제는 “파이썬의 `**`(거듭제곱 연산자)나 `pow()`를 쓰면 한 줄이잖아?”  
→ **그걸 쓰지 말고, 거듭제곱이 어떻게 계산되는지 원리대로 직접 구현해봐**  
라는 뜻이야.

특히 코딩테스트/LeetCode의 `Pow(x, n)` 문제는 보통:

- 단순히 `x`를 `n`번 곱하면 O(n)이라 느림
- **더 빠른 방법(O(log n))**을 쓰는지 보려는 문제

그래서 “제곱을 처음 배우는 학생에게 설명하듯” **원리를 쭉 풀어서** 구현하는 게 정답 방향이야.

---

## 1) 아주 쉬운 버전 (진짜 처음 배우는 방식, O(n))
이건 원리 설명용으로 좋아:

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        # 1) 0제곱은 항상 1
        if n == 0:
            return 1.0
        
        # 2) 음수 제곱이면 양수로 바꾸고 마지막에 뒤집기
        if n < 0:
            x = 1 / x
            n = -n
        
        result = 1.0
        # 3) x를 n번 곱한다
        for _ in range(n):
            result *= x
        
        return result
```

근데 이건 n이 엄청 크면 너무 느려서 보통 **통과가 안 돼.**

---

## 2) 진짜 정답용: 빠른 거듭제곱 (O(log n))
“제곱을 반으로 쪼개면서 계산”하는 아이디어야.

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        # 0제곱
        if n == 0:
            return 1.0
        
        # 음수 처리: x^-n = 1 / x^n
        if n < 0:
            x = 1 / x
            n = -n
        
        result = 1.0
        base = x
        
        while n > 0:
            # n이 홀수면, result에 base 한 번 곱해줌
            if n % 2 == 1:
                result *= base
            
            # base를 제곱 (x, x^2, x^4, x^8 ...)
            base *= base
            
            # n을 절반으로 줄임
            n //= 2
        
        return result
```

### 왜 이게 빠르냐면?
예를 들어 \(2^{10}\)을 구한다고 하면

- **그냥 곱하면** 2를 10번 곱함  
- **빠른 거듭제곱은**
  - \(2^{10} = (2^5)^2\)
  - \(2^5 = 2 \cdot (2^2)^2\)
  - 이렇게 **지수를 계속 반으로 줄여서** 계산 횟수가 확 줄어듦

그래서 n이 10억 같은 수여도 금방 계산돼.

---

정리하면:

✅ 네가 말한 것처럼  
`return x ** n` 이런 걸 원하는 게 아니라

✅ **거듭제곱의 정의와 원리를 코드로 직접 구현할 수 있냐**  
특히 **빠르게 구현할 수 있냐**를 보는 문제야.

원하면 내가 위 O(log n) 코드를 가지고,
`x=2, n=13` 같은 예시로 단계별로 값이 어떻게 변하는지 “진짜 학생 가르치듯” 추적 설명도 해줄게!

---
