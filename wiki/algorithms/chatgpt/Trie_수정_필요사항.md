---
type: Concept
title: "Trie 수정 필요사항"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-11-19)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-11-19
status: active
---

# Trie 수정 필요사항

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-11-19

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
class Trie :
    def __init__(self):
        self.bags = {}

    def insert(self, word: str):
        curr = self.bags

        for letter in word :
            if letter not in curr :
                curr[letter] = {}
            curr = curr[letter]

        curr["end_of_word"] = ""

    def find(self, word: str):
        curr = self.bags

        for letter in word :
            if letter not in curr :
                return False
            curr = curr[letter]

        return "end_of_word" in curr

    def startsWith(self, prefix: str):
        curr = self.bags

        for letter in prefix :
            if letter not in curr :
                return False
            curr = curr[letter]

        return True

def solution(words, queries) :
    answer = [0] * len(words)
    trie = Trie()

    for word in words :
        trie.insert(word)

    for idx in range(len(queries)) :
        if queries[idx] == '?' :
            continue
        trie.startsWith(queries[idx])
        answer[idx] += 1

    return answer

if __name__ == "__main__" :
    print(solution(["frodo", "front", "frost", "frozen", "frame", "kakao"],
                   ["fro??", "????o", "fr???", "fro???", "pro?"]))
    # [3, 2, 4, 1, 0]
```

[본 문제는 정확성과 효율성 테스트 각각 점수가 있는 문제입니다.]

친구들로부터 천재 프로그래머로 불리는 "프로도"는 음악을 하는 친구로부터 자신이 좋아하는 노래 가사에 사용된 단어들 중에 특정 키워드가 몇 개 포함되어 있는지 궁금하니 프로그램으로 개발해 달라는 제안을 받았습니다.
그 제안 사항 중, 키워드는 와일드카드 문자중 하나인 '?'가 포함된 패턴 형태의 문자열을 뜻합니다. 와일드카드 문자인 '?'는 글자 하나를 의미하며, 어떤 문자에도 매치된다고 가정합니다. 예를 들어 "fro??"는 "frodo", "front", "frost" 등에 매치되지만 "frame", "frozen"에는 매치되지 않습니다.

가사에 사용된 모든 단어들이 담긴 배열 words와 찾고자 하는 키워드가 담긴 배열 queries가 주어질 때, 각 키워드 별로 매치된 단어가 몇 개인지 순서대로 배열에 담아 반환하도록 solution 함수를 완성해 주세요.

가사 단어 제한사항
words의 길이(가사 단어의 개수)는 2 이상 100,000 이하입니다.
각 가사 단어의 길이는 1 이상 10,000 이하로 빈 문자열인 경우는 없습니다.
전체 가사 단어 길이의 합은 2 이상 1,000,000 이하입니다.
가사에 동일 단어가 여러 번 나올 경우 중복을 제거하고 words에는 하나로만 제공됩니다.
각 가사 단어는 오직 알파벳 소문자로만 구성되어 있으며, 특수문자나 숫자는 포함하지 않는 것으로 가정합니다.
검색 키워드 제한사항
queries의 길이(검색 키워드 개수)는 2 이상 100,000 이하입니다.
각 검색 키워드의 길이는 1 이상 10,000 이하로 빈 문자열인 경우는 없습니다.
전체 검색 키워드 길이의 합은 2 이상 1,000,000 이하입니다.
검색 키워드는 중복될 수도 있습니다.
각 검색 키워드는 오직 알파벳 소문자와 와일드카드 문자인 '?' 로만 구성되어 있으며, 특수문자나 숫자는 포함하지 않는 것으로 가정합니다.
검색 키워드는 와일드카드 문자인 '?'가 하나 이상 포함돼 있으며, '?'는 각 검색 키워드의 접두사 아니면 접미사 중 하나로만 주어집니다.
예를 들어 "??odo", "fro??", "?????"는 가능한 키워드입니다.
반면에 "frodo"('?'가 없음), "fr?do"('?'가 중간에 있음), "?ro??"('?'가 양쪽에 있음)는 불가능한 키워드입니다.
입출력 예
words	queries	result
["frodo", "front", "frost", "frozen", "frame", "kakao"]	["fro??", "????o", "fr???", "fro???", "pro?"]	[3, 2, 4, 1, 0]
입출력 예에 대한 설명
"fro??"는 "frodo", "front", "frost"에 매치되므로 3입니다.
"????o"는 "frodo", "kakao"에 매치되므로 2입니다.
"fr???"는 "frodo", "front", "frost", "frame"에 매치되므로 4입니다.
"fro???"는 "frozen"에 매치되므로 1입니다.
"pro?"는 매치되는 가사 단어가 없으므로 0 입니다.

이 문제를 위 코드로 해결하려고 했는데 마무리가 잘 되지 않아서 어떤점이 문제인지 지적해줄 수 있을까?

### 💡 답변 (Assistant)
좋은 시도야! 지금 코드가 **왜 원하는 결과가 안 나오는지** 하나씩 짚어볼게. 결론부터 말하면:

> 이 코드는  
> 1) `?`를 전혀 처리하지 않고,  
> 2) 매치 개수를 세지도 않고,  
> 3) 길이 조건도 무시하고,  
> 4) `answer` 길이도 잘못 잡아서  
> 절대 정답이 나올 수 없는 구조야.

차근차근 보자.

---

## 1. `answer` 길이 잘못 잡음

```python
def solution(words, queries) :
    answer = [0] * len(words)   # 👉 여기
    ...
    for idx in range(len(queries)) :
        ...
        answer[idx] += 1
