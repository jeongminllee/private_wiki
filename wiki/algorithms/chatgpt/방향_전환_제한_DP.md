---
type: Concept
title: "방향 전환 제한 DP"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-12-09)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-12-09
status: active
---

# 방향 전환 제한 DP

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-12-09

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
Leetcode 63. Unique Paths 2 문제에서 방향 전환을 제한을 두는 것을 추가하면 문제 풀이가 어떻게 될까?
예를 들어 
matrix = [[0,0,0],[0,1,0],[0,0,0]], k=2 
matrix = [[0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]], k=3
이런 두 테스트 케이스가 있다고 가정하고 문제를 해결해줘.

### 💡 답변 (Assistant)
핵심만 먼저 말하면:

- **방향 전환 제한(k)** 을 넣으면,  
  기존 `dp[i][j]` 한 칸짜리 DP로는 안 되고,
- **“마지막 이동 방향”과 “지금까지 쓴 방향 전환 횟수”** 까지 상태로 들고 가는 DP로 바꿔야 해요.

---

## 1. 문제 재정의

기존 LeetCode 63 (Unique Paths II):

- 시작: `(0,0)`
- 도착: `(m-1, n-1)`
- 이동: 오른쪽(R), 아래(D)만 가능
- `1`은 장애물, `0`은 빈 칸
- **모든 경로 개수**를 세는 문제

여기에 조건 하나를 더 붙입니다:

> “경로를 따라 이동할 때,  
>  **방향 전환(= R → D or D → R)** 을 최대 `k`번까지만 허용.”

즉,

- 같은 방향으로 계속 가는 건 괜찮고,
- **이동 방향이 바뀌는 순간을 1회 “turn”** 이라고 보고  
- 전체 turn 수 ≤ k 인 경로만 세는 문제.

---

## 2. 새 DP 정의

방향 전환을 세려면 “이전에 어떤 방향으로 왔는지”를 알아야 하죠.

그래서 상태를 이렇게 정의합니다:

> `dp[i][j][d][c]`  
> = `(i, j)` 칸에 도착했을 때  
>   - 마지막 이동 방향이 `d` (`0`: 오른쪽, `1`: 아래쪽) 이고  
>   - 방향 전환을 **정확히 `c`번** 사용한 경로의 수

최종 답은:

```text
answer = sum(dp[m-1][n-1][d][c])   # d in {0,1}, 0 ≤ c ≤ k
```

### 전이(transition)

1. 왼쪽에서 오는 경우: `(i, j-1) -> (i, j)` (이동 방향 = 오른쪽, `d = 0`)

   - 이전에도 오른쪽이었으면 turn 증가 없음
   - 이전에 아래쪽이었다면 turn + 1

   수식으로 쓰면:

   ```text
   # from left (i, j-1) with last dir = right
   dp[i][j][0][c] += dp[i][j-1][0][c]

   # from left (i, j-1) with last dir = down -> 방향 전환 발생
   dp[i][j][0][c] += dp[i][j-1][1][c-1]   (c ≥ 1일 때만)
   ```

2. 위에서 오는 경우: `(i-1, j) -> (i, j)` (이동 방향 = 아래, `d = 1`)

   ```text
   # from top (i-1, j) with last dir = down
   dp[i][j][1][c] += dp[i-1][j][1][c]

   # from top (i-1, j) with last dir = right -> 방향 전환
   dp[i][j][1][c] += dp[i-1][j][0][c-1]   (c ≥ 1일 때만)
   ```

3. 시작점 처리 `(0, 0)`

- 시작점에는 “이전 이동 방향”이 없습니다.
- 그래서 `(0,0)`에서 **직접 한 칸 옆으로 나가는 첫 이동**을 “방향 전환 0번 사용”으로 초기화하면 됩니다.

예:

- `(0,0) -> (0,1)` : 오른쪽으로 첫 이동

  ```text
  dp[0][1][RIGHT][0] += 1
  ```

- `(0,0) -> (1,0)` : 아래로 첫 이동

  ```text
  dp[1][0][DOWN][0] += 1
  ```

장애물(`grid[i][j] == 1`)이 있는 칸은 애초에 전이를 안 시키면 됩니다.

---

## 3. 시간·공간 복잡도

그리드 크기가 `m x n`, 방향 전환 제한이 `k`라면,

- 상태 수: `m * n * 2 * (k+1)`
- 전이도 각 칸에서 상수 번이므로

> **시간 복잡도**: `O(m * n * k)`  
> **공간 복잡도**: `O(m * n * k)`

