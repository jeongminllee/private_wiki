---
type: Concept
title: "LeetCode 637 문제 설명"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-03-23)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-03-23
status: active
---

# LeetCode 637 문제 설명

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-03-23

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
LeetCode 637. Average of Levels in Binary Tree 에 대해서 설명해줘

### 💡 답변 (Assistant)
LeetCode 637번 "Average of Levels in Binary Tree" 문제는 이진 트리의 각 레벨(깊이)에 있는 노드들의 값을 평균 내어 배열로 반환하는 문제입니다.

---

### 문제 설명
- **입력:** 이진 트리의 루트 노드.
- **출력:** 트리의 각 레벨별 노드 값의 평균을 담은 배열. 예를 들어, 첫 번째 원소는 루트 노드의 값(첫 번째 레벨), 두 번째 원소는 두 번째 레벨의 모든 노드 값의 평균 등입니다.

---

### 문제 요구사항
- 각 레벨의 노드들을 순회하며 해당 레벨의 노드 값들을 모두 더하고 노드의 개수로 나누어 평균을 구합니다.
- 반환되는 배열의 인덱스는 트리의 레벨과 일치하며, 평균 값은 소수점 이하도 포함됩니다.

---

### 접근 방법

1. **BFS(너비 우선 탐색) 이용:**
   - **아이디어:** 레벨 순회(level-order traversal)를 수행하여 각 레벨별로 노드를 처리합니다.
   - **절차:**
     1. 큐(Queue)를 사용해 루트 노드를 넣고 시작합니다.
     2. 큐가 빌 때까지 다음을 반복:
        - 현재 큐에 담긴 노드들이 한 레벨을 구성하므로, 이 레벨의 노드 개수를 확인합니다.
        - 각 노드를 꺼내면서 그 값들을 더하고, 자식 노드(왼쪽, 오른쪽)가 있다면 큐에 추가합니다.
     3. 해당 레벨의 합을 노드 개수로 나누어 평균을 구한 후 결과 배열에 추가합니다.
   - **시간 복잡도:** 모든 노드를 한 번씩 방문하므로 O(N)
   - **공간 복잡도:** 큐에 최대 한 레벨의 노드가 들어가므로 최악의 경우 O(N)

2. **DFS(깊이 우선 탐색) 이용:**
   - **아이디어:** 재귀를 통해 트리의 각 노드를 방문하며, 레벨별로 누적 합과 개수를 기록합니다.
   - **절차:**
     1. 재귀 함수에 현재 노드와 해당 레벨을 전달합니다.
     2. 각 레벨에 대해, 값의 합과 노드 개수를 저장할 배열이나 해시맵을 업데이트합니다.
     3. 모든 노드 방문 후, 각 레벨의 합을 해당 레벨의 노드 개수로 나누어 평균을 구합니다.
   - **시간 복잡도:** 모든 노드를 방문하므로 O(N)
   - **공간 복잡도:** 재귀 호출 스택 공간이 최대 트리의 높이만큼 필요하므로 O(H), H는 트리의 높이

---

### 코드 예시 (Python)

```python
from collections import deque

# BFS 접근법 예시
def averageOfLevels(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_sum = 0
        level_count = len(queue)
        for _ in range(level_count):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level_sum / level_count)
    
    return result
```

```python
# DFS 접근법 예시
def averageOfLevelsDFS(root):
    sums, counts = [], []
    
    def dfs(node, level):
        if not node:
            return
        if level < len(sums):
            sums[level] += node.val
            counts[level] += 1
        else:
            sums.append(node.val)
            counts.append(1)
        dfs(node.left, level + 1)
        dfs(node.right, level + 1)
    
    dfs(root, 0)
    return [s / c for s, c in zip(sums, counts)]
```

---

### 결론
이 문제는 이진 트리의 각 레벨에 대한 평균 값을 구하는 문제로, BFS 또는 DFS 방법으로 접근할 수 있습니다. BFS를 사용하면 레벨 단위로 자연스럽게 노드를 처리할 수 있고, DFS를 사용하면 재귀를 통해 레벨별 누적 합과 개수를 기록할 수 있습니다. 두 방법 모두 효율적이며, 문제의 요구사항에 맞게 평균 값을 배열 형태로 반환하면 됩니다.

---
