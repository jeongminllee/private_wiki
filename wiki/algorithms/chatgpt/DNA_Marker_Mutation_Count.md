---
type: Concept
title: "DNA Marker Mutation Count"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2023-11-20)"
tags: [algorithms, chatgpt-export]
timestamp: 2023-11-20
status: active
---

# DNA Marker Mutation Count

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-11-20

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
문제
인간의 DNA 구조는 A, C, G, T로 이루어진 하나의 긴 문자열로 표현할 수 있다.

이때, 몇 몇 질병은 DNA 구조를 나타낸 문자열의 어떤 연속된 부분 문자열과 관련이 있다는 것이 밝혀져 있다. 만일 DNA가 특정 문자열을 부분 문자열로 가진다면 그 질병에 걸릴 가능성이 높다는 것이다. 이러한 특정 문자열을 마커(marker)라 한다.

하지만 때때로 DNA 구조를 그대로 확인하는 것만으로는 질병과 관련된 마커를 확인할 수 없는 경우가 있다. 마커의 돌연변이 가능성 때문이다.

마커의 돌연변이는 아래와 같이 일어난다.

먼저, 마커를 세 부분으로 나눈다, 이때, 첫 부분과 세 번째 부분은 비어 있어도 된다.
두 번째 부분을 뒤집는다.
예를 들어 마커가 AGGT라면 아래와 같은 여섯 가지 경우가 가능하다.

GAGT, GGAT, TGGA, AGGT, ATGG, AGTG

어떤 사람의 DNA 구조와 마커가 주어졌을 때, DNA 내에 마커가 돌연변이의 형태를 포함하여 몇 번 출현하는지 세는 프로그램을 작성하라.

단, 마커의 출현 위치는 서로 겹쳐도 된다. 예를 들어 DNA 구조가 ATGGAT이며 마커가 AGGT라면 답은 3이 된다. ATGG, TGGA, GGAT가 한 번씩 출현하기 때문이다.

입력
첫 줄에 테스트 케이스의 수 T가 주어진다.

각 테스트 케이스의 첫 줄엔 두 개의 정수 n과 m이 주어진다. 이는 각각 DNA 문자열의 길이와 마커의 길이이다. (1 ≤ n ≤ 1,000,000, 1 ≤ m ≤ 100) 두 번째 줄엔 DNA 구조가 주어진다. 마지막 줄엔 마커가 주어진다.

모든 DNA와 마커는 A,G,T,C로만 이루어진 문자열이다.

출력
각 테스트 케이스마다 주어진 DNA 구조에 마커와 그 돌연변이가 몇 번 출현하는지 하나의 정수로 출력한다.

만일 DNA 구조 내에 마커 또는 그 돌연변이가 한 번도 출현하지 않는다면 답은 0이 된다.

2
6 4
ATGGAT
AGGT
6 4
ATGGAT
AGCT

### 💡 답변 (Assistant)
문자열 내에서 특정 패턴 또는 부분 문자열을 찾는 문제군요! 주어진 조건에 따라 문자열을 처리하여 출현 횟수를 찾을 수 있습니다. Python을 사용하여 풀어보도록 하죠.

```python
def count_mutated_markers(dna, marker):
    count = 0
    marker_length = len(marker)
    for i in range(len(dna) - marker_length + 1):
        substring = dna[i:i + marker_length]
        # 마커와 부분 문자열이 일치하는지 확인
        if substring == marker:
            count += 1
        else:
            # 두 번째 부분을 뒤집어서 일치하는지 확인 (돌연변이 확인)
            mutated_marker = substring[0] + substring[-1:0:-1] + substring[-1]
            if mutated_marker == marker:
                count += 1
    return count

# 테스트 케이스 수 입력 받기
test_cases = int(input())

for _ in range(test_cases):
    n, m = map(int, input().split())
    dna = input()
    marker = input()

    # 결과 출력
    result = count_mutated_markers(dna, marker)
    print(result)
```

이 코드는 각 테스트 케이스에 대해 DNA 문자열과 마커를 입력 받고, `count_mutated_markers` 함수를 통해 마커와 돌연변이가 출현하는 횟수를 계산하여 출력합니다. 주어진 조건에 따라 돌연변이를 확인하고, 해당하는 출현 횟수를 계산합니다.

---

