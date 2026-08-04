---
type: Concept
title: "Python itertools Permutation Implementation"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-11-29)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-11-29
status: active
---

# Python itertools Permutation Implementation

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-11-29

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
itertools의 permutation 라이브러리 내부 구조를 파이썬 코드로 구현해줘

### 💡 답변 (Assistant)
`itertools.permutations`는 주어진 iterable에서 가능한 모든 순열을 생성하는 반복자(iterator)를 제공합니다. 아래는 Python으로 구현한 `itertools.permutations`와 유사한 동작을 하는 코드입니다.

```python
def permutations(iterable, r=None):
    # Convert input to a tuple to allow index-based operations
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r  # Set default r to len(iterable) if not provided
    if r > n:
        return  # If r > n, no permutations are possible
    
    indices = list(range(n))  # Indices of the input iterable
    cycles = list(range(n, n - r, -1))  # Cycle lengths for each position in the permutation
    yield tuple(pool[i] for i in indices[:r])  # Yield the first permutation
    
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1  # Decrease the current cycle
            if cycles[i] == 0:
                # Cycle is finished; rotate indices to the left and reset the cycle length
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                # Swap the i-th index with the next index in the cycle
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])  # Yield the next permutation
                break
        else:
            # If no break occurred, all cycles are complete, and we exit
            return
```

### 설명
1. **입력 변환**:
   - 입력된 iterable은 `tuple`로 변환하여 순서를 보장하고, index 기반의 접근을 가능하게 합니다.

2. **초기화**:
   - `indices`: iterable의 인덱스를 나타냅니다.
   - `cycles`: 순열을 생성하기 위해 각 위치에서의 회전 길이를 설정합니다.

3. **순열 생성**:
   - 첫 번째 순열은 `indices`의 처음 `r`개의 인덱스를 사용하여 생성됩니다.
   - `cycles` 값이 감소되며, 순열의 다음 요소를 생성하기 위해 인덱스의 순서를 조정합니다.

4. **종료 조건**:
   - 모든 `cycles` 값이 0이 되면 순열 생성이 종료됩니다.

### 사용 예시
```python
for perm in permutations('ABCD', 2):
    print(perm)
```

**출력**:
```
('A', 'B')
('A', 'C')
('A', 'D')
('B', 'A')
('B', 'C')
('B', 'D')
('C', 'A')
('C', 'B')
('C', 'D')
('D', 'A')
('D', 'B')
('D', 'C')
```

이 구현은 `itertools.permutations`의 동작을 충실히 모방하며, 효율적인 메모리 사용과 lazy evaluation을 지원합니다.

---

### 💡 답변 (Assistant)
`itertools.permutations`는 주어진 iterable에서 가능한 순열을 생성하는 Python의 내장 함수입니다. 이 함수는 메모리를 효율적으로 사용하며, 실제로 `yield`를 통해 순열을 하나씩 생성합니다. 다음은 Python으로 `itertools.permutations`의 동작 방식을 구현한 코드입니다.

```python
def permutations(iterable, r=None):
    # 입력을 튜플로 변환하여 다루기 쉽게 함
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return  # r이 n보다 크면 순열을 만들 수 없으므로 종료

    # 위치를 나타낼 인덱스 배열 생성
    indices = list(range(n))
    cycles = list(range(n, n - r, -1))  # r개의 순열 생성

    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                # i번째 위치의 인덱스를 마지막으로 이동
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                # 현재 위치와 cycles에 따라 교환
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return  # 모든 순열을 생성하면 종료

# 테스트
for p in permutations('ABC', 2):
    print(p)
```

### 주요 동작 원리:
1. **Initialization (초기화)**: 
   - `pool`: iterable을 튜플로 변환하여 저장.
   - `indices`: 순열 생성에 사용할 인덱스 리스트.
   - `cycles`: 각 위치에서 남은 반복 횟수를 추적하는 리스트.

2. **첫 번째 순열 생성**: `indices[:r]`를 기반으로 첫 번째 순열을 생성.

3. **순열 생성**:
   - 뒤에서부터 `cycles` 값을 감소시키며, 각 자리의 값을 순환시킴.
   - `indices`를 교환하여 다음 순열 생성.

4. **종료 조건**:
   - 모든 `cycles` 값이 0이 되면, 더 이상 생성할 순열이 없으므로 종료.

이 구현은 메모리를 효율적으로 사용하며, 생성기(generator)를 사용해 순열을 하나씩 생성합니다. `itertools.permutations`의 동작과 동일합니다.

---

### ❓ 질문 (User)
Given a collection of numbers, nums, that might contain duplicates, return all possible unique permutations in any order.

 

Example 1:

Input: nums = [1,1,2]
Output:
[[1,1,2],
 [1,2,1],
 [2,1,1]]
Example 2:

Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
이 문제를 파이썬 코드로 구현해줘

