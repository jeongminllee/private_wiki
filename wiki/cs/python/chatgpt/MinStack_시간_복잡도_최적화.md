---
type: Concept
title: "MinStack 시간 복잡도 최적화"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2025-08-31)"
tags: [cs, chatgpt-export]
timestamp: 2025-08-31
status: active
---

# MinStack 시간 복잡도 최적화

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-08-31

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
class MinStack:
    def __init__(self):
        self.minstack = []

    def push(self, val: int) -> None:
        return self.minstack.append(val)

    def pop(self) -> None:
        return self.minstack.pop()

    def top(self) -> int:
        return self.minstack[-1]

    def getMin(self) -> int:
        return min(self.minstack)


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```
다음 함수를 하나 만들었어. 여기서 시간복잡도가 O(1)이 되도록 하는 것에 방해가 되는 부분을 가르쳐주고, 해결방안도 가르쳐줘.

### 💡 답변 (Assistant)
가장 큰 병목은 `getMin()`이에요.  
`return min(self.minstack)`는 매 호출마다 스택 전체를 스캔하므로 **O(n)** 이 됩니다. 나머지 `push/pop/top`은 O(1)인데, `getMin` 때문에 전체 요구 조건(모든 연산 O(1))을 깨요.

고치는 방법은 “현재까지의 최소값”을 함께 저장해 두는 겁니다. 대표적인 두 가지 패턴을 보여드릴게요.

---

# 1) (값, 그 시점의 최소값)으로 함께 저장 (가장 간단)
```python
class MinStack:
    def __init__(self):
        self.stack = []  # 각 원소: (val, cur_min)

    def push(self, val: int) -> None:
        cur_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, cur_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```
- 아이디어: i번째 원소를 넣을 때 그 시점의 최소값을 같이 저장.  
- 복잡도: 모든 연산 **O(1)**, 공간 **O(n)**.

---

# 2) 값 스택 + 최소 스택(카운트 포함) 두 개 쓰기
중복 최소값을 효율적으로 다루고 싶다면 최소 스택에 **(최소값, 개수)**를 저장합니다.
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # 각 원소: [min_val, count]

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val < self.min_stack[-1][0]:
            self.min_stack.append([val, 1])
        elif val == self.min_stack[-1][0]:
            self.min_stack[-1][1] += 1

    def pop(self) -> None:
        v = self.stack.pop()
        if v == self.min_stack[-1][0]:
            self.min_stack[-1][1] -= 1
            if self.min_stack[-1][1] == 0:
                self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1][0]
```
- 아이디어: 현재 최소값이 여러 번 들어왔을 때 카운트만 올리고, pop 시 카운트를 줄여 0이면 제거.  
- 복잡도: 역시 모든 연산 **O(1)**, 공간 **O(n)**(중복이 많을수록 이 방식이 메모리를 조금 절약).

---

## 요약
- 문제점: `getMin()`이 `min()` 호출로 **O(n)**.  
- 해결: 스택에 “그 시점의 최소값”을 같이 관리하거나, 보조 최소 스택을 유지해서 **모든 연산 O(1)** 달성.  
- 실무/코테에선 1) 튜플 저장 방식이 구현이 가장 간단하고 안전합니다.

---