### 💡 답변 (Assistant)
문자열 처리와 관련된 문제로 보입니다! 주어진 DNA 문자열과 마커의 출현 횟수를 계산하는 것이 목표군요. 이를 Python으로 구현하여 보겠습니다.

```python
def count_mutated_markers(dna, marker):
    count = 0
    marker_length = len(marker)
    for i in range(len(dna) - marker_length + 1):
        substring = dna[i:i + marker_length]
        # 마커와 부분 문자열이 일치하는지 확인
        if substring == marker:
            count += 1
        else:
            # 두 번째 부분을 뒤집어서 일치하는지 확인 (돌연변이 확인)
            mutated_marker = substring[0] + substring[-1:0:-1] + substring[-1]
            if mutated_marker == marker:
                count += 1
    return count

# 테스트 케이스 수 입력 받기
test_cases = int(input())

for _ in range(test_cases):
    n, m = map(int, input().split())
    dna = input()
    marker = input()

    # 결과 출력
    result = count_mutated_markers(dna, marker)
    print(result)
```

이 코드는 입력을 받아 각 테스트 케이스에 대해 `count_mutated_markers` 함수를 통해 마커와 돌연변이가 출현하는 횟수를 계산하여 출력합니다. 부분 문자열을 확인하고, 돌연변이를 고려하여 출현 횟수를 계산합니다.

---

### 💡 답변 (Assistant)
이 문제를 해결하는 방법 중 하나는 주어진 DNA 문자열에서 마커와 돌연변이를 고려하여 출현 횟수를 계산하는 것입니다. Python을 사용하여 코드를 작성해보겠습니다.

```python
def count_mutated_markers(dna, marker):
    count = 0
    marker_length = len(marker)
    for i in range(len(dna) - marker_length + 1):
        substring = dna[i:i + marker_length]
        # 마커와 부분 문자열이 일치하는지 확인
        if substring == marker:
            count += 1
        else:
            # 두 번째 부분을 뒤집어서 일치하는지 확인 (돌연변이 확인)
            mutated_marker = substring[0] + substring[-1:0:-1] + substring[-1]
            if mutated_marker == marker:
                count += 1
    return count

# 테스트 케이스 수 입력 받기
test_cases = int(input())

for _ in range(test_cases):
    n, m = map(int, input().split())
    dna = input()
    marker = input()

    # 결과 출력
    result = count_mutated_markers(dna, marker)
    print(result)
```

이 코드는 각 테스트 케이스에 대해 DNA 문자열과 마커를 입력 받고, `count_mutated_markers` 함수를 통해 마커와 돌연변이가 출현하는 횟수를 계산하여 출력합니다. 주어진 조건에 따라 돌연변이를 확인하고, 해당하는 출현 횟수를 계산합니다.

---

### 💡 답변 (Assistant)
문자열 처리 문제로 보이네요! DNA 문자열과 마커의 출현 횟수를 계산하는 방법을 Python으로 작성해볼게요.

```python
def count_mutated_markers(dna, marker):
    count = 0
    marker_length = len(marker)
    for i in range(len(dna) - marker_length + 1):
        substring = dna[i:i + marker_length]
        if substring == marker:
            count += 1
        else:
            mutated_marker = substring[0] + substring[-1:0:-1] + substring[-1]
            if mutated_marker == marker:
                count += 1
    return count

# 테스트 케이스 수 입력 받기
test_cases = int(input())

for _ in range(test_cases):
    n, m = map(int, input().split())
    dna = input()
    marker = input()

    # 결과 출력
    result = count_mutated_markers(dna, marker)
    print(result)
```

이 코드는 각 테스트 케이스마다 DNA 문자열과 마커를 입력받고, `count_mutated_markers` 함수를 사용하여 마커와 돌연변이가 출현하는 횟수를 계산하고 출력합니다. 함수는 문자열을 순회하며 해당 패턴과 돌연변이 패턴을 비교하여 카운트합니다.

---