### 💡 답변 (Assistant)
중복된 요소를 처리하고 고유한 순열을 생성하려면 백트래킹과 정렬을 활용하여 구현할 수 있습니다. 아래는 이를 구현한 Python 코드입니다.

```python
def unique_permutations(nums):
    def backtrack(path, used):
        # If the path length equals nums length, we've formed a full permutation
        if len(path) == len(nums):
            result.append(path[:])  # Append a copy of the path
            return
        
        for i in range(len(nums)):
            # Skip used elements or duplicates (only the first unused duplicate is valid)
            if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]):
                continue
            
            # Mark this element as used
            used[i] = True
            path.append(nums[i])
            
            # Recursively backtrack with the updated path
            backtrack(path, used)
            
            # Undo the choice (backtrack)
            path.pop()
            used[i] = False

    nums.sort()  # Sort to handle duplicates easily
    result = []
    backtrack([], [False] * len(nums))
    return result

# Example usage:
nums1 = [1, 1, 2]
print(unique_permutations(nums1))

nums2 = [1, 2, 3]
print(unique_permutations(nums2))
```

### 설명
1. **정렬**:
   - 입력 배열 `nums`를 정렬하여 중복 요소가 인접하도록 합니다. 이를 통해 중복 순열을 쉽게 제거할 수 있습니다.

2. **백트래킹**:
   - `path`는 현재까지 선택한 요소를 나타냅니다.
   - `used`는 각 요소가 현재 사용되었는지를 추적하는 boolean 배열입니다.

3. **중복 제거**:
   - `nums[i] == nums[i - 1]` 조건을 통해 중복된 요소를 건너뜁니다. 그러나 이전 요소가 사용 중(`not used[i - 1]`)이라면, 중복 처리 로직은 무시됩니다.

4. **결과 저장**:
   - `path`의 길이가 `nums`와 같아지면 완전한 순열이므로 `result`에 저장합니다.

5. **백트래킹 해제**:
   - 요소를 제거하고(`path.pop()`), `used`를 다시 `False`로 설정하여 다른 경로를 탐색합니다.

### 입력 및 출력 예시
#### 입력:
```python
nums1 = [1, 1, 2]
```

#### 출력:
```python
[[1, 1, 2], [1, 2, 1], [2, 1, 1]]
```

#### 입력:
```python
nums2 = [1, 2, 3]
```

#### 출력:
```python
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
```

이 코드는 중복된 숫자를 포함한 배열에서도 고유한 순열을 생성하며 효율적으로 동작합니다.

---

### ❓ 질문 (User)
set()을 활용한 풀이도 구현해줘

### 💡 답변 (Assistant)
`set()`을 활용하면 중복된 순열을 쉽게 제거할 수 있습니다. 모든 순열을 생성한 후, 이를 `set`에 넣어 중복을 없앤 다음 다시 리스트로 변환하여 결과를 반환하는 방식입니다.

아래는 `set()`을 활용한 Python 구현입니다.

```python
from itertools import permutations

def unique_permutations(nums):
    # Use itertools.permutations to generate all permutations
    all_perms = permutations(nums)
    # Use a set to filter out duplicate permutations
    unique_perms = set(all_perms)
    # Convert the set back to a list of lists
    return [list(perm) for perm in unique_perms]

# Example usage:
nums1 = [1, 1, 2]
print(unique_permutations(nums1))

nums2 = [1, 2, 3]
print(unique_permutations(nums2))
```

### 설명
1. **`itertools.permutations`**:
   - 모든 가능한 순열을 생성합니다. 결과는 튜플의 형태로 반환됩니다.

2. **중복 제거**:
   - 생성된 순열을 `set`에 넣으면 중복된 튜플이 제거됩니다.

3. **형식 변환**:
   - `set`에 있는 고유한 순열 튜플을 리스트로 변환하여 최종 결과를 반환합니다.

### 입력 및 출력 예시
#### 입력:
```python
nums1 = [1, 1, 2]
```

#### 출력:
```python
[[1, 2, 1], [2, 1, 1], [1, 1, 2]]
```

#### 입력:
```python
nums2 = [1, 2, 3]
```

#### 출력:
```python
[[1, 3, 2], [3, 1, 2], [2, 3, 1], [2, 1, 3], [3, 2, 1], [1, 2, 3]]
```

### 장점
- 구현이 간단하며, 코드가 짧고 직관적입니다.
- `set`이 자동으로 중복을 처리해주므로 중복 제거를 위한 추가 로직이 필요 없습니다.

### 단점
- 모든 순열을 생성한 뒤에 중복을 제거하기 때문에, 입력 크기가 커질 경우 메모리 사용량이 늘어날 수 있습니다.

이 방식은 간결하지만, 중복 제거를 즉시 처리하지 않으므로 메모리 효율성보다는 코드 간결성을 우선하는 상황에 적합합니다.

---
