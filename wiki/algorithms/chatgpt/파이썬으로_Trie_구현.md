---
type: Concept
title: "파이썬으로 Trie 구현"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-11-19)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-11-19
status: active
---

# 파이썬으로 Trie 구현

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-11-19

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
// 작성자 : 가자
// 작성일 : 11/18/2025 
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Trie{
    int pos[100000][26]; // nodeCnt -> A B C D ,.. Z
    bool isEnd[100000];  // ABCD <- 끝?
    int nodeCnt = 0;     // 문자열 트리 노드 개수 

    // 이 nodeCnt는 노드의 번호를 pos 배열에 저장하는 일종의 포인터입니다.  
    // 예를 들면 pos[nodeCnt]라고 한다면 
    // insert된 문자열 개수입니다.
    // 여기서 Pl PLA PLC 첫문자 P, 두번째 문자 L처럼 
    // 경로가 겹치는 경우에는 nodeCnt를 증가시키지 않습니다. 
    // 이미 해당 path에 노드가 생성되었기 때문입니다.
    // 이와 관련한 구현은 아래 insert 함수 구현에서 좀 더 살펴보겠습니다. 
    // 트리 모양으로 적어보면 
    //         P
    //         |
    //         L -end
    //        | \ 
    //       /   C - end     
    //      A-end  -> 즉 이 경우는 nodeCnt가 4가 나와야 합니다. 

    void insert(string &s) { // 전체 시간복잡도 |s1|+|s2|+|s3|+...|sn| = O(최대길이 x 문자열 개수)
        int cur = 0; 
        // 현재 탐색하고 있는 문자열의 n번째를 뜻하는 겁니다.   
        // 0이므로 s의 첫번째 문자열을 가리키는 겁니다. 
        
        cout << s << '\n';
        for(char c : s){ // 시간복잡도 O(N), |s| = N 
            int cur_idx = c-'A'; 
            // 알파벳 소문자만 나온다는 가정으로 이렇게 -'a'를 빼서 인덱스를 구했습니다. 
            // 이렇게 연속적(consecutive)하지 않는 경우에는 좌표압축을 한 후에 
            // 사용하는 문자열의 개수만큼 26을 바꿔주면 됩니다. 
            if(pos[cur][cur_idx]==0){
                cout << c << '\n';
                pos[cur][cur_idx] = ++nodeCnt;
            }
            cur = pos[cur][cur_idx];
        }
        cout << nodeCnt << '\n';
        isEnd[cur] = true; 
        // abcd 라는 문자열이 있다면 
        // abcd d의 문자열에 해당하는 pos[cur][cur_idx]의 nodeCnt에
        // a->b->c->d 라는 문자열은 d에서 끝난다는 걸 기록하는 것입니다. 
        // 이는 find 함수의 59번 라인과 연결되는 내용입니다.  
    }

    bool find(string s){ // 시간복잡도 O(N)
        int cur = 0; 
        // 이제 insert와 방식이 비슷합니다. 
        // cur 시작 위치, 해당 문자의 인덱스로 접근하여
        // nodeCnt(노드번호)를 찾고 다음 레벨로 넘어갑니다. 
        // 이걸 level로 나타내면 Tree처럼 나타낼 수 있어서 이름이 Trie입니다. 

        for(char c : s){
            int char_idx = c-'A';
            cur = pos[cur][char_idx];
        }

        return isEnd[cur];
    }
};

Trie trie;
int main(void){
    int n = 3; 
    
    string tmp;
    for(int i =0;i<n;i++){ // 여기서 입력을 PL, PLA, PLC를 하면 
        cin>> tmp;
        trie.insert(tmp);
    }

    cout << trie.find("PL") << '\n'; // 1이 나옵니다. g++ -std=c++17 Trie.cpp -o Trie 

    cout << trie.find("PLA") << '\n'; //로 컴파일 한 뒤에, 윈도우) Trie / 맥은 ./Trie로 체크해보세요

    cout << trie.find("PLC") << '\n';

}
```
이 코드를 파이썬 코드로 구현해줘

### 💡 답변 (Assistant)
파이썬으로 그대로 옮긴 버전이야. C++ 코드의 동작(배열 크기, `cout` 디버깅 출력, find 로직까지) 최대한 똑같이 맞춰 놨어.

```python
# 작성자 : 가자 (Python 버전)
# 작성일 : 11/18/2025