### ❓ 질문 (User)
#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;
int N, M;
struct Trie {
	Trie* next[4];
	Trie* fail;
	int output;
	Trie() : output(0), fail(nullptr) {
		fill(next, next + 4, nullptr);
	}
	~Trie() {
		for (int i = 0; i < 4; i++) {
			if (next[i])
				delete next[i];
		}
	}
	void insert(string& s, int idx) {
		if (idx >= s.length()) {
			output = 1;
			return;
		}
		int x = s[idx] - '0';
		if (!next[x]) {
			next[x] = new Trie();
		}
		next[x]->insert(s, idx + 1);
	}
};
void fail(Trie* root) {
	queue<Trie*> q;
	root->fail = root;
	q.push(root);
	while (!q.empty()) {
		Trie* cur = q.front();
		q.pop();
		for (int i = 0; i < 4; i++) {
			Trie* nxt = cur->next[i];
			if (!nxt)
				continue;
			if (root == cur)
				nxt->fail = root;
			else {
				Trie* tmp = cur->fail;
				while (tmp != root && !tmp->next[i])
					tmp = tmp->fail;
				if (tmp->next[i])
					tmp = tmp->next[i];
				nxt->fail = tmp;
			}
			nxt->output += nxt->fail->output;
			q.push(nxt);
		}
	}
}
int solve(string s, Trie* root) {
	int ret = 0;
	Trie* cur = root;
	for (int i = 0; i < s.length(); i++) {
		int nxt = s[i] - '0';
		while (cur != root && !cur->next[nxt])
			cur = cur->fail;
		if (cur->next[nxt])
			cur = cur->next[nxt];
		ret += cur->output;
	}
	return ret;
}
int main() {
	cin.tie(0);
	cout.tie(0);
	ios::sync_with_stdio(false);
	
	int t;
	cin >> t;
	while (t--) {
		cin >> N >> M;
		string s, m;
		cin >> s >> m;
		Trie* root = new Trie();
		for (int i = 0; i < N; i++) {
			if (s[i] == 'A')
				s[i] = '0';
			else if (s[i] == 'C')
				s[i] = '1';
			else if (s[i] == 'G')
				s[i] = '2';
			else
				s[i] = '3';
		}
		for (int i = 0; i < M; i++) {
			if (m[i] == 'A')
				m[i] = '0';
			else if (m[i] == 'C')
				m[i] = '1';
			else if (m[i] == 'G')
				m[i] = '2';
			else
				m[i] = '3';
		}
		root->insert(m, 0);
		for (int i = 0; i <= M; i++) {
			for (int j = i + 2; j <= M; j++) {
				reverse(m.begin() + i, m.begin() + j);
				root->insert(m, 0);
				reverse(m.begin() + i, m.begin() + j);
			}
		}
		fail(root);
		cout << solve(s, root) << "\n";
		delete root;
	}
}
파이썬 코드로 바꿔줘

### 💡 답변 (Assistant)
주어진 C++ 코드를 Python으로 옮겨볼게요. 주어진 C++ 코드는 Trie 자료구조를 사용하여 문자열을 처리하고, 마커의 돌연변이를 고려하여 출현 횟수를 계산하는 것 같아요.

```python
from collections import deque

class Trie:
    def __init__(self):
        self.next = [None] * 4
        self.fail = None
        self.output = 0

def insert(trie, s, idx):
    if idx >= len(s):
        trie.output = 1
        return
    x = ord(s[idx]) - ord('0')
    if not trie.next[x]:
        trie.next[x] = Trie()
    insert(trie.next[x], s, idx + 1)

def construct_fail(root):
    q = deque()
    root.fail = root
    q.append(root)
    while q:
        cur = q.popleft()
        for i in range(4):
            nxt = cur.next[i]
            if not nxt:
                continue
            if root == cur:
                nxt.fail = root
            else:
                tmp = cur.fail
                while tmp != root and not tmp.next[i]:
                    tmp = tmp.fail
                if tmp.next[i]:
                    tmp = tmp.next[i]
                nxt.fail = tmp
            nxt.output += nxt.fail.output
            q.append(nxt)

def solve(s, root):
    ret = 0
    cur = root
    for char in s:
        nxt = ord(char) - ord('0')
        while cur != root and not cur.next[nxt]:
            cur = cur.fail
        if cur.next[nxt]:
            cur = cur.next[nxt]
        ret += cur.output
    return ret

t = int(input())
for _ in range(t):
    N, M = map(int, input().split())
    s = list(input())
    m = list(input())
    
    root = Trie()
    for i in range(N):
        if s[i] == 'A':
            s[i] = '0'
        elif s[i] == 'C':
            s[i] = '1'
        elif s[i] == 'G':
            s[i] = '2'
        else:
            s[i] = '3'
    
    for i in range(M):
        if m[i] == 'A':
            m[i] = '0'
        elif m[i] == 'C':
            m[i] = '1'
        elif m[i] == 'G':
            m[i] = '2'
        else:
            m[i] = '3'
    
    insert(root, m, 0)
    for i in range(M + 1):
        for j in range(i + 2, M + 1):
            m[i:j] = reversed(m[i:j])
            insert(root, m, 0)
            m[i:j] = reversed(m[i:j])
    
    construct_fail(root)
    print(solve(s, root))
```

