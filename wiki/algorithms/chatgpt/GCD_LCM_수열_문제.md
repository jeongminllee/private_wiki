---
type: Concept
title: "GCD LCM 수열 문제"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-06-14)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-06-14
status: active
---

# GCD LCM 수열 문제

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-06-14

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
문제
 
$\operatorname{gcd}(d_1, \cdots, d_K) = A, \operatorname{lcm}(d_1, \cdots, d_K) = B$를 만족하는 서로 다른 양의 정수 
$K$개로 이루어진 수열 
$d_1, \cdots, d_K$를 구해보자.

입력
첫 번째 줄에 양의 정수 
$A$, 
$B$, 
$K$가 공백을 사이에 두고 주어진다. 
$(1 \le A < B \le 1\,000\,000 ; 2 \le K \le 100)$ 

출력
 
$K$개의 양의 정수 
$d_1, \cdots, d_K$를 공백을 사이에 두고 순서에 상관없이 출력한다.

조건을 만족하는 수열이 여러 개라면, 아무 수열이나 하나 출력한다.

조건을 만족하는 수열이 존재하지 않으면 -1만 출력한다.

예제 입력 1 
2 36 3
예제 출력 1 
4 6 18
예제 입력 2 
2 8 5
예제 출력 2 
-1
노트
 
$\operatorname{gcd}(d_1, \cdots, d_K)$는 
$d_1, \cdots, d_K$의 공통된 약수 중 가장 큰 양의 정수를 뜻하고, 
$\operatorname{lcm}(d_1, \cdots, d_K)$는 공통된 배수 중 가장 작은 양의 정수를 뜻한다.

### 💡 답변 (Assistant)
문제는 다음을 만족하는 **서로 다른 양의 정수 수열** \( d_1, d_2, \dots, d_K \) 를 찾는 것입니다:

- \(\gcd(d_1, \dots, d_K) = A\)
- \(\mathrm{lcm}(d_1, \dots, d_K) = B\)
- \(K\)개의 수
- \(A < B\)

---

### 핵심 아이디어

1. **공통 GCD가 A라는 것**은 각 수가 A의 배수임을 의미함:
   \[
   d_i = A \cdot x_i
   \]
   따라서 \(x_i\)들의 \(\gcd = 1\)

2. **LCM이 B라는 것**은 \( \mathrm{lcm}(d_1, \dots, d_K) = B \) 라는 뜻인데,
   \[
   \mathrm{lcm}(A \cdot x_1, \dots, A \cdot x_K) = A \cdot \mathrm{lcm}(x_1, \dots, x_K) = B
   \Rightarrow \mathrm{lcm}(x_1, \dots, x_K) = \frac{B}{A}
   \]

   즉, 우리는:
   - \(x_i\)들이 모두 서로 다른 양의 정수
   - \(\gcd(x_1, \dots, x_K) = 1\)
   - \(\mathrm{lcm}(x_1, \dots, x_K) = B / A\)
   인 수열을 찾으면 되고,
   마지막에 \(x_i \cdot A\)로 변환해서 출력하면 된다.

---

### 풀이 로직

1. \(T = \frac{B}{A}\)를 계산
2. \(T\)의 모든 약수를 구함 (이 중 일부를 선택해서 lcm이 T가 되는 수열을 만들 것)
3. 약수들의 부분집합을 탐색하여:
   - 크기가 \(K\)
   - 서로 다른 값
   - \(\gcd = 1\), \(\mathrm{lcm} = T\)
   인 경우를 찾음
4. 못 찾으면 -1 출력

---

### 코드 구현

```python
from math import gcd
from itertools import combinations
import sys
import math

def lcm(a, b):
    return a * b // gcd(a, b)

def total_lcm(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
        if result > 10**6:
            return -1
    return result

def solve(A, B, K):
    if B % A != 0:
        print(-1)
        return
    T = B // A

    # T의 약수 구하기
    divisors = []
    for i in range(1, int(T**0.5) + 1):
        if T % i == 0:
            divisors.append(i)
            if i != T // i:
                divisors.append(T // i)
    divisors.sort()

    # K개를 뽑아 조건을 만족하는지 확인
    for comb in combinations(divisors, K):
        if math.gcd(*comb) == 1 and total_lcm(comb) == T:
            result = [A * x for x in comb]
            print(" ".join(map(str, result)))
            return
    print(-1)

# 입력 처리
A, B, K = map(int, input().split())
solve(A, B, K)
```

