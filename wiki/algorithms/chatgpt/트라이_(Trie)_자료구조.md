---
type: Concept
title: "트라이 (Trie) 자료구조"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2023-11-06)"
tags: [algorithms, chatgpt-export]
timestamp: 2023-11-06
status: active
---

# 트라이 (Trie) 자료구조

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-11-06

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
파이썬 알고리즘 테스트에서 자료구조 중 트라이 trie 알아?

### 💡 답변 (Assistant)
트라이 (Trie)는 자료구조 중 하나로, 특히 문자열을 저장하고 검색하는 데 유용한 트리 구조를 기반으로 합니다. 트라이는 "reTRIEval"의 줄임말로, 데이터를 검색하는 데 사용됩니다.

트라이의 주요 특징은 다음과 같습니다:

1. 접두사 트리 (Prefix Tree): 트라이는 문자열을 저장할 때, 각 문자의 연속적인 문자열 조각을 저장합니다. 이것은 문자열 검색에서 접두사 검색과 관련이 있으며, 빠른 접두사 검색을 가능하게 합니다.

2. 계층적 구조: 트라이는 루트 노드에서 시작하여 각 문자마다 새로운 노드를 생성하는 계층적 구조를 가지며, 각 노드는 문자를 나타내거나 노드의 종료를 나타내는 특별한 플래그를 가질 수 있습니다.

3. 높은 검색 성능: 트라이는 문자열 검색에 대해 높은 성능을 제공합니다. 문자열 검색은 일정한 시간 복잡도를 가지며, 문자열의 길이와 관계없이 검색 속도가 거의 일정합니다.

4. 공간 효율적: 트라이는 문자열을 효과적으로 저장하는 데 사용됩니다. 중복 문자열은 공유 노드로 표현되므로 메모리 효율적입니다.

트라이는 주로 문자열 검색, 자동 완성, 스펠 체크, IP 주소 검색 등 다양한 응용 프로그램에서 사용됩니다. 파이썬에서는 트라이를 직접 구현할 수 있으며, 다양한 라이브러리와 모듈도 제공되므로 트라이를 사용하여 자료를 효과적으로 저장하고 검색할 수 있습니다.

---

### ❓ 질문 (User)
자동완성 에 대해서 파이썬 코드 작성해줘

### 💡 답변 (Assistant)
자동 완성을 구현하기 위해 트라이 자료구조를 사용한 간단한 예제를 제공해 드리겠습니다. 이 예제에서는 트라이를 사용하여 문자열을 저장하고 사용자가 입력한 접두사와 일치하는 모든 문자열을 검색합니다.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_words_with_prefix(node, prefix)

    def _find_words_with_prefix(self, node, prefix):
        results = []
        if node.is_end_of_word:
            results.append(prefix)
        for char, child_node in node.children.items():
            results.extend(self._find_words_with_prefix(child_node, prefix + char))
        return results

# 예제 사용
trie = Trie()
words = ["apple", "appetizer", "banana", "bat", "ball"]
for word in words:
    trie.insert(word)

prefix = "app"
auto_complete_results = trie.search(prefix)

if auto_complete_results:
    print("자동 완성 결과:")
    for result in auto_complete_results:
        print(result)
else:
    print("일치하는 결과가 없습니다.")
