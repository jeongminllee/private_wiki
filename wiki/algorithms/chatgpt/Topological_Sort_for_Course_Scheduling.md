---
type: Concept
title: "Topological Sort for Course Scheduling"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-11-28)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-11-28
status: active
---

# Topological Sort for Course Scheduling

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-11-28

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
문제
올해 Z대학 컴퓨터공학부에 새로 입학한 민욱이는 학부에 개설된 모든 전공과목을 듣고 졸업하려는 원대한 목표를 세웠다. 어떤 과목들은 선수과목이 있어 해당되는 모든 과목을 먼저 이수해야만 해당 과목을 이수할 수 있게 되어 있다. 공학인증을 포기할 수 없는 불쌍한 민욱이는 선수과목 조건을 반드시 지켜야만 한다. 민욱이는 선수과목 조건을 지킬 경우 각각의 전공과목을 언제 이수할 수 있는지 궁금해졌다. 계산을 편리하게 하기 위해 아래와 같이 조건을 간소화하여 계산하기로 하였다.

한 학기에 들을 수 있는 과목 수에는 제한이 없다.
모든 과목은 매 학기 항상 개설된다.
모든 과목에 대해 각 과목을 이수하려면 최소 몇 학기가 걸리는지 계산하는 프로그램을 작성하여라.

입력
첫 번째 줄에 과목의 수 N(1 ≤ N ≤ 1000)과 선수 조건의 수 M(0 ≤ M ≤ 500000)이 주어진다. 선수과목 조건은 M개의 줄에 걸쳐 한 줄에 정수 A B 형태로 주어진다. A번 과목이 B번 과목의 선수과목이다. A < B인 입력만 주어진다. (1 ≤ A < B ≤ N)

출력
1번 과목부터 N번 과목까지 차례대로 최소 몇 학기에 이수할 수 있는지를 한 줄에 공백으로 구분하여 출력한다.

예제 입력 1 
3 2
2 3
1 2
예제 출력 1 
1 2 3
예제 입력 2 
6 4
1 2
1 3
2 5
4 5
예제 출력 2 
1 2 2 1 3 1
힌트
3개의 과목이 있고, 2번 과목을 이수하기 위해서는 1번 과목을 이수해야 하고, 3번 과목을 이수하기 위해서는 2번 과목을 이수해야 한다.

### 💡 답변 (Assistant)
이 문제는 **위상 정렬(Topological Sort)** 알고리즘을 활용하여 해결할 수 있습니다. 각 과목을 그래프의 노드로 보고, 선수과목 관계를 방향성을 가진 간선으로 나타내는 방식으로 접근합니다. 다음은 문제를 해결하기 위한 단계입니다.

---

### 문제 해결 과정

1. **입력 데이터 처리**:
   - 과목 수 \( N \)과 선수 조건 수 \( M \)을 입력받습니다.
   - 선수 조건 정보를 그래프 형태로 저장하고, 각 노드의 진입 차수를 계산합니다.

2. **위상 정렬 수행**:
   - 진입 차수가 0인 노드를 큐에 넣습니다. 이 노드들은 선수과목 없이 들을 수 있는 과목입니다.
   - 큐에서 노드를 하나씩 꺼내면서 해당 노드가 선수과목인 모든 노드의 진입 차수를 1씩 감소시킵니다.
   - 진입 차수가 0이 된 노드는 다음 학기에 이수할 수 있으므로 큐에 추가합니다.
   - 각 노드가 이수 가능한 학기를 기록합니다.

3. **결과 출력**:
   - 각 과목의 이수 가능한 최소 학기를 출력합니다.

---

### Python 코드

```python
from collections import deque

def calculate_min_semesters(N, M, prerequisites):
    # 그래프와 진입 차수 초기화
    graph = [[] for _ in range(N + 1)]
    in_degree = [0] * (N + 1)
    
    for A, B in prerequisites:
        graph[A].append(B)
        in_degree[B] += 1
    
    # 큐 초기화 및 학기 저장 리스트
    queue = deque()
    semesters = [0] * (N + 1)
    
    # 진입 차수가 0인 노드를 큐에 삽입
    for i in range(1, N + 1):
        if in_degree[i] == 0:
            queue.append(i)
            semesters[i] = 1  # 첫 학기에 들을 수 있음
    
    # 위상 정렬 수행
    while queue:
        current = queue.popleft()
        for next_course in graph[current]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
                semesters[next_course] = semesters[current] + 1
    
    # 결과 반환
    return semesters[1:]  # 1번 과목부터 N번 과목까지

# 입력 처리
N, M = map(int, input().split())
prerequisites = [tuple(map(int, input().split())) for _ in range(M)]

# 결과 계산
result = calculate_min_semesters(N, M, prerequisites)

# 결과 출력
print(" ".join(map(str, result)))
```