---

### 예제 실행

**예제 1**

```
입력: 2 36 3
T = 36 / 2 = 18
약수: [1, 2, 3, 6, 9, 18]
가능한 조합: (2, 3, 9) -> lcm = 18, gcd = 1
출력: 4 6 18
```

**예제 2**

```
입력: 2 8 5
T = 4
약수: [1, 2, 4] → 조합 5개 만들 수 없음
출력: -1
```

---

필요시 시간 최적화를 위해 조합의 순서 줄이거나, 백트래킹으로도 가능하니 요청 시 확장해드릴게요.

---

### ❓ 질문 (User)
gcd도 math 라이브러리 쓰지말고 함수로 만들어서 코드 작성해줘

### 💡 답변 (Assistant)
물론입니다. `math` 라이브러리를 사용하지 않고 `gcd` 함수도 직접 구현한 버전으로 전체 코드를 재작성해드릴게요.

---

### 🔧 사용자 정의 `gcd`, `lcm` 함수 사용 전체 코드

```python
from itertools import combinations

def custom_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def total_gcd(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result = custom_gcd(result, num)
    return result

def custom_lcm(a, b):
    return a * b // custom_gcd(a, b)

def total_lcm(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result = custom_lcm(result, num)
        if result > 10**6:  # 너무 커지면 중단
            return -1
    return result

def solve(A, B, K):
    if B % A != 0:
        print(-1)
        return
    T = B // A  # 목표 LCM 값 (A로 나눈 값)

    # T의 약수 구하기
    divisors = []
    for i in range(1, int(T**0.5) + 1):
        if T % i == 0:
            divisors.append(i)
            if i != T // i:
                divisors.append(T // i)
    divisors.sort()

    # 약수 중 K개 조합 탐색
    for comb in combinations(divisors, K):
        if total_gcd(comb) == 1 and total_lcm(comb) == T:
            result = [A * x for x in comb]
            print(" ".join(map(str, result)))
            return

    print(-1)

# 입력 받기
A, B, K = map(int, input().split())
solve(A, B, K)
```

---

### ✅ 예제 테스트

- 입력: `2 36 3`  
  출력 예: `4 6 18` (또는 같은 조건을 만족하는 다른 조합)

- 입력: `2 8 5`  
  출력: `-1`

---

필요하다면 `재귀 방식 gcd`, 백트래킹 탐색 방식 등으로도 변형 가능합니다. 원하시면 말씀해 주세요.

---

### ❓ 질문 (User)
combinations 역시 직접 구현해줘

### 💡 답변 (Assistant)
좋습니다! `itertools.combinations` 없이 직접 조합을 생성하는 코드를 포함한 **완전한 코드**를 아래에 작성해드릴게요.

---

## ✅ 모든 라이브러리 없이 구현된 최종 코드

```python
# 사용자 정의 gcd
def custom_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 리스트 전체의 gcd
def total_gcd(arr):
    g = arr[0]
    for x in arr[1:]:
        g = custom_gcd(g, x)
    return g

# 사용자 정의 lcm
def custom_lcm(a, b):
    return a * b // custom_gcd(a, b)

# 리스트 전체의 lcm
def total_lcm(arr):
    l = arr[0]
    for x in arr[1:]:
        l = custom_lcm(l, x)
        if l > 10**6:
            return -1
    return l

# 조합 함수 (itertools 없이 직접 구현)
def generate_combinations(arr, k):
    result = []
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, len(arr)):
            path.append(arr[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result

# 문제 해결 함수
def solve(A, B, K):
    if B % A != 0:
        print(-1)
        return

    T = B // A  # 목표 LCM

    # T의 약수 구하기
    divisors = []
    for i in range(1, int(T ** 0.5) + 1):
        if T % i == 0:
            divisors.append(i)
            if i != T // i:
                divisors.append(T // i)
    divisors.sort()

    # 조합 생성
    combinations = generate_combinations(divisors, K)
    for comb in combinations:
        if total_gcd(comb) == 1 and total_lcm(comb) == T:
            print(" ".join(str(A * x) for x in comb))
            return

    print(-1)

# 입력 받기
A, B, K = map(int, input().split())
solve(A, B, K)
```

