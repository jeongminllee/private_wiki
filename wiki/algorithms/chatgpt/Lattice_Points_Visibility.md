---
type: Concept
title: "Lattice Points Visibility"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-03-29)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-03-29
status: active
---

# Lattice Points Visibility

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-03-29

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
문제를 풀기 위한 핵심 아이디어는 “어떤 점이 (0,0,0)에서 보인다”는 말이, 그 점으로 향하는 벡터가 **소수 벡터(primitive vector)** 임을 의미한다는 점입니다. 즉, 점 \( (x,y,z) \)가 (0,0,0)에서 보이려면 \( x, y, z \)의 최대공약수(\(\gcd(x,y,z)\))가 1이어야 합니다.

아래에 두 가지 접근법을 소개합니다.

---

### 1. 단순 반복(Brute-force) 접근법

**개념:**
- \(0 \le x, y, z \le N\)인 모든 격자점에 대해, (0,0,0)은 제외하고 각 점 \( (x,y,z) \)에 대해 \(\gcd(x,y,z)\)를 구합니다.
- 만약 \(\gcd(x,y,z)=1\)이면, 이 점은 (0,0,0)에서 다른 격자점이 사이에 있지 않으므로 “보인다”라고 판단할 수 있습니다.

**구현 아이디어:**
- 3중 반복문을 사용하여 모든 점을 탐색합니다.
- 파이썬의 경우 `math.gcd`를 두 번 사용하여 \( \gcd(x, y, z) = \gcd(x, \gcd(y,z)) \)를 구할 수 있습니다.
- \(N \le 100\)이므로 반복문의 총 횟수는 \((N+1)^3\)로 최대 약 1,000,000번이 되어 충분히 빠르게 처리됩니다.

---

### 2. 수론적 접근 – 뫼비우스 함수(Möbius Function)를 이용한 포함-배제 원리

**개념:**
- 격자점의 개수를 직접 세는 대신, 뫼비우스 함수를 이용하여 소수 벡터의 개수를 수식으로 나타낼 수 있습니다.
- \( (x,y,z) \)가 보이려면 \(\gcd(x,y,z)=1\)여야 하므로, 뫼비우스 함수 \(\mu\)를 사용하여 포함-배제 원리를 적용할 수 있습니다.
  
**수식:**
\[
\text{visible}(N) = \sum_{d=1}^{N} \mu(d) \times \left(\left\lfloor \frac{N}{d} \right\rfloor + 1\right)^3 - 1
\]
- 여기서 \(\left(\left\lfloor \frac{N}{d} \right\rfloor + 1\right)^3\)는 \(d\)가 공약수인 점들의 개수를 나타내며, 최종적으로 원점을 빼주어 (0,0,0)을 제외합니다.
- 이 방법은 \(N\)의 범위가 클 때 더 효율적일 수 있으나, \(N \le 100\)인 경우 단순 반복으로도 충분합니다.

---

### 결론

문제 해결의 기본 아이디어는 **격자점의 좌표들이 서로 소(서로의 최대공약수가 1)인지 확인**하는 것입니다.  
- **단순 반복법**은 구현이 직관적이며, \(N \le 100\)에서는 효율적입니다.
- **뫼비우스 함수를 이용한 방법**은 수학적 사고를 바탕으로 포함-배제 원리를 적용하는 방법으로, 보다 일반적인 문제(예: \(N\)이 매우 큰 경우)에도 확장할 수 있습니다.

이러한 접근법을 바탕으로 문제를 풀면 주어진 예제처럼 \(N=1\)일 때 7, \(N=2\)일 때 19, \(N=5\)일 때 175가 나오는 결과를 얻을 수 있습니다.

---

### ❓ 질문 (User)
문제
Consider a N × N × N lattice. One corner is at (0,0,0) and the opposite one is at (N, N, N). How many lattice points are visible from corner at (0,0,0)? A point X is visible from point Y iff no other lattice point lies on the segment joining X and Y.

입력
The first line contains the number of test cases T. The next T lines contain an interger N.

출력
Output T lines, one corresponding to each test case.

제한
T ≤ 100, 1 ≤ N ≤ 100
예제 입력 1 
3
1
2
5
예제 출력 1 
7
19
175