---

### 코드 설명

1. **그래프 구성**:
   - `graph[A]`에는 A번 과목을 선수과목으로 요구하는 과목들을 저장합니다.
   - `in_degree[B]`는 B번 과목의 진입 차수를 나타냅니다.

2. **위상 정렬**:
   - 선수과목을 모두 이수한 과목부터 큐에 추가하며, 각 과목을 이수 가능한 학기를 계산합니다.

3. **결과 출력**:
   - `semesters` 배열에는 각 과목을 최소 몇 학기에 들을 수 있는지 저장됩니다. 이를 출력합니다.

---

### 시간 복잡도

- **그래프 초기화 및 입력 처리**: \( O(M) \)
- **위상 정렬**: \( O(N + M) \)
- 전체 시간 복잡도는 \( O(N + M) \)로 효율적입니다.

---

### 예제 실행

#### 입력
```
3 2
2 3
1 2
```

#### 출력
```
1 2 3
```

#### 입력
```
6 4
1 2
1 3
2 5
4 5
```

#### 출력
```
1 2 2 1 3 1
```

이 코드는 문제 조건을 만족하며, 효율적으로 동작합니다.

---

### ❓ 질문 (User)
```

from collections import deque

# N : 과목의 수, M : 선수 조건의 수
N, M = map(int, input().split())

graph = [[] for _ in range(N + 1)]
in_degree = [0] * (N + 1)

for _ in range(M) :
    A, B = map(int, input().split())
    graph[A].append(B)
    in_degree[B] += 1

# 위상 정렬 수행
q = deque()
res = [0] * (N + 1)

# 진입 차수가 0인 노드부터 시작
for i in range(1, N + 1) :
    if in_degree[i] == 0 :
        q.append(i)
        res[i] = 1  # 첫 학기부터 수강 가능

while q :
    curr = q.popleft()

    for neighbor in graph[curr] :
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0 :
            q.append(neighbor)
            res[neighbor] = res[curr] + 1

print(res[1:])
```
이 코드와 로직이 다른 점을 가르쳐줘

### 💡 답변 (Assistant)
당신이 작성한 코드와 내가 제안한 코드의 로직은 **근본적으로 동일**하며, 둘 다 **위상 정렬**을 사용하여 선수 과목 조건을 충족하는 최소 학기를 계산합니다. 하지만 몇 가지 차이점이 존재합니다. 아래에서 세부적으로 설명하겠습니다.

---

### 주요 차이점

#### 1. **입력 방식**
- **당신의 코드**: `input()`을 사용하여 직접 입력을 처리합니다.
  ```python
  N, M = map(int, input().split())
  ```
- **내 코드**: 입력을 함수로 분리하여 처리하며, 함수 호출로 값을 전달받는 구조입니다.
  ```python
  def calculate_min_semesters(N, M, prerequisites):
      ...
  N, M = map(int, input().split())
  prerequisites = [tuple(map(int, input().split())) for _ in range(M)]
  ```

  **차이점**: 내 코드는 함수화되어 재사용성이 높고, 테스트에 적합합니다. 반면, 당신의 코드는 입력과 로직이 한곳에 있어 간단하지만 확장성이 떨어집니다.

---

#### 2. **결과 저장 및 출력**
- **당신의 코드**:
  - `res` 배열을 사용하여 각 과목의 이수 가능한 최소 학기를 저장합니다.
  - `print(res[1:])`를 통해 결과를 출력합니다.
- **내 코드**:
  - `semesters` 배열을 사용하여 최소 학기를 저장합니다.
  - `return semesters[1:]`를 통해 결과를 반환하며, 출력은 별도로 처리합니다.
  ```python
  result = calculate_min_semesters(N, M, prerequisites)
  print(" ".join(map(str, result)))
  ```

  **차이점**: 
  - 당신의 코드는 결과를 바로 출력하지만, 내 코드는 결과를 반환하도록 설계되어 다른 작업과 연계가 쉽습니다.

---

#### 3. **큐 초기화 위치**
- **당신의 코드**:
  큐(`q`) 초기화와 진입 차수 0인 노드를 큐에 추가하는 로직이 별도로 구성되어 있습니다.
  ```python
  q = deque()
  for i in range(1, N + 1):
      if in_degree[i] == 0:
          q.append(i)
          res[i] = 1
  ```
- **내 코드**:
  큐 초기화와 진입 차수 0인 노드 추가가 함수 내에서 한 번에 처리됩니다.
  ```python
  for i in range(1, N + 1):
      if in_degree[i] == 0:
          queue.append(i)
          semesters[i] = 1
  ```

  **차이점**: 기능적으로는 동일하지만, 내 코드는 변수 이름을 조금 더 명확히 하며 구조적으로 읽기 쉽습니다.

