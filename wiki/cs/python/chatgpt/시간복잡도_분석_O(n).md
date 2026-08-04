---
type: Concept
title: "시간복잡도 분석: O(n)"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2024-06-09)"
tags: [cs, chatgpt-export]
timestamp: 2024-06-09
status: active
---

# 시간복잡도 분석: O(n)

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-06-09

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
def solution(answers) :
    # 수포자마다의 규칙을 정의
    patterns = [
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
    ]
    
    # 수포자 정답 리스트
    results = [0] * 3

    # 정답에 해당하는 키-값을 설정
    for i, answer in enumerate(answers) :
        # 각 수포자의 패턴을 키-값으로 설정
        for j, pattern in enumerate(patterns) :
            # 맞아 떨어지면
            if answer == pattern[i % len(pattern)] :
                # 각 수포자의 리스트에 +1
                results[j] += 1

    max_result = max(results)
    # 세 수포자의 정답을 가장 많이 맞춘 사람을 담는 리스트 생성
    highest_results = []
    
    for i, result in enumerate(results) :
        # 정답을 가장 많이 맞춘 사람이라면
        if result == max_result :
            # 최대 정답자를 정답 리스트에 삽입(리스트 0 부터 시작이니까 i+1)
            highest_results.append(i + 1)

    return highest_results

해당 코드의 시간복잡도를 분석해줘

### 💡 답변 (Assistant)
The given code solves the problem of finding the person (or people) who got the most answers correct out of three contestants, each following a specific repeating pattern. Let's analyze its time complexity step by step.

### Key Operations and Time Complexity Analysis

1. **Defining Patterns**:
    ```python
    patterns = [
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
    ]
    ```
    - This is a constant-time operation, \( O(1) \).

2. **Initialization of Results**:
    ```python
    results = [0] * 3
    ```
    - This is also a constant-time operation, \( O(1) \).

3. **Loop Over Answers**:
    ```python
    for i, answer in enumerate(answers):
        for j, pattern in enumerate(patterns):
            if answer == pattern[i % len(pattern)]:
                results[j] += 1
    ```
    - The outer loop runs \( n \) times, where \( n \) is the length of `answers`.
    - Inside this loop, there is a second loop that iterates over `patterns`, which always has a length of 3 (a constant).
    - The comparison `answer == pattern[i % len(pattern)]` and the increment operation `results[j] += 1` are both constant-time operations, \( O(1) \).

    Thus, the nested loops together run in \( O(n) \) time.

4. **Finding the Maximum**:
    ```python
    max_result = max(results)
    ```
    - The list `results` has a constant size of 3, so finding the maximum element takes constant time, \( O(1) \).

5. **Identifying the Highest Results**:
    ```python
    highest_results = []
    for i, result in enumerate(results):
        if result == max_result:
            highest_results.append(i + 1)
    ```
    - The loop runs a constant number of times (3 iterations), hence \( O(1) \).
    - Checking `result == max_result` and appending to `highest_results` are constant-time operations, \( O(1) \).

### Overall Time Complexity
Combining all these operations, the most time-consuming part is the loop over the `answers`, which operates in \( O(n) \) time. All other operations (initialization, finding the maximum, and identifying the highest results) are constant-time operations.

Thus, the overall time complexity of the solution is:
\[ O(n) \]

Where \( n \) is the number of elements in the `answers` list.

---
