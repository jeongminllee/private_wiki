---
type: Concept
title: "Leetcode 병합 두 리스트 분석"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-04-11)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-04-11
status: active
---

# Leetcode 병합 두 리스트 분석

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-04-11

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
이 코드는 두 개의 정렬된 연결 리스트를 하나의 정렬된 연결 리스트로 병합하는 Leetcode 문제 21 "Merge Two Sorted Lists"의 일반적인 해법입니다. 코드의 동작 원리와 핵심 포인트를 단계별로 분석하면 다음과 같습니다.

---

### 1. 초기 준비

- **더미 노드(dummy node) 생성**:  
  ```python
  dummy = ListNode()
  curr = dummy
  ```  
  - **목적**: 결과 리스트의 시작점을 쉽게 관리하기 위해 사용합니다. 더미 노드는 임시로 연결 리스트의 머리 역할을 하며, 실제 결과 리스트의 head는 `dummy.next`가 됩니다.
  - **참고**: 더미 노드는 edge case(예: 입력 리스트 중 하나가 비어있는 경우)를 다룰 때 유용합니다.

- **포인터 설정**:  
  - `curr`는 결과 리스트를 구성할 때 현재 노드를 가리키기 위한 포인터입니다.
  - 입력 리스트 `list1`과 `list2`는 정렬된 상태로 주어집니다.

---

### 2. 병합 과정 (While 루프)

- **반복 조건**:  
  ```python
  while list1 and list2 :
  ```  
  - 두 리스트 모두 노드가 남아있는 동안 반복합니다.

- **노드 비교와 연결**:
  ```python
  if list1.val > list2.val :
      curr.next = list2
      list2 = list2.next
  else :
      curr.next = list1
      list1 = list1.next
  curr = curr.next
  ```  
  - **비교**: 두 리스트의 현재 노드 값을 비교합니다.
    - 만약 `list1`의 값이 `list2`의 값보다 크면, `list2`의 노드를 결과 리스트에 연결하고 `list2` 포인터를 다음 노드로 이동합니다.
    - 그렇지 않으면 (`list1.val`이 작거나 같으면), `list1`의 노드를 결과 리스트에 연결하고 `list1` 포인터를 이동시킵니다.
  - **커서 이동**: 연결한 후, `curr` 포인터를 한 칸 옮겨 결과 리스트의 다음 연결 위치를 준비합니다.

---

### 3. 남은 노드 연결

- **하나의 리스트가 다 소진된 경우 처리**:
  ```python
  if list1 :
      curr.next = list1
  else :
      curr.next = list2
  ```  
  - 위의 반복문을 빠져나왔을 때, 두 리스트 중 하나가 완전히 소진되었지만 다른 하나는 여전히 노드가 남아 있을 수 있습니다.
  - 이 경우, 남아 있는 리스트는 이미 정렬된 상태이므로 그대로 결과 리스트에 이어 붙입니다.

---

### 4. 결과 반환

- **더미 노드의 다음 노드 반환**:
  ```python
  return dummy.next
  ```  
  - 최종적으로 더미 노드 뒤부터 연결된 실제 병합된 리스트의 헤드를 반환합니다.

---

### 5. 시간 복잡도와 공간 복잡도

- **시간 복잡도**:  
  - 두 리스트의 모든 노드를 한 번씩 처리하므로, 시간 복잡도는 O(n + m)입니다. (여기서 n과 m은 각각 list1과 list2의 노드 수)
  
- **공간 복잡도**:  
  - 추가적인 공간은 상수 공간(더미 노드와 몇 개의 포인터)만 사용하므로, O(1)의 추가 공간을 사용합니다.

---

### 6. 요약

- **핵심 아이디어**:  
  두 개의 포인터를 사용해 각 리스트에서 가장 작은 노드를 선택하며 새로운 정렬된 리스트를 구성합니다.
  
- **주요 이점**:  
  - 더미 노드를 사용하여 리스트의 첫 노드 처리를 간소화하였으며, 
  - 남은 노드를 한 번에 붙여주는 로직을 추가하여 간결하고 효율적인 병합을 구현했습니다.

이와 같은 방식은 연결 리스트 문제에서 자주 사용되는 테크닉이며, 코드 자체도 직관적이면서도 효율적인 해법을 제공합니다.

---

### ❓ 질문 (User)
```
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        curr = dummy

        while list1 and list2 :
            if list1.val > list2.val :
                curr.next = list2
                list2 = list2.next
            else :
                curr.next = list1
                list1 = list1.next

            curr = curr.next

        if list1 :
            curr.next = list1
        else :
            curr.next = list2

        return dummy.next
```
Leetcode 의 21 Merge Two Sorted Lists 의 해답 코드야. 분석해줘.