---

#### 4. **가독성과 변수 이름**
- **당신의 코드**:
  - 변수 이름: `q`, `res`, `curr`, `neighbor` 등을 사용하여 간결합니다.
  ```python
  q = deque()
  res[i] = 1
  curr = q.popleft()
  for neighbor in graph[curr]:
      ...
  ```
- **내 코드**:
  - 변수 이름: `queue`, `semesters`, `current`, `next_course` 등 조금 더 직관적이고 설명적인 이름을 사용합니다.
  ```python
  queue = deque()
  semesters[i] = 1
  current = queue.popleft()
  for next_course in graph[current]:
      ...
  ```

  **차이점**: 내 코드가 변수 이름에서 의도를 명확히 드러내며, 코드 가독성이 더 좋을 수 있습니다.

---

#### 5. **함수화 여부**
- **당신의 코드**:
  전체 로직이 하나의 스크립트로 작성되어 함수화가 이루어지지 않았습니다.
- **내 코드**:
  로직을 함수로 분리하여 입력 처리, 그래프 생성, 위상 정렬 계산 등을 모듈화했습니다.
  ```python
  def calculate_min_semesters(N, M, prerequisites):
      ...
  ```

  **차이점**: 내 코드는 함수화로 인해 유지보수성과 확장성이 더 뛰어납니다. 테스트 시에 함수만 독립적으로 호출하기 쉽습니다.

---

### 유사점
- 두 코드 모두 **위상 정렬 알고리즘**을 사용하여 문제를 해결합니다.
- 큐를 사용해 진입 차수를 관리하고, 위상 정렬의 순서를 결정합니다.
- 모든 노드를 방문하며 각 노드의 최소 학기를 기록합니다.
- 시간 복잡도 \( O(N + M) \)로 효율적입니다.

---

### 결론
로직 자체는 두 코드가 동일하며, 차이점은 주로 **구조화**, **가독성**, **입력 처리 방식**에 있습니다.  
- 당신의 코드는 간결하고, 입출력이 직접적입니다.
- 내 코드는 함수화와 모듈화로 확장성과 재사용성이 더 좋습니다.

---

### 💡 답변 (Assistant)
이 코드는 문제에서 주어진 선수과목 조건을 바탕으로, 각 과목을 최소 몇 학기에 이수할 수 있는지를 계산하는 프로그램입니다. 아래에 코드의 동작을 단계별로 설명하겠습니다.

---

### **1. 함수 정의**
```python
def calculate_min_semesters(N, M, prerequisites):
```
- `N`: 과목의 수 (1번부터 \( N \)번 과목까지).
- `M`: 선수 조건의 수 (선수과목 관계의 개수).
- `prerequisites`: 선수과목 조건을 나타내는 리스트, 각 요소는 `(A, B)` 형태로 `A` 과목을 수강해야 `B` 과목을 수강할 수 있음을 나타냄.

---

### **2. 그래프와 진입 차수 초기화**
```python
graph = [[] for _ in range(N + 1)]
in_degree = [0] * (N + 1)
```
- **`graph`**:
  - 각 과목에 대해 선수과목 관계를 저장하는 인접 리스트입니다.
  - `graph[A]`는 A 과목을 선수과목으로 요구하는 과목들의 리스트입니다.
- **`in_degree`**:
  - 각 과목의 진입 차수를 저장하는 배열입니다.
  - 진입 차수는 해당 과목을 수강하기 위해 선수과목으로 지정된 과목의 개수입니다.

---

### **3. 선수과목 관계 입력**
```python
for A, B in prerequisites:
    graph[A].append(B)
    in_degree[B] += 1
```
- `A → B` 관계를 그래프에 추가합니다.
- `graph[A]`에 `B`를 추가하여 A가 B의 선수과목임을 저장합니다.
- `B`의 진입 차수(`in_degree[B]`)를 1 증가시킵니다.

예를 들어, 입력 `prerequisites = [(1, 2), (2, 3)]`가 주어지면:
- `graph = [[], [2], [3], [], ..., []]`
- `in_degree = [0, 0, 1, 1, 0, ..., 0]`

---

### **4. 초기 큐와 학기 저장 배열 초기화**
```python
queue = deque()
semesters = [0] * (N + 1)
```
- **`queue`**:
  - 현재 진입 차수가 0인 과목들을 저장하는 큐입니다.
  - 이 큐를 이용해 위상 정렬을 수행합니다.
- **`semesters`**:
  - 각 과목을 최소 몇 학기에 이수할 수 있는지를 저장하는 배열입니다.
  - `semesters[i]`는 \( i \)번 과목을 이수할 수 있는 최소 학기를 의미합니다.

---