이 문제의 접근방법을 알려줘

### 💡 답변 (Assistant)
아래는 뫼비우스 함수를 이용한 포함‑배제 원리를 활용하는 Python 코드 예제입니다.  
  
```python
import sys
import math

def mobius(n):
    """n에 대한 뫼비우스 함수 값을 반환합니다."""
    # 1인 경우
    if n == 1:
        return 1
    # 소인수분해 진행
    prime_count = 0
    i = 2
    temp = n
    while i * i <= temp:
        if temp % i == 0:
            prime_count += 1
            # 제곱 인수가 있는지 검사
            if temp // i % i == 0:
                return 0
            while temp % i == 0:
                temp //= i
        i += 1
    if temp > 1:
        prime_count += 1
    return -1 if prime_count % 2 else 1

def count_visible(N):
    """(0,0,0)를 제외한 [0,N]^3 내에서 (0,0,0)로부터 보이는 격자점의 개수를 반환합니다."""
    total = 0
    for d in range(1, N+1):
        count = (N // d + 1) ** 3 - 1  # d의 배수를 고려한 점의 개수, (0,0,0)은 제외
        total += mobius(d) * count
    return total

if __name__ == "__main__":
    input_data = sys.stdin.read().split()
    T = int(input_data[0])
    results = []
    for i in range(T):
        N = int(input_data[i+1])
        results.append(str(count_visible(N)))
    sys.stdout.write("\n".join(results))
```

---

### 코드 설명

1. **mobius(n):**  
   - \( n = 1 \)이면 1을 반환합니다.
   - \( n \)을 소인수분해하여, 제곱 인수가 있으면 0, 그렇지 않으면 소인수의 개수에 따라 (-1)^(개수)를 반환합니다.

2. **count_visible(N):**  
   - 각 \( d \) (1부터 \( N \)까지)에 대해, \( d \)가 공약수인 격자점의 개수를 \(\left(\left\lfloor \frac{N}{d} \right\rfloor + 1\right)^3 - 1\)로 계산하고, 뫼비우스 함수를 곱하여 포함‑배제 원리를 적용합니다.
   - 최종 합을 반환하면 (0,0,0)을 제외한 보이는 격자점의 개수가 됩니다.

3. **메인 부분:**  
   - 입력을 읽어 T개의 테스트 케이스에 대해 결과를 계산하고, 각 줄에 출력합니다.

이 코드를 이용하면 문제에서 주어진 예제 입력에 대해  
- N=1 → 7  
- N=2 → 19  
- N=5 → 175  
와 같은 결과를 얻을 수 있습니다.

---

### ❓ 질문 (User)
파이썬 코드로 구현해줘

### 💡 답변 (Assistant)
다음은 직접 구현한 최대공약수 함수를 사용하여 (0,0,0)에서 보이는 격자점을 세는 Python 코드 예제입니다.

```python
import sys

def gcd(a, b):
    # 유클리드 알고리즘을 사용한 최대공약수 함수
    while b:
        a, b = b, a % b
    return a

def gcd3(x, y, z):
    # 3개의 수에 대한 최대공약수를 계산 (0,0,0)은 제외 처리 필요
    return gcd(x, gcd(y, z))

def count_visible_bruteforce(N):
    count = 0
    # 모든 격자점 (x,y,z) 탐색, 단 (0,0,0)은 제외
    for x in range(N+1):
        for y in range(N+1):
            for z in range(N+1):
                if x == 0 and y == 0 and z == 0:
                    continue
                # (x,y,z)가 (0,0,0)으로부터 보이려면
                # 세 좌표의 최대공약수가 1이어야 함
                if gcd3(x, y, z) == 1:
                    count += 1
    return count

if __name__ == "__main__":
    input_data = sys.stdin.read().split()
    T = int(input_data[0])
    results = []
    for i in range(T):
        N = int(input_data[i+1])
        results.append(str(count_visible_bruteforce(N)))
    sys.stdout.write("\n".join(results))
```

---

### 코드 설명

1. **gcd(a, b):**  
   - 유클리드 알고리즘을 사용해 두 수의 최대공약수를 구합니다.

