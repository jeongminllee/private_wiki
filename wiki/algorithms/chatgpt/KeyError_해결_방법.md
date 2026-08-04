---
type: Concept
title: "KeyError 해결 방법"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-02-12)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-02-12
status: active
---

# KeyError 해결 방법

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-02-12

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
from typing import List
class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], indexDiff: int, valueDiff: int) -> bool:
        hash_idx = {}
        hash_val = {}

        for idx, val in enumerate(nums):
            if hash_idx is None:
                hash_idx[val] = idx
                hash_val[idx] = val
                continue

            if (val in hash_val and \
                    abs(idx - hash_idx[val]) <= indexDiff and \
                    abs(val - hash_val[hash_idx[val]]) == valueDiff):
                return True

            hash_idx[val] = idx
            hash_val[idx] = val

        return False

print(Solution().containsNearbyAlmostDuplicate([1,0,1,1], 1, 2))
```

Traceback (most recent call last):
  File "~/Baekjoon/main.py", line 38, in <module>
    print(Solution().containsNearbyAlmostDuplicate([1,0,1,1], 1, 2))
  File "~/Baekjoon/main.py", line 29, in containsNearbyAlmostDuplicate
    abs(idx - hash_idx[val]) <= indexDiff and \
KeyError: 0

이런 애러가 나오네. 에러에 대해서 설명해주고, 해결책에 대해서 알려줘.

### 💡 답변 (Assistant)
좋습니다. 에러의 **정확한 원인**부터 짚고 가겠습니다.

---

# ✅ 1️⃣ 왜 `KeyError: 0` 가 발생하는가?

문제가 발생한 줄:

```python
abs(idx - hash_idx[val]) <= indexDiff
```

에러 메시지:
```
KeyError: 0
```

즉,

```python
hash_idx[val]
```

에서 `val = 0` 인데  
`hash_idx`에 `0`이라는 key가 존재하지 않는 상태입니다.

---

## 🔎 코드 흐름을 따라가보면

입력:
```python
[1, 0, 1, 1]
```

초기 상태:
```python
hash_idx = {}
hash_val = {}
```

### 🔹 첫 번째 반복 (idx=0, val=1)

```python
if hash_idx is None:
```

❗ 문제점:  
`hash_idx`는 `{}` 이지 `None`이 아닙니다.

따라서 이 조건은 **항상 False** 입니다.

즉, 첫 원소도 그냥 아래 로직으로 내려갑니다.

---

### 🔹 두 번째 반복 (idx=1, val=0)

이 시점에서:

```python
hash_idx = {1: 0}
hash_val = {0: 1}
```

이제 조건문으로 들어갑니다:

```python
if (val in hash_val and ...
```

여기서 문제:

```python
val in hash_val
```

- `hash_val`의 key는 **index**
- 그런데 `val`은 값

즉, 구조가 뒤섞여 있습니다.

---

# ✅ 핵심 문제 2가지

### ① `hash_idx is None` 조건이 잘못됨
딕셔너리는 빈 경우 `{}`이지 `None`이 아닙니다.

### ② `hash_idx` / `hash_val` 구조가 논리적으로 꼬여 있음

- `hash_idx[val] = idx`
- `hash_val[idx] = val`

그런데 검사할 때는

```python
val in hash_val   # 잘못된 비교
```

입니다.

---

# ✅ 더 중요한 문제 (논리 오류)

문제 조건은:

> |i - j| ≤ indexDiff  
> |nums[i] - nums[j]| ≤ valueDiff

그런데 코드에서는:

```python
abs(val - hash_val[...]) == valueDiff
```

❗ `==` 가 아니라 `<=` 이어야 합니다.

---

# 🚨 근본적 해결책

이 문제는 단순 hash 비교로는 해결이 어렵습니다.

왜냐하면

- index 범위 제한
- value 범위 제한

두 조건을 동시에 만족해야 하기 때문입니다.

---

# ✅ 가장 올바른 해결법: Bucket 방식 (O(n))

LeetCode에서 이 문제의 정석 해법입니다.

아이디어:

- valueDiff+1 크기의 bucket을 만든다
- 같은 bucket 안에 있으면 value 차이는 무조건 ≤ valueDiff
- 인접 bucket도 체크

---

## ✔ 수정된 올바른 코드

```python
from typing import List

class Solution:
    def containsNearbyAlmostDuplicate(
        self, nums: List[int], indexDiff: int, valueDiff: int
    ) -> bool:

        if valueDiff < 0:
            return False

        bucket = {}
        width = valueDiff + 1

        for i, num in enumerate(nums):

            bucket_id = num // width

            # 같은 bucket
            if bucket_id in bucket:
                return True

            # 왼쪽 bucket
            if (bucket_id - 1 in bucket and
                abs(num - bucket[bucket_id - 1]) <= valueDiff):
                return True

            # 오른쪽 bucket
            if (bucket_id + 1 in bucket and
                abs(num - bucket[bucket_id + 1]) <= valueDiff):
                return True

            bucket[bucket_id] = num

            # indexDiff 초과 제거 (sliding window)
            if i >= indexDiff:
                old_bucket_id = nums[i - indexDiff] // width
                del bucket[old_bucket_id]

        return False
```

---

# 📌 정리

### 🔴 당신 코드의 에러 원인

1. `hash_idx is None` → 잘못된 조건
2. `val in hash_val` → key 구조 오류
3. `hash_idx[val]` 접근 시 key 없음 → KeyError
4. `== valueDiff` → 문제 조건과 다름

---

# 🎯 추가 조언

이 문제는 단순 dict로는 안 됩니다.

- Sliding window
- Bucket hashing
- 또는 SortedList (Tree 구조)

중 하나가 필요합니다.

---

원하시면:

- 🔍 bucket 방식 원리 수학적으로 설명
- 📊 시간복잡도 증명
- 🧠 naive → 개선 과정 단계별 설명
- ❌ 왜 단순 hash는 안 되는지 반례 설명

어디까지 깊게 들어갈까요?

---
