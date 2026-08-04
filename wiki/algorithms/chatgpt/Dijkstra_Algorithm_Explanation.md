---
type: Concept
title: "Dijkstra Algorithm Explanation"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-12-03)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-12-03
status: active
---

# Dijkstra Algorithm Explanation

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-12-03

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
import heapq

def dijkstra(graph, start) :
    distances = {node : float('inf') for node in range(1, len(graph) + 1)}
    distances[start] = 0
    q = []
    heapq.heappush(q, (distances[start], start))

    while q:
        current_distance, current_node = heapq.heappop(q)

        if distances[current_node] < current_distance :
            continue

        for adj, weight in graph[current_node].items() :
            distance = current_distance + weight

            if distance < distances[adj] :
                distances[adj] = distance
                heapq.heappush(q, (distance, adj))

    return distances

# N : 학생 수, M : 도로 수, X : 모여서 놀 집
N, M, X = map(int, input().split())

go_graph = {node : {} for node in range(1, N + 1)}
back_graph = {node : {} for node in range(1, N + 1)}

for _ in range(M) :
    A, B, T = map(int, input().split())
    go_graph[A][B] = T
    back_graph[B][A] = T

to_x = dijkstra(go_graph, X)
from_x = dijkstra(back_graph, X)

ans = 0
for i in range(1, N + 1) :
    ans = max(ans, to_x[i] + from_x[i])

print(ans)
```
이 코드를 보고 해설을 해줘

### 💡 답변 (Assistant)
이 코드는 학생들이 X번 집에서 모여서 놀 때, 각 학생이 이동하는 데 걸리는 시간 중 최댓값을 구하는 프로그램입니다. 이를 통해 전체 학생 중 가장 먼 학생이 집으로 이동하는 데 필요한 시간을 계산합니다.

### **코드 구조 및 해설**

#### **1. Dijkstra 알고리즘 구현**
```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in range(1, len(graph) + 1)}
    distances[start] = 0
    q = []
    heapq.heappush(q, (distances[start], start))

    while q:
        current_distance, current_node = heapq.heappop(q)

        if distances[current_node] < current_distance:
            continue

        for adj, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[adj]:
                distances[adj] = distance
                heapq.heappush(q, (distance, adj))

    return distances
```
- **목적:** Dijkstra 알고리즘을 사용하여 주어진 시작 노드에서 다른 노드까지의 최단 거리를 계산합니다.
- **매개변수:**
  - `graph`: 그래프를 딕셔너리로 표현한 자료구조.
  - `start`: 시작 노드 번호.
- **동작:**
  - `distances`는 시작 노드에서 각 노드까지의 최단 거리를 저장합니다. 초기에는 모두 `inf`로 설정하고, 시작 노드는 0으로 초기화합니다.
  - 우선순위 큐 `q`를 사용하여 탐색할 노드를 관리합니다.
  - `heapq.heappop`으로 가장 짧은 거리를 가진 노드를 꺼내 현재 노드로 설정합니다.
  - 현재 노드의 인접 노드들에 대해 거리를 계산하고, 더 짧은 경로가 발견되면 업데이트 후 큐에 추가합니다.
- **결과:** 시작 노드에서 모든 노드까지의 최단 거리를 딕셔너리로 반환합니다.

---

#### **2. 입력 처리 및 그래프 생성**
```python
N, M, X = map(int, input().split())

go_graph = {node: {} for node in range(1, N + 1)}
back_graph = {node: {} for node in range(1, N + 1)}

for _ in range(M):
    A, B, T = map(int, input().split())
    go_graph[A][B] = T
    back_graph[B][A] = T
```
- **입력:** 
  - `N`: 학생 수 (노드 개수).
  - `M`: 도로 수 (엣지 개수).
  - `X`: 학생들이 모일 집의 번호.
- **그래프 생성:**
  - `go_graph`: 출발점에서 목적지로 향하는 단방향 그래프.
  - `back_graph`: 목적지에서 출발점으로 향하는 단방향 그래프 (역방향).
  - 각 도로의 정보를 읽어서 그래프를 구성합니다. `(A, B, T)`는 A에서 B로 가는 데 걸리는 시간이 `T`임을 나타냅니다.

---

#### **3. 다익스트라로 거리 계산**
```python
to_x = dijkstra(go_graph, X)
from_x = dijkstra(back_graph, X)
```
- `to_x`: 모든 노드에서 X번 집으로 가는 최단 거리를 계산.
- `from_x`: X번 집에서 모든 노드로 가는 최단 거리를 계산.

---

#### **4. 왕복 시간 계산 및 결과 출력**
```python
ans = 0
for i in range(1, N + 1):
    ans = max(ans, to_x[i] + from_x[i])

print(ans)
```
- 각 학생이 X번 집까지 왕복하는 데 걸리는 시간은 `to_x[i] + from_x[i]`로 계산됩니다.
- 모든 학생의 왕복 시간 중 최댓값을 `ans`에 저장합니다.
- 최종적으로, X번 집까지 왕복하는 데 걸리는 최대 시간을 출력합니다.

---

### **예제**
#### **입력**
```
4 8 2
1 2 4
1 3 2
1 4 7
2 3 1
2 4 5
3 4 4
4 2 3
4 3 6
```
- 학생 수: 4명, 도로 수: 8개, 모일 집 번호: 2번.
- 도로 정보는 `A, B, T`로 주어짐.

#### **출력**
```
10
```
- 각 학생의 왕복 시간: 
  - 1번 학생: `4 (1→2) + 6 (2→1) = 10`
  - 2번 학생: `0 (2→2) + 0 (2→2) = 0`
  - 3번 학생: `1 (3→2) + 6 (2→3) = 7`
  - 4번 학생: `3 (4→2) + 7 (2→4) = 10`
- 최댓값은 10이므로 출력은 `10`입니다.

---

### **전체 요약**
이 코드는 다익스트라 알고리즘을 이용하여 특정 집으로 가는 왕복 시간을 계산하고, 그 중 최대 왕복 시간을 출력하는 프로그램입니다. 그래프의 방향성과 비용 정보를 정확히 고려하며, 우선순위 큐를 활용해 효율적으로 최단 경로를 계산합니다.

---