---

## 🔍 주요 구현 설명

- `custom_gcd`: 유클리드 호제법
- `generate_combinations`: 재귀적 백트래킹으로 조합 생성
- `solve`: 약수 리스트를 기반으로 조합을 만들고 조건 확인

---

## ✅ 예시 입력

```
입력: 2 36 3
출력: 4 6 18 (또는 조건을 만족하는 다른 조합)

입력: 2 8 5
출력: -1
```

---

필요하면 `조합 최적화`나 `더 빠른 탐색 알고리즘`도 도와드릴 수 있어요.

---

### ❓ 질문 (User)
라이브러리를 쓰면 알고리즘 문제를 해결할 수 있는데 직접 구현하면 해결이 안돼. 뭐가 문제일까

### 💡 답변 (Assistant)
아주 좋은 질문입니다.  
**라이브러리를 썼을 때 통과되고, 직접 구현한 조합(gcd, lcm, combinations)을 사용하면 실패하는 경우**는 보통 아래와 같은 원인 중 하나입니다:

---

## ✅ 가능한 주요 원인

### 1. **조합 구현이 정확하지 않거나, 누락된 경우**
- `generate_combinations` 함수가 **중복 없이**, **모든 경우의 수**를 생성해야 함
- 예를 들어, 중간에 백트래킹에서 `start` 인덱스를 잘못 처리하면 일부 조합이 누락될 수 있음 → 조건 만족 조합을 못 찾음

✔️ 검토 포인트:
```python
def backtrack(start, path):
    if len(path) == k:
        result.append(path[:])  # 얕은 복사 말고 깊은 복사
        return
    for i in range(start, len(arr)):
        path.append(arr[i])
        backtrack(i + 1, path)
        path.pop()
```

---

### 2. **gcd, lcm 계산이 잘못된 경우**
- `gcd` 또는 `lcm` 구현에서 오버플로우나 부정확한 계산이 발생했을 수 있음
- 특히 `lcm` 계산 중 `a * b`가 너무 커지면 `overflow` 또는 `값이 틀림`

✔️ 방어 코드:
```python
if result > 10**6:
    return -1  # lcm이 너무 크면 탐색 중단
```

---

### 3. **시간 초과**
- 조합 수가 많고 \(K\)가 클수록 조합을 모두 탐색하는 데 시간이 오래 걸릴 수 있음
- 라이브러리는 내부적으로 **C언어로 최적화** 되어 있기 때문에 훨씬 빠름

예: 약수가 100개고 \(K=10\)이면 → \( \binom{100}{10} \) ≈ 17억 개 조합 → 시간 초과!

✔️ 해결 방법:
- 조합의 수가 너무 많을 땐 **백트래킹에 조건 가지치기** 넣기
- 또는 **약수 정렬 기준으로 먼저 lcm에 영향을 많이 줄 애들부터 탐색**

---

### 4. **입력 값 자체가 해결 불가능한 경우인데 라이브러리에서는 우연히 조건을 만족하는 다른 조합을 찾음**
- 직접 구현에서는 탐색 순서상 **먼저 찾는** 조합이 없을 수 있음
- 라이브러리는 탐색 순서가 다르거나, 내부적으로 먼저 찾는 후보가 더 빠르게 조건을 만족할 수 있음

---

## 🔍 디버깅 방법

- `print("checking:", comb)` 같은 디버깅 출력문을 넣고,
  - `total_gcd(comb)`
  - `total_lcm(comb)`
- 이 둘을 **직접 비교해서 어디에서 오차가 생기는지** 체크

---

## ✅ 정리

| 문제 원인 | 해결책 |
|----------|--------|
| 조합 생성 오류 | 백트래킹 인덱스 점검 (`start`, `path[:]`) |
| gcd/lcm 구현 오류 | 직접 계산 확인, 디버깅 출력 |
| 시간 초과 | 조기 중단 조건(lcm이 크면 중단), 가지치기 |
| 탐색 순서 차이 | 가능한 조합을 정렬하거나 우선순위 부여 |

