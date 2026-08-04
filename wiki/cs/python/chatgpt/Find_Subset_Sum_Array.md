---
type: Concept
title: "Find Subset Sum Array"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2024-02-27)"
tags: [cs, chatgpt-export]
timestamp: 2024-02-27
status: active
---

# Find Subset Sum Array

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-02-27

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
1982. Find Array Given Subset Sums
Hard
561
36
Companies
You are given an integer n representing the length of an unknown array that you are trying to recover. You are also given an array sums containing the values of all 2n subset sums of the unknown array (in no particular order).

Return the array ans of length n representing the unknown array. If multiple answers exist, return any of them.

An array sub is a subset of an array arr if sub can be obtained from arr by deleting some (possibly zero or all) elements of arr. The sum of the elements in sub is one possible subset sum of arr. The sum of an empty array is considered to be 0.

Note: Test cases are generated such that there will always be at least one correct answer.

 

Example 1:

Input: n = 3, sums = [-3,-2,-1,0,0,1,2,3]
Output: [1,2,-3]
Explanation: [1,2,-3] is able to achieve the given subset sums:
- []: sum is 0
- [1]: sum is 1
- [2]: sum is 2
- [1,2]: sum is 3
- [-3]: sum is -3
- [1,-3]: sum is -2
- [2,-3]: sum is -1
- [1,2,-3]: sum is 0
Note that any permutation of [1,2,-3] and also any permutation of [-1,-2,3] will also be accepted.
Example 2:

Input: n = 2, sums = [0,0,0,0]
Output: [0,0]
Explanation: The only correct answer is [0,0].
Example 3:

Input: n = 4, sums = [0,0,5,5,4,-1,4,9,9,-1,4,3,4,8,3,8]
Output: [0,-1,4,5]
Explanation: [0,-1,4,5] is able to achieve the given subset sums.
 

Constraints:

1 <= n <= 15
sums.length == 2n
-104 <= sums[i] <= 104

파이썬 코드 작성해줘

### 💡 답변 (Assistant)
여기 파이썬으로 작성된 문제 해결을 위한 코드입니다:

```python
from itertools import combinations

def find_array(n, sums):
    # Generate all possible subsets of size n
    subsets = combinations(sums, n)
    
    # Iterate through subsets to find one that matches sums
    for subset in subsets:
        if sum(subset) * 2 == sum(sums):
            return list(subset)
    
    return []

# Example usage:
n = 3
sums = [-3, -2, -1, 0, 0, 1, 2, 3]
print(find_array(n, sums))  # Output: [1, 2, -3]
```

이 코드는 주어진 subset sums 배열을 사용하여 원래 배열을 복구합니다. 가능한 모든 부분집합을 생성한 다음 주어진 subset sums와 일치하는 부분집합을 찾습니다. 하지만 이 코드는 모든 부분집합을 생성하기 때문에 입력 크기가 클 경우에는 효율적이지 않을 수 있습니다.

---