위 코드는 C++ 코드를 Python으로 변환한 것입니다. Trie 자료구조와 관련된 로직은 유지되고, 문자열 처리 및 알고리즘 로직이 변경되었습니다. 이제 파이썬 코드로 주어진 문제를 해결할 수 있을 것입니다!

---

### ❓ 질문 (User)
#include <bits/stdc++.h>
using namespace std;

class NODE {
public:
	int state, fail;
	vector<int> next;
	NODE(int num) {
		next.resize(num);
		state = -1;
		fail = 0;
	}
};
class Trie
{
public:
	int nsz; // node size
	vector<NODE> node;
	int MX;
	int num; // 등장 가능한 문자의 갯수	
	Trie(int _MX, int _num) {
		MX = _MX;
		num = _num;
		node.resize(MX, NODE(num));
		nsz = 0;
	}
	int c2i(char c) { // character to int
		if (c == 'A')return 0;
		else if (c == 'C')return 1;
		else if (c == 'G') return 2;
		else return 3;
	}
	void insert(string& P, int ptag) // ptag : pattern의 tag
	{
		int cur = 0;
		for (auto c : P) {
			int n = c2i(c);
			if (node[cur].next[n] == 0) {
				++nsz;
				node[cur].next[n] = nsz;
				cur = nsz;
			}
			else
				cur = node[cur].next[n];
		}
		node[cur].state = ptag;
	}

	void Fail()
	{
		int root = 0;
		queue <int> q;
		node[root].fail = root;
		q.push(root);

		while (!q.empty()) {
			int cur = q.front();
			q.pop();
			for (int n = 0; n < num; ++n) {
				int child = node[cur].next[n];
				if (!child) continue;
				if (cur == root)
					node[child].fail = root;
				else {
					int t = node[cur].fail;
					while (t != root && node[t].next[n] == 0)
						t = node[t].fail;
					if (node[t].next[n])
						t = node[t].next[n];
					node[child].fail = t;
				}
				if (node[node[child].fail].state != -1)
					node[child].state = node[node[child].fail].state;
				q.push(child);
			}
		}
	}

	int Aho(string& S) {
		int cnt = 0;
		int cur = 0, root = 0;
		for (int i = 0; i < S.size(); i++) {
			int n = c2i(S[i]);
			while (cur != root && node[cur].next[n] == 0)
				cur = node[cur].fail;
			if (node[cur].next[n])
				cur = node[cur].next[n];
			if (node[cur].state != -1)
				cnt++;
		}
		return cnt;
	}
};

int T;
int N, M;
int main()
{
	ios::sync_with_stdio(false);
	cin.tie(0);
	int T;
	cin >> T;
	while (T--) {
		int N, M;
		cin >> N >> M;
		string S, Marker;
		cin >> S >> Marker;
		vector<string> P;
		for (int i = 0; i < M; i++) {
			for (int j = i + 1; j <= M; j++) {
				reverse(Marker.begin() + i, Marker.begin() + j);
				P.push_back(Marker);
				reverse(Marker.begin() + i, Marker.begin() + j);
			}
		}
		sort(P.begin(), P.end());
		P.erase(unique(P.begin(), P.end()), P.end());
		Trie T(P.size()*M + 15, 4);
		for (int i = 0; i < P.size(); i++)
			T.insert(P[i], i);
		T.Fail();
		cout << T.Aho(S) << '\n';
	}
}

파이썬 코드로 작성해줘

### 💡 답변 (Assistant)
주어진 C++ 코드를 파이썬으로 옮기는 작업을 해보겠습니다. 이 코드는 Aho-Corasick 알고리즘을 사용하여 문자열에서 패턴과 패턴의 돌연변이가 출현하는 횟수를 계산하는 문제입니다.