필요하면, 한 줄(or 두 줄)씩만 유지해서 `O(n * k)`까지 줄이는 것도 가능해요.

---

## 4. 예제 1

```python
matrix = [
    [0,0,0],
    [0,1,0],
    [0,0,0]
]
k = 2
```

먼저 원래 Unique Paths II 기준으로 가능한 경로를 떠올려 보면:

- 장애물은 중앙 `(1,1)`
- 유효 경로는 딱 2개:

  1. 오른쪽, 오른쪽, 아래, 아래  
     `R R D D`  
     → 방향 시퀀스: `R, R, D, D`  
     → 방향 전환: `R -> D` 한 번 → **1회**

  2. 아래, 아래, 오른쪽, 오른쪽  
     `D D R R`  
     → 방향 시퀀스: `D, D, R, R`  
     → 방향 전환: `D -> R` 한 번 → **1회**

- 어떤 경로도 turn = 0 으로는 도착할 수 없음  
  (오른쪽만, 혹은 아래만으로는 (2,2)에 도착 불가)

그래서:

- `k = 0` → 0개
- `k = 1` → 2개
- `k = 2` → 여전히 2개 (추가 경로 없음)

> **질문에서 준 `k = 2`에 대한 답: `2`**

---

## 5. 예제 2

```python
matrix = [
    [0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
]
k = 3
```

이건 사람이 손으로 세기에는 거의 불가능한 수준이라  
위에서 설명한 **4차원 DP**로 계산하는 게 맞습니다.

그 DP대로 계산하면:

- `k = 2` 일 때: **12개 경로**
- `k = 3` 일 때: **78개 경로**

> **질문에서 준 `k = 3`에 대한 답: `78`**

(참고로 장애물이 같은 열에 몇 개 있어서,  
turn 수가 작을수록 돌아가야 하는 경로가 제한되면서 경로 수가 꽤 줄어들어요.)

---

## 6. 파이썬 구현 예시

LeetCode 스타일로 쓰면 대략 이런 느낌입니다:

```python
from typing import List

def uniquePathsWithObstaclesKTurns(grid: List[List[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[m-1][n-1] == 1:
        return 0

    # dp[i][j][dir][c]
    # dir: 0 = 오른쪽, 1 = 아래쪽
    dp = [[[[0] * (k + 1) for _ in range(2)] for _ in range(n)] for _ in range(m)]

    # (0,0)에서 한 칸 오른쪽 / 아래로 가는 첫 이동 초기화
    if n > 1 and grid[0][1] == 0:
        dp[0][1][0][0] = 1  # 첫 이동: 오른쪽, turn 0
    if m > 1 and grid[1][0] == 0:
        dp[1][0][1][0] = 1  # 첫 이동: 아래, turn 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                continue
            if i == 0 and j == 0:
                continue
            # 왼쪽에서 오는 경우: dir = 0 (right)
            if j - 1 >= 0 and grid[i][j-1] == 0:
                for c in range(k + 1):
                    # 이전에도 오른쪽
                    dp[i][j][0][c] += dp[i][j-1][0][c]
                    # 이전이 아래였다면 turn + 1
                    if c > 0:
                        dp[i][j][0][c] += dp[i][j-1][1][c-1]

            # 위에서 오는 경우: dir = 1 (down)
            if i - 1 >= 0 and grid[i-1][j] == 0:
                for c in range(k + 1):
                    # 이전에도 아래
                    dp[i][j][1][c] += dp[i-1][j][1][c]
                    # 이전이 오른쪽이었다면 turn + 1
                    if c > 0:
                        dp[i][j][1][c] += dp[i-1][j][0][c-1]

    ans = 0
    for d in range(2):
        for c in range(k + 1):
            ans += dp[m-1][n-1][d][c]
    return ans
```

---

## 7. 정리

- **방향 전환 제한**이 들어가는 순간,  
  단순 `dp[i][j]`가 아니라 **“현재 칸 + 마지막 방향 + 사용한 turn 수”** 를 함께 들고 가야 합니다.
- 이걸 4차원 DP로 구현하면:

  - 예제 1: `[[0,0,0],[0,1,0],[0,0,0]], k=2` → **2**
  - 예제 2: 9×9 그리드, `k=3` → **78**

원하면 이걸 **1D/2D로 압축해서 메모리 줄이는 버전**이나,  
**k가 충분히 클 때(사실상 제한 없는 경우) 원래 LeetCode 63 결과와 같아지는 조건**도 같이 정리해 줄게.

