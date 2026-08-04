---
type: Concept
title: "Linear runtime 설명"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-08-01)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-08-01
status: active
---

# Linear runtime 설명

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-08-01

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
You must implement a solution with a linear runtime complexity and use only constant extra space.
리트코드 Single Number 문제에 제시되어 있던 문장이야. 이 문장이 무슨 말인지 설명해줘

### 💡 답변 (Assistant)
리트코드 **Single Number** 문제에 제시된 문장:

> "You must implement a solution with a linear runtime complexity and use only constant extra space."

이 문장은 문제를 풀 때 **시간 복잡도와 공간 복잡도**에 대한 **제약 조건**을 말합니다. 하나씩 풀어서 설명해드릴게요:

---

### 🔹 1. **Linear Runtime Complexity**
- **뜻**: 알고리즘의 실행 시간이 입력 크기 \( n \)에 비례해야 한다는 뜻입니다.
- **Big-O 표기**: \( O(n) \)
- **예시**:
  - 한 번의 `for` 루프로 배열 전체를 순회하는 것 → ✅
  - 배열을 정렬하는 것 → ❌ (정렬은 보통 \( O(n \log n) \)이므로 조건을 만족하지 않음)

---

### 🔹 2. **Constant Extra Space**
- **뜻**: 입력 배열을 제외하고, 추가로 사용하는 **메모리 공간이 고정되어야 한다**는 의미입니다.
- **Big-O 표기**: \( O(1) \)
- **예시**:
  - 변수를 몇 개 선언해서 쓰는 건 괜찮음 → ✅
  - 해시셋이나 딕셔너리를 사용해서 여러 값을 저장하는 건 입력 크기에 따라 공간이 늘어나므로 안 됨 → ❌

---

### 🔹 요약
이 문장은 다음을 의미합니다:

> "입력 배열을 **한 번만** 순회하면서(=선형 시간), **추가 메모리를 거의 사용하지 않고** 정답을 찾아라."

---

### 🔹 Single Number 문제에 적용하면?
배열에서 **오직 하나만 한 번 등장하고 나머지는 모두 두 번씩 등장**하는 수를 찾는 문제죠.

이 조건을 만족하면서 풀 수 있는 대표적인 방법은 **XOR 비트 연산**을 사용하는 것입니다:

```python
def singleNumber(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

- 이 방법은 **한 번의 루프**만 돌고 → \( O(n) \)
- 변수 `result` 하나만 쓰므로 **공간도 \( O(1) \)** → 조건 모두 만족 ✅

---

필요하시면 XOR 연산을 이용한 풀이 아이디어도 설명해드릴게요.

---
