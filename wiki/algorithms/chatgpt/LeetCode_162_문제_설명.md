---
type: Concept
title: "LeetCode 162 문제 설명"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-07-03)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-07-03
status: active
---

# LeetCode 162 문제 설명

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-07-03

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
leetcode의 162. Find Peak Element 문제 설명해줘

### 💡 답변 (Assistant)
물론입니다! LeetCode 162번 문제 **"Find Peak Element"**는 **배열에서 피크(peak) 원소를 찾는** 문제입니다. 아래에 문제 설명, 예제, 그리고 해결 방법에 대해 정리해 드릴게요.

---

## 🔍 문제 설명

**문제 이름**: 162. Find Peak Element  
**난이도**: Medium  

> **배열 `nums`에서 피크 요소를 찾으세요.**
>
> 피크 요소란 **자기 양옆보다 큰 요소**를 의미합니다. 즉, `nums[i]`가 **`nums[i-1] < nums[i] > nums[i+1]`**이면 `nums[i]`는 피크 요소입니다.
>
> 배열이 경계에 도달하면, `nums[-1] = nums[n] = -∞` 라고 가정합니다.
>
> **하나 이상의 피크는 항상 존재합니다.**
>
> 정답이 여러 개일 수 있으며, 그 중 **아무 인덱스 하나만 리턴하면 됩니다.**

---

## 📘 입력 및 출력 형식

- **입력**: 정수 배열 `nums` (길이 `n`)
- **출력**: 피크 요소의 인덱스

---

## 🧪 예제

```python
Input: nums = [1, 2, 3, 1]
Output: 2
설명: nums[2] = 3은 nums[1] = 2, nums[3] = 1 보다 크므로 피크입니다.
```

```python
Input: nums = [1, 2, 1, 3, 5, 6, 4]
Output: 5
설명: nums[5] = 6은 nums[4] = 5, nums[6] = 4보다 크므로 피크입니다.
(또는 인덱스 2도 피크입니다. 여러 정답 허용)
```

---

## ⚙️ 제한사항

- `1 <= nums.length <= 1000`
- `-2^31 <= nums[i] <= 2^31 - 1`
- **인접한 값들은 같지 않다 (`nums[i] != nums[i+1]`)**

---

## 💡 해결 아이디어

### 1. **선형 탐색 (O(n))**
왼쪽부터 오른쪽으로 쭉 보면서 `nums[i] > nums[i+1]` 이면 `i`가 피크입니다.

```python
def findPeakElement(nums):
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            return i
    return len(nums) - 1
```

### 2. **이진 탐색 (O(log n)) – 추천 풀이**

배열 전체를 볼 필요 없이, **기울기를 기준으로 피크가 있는 방향으로만 이진 탐색**합니다.

```python
def findPeakElement(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1
    
    return left
```

#### 🔍 핵심 아이디어
- `nums[mid] < nums[mid+1]` 이면 오른쪽에 더 큰 값(즉, 피크)이 있다는 의미 → 오른쪽으로 이동
- `nums[mid] > nums[mid+1]` 이면 왼쪽에 피크가 있다는 의미 → 왼쪽으로 이동
- 언젠가는 하나의 인덱스만 남는데, 그것이 피크 인덱스

---

## 🧠 요약

- **피크 요소는 무조건 존재**한다.
- **O(n)** 풀이도 가능하지만, **O(log n)** 이진 탐색 풀이가 가장 효율적이다.
- 인접 원소가 항상 다르기 때문에, 중복에 대한 처리를 할 필요 없다.

---

더 궁금한 점이나 디버깅하고 싶은 코드가 있다면 알려주세요!

---
