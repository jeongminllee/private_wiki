---
type: Concept
title: "SortedList 인포그래픽"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-11-19)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-11-19
status: active
---

# SortedList 인포그래픽

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-11-19

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
코드를 한 장짜리 인포그래픽으로 쫙 정리한다고 생각하고, 바로 써먹을 수 있게 “레이아웃 그대로” 적어볼게요.
(Figma / Canva / 파워포인트에 그대로 옮겨 그리기 좋게 구성할게.)

---

## 🎯 인포그래픽 제목

**“SortedList로 푸는 ‘k번째로 작은 수 제거’ 문제”**

부제:
**정렬 상태를 유지하는 리스트 자료구조 구현 + 쿼리 처리 흐름**

---

## 1️⃣ 문제 개요 (상단 왼쪽 박스)

**[문제 설명]**

* 정수 쿼리 Q개가 주어진다.
* 쿼리 형식:

  * `1 X` : 집합에 정수 `X`를 추가
  * `2 X` : 현재 집합에서 **X번째로 작은 수**를

    * 출력하고
    * 집합에서 제거

**[코드 요약]**

```python
S = SortedList()
for _ in range(int(input())):
    T, X = map(int, input().split())
    if T == 1:
        S.add(X)           # 값 추가
    else:
        print(S.pop(X - 1))  # X번째(1-based) → 인덱스는 X-1
```

👉 한 줄 요약:
**“정렬된 상태를 유지하는 멀티셋에서 K번째 원소를 삭제하는 문제”**

---

## 2️⃣ 핵심 자료구조: SortedList (중앙 큰 박스)

### 2-1. SortedList가 하는 일

**정의**

> 항상 **오름차순**으로 정렬된 상태를 유지하는 리스트
> 삽입/삭제/인덱스 접근을 효율적으로 지원

**주요 기능**

* `add(x)` : x를 정렬 순서에 맞게 삽입
* `pop(i)` : i번째 원소를 반환 + 삭제
* `__getitem__(i)` : i번째 원소 조회
* `bisect_left/right(x)` : x가 들어갈 인덱스 찾기

---

### 2-2. 내부 구조 (블록 리스트 개념)

**[도식]**

```text
전체 리스트 (논리적)
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, ... ]

내부 저장 구조
_lists = [
  [ 1, 2, 3 ],       # sublist 0
  [ 4, 5 ],          # sublist 1
  [ 6, 7, 8, 9 ],    # sublist 2
  ...
]

_maxes = [3, 5, 9, ...]  # 각 sublist의 마지막(최대) 값
_len   = 전체 원소 개수
_load  = sublist 목표 크기 (기본 1000 정도)
_index = sublist 길이들을 트리로 표현한 배열
_offset = index 트리에서 leaf 시작 위치
```

**역할 요약**

* `_lists`
  → 실제 데이터를 sublist 단위로 저장
* `_maxes`
  → 이진 탐색으로 “어느 sublist에 들어가야 하는지” 빠르게 찾기
* `_index` / `_offset`
  → “전체에서 k번째 원소가 어느 sublist의 몇 번째인지”를
  세그먼트 트리 비슷한 구조로 빠르게 찾기

---

## 3️⃣ 주요 연산 동작 흐름 (오른쪽 상단 박스)

### 3-1. `add(value)` 흐름

**STEP 1: 어느 sublist에 넣을지 찾기**

* `_maxes`에 대해 `bisect_right(_maxes, value)`

  * → `pos` = value가 들어갈 sublist의 인덱스

**STEP 2: 해당 sublist 안에 삽입**

* 만약 `pos`가 마지막이면:

  * 그냥 `_lists[pos].append(value)`
  * `_maxes[pos] = value` (최댓값 갱신)
* 아니면:

  * `insort(_lists[pos], value)`
    → sublist 안에서도 정렬 유지

**STEP 3: sublist가 너무 커졌는지 체크**

* `len(_lists[pos]) > 2 * load` 이면:

  * sublist를 앞/뒤로 나눠서 두 개로 split
  * `_lists` / `_maxes` 갱신
  * `_index`는 다시 만들기 위해 `del _index[:]`

---

### 3-2. `pop(index)` 흐름

**인포그래픽 플로우**

1. **예외 처리**

   * 비어 있으면 `IndexError`