```python
class Node:
    def __init__(self, num):
        self.state = -1
        self.fail = 0
        self.next = [0] * num

class Trie:
    def __init__(self, MX, num):
        self.nsz = 0
        self.node = [Node(num) for _ in range(MX)]
        self.MX = MX
        self.num = num
    
    def c2i(self, c):
        if c == 'A':
            return 0
        elif c == 'C':
            return 1
        elif c == 'G':
            return 2
        else:
            return 3
    
    def insert(self, P, ptag):
        cur = 0
        for c in P:
            n = self.c2i(c)
            if self.node[cur].next[n] == 0:
                self.nsz += 1
                self.node[cur].next[n] = self.nsz
                cur = self.nsz
            else:
                cur = self.node[cur].next[n]
        self.node[cur].state = ptag

    def fail(self):
        root = 0
        q = []
        self.node[root].fail = root
        q.append(root)

        while q:
            cur = q.pop(0)
            for n in range(self.num):
                child = self.node[cur].next[n]
                if not child:
                    continue
                if cur == root:
                    self.node[child].fail = root
                else:
                    t = self.node[cur].fail
                    while t != root and self.node[t].next[n] == 0:
                        t = self.node[t].fail
                    if self.node[t].next[n]:
                        t = self.node[t].next[n]
                    self.node[child].fail = t
                if self.node[self.node[child].fail].state != -1:
                    self.node[child].state = self.node[self.node[child].fail].state
                q.append(child)

    def aho(self, S):
        cnt = 0
        cur = 0
        root = 0
        for i in range(len(S)):
            n = self.c2i(S[i])
            while cur != root and self.node[cur].next[n] == 0:
                cur = self.node[cur].fail
            if self.node[cur].next[n]:
                cur = self.node[cur].next[n]
            if self.node[cur].state != -1:
                cnt += 1
        return cnt

T = int(input())
for _ in range(T):
    N, M = map(int, input().split())
    S, Marker = input().split()

    P = []
    for i in range(M):
        for j in range(i + 1, M + 1):
            Marker = list(Marker)
            Marker[i:j] = reversed(Marker[i:j])
            P.append("".join(Marker))
            Marker = list(Marker)
            Marker[i:j] = reversed(Marker[i:j])

    P = list(set(P))
    P.sort()
    T = Trie(len(P) * M + 15, 4)
    for idx, pattern in enumerate(P):
        T.insert(pattern, idx)
    T.fail()
    print(T.aho(S))
```

위 코드는 C++ 코드를 파이썬으로 옮긴 것입니다. 클래스와 메소드 이름을 변경하고 일부 로직을 파이썬에 맞게 수정하였습니다. 이제 주어진 문제를 해결하는 파이썬 코드를 가지고 있습니다!

---

### ❓ 질문 (User)
class Node:
    def __init__(self, num):
        self.state = -1
        self.fail = 0
        self.next = [0] * num

class Trie:
    def __init__(self, MX, num):
        self.nsz = 0
        self.node = [Node(num) for _ in range(MX)]
        self.MX = MX
        self.num = num
    
    def c2i(self, c):
        if c == 'A':
            return 0
        elif c == 'C':
            return 1
        elif c == 'G':
            return 2
        else:
            return 3
    
    def insert(self, P, ptag):
        cur = 0
        for c in P:
            n = self.c2i(c)
            if self.node[cur].next[n] == 0:
                self.nsz += 1
                self.node[cur].next[n] = self.nsz
                cur = self.nsz
            else:
                cur = self.node[cur].next[n]
        self.node[cur].state = ptag

    def fail(self):
        root = 0
        q = []
        self.node[root].fail = root
        q.append(root)

        while q:
            cur = q.pop(0)
            for n in range(self.num):
                child = self.node[cur].next[n]
                if not child:
                    continue
                if cur == root:
                    self.node[child].fail = root
                else:
                    t = self.node[cur].fail
                    while t != root and self.node[t].next[n] == 0:
                        t = self.node[t].fail
                    if self.node[t].next[n]:
                        t = self.node[t].next[n]
                    self.node[child].fail = t
                if self.node[self.node[child].fail].state != -1:
                    self.node[child].state = self.node[self.node[child].fail].state
                q.append(child)

    def aho(self, S):
        cnt = 0
        cur = 0
        root = 0
        for i in range(len(S)):
            n = self.c2i(S[i])
            while cur != root and self.node[cur].next[n] == 0:
                cur = self.node[cur].fail
            if self.node[cur].next[n]:
                cur = self.node[cur].next[n]
            if self.node[cur].state != -1:
                cnt += 1
        return cnt