2. **gcd3(x, y, z):**  
   - 3개의 수 \(x\), \(y\), \(z\)에 대해 \(\gcd(x, \gcd(y, z))\)를 구합니다.

3. **count_visible_bruteforce(N):**  
   - \(0 \le x, y, z \le N\)인 모든 격자점에 대해, (0,0,0)은 제외하고, \( \gcd(x, y, z) \)가 1이면 보이는 격자점으로 간주하여 카운트합니다.

4. **메인 부분:**  
   - 표준 입력에서 테스트 케이스 개수 \(T\)와 각 \(N\)값을 읽어, 각 테스트 케이스에 대해 결과를 출력합니다.

이 코드는 문제에서 요구하는 예제 입력에 대해  
- N = 1 → 7  
- N = 2 → 19  
- N = 5 → 175  
와 같은 결과를 출력합니다.

---

### ❓ 질문 (User)
최대공약수 함수를 직접 만들어서 구하는 방법도 있던데 그 방식으로도 구현해줘

### 💡 답변 (Assistant)
이 코드는 뫼비우스 함수를 활용하여 3차원 격자 내에서 (0,0,0)로부터 보이는 점(격자점)의 개수를 효율적으로 세는 방법을 구현한 예제입니다. 각 함수와 코드의 흐름을 단계별로 설명하면 다음과 같습니다.

---

## 1. 뫼비우스 함수 (mobius)

```python
def mobius(n):
    """n에 대한 뫼비우스 함수 값을 반환합니다."""
    # 1인 경우
    if n == 1:
        return 1
    # 소인수분해 진행
    prime_count = 0
    i = 2
    temp = n
    while i * i <= temp:
        if temp % i == 0:
            prime_count += 1
            # 제곱 인수가 있는지 검사: 만약 i^2가 n의 약수이면, 뫼비우스 함수의 값은 0
            if temp // i % i == 0:
                return 0
            # i가 더 이상 약수인 동안 나누어 줌
            while temp % i == 0:
                temp //= i
        i += 1
    # 남은 수가 1보다 크면 소수가 하나 더 존재한다는 의미
    if temp > 1:
        prime_count += 1
    # 소인수의 개수가 홀수이면 -1, 짝수이면 1을 반환
    return -1 if prime_count % 2 else 1
```

### 상세 설명
- **뫼비우스 함수 개념:**  
  뫼비우스 함수 μ(n)는 수론에서 중요한 함수로, \( n \)이 제곱 인수를 가지면 0, 그렇지 않으면 소인수의 개수가 홀수이면 -1, 짝수이면 1을 반환합니다.
- **구현 과정:**  
  - \( n=1 \)이면 바로 1을 반환합니다.
  - \( n \)을 소인수분해하면서, 각 소수 \( i \)가 몇 번 나타나는지 확인합니다.
  - 만약 \( i \)가 \( n \)에 두 번 이상 등장하면(즉, \( i^2 \)가 \( n \)의 약수이면) 바로 0을 반환합니다.
  - 최종적으로 남은 수가 1보다 크다면 그 숫자도 소수이므로 소인수의 개수를 1 증가시킵니다.
  - 소인수의 개수에 따라 (-1) 또는 1을 반환합니다.

---

## 2. 보이는 격자점 세기 (count_visible)

```python
def count_visible(N):
    """(0,0,0)를 제외한 [0,N]^3 내에서 (0,0,0)로부터 보이는 격자점의 개수를 반환합니다."""
    total = 0
    for d in range(1, N+1):
        count = (N // d + 1) ** 3 - 1  # d의 배수를 고려한 점의 개수, (0,0,0)은 제외
        total += mobius(d) * count
    return total
```

### 상세 설명
- **문제의 핵심:**  
  (0,0,0)에서 어떤 점 \( (x,y,z) \)가 보이려면, \( x \), \( y \), \( z \)의 최대공약수가 1이어야 합니다.  
  이를 수론적 관점에서 다루기 위해 뫼비우스 함수를 사용하여 포함‑배제 원리를 적용할 수 있습니다.