2. **쉬운 케이스 최적화**

   * `index == 0` → `_lists[0][0]` 삭제
   * `index == -1` → 마지막 sublist의 마지막 원소 삭제
   * 앞/뒤 sublist 안에 바로 있는 경우는 바로 처리

3. **일반 케이스**

   * `_pos(index)` 호출
     → “전체 인덱스 index → (sublist 번호 pos, 그 안의 idx)”

4. 해당 `(pos, idx)` 위치의 값을 꺼낸 뒤

   * `_delete(pos, idx)`로 실제 삭제 + 재구조화

---

### 3-3. `_pos(idx)` : 인덱스를 (pos, idx)로 바꾸는 과정

**아이디어**

* `_index`는 sublist 길이들을 세그먼트 트리 형태로 쌓아둔 것
* 루트에서 시작해서:

  * 왼쪽 자식 길이와 비교
  * `idx`가 왼쪽 길이보다 작으면 왼쪽으로
  * 아니면 `idx -= 왼쪽 길이` 하고 오른쪽으로
* leaf(= 실제 sublist)까지 내려간 뒤:

  * `sublist 번호 = pos - _offset`
  * `sublist 내부 인덱스 = 남은 idx`

👉 덕분에 “전체에서 k번째”를 **O(log n)**으로 찾을 수 있음

---

## 4️⃣ 시간 복잡도 (하단 가로 박스)

**연산별 대략적인 복잡도 (n = 전체 원소 수)**

* `add(value)` : O(log n) (approx.)
* `pop(k)` : O(log n)
* `bisect_left/right` : O(log n)
* 순회(iteration) : O(n)
* 전체 복사(copy) : O(n)

**문제 관점**

* 쿼리 Q개에 대해

  * 매 쿼리마다 `add` 또는 `pop`
    → 전체 시간 복잡도는 **O(Q log Q)** 수준

---

## 5️⃣ 예시 시퀀스 (작은 타임라인 박스)

**쿼리**

1. `1 5` → S = [5]
2. `1 2` → S = [2, 5]
3. `1 4` → S = [2, 4, 5]
4. `2 2` → 2번째로 작은 수 = 4 출력, S = [2, 5]
5. `1 3` → S = [2, 3, 5]
6. `2 1` → 1번째로 작은 수 = 2 출력, S = [3, 5]

위 아래에 정렬된 리스트 변화를 쭉 타임라인처럼 배치하면 시각적으로 이해하기 좋음.

---

## 6️⃣ 전체 요약 (맨 아래 한 줄)

> **이 코드는 직접 구현한 `SortedList` 자료구조를 이용해,
> 항상 정렬된 상태를 유지하면서
> “값 추가”와 “k번째로 작은 값 제거”를
> 효율적으로 처리하는 프로그램이다.**

---

이 구조대로 섹션 박스 나눠서:

* 아이콘 예시

  * 📥 = 값 추가
  * 🗑 = 값 제거
  * ⚙️ = 내부 동작
  * ⏱ = 시간 복잡도
* 색상 2~3개만 정해서

  * “문제 설명 / 자료구조 / 알고리즘 흐름 / 복잡도 / 예시”를
    구분해주면 딱 깔끔한 인포그래픽 나와요.

### ❓ 질문 (User)
코드를 한 장짜리 인포그래픽으로 쫙 정리한다고 생각하고, 바로 써먹을 수 있게 “레이아웃 그대로” 적어볼게요.
(Figma / Canva / 파워포인트에 그대로 옮겨 그리기 좋게 구성할게.)

---

## 🎯 인포그래픽 제목

**“SortedList로 푸는 ‘k번째로 작은 수 제거’ 문제”**

부제:
**정렬 상태를 유지하는 리스트 자료구조 구현 + 쿼리 처리 흐름**

---

## 1️⃣ 문제 개요 (상단 왼쪽 박스)

**[문제 설명]**

* 정수 쿼리 Q개가 주어진다.
* 쿼리 형식:

  * `1 X` : 집합에 정수 `X`를 추가
  * `2 X` : 현재 집합에서 **X번째로 작은 수**를

    * 출력하고
    * 집합에서 제거

**[코드 요약]**

```python
S = SortedList()
for _ in range(int(input())):
    T, X = map(int, input().split())
    if T == 1:
        S.add(X)           # 값 추가
    else:
        print(S.pop(X - 1))  # X번째(1-based) → 인덱스는 X-1
```