---

### ❓ 질문 (User)
```
N = int(input())
K = int(input())
AB = [tuple(map(int, input().split())) for _ in range(K)]

# Please write your code here.
solutions = [i for i in range(1, 2*N+1)]

def combine(arr, k) :
    res = []
    visited = [0] * len(arr)
    combinations(0, k, arr, visited, [], 0, res)

    return res

def combinations(bgn, end, nums, visited, buildings, depth, res) :
    if depth == end :
        res.append(buildings[:])
        return

    for idx in range(bgn, len(nums)) :
        if visited[idx] :
            continue
        
        visited[idx] = 1
        combinations(idx+1, end, nums, visited, buildings + [nums[idx]], depth + 1, res)
        visited[idx] = 0

com_sol = combine(solutions, N)
ans = 0
for com in com_sol :
    res = set()
    for c in com :
        for a, b in AB :
            if c == a :
                res.add(c)
            if c == b :
                res.add(c)
    ans = max(ans, len(res))

print(ans)
    
```

이 문제를 보고 다음 코드가 왜 틀렸는지 분석해줘

### 💡 답변 (Assistant)
일단 문제부터 다시 한 줄로 정리하면:

> 1~2N 번 음료 중 **정확히 N개**를 골라서 살 수 있고,  
> i번째 완성 음료는 (Aᵢ, Bᵢ) 두 음료를 모두 샀을 때만 만들 수 있다.  
> 만들 수 있는 **완성 음료의 개수** 최대값을 구하는 문제.

---

## 1. 지금 코드가 실제로 계산하는 것

코드 흐름을 보면:

```python
solutions = [i for i in range(1, 2*N+1)]
com_sol = combine(solutions, N)   # 2N개 중 N개 고르는 모든 조합

ans = 0
for com in com_sol :
    res = set()
    for c in com :
        for a, b in AB :
            if c == a :
                res.add(c)
            if c == b :
                res.add(c)
    ans = max(ans, len(res))
```

여기서 `res` 에 들어가는 건 **“선택한 음료 번호들(com) 중에서, 레시피의 Aᵢ 또는 Bᵢ로 한 번이라도 등장한 음료 번호”** 입니다.

즉, 이 코드는

> “선택한 N개의 음료 중에서,  
>  최소 한 번이라도 어떤 완성 음료의 재료로 쓰이는 음료 번호의 개수”

를 세고 있습니다.  

하지만 우리가 구해야 하는 건

> “선택한 N개로 **실제로 만들 수 있는 완성 음료(쌍 (Aᵢ, Bᵢ))의 개수**”

죠.  
**재료(번호)의 개수**를 세고 있고,  
**‘둘 다 포함되어 있는 레시피 쌍(Aᵢ, Bᵢ)’의 개수**를 세고 있지 않습니다.

---

## 2. 왜 틀렸는지 간단한 반례

### 반례 1

```text
N = 2, K = 1
AB = [(1, 2)]    # 완성 음료는 1번+2번 하나뿐
2N = 4 이라고 하자 (음료 1,2,3,4)
```

- 조합 {1, 2} 를 선택했다고 하면

  ```python
  com = [1, 2]
  res = set()
  # c = 1: (a,b) = (1,2) 이므로 c == a → res = {1}
  # c = 2: (a,b) = (1,2) 이므로 c == b → res = {1, 2}
  len(res) = 2
  ```

  **코드 결과:** 2  
  **진짜 정답:** 만들 수 있는 완성 음료는 (1,2) 하나 → 1

- 조합 {1, 3} 을 선택하면?

  ```python
  com = [1, 3]
  res = set()
  # c = 1 → (1,2)의 a와 같음 → res = {1}
  # c = 3 → (1,2)와 아무 상관 없음
  len(res) = 1
  ```

  **코드 결과:** 1  
  하지만 2번 음료를 안 샀으니 (1,2) 음료는 만들 수 없음 → **실제 0** 이 되어야 합니다.

즉,

- “재료 중 하나라도 포함되어 있으면 카운트”
  → 이렇게 세고 있기 때문에,
- **두 재료를 모두 샀는지 여부를 전혀 확인하지 못하는 것**이 핵심 버그입니다.

---

## 3. 무엇을 해야 하는가 (논리 수정)

각 조합 `com`에 대해 해야 할 일은:

1. `com`을 set으로 만들어서 빠르게 포함 여부를 확인하고,
2. 매 레시피 (Aᵢ, Bᵢ)에 대해

   ```python
   if Aᵢ in chosen and Bᵢ in chosen:
       count += 1
   ```

   처럼 **두 재료가 모두 선택된 경우에만** 완성 음료 개수를 1 증가.

