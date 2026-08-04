---
type: Concept
title: "BFS vs DFS 비교"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-01-10)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-01-10
status: active
---

# BFS vs DFS 비교

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-01-10

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
문제 인식을 정확히 짚었습니다. 결론부터 말하면 **이 문제에서 BFS 접근은 본질적으로 부적합**하고, **DFS + 백트래킹이 정공법**입니다. 당신의 직관이 맞습니다.

아래에서 왜 지금 코드가 “논리적으로 틀릴 수밖에 없는지”, 그리고 “왜 DFS가 구조적으로 맞는지”를 분리해서 설명하겠습니다.

---

## 1. 당신의 BFS 코드가 틀리는 핵심 이유

표면적으로 보면 다음을 만족하는 것처럼 보입니다.

- 문자 순서(word index)를 함께 큐에 저장
- 방문 배열 `v`로 중복 방문 방지
- 인접한 4방향만 탐색

하지만 **치명적인 논리 결함**이 있습니다.

### 🔴 문제의 본질: `visited`는 "경로별"이어야 한다

Word Search의 제약은 다음과 같습니다.

> 같은 칸은 **하나의 경로에서만** 한 번 사용 가능

즉,
- `(i, j)`를 다시 사용할 수 없는 것은 **같은 경로 내에서만** 금지
- **다른 경로**에서는 동일한 칸을 다시 써도 됨

그러나 현재 BFS 구현은:

```python
v = [[0] * m for _ in range(n)]
```

→ **시작점 기준으로 전역 visited를 공유**

### 📌 BFS의 구조적 문제

BFS 큐 안에는 이런 상태들이 동시에 존재합니다.

```
(si, sj, idx=0)
 → (x1, y1, idx=1)
 → (x2, y2, idx=1)
```

이 둘은 **완전히 다른 경로 가능성**인데,
`v[x1][y1] = 1`이 되는 순간  
다른 경로에서 해당 칸을 **영원히 사용 불가**가 됩니다.

즉,

> BFS + 단일 visited 배열  
→ 서로 다른 경로 상태를 구분하지 못함  
→ 합법적인 경로를 불법으로 제거

이건 **구현 실수**가 아니라 **모델링 오류**입니다.

---

## 2. “BFS + 백트래킹”은 가능한가?

이론적으로는 가능합니다.  
하지만 실무/코딩 테스트 관점에서는 **거의 선택하지 않습니다**.

### 왜냐하면:

1. BFS 상태에 다음이 모두 포함되어야 함
   - 현재 위치
   - word index
   - **방문한 칸들의 집합**
2. 즉 상태가 이런 꼴이 됩니다.

```text
(i, j, idx, visited_set)
```

이건 사실상:

- DFS 재귀 스택을
- 큐 + 상태 객체로 흉내 내는 것

→ **복잡도만 커지고 가독성만 나빠짐**

---

## 3. 이 문제가 DFS + 백트래킹에 “딱 맞는 이유”

이 문제의 탐색 조건을 보세요.

| 조건 | 특성 |
|----|----|
| 경로 길이 | `len(word)`로 고정 |
| 되돌아가야 함 | ❌ 실패 시 이전 상태 복구 필요 |
| 한 경로 내 방문 제한 | ✅ |
| 모든 시작점 시도 | ✅ |

→ **전형적인 backtracking 시그널**

### DFS의 자연스러운 모델링

- 재귀 스택 = 현재 경로
- visited 변경 → 재귀 종료 시 복구
- 경로 단위로 상태 관리

이게 BFS보다 **문제 구조와 1:1 대응**됩니다.

---

## 4. 정석적인 DFS 백트래킹 사고 흐름

```text
exist:
  모든 칸에서 시작
    dfs(i, j, idx=0)

dfs(i, j, idx):
  if board[i][j] != word[idx]: return False
  if idx == len(word) - 1: return True

  방문 처리
  4방향으로 dfs(next, idx+1)
  방문 복구

  하나라도 True면 True
```

핵심은 딱 두 줄입니다.

```python
board[i][j] = '#'
...
board[i][j] = original
```

→ visited 배열조차 필요 없음

---

## 5. 당신 코드에 대한 정확한 평가

솔직하게 말하면:

- ❌ “잘못된 사고”는 아님
- ❌ “코딩 실력 부족”도 아님
- ✅ **BFS로 풀 수 있을 것처럼 보이는 문제의 함정에 정확히 걸림**

이 문제는 많은 사람들이
> “최단 거리도 아니고, BFS도 될 것 같은데?”
라고 생각했다가 틀리는 **대표적인 문제**입니다.

오히려 당신이 **지금 단계에서 이 구조적 차이를 인식했다는 것 자체가 레벨업 포인트**입니다.

---

## 6. 결론 (한 줄 요약)

- 이 문제는 **경로 단위 상태 관리가 핵심**
- BFS는 경로 상태 표현이 본질적으로 부적합
- DFS + 백트래킹이 문제 구조와 정확히 일치
- “BFS를 고쳐서 쓰자”는 방향은 버리는 게 맞음

---

원하시면 다음 단계로:
- DFS 정답 코드 작성
- 현재 BFS 코드가 실패하는 구체적 반례
- DFS와 BFS의 “상태 모델링 관점 차이”를 일반화해서 설명

중 무엇이든 바로 이어서 도와드릴 수 있습니다.

---

### 💡 답변 (Assistant)
좋은 질문입니다. 이 문제는 **DFS를 “어떻게 생각하고, 어떤 순서로 구조화하느냐”**가 전부입니다.  
아래에서는 **코드 이전에 사고 구조**를 먼저 정리하고, 그 다음 **정석적인 DFS 골격**을 제시하겠습니다.