👉 한 줄 요약:
**“정렬된 상태를 유지하는 멀티셋에서 K번째 원소를 삭제하는 문제”**

---

## 2️⃣ 핵심 자료구조: SortedList (중앙 큰 박스)

### 2-1. SortedList가 하는 일

**정의**

> 항상 **오름차순**으로 정렬된 상태를 유지하는 리스트
> 삽입/삭제/인덱스 접근을 효율적으로 지원

**주요 기능**

* `add(x)` : x를 정렬 순서에 맞게 삽입
* `pop(i)` : i번째 원소를 반환 + 삭제
* `__getitem__(i)` : i번째 원소 조회
* `bisect_left/right(x)` : x가 들어갈 인덱스 찾기

---

### 2-2. 내부 구조 (블록 리스트 개념)

**[도식]**

```text
전체 리스트 (논리적)
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, ... ]

내부 저장 구조
_lists = [
  [ 1, 2, 3 ],       # sublist 0
  [ 4, 5 ],          # sublist 1
  [ 6, 7, 8, 9 ],    # sublist 2
  ...
]

_maxes = [3, 5, 9, ...]  # 각 sublist의 마지막(최대) 값
_len   = 전체 원소 개수
_load  = sublist 목표 크기 (기본 1000 정도)
_index = sublist 길이들을 트리로 표현한 배열
_offset = index 트리에서 leaf 시작 위치
```

**역할 요약**

* `_lists`
  → 실제 데이터를 sublist 단위로 저장
* `_maxes`
  → 이진 탐색으로 “어느 sublist에 들어가야 하는지” 빠르게 찾기
* `_index` / `_offset`
  → “전체에서 k번째 원소가 어느 sublist의 몇 번째인지”를
  세그먼트 트리 비슷한 구조로 빠르게 찾기

---

## 3️⃣ 주요 연산 동작 흐름 (오른쪽 상단 박스)

### 3-1. `add(value)` 흐름

**STEP 1: 어느 sublist에 넣을지 찾기**

* `_maxes`에 대해 `bisect_right(_maxes, value)`

  * → `pos` = value가 들어갈 sublist의 인덱스

**STEP 2: 해당 sublist 안에 삽입**

* 만약 `pos`가 마지막이면:

  * 그냥 `_lists[pos].append(value)`
  * `_maxes[pos] = value` (최댓값 갱신)
* 아니면:

  * `insort(_lists[pos], value)`
    → sublist 안에서도 정렬 유지

**STEP 3: sublist가 너무 커졌는지 체크**

* `len(_lists[pos]) > 2 * load` 이면:

  * sublist를 앞/뒤로 나눠서 두 개로 split
  * `_lists` / `_maxes` 갱신
  * `_index`는 다시 만들기 위해 `del _index[:]`

---

### 3-2. `pop(index)` 흐름

**인포그래픽 플로우**

1. **예외 처리**

   * 비어 있으면 `IndexError`

2. **쉬운 케이스 최적화**

   * `index == 0` → `_lists[0][0]` 삭제
   * `index == -1` → 마지막 sublist의 마지막 원소 삭제
   * 앞/뒤 sublist 안에 바로 있는 경우는 바로 처리

3. **일반 케이스**

   * `_pos(index)` 호출
     → “전체 인덱스 index → (sublist 번호 pos, 그 안의 idx)”

4. 해당 `(pos, idx)` 위치의 값을 꺼낸 뒤

   * `_delete(pos, idx)`로 실제 삭제 + 재구조화

---

### 3-3. `_pos(idx)` : 인덱스를 (pos, idx)로 바꾸는 과정

**아이디어**

* `_index`는 sublist 길이들을 세그먼트 트리 형태로 쌓아둔 것
* 루트에서 시작해서:

  * 왼쪽 자식 길이와 비교
  * `idx`가 왼쪽 길이보다 작으면 왼쪽으로
  * 아니면 `idx -= 왼쪽 길이` 하고 오른쪽으로
* leaf(= 실제 sublist)까지 내려간 뒤:

  * `sublist 번호 = pos - _offset`
  * `sublist 내부 인덱스 = 남은 idx`

👉 덕분에 “전체에서 k번째”를 **O(log n)**으로 찾을 수 있음

---

