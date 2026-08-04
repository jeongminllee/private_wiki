---
type: Concept
title: "New chat"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-02-13)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-02-13
status: active
---

# New chat

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-02-13

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
def main() :
    N = int(input())
    H = list(map(int, input().split()))
    tour = {}
    res = 0

    for idx, height in enumerate(H):
        if 0 < idx < (N - 1) :
            if tour[idx - 1] < height and tour[idx + 1] < height :
                res += 1
        tour[idx] = height

    return res

if __name__ == "__main__" :
    T = int(input())
    for test_case in range(1,T+1) :
        print(f"Case #{test_case}: {main()}")
```

4
3
10 20 14
4
7 7 7 7
5
10 90 20 90 10
3
10 3 10
    if tour[idx - 1] < height and tour[idx + 1] < height :
KeyError: 2

무슨 에러인지 모르겠네

### 💡 답변 (Assistant)
좋습니다. 이 에러는 **자료구조 사용 순서 문제**입니다.  
결론부터 말하면:

> `tour[idx + 1]` 이 아직 딕셔너리에 존재하지 않기 때문에 `KeyError` 가 발생한 것입니다.

---

## 🔎 왜 KeyError 가 발생하는가?

당신 코드의 핵심 부분:

```python
for idx, height in enumerate(H):
    if 0 < idx < (N - 1) :
        if tour[idx - 1] < height and tour[idx + 1] < height :
            res += 1
    tour[idx] = height
```

### 실행 순서를 보겠습니다.

예시 입력:
```
3
10 20 14
```

반복 흐름:

| idx | height | tour 상태 | 검사 가능? |
|------|--------|------------|------------|
| 0 | 10 | {} | X |
| 1 | 20 | {0:10} | **여기서 검사 시도** |
| 2 | 14 | {0:10,1:20} | |

### idx = 1 일 때

```python
tour[idx - 1]  # tour[0] → OK
tour[idx + 1]  # tour[2] → ❌ 아직 없음
```

`tour[2]` 는 아직 저장되지 않았기 때문에

```
KeyError: 2
```

이 발생합니다.

---

## 📌 근본 원인

딕셔너리 `tour` 는 **왼쪽 값만 저장된 상태에서 오른쪽 값을 참조하려고 하기 때문**입니다.

즉,

> 오른쪽 이웃(height at idx+1)은 아직 딕셔너리에 저장되지 않았습니다.

---

## 💡 해결 방법

### ✔ 방법 1 — 딕셔너리 사용하지 않기 (가장 깔끔)

이미 리스트 `H` 가 있는데 굳이 딕셔너리 필요 없습니다.

```python
def main():
    N = int(input())
    H = list(map(int, input().split()))
    res = 0

    for idx in range(1, N-1):
        if H[idx-1] < H[idx] and H[idx+1] < H[idx]:
            res += 1

    return res
```

이게 정답 구조입니다.

---

### ✔ 방법 2 — 딕셔너리를 먼저 채우고 검사

```python
tour = {i: h for i, h in enumerate(H)}

for idx in range(1, N-1):
    if tour[idx-1] < tour[idx] and tour[idx+1] < tour[idx]:
        res += 1
```

하지만 이 문제에서는 딕셔너리 자체가 필요 없습니다.

---

## 📘 문제의 본질

이 문제는 **양 옆보다 큰 값(peak) 개수 세기** 입니다.

시간복잡도:
```
O(N)
```

추가 공간:
```
O(1)
```

딕셔너리를 쓰면 오히려 복잡해집니다.

---

## 🎯 한 줄 요약

> KeyError는 존재하지 않는 키(`idx+1`)를 딕셔너리에서 조회했기 때문에 발생한 것입니다.  
> 이 문제는 리스트 인덱싱만으로 해결하는 것이 올바른 접근입니다.

---

원하면  
이걸 **알고리즘 설계 관점에서 왜 딕셔너리가 잘못된 모델링인지**  
자료구조 선택 관점으로도 설명해드릴까요?

---
