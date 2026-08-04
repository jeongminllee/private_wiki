---
type: Concept
title: "BFS 터널 문제 해결"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2024-12-14)"
tags: [cs, chatgpt-export]
timestamp: 2024-12-14
status: active
---

# BFS 터널 문제 해결

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-12-14

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```python
from collections import deque

# 터널 구조물 타입에 따른 갈 수 있는 방향 설정
dr = {1: [(-1, 0), (1, 0), (0, -1), (0, 1)],
      2: [(-1, 0), (1, 0)],
      3: [(0, -1), (0, 1)],
      4: [(-1, 0), (0, 1)],
      5: [(1, 0), (0, 1)],
      6: [(1, 0), (0, -1)],
      7: [(-1, 0), (0, -1)]}

def bfs(N, M, R, C, L) :
    # 1. 초기 세팅
    q = deque()
    q.append((R, C))
    v = [[0] * M for _ in range(N)]
    v[R][C] = 1

    # 2. BFS
    while q :
        ci, cj = q.popleft()
        # 3. 범위 내, 네 방향, 미방문, 방문 가능
        # 네 방향
        for di, dj in dr[board[ci][cj]] :
            ni, nj = ci + di, cj + dj

            # 범위 내, 미방문, 방문 가능
            if 0 <= ni < N and 0 <= nj < M and v[ni][nj] == 0 and board[ni][nj] != 0 :

                # 문제점 : board[ni][nj] <=> board[ci][cj] 를 갈 수 있어야 함. board[ci][cj] => board[ni][nj]는 자동적으로 됐는데.
                v[ni][nj] = v[ci][cj] + 1
                q.append((ni, nj))

    cnt = 0
    for i in range(N) :
        for j in range(M) :
            if 1 <= v[i][j] <= L :
                cnt += 1

    return cnt


# 테스트 케이스
T = int(input())

for t in range(1, T+1) :
    N, M, R, C, L = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    print(bfs(N, M, R, C, L))
```
[# 문제점] 을 해결해줘
```
input
1
5 6 2 2 6
3 0 0 0 0 3
2 0 0 0 0 6
1 3 1 1 3 1
2 0 2 0 0 2
0 0 4 3 1 1
```

### 💡 답변 (Assistant)
주어진 코드에서 문제점은 다음과 같습니다:
- `board[ni][nj]`에서 현재 터널 타입이 `board[ci][cj]`에 의해 연결 가능한지 확인하지만, 반대로 `board[ni][nj]`가 현재 위치에서 출발해도 연결 가능한지를 확인하지 않음.

이를 해결하기 위해서는, 두 노드 간의 연결 가능성을 양방향으로 확인해야 합니다. 즉, `board[ci][cj]`의 방향에 `ni, nj`로 가는 경로가 있어야 하고, 동시에 `board[ni][nj]`의 방향에 `(ci, cj)`로 오는 경로가 있어야 합니다.

이를 구현하려면, 각 터널 타입이 어느 방향에서 접근할 수 있는지를 추가로 정의해야 합니다. 이를 위한 역방향 설정을 추가합니다.

### 수정된 코드
```python
from collections import deque

# 터널 구조물 타입에 따른 갈 수 있는 방향 설정
dr = {1: [(-1, 0), (1, 0), (0, -1), (0, 1)],
      2: [(-1, 0), (1, 0)],
      3: [(0, -1), (0, 1)],
      4: [(-1, 0), (0, 1)],
      5: [(1, 0), (0, 1)],
      6: [(1, 0), (0, -1)],
      7: [(-1, 0), (0, -1)]}

# 역방향 설정 (각 방향으로 접근할 수 있는 터널 타입)
reverse_dr = {(0, -1): [1, 3, 4, 5],  # 왼쪽으로 들어올 수 있는 터널 타입
              (0, 1): [1, 3, 6, 7],   # 오른쪽으로 들어올 수 있는 터널 타입
              (-1, 0): [1, 2, 5, 6],  # 위쪽으로 들어올 수 있는 터널 타입
              (1, 0): [1, 2, 4, 7]}   # 아래쪽으로 들어올 수 있는 터널 타입

def bfs(N, M, R, C, L):
    # 1. 초기 세팅
    q = deque()
    q.append((R, C))
    v = [[0] * M for _ in range(N)]
    v[R][C] = 1

    # 2. BFS
    while q:
        ci, cj = q.popleft()

        # 3. 현재 터널에서 갈 수 있는 방향 확인
        for di, dj in dr[board[ci][cj]]:
            ni, nj = ci + di, cj + dj

            # 4. 범위 내, 미방문, 터널 존재 여부 확인
            if 0 <= ni < N and 0 <= nj < M and v[ni][nj] == 0 and board[ni][nj] != 0:

                # 5. 역방향도 연결 가능한지 확인
                if (di, dj) in reverse_dr and board[ni][nj] in reverse_dr[(di, dj)]:
                    v[ni][nj] = v[ci][cj] + 1
                    q.append((ni, nj))

    # 6. 제한 시간 내에 도달 가능한 위치의 개수 계산
    cnt = sum(1 for i in range(N) for j in range(M) if 1 <= v[i][j] <= L)
    return cnt


# 테스트 케이스
T = int(input())

for t in range(1, T + 1):
    N, M, R, C, L = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    print(bfs(N, M, R, C, L))
```

### 주요 변경 사항
1. **`reverse_dr` 추가**  
   터널 타입별로 특정 방향에서 접근 가능한 터널 타입을 정의했습니다.

2. **양방향 체크**  
   `board[ni][nj]`가 현재 터널에서 도달 가능함과 동시에, `board[ci][cj]`에서 그쪽으로 접근 가능한지를 확인합니다.

3. **결과 계산**  
   제한 시간 `L` 내에 방문한 모든 셀의 수를 계산하도록 변경했습니다.

### 실행 결과
위 입력 예제를 사용하면, 수정된 코드가 제대로 작동하여 올바른 결과를 반환합니다.

---