## 4️⃣ 시간 복잡도 (하단 가로 박스)

**연산별 대략적인 복잡도 (n = 전체 원소 수)**

* `add(value)` : O(log n) (approx.)
* `pop(k)` : O(log n)
* `bisect_left/right` : O(log n)
* 순회(iteration) : O(n)
* 전체 복사(copy) : O(n)

**문제 관점**

* 쿼리 Q개에 대해

  * 매 쿼리마다 `add` 또는 `pop`
    → 전체 시간 복잡도는 **O(Q log Q)** 수준

---

## 5️⃣ 예시 시퀀스 (작은 타임라인 박스)

**쿼리**

1. `1 5` → S = [5]
2. `1 2` → S = [2, 5]
3. `1 4` → S = [2, 4, 5]
4. `2 2` → 2번째로 작은 수 = 4 출력, S = [2, 5]
5. `1 3` → S = [2, 3, 5]
6. `2 1` → 1번째로 작은 수 = 2 출력, S = [3, 5]

위 아래에 정렬된 리스트 변화를 쭉 타임라인처럼 배치하면 시각적으로 이해하기 좋음.

---

## 6️⃣ 전체 요약 (맨 아래 한 줄)

> **이 코드는 직접 구현한 `SortedList` 자료구조를 이용해,
> 항상 정렬된 상태를 유지하면서
> “값 추가”와 “k번째로 작은 값 제거”를
> 효율적으로 처리하는 프로그램이다.**

---

이 구조대로 섹션 박스 나눠서:

* 아이콘 예시

  * 📥 = 값 추가
  * 🗑 = 값 제거
  * ⚙️ = 내부 동작
  * ⏱ = 시간 복잡도
* 색상 2~3개만 정해서

  * “문제 설명 / 자료구조 / 알고리즘 흐름 / 복잡도 / 예시”를
    구분해주면 딱 깔끔한 인포그래픽 나와요.

### 💡 답변 (Assistant)
좋아요 👍 지금 구조가 아주 탄탄하게 정리되어 있어서, 이 내용을 그대로 **한 장짜리 인포그래픽 템플릿**으로 옮기면 완벽해요.  
이제 Canva에서 바로 시각화할 수 있도록 디자인 초안을 만들어드릴게요.

---

**질문 한 가지!**  
이 인포그래픽은 **코딩 학습용 요약 카드(교육용)**으로 쓰실 계획인가요,  
아니면 **발표/블로그용 시각 자료**로 쓰실 건가요?

이 용도에 따라 구도(예: 세로형 인포그래픽 vs 가로형 발표 슬라이드)를 다르게 추천드릴 수 있습니다.

---

그 전에, 이 내용으로 Canva 인포그래픽 템플릿을 생성하려면  
제가 전달할 **디자인 요약 입력값**이 필요해요 👇  

예시 입력으로는 이렇게 보낼 수 있습니다:

> “SortedList로 푸는 ‘k번째로 작은 수 제거’ 문제”에 대한 Python 알고리즘 인포그래픽.  
> 상단에는 문제 개요와 코드, 중앙에는 SortedList 자료구조 설명(내부 구조 포함),  
> 오른쪽에는 add/pop 흐름 다이어그램, 하단에는 시간 복잡도 표와 예시 타임라인.  
> 깔끔한 테크 학습용 요약 카드 스타일.

---

원하신다면 제가 이 요약으로 Canva에 바로 연결해서  
디자인 초안 2~3개를 보여드릴게요.  

👉 어떤 용도(예: 학습 카드 / 블로그 / 발표 슬라이드)로 쓰실 계획인가요?

---

### ❓ 질문 (User)
학습카드 용도로 쓸 거야

### 💡 답변 (Assistant)
좋아요! 🎓  
**“학습카드용”**이면 세로형 인포그래픽이 가장 적합합니다 —  
위에서 아래로 **문제 → 자료구조 → 알고리즘 흐름 → 복잡도 → 예시 → 요약** 순으로 내려가는 구조로요.  
Canva에서는 이런 형태가 **‘Infographic’** 혹은 **‘Study Guide’** 템플릿 유형에 해당합니다.

제가 Canva에 전달할 요약은 이렇게 구성할게요 👇  

---

