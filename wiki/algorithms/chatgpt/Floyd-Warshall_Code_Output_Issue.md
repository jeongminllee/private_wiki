---
type: Concept
title: "Floyd-Warshall Code Output Issue"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-12-02)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-12-02
status: active
---

# Floyd-Warshall Code Output Issue

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-12-02

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
주어진 두 코드는 모두 `Floyd-Warshall` 알고리즘을 사용하여 도시 간 최단 거리를 계산하고 결과를 출력합니다. 그러나 출력 형식에서 미세한 차이가 존재하며, 그로 인해 일부 테스트 케이스에서 2번 코드가 통과하지 않을 가능성이 있습니다.

---

### 차이점 분석
#### 1. **결과 출력 방식의 차이**
- **1번 코드**는 결과를 출력할 때 `INF` 값을 `0`으로 변환한 후 각 값을 공백으로 구분하여 출력합니다.
    ```python
    if res[i][j] == INF:
        print('0', end=' ')
    else:
        print(res[i][j], end=' ')
    ```
    각 행 끝마다 `print()`를 호출하여 줄 바꿈을 명시적으로 수행합니다.

- **2번 코드**는 `print(*res[i])`를 사용하여 한 행의 값을 공백으로 구분하여 출력합니다.
    ```python
    print(*res[i])
    ```
    이 경우 `INF` 값을 `0`으로 변환하는 처리가 없습니다.

#### 2. **`INF` 처리 여부**
- **1번 코드**는 `INF` 값을 `0`으로 출력하여, 도시 간에 경로가 없음을 나타냅니다. 이는 문제에서 요구한 출력 형식과 일치할 가능성이 높습니다.
- **2번 코드**는 `INF` 값을 변환하지 않고 그대로 출력하기 때문에, 출력 결과가 예상과 다를 수 있습니다. `INF`는 화면에 출력되지 않거나, 다른 형태로 표현될 수 있어 오답으로 간주될 수 있습니다.

---

### 수정 방안
2번 코드를 수정하여 `INF` 값을 `0`으로 변환하는 처리를 추가하면 문제를 해결할 수 있습니다. 수정된 코드는 아래와 같습니다:

```python
for i in range(n):
    for j in range(n):
        if res[i][j] == INF:
            res[i][j] = 0
    print(*res[i])
```

이렇게 하면 1번 코드와 동일하게 `INF`를 처리하여 올바른 출력 형식을 만족할 수 있습니다.

---

### 결론
- 1번 코드가 통과되는 이유는 출력 형식에서 `INF` 값을 `0`으로 변환하여 문제의 요구사항을 충족하기 때문입니다.
- 2번 코드가 통과되지 않는 이유는 `INF`를 처리하지 않아 출력 형식이 요구사항과 일치하지 않기 때문입니다.
- **수정 방법**: `INF` 값을 `0`으로 변환하는 로직을 추가하면 2번 코드도 통과할 수 있습니다.

---

### ❓ 질문 (User)
```
INF = float('inf')

def floyd_warshall(bus) :
    distance = [[INF] * n for _ in range(n)]

    for i in range(n) :
        for j in range(n) :
            if i == j :
                distance[i][j] = 0

    for a, b, c in bus :
        distance[a-1][b-1] = min(distance[a-1][b-1], c)

    for k in range(n) :
        for i in range(n) :
            for j in range(n) :
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

    return distance

# 도시의 개수
n = int(input())

# 버스의 개수
m = int(input())

# 버스 정보
bus = [list(map(int, input().split())) for _ in range(m)]

res = floyd_warshall(bus)

for i in range(n) :
    for j in range(n) :
        if res[i][j] == INF :
            print('0', end=' ')
        else :
            print(res[i][j], end=' ')
    print()
```
```
INF = float('inf')

def floyd_warshall(bus) :
    distance = [[INF] * n for _ in range(n)]

    for i in range(n) :
        for j in range(n) :
            if i == j :
                distance[i][j] = 0

    for a, b, c in bus :
        distance[a-1][b-1] = min(distance[a-1][b-1], c)

    for k in range(n) :
        for i in range(n) :
            for j in range(n) :
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

    return distance

# 도시의 개수
n = int(input())

# 버스의 개수
m = int(input())

# 버스 정보
bus = [list(map(int, input().split())) for _ in range(m)]

res = floyd_warshall(bus)
for i in range(n) :
    print(*res[i])
```
차이를 보고 왜 1번 코드는 통과되는데 2번 코드는 통과가 안되는지 알려줘