```

- `answer`는 **queries 개수만큼** 있어야 해.
- 그런데 지금은 `len(words)`로 만들었어.
- 예제에서 `len(words) = 6`, `len(queries) = 5`니까,
  - `answer`는 `[0,0,0,0,0,0]` (길이 6)
  - for 문은 `idx = 0~4`까지만 돌고
  - 결과는 `[1,1,1,1,1,0]` 이런 식으로 나와버릴 거야.

✔️ 수정해야 할 부분:

```python
answer = [0] * len(queries)
```

---

## 2. `?`(와일드카드)를 전혀 처리하지 않음

지금 쿼리 처리 부분을 보면:

```python
for idx in range(len(queries)) :
    if queries[idx] == '?' :
        continue
    trie.startsWith(queries[idx])
    answer[idx] += 1
```

문제점:

1. `"fro??"` 같이 `?`가 섞인 쿼리를 그대로 `startsWith("fro??")`에 넣고 있음  
   - **Trie에는 `'?'`라는 문자가 아예 안 들어가 있으니까** 항상 False가 나와야 정상인데,  
   - 심지어 **반환값도 안 쓰고** 있음 ⬇️

2. `startsWith`의 결과(True/False)를 전혀 사용하지 않고,  
   그냥 `answer[idx] += 1`만 하고 있음  
   → 결국 **모든 쿼리가 “있든 말든 무조건 +1”**이 되어버려.

즉, 지금 로직은:

> 쿼리가 `'?'`가 아니면  
> → `startsWith`를 그냥 호출만 하고  
> → 무조건 `answer[idx] += 1`

이라서, **매치 개수랑 전혀 관계가 없어**.

---

## 3. Trie 구조가 “개수 세기용”으로 설계되어 있지 않음

현재 Trie는 이렇게 되어 있지:

```python
class Trie :
    def __init__(self):
        self.bags = {}

    def insert(self, word: str):
        curr = self.bags

        for letter in word :
            if letter not in curr :
                curr[letter] = {}
            curr = curr[letter]

        curr["end_of_word"] = ""
```

- 각 노드에 **“이 노드를 지나가는 단어가 몇 개냐”** 같은 정보가 전혀 없음.
- 그런데 이 문제는 쿼리별로 **“매칭되는 단어 개수”**를 요구하니까,
  - `startsWith(prefix)` → True/False가 아니라,
  - 그 prefix 아래에 **몇 개의 단어가 있는지**를 알려줘야 해.

그래서 보통 이 문제를 Trie로 풀 때는:

```python
class Node:
    def __init__(self):
        self.children = {}
        self.count = 0   # 이 노드를 거치는 단어 수

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        curr = self.root
        curr.count += 1
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = Node()
            curr = curr.children[ch]
            curr.count += 1

    def count_prefix(self, prefix):
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return 0
            curr = curr.children[ch]
        return curr.count
