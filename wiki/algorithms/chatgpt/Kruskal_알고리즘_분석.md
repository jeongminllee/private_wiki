---
type: Concept
title: "Kruskal 알고리즘 분석"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-12-31)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-12-31
status: active
---

# Kruskal 알고리즘 분석

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-12-31

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
def find(v) :
    if v != parents[v] :
        parents[v] = find(parents[v])

    return parents[v]

def union(v1, v2) :
    if v1 > v2 :
        parents[v2] = v1
    else :
        parents[v1] = v2


V, E = map(int, input().split())
parents = [v for v in range(V + 1)]
edges = []

for _ in range(E) :
    v1, v2, w = map(int, input().split())
    edges.append([w, v1, v2])

edges.sort()
sum_weight = 0

for w, v1, v2 in edges :
    v1_root = find(v1)
    v2_root = find(v2)

    if v1_root != v2_root :
        union(v1_root, v2_root)
        sum_weight += w

print(sum_weight)
``` 
이 코드를 분석해줘

### 💡 답변 (Assistant)
주어진 코드는 **최소 신장 트리(Minimum Spanning Tree, MST)**를 찾기 위한 **Kruskal 알고리즘**을 구현한 Python 코드입니다. MST는 가중치가 있는 연결 그래프에서 모든 정점을 연결하는 최소 비용의 트리를 찾는 문제입니다. 이 코드는 입력받은 그래프에 대해 MST의 총 가중치를 계산합니다. 아래에서 코드를 단계별로 분석합니다.

---

### **1. 함수 분석**
#### `find(v)` (경로 압축)
- **목적**: 주어진 정점 `v`의 부모 정점을 찾음.
- **작동 원리**:
  - 만약 `v`가 자신의 부모가 아니라면, 재귀적으로 부모를 찾음.
  - 경로 압축을 통해 `v`와 관련된 모든 정점들이 직접 부모를 가리키도록 최적화.
- **결과**: 집합의 루트 정점 반환.

```python
def find(v):
    if v != parents[v]:
        parents[v] = find(parents[v])  # 경로 압축
    return parents[v]
```

---

#### `union(v1, v2)` (집합 합치기)
- **목적**: 두 정점 `v1`과 `v2`가 속한 집합을 합침.
- **작동 원리**:
  - `v1`과 `v2`의 크기에 따라 부모를 설정.
  - 작은 쪽이 큰 쪽의 자식이 됨. (여기선 번호가 작은 정점이 부모가 되는 규칙은 아님.)
- **결과**: 두 정점을 같은 집합으로 병합.

```python
def union(v1, v2):
    if v1 > v2:
        parents[v2] = v1
    else:
        parents[v1] = v2
```

---

### **2. 메인 알고리즘**
#### 입력 처리
1. **정점(V)와 간선(E)** 입력:
   ```python
   V, E = map(int, input().split())
   ```
2. **부모 배열 초기화**:
   - 각 정점이 자기 자신을 부모로 가지도록 설정.
   ```python
   parents = [v for v in range(V + 1)]
   ```
3. **간선 정보 입력**:
   - 각 간선의 가중치와 두 정점 정보를 리스트에 저장.
   ```python
   for _ in range(E):
       v1, v2, w = map(int, input().split())
       edges.append([w, v1, v2])
   ```

---

#### Kruskal 알고리즘
1. **간선 정렬**:
   - 가중치 기준으로 오름차순 정렬.
   ```python
   edges.sort()
   ```
2. **최소 신장 트리 생성**:
   - 간선들을 순회하면서, 두 정점이 서로 다른 집합에 속해 있다면 합침.
   - 가중치를 더하며 MST를 구성.
   ```python
   for w, v1, v2 in edges:
       v1_root = find(v1)
       v2_root = find(v2)

       if v1_root != v2_root:
           union(v1_root, v2_root)
           sum_weight += w
   ```

3. **결과 출력**:
   - MST의 총 가중치 출력.
   ```python
   print(sum_weight)
   ```

---

### **3. 동작 예시**
#### 입력
```
4 5
1 2 1
1 3 2
2 3 2
3 4 3
2 4 3
```
- 정점: 4개 (`V=4`)
- 간선: 5개 (`E=5`)
- 간선 정보: `(1-2, 1)`, `(1-3, 2)`, `(2-3, 2)`, `(3-4, 3)`, `(2-4, 3)`

#### 간선 정렬
```
edges = [
    [1, 1, 2],
    [2, 1, 3],
    [2, 2, 3],
    [3, 3, 4],
    [3, 2, 4]
]
```

#### MST 구성
- `1-2` 연결, 가중치: 1
- `1-3` 연결, 가중치: 2
- `3-4` 연결, 가중치: 3
- 총 가중치: `1 + 2 + 3 = 6`

#### 출력
```
6
```

---

### **4. 주요 특성**
- **시간 복잡도**:
  - 간선 정렬: \(O(E \log E)\)
  - 유니온-파인드 연산: \(O(\alpha(V))\) (거의 상수 시간)
  - 전체 복잡도: \(O(E \log E + V)\)
- **공간 복잡도**: \(O(V + E)\) (부모 배열 및 간선 리스트)

### **5. 개선 사항**
- `union` 함수에서 번호가 작은 쪽이 부모가 되는 규칙을 추가하면 트리가 더 균형 잡힐 수 있음.
- 주석 추가로 가독성을 향상시킬 수 있음.

---