class Trie:
    def __init__(self, max_nodes=100000):
        # pos[node][0~25] : 다음 노드 번호
        self.pos = [[0] * 26 for _ in range(max_nodes)]
        # is_end[node] : 이 노드에서 문자열이 끝나는지 여부
        self.is_end = [False] * max_nodes
        # 사용된 노드 개수 (0번이 루트)
        self.node_cnt = 0

    def insert(self, s: str):
        # 전체 시간복잡도 |s1|+|s2|+...+|sn| = O(최대길이 x 문자열 개수)
        cur = 0  # 현재 노드 번호 (0 = 루트)

        print(s)
        for c in s:  # O(|s|)
            cur_idx = ord(c) - ord('A')  # 대문자 A~Z 기준
            # 해당 경로에 노드가 없다면 새로 생성
            if self.pos[cur][cur_idx] == 0:
                print(c)
                self.node_cnt += 1
                self.pos[cur][cur_idx] = self.node_cnt
            # 다음 노드로 이동
            cur = self.pos[cur][cur_idx]

        print(self.node_cnt)
        # 문자열이 여기서 끝난다고 표시
        self.is_end[cur] = True

    def find(self, s: str) -> bool:
        # 시간복잡도 O(|s|)
        cur = 0
        for c in s:
            char_idx = ord(c) - ord('A')
            cur = self.pos[cur][char_idx]
        # 해당 노드가 문자열의 끝으로 기록되어 있는지 반환
        return self.is_end[cur]


def main():
    trie = Trie()
    n = 3

    for _ in range(n):
        tmp = input().strip()
        trie.insert(tmp)

    # C++ 코드와 동일한 테스트
    print(int(trie.find("PL")))   # True -> 1
    print(int(trie.find("PLA")))  # True -> 1
    print(int(trie.find("PLC")))  # True -> 1


if __name__ == "__main__":
    main()
```

- 입력 예시  
  ```
  PL
  PLA
  PLC
  ```
- 실행하면 C++처럼 `insert` 과정에서 문자열과 새로 만든 문자, `node_cnt`가 출력되고  
  마지막에 `1 1 1` 이 순서대로 찍힐 거야.  

원하면 `print` 디버깅 부분을 없애고 “깨끗한 버전”도 따로 정리해 줄게.

---

### ❓ 질문 (User)
내가 공부할때는 Trie 알고리즘을 파이썬 딕셔너리 활용해서 구현했거든. 니가 직접 딕셔너리 자료구조를 활용해서 구현해주고 현재 이 코드와 어떤점이 차이가 있는지 설명해줘.

### 💡 답변 (Assistant)
좋지, 이제 “파이썬다운” Trie로 한번 바꿔보자.  
배열 인덱스 기반(C++ 스타일) 말고, **딕셔너리로 구현한 Trie** + **둘의 차이점 정리**까지 해볼게.

---

## 1. 딕셔너리 기반 Trie 구현 (파이썬스럽게)

### (1) 가장 직관적인 버전 – 중첩 dict + `'#'` 마커

```python
class DictTrie:
    def __init__(self):
        # 루트는 비어있는 dict
        self.root = {}

    def insert(self, s: str):
        cur = self.root
        print(s)  # C++ 코드와 비슷하게 디버깅 출력

        for c in s:
            # 현재 노드에 c라는 자식이 없으면 새 dict 생성
            if c not in cur:
                print(c)
                cur[c] = {}
            # 다음 노드로 이동
            cur = cur[c]

        # 단어의 끝이라는 표시용 마커
        cur['#'] = True     # '#': end-of-word 마커
        # nodeCnt 개념이 없으니, 대신 현재 노드 수 비슷하게 보고 싶다면:
        # (선택) print("노드 수 비슷한 개념:", self._count_nodes())

    def find(self, s: str) -> bool:
        cur = self.root
        for c in s:
            if c not in cur:     # 경로가 없으면 바로 False
                return False
            cur = cur[c]
        return cur.get('#', False)

    # (선택) 디버깅용 노드 개수 세기
    def _count_nodes(self):
        def dfs(node):
            cnt = 1  # 자기 자신
            for k, child in node.items():
                if k == '#':
                    continue
                cnt += dfs(child)
            return cnt
        return dfs(self.root) if self.root else 0


def main():
    trie = DictTrie()
    n = 3

    for _ in range(n):
        tmp = input().strip()
        trie.insert(tmp)

    print(int(trie.find("PL")))
    print(int(trie.find("PLA")))
    print(int(trie.find("PLC")))


if __name__ == "__main__":
    main()