3. 그 `count` 의 최대값을 갱신.

이렇게 해야 “만들 수 있는 완성 음료 개수”를 제대로 셉니다.

---

## 4. 고친 코드 예시

조합 생성은 그대로 두고, 내부 로직만 고쳐 보면:

```python
from itertools import combinations

N = int(input())
K = int(input())
AB = [tuple(map(int, input().split())) for _ in range(K)]

solutions = [i for i in range(1, 2*N + 1)]
ans = 0

# 조합은 itertools.combinations 써도 되고, 기존 combine 써도 됨
for com in combinations(solutions, N):
    chosen = set(com)
    cnt = 0
    for a, b in AB:
        if a in chosen and b in chosen:  # 두 재료를 모두 샀을 때만 +1
            cnt += 1
    ans = max(ans, cnt)

print(ans)
```

`combine` 함수를 계속 쓰고 싶다면:

```python
com_sol = combine(solutions, N)
ans = 0
for com in com_sol:
    chosen = set(com)
    cnt = 0
    for a, b in AB:
        if a in chosen and b in chosen:
            cnt += 1
    ans = max(ans, cnt)
print(ans)
```

이렇게 수정하면 **문제에서 요구하는 “완성 음료 수”**를 정확히 세게 됩니다.

---

## 5. 보너스: 시간 복잡도는 괜찮나?

제한 조건(스크린샷 기준)이:

- `1 ≤ N ≤ 10` → `2N ≤ 20`
- `1 ≤ K ≤ 20` 정도라면,

조합 개수는 최대 `C(20, 10) ≈ 184,756` 개이고,  
각 조합마다 `K ≤ 20` 레시피를 검사하니 대략

> 18만 × 20 ≈ 360만 번의 레시피 검사

+ 약간의 오버헤드 정도라서 파이썬으로도 충분히 돌아갈 수 있는 수준입니다.

---

정리하면,

- **현재 코드는 “재료 번호”를 세고 있고,**
- **실제 문제는 “레시피 쌍(Aᵢ, Bᵢ)”의 개수를 세야 해서 틀린 것**입니다.  
- 각 조합에 대해 `(a in chosen and b in chosen)` 으로 체크해서 완성 음료 수를 세도록 고치면 됩니다.

---

### ❓ 질문 (User)
# Please write your code here.
# 1번 구간 : 5 6 7 8 9 10
# 2번 구간 : 1 2 3 4
# 3번 구간 : 3 4 5 6 7 
# N+1번 구간 : 5 6 7 8 9 10
# K번 이상 등장하는 수. 근데 한 번은 복사가 가능함. 
# K 이상 등장하는 개수의 최대값을 출력하라

이런 문제를 받았어. 설계부터 도와줘

### 💡 답변 (Assistant)
좋아, 이 문제는 살짝 “트릭”이 있지만 DP까지 갈 필요는 없고  
**구간 + 누적합(차분 배열)** 로 해결할 수 있어요. 설계부터 차근차근 짤게.

---

## 0. 문제를 내가 이해한 버전

- 정수 구간들이 여러 개 있다.  
  예)  
  - 1번 구간: 5 6 7 8 9 10  
  - 2번 구간: 1 2 3 4  
  - 3번 구간: 3 4 5 6 7  
  - …  
- 어떤 정수 x가 “등장한다” = x가 포함된 구간이 몇 개 있는지(겹치는 구간 수).

여기서

> 한 번, **어떤 한 구간을 복사해서 한 번 더 추가**할 수 있다.  
> 이때, “등장 횟수 ≥ K” 인 정수의 개수를 최대화하라.

로 이해하고 설계할게.

---

## 1. 관찰: 복사의 효과는 어디에만 의미가 있을까?

각 정수 x에 대해,  
현재 구간들에서의 등장 횟수를 `cnt[x]`라고 하자.

복사를 한 번 하면, 선택한 한 구간 [L, R] 안에 있는 정수들의 등장 횟수가 +1씩 늘어난다.

- 이미 `cnt[x] ≥ K` 이면 → 복사하든 말든 **이미 조건 만족**, 개수는 그대로.
- `cnt[x] ≤ K-2` 이면 → +1 해도 `cnt[x] + 1 ≤ K-1` → 여전히 조건 불만족.
- **`cnt[x] == K-1`** 이면 → +1 하면 `K`가 되어 **새로 조건을 만족**.