```

이런 식으로, `count_prefix("fro")` 하면 `"fro"`로 시작하는 단어가 몇 개인지 알려주는 식으로 구현해.

---

## 4. 쿼리 길이 및 `'?'` 위치를 고려하지 않음

이 문제의 핵심 조건:

- **단어 길이와 쿼리 길이가 같을 때만 매칭**  
- `?`는 **항상 접두사 또는 접미사**로만 등장

예를 들어 `"fro??"`는 길이 5니까,
- `["frodo", "front", "frost", "frame"]` 정도만 후보고,
- `"frozen"`(길이 6)은 애초에 후보에서 제외해야 해.

그런데 지금 코드에서는:

- 한 개의 Trie에 모든 단어를 그냥 다 넣었고,
- 쿼리 길이도 전혀 신경 안 쓰고 있음.
- `"fro??"`로 검색하면 `"fro"`로 시작하는 **모든 길이의 단어**가 다 포함돼버리는 구조.

그래서 제대로 풀려면:

1. **길이별로 Trie를 따로 관리**해야 해.
   - 예) 길이가 5인 단어들만 담는 Trie, 6인 단어들만 담는 Trie …

2. 그리고 `'????o'`처럼 **앞에 `?`가 있는 경우**는 뒤에서부터 비교해야 하니까
   - **뒤집은 단어들로 만든 Trie**도 따로 필요해.
   - `word = "frodo"` → `"odorf"`
   - 쿼리 `"????o"` → 뒤집고 `'o????'` → `'o'`를 prefix로 검색

대략적인 구조는 이런 느낌:

```python
from collections import defaultdict

tries = defaultdict(Trie)        # 정방향 trie: 길이별
rev_tries = defaultdict(Trie)    # 역방향 trie: 길이별

for word in words:
    L = len(word)
    tries[L].insert(word)
    rev_tries[L].insert(word[::-1])

for q in queries:
    L = len(q)
    if q[0] != '?':  # 접미사가 '?'
        prefix = q.rstrip('?')
        answer.append(tries[L].count_prefix(prefix))
    else:            # 접두사가 '?'
        suffix = q.lstrip('?')[::-1]
        answer.append(rev_tries[L].count_prefix(suffix))
```

---

## 5. 요약: 지금 코드의 핵심 문제 정리

정리하면, 현재 코드의 문제는:

1. `answer` 배열 길이가 잘못됨  
   → `len(words)`가 아니라 `len(queries)`여야 함

2. `startsWith`의 결과를 사용하지 않음  
   → 무조건 `answer[idx] += 1`만 함

3. `?`를 전혀 다루지 않음  
   → `"fro??"`를 그대로 prefix로 쓰면 Trie에 없는 문자 `'?'` 때문에 로직이 안 맞음

4. Trie 노드에 **개수 정보(count)**가 없음  
   → prefix에 매칭되는 단어 개수를 셀 수 없음

5. **단어 길이와 쿼리 길이**를 고려하지 않음  
   → 길이가 다른 단어도 매칭될 위험이 있음

6. 접두사 `?` 쿼리(`"????o"` 같은 것)를 처리하기 위한 **역방향 Trie**가 없음

---

원하면,
- 지금 네 Trie 구조를 기반으로 **count 기능 추가 + 길이별 Trie + 역방향 Trie**까지 넣은 **완성 코드**도 한 번에 만들어줄게.  
"Trie 방식으로 끝까지 구현한 정답 코드 보여줘" 라고 말해주면 바로 짜줄게.

---

### ❓ 질문 (User)
끝까지 구현한 정답 코드 보여줘.

### 💡 답변 (Assistant)
바로 Trie로 끝까지 구현한 버전 보여줄게.  
(길이별 Trie + 역방향 Trie + 쿼리 캐싱까지 포함)

```python
from collections import defaultdict

