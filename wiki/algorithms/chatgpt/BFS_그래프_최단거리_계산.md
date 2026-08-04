---
type: Concept
title: "BFS 그래프 최단거리 계산"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-02-03)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-02-03
status: active
---

# BFS 그래프 최단거리 계산

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-02-03

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
from collections import deque

def bfs(s) :
    q = deque()
    q.append(s)

    visited = [-1] * (n + 1)
    visited[s] = 0

    while q :
        c = q.popleft()
        for nxt in edges[c] :
            if visited[nxt] == -1 :
                q.append(nxt)
                visited[nxt] = visited[c] + 1

    return visited[1:]

n, m = map(int, input().split())
edges = [[] for _ in range(n + 1)]

for _ in range(m) :
    a, b = map(int, input().split())
    edges[a].append(b)
    edges[b].append(a)

t = int(input())
distances = [-1] * (n + 1)
distances[1] = 0

for _ in range(t) :
    a, b = map(int, input().split())
    edges[a].append(b)
    edges[b].append(a)
    res = bfs(1)
    print(*res)
```
코드 분석해줘

### 💡 답변 (Assistant)
이 코드는 **BFS(너비 우선 탐색)** 을 활용하여 그래프에서 특정 노드로부터 다른 노드들까지의 최단 거리를 계산하는 프로그램이다.  

### **📌 코드 분석**
1. **BFS 함수 정의 (`bfs(s)`)**
   - `bfs(s)` 함수는 시작점 `s`로부터 모든 노드까지의 최단 거리를 계산한다.
   - `deque`를 사용해 BFS를 수행하고, `visited` 리스트를 활용해 방문 여부 및 거리를 저장한다.
   - BFS 탐색을 하면서 각 노드까지의 거리를 `visited` 리스트에 기록한다.
   - 탐색이 끝나면 **노드 1부터 n까지의 거리 리스트를 반환**한다.

2. **그래프 초기화**
   - `n, m = map(int, input().split())`
     - `n`: 노드(정점) 개수
     - `m`: 간선 개수
   - `edges = [[] for _ in range(n + 1)]`
     - 각 노드에 연결된 노드 리스트를 저장하기 위한 **인접 리스트** 초기화
   - `for _ in range(m):`
     - `a, b = map(int, input().split())`
     - `a`와 `b`가 연결된 **양방향 그래프**(무방향 그래프)이므로, `edges[a]`, `edges[b]` 모두에 추가

3. **거리 리스트 초기화**
   - `distances = [-1] * (n + 1)`
     - 모든 노드의 초기 거리를 -1로 설정 (방문하지 않았음을 의미)
   - `distances[1] = 0`
     - 시작점(1번 노드)은 자기 자신까지의 거리가 0

4. **실시간 간선 추가 및 BFS 수행**
   - `t = int(input())`
     - 새로운 간선을 추가할 횟수 `t` 입력 받음
   - `for _ in range(t):`
     - `a, b = map(int, input().split())`
     - `(a, b)` 간선을 추가하고 BFS 재실행
     - `bfs(1)`을 호출해 **1번 노드에서 모든 노드까지의 거리**를 다시 계산하고 출력

---

### **📌 코드 실행 흐름**
1. 그래프의 기본 구조를 입력받고, 초기 간선들을 저장한다.
2. 이후 새로운 간선을 추가할 때마다 `bfs(1)`을 호출하여 거리 정보를 갱신한다.
3. 갱신된 거리 정보를 출력한다.

---

### **📌 시간 복잡도 분석**
- BFS 탐색 자체는 `O(n + m)` (노드 개수 + 간선 개수)
- 새로운 간선이 추가될 때마다 `bfs(1)`을 다시 실행하므로, 최악의 경우 `O(t(n + m))`이 된다.
- `t`가 크다면 **매번 BFS를 수행하는 것은 비효율적**이며, 더 효율적인 방식(예: 다익스트라, 동적 업데이트)이 필요할 수 있음.

---

### **📌 개선점**
1. **BFS 매번 실행 최적화**
   - 새로운 간선이 추가될 때마다 BFS를 다시 수행하는 것은 비효율적임.
   - **Union-Find(Disjoint Set)나 다익스트라 알고리즘**을 활용하면 더 빠른 업데이트가 가능할 수 있음.
   - 만약 노드 1에서 다른 모든 노드까지의 거리를 유지해야 한다면 **다익스트라 알고리즘**을 고려할 수 있음.

2. **거리 저장 방식 최적화**
   - `distances` 리스트를 계속 갱신하는 구조로 바꿔서 BFS를 반복 호출하지 않고 **변화가 있는 노드만 업데이트**하는 방식도 가능.

이 코드가 적용될 **실제 문제**나 **입력 크기**에 따라 개선이 필요할 수 있음. 🚀

---

### ❓ 질문 (User)
다익스트라 알고리즘으로 설계한 코드 구현해줘

### 💡 답변 (Assistant)
다익스트라 알고리즘을 사용하여 **1번 노드에서 모든 노드까지의 최단 거리**를 계산하고, 간선을 추가할 때마다 최적의 경로를 업데이트하는 방식으로 개선할 수 있다.  

### **💡 개선된 접근 방식**
1. **BFS 대신 다익스트라 알고리즘 사용**
   - 다익스트라는 우선순위 큐(`heapq`)를 활용해 최단 거리를 빠르게 갱신하는 알고리즘이다.
   - 각 노드까지의 거리를 `dist` 리스트에 저장하고, `heapq`를 사용해 최소 비용 노드부터 처리한다.

2. **새로운 간선 추가 시, 다익스트라 알고리즘 실행**
   - 새로운 간선이 추가될 때마다 `dijkstra(1)`을 호출하여 최단 거리를 갱신한다.

---

### **📌 코드 구현**
```python
import sys
import heapq