- **포함‑배제 원리와 뫼비우스 함수:**  
  - 임의의 양의 정수 \( d \)에 대해, \( d \)가 모든 좌표의 공약수인 점들을 세면, \( (N // d + 1)^3 \)가 됩니다.
  - 여기서 \( -1 \)을 해주는 이유는 \( (0,0,0) \)은 제외하기 위함입니다.
  - 각 \( d \)에 대해 \( mobius(d) \)를 곱해 포함‑배제 원리를 적용하면, 최종적으로 \( \gcd(x,y,z)=1 \)인 점들의 총 개수를 얻을 수 있습니다.
- **반복문:**  
  \( d \)를 1부터 \( N \)까지 순회하면서 각 \( d \)에 대해 위의 점의 개수를 계산하고, 뫼비우스 함수 값과 곱한 후 누적합에 더합니다.

---

## 3. 메인 실행 부분

```python
if __name__ == "__main__":
    input_data = sys.stdin.read().split()
    T = int(input_data[0])
    results = []
    for i in range(T):
        N = int(input_data[i+1])
        results.append(str(count_visible(N)))
    sys.stdout.write("\n".join(results))
```

### 상세 설명
- **입력 처리:**  
  - `sys.stdin.read()`로 전체 입력을 읽고, 공백 기준으로 분리하여 리스트 `input_data`에 저장합니다.
  - 첫 번째 항목은 테스트 케이스의 개수 \( T \)입니다.
- **테스트 케이스 처리:**  
  - 이후 각 테스트 케이스에 대해 \( N \) 값을 읽고, `count_visible(N)` 함수를 호출하여 결과를 계산합니다.
  - 각 결과를 문자열 형태로 `results` 리스트에 저장합니다.
- **출력:**  
  - 모든 결과를 줄바꿈으로 연결하여 표준 출력으로 출력합니다.

---

## 전체적인 동작 원리

1. **뫼비우스 함수 계산:**  
   각 \( d \) (1부터 \( N \)까지)에 대해 뫼비우스 함수 \( \mu(d) \)를 계산합니다.

2. **점의 개수 계산:**  
   \( d \)가 공약수인 점들의 개수를 \((N // d + 1)^3 - 1\)로 계산합니다.  
   이때, \( N // d \)는 \( d \)가 배수인 좌표가 몇 개 있는지 나타내고, \( +1 \)은 0을 포함하기 때문입니다. \( -1 \)은 (0,0,0)을 빼기 위함입니다.

3. **포함‑배제 적용:**  
   뫼비우스 함수를 곱하여 포함‑배제 원리를 적용하면, 최종적으로 \( \gcd(x,y,z)=1 \)인, 즉 (0,0,0)에서 보이는 격자점의 수가 계산됩니다.

4. **테스트 케이스별 처리:**  
   각 입력 \( N \)에 대해 위의 계산을 수행하고 결과를 출력합니다.

이 코드는 수론적 지식을 응용하여 3차원 격자 문제를 효율적으로 해결하는 좋은 예제입니다.

---

### ❓ 질문 (User)
```
import sys
import math

def mobius(n):
    """n에 대한 뫼비우스 함수 값을 반환합니다."""
    # 1인 경우
    if n == 1:
        return 1
    # 소인수분해 진행
    prime_count = 0
    i = 2
    temp = n
    while i * i <= temp:
        if temp % i == 0:
            prime_count += 1
            # 제곱 인수가 있는지 검사
            if temp // i % i == 0:
                return 0
            while temp % i == 0:
                temp //= i
        i += 1
    if temp > 1:
        prime_count += 1
    return -1 if prime_count % 2 else 1

def count_visible(N):
    """(0,0,0)를 제외한 [0,N]^3 내에서 (0,0,0)로부터 보이는 격자점의 개수를 반환합니다."""
    total = 0
    for d in range(1, N+1):
        count = (N // d + 1) ** 3 - 1  # d의 배수를 고려한 점의 개수, (0,0,0)은 제외
        total += mobius(d) * count
    return total

if __name__ == "__main__":
    input_data = sys.stdin.read().split()
    T = int(input_data[0])
    results = []
    for i in range(T):
        N = int(input_data[i+1])
        results.append(str(count_visible(N)))
    sys.stdout.write("\n".join(results))
```
이 코드에 대해서 자세하게 설명해줘