### **5. 진입 차수가 0인 노드 큐에 삽입**
```python
for i in range(1, N + 1):
    if in_degree[i] == 0:
        queue.append(i)
        semesters[i] = 1  # 첫 학기에 들을 수 있음
```
- 진입 차수가 0인 과목들은 선수과목 없이 들을 수 있으므로, 첫 학기부터 수강 가능합니다.
- `semesters[i] = 1`로 설정하여 첫 학기를 기록합니다.

---

### **6. 위상 정렬 수행**
```python
while queue:
    current = queue.popleft()
    for next_course in graph[current]:
        in_degree[next_course] -= 1
        if in_degree[next_course] == 0:
            queue.append(next_course)
            semesters[next_course] = semesters[current] + 1
```
- **큐에서 과목 꺼내기**:
  - 큐의 가장 앞에 있는 과목(`current`)을 꺼내고, 이 과목을 선수과목으로 요구하는 과목들에 대해 처리합니다.
- **진입 차수 갱신**:
  - `current` 과목이 선수과목으로 설정된 모든 과목(`next_course`)에 대해 진입 차수를 1 감소시킵니다.
- **다음 학기 과목 추가**:
  - 만약 `next_course`의 진입 차수가 0이 되었다면, 선수과목 조건을 모두 만족했으므로 큐에 추가하고, `semesters[next_course]`를 갱신합니다.
  - `semesters[next_course] = semesters[current] + 1`로 설정하여, `current`를 이수한 다음 학기에 이수 가능하다고 기록합니다.

---

### **7. 결과 반환**
```python
return semesters[1:]  # 1번 과목부터 N번 과목까지
```
- 1번 과목부터 \( N \)번 과목까지 최소 학기를 리스트로 반환합니다.

---

### **8. 입력 및 출력 처리**
```python
N, M = map(int, input().split())
prerequisites = [tuple(map(int, input().split())) for _ in range(M)]

result = calculate_min_semesters(N, M, prerequisites)
print(" ".join(map(str, result)))
```
- `N`, `M` 및 선수 조건을 입력받아 `prerequisites` 리스트로 저장합니다.
- `calculate_min_semesters` 함수를 호출하여 결과를 계산합니다.
- 결과 리스트를 공백으로 구분하여 출력합니다.

---

### **동작 예시**

#### 입력
```
3 2
2 3
1 2
```

#### 동작
1. **그래프와 진입 차수 초기화**:
   - `graph = [[], [2], [3], []]`
   - `in_degree = [0, 0, 1, 1]`

2. **초기 큐 설정**:
   - 진입 차수가 0인 노드: `[1]`
   - `queue = deque([1])`, `semesters = [0, 1, 0, 0]`

3. **위상 정렬**:
   - 1번 꺼냄: `queue = []`, 2번 추가 (`semesters[2] = 2`).
   - 2번 꺼냄: `queue = []`, 3번 추가 (`semesters[3] = 3`).

4. **결과**:
   - `semesters = [0, 1, 2, 3]`
   - 출력: `1 2 3`

---

### **시간 복잡도**
- **그래프 생성**: \( O(M) \) (간선 수만큼 반복).
- **위상 정렬**: \( O(N + M) \) (노드 및 간선 수만큼 반복).
- **전체**: \( O(N + M) \).

### **공간 복잡도**
- 그래프: \( O(N + M) \).
- 진입 차수 배열 및 기타 데이터 구조: \( O(N) \).
- **전체**: \( O(N + M) \).

---

이 코드는 문제에서 요구한 조건을 충족하며, 효율적으로 작동합니다.

---

### ❓ 질문 (User)
```
from collections import deque

def calculate_min_semesters(N, M, prerequisites):
    # 그래프와 진입 차수 초기화
    graph = [[] for _ in range(N + 1)]
    in_degree = [0] * (N + 1)
    
    for A, B in prerequisites:
        graph[A].append(B)
        in_degree[B] += 1
    
    # 큐 초기화 및 학기 저장 리스트
    queue = deque()
    semesters = [0] * (N + 1)
    
    # 진입 차수가 0인 노드를 큐에 삽입
    for i in range(1, N + 1):
        if in_degree[i] == 0:
            queue.append(i)
            semesters[i] = 1  # 첫 학기에 들을 수 있음
    
    # 위상 정렬 수행
    while queue:
        current = queue.popleft()
        for next_course in graph[current]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
                semesters[next_course] = semesters[current] + 1
    
    # 결과 반환
    return semesters[1:]  # 1번 과목부터 N번 과목까지

# 입력 처리
N, M = map(int, input().split())
prerequisites = [tuple(map(int, input().split())) for _ in range(M)]

# 결과 계산
result = calculate_min_semesters(N, M, prerequisites)

# 결과 출력
print(" ".join(map(str, result)))
```
이 코드 동작에 대해서 자세하게 설명해줘