input = sys.stdin.read
data = input().split("\n")

def dijkstra(start):
    pq = []
    heapq.heappush(pq, (0, start))  # (거리, 노드)
    dist = [float("inf")] * (n + 1)
    dist[start] = 0
    
    while pq:
        d, node = heapq.heappop(pq)
        if dist[node] < d:  # 이미 더 짧은 거리로 방문한 경우 무시
            continue
        
        for nxt, cost in edges[node]:
            new_dist = d + cost
            if new_dist < dist[nxt]:  # 더 짧은 경로 발견 시 업데이트
                dist[nxt] = new_dist
                heapq.heappush(pq, (new_dist, nxt))
    
    return dist[1:]  # 1번 노드에서 각 노드까지의 최단 거리 반환

# 입력 처리
idx = 0
n, m = map(int, data[idx].split())
idx += 1
edges = [[] for _ in range(n + 1)]

# 그래프 초기화
for _ in range(m):
    a, b = map(int, data[idx].split())
    idx += 1
    edges[a].append((b, 1))  # 가중치 1 (모든 간선 가중치 동일)
    edges[b].append((a, 1))

# 최초 최단 거리 계산
distances = dijkstra(1)

# 간선 추가 및 갱신
t = int(data[idx])
idx += 1
output = []
for _ in range(t):
    a, b = map(int, data[idx].split())
    idx += 1
    edges[a].append((b, 1))  # 새로운 간선 추가
    edges[b].append((a, 1))
    
    distances = dijkstra(1)  # 최단 거리 갱신
    output.append(" ".join(map(str, distances)))

print("\n".join(output))
```

---

### **📌 코드 설명**
1. **다익스트라 알고리즘(`dijkstra`)**
   - `heapq`(우선순위 큐)를 사용하여 **최소 거리 노드**부터 탐색.
   - 방문한 노드의 거리를 `dist` 리스트에 저장.
   - 인접한 노드를 탐색하며 최단 거리 갱신.

2. **초기 그래프 입력 (`edges` 리스트)**
   - `n, m`을 입력받고 **무방향 그래프**를 `edges` 리스트로 저장.
   - 각 간선의 가중치는 `1` (모든 간선의 비용이 동일하므로 BFS와 유사한 형태).

3. **최초 다익스트라 실행**
   - `dijkstra(1)`을 실행하여 1번 노드에서 모든 노드까지의 최단 거리 계산.

4. **간선 추가 및 최단 거리 갱신**
   - 새로운 간선이 추가될 때마다 `edges` 리스트에 반영.
   - 다익스트라 알고리즘을 다시 실행하여 최단 거리 갱신.

5. **결과 출력 최적화**
   - `output` 리스트에 결과를 저장한 후 한 번에 출력하여 성능 최적화.

---

### **📌 시간 복잡도 분석**
- **다익스트라 알고리즘**: `O((n + m) log n)`
  - `heapq`를 사용해 우선순위 큐를 관리하므로 **O(log n)** 의 시간 복잡도를 가짐.
- **최악의 경우** `t`번 다익스트라를 실행 → `O(t (n + m) log n)`

이전 BFS 기반 코드보다 **더 효율적인 경로 탐색이 가능**하며, `heapq`를 활용한 다익스트라 알고리즘으로 **매번 모든 노드를 탐색하는 비용을 절감**할 수 있다. 🚀

---

### ❓ 질문 (User)
```
from collections import deque

def bfs(s) :
    q = deque()
    q.append(s)
    distances = [-1] * (n + 1)
    distances[s] = 0

    while q :
        c = q.popleft()

        for nxt in edges[c] :
            dist = distances[c] + 1
            if distances[nxt] == -1 :
                distances[nxt] = dist
                q.append(nxt)

    return distances[1:]


n, m = map(int, input().split())
edges = [[] for _ in range(n + 1)]
for _ in range(m) :
    u, v = map(int, input().split())
    edges[u].append(v)
    edges[v].append(u)