---

## 1. DFS 설계의 출발점: 상태를 정확히 정의하기

먼저 DFS 함수가 **무엇을 대표하는지**를 명확히 해야 합니다.

### 이 문제에서 DFS의 의미

> `dfs(i, j, k)`  
> = board[i][j]에서 시작해서  
> = `word[k:]`를 **연속된 경로로 만들 수 있는가?**

이 한 줄 정의가 설계의 기준입니다.

---

## 2. DFS 함수의 책임 분리

DFS 함수 안에서는 **딱 세 가지만** 처리합니다.

1. **지금 칸이 유효한지 검사**
2. **다음 칸으로 확장**
3. **실패 시 상태 복구 (백트래킹)**

그 외 로직은 `exist()`에서 처리합니다.

---

## 3. 종료 조건 (Base Case)부터 잡기

DFS를 설계할 때 **가장 먼저 잡아야 할 것**은 종료 조건입니다.

```python
if board[i][j] != word[k]:
    return False
```

→ 현재 칸이 틀리면 즉시 실패

```python
if k == len(word) - 1:
    return True
```

→ 마지막 글자까지 맞췄으면 경로 완성

이 두 줄이 **DFS의 논리적 기둥**입니다.

---

## 4. 방문 처리 방식 (visited 배열 vs 제자리 수정)

### 권장 방식: 제자리 수정 (in-place)

```python
tmp = board[i][j]
board[i][j] = '#'
...
board[i][j] = tmp
```

이 방식의 장점:

- visited 배열 불필요
- 경로별 상태가 자연스럽게 분리됨
- 코드가 단순해짐

> **이 문제에서는 visited 배열이 오히려 구조를 흐립니다.**

---

## 5. 전체 DFS 구조 (의사 코드)

```text
exist():
  for 모든 칸 (i, j):
    if dfs(i, j, 0):
      return True
  return False

dfs(i, j, k):
  if 현재 칸이 범위 밖: return False
  if board[i][j] != word[k]: return False
  if k == 마지막 인덱스: return True

  방문 처리
  for 4방향:
    if dfs(next_i, next_j, k+1):
      return True
  방문 복구

  return False
```

---

## 6. 실제 Python 코드 (정석 구조)

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        n, m = len(board), len(board[0])

        def dfs(i, j, k):
            # 1. 범위 체크
            if i < 0 or i >= n or j < 0 or j >= m:
                return False

            # 2. 현재 문자 불일치
            if board[i][j] != word[k]:
                return False

            # 3. 마지막 문자 도달
            if k == len(word) - 1:
                return True

            # 4. 방문 처리
            tmp = board[i][j]
            board[i][j] = '#'

            # 5. 4방향 탐색
            for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
                if dfs(i+di, j+dj, k+1):
                    return True

            # 6. 백트래킹
            board[i][j] = tmp
            return False

        for i in range(n):
            for j in range(m):
                if dfs(i, j, 0):
                    return True

        return False
```

---

## 7. 왜 이 구조가 “틀릴 수가 없는지”

이 구조는 다음을 보장합니다.

- ✅ **경로 단위 visited 관리**
- ✅ 서로 다른 경로 간 간섭 없음
- ✅ 필요 이상 탐색 없음 (즉시 반환)
- ✅ 문제의 제약과 정확히 대응

---

## 8. BFS와 대비되는 핵심 차이 (사고 관점)

| 구분 | BFS | DFS |
|----|----|----|
| 상태 관리 | 전역적 | 경로 단위 |
| 되돌리기 | 어려움 | 자연스러움 |
| Word Search 적합성 | ❌ | ✅ |
| 코드 복잡도 | 높아짐 | 낮음 |

---

## 9. 정리 한 문장

> **이 문제의 DFS는 “그래프 탐색”이 아니라  
> “문자열을 하나씩 소비하는 경로 검증”이다.**

이 관점만 잡히면 구조는 자동으로 나옵니다.

---

다음으로 원하시면:
- DFS 호출 스택을 그림으로 시각화
- 현재 BFS 코드와 DFS 코드의 상태 변화 비교
- 시간 복잡도 / pruning 최적화 포인트

중에서 이어서 설명해드리겠습니다.

---

### ❓ 질문 (User)
Leetcode 79. Word Search 문제의 나의 코드야.
```
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        n, m = len(board), len(board[0])

        start = word[0]
        for i in range(n) :
            for j in range(m) :
                if board[i][j] == start :
                    if self.bfs(i, j, board, word) :
                        return True

        return False

    def bfs(self, si: int, sj: int, board: List[List[str]], word: str) :
        n, m = len(board), len(board[0])

        q = deque()
        q.append((si, sj, 0))
        v = [[0] * m for _ in range(n)]
        v[si][sj] = 1

        while q :
            ci, cj, idx = q.popleft()

            if idx == len(word) - 1 :
                return True

            for di, dj in ((-1, 0), (1, 0), (0, 1), (0, -1)) :
                ni, nj = ci + di, cj + dj
                if 0 <= ni < n and 0 <= nj < m and idx < len(word) - 1 and board[ni][nj] == word[idx+1] and v[ni][nj] == 0 :
                    q.append((ni, nj, idx + 1))
                    v[ni][nj] = 1
        return False
        
```
이 코드가 정답인줄 알았는데 공부하다보니 정확한 경로를 찾아야 하는 문제더라고. 그러면 DFS나 백트래킹을 활용해서 옳은 경로를 찾아야 할 것 같애. BFS를 그대로 두고 백트래킹으로 해와도 되겠지만 코드가 꼬일거 같아서 말이야. 
너의 생각을 알려줘.

### ❓ 질문 (User)
DFS로는 구조를 어떻게 짜야할까