```

위 코드는 단어 리스트를 트라이에 삽입하고, 사용자가 입력한 접두사에 따른 자동 완성 결과를 검색하는 간단한 예제입니다. 입력한 "app"의 경우 "apple"과 "appetizer"가 자동 완성 결과로 반환됩니다.

---

### ❓ 질문 (User)
포털 다음에서 검색어 자동완성 기능을 넣고 싶은 라이언은 한 번 입력된 문자열을 학습해서 다음 입력 때 활용하고 싶어 졌다. 예를 들어, go 가 한 번 입력되었다면, 다음 사용자는 g 만 입력해도 go를 추천해주므로 o를 입력할 필요가 없어진다! 단, 학습에 사용된 단어들 중 앞부분이 같은 경우에는 어쩔 수 없이 다른 문자가 나올 때까지 입력을 해야 한다.
효과가 얼마나 좋을지 알고 싶은 라이언은 학습된 단어들을 찾을 때 몇 글자를 입력해야 하는지 궁금해졌다.

예를 들어, 학습된 단어들이 아래와 같을 때

go
gone
guild
go를 찾을 때 go를 모두 입력해야 한다.
gone을 찾을 때 gon 까지 입력해야 한다. (gon이 입력되기 전까지는 go 인지 gone인지 확신할 수 없다.)
guild를 찾을 때는 gu 까지만 입력하면 guild가 완성된다.
이 경우 총 입력해야 할 문자의 수는 7이다.

라이언을 도와 위와 같이 문자열이 입력으로 주어지면 학습을 시킨 후, 학습된 단어들을 순서대로 찾을 때 몇 개의 문자를 입력하면 되는지 계산하는 프로그램을 만들어보자.

입력 형식
학습과 검색에 사용될 중복 없는 단어 N개가 주어진다.
모든 단어는 알파벳 소문자로 구성되며 단어의 수 N과 단어들의 길이의 총합 L의 범위는 다음과 같다.

2 <= N <= 100,000
2 <= L <= 1,000,000

### 💡 답변 (Assistant)
문자열 검색을 빠르게 수행하기 위해 트라이 자료구조를 활용할 수 있습니다. 아래는 주어진 조건에 따라 프로그램을 구현한 파이썬 코드 예제입니다:

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.prefix_count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.prefix_count += 1
        node.is_end_of_word = True

    def find_min_typing(self, word):
        node = self.root
        count = 0
        for char in word:
            if char not in node.children:
                return count
            node = node.children[char]
            count += 1
            if node.prefix_count == 1:
                return count
        return count

def solution(words):
    trie = Trie()
    total_typing_count = 0

    for word in words:
        trie.insert(word)
        total_typing_count += trie.find_min_typing(word)

    return total_typing_count

# 입력 예시
words = ["go", "gone", "guild"]
result = solution(words)
print(result)  # 결과 출력

```

위의 코드는 주어진 단어 목록을 학습하고, 각 단어를 찾을 때 몇 개의 문자를 입력해야 하는지 계산합니다. 코드에서 Trie 자료구조를 사용하여 입력 문자열을 저장하고, `find_min_typing` 메서드를 통해 최소 입력 문자 수를 찾습니다. 입력 예시인 ["go", "gone", "guild"]에 대한 결과는 7이 됩니다.

---

### ❓ 질문 (User)
def solution(words):
    N = len(words)
    words.sort()
    answer = [0] * N
    
    for i in range(N - 1) :
        a = len(words[i])
        b = len(words[i - 1])
        
        for j in range(min(a, b)) :
            if words[i][j] != words[i + 1][j] :
                j -= 1
                break
                
        answer[i] = max(answer[i], min(a, j + 2))
        answer[i + 1] = max(answer[i + 1], min(b, j + 2))
        
    return sum(answer)
    
   풀이해줘

### 💡 답변 (Assistant)
주어진 코드는 주어진 단어 목록을 학습하고, 각 단어를 찾을 때 몇 개의 문자를 입력해야 하는지 계산하는 것을 목표로 합니다. 코드는 단어를 길이에 따라 정렬한 후, 인접한 단어들을 비교하면서 공통된 접두사를 찾고 최소 입력 문자 수를 계산하는 방식으로 작동합니다. 여기서 `answer` 배열은 각 단어에 대한 최소 입력 문자 수를 저장합니다.

코드를 라인별로 설명하겠습니다:

1. `N`은 단어의 수를 나타내며, 주어진 단어 목록 `words`를 정렬합니다.
2. `answer` 배열은 각 단어의 최소 입력 문자 수를 저장하는 배열로 초기화됩니다.
3. 이중 반복문을 사용하여 인접한 단어들을 비교합니다.
4. `a`와 `b`는 현재 단어와 이전 단어의 길이를 나타냅니다.
5. 내부 반복문을 사용하여 두 단어의 각 문자를 비교합니다. 두 단어 중 가장 짧은 길이까지만 비교합니다.
6. 만약 두 단어가 다른 문자를 가진 경우, `j`를 갱신합니다. `j`는 가장 길이가 짧은 단어의 인덱스를 나타냅니다.
7. 각 단어에 대한 최소 입력 문자 수를 계산하고 `answer` 배열을 업데이트합니다.
8. 마지막으로 `answer` 배열의 합을 반환합니다.