```

- 입력:
  ```
  PL
  PLA
  PLC
  ```
- 출력 마지막 세 줄: `1 1 1` (C++ 코드의 `find`와 동일한 의미)

---

## 2. 지금 배열 기반 Trie와 **무엇이 다른지**

### ① 메모리 구조 / 관리 방식

**배열 기반(C++) / 파이썬 포팅 코드:**

```cpp
int pos[100000][26];
bool isEnd[100000];
int nodeCnt;
```

- `pos[node][0~25]`로 **다음 노드 인덱스를 정적 배열에 박아두는 방식**.
- `nodeCnt`가 “노드 번호”이자 “현재까지 사용된 노드 개수”.
- **최대 노드 수(100000)** 를 미리 잡아야 해서,
  - 실제로 적게 써도 메모리를 크게 먹고,
  - 더 많이 필요하면 오버플로우 위험.

**딕셔너리 기반:**

```python
self.root = {}
# 각 노드는 dict, { 'P': {...}, 'L': {...}, '#': True } 이런 식
```

- 필요한 순간에만 키를 추가하는 **동적 구조**.
- 미리 `max_nodes`를 잡을 필요가 없음.
- 다양한 문자(알파벳, 숫자, 한글 등)를 그대로 키로 쓸 수 있음.
- 메모리는 실제로 사용된 경로만큼만 쓰는 느낌(오버헤드는 있지만 낭비되는 큰 고정 배열은 없음).

---

### ② 문자 집합 제약

**배열 기반:**

```cpp
int cur_idx = c - 'A';   // 0~25
```

- **대문자 A~Z 26개만** 처리 가능.
- 소문자, 숫자, 한글 등 쓰려면
  - “좌표 압축”하거나
  - 범위를 더 크게 잡은 배열이 필요함.

**딕셔너리 기반:**

```python
if c not in cur:
    cur[c] = {}
cur = cur[c]
```

- `c`가 **어떤 문자든 상관 없음** (유니코드 포함).
- 별도의 인덱스 계산, 좌표 압축 없이 바로 `dict` 키로 사용.

---

### ③ 없는 경로를 만났을 때의 동작 (여기가 꽤 중요해)

**배열 기반 `find` (현재 코드)**

```cpp
bool find(string s){
    int cur = 0;
    for(char c : s){
        int char_idx = c-'A';
        cur = pos[cur][char_idx];  // 여기가 문제 포인트
    }
    return isEnd[cur];
}
```

- 만약 중간에 `pos[cur][char_idx] == 0`이면,
  - `cur`이 다시 **0(루트)** 로 돌아가버림.
- 즉, 실제로는 **경로가 없는데도**, 그냥 0번 노드(루트)를 따라가 버리고,
- 마지막에 `isEnd[0]`를 보고 판단함.
- 이 코드는 “입력으로 주는 문자열은 항상 트라이 안에 있다”는 전제를 깔고 만든 거에 가깝고,  
  **없는 문자열에 대한 예외 처리가 없다**는 게 단점.

**딕셔너리 기반 `find`**

```python
for c in s:
    if c not in cur:
        return False
    cur = cur[c]
return cur.get('#', False)
```

- 중간에 경로가 없으면 **그 즉시 False 반환**.
- 더 안전하고, 직관적인 동작.
- 보통 알고리즘 문제/실전 코드에서는 이쪽이 더 바람직함.

> ✏️ 요약:  
> - **배열 버전**: 경로가 없을 때도 그냥 0으로 가버려서, 버그의 씨앗이 될 수 있음.  
> - **dict 버전**: 경로가 없으면 바로 `False`, 예측 가능한 동작.

---

### ④ 구현 난이도 / 가독성

- **배열 기반**:
  - 인덱스, 노드 번호, `nodeCnt`, 배열 크기 등 신경쓸 게 많음.
  - C++에선 빠르고 익숙한 패턴이지만, 파이썬에선 오히려 코드가 장황해짐.
- **딕셔너리 기반**:
  - 논리 자체가 트리 모습과 거의 1:1이라 읽기 좋음.
  - "없으면 dict 하나 만들고, 있으면 그걸로 들어간다"라는 패턴이라 **학습/디버깅에 훨씬 유리**.

---

### ⑤ 시간복잡도 측면

둘 다 **논리적 시간복잡도는 동일**:

- `insert(s)` : `O(|s|)`
- `find(s)`   : `O(|s|)`

다만,

- 배열 기반은 **상수 시간 factor**가 조금 더 작을 수 있음(C에서 메모리 연속).
- 파이썬 dict는 해시 테이블이라, 키 접근이 평균 `O(1)`이지만, 해시 계산 + 해시 테이블 오버헤드가 있음.
- 실전 파이썬에서는 “트라이는 대부분 딕셔너리 버전”을 쓰는 편이고,  
  알고리즘 문제에서도 속도 문제 거의 없음.

---

## 3. 정리해보면

- 너가 C++ 스타일 배열 기반 구현을 **파이썬으로 그대로 옮긴 현재 코드**는:
  - 최대 노드 수 제한이 있고,
  - 문자 집합이 고정(대문자 26개),
  - 없는 문자열 처리에 대한 예외 케이스가 약함.
- 내가 지금 만든 **딕셔너리 기반 구현**은:
  - 동적으로 확장되고,
  - 문자에 제한이 없고,
  - 없는 문자열에 대해 안전하게 `False`를 반환하고,
  - 파이썬스럽고, 공부용/실전용으로 더 쓰기 좋음.

---

원하면  
- 딕셔너리 버전으로 “**자동 완성(접두사로 시작하는 단어들 찾기)**”,  
- “**단어 개수 세기**”,  
- “**지워지는 Trie(erase)**”  
같은 것도 확장해서 같이 짜볼까?

---