class Trie:
    def __init__(self):
        # root는 dict
        # 각 노드에 '#': 지나가는 단어 수를 저장
        self.root = {}

    def insert(self, word: str):
        curr = self.root
        # 루트를 지나가는 단어 수 +1
        curr['#'] = curr.get('#', 0) + 1

        for ch in word:
            if ch not in curr:
                curr[ch] = {}
            curr = curr[ch]
            # 이 노드를 지나가는 단어 수 +1
            curr['#'] = curr.get('#', 0) + 1

    def count_prefix(self, prefix: str) -> int:
        """prefix 로 시작하는 단어가 몇 개인지 반환"""
        curr = self.root
        for ch in prefix:
            if ch not in curr:
                return 0
            curr = curr[ch]
        return curr.get('#', 0)


def solution(words, queries):
    # 길이별 정방향 Trie, 역방향 Trie
    forward_tries = defaultdict(Trie)  # 예: "fro??" → "fro" 로 검색
    reverse_tries = defaultdict(Trie)  # 예: "????o" → 단어 뒤집어서 "o" 로 검색

    # 단어 삽입
    for word in words:
        L = len(word)
        forward_tries[L].insert(word)          # 정방향
        reverse_tries[L].insert(word[::-1])    # 역방향 (뒤집어서 저장)

    answer = []
    cache = {}  # 같은 쿼리 여러 번 나올 수 있으니 캐싱

    for q in queries:
        if q in cache:
            answer.append(cache[q])
            continue

        L = len(q)

        # 쿼리 길이와 같은 단어가 아예 없는 경우
        # (defaultdict라 없어도 Trie는 생기지만, root에 '#'(카운트)가 없으면 0으로 처리됨)
        # 어차피 아래에서 처리되므로 생략해도 됨.

        # 1) 앞부분이 글자, 뒷부분이 '?' 인 경우: 접두사 검색
        if q[0] != '?':
            # 처음 '?'가 나오기 전까지가 prefix
            prefix = q.split('?', 1)[0]
            cnt = forward_tries[L].count_prefix(prefix)

        # 2) 앞부분이 '?' 이고, 뒷부분이 글자인 경우: 접미사 검색 → 뒤집어서 prefix로 처리
        else:
            # 왼쪽의 '?'들을 제거하면 실제 접미사만 남음
            suffix = q.lstrip('?')

            # 전부 '?' 인 경우: 해당 길이의 단어 개수 전체
            if suffix == "":
                cnt = forward_tries[L].root.get('#', 0)
            else:
                # 단어를 뒤집어서 저장했으니, suffix를 뒤집어서 prefix로 검색
                rev_prefix = suffix[::-1]
                cnt = reverse_tries[L].count_prefix(rev_prefix)

        cache[q] = cnt
        answer.append(cnt)

    return answer


if __name__ == "__main__":
    print(solution(
        ["frodo", "front", "frost", "frozen", "frame", "kakao"],
        ["fro??", "????o", "fr???", "fro???", "pro?"]
    ))
    # 기대 출력: [3, 2, 4, 1, 0]
```

### 핵심 아이디어 요약

- **길이별로 Trie를 따로 관리**  
  → 쿼리와 길이가 다른 단어는 아예 후보에서 제외.

- **정방향 / 역방향 Trie 둘 다 사용**
  - `"fro??"` → 앞글자(`"fro"`)로 검색 → 정방향 Trie
  - `"????o"` → 접미사(`"o"`) 기준 → 단어/쿼리 뒤집어서 `"o????"`로 보고 → 역방향 Trie에서 `"o"` prefix 검색

- **각 Trie 노드에 `'#'` 카운트 저장**  
  → 그 노드를 거치는 단어 수 = 해당 prefix로 시작하는 단어 수.

- **쿼리 캐싱(cache)**  
  → 같은 쿼리가 여러 번 나와도 한 번만 계산.

원하면, 위 코드 기준으로  
- 메모리/시간 복잡도 분석,  
- 또는 네가 처음 짜 놓은 `class Trie` 스타일로 조금만 수정해서 쓰는 버전도 따로 만들어줄게.

---

### ❓ 질문 (User)
```
from bisect import bisect_left, bisect_right