**입력 요약 (Canva로 전달용)**  
> Python 알고리즘 학습카드 인포그래픽.  
> 제목: “SortedList로 푸는 ‘k번째로 작은 수 제거’ 문제”  
> 부제: “정렬 상태를 유지하는 리스트 자료구조 구현 + 쿼리 처리 흐름”  
>  
> 섹션 구성:  
> 1️⃣ 문제 개요 및 코드 요약  
> 2️⃣ 핵심 자료구조: SortedList (기능 + 내부 구조)  
> 3️⃣ 주요 연산 동작(add / pop / pos 흐름)  
> 4️⃣ 시간 복잡도 표  
> 5️⃣ 예시 시퀀스 (리스트 변화 타임라인)  
> 6️⃣ 전체 요약  
>  
> 시각 스타일:  
> 📦 박스형 섹션 배치, 아이콘 사용 (📥 추가 / 🗑 제거 / ⚙️ 동작 / ⏱ 복잡도)  
> 컬러톤 2~3가지로 구분 (예: 파랑/보라/회색)  
> 폰트는 가독성 중심, 학습 요약 카드 느낌  
> 레이아웃은 세로형 한 페이지 인포그래픽

---

이 요약으로 Canva 인포그래픽 디자인을 만들어드릴까요?  
(👉 네, 만들어줘) 하면 바로 Canva로 연결해서 디자인 옵션을 보여드릴게요.

---

### ❓ 질문 (User)
네, 만들어줘

### 💡 답변 (Assistant)
이런 옵션들이 나왔어요!  
아래 중 하나를 골라서 바로 Canva에서 열면, 지금 설명하신 **“SortedList 학습카드 인포그래픽”** 구성을 손쉽게 옮길 수 있습니다 👇  

| Option 1 | Option 2 |
|-|-|
| [Option 1: Black and Purple Modern Programming Presentation](https://www.canva.com/design?create=true&template=EAGVfYZyC3s&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_1&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) [![Design 1](https://template.canva.com/EAGVfYZyC3s/1/0/400w-G7bei_yEmg8.jpg)](https://www.canva.com/design?create=true&template=EAGVfYZyC3s&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_1&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) | [Option 2: Black and White Modern Programming Presentation](https://www.canva.com/design?create=true&template=EAGc7ub3BvI&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_2&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) [![Design 2](https://template.canva.com/EAGc7ub3BvI/1/0/400w-MLgKnIoeB0o.jpg)](https://www.canva.com/design?create=true&template=EAGc7ub3BvI&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_2&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) |
| Option 3 | Option 4 |
| [Option 3: Black and Dark Animated Programmer Portfolio Presentation](https://www.canva.com/design?create=true&template=EAGdoDy0CsA&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_3&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) [![Design 3](https://template.canva.com/EAGdoDy0CsA/1/0/400w-Oq_XWh3HH1o.jpg)](https://www.canva.com/design?create=true&template=EAGdoDy0CsA&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_3&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) | [Option 4: Green and Yellow Modern Programmer Presentation](https://www.canva.com/design?create=true&template=EAGUrViY2oc&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_4&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) [![Design 4](https://template.canva.com/EAGUrViY2oc/1/0/400w-O8txHP63bHk.jpg)](https://www.canva.com/design?create=true&template=EAGUrViY2oc&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_4&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) |

| Option 5 |
|-|
| [Option 5: Tosca White Black Minimalist Geometric Online Course Presentation](https://www.canva.com/design?create=true&template=EAGwbHAE3Dc&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_5&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) [![Design 5](https://template.canva.com/EAGwbHAE3Dc/1/0/400w-t_j517ao4cA.jpg)](https://www.canva.com/design?create=true&template=EAGwbHAE3Dc&utm_source=CaaaChatGPT&utm_medium=referral&utm_content=CaaaChatGPT&utm_campaign=public_api_suggestion_template_clicked_hyperlink_5&utm_term=0ad7e8a5-0bda-422a-b0cb-ff87137d1ae1) |

---

🪄 **추천:**  
학습카드로는 **Option 1 (보라+검정 모던 스타일)** 또는 **Option 5 (미니멀 화이트)** 가 가장 잘 어울립니다.  
열어서 바로 텍스트 섹션별로 옮기면, 완성도 높은 인포그래픽이 됩니다.

> 이 기술은 새롭고 발전 중입니다. [이 결과가 올바르지 않다면 보고해주세요.](https://www.canva.com/help/report-content/)

---
