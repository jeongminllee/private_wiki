---
type: Concept
title: "Binary Watch Explanation"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-08-01)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-08-01
status: active
---

# Binary Watch Explanation

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-08-01

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
leetcode 401. binary watch 문제 해설해줘

### 💡 답변 (Assistant)
Leetcode 문제 401번 "Binary Watch"는 주어진 케이스에서 켜져 있는 LED의 개수를 이용하여 가능한 모든 시간을 출력하는 문제입니다. 이 문제를 해결하기 위해서는 LED의 개수와 시간의 관계를 잘 이해해야 합니다.

## 문제 설명

Binary Watch는 총 10개의 LED로 구성됩니다:
- 4개의 LED는 시(hour)를 나타냅니다.
- 6개의 LED는 분(minute)을 나타냅니다.

각 LED가 나타내는 값은 다음과 같습니다:
- 시간의 LED는 각각 1, 2, 4, 8을 나타냅니다. (0~11 사이의 값을 가질 수 있음)
- 분의 LED는 각각 1, 2, 4, 8, 16, 32를 나타냅니다. (0~59 사이의 값을 가질 수 있음)

주어진 `turnedOn`이라는 변수는 켜져 있는 LED의 수를 나타냅니다. 켜져 있는 LED의 개수가 `turnedOn`일 때 가능한 모든 시간을 문자열 형식으로 반환하는 것이 목표입니다.

## 접근 방법

1. **모든 가능한 시간 탐색**: 시간을 나타내는 4개의 LED와 분을 나타내는 6개의 LED의 모든 조합을 탐색합니다.
2. **켜져 있는 LED의 개수 세기**: 현재 조합에서 켜져 있는 LED의 개수를 세고, 이것이 `turnedOn`과 일치하는지 확인합니다.
3. **유효한 시간 확인**: 시간이 0~11 범위에 있고, 분이 0~59 범위에 있는지 확인합니다.
4. **결과 형식 맞추기**: 유효한 시간과 분을 적절한 형식 (예: "h:mm" 형식)으로 변환합니다.

## 코드 구현

```python
def readBinaryWatch(turnedOn):
    def countBits(n):
        # n의 이진수 표현에서 1의 개수를 센다.
        return bin(n).count('1')
    
    result = []
    
    # 가능한 모든 시간 (h: 0~11)과 분 (m: 0~59) 조합 탐색
    for h in range(12):
        for m in range(60):
            # 켜져 있는 LED의 개수가 turnedOn과 일치하면 결과에 추가
            if countBits(h) + countBits(m) == turnedOn:
                result.append(f"{h}:{m:02d}")
    
    return result
```

## 설명

1. `countBits` 함수는 주어진 숫자 `n`의 이진수 표현에서 1의 개수를 세는 함수입니다. 이를 통해 현재 시간과 분에서 켜져 있는 LED의 개수를 계산할 수 있습니다.
2. `readBinaryWatch` 함수에서는 가능한 모든 시간(0~11)과 분(0~59)을 순회합니다.
3. 각 시간과 분 조합에서 켜져 있는 LED의 총 개수를 계산하고, 이 값이 `turnedOn`과 일치하면 결과 리스트에 추가합니다.
4. 시간과 분을 "h:mm" 형식으로 포맷팅하여 결과 리스트에 추가합니다.
5. 모든 조합을 확인한 후 결과 리스트를 반환합니다.

이 접근 방식은 모든 가능한 조합을 확인하기 때문에 브루트 포스 방법입니다. 하지만 시간과 분의 범위가 작기 때문에 (12 * 60 = 720가지 조합) 성능 문제는 없습니다.

---
