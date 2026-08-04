---
type: Concept
title: "Negative Cycle Detection"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-12-07)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-12-07
status: active
---

# Negative Cycle Detection

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-12-07

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
문제
때는 2020년, 백준이는 월드나라의 한 국민이다. 월드나라에는 N개의 지점이 있고 N개의 지점 사이에는 M개의 도로와 W개의 웜홀이 있다. (단 도로는 방향이 없으며 웜홀은 방향이 있다.) 웜홀은 시작 위치에서 도착 위치로 가는 하나의 경로인데, 특이하게도 도착을 하게 되면 시작을 하였을 때보다 시간이 뒤로 가게 된다. 웜홀 내에서는 시계가 거꾸로 간다고 생각하여도 좋다.

시간 여행을 매우 좋아하는 백준이는 한 가지 궁금증에 빠졌다. 한 지점에서 출발을 하여서 시간여행을 하기 시작하여 다시 출발을 하였던 위치로 돌아왔을 때, 출발을 하였을 때보다 시간이 되돌아가 있는 경우가 있는지 없는지 궁금해졌다. 여러분은 백준이를 도와 이런 일이 가능한지 불가능한지 구하는 프로그램을 작성하여라.

입력
첫 번째 줄에는 테스트케이스의 개수 TC(1 ≤ TC ≤ 5)가 주어진다. 그리고 두 번째 줄부터 TC개의 테스트케이스가 차례로 주어지는데 각 테스트케이스의 첫 번째 줄에는 지점의 수 N(1 ≤ N ≤ 500), 도로의 개수 M(1 ≤ M ≤ 2500), 웜홀의 개수 W(1 ≤ W ≤ 200)이 주어진다. 그리고 두 번째 줄부터 M+1번째 줄에 도로의 정보가 주어지는데 각 도로의 정보는 S, E, T 세 정수로 주어진다. S와 E는 연결된 지점의 번호, T는 이 도로를 통해 이동하는데 걸리는 시간을 의미한다. 그리고 M+2번째 줄부터 M+W+1번째 줄까지 웜홀의 정보가 S, E, T 세 정수로 주어지는데 S는 시작 지점, E는 도착 지점, T는 줄어드는 시간을 의미한다. T는 10,000보다 작거나 같은 자연수 또는 0이다.

두 지점을 연결하는 도로가 한 개보다 많을 수도 있다. 지점의 번호는 1부터 N까지 자연수로 중복 없이 매겨져 있다.

출력
TC개의 줄에 걸쳐서 만약에 시간이 줄어들면서 출발 위치로 돌아오는 것이 가능하면 YES, 불가능하면 NO를 출력한다.

예제 입력 1 
2
3 3 1
1 2 2
1 3 4
2 3 1
3 1 3
3 2 1
1 2 3
2 3 4
3 1 8
예제 출력 1 
NO
YES

### 💡 답변 (Assistant)
이 문제는 그래프에서 음의 사이클(negative cycle)이 존재하는지 판별하는 문제입니다. 음의 사이클이 존재하면, 시작 지점에서 출발하여 사이클을 통해 다시 시작 지점으로 돌아올 때 시간이 되돌아갈 수 있습니다. 이를 판별하기 위해 **벨만-포드 알고리즘**을 사용합니다.

### 문제 풀이
1. **입력 처리**:
   - 여러 개의 테스트케이스가 주어지므로 각 테스트케이스를 독립적으로 처리합니다.
   - 도로와 웜홀의 정보를 읽어 그래프를 구성합니다.

2. **벨만-포드 알고리즘**:
   - 음의 사이클 여부를 확인하기 위해 모든 지점을 출발점으로 설정하여 탐색합니다.
   - 벨만-포드 알고리즘은 정점의 개수 \( N \)에 대해 최대 \( N-1 \)번의 릴랙스(relaxation)를 수행하며, \( N \)번째에 여전히 거리가 갱신된다면 음의 사이클이 존재한다고 판단합니다.

3. **출력**:
   - 각 테스트케이스에 대해 음의 사이클이 있으면 "YES", 없으면 "NO"를 출력합니다.

### 코드 구현

```python
def wormhole():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    TC = int(data[0])  # 테스트 케이스 개수
    results = []
    idx = 1  # 데이터 읽기 인덱스
    
    for _ in range(TC):
        # 지점 수, 도로 개수, 웜홀 개수
        N, M, W = map(int, data[idx].split())
        idx += 1
        
        edges = []
        
        # 도로 정보 추가
        for _ in range(M):
            S, E, T = map(int, data[idx].split())
            edges.append((S, E, T))  # 도로는 양방향
            edges.append((E, S, T))
            idx += 1
        
        # 웜홀 정보 추가
        for _ in range(W):
            S, E, T = map(int, data[idx].split())
            edges.append((S, E, -T))  # 웜홀은 방향성과 음의 가중치를 가짐
            idx += 1
        
        # 벨만-포드 알고리즘으로 음의 사이클 판별
        def has_negative_cycle():
            # 거리 초기화
            distance = [float('inf')] * (N + 1)
            
            # 모든 노드에서 시작
            for start in range(1, N + 1):
                distance[start] = 0
                
                # N-1번 릴랙스
                for _ in range(N - 1):
                    for u, v, w in edges:
                        if distance[u] != float('inf') and distance[u] + w < distance[v]:
                            distance[v] = distance[u] + w
                
                # N번째 릴랙스에서 갱신이 일어난다면 음의 사이클 존재
                for u, v, w in edges:
                    if distance[u] != float('inf') and distance[u] + w < distance[v]:
                        return True
            
            return False
        
        if has_negative_cycle():
            results.append("YES")
        else:
            results.append("NO")
    
    # 결과 출력
    sys.stdout.write("\n".join(results) + "\n")

```

