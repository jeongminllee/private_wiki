---
type: Concept
title: "DFS를 이용한 계산"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-04-28)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-04-28
status: active
---

# DFS를 이용한 계산

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-04-28

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
이 코드는 LeetCode “Evaluate Division” 문제(주어진 변수 간의 비율을 계산하는 문제)를 DFS(깊이 우선 탐색)로 푼 한 가지 구현 예입니다. 크게 두 부분으로 나뉩니다.

---

## 1. 그래프(인접 리스트) 구성 부분 (`calcEquation` 내부)

```python
dct = {}
for i in range(len(values)):
    d1, d2 = equations[i]
    v = values[i]

    # d1 → d2 간 비율 저장
    if d1 not in dct:
        dct[d1] = {}
    dct[d1][d2] = v
    dct[d1][d1] = 1  # 자기 자신으로의 비율은 1

    # d2 → d1 간 역비율 저장
    if d2 not in dct:
        dct[d2] = {}
    dct[d2][d1] = 1 / v
    dct[d2][d2] = 1
```

- `dct`는 변수(문자열)를 key 로, 그 변수에서 갈 수 있는 다른 변수들과의 비율(실수)을 value 로 갖는 중첩 딕셔너리입니다.
- 예를 들어 `["a","b"], 2.0` 이 주어지면  
  - `dct["a"]["b"] = 2.0`  
  - `dct["b"]["a"] = 0.5`  
  - 그리고 자기 자신으로의 경로(`dct[x][x] = 1`)도 미리 넣어 둡니다.  
- 이렇게 하면 그래프 상에서 “가중치 있는 양방향 간선”을 구성하게 됩니다.

---

## 2. 쿼리 처리 및 DFS 탐색

```python
res = []
for q1, q2 in queries:
    if q1 not in dct:
        res.append(-1)  # q1 자체가 그래프에 없으면 -1 반환
        continue

    rtn = self.dfs(dct, q1, q2, 1, [])
    res.append(rtn)
return res
```

- 각 쿼리 `(q1, q2)`에 대해, 출발 노드 `q1`가 그래프에 없으면 바로 `-1` 을, 있으면 `dfs` 호출로 비율을 계산합니다.

```python
def dfs(self, dct, bgn, end, v, visited):
    for mid in dct[bgn]:
        if mid not in visited:
            if mid == end:
                return v * dct[bgn][mid]
            else:
                rtn = self.dfs(dct, mid, end, v * dct[bgn][mid], visited + [bgn])
                if rtn != -1:
                    return rtn
    return -1
```

- `bgn`에서 출발해 `end`를 찾을 때까지 재귀적으로 이웃 노드를 타고 들어갑니다.
- 매 단계마다 현재까지 곱해진 비율 `v`를 넘기고, 방문한 노드 목록 `visited` 로 사이클을 방지합니다.
- 만약 이웃 노드 `mid` 가 목표 노드 `end` 면, 현재까지 곱해진 값에 `dct[bgn][mid]` 을 곱해 결과를 반환합니다.
- 그렇지 않다면 `mid` 를 새 출발점으로 재귀 호출하며, 깊이 탐색 중 하나라도 `-1` 이 아닌 값을 돌려주면 그 값을 곧바로 반환합니다.
- 모든 경로를 다 뒤졌는데 목표를 찾지 못하면 `-1` 을 반환합니다.

---

## 시간·공간 복잡도

- **그래프 구성**: `O(E)` (E = 방정식 수)  
- **쿼리당 DFS 탐색**: 최악의 경우 그래프의 모든 간선을 탐색하므로 `O(E)`  
- **전체**: `O(E + Q·E)`, 여기서 `Q` 는 쿼리 수

---

## 개선할 수 있는 점

1. **방문 처리 최적화**  
   - `visited + [bgn]` 처럼 매 재귀마다 리스트를 복사하지 않고, 함수 진입 시 `visited.add(bgn)` / 탈출 시 `visited.remove(bgn)` 방식으로 처리하면 메모리·속도 면에서 더 효율적입니다.

2. **양쪽 쿼리 존재 여부 사전 검사**  
   - 현재는 `q1` 만 체크하지만, `q2` 도 그래프에 없으면 즉시 `-1` 을 반환하도록 초기 검사할 수 있습니다.

3. **Union-Find(분리 집합) 활용**  
   - DFS 대신 Union-Find 자료구조에 비율 관계를 함께 저장해 두면, 쿼리마다 경로를 찾기보다 상위 집합(root) 간의 비율을 바로 계산할 수 있어 훨씬 빠릅니다.

4. **딕셔너리 초기화 정리**  
   - 자기 자신으로 가는 간선(`dct[x][x] = 1`)은 노드가 처음 등장할 때 한 번만 넣도록 바꾸면 중복 삽입을 방지할 수 있습니다.

---

이 코드가 “a/b = k” 형태의 방정식을 그래프로 보고, DFS로 쿼리한 두 변수 사이의 비율을 찾아내는 전형적인 풀이 방식임을 이해하시면 됩니다. 궁금한 점이나 다른 구현 방법(예: Union-Find) 등에 대해 더 알고 싶으시면 말씀해 주세요!

---

### ❓ 질문 (User)
```
class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        dct = {}

        for i in range(len(values)) :
            d1, d2 = equations[i]
            v = values[i]

            if d1 not in dct :
                dct[d1] = {}

            dct[d1][d2] = v
            dct[d1][d1] = 1

            if d2 not in dct :
                dct[d2] = {}
            
            dct[d2][d1] = 1 / v
            dct[d2][d2] = 1

        res = []

        for q1, q2 in queries :
            if q1 not in dct :
                res.append(-1)
                continue
            
            rtn = self.dfs(dct, q1, q2, 1, [])
            res.append(rtn)

        return res
    
    def dfs(self, dct, bgn, end, v, visited) :
        for mid in dct[bgn] :
            if mid not in visited :
                if mid == end :
                    v *= dct[bgn][mid]
                    return v
                else :
                    rtn = self.dfs(dct, mid, end, v * dct[bgn][mid], visited + [bgn])
                    if rtn != -1 :
                        return rtn
        return -1
```
이 코드를 분석해줘