def count(words, left_value, right_value):
    right_index = bisect_right(words, right_value)
    left_index = bisect_left(words, left_value)

    return right_index - left_index
def solution(words, queries):
    answer = []

    data = [[] for _ in range(10001)]
    reverse = [[] for _ in range(10001)]
    for word in words:
        data[len(word)].append(word)
        reverse[len(word)].append(word[::-1])

    for i in range(10001):
        data[i].sort()
        reverse[i].sort()

    for query in queries:
        if query.startswith('?'):
            reversed_query = query[::-1]
            left_value = reversed_query.replace('?', 'a')
            right_value = reversed_query.replace('?', 'z')

            result = count(reverse[len(query)], left_value, right_value)

        else:
            left_value = query.replace('?', 'a')
            right_value = query.replace('?', 'z')

            result = count(data[len(query)], left_value, right_value)

        answer.append(result)
    return answer
```
이 풀이는 어떤 점을 공략한건지 설명해줘

### 💡 답변 (Assistant)
이 풀이는 딱 세 가지 포인트를 아주 예쁘게 공략하고 있어:

1. **“길이가 같은 단어끼리만 비교하면 된다”**  
2. **“`?`는 항상 접두사 또는 접미사다” → 결국 “일정 구간” 탐색 문제**  
3. **정렬 + 이분 탐색으로 “구간의 개수”만 세면 된다**

코드를 그 관점에서 뜯어볼게.

---

## 1️⃣ 길이별로 단어를 분리한 것의 의미

```python
data = [[] for _ in range(10001)]
reverse = [[] for _ in range(10001)]
for word in words:
    data[len(word)].append(word)
    reverse[len(word)].append(word[::-1])
```

- 문제 조건: **단어 길이와 쿼리 길이가 같을 때만 매칭 가능**  
  → `"fro??"`(길이 5) 는 길이 5인 단어만 보면 됨.
- 그래서 `data[length]`에 **해당 길이의 단어들만** 모아놓고,
- `reverse[length]`에는 **뒤집은 단어**들을 모아둠.

이렇게 하면 쿼리를 처리할 때:

```python
result = count(data[len(query)], ...)     # 정방향
result = count(reverse[len(query)], ...)  # 역방향
```

처럼 **해당 길이 배열만 보면 되니까**  
불필요한 비교(길이 다른 단어)는 아예 안 하게 됨.

> 🔑 포인트 1:  
> “길이 필터링”을 전처리 단계에서 끝내버려서,  
> 쿼리 하나당 볼 단어 수를 크게 줄임.

---

## 2️⃣ 접두사 `?` vs 접미사 `?` → “앞부분 비교”로 통일

```python
if query.startswith('?'):
    reversed_query = query[::-1]
    ...
    result = count(reverse[len(query)], left_value, right_value)
else:
    ...
    result = count(data[len(query)], left_value, right_value)