### 코드 설명
1. **입력 처리**:
   - 테스트케이스별로 그래프의 간선 정보를 읽어 `edges` 리스트에 저장합니다.
   - 도로는 양방향이므로 간선을 양쪽으로 추가합니다.
   - 웜홀은 단방향이고 시간 감소를 나타내므로 가중치를 음수로 추가합니다.

2. **벨만-포드 알고리즘**:
   - 각 지점을 출발점으로 삼아 음의 사이클 여부를 확인합니다.
   - \( N-1 \)번 릴랙스 후에도 거리 갱신이 발생하면 음의 사이클이 존재한다고 판단합니다.

3. **출력**:
   - 각 테스트케이스의 결과를 리스트에 저장한 후, 한 번에 출력합니다.

### 예제 실행
#### 입력:
```
2
3 3 1
1 2 2
1 3 4
2 3 1
3 1 3
3 2 1
1 2 3
2 3 4
3 1 8
```

#### 출력:
```
NO
YES
```

---

### ❓ 질문 (User)
벨만 포드 알고리즘을 파이썬 코드로 작성해줘

### 💡 답변 (Assistant)
벨만-포드 알고리즘은 음수 가중치가 포함된 그래프에서 최단 경로를 찾을 수 있는 알고리즘입니다. 아래는 파이썬으로 작성한 벨만-포드 알고리즘의 기본 구현입니다.

### 벨만-포드 알고리즘 구현

```python
def bellman_ford(n, edges, start):
    """
    벨만-포드 알고리즘 구현
    :param n: 정점의 개수
    :param edges: 간선 리스트 (u, v, w) 형태의 튜플로 표현. u에서 v로 가는 가중치 w의 간선.
    :param start: 시작 정점 번호
    :return: 최단 거리 리스트, 음수 사이클 존재 여부 (True/False)
    """
    # 거리 배열 초기화
    INF = float('inf')
    distance = [INF] * (n + 1)
    distance[start] = 0

    # 정점 수 - 1번 반복하여 모든 간선에 대해 거리 갱신
    for i in range(n - 1):
        for u, v, w in edges:
            if distance[u] != INF and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w

    # 음수 사이클 확인 (n번째 반복에서 갱신이 발생하면 음수 사이클 존재)
    has_negative_cycle = False
    for u, v, w in edges:
        if distance[u] != INF and distance[u] + w < distance[v]:
            has_negative_cycle = True
            break

    return distance, has_negative_cycle


# 테스트 예제
if __name__ == "__main__":
    # 정점과 간선 정의
    n = 5  # 정점의 수
    edges = [
        (1, 2, 6),
        (1, 3, 7),
        (2, 3, 8),
        (2, 4, 5),
        (2, 5, -4),
        (3, 4, -3),
        (3, 5, 9),
        (4, 2, -2),
        (5, 1, 2),
        (5, 4, 7)
    ]
    start = 1  # 시작 정점

    # 알고리즘 실행
    distances, negative_cycle = bellman_ford(n, edges, start)

    # 결과 출력
    if negative_cycle:
        print("음수 사이클이 존재합니다.")
    else:
        print("최단 거리:", distances[1:])  # 1번 정점부터 출력
```

---

### 코드 설명

1. **입력 정의**:
   - `n`: 정점의 개수.
   - `edges`: 간선 리스트. 각 간선은 `(u, v, w)`로, \( u \)에서 \( v \)로 가는 가중치 \( w \)를 나타냅니다.
   - `start`: 시작 정점.

2. **거리 배열 초기화**:
   - `distance` 배열을 무한대로 초기화하고, 시작 정점의 거리를 0으로 설정합니다.

3. **거리 갱신 (릴랙스)**:
   - 정점 수 - 1번 반복하면서 모든 간선에 대해 거리 갱신을 수행합니다.
   - 릴랙스는 `distance[u] + w < distance[v]` 조건이 성립하면 \( v \)의 거리를 갱신하는 과정입니다.

4. **음수 사이클 확인**:
   - 모든 간선에 대해 \( n \)번째 릴랙스에서 갱신이 발생하면 음수 사이클이 존재한다고 판단합니다.

5. **결과 출력**:
   - 음수 사이클이 있으면 이를 출력하고, 없다면 최단 거리를 출력합니다.

---

### 테스트 예제 설명
위 예제에서 시작 정점 1에서 각 정점으로의 최단 거리를 구합니다. 음수 사이클이 존재하는 경우, 최단 거리 계산은 무효가 됩니다.

---
