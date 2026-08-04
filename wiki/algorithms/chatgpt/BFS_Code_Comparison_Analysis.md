---
type: Concept
title: "BFS Code Comparison Analysis"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-12-08)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-12-08
status: active
---

# BFS Code Comparison Analysis

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-12-08

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
from collections import deque

def bfs() :
    q = deque()
    q.append((0, 0, 0))
    v = [[[0] * 2 for _ in range(M)] for _ in range(N)]
    v[0][0][0] = 1

    while q :
        ci, cj, br = q.popleft()

        if (ci, cj) == (N-1, M-1) :
            return v[ci][cj][br]

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)) :
            ni, nj = ci + di, cj + dj
            if 0 <= ni < N and 0 <= nj < M and v[ni][nj][br] == 0 :
                if board[ni][nj] == 0 :
                    v[ni][nj][br] = v[ci][cj][br] + 1
                    q.append((ni, nj, br))
                elif board[ni][nj] == 1 and br == 0 :
                    v[ni][nj][1] = v[ci][cj][0] + 1
                    q.append((ni, nj, 1))

    return -1
```

```
from collections import deque

def bfs() :
    v = [[[-1] * 2 for _ in range(M)] for _ in range(N)]
    q = deque()
    q.append((0, 0, 0))
    v[0][0][0] = 1

    while q :
        ci, cj, broken = q.popleft()

        if (ci, cj) == (N-1, M-1) :
            return v

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)) :
            ni, nj = ci + di, cj + dj
            if 0 <= ni < N and 0 <= nj < M and v[ni][nj][broken] == 0:
                if maps[ni][nj] == 0  :
                    v[ni][nj][broken] = v[ci][cj][broken] + 1
                    q.append((ni, nj, broken))

                elif maps[ni][nj] == 1 and broken == 0 :
                    v[ni][nj][1] = v[ci][cj][0] + 1
                    q.append((ni, nj, 1))

    return -1
```
bfs 첫 번째 코드와 두번째 코드간의 차이를 알려줘.

### 💡 답변 (Assistant)
두 코드 모두 BFS(너비 우선 탐색)를 활용하여 벽을 하나까지 부수고 최단 경로를 탐색하는 문제를 해결하려는 목적을 가지고 있지만, 구현상의 차이점이 있습니다. 주요 차이점을 정리하겠습니다.

---

### 1. **초기화 및 방문 처리 방식**
#### 첫 번째 코드:
- 방문 배열 `v`를 `[[[0] * 2 for _ in range(M)] for _ in range(N)]`로 초기화.  
  방문하지 않은 상태는 `0`으로 표현.
- 시작점 `(0, 0, 0)`은 `v[0][0][0] = 1`로 설정하며, 거리를 직접 나타냄.
- 방문 여부를 통해 동시에 이동 거리를 확인 가능.

#### 두 번째 코드:
- 방문 배열 `v`를 `[[[-1] * 2 for _ in range(M)] for _ in range(N)]`로 초기화.  
  방문하지 않은 상태는 `-1`로 표현.
- 시작점 `(0, 0, 0)`은 `v[0][0][0] = 1`로 설정하며, 이동 거리를 저장.
- `-1`을 사용하여 방문 여부와 거리를 구분.

---

### 2. **리턴 값**
#### 첫 번째 코드:
- 목적지 `(N-1, M-1)`에 도달하면 `return v[ci][cj][br]`로 방문 배열에서 최단 거리를 반환.
- 도달하지 못하면 `-1` 반환.

#### 두 번째 코드:
- 목적지 `(N-1, M-1)`에 도달하면 방문 배열 `v` 전체를 반환.
- 도달하지 못하면 `-1` 반환.
- 그러나 반환된 `v`는 문제의 정답으로 적합하지 않음(의도된 동작인지 확인 필요).

---

### 3. **방문 조건**
#### 첫 번째 코드:
- 방문 배열의 조건을 `v[ni][nj][br] == 0`으로 확인.
- 방문하지 않은 상태(`0`)에서만 다음 좌표를 큐에 추가.

#### 두 번째 코드:
- 방문 배열의 조건을 `v[ni][nj][broken] == 0`으로 확인.
- 하지만 초기화 시 방문하지 않은 상태를 `-1`로 설정했으므로, 조건이 의도대로 작동하지 않음.
  - `v[ni][nj][broken] == 0` 조건은 항상 `False`가 되어 이동이 제한됨.

---

### 4. **변수 이름**
#### 첫 번째 코드:
- 벽을 부쉈는지 여부를 `br`로 간결하게 명명.
- 전체적으로 코드가 간결하며, 직관적으로 변수 이름 설정.

#### 두 번째 코드:
- 벽을 부쉈는지 여부를 `broken`으로 명명.
- 직관적이지만 첫 번째 코드에 비해 약간 더 길음.

---

### 5. **로직 동작 가능 여부**
#### 첫 번째 코드:
- 올바르게 동작하며 최단 경로를 정확히 계산.

#### 두 번째 코드:
- `v` 초기값이 `-1`인데 방문 조건에서 `v[ni][nj][broken] == 0`을 사용하여 의도한 동작을 수행하지 못함.
- 초기값이나 조건 수정이 필요.

---

### 결론
- 첫 번째 코드는 올바르게 작동하며, BFS로 최단 경로를 계산.
- 두 번째 코드는 초기화와 방문 조건에 논리적 오류가 있어 수정이 필요. `v`의 초기값을 `0`으로 설정하거나 조건을 `v[ni][nj][broken] == -1`로 변경해야 올바르게 작동할 것으로 보임.

---