```

문제 조건:

- `?`는 항상 **앞에 몰려 있거나** (`"????o"`)
- **뒤에 몰려 있거나** (`"fro??"`)

즉:

- `"fro??"` → **앞 3글자 `"fro"`만 중요**  
- `"????o"` → **뒤 1글자 `"o"`만 중요**

그래서 이 풀이에서는:

- 접두사가 `?`가 아닌 경우 (`"fro??"`)  
  → 그냥 **앞부분 고정 문자열** + 뒷부분 `?`

- 접두사가 `?`인 경우 (`"????o"`)  
  → 문자열 뒤집어서 `"o????"`로 만들고  
    → **다시 “앞부분 고정 문자열” + 뒷부분 `?`**로 바꿔버림  
    → 그래서 `reverse` 배열(뒤집힌 단어들)에서 **앞부분만 보고 비교**한다.

> 🔑 포인트 2:  
> “접두사 `?` / 접미사 `?` 둘 다  
> → 단어/쿼리를 뒤집어서  
> → 결국 *접두사 패턴* 하나로 통일해버림.”

---

## 3️⃣ `?`를 `'a'`~`'z'` 범위로 치환 → 이분 탐색 가능하게 만들기

```python
left_value = query.replace('?', 'a')
right_value = query.replace('?', 'z')
result = count(data[len(query)], left_value, right_value)
```

예를 들어 `"fro??"`라는 쿼리를 보자.

- 사전순으로 `"froaa"` 이상, `"frozz"` 이하인 모든 단어는  
  `"fro??"` 패턴에 매칭되는 후보야.

왜냐면:

- `'?'`는 알파벳 소문자 하나를 의미하고,
- `'a'` ~ `'z'`가 가능한 모든 문자이기 때문에,
- `"froaa"` ~ `"frozz"` 사이에 있는 단어들은  
  앞 3글자가 `"fro"`이고, 뒤 2글자가 아무거나인 단어들.

그래서:

```python
def count(words, left_value, right_value):
    right_index = bisect_right(words, right_value)
    left_index = bisect_left(words, left_value)
    return right_index - left_index