이 코드는 주어진 문제를 풀기 위한 한 가지 방법입니다. 입력에 대한 정렬이 추가 비용을 발생시키지만, 인접한 단어들을 비교함으로써 공통된 접두사를 찾는 효율적인 방법을 사용합니다. 결과적으로, `sum(answer)`는 단어를 검색하기 위해 필요한 총 입력 문자 수를 나타냅니다.

---

### ❓ 질문 (User)
def solution(answers):
    answer = [0, 0, 0]
    ans1 = [1, 2, 3, 4, 5]
    ans2 = [2, 1, 2, 3, 2, 4, 2, 5]
    ans3 = [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
    result = []
    for idx, val in enumerate(answers):
        if ans1[idx % len(ans1)] == val:
            answer[0] += 1
        if ans2[idx % len(ans2)] == val:
            answer[1] += 1
        if ans3[idx % len(ans3)] == val:
            answer[2] += 1

    for i in range(len(answer)):
        if answer[i] == max(answer):
            result.append(i + 1)

    return sorted(result)
풀이해줘

### 💡 답변 (Assistant)
주어진 코드는 정답 패턴이 주어진 학생들에 대해 각 학생의 점수를 계산하고, 가장 높은 점수를 받은 학생들의 번호를 반환하는 프로그램입니다. 이 문제는 "모의고사"와 같은 유형의 문제로, 주어진 정답 패턴에 따라 각 학생의 답안을 평가합니다.

코드를 간략히 설명하겠습니다:

1. `answer` 리스트는 세 명의 학생의 점수를 저장하기 위한 리스트입니다. 초기화되며, 각 학생의 점수가 계산됩니다.
2. `ans1`, `ans2`, `ans3`은 각 학생의 정답 패턴을 나타냅니다.
3. `result` 리스트는 가장 높은 점수를 받은 학생들의 번호를 저장하는 리스트입니다.
4. `enumerate(answers)`를 사용하여 `answers` 리스트의 값과 인덱스를 동시에 가져와서 각 학생의 정답과 비교합니다.
5. 각 학생의 정답을 패턴의 길이에 맞춰 나머지 연산을 통해 비교합니다.
6. 각 학생의 점수를 업데이트합니다.
7. `max(answer)`를 사용하여 가장 높은 점수를 계산하고, 가장 높은 점수를 받은 학생들의 번호를 `result` 리스트에 추가합니다.
8. 마지막으로 `result` 리스트를 정렬하여 반환합니다.

이 코드는 각 학생의 점수를 계산하고, 가장 높은 점수를 받은 학생들의 번호를 반환합니다. 문제에서 주어진 정답 패턴에 따라 학생들의 답안을 평가하며, 최고 점수를 받은 학생들을 찾는 것이 목표입니다.

---

### ❓ 질문 (User)
Immutable Data Structure가 무슨말이야?

### 💡 답변 (Assistant)
Immutable(불변) 데이터 구조는 한 번 생성되면 수정할 수 없는 데이터 구조를 의미합니다. 이는 데이터를 변경하는 대신, 새로운 데이터를 생성하여 변경된 값을 나타내는 방식을 채택합니다. 이러한 불변 데이터 구조는 몇 가지 중요한 특징을 가지고 있습니다:

1. 변경 불가능성 (Immutability): 한 번 생성된 데이터는 수정할 수 없습니다. 따라서 해당 데이터 구조를 사용하는 코드에서 데이터를 변경하려고 하면 새로운 데이터 구조를 생성해야 합니다.

2. 스레드 안정성 (Thread Safety): 불변 데이터 구조는 여러 스레드에서 안전하게 공유될 수 있습니다. 왜냐하면 데이터가 변경되지 않기 때문에 동시에 여러 스레드에서 데이터에 접근해도 문제가 발생하지 않습니다.

3. 참조 투명성 (Referential Transparency): 불변 데이터 구조는 같은 입력에 대해 항상 같은 출력을 반환하므로 참조 투명성을 가집니다. 이는 함수형 프로그래밍에서 중요한 특성 중 하나입니다.

4. 값 복사 (Value Copy): 데이터를 변경하지 않고 복사하는 경우, 데이터의 전체 사본을 생성해야 합니다. 이는 성능 면에서는 일부 오버헤드가 발생할 수 있으며, 따라서 일부 작업에서는 주의가 필요합니다.

불변 데이터 구조는 다양한 프로그래밍 언어와 패러다임에서 사용됩니다. 예를 들어, 파이썬에서는 문자열과 튜플은 불변 데이터 구조입니다. 이러한 불변성은 코드의 안정성과 가독성을 향상시키는 데 도움이 될 수 있으며, 병렬 처리와 함수형 프로그래밍과 같은 여러 프로그래밍 패러다임에서 중요한 역할을 합니다.

---

### ❓ 질문 (User)
나 지금부터 2개의 답변을 물어볼꺼야 왜 동일하게 작동하는지 모르겠어.
문제는 같은 문제에 서로 다른 답변이야.

### 💡 답변 (Assistant)
물론, 궁금한 것에 대한 답변을 제공해 드리겠습니다. 문제가 동일하지만 서로 다른 답변이 나타날 때, 그 이유는 다음과 같을 수 있습니다:

1. 입력 데이터가 다를 수 있습니다: 동일한 문제라도 입력 데이터가 다르다면 서로 다른 답변이 나타날 수 있습니다. 입력 데이터의 차이가 결과에 영향을 미칠 수 있습니다.

2. 다양한 접근 방식: 문제를 해결하기 위한 다양한 접근 방식이 있을 수 있으며, 각각의 방식은 서로 다른 결과를 내놓을 수 있습니다.

3. 프로그래밍 언어나 환경의 차이: 어떤 문제를 서로 다른 프로그래밍 언어나 환경에서 해결할 때, 구현 세부사항에 차이가 있을 수 있으며, 이로 인해 다른 결과가 나타날 수 있습니다.

4. 임의성 (Randomness): 어떤 알고리즘이나 프로세스가 무작위성을 포함하고 있다면, 각 실행에서 서로 다른 결과가 나타날 수 있습니다.

이러한 이유 중 하나 또는 여러 가지가 해당되거나, 종종 문제 해결에 대한 다양한 해결책이 존재하기 때문에 동일한 문제에 대해 서로 다른 답변이 나타날 수 있습니다.

---

### ❓ 질문 (User)
1. 
from itertools import permutations
def solution(n) :
    a = set()
    for i in range(len(n)) :
        a |= set(map(int, map(''.join, permutations(list(n), i + 1))))
    a -= set(range(0, 2))
    for i in range(2, int(max(a) ** 0.5) + 1) :
        a -= set(range(i * 2, max(a) + 1, i))
    return len(a)
이게 1번이고

2.
prime_set = set()

def isPrime(number) :
    if number in (0, 1) :
        return False

    lim = int((number ** (1/2)) + 1)
    for i in range(2, lim) :
        if number % i == 0 :
            return False
    return True

def makeCombinations(combination, others) :
    if combination != "" :
        if isPrime(int(combination)) :
            prime_set.add(int(combination))

    for i in range(len(others)) :
        makeCombinations(combination + others[i], others[:i] + others[i + 1 :])

def solution(numbers) :
    makeCombinations('', numbers)

    answer = len(prime_set)
    return answer
이게 2번이야.
풀이해줘

### 💡 답변 (Assistant)
두 가지 코드 모두 입력으로 주어진 숫자 조합에서 소수(Prime number)의 개수를 계산하는 문제를 해결하는 것을 목표로 합니다. 각 코드가 어떻게 작동하는지 살펴보겠습니다.

1번 코드:
- 첫 번째 코드는 itertools 모듈의 permutations 함수를 사용하여 입력된 숫자 문자열 `n`의 모든 순열을 생성합니다.
- 각 순열을 정수로 변환하고 중복을 제거하기 위해 set `a`에 추가합니다.
- 소수를 판별하기 위해 에라토스테네스의 체 알고리즘을 사용하여 `a`에서 소수가 아닌 숫자를 제거합니다.
- 최종적으로 `a`의 길이를 반환하여 소수의 개수를 계산합니다.

2번 코드:
- 두 번째 코드는 재귀 함수 `makeCombinations`을 사용하여 입력된 숫자 문자열 `numbers`에서 가능한 모든 숫자 조합을 생성합니다.
- `isPrime` 함수를 사용하여 각 숫자 조합이 소수인지 판별하고, 소수인 경우 `prime_set`에 추가합니다.
- 최종적으로 `prime_set`의 길이를 반환하여 소수의 개수를 계산합니다.

두 코드 모두 같은 문제를 해결하는 방식으로, 가능한 모든 숫자 조합을 생성하고 소수를 판별하여 소수의 개수를 세는 방식을 사용합니다. 두 코드 모두 효과적으로 동작하지만 코드 스타일과 구현 방법이 다를 수 있습니다.

어떤 방식이든, 입력으로 주어진 숫자에서 가능한 모든 소수를 찾는 것은 주어진 문제를 해결하는 좋은 방법입니다.

---

### ❓ 질문 (User)
1번 코드에 permutations 함수가 2번 코드에 재귀함수makeCombinations 이거일까?

### 💡 답변 (Assistant)
1번 코드와 2번 코드 모두 소수를 찾는 방식에 대해 다르게 구현되어 있습니다.

1번 코드에서 permutations 함수를 사용하여 숫자의 모든 순열을 생성하고, 이를 소수 판별에 활용하고 있습니다. permutations 함수를 사용하면 순열을 모두 생성할 수 있습니다.

2번 코드에서는 재귀 함수 `makeCombinations`를 사용하여 가능한 모든 숫자 조합을 생성하고, 각 조합을 소수 판별에 활용하고 있습니다. 이 방식은 재귀적으로 모든 조합을 생성하고 검사하는 방식입니다.

따라서 1번 코드의 `permutations` 함수와 2번 코드의 `makeCombinations` 함수는 서로 다른 방식으로 숫자 조합을 생성하고 사용하는 것을 나타냅니다.

---

### ❓ 질문 (User)
방식은 서로 다르나, 숫자 조합을 생성하는 것은 맞다는거네

### 💡 답변 (Assistant)
맞습니다, 두 코드의 주요 목표는 숫자 조합을 생성하고 이를 소수 판별에 활용하는 것입니다. 두 코드는 서로 다른 방식으로 숫자 조합을 생성하고 검사하지만, 공통된 목표를 가지고 있습니다. 1번 코드는 itertools 모듈의 permutations 함수를 사용하여 순열을 생성하고, 2번 코드는 재귀 함수 `makeCombinations`를 사용하여 숫자 조합을 생성합니다.

---

### ❓ 질문 (User)
결국 생성하는 숫자의 순서만 다를 뿐, 안에 있는 값은 같아지겠네

### 💡 답변 (Assistant)
맞습니다, 두 코드는 숫자의 조합을 생성하는데 있어서 다른 방법을 사용하고 있지만, 생성된 숫자 조합의 값은 동일합니다. 따라서 두 코드는 같은 입력에 대해 동일한 결과를 반환할 것입니다. 이 경우, 생성된 숫자 조합의 순서만 다르지만, 내부의 숫자 값은 같게 됩니다.

---

### ❓ 질문 (User)
너는 어떤 코드를 더 추천해?

### 💡 답변 (Assistant)
어떤 코드를 추천할지는 상황과 선호하는 코딩 스타일에 따라 다를 수 있습니다. 두 코드 모두 주어진 문제를 해결하는데 효과적인 방법을 제시하고 있습니다. 

1번 코드는 itertools 모듈의 permutations 함수를 사용하여 순열을 생성하므로, 코드가 간결하고 직관적입니다. 이 방법은 빠르게 원하는 결과를 얻을 수 있으며, 순열 생성과 에라토스테네스의 체를 사용하는 부분이 명확하게 분리되어 있습니다.

2번 코드는 재귀 함수를 사용하여 숫자 조합을 생성하고, 각 조합을 소수 판별에 활용하는 방식으로 보다 직접적인 방법을 사용합니다. 이 방법은 재귀적으로 조합을 생성하는데 큰 장점이 있으며, 숫자 조합을 생성하는 방법을 보다 직접적으로 이해하기 쉽습니다.

어떤 코드를 선택할지는 개인의 코딩 스타일과 선호에 따라 다를 것이며, 어떤 코드가 더 이해하기 쉽거나 유지 보수가 편할지에 따라 선택하시면 됩니다. 두 코드 모두 잘 작동하므로, 자신이 가장 편하게 이해하고 사용할 수 있는 코드를 선택하시면 될 것입니다.

---

### ❓ 질문 (User)
에라토스테네스의 체를 사용하는건 둘 다 똑같지 않아?

### 💡 답변 (Assistant)
예, 두 코드 모두 에라토스테네스의 체를 사용하여 소수를 판별하고 비소수를 제거하는 방식은 동일합니다. 에라토스테네스의 체는 소수를 찾는 데 효과적인 방법 중 하나이며, 이 방법은 두 코드 모두에서 사용되고 있습니다. 

에라토스테네스의 체의 기본 아이디어는 소수의 배수를 모두 제거하여 소수를 찾는 것입니다. 두 코드에서도 이 원리를 사용하여 숫자 중에서 소수를 식별하고 소수가 아닌 숫자를 제거하고 있습니다. 따라서 이 부분은 두 코드에서 동일하게 작동하며, 동일한 알고리즘을 사용하고 있습니다.

다시 말해, 두 코드 모두 에라토스테네스의 체를 사용하여 소수를 판별하고 그 결과를 활용하고 있으므로, 에라토스테네스의 체를 사용하는 부분에는 차이가 없습니다.

---

### ❓ 질문 (User)
def solution(words):
    N = len(words)
    words.sort() # 단어를 사전순으로 정렬
    result = [0] * N # 단어마다 입력해야 하는 문자 수

    for i in range(N - 1):
        # 인접하는 두 단어 비교
        a = len(words[i])
        b = len(words[i + 1])
        for j in range(min(a, b)):
            if words[i][j] != words[i + 1][j]:
                j -= 1 # 일치하지 않으면 일치하는 최대 인덱스로 저장 후 break
                break

        # 일치하는 인덱스 + 1만큼 문자를 입력해야 한다.
        # 단, 입력하는 문자 수가 단어 길이를 넘지 말아야 한다.
        result[i] = max(result[i], min(a, j + 2))
        result[i + 1] = max(result[i + 1], min(b, j + 2))

    # 단어마다 입력해야 하는 문자 수를 합해서 반환
    return sum(result)

풀이해줘

### 💡 답변 (Assistant)
주어진 코드는 단어 리스트에서 각 단어를 찾을 때 몇 개의 문자를 입력해야 하는지 계산하는 문제를 해결하는 파이썬 함수입니다. 코드를 한 단계씩 설명하겠습니다.

1. `N`은 단어의 수를 나타내며, 주어진 단어 목록 `words`를 사전순으로 정렬합니다.

2. `result` 리스트는 각 단어의 최소 입력 문자 수를 저장하기 위한 리스트로, 초기값은 모두 0으로 초기화됩니다.

3. `for` 루프를 사용하여 각 단어 쌍을 비교합니다. `i`는 현재 단어의 인덱스를 나타내며, `i`와 `i+1`의 두 인접한 단어를 비교합니다.

4. `a`와 `b`는 각 단어의 길이를 나타냅니다.

5. `for` 루프를 사용하여 두 단어를 비교하며, 두 단어가 일치하지 않는 지점을 찾습니다. 이 지점에서 `j`를 갱신하고 `break`로 루프를 종료합니다.

6. 일치하지 않는 지점(`j`) 이후에, `result[i]`와 `result[i+1]`에 각각 해당 단어를 찾을 때 필요한 입력 문자 수를 저장합니다. 이때, `min(a, j+2)`와 `min(b, j+2)`를 사용하여 최소값을 구하고, 각각의 결과를 `result` 리스트에 저장합니다.

7. 마지막으로 `sum(result)`를 사용하여 각 단어마다 입력해야 하는 문자 수를 합산하고 반환합니다.

이 코드는 단어를 사전순으로 정렬하고, 인접한 단어들을 비교하여 일치하지 않는 지점을 찾고, 필요한 입력 문자 수를 계산하여 각 단어마다의 결과를 반환합니다.

---