즉:

> 복사가 의미가 있는 지점은  
> **“현재 등장 횟수가 정확히 K-1인 정수들”** 뿐이다.

그래서 전략은:

1. 복사 안 해도 이미 `cnt[x] ≥ K` 인 정수들의 개수 = **기본값(base)**.
2. 복사할 구간 하나를 골라서,
   - 그 구간 안에 있는 `cnt[x] == K-1` 인 정수의 개수를 최대화.
3. 최종 정답 = `base + (복사로 새로 K 이상이 되는 개수의 최대값)`.

---

## 2. cnt[x]를 어떻게 구할까? (차분 배열 + 누적합)

구간이 많고, 좌표 범위가 클 수 있으니 일일이 x마다 “몇 개의 구간이 나를 포함하지?” 를 세면 O(N * 좌표)라서 비효율적이죠.

### (1) 좌표 범위가 크지 않은 경우 (예: 최대 1e6 정도)

가장 쉬운 버전:

- `diff` 라는 배열을 준비해서,  
  각 구간 [L, R]에 대해
  ```python
  diff[L] += 1
  diff[R+1] -= 1
  ```
- 그 다음,
  ```python
  cnt[x] = cnt[x-1] + diff[x]
  ```
  로 전체 구간을 한 번만 스캔하면,  
  각 x마다 몇 개의 구간에 포함되는지(=겹치는 횟수)를 알 수 있어.

### (2) 좌표가 1e9 이런 식으로 큰 경우 → 좌표 압축

- 모든 구간의 L, R, 그리고 R+1 을 모아서
- 정렬해서 인덱스를 매긴 뒤
- 그 압축된 인덱스 공간에서 위의 diff/누적합을 돌리면 됨.

아이디어 자체는 동일하고, 구현만 압축을 끼우는 정도라 여기서는 (1) 버전으로 설계 설명할게.

---

## 3. base와 “K-1 개수”를 위한 prefix sums

`cnt[x]`를 알면, 우리는 두 가지 정보가 필요해:

1. **현재 이미 K번 이상 등장하는 정수의 개수**  
   → `cnt[x] >= K` 인 x의 개수

2. **각 구간 [L, R] 안에 `cnt[x] == K-1` 인 x가 몇 개나 있는지**  
   → 복사했을 때 새로 K 이상이 되는 정수의 수 = 이 값.

이걸 빠르게 하기 위해 “조건에 따라 0/1 배열 + prefix sum”을 쓴다.

```python
geK[x] = 1 if cnt[x] >= K else 0      # 이미 조건 만족
eqKm1[x] = 1 if cnt[x] == K-1 else 0  # 한 번만 더 나오면 K 되는 애들

# prefix sum
pre_geK[0] = pre_eqKm1[0] = 0
for x in range(1, MAX+1):
    pre_geK[x]   = pre_geK[x-1]   + geK[x]
    pre_eqKm1[x] = pre_eqKm1[x-1] + eqKm1[x]
```

- 복사 안 했을 때 기본값:
  ```python
  base = pre_geK[MAX]
  ```

- 어떤 구간 [L, R]을 복사했을 때,  
  그 구간 안에서 새로 K 이상이 되는 정수 개수는:
  ```python
  gain = pre_eqKm1[R] - pre_eqKm1[L-1]
  ```

그래서 모든 구간에 대해 `gain`을 계산해 최댓값을 찾고:

```python
max_gain = max(gain over all intervals)
answer = base + max_gain
```

하면 끝.

복사 안 하는 게 더 나은 경우는?  
`max_gain`이 0이면 그냥 base 그대로고,  
복사는 해도 손해는 없으니 따로 분기 안 해도 됩니다.

---

## 4. 전체 알고리즘 흐름 정리

1. 입력:  
   - M개의 구간 [Lᵢ, Rᵢ] (1 ≤ i ≤ M)  
   - 정수 K
2. `MAX = max(Rᵢ)` 계산.
3. 길이 `MAX+2` 짜리 `diff` 배열 생성, 0으로 초기화.
4. 각 구간마다:
   ```python
   diff[Lᵢ]   += 1
   diff[Rᵢ+1] -= 1
   ```
5. 누적합으로 `cnt[x]` 계산:
   ```python
   cnt[0] = 0
   for x in 1..MAX:
       cnt[x] = cnt[x-1] + diff[x]
   ```