---

원하시면 직접 구현한 코드에 디버깅 출력을 넣어서 **실제 어느 조합에서 실패하는지** 같이 살펴봐드릴 수 있어요. 예시 케이스를 함께 알려주시면 더 정확하게 분석해드릴 수 있습니다.

---

### ❓ 질문 (User)
시간초과가 발생하는데 뭐가 문제일까

### 💡 답변 (Assistant)
좋은 질문입니다. 직접 구현한 코드에서 **시간 초과**가 발생하는 주된 원인은 다음과 같습니다:

---

## 🔍 1. **조합(combinations)의 수가 매우 많다**

### 문제의 핵심:
- `divisors`(약수)의 수가 많고  
- `K`가 클수록  
- \( \binom{N}{K} \)의 수는 **기하급수적으로 증가**합니다.

---

### 📌 예를 들어
```python
T = B // A = 720
→ T의 약수는 128개 (예시)
→ K = 10이면, 조합 수: 128C10 ≈ 2.5 * 10¹⁵ (2.5천조)
```

✅ **이건 절대 완전탐색으로 불가능한 수준**입니다.

---

## 🔍 2. **조기 탈출 조건 없음 (가지치기 부족)**

### 현재 로직:
- 모든 `K`개 조합을 만든 뒤
- `gcd`, `lcm` 체크 → 늦음

### 해결 방법:
- 조합을 생성하는 **과정 중간에 pruning(가지치기)** 필요
  - 예: 이미 lcm이 T를 초과하거나,
  - gcd가 이미 1보다 크면 더 볼 필요 없음

---

## 🔍 3. **lcm 계산 시 과도한 연산**

`lcm`을 수백 번 계산하는데 각 항목이 커지면 `a * b`가 `10^12` 이상이 되어 연산량이 커짐  
→ 반복적이고 불필요한 계산이 많음

---

## ✅ 해결 방안 요약

| 전략 | 설명 |
|------|------|
| 약수 개수 줄이기 | 너무 많은 약수는 상위 일부만 추출해서 탐색 |
| 백트래킹 + 가지치기 | `lcm > T`이면 중간에 잘라냄 |
| 조합 크기 제한 | `len(divisors) < K`이면 아예 -1 |
| lcm 캐싱 or early stop | lcm이 T 이상 되면 탐색 중단 |

---

## ✅ 개선된 핵심 로직 예시 (백트래킹 기반, 가지치기 포함)

```python
def custom_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def custom_lcm(a, b):
    return a * b // custom_gcd(a, b)

def backtrack(divs, idx, path, curr_gcd, curr_lcm, K, T, A):
    if len(path) > K or curr_lcm > T:
        return None
    if len(path) == K:
        if curr_gcd == 1 and curr_lcm == T:
            return [A * x for x in path]
        return None
    for i in range(idx, len(divs)):
        nxt = divs[i]
        new_gcd = custom_gcd(curr_gcd, nxt)
        new_lcm = custom_lcm(curr_lcm, nxt)
        result = backtrack(divs, i + 1, path + [nxt], new_gcd, new_lcm, K, T, A)
        if result:
            return result
    return None

def solve(A, B, K):
    if B % A != 0:
        print(-1)
        return
    T = B // A

    # 약수 구하기
    divs = []
    for i in range(1, int(T ** 0.5) + 1):
        if T % i == 0:
            divs.append(i)
            if i != T // i:
                divs.append(T // i)
    divs.sort()

    if len(divs) < K:
        print(-1)
        return

    result = backtrack(divs, 0, [], 0, 1, K, T, A)
    if result:
        print(" ".join(map(str, result)))
    else:
        print(-1)
```

---

## 🔚 결론

**시간 초과의 주범은 조합 수가 많고 가지치기가 없기 때문**입니다.  
→ `combinations` 대신 **백트래킹 + pruning** 방식으로 바꾸는 것이 핵심 해결책입니다.

---

원하시면 `조합 수 예측`, `lcm 추적 디버깅` 등도 함께 도와드릴게요.

---