```

- `words`가 **정렬된 상태**라면,
  - `bisect_left(words, left_value)`  → 이 구간이 시작되는 인덱스
  - `bisect_right(words, right_value)` → 이 구간이 끝나는 인덱스
- 둘의 차이가 곧  
  → 해당 쿼리에 매칭되는 단어 개수.

`?`가 앞에 있는 경우도 마찬가지야:

- `"????o"` → 뒤집으면 `"o????"`  
- `"o????"` → `"oaaaa"` ~ `"ozzzz"` 범위  
- 이걸 `reverse[len(query)]`에서 이분 탐색으로 세는 구조.

> 🔑 포인트 3:  
> `?`를 `'a'`와 `'z'`로 치환해서  
> **“이 구간에 들어오는 모든 문자열을 세는 문제”**로 바꾼 다음,  
> 정렬 + 이분 탐색으로 O(log N)에 해결.

---

## 4️⃣ 이 풀이의 시간 복잡도

1. **전처리**
   - 단어 삽입: `O(Σ |word|)` (여기선 length 분배라 사실상 `O(#words)`)
   - 길이별 정렬:  
     각 길이 L에 대해 `data[L].sort()`  
     전체적으로 `O(Σ N_L log N_L)` → `N`개 단어 기준 `O(N log N)` 정도.

2. **쿼리 처리**
   - 쿼리마다:
     - `replace` 2번: O(|query|)
     - `bisect_left/right`: O(log N_L)  
       (N_L = 해당 길이 단어 수)
   - 전체 쿼리 수 Q라고 하면  
     대략 `O(Σ |query| + Q log N_max)`.

제한 조건(단어/쿼리 10만, 전체 길이 합 100만)에서  
충분히 통과 가능한 효율적인 풀이.

---

## 5️⃣ Trie 풀이랑 비교하면

**Trie 풀이**는:

- 각 노드에 `count`를 넣고
- 길이별로 Trie / Reverse Trie를 만들고
- prefix에 대응하는 노드의 `count`를 리턴

**이 bisect 풀이**는:

- 정렬 + 이분 탐색으로 **문자열 범위**를 계산해서 개수를 리턴

둘 다 아이디어는 비슷해:

- 길이별 분할
- 접두사/접미사 → 접두사로 통일
- 매칭 개수만 빠르게 세기

차이는:

- Trie: 구현은 약간 더 복잡하지만, 이론적으로는 문자열 길이에 비례
- 정렬 + 이분 탐색: 구현이 더 간단하고, Python에서 상수도 작은 편이라 실전 코딩 테스트에서 많이 쓰는 방식

---

## 한 줄 요약

> 이 풀이는  
> **① 길이별 분할, ② 단어·쿼리 뒤집기로 접미사 패턴을 접두사로 통일, ③ `?`를 `'a'`~`'z'` 범위로 바꿔서 정렬된 배열에서 이분 탐색으로 개수만 세는 전략**을 쓴 거야.

원하면,  
- 이 풀이를 기반으로 **직접 손으로 예제(`"fro??"`, `"????o"`)를 추적해보는 시뮬레이션**도 같이 해줄게.

---

### ❓ 질문 (User)
bisect 라이브러리를 실제 함수로 구현한 코드를 포함하여 정답 코드를 구현해줘.

### 💡 답변 (Assistant)
좋지, 이번엔 `bisect` 모듈을 *직접 구현한 함수*로만 써서 정답 코드를 한 번에 보여줄게.  
(= 표준 라이브러리 `bisect`는 안 쓰고, 똑같이 동작하는 `bisect_left`, `bisect_right`를 우리가 직접 구현)

---

## ✅ 전체 정답 코드 (수기 bisect 포함)

```python
def bisect_left(a, x):
    """정렬된 리스트 a에서 x가 들어갈 가장 왼쪽 인덱스를 반환"""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bisect_right(a, x):
    """정렬된 리스트 a에서 x가 들어갈 가장 오른쪽 인덱스를 반환"""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_in_range(words, left_value, right_value):
    """정렬된 words에서 [left_value, right_value] 사이에 있는 문자열 개수"""
    right_index = bisect_right(words, right_value)
    left_index = bisect_left(words, left_value)
    return right_index - left_index


def solution(words, queries):
    answer = []

    # 길이별 단어 리스트, 길이별 뒤집은 단어 리스트
    MAX_LEN = 10000
    data = [[] for _ in range(MAX_LEN + 1)]
    reverse = [[] for _ in range(MAX_LEN + 1)]

    # 단어를 길이별로 분류 + 뒤집은 버전도 저장
    for word in words:
        L = len(word)
        data[L].append(word)
        reverse[L].append(word[::-1])

    # 각 길이별로 정렬
    for i in range(MAX_LEN + 1):
        if data[i]:
            data[i].sort()
        if reverse[i]:
            reverse[i].sort()

    # 쿼리 처리
    for query in queries:
        L = len(query)

        # 해당 길이의 단어가 하나도 없으면 0
        if not data[L]:
            answer.append(0)
            continue

        # 1) 접두사가 고정이고 뒤가 '?'인 경우 → 정방향 배열 사용
        if query[0] != '?':
            left_value = query.replace('?', 'a')
            right_value = query.replace('?', 'z')
            result = count_in_range(data[L], left_value, right_value)

        # 2) 앞이 '?'이고 접미사가 고정인 경우 → 단어/쿼리를 뒤집고 접두사로 처리
        else:
            reversed_query = query[::-1]
            left_value = reversed_query.replace('?', 'a')
            right_value = reversed_query.replace('?', 'z')
            result = count_in_range(reverse[L], left_value, right_value)

        answer.append(result)

    return answer


if __name__ == "__main__":
    print(solution(
        ["frodo", "front", "frost", "frozen", "frame", "kakao"],
        ["fro??", "????o", "fr???", "fro???", "pro?"]
    ))
    # 출력: [3, 2, 4, 1, 0]
```

---

### 간단 요약

- **`bisect_left`, `bisect_right`**  
  → 우리가 직접 이분 탐색으로 구현해서,  
  정렬된 리스트에서 어떤 문자열이 들어갈 왼쪽/오른쪽 경계를 찾음.

- **길이별 배열 `data[len]`, `reverse[len]`**  
  → 쿼리와 길이가 같은 단어만 대상으로 해서 시간 절약.  
  → 접미사 패턴(`????o`)은 뒤집어서 **접두사 패턴**으로 통일.

- **`?` → `'a'` / `'z'` 치환**  
  → `"fro??"` → `"froaa"` ~ `"frozz"` 범위로 보고  
    이 구간에 들어오는 단어 개수를 이분 탐색으로 셈.

원하면, 위 코드 기준으로  
직접 `"fro??"` / `"????o"` 하나씩 손으로 추적해보는 과정도 같이 풀어서 보여줄게.

---