6. `geK[x]`, `eqKm1[x]` 만들고, `pre_geK`, `pre_eqKm1` prefix sum 계산.
7. `base = pre_geK[MAX]`.
8. 모든 구간 [Lᵢ, Rᵢ] 에 대해:
   ```python
   gain = pre_eqKm1[Rᵢ] - pre_eqKm1[Lᵢ - 1]
   max_gain = max(max_gain, gain)
   ```
9. `answer = base + max_gain` 출력.

### 시간 복잡도

- diff / 누적합 / prefix sum: O(MAX)
- 구간 수 M 만큼 gain 계산: O(M)

좌표 범위가 너무 크다면 MAX 대신 “좌표 압축된 size”가 들어가서  
전체는 `O((M + 압축된좌표개수) log M)` 정도.

---

## 5. 예시로 감각 잡기

아까 예시처럼:

- 1번: [5, 10]
- 2번: [1, 4]
- 3번: [3, 7]
- 4번: [5, 10]
- K = 2 라고 해보자.

`cnt[x]`를 세면:

- 1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:3, 8:2, 9:2, 10:2

- `cnt[x] >= 2` 인 x: 3~10 → base = 8
- `cnt[x] == 1` 인 x: 1,2 → eqKm1

각 구간의 gain:

- [5,10]: 1,2가 포함 안 돼서 gain = 0
- [1,4]: 1,2 둘 다 포함 → gain = 2
- [3,7]: 3,4는 이미 cnt=2 → eqKm1 아님 → gain = 0
- [5,10]: 0

max_gain = 2 → answer = 8 + 2 = 10  
→ 결국 1~10 모두 등장횟수 ≥ 2가 되도록 만들 수 있다.

---

## 6. (보너스) 파이썬 코드 틀

입력 포맷만 알면 바로 이렇게 짤 수 있어:

```python
import sys
input = sys.stdin.readline

M, K = map(int, input().split())
intervals = []
max_r = 0
for _ in range(M):
    l, r = map(int, input().split())
    intervals.append((l, r))
    if r > max_r:
        max_r = r

# 1. diff 배열
diff = [0] * (max_r + 3)
for l, r in intervals:
    diff[l] += 1
    diff[r + 1] -= 1

# 2. cnt[x] 계산
cnt = [0] * (max_r + 2)
for x in range(1, max_r + 1):
    cnt[x] = cnt[x-1] + diff[x]

# 3. geK, eqKm1 및 prefix sums
geK = [0] * (max_r + 2)
eqKm1 = [0] * (max_r + 2)
for x in range(1, max_r + 1):
    if cnt[x] >= K:
        geK[x] = 1
    if cnt[x] == K - 1:
        eqKm1[x] = 1

pre_geK = [0] * (max_r + 2)
pre_eqKm1 = [0] * (max_r + 2)
for x in range(1, max_r + 1):
    pre_geK[x] = pre_geK[x-1] + geK[x]
    pre_eqKm1[x] = pre_eqKm1[x-1] + eqKm1[x]

base = pre_geK[max_r]

max_gain = 0
for l, r in intervals:
    gain = pre_eqKm1[r] - pre_eqKm1[l-1]
    if gain > max_gain:
        max_gain = gain

print(base + max_gain)
```

---

여기까지가 전체 설계야.  
입력 형식이랑 좌표 범위 알려주면, 그에 맞게 딱 맞는 코드로 정리도 해 줄 수 있어.

---

### ❓ 질문 (User)
입력
0 0 0 1 0
0 0 0 1 0
0 0 1 1 0
0 1 0 0 0
0 0 0 0 0
출력

5
예제 설명

접기
N=5.

(1, 1)에서 (5, 5) 지점으로 이동하는 최소 이동 횟수는 5번으로 다음과 같습니다.

(1, 1)→(2, 2)→(3, 2)→(4, 3)→(5, 4)→(5, 5)로 가는 것이 최소 이동이며, 5번 이동했습니다.