T = int(input())
for _ in range(T):
    N, M = map(int, input().split())
    S = input()
    Marker = input()

    P = []
    for i in range(M):
        for j in range(i + 1, M + 1):
            Marker = list(Marker)
            Marker[i:j] = reversed(Marker[i:j])
            P.append("".join(Marker))
            Marker = list(Marker)
            Marker[i:j] = reversed(Marker[i:j])

    P = list(set(P))
    P.sort()
    T = Trie(len(P) * M + 15, 4)
    for idx, pattern in enumerate(P):
        T.insert(pattern, idx)
    T.fail()
    print(T.aho(S))
이 코드가 지금 시간 복잡도가 어떻게 되는지 알아?

### 💡 답변 (Assistant)
주어진 코드는 Aho-Corasick 알고리즘을 사용하여 문자열에서 패턴과 패턴의 돌연변이가 출현하는 횟수를 계산합니다. 시간 복잡도는 일반적인 경우에는 **O(N + M + Z)**입니다. 여기서 N은 입력 문자열 S의 길이, M은 마커의 길이, Z는 모든 마커와 그 돌연변이의 총 길이입니다.

처음에 마커의 돌연변이를 생성할 때 이중 반복문을 사용하여 마커의 모든 부분 문자열을 생성합니다. 이 작업은 **O(M^2)**입니다. 그리고 이 부분 문자열의 중복을 제거하고 정렬하는 과정은 **O(M^2 * log(M))**이 소요됩니다.

그 후 Trie 자료구조를 만들고 초기화하는 과정은 Trie의 노드 수를 MX라고 할 때, **O(MX)**입니다. 이후 Aho-Corasick 알고리즘에서 각 문자에 대해 패턴 매칭을 수행하는데, 이는 문자열 S의 길이인 N에 대해 수행되므로 **O(N)**입니다.

따라서 전체적으로 이 코드의 시간 복잡도는 **O(M^2 * log(M) + MX + N)**입니다. 여기서 MX는 Trie의 노드 수로, 패턴과 패턴의 돌연변이의 총 길이와 관련이 있습니다.

---

### ❓ 질문 (User)
시간 복잡도를 줄일 수 있는 방법 있을까>?

### 💡 답변 (Assistant)
시간 복잡도를 줄일 수 있는 몇 가지 방법이 있습니다. 주어진 코드에서 시간 복잡도를 개선할 수 있는 몇 가지 방법을 알려드릴게요.

1. **중복 제거와 정렬 단계 최적화**: 마커의 모든 부분 문자열을 생성하는 과정에서 중복을 제거하고 정렬하는 부분은 시간이 많이 소요됩니다. 중복을 제거하는 과정에서 set을 사용하고, 정렬은 마지막에 한 번만 수행하는 것이 효율적입니다.

2. **마커 생성 최적화**: 중복을 최소화하면서 마커의 돌연변이를 생성하는 부분을 최적화할 수 있습니다. 이 부분에서 모든 부분 문자열을 생성하는 것이 아니라, 필요한 부분만 생성하도록 로직을 수정할 수 있습니다.

3. **Trie 자료구조 최적화**: Trie 자료구조를 더 효율적으로 구현하여 노드 수를 줄일 수 있습니다. 일부 Trie 구현 방법은 메모리를 더 효율적으로 사용할 수 있습니다.

4. **Aho-Corasick 알고리즘 최적화**: Aho-Corasick 알고리즘의 구현을 최적화하여 문자열을 더 효율적으로 처리할 수 있습니다. 예를 들어, 불필요한 계산을 줄이고 더 효율적인 탐색을 수행하는 방법 등이 있습니다.

이러한 최적화를 통해 시간 복잡도를 줄일 수 있습니다. 특히 중복 제거와 정렬 과정을 최적화하는 것이 시간 단축에 큰 영향을 미칠 수 있습니다. 하지만 각 단계의 최적화가 알고리즘 전체에 미치는 영향을 고려하여 수정하는 것이 중요합니다.

---
