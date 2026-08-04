---
type: Concept
title: "Next Permutation Algorithm"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-11-29)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-11-29
status: active
---

# Next Permutation Algorithm

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-11-29

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
A permutation of an array of integers is an arrangement of its members into a sequence or linear order.

For example, for arr = [1,2,3], the following are all the permutations of arr: [1,2,3], [1,3,2], [2, 1, 3], [2, 3, 1], [3,1,2], [3,2,1].
The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).

For example, the next permutation of arr = [1,2,3] is [1,3,2].
Similarly, the next permutation of arr = [2,3,1] is [3,1,2].
While the next permutation of arr = [3,2,1] is [1,2,3] because [3,2,1] does not have a lexicographical larger rearrangement.
Given an array of integers nums, find the next permutation of nums.

The replacement must be in place and use only constant extra memory.

 

Example 1:

Input: nums = [1,2,3]
Output: [1,3,2]
Example 2:

Input: nums = [3,2,1]
Output: [1,2,3]
Example 3:

Input: nums = [1,1,5]
Output: [1,5,1]
 

Constraints:

1 <= nums.length <= 100
0 <= nums[i] <= 100
---
파이썬 코드를 작성해줘

### 💡 답변 (Assistant)
아래는 주어진 문제를 해결하는 파이썬 코드입니다. 이 코드는 배열을 "다음 순열"로 변환하는 알고리즘을 구현합니다. **O(n)** 시간 복잡도로 작동하며, 상수 크기의 추가 메모리만 사용합니다.

---

### 💡 답변 (Assistant)
### 코드 설명:
1. **첫 번째 감소 요소 찾기**:
   - 오른쪽에서 왼쪽으로 탐색하여 처음으로 `nums[i] < nums[i + 1]`를 만족하는 `i`를 찾습니다.
   - 이 지점까지는 배열이 비내림차순으로 정렬되어 있음을 의미합니다.

2. **교환 가능한 작은 값 찾기**:
   - 오른쪽에서 왼쪽으로 탐색하며, `nums[j] > nums[i]`를 만족하는 가장 작은 인덱스 `j`를 찾습니다.

3. **교환**:
   - `nums[i]`와 `nums[j]`를 교환합니다.

4. **뒷부분 정렬**:
   - `i+1` 이후의 모든 요소를 역순으로 정렬합니다. 이는 사전식으로 가장 작은 배열을 보장합니다.

위 코드는 입력 배열을 수정하여 다음 순열을 반환합니다. `print`를 통해 다양한 입력값을 확인할 수 있습니다.

---