이런 알고리즘 문제를 어떻게 하면 해결할 수 있을까? 
```
N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]
 
# Please write your code here.
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

dig = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

from collections import deque

def bfs(si, sj) :
    q = deque()
    q.append((si, sj, 0))
    v = [[[0] * 4 for _ in range(N)] for _ in range(N)]
    v[si][sj][0] = 1

    while q :
        ci, cj, cnt = q.popleft()

        if (ci, cj) == (N-1, N-1) :
            return v[ci][cj]

        for d in range(4) :
            ni, nj = ci + di[d], cj + dj[d]
            if 0 <= ni < N and 0 <= nj < N and grid[ni][nj] == 0 and v[ni][nj][cnt] == 0 :
                q.append((ni, nj, cnt))
                v[ni][nj][cnt] = v[ci][cj][cnt] + 1
        
        while cnt < 3 :
            for dgi, dgj in dig :
                ni, nj = ci + dgi, cj + dgj
                if 0 <= ni < N and 0 <= nj < N and grid[ni][nj] == 0 and v[ni][nj][cnt] == 0 :
                    q.append((ni,nj,cnt+1))
                    v[ni][nj][cnt+1] = v[ci][cj][cnt] + 1

    return -1

res = bfs(0, 0)

print(res)
```
내가 작성한 중간 코드야. res 부분에서 값을 확인하려고 했는데 시간초과나 메모리 초과가 나왔어.

### 💡 답변 (Assistant)
우선 문제 자체부터 정리해볼게.

- N×N 격자, 0은 빈칸, 1은 장애물
- 시작: (1,1) → 코드상 (0,0)
- 도착: (N,N) → 코드상 (N-1,N-1)
- 이동:
  - 상/하/좌/우로 1칸
  - 대각선(↖↗↙↘)은 **최대 3번까지만** 사용 가능
- 최소 이동 횟수를 구하는 문제

정답 알고리즘 자체는 **BFS + 상태에 ‘대각선 사용 횟수’를 추가한 3차원 방문 배열**이면 충분해요.  
지금 코드가 시간초과/메모리초과 나는 이유는 **상태 설계는 거의 맞는데, 구현에서 두 군데가 크게 잘못되어서 사실상 무한 루프에 가까운 상태**가 되었기 때문입니다.

---

## 1. 이런 유형을 어떻게 설계하느냐?

이런 “특수한 이동을 K번까지 쓸 수 있다” 류 문제는 패턴이 거의 고정입니다.

1. **상태 정의**

   - 보통 격자 BFS는 `(i, j)` 가 상태죠.
   - 여기서는 “대각선 이동을 몇 번 썼는지” 도 중요하므로

     > 상태 = `(i, j, k)`  
     > `k` = 지금까지 사용한 대각선 이동 횟수 (0~3)

2. **방문 배열 정의**

   - 같은 칸 `(i, j)` 에 와도,  
     `k=0`일 때와 `k=3`일 때는 “앞으로 쓸 수 있는 대각선 기회”가 다르니까
   - 따라서 방문도 3차원:

     ```python
     dist[i][j][k] = (i, j, k) 상태까지의 최소 이동 횟수
     ```

3. **BFS**

   - 큐에는 `(i, j, k)` 를 넣고,
   - 한 상태에서
     - 4방향 이동은 `k` 그대로
     - 대각선 이동은 `k` → `k+1` 로 바꿔서 push (`k < 3` 일 때만)
   - 아직 방문하지 않은 `(ni, nj, k')` 만 넣는다.

4. **정답**

   - 도착점 `(N-1, N-1, k)` 에 도달하는 순간의 `dist` 가 곧 정답
   - 여러 `k` 로 도착할 수 있으면 최소값을 사용 (BFS라서 처음 도착하는 게 최소).

---

## 2. 지금 코드에서 시간/메모리 터지는 핵심 버그

네 코드:

```python
while cnt < 3 :
    for dgi, dgj in dig :
        ni, nj = ci + dgi, cj + dgj
        if 0 <= ni < N and 0 <= nj < N and grid[ni][nj] == 0 and v[ni][nj][cnt] == 0 :
            q.append((ni,nj,cnt+1))
            v[ni][nj][cnt+1] = v[ci][cj][cnt] + 1
```

여기서 문제가 두 개 있어요.

### (1) `while cnt < 3` → 사실상 **무한 루프**

- `cnt` 값은 **while 안에서 절대 바뀌지 않아요.**
- 그래서 `cnt < 3`인 상태가 큐에서 한 번 나오면,
  - 그 상태에서 **무한히** `while`을 돌게 됩니다.
- Python에서 완전한 무한루프는 아니더라도,  
  내부에서 큐에 계속 push 하면서 **엄청난 상태가 생성** → 시간 & 메모리 폭발.

여기는 그냥

```python
if cnt < 3:
    ...
```

이어야 합니다.  
한 상태에서 “대각선 이동을 한 번 시도”만 하면 되지,  
`cnt`가 늘어나지 않는 `while`을 돌릴 이유가 전혀 없어요.

### (2) 방문 체크 인덱스가 틀렸음

조건문:

```python
if 0 <= ni < N and 0 <= nj < N and grid[ni][nj] == 0 and v[ni][nj][cnt] == 0 :
    q.append((ni,nj,cnt+1))
    v[ni][nj][cnt+1] = v[ci][cj][cnt] + 1
```

- **체크는 `v[ni][nj][cnt] == 0`**
- **표시는 `v[ni][nj][cnt+1] = ...`**

즉, 대각선으로 새 상태 `(ni, nj, cnt+1)` 를 만들면서  
`(ni, nj, cnt)` 만 검사하고 있어요.

그 결과:

- `(ni, nj, cnt+1)` 이 이미 수십 번 방문되어 있어도,
- `(ni, nj, cnt)` 는 계속 0이라서
- **동일한 상태 `(ni, nj, cnt+1)` 를 계속 큐에 밀어넣게 됩니다.**

이것도 상태 수 폭발 → 시간/메모리 초과.

여기는 이렇게 되어야 합니다.

```python
if 0 <= ni < N and 0 <= nj < N and grid[ni][nj] == 0 and v[ni][nj][cnt+1] == 0:
    q.append((ni, nj, cnt+1))
    v[ni][nj][cnt+1] = v[ci][cj][cnt] + 1
```

---

## 3. 전체적으로 깔끔하게 고친 코드

대각선 최대 3번이라고 가정하고, 좀 정리해서 써 보면:

```python
from collections import deque

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# 상하좌우
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]
# 대각선 4방향
dig = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

MAX_K = 3  # 대각선 최대 사용 횟수

def bfs(si, sj):
    # dist[i][j][k] = (i,j)까지 오면서 대각선 k번 쓴 상태의 최소 이동 횟수
    dist = [[[-1] * (MAX_K + 1) for _ in range(N)] for _ in range(N)]
    q = deque()

    dist[si][sj][0] = 0
    q.append((si, sj, 0))

    while q:
        ci, cj, used = q.popleft()
        # 도착
        if ci == N - 1 and cj == N - 1:
            return dist[ci][cj][used]

        # 4방향 이동 (대각선 X)
        for d in range(4):
            ni, nj = ci + di[d], cj + dj[d]
            if 0 <= ni < N and 0 <= nj < N and grid[ni][nj] == 0:
                if dist[ni][nj][used] == -1:
                    dist[ni][nj][used] = dist[ci][cj][used] + 1
                    q.append((ni, nj, used))

        # 대각선 이동 (used < MAX_K 일 때만)
        if used < MAX_K:
            for dgi, dgj in dig:
                ni, nj = ci + dgi, cj + dgj
                if 0 <= ni < N and 0 <= nj < N and grid[ni][nj] == 0:
                    if dist[ni][nj][used + 1] == -1:
                        dist[ni][nj][used + 1] = dist[ci][cj][used] + 1
                        q.append((ni, nj, used + 1))

    return -1  # 도달 불가

ans = bfs(0, 0)
print(ans)
```

이렇게 고치면

- 시간복잡도: `O(N^2 * MAX_K)` (MAX_K = 3이므로 사실상 `O(N^2)`)
- 메모리: `O(N^2 * MAX_K)` 도 충분히 여유 있습니다.

샘플 입력으로도

```text
0 0 0 1 0
0 0 0 1 0
0 0 1 1 0
0 1 0 0 0
0 0 0 0 0
```

를 넣으면 `5`가 잘 나와요.

---

## 4. 이런 문제를 풀 때 생각 순서 요약

앞으로 비슷한 문제 볼 때는 이렇게 생각해 보면 좋아요.

1. **기본형이 뭐냐?**  
   → 격자 최단거리 → BFS

2. **추가 제약은 뭔가?**  
   → “특별한 이동을 K번까지 쓸 수 있다”  
   → “말 이동, 대각선, 점프, 텔레포트…” 이런 건 다 비슷한 패턴

3. **상태에 어떤 차원을 더해야 하나?**  
   → “지금까지 특별 이동을 몇 번 썼는지” (`k`)

4. **방문/거리 배열도 그 차원을 포함하게 만들기**  
   → `visited[i][j][k]` / `dist[i][j][k]`

5. **큐에는 항상 (좌표 + 상태) 를 같이 넣기**  
   → `(i, j, k)`

이 패턴만 익혀두면, 나중에
- “말처럼 뛰기 K번, 평소엔 상하좌우”
- “벽 부수기 최대 1번”
- “점프는 하루에 한 번만”

같은 문제들 전부 같은 구조로 풀 수 있어요.

---