bridges = int(input())
for _ in range(bridges) :
    u, v = map(int, input().split())
    edges[u].append(v)
    edges[v].append(u)
    res = bfs(s=1)
    print(*res)
```
이 코드를 분석해주고 분석을 주석으로 달아줘

### 💡 답변 (Assistant)
아래는 코드의 분석과 함께 상세한 주석을 추가한 버전이다.  

---

### **📌 코드 분석**
이 코드는 **BFS(너비 우선 탐색)** 을 사용하여 **1번 노드에서 모든 노드까지의 최단 거리**를 구하는 프로그램이다.  
또한, **새로운 간선(bridge)이 추가될 때마다 BFS를 다시 실행하여 거리 정보를 갱신**한다.  

```python
from collections import deque  # BFS를 위한 deque 사용

def bfs(s):
    """ 
    BFS를 사용하여 시작점 s에서 모든 노드까지의 최단 거리를 계산하는 함수.
    """
    q = deque()
    q.append(s)  # 시작 노드를 큐에 추가
    distances = [-1] * (n + 1)  # 모든 노드의 거리를 -1로 초기화 (방문하지 않음)
    distances[s] = 0  # 시작 노드의 거리는 0

    while q:
        c = q.popleft()  # 현재 노드(c)를 큐에서 꺼냄

        for nxt in edges[c]:  # 현재 노드 c에 연결된 모든 인접 노드 탐색
            dist = distances[c] + 1  # 현재 노드에서 한 단계 이동한 거리
            if distances[nxt] == -1:  # 아직 방문하지 않은 경우만 갱신
                distances[nxt] = dist
                q.append(nxt)  # 인접 노드를 큐에 추가하여 계속 탐색

    return distances[1:]  # 1번 노드에서 각 노드까지의 최단 거리 리스트 반환

# ----------------------- 입력 처리 -----------------------
n, m = map(int, input().split())  # n: 노드 개수, m: 초기 간선 개수
edges = [[] for _ in range(n + 1)]  # 인접 리스트 생성 (노드 번호는 1부터 시작)

for _ in range(m):
    u, v = map(int, input().split())  # 두 노드 u, v를 입력받아 간선 추가
    edges[u].append(v)  # 양방향 그래프이므로 양쪽에 추가
    edges[v].append(u)

# ---------------------- 추가 간선 처리 ----------------------
bridges = int(input())  # 추가할 간선(bridge)의 개수

for _ in range(bridges):
    u, v = map(int, input().split())  # 새로운 간선 (u, v) 입력
    edges[u].append(v)  # 양방향 간선 추가
    edges[v].append(u)

    res = bfs(s=1)  # 1번 노드에서 모든 노드까지의 최단 거리 다시 계산
    print(*res)  # 결과 출력 (공백으로 구분하여 출력)
```

---

### **📌 코드 실행 흐름**
1. **그래프 초기화**
   - `n, m`을 입력받아 **노드 개수와 초기 간선 개수**를 설정한다.
   - `edges` 리스트를 **인접 리스트** 방식으로 생성한다.
   - `m`개의 간선을 입력받아 그래프를 구성한다.

2. **BFS 함수 (`bfs`) 실행**
   - `bfs(1)`을 호출하면, **1번 노드에서 모든 노드까지의 최단 거리**를 구한다.
   - BFS를 사용하여 `distances` 리스트를 갱신한다.

3. **새로운 간선(bridge) 추가 후 거리 재계산**
   - 새로운 간선 `u, v`를 `edges` 리스트에 추가한다.
   - `bfs(1)`을 다시 실행하여 최단 거리 정보를 갱신한다.
   - 변경된 거리 정보를 출력한다.

---

### **📌 시간 복잡도 분석**
- **BFS의 시간 복잡도**: `O(n + m)`
  - 각 노드를 한 번만 방문하고, 각 간선도 한 번만 탐색한다.
- **t개의 추가 간선 처리 시 최악의 경우** `O(t(n + m))`
  - 새로운 간선이 추가될 때마다 BFS를 다시 수행하므로 `t`회 반복하면 성능 저하 가능.
- **최악의 경우** (`n = 100,000`, `m = 200,000`, `t = 100,000`) → **비효율적**  
  - 더 빠른 알고리즘(예: 다익스트라, 동적 업데이트)이 필요할 수 있음.

---

### **📌 개선점**
1. **BFS 매번 실행 최적화**
   - 새로운 간선이 추가될 때마다 `bfs(1)`을 실행하는 것은 비효율적.
   - **다익스트라 알고리즘**을 활용하면 우선순위 큐를 사용하여 더 빠르게 업데이트 가능.

2. **거리 갱신 방식 변경**
   - 모든 노드에 대해 처음부터 다시 계산하는 대신, **새로운 간선이 추가된 부분만 업데이트**하는 방식 사용 가능.

이 코드가 적용될 **입력 크기**나 **성능 요구 사항**에 따라 개선이 필요할 수 있다. 🚀

---
