---
type: Concept
title: "Leetcode 72 문제 풀이"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-05-01)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-05-01
status: active
---

# Leetcode 72 문제 풀이

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-05-01

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
**문제 설명**  
두 개의 문자열 `word1`과 `word2`가 주어졌을 때, `word1`을 `word2`로 바꾸기 위해 필요한 최소 연산 횟수를 구하는 문제입니다. 허용되는 연산은 다음 세 가지입니다.

1. **삽입** (Insert)  
2. **삭제** (Delete)  
3. **교체** (Replace)  

예를 들어,  
```
word1 = "horse"
word2 = "ros"
```
이라면 최소 3번의 연산으로 변환할 수 있습니다.  
- horse → rorse (h → r, replace)  
- rorse → rose  (delete 'r')  
- rose  → ros   (delete 'e')  

---

## 동적 계획법(DP) 풀이 아이디어

1. **DP 상태 정의**  
   `dp[i][j]`를  
   > `word1`의 처음 i글자(`word1[0..i-1]`)를  
   > `word2`의 처음 j글자(`word2[0..j-1]`)로 바꾸는 최소 연산 횟수  
   로 정의합니다.

2. **초기값**  
   - `dp[0][j] = j` : `word1` 빈 문자열 → `word2` 첫 j글자 : 삽입만 j번  
   - `dp[i][0] = i` : `word1` 첫 i글자 → 빈 문자열 : 삭제만 i번  

3. **점화식**  
   - 만약 `word1[i-1] == word2[j-1]` 이면  
     ```
     dp[i][j] = dp[i-1][j-1]
     ```  
     (추가 연산 필요 없음)
   - 그렇지 않으면 세 가지 연산 중 최소값 +1  
     ```
     dp[i][j] = min(
       dp[i-1][j]   + 1,   // delete : word1[i-1] 삭제
       dp[i][j-1]   + 1,   // insert : word2[j-1] 삽입
       dp[i-1][j-1] + 1    // replace: word1[i-1] → word2[j-1]
     )
     ```
   
4. **최종 답**  
   ```
   dp[m][n]
   ```
   (`m = len(word1)`, `n = len(word2)`)

---

## 예시 동작 흐름

`word1 = "horse"`, `word2 = "ros"`  
```text
   ''  r   o   s
''  0   1   2   3
h   1   1   2   3
o   2   2   1   2
r   3   2   2   2
s   4   3   3   2
e   5   4   4   3 ← 결과: 3
```
- `dp[5][3] = 3` → 최소 3회 연산

---

## 파이썬 구현 예시

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp 테이블 초기화 ( (m+1) x (n+1) )
    dp = [[0] * (n+1) for _ in range(m+1)]
    
    # 초기값 설정
    for i in range(1, m+1):
        dp[i][0] = i
    for j in range(1, n+1):
        dp[0][j] = j
    
    # DP 채우기
    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(
                    dp[i-1][j] + 1,    # delete
                    dp[i][j-1] + 1,    # insert
                    dp[i-1][j-1] + 1   # replace
                )
    return dp[m][n]
```

---

## 시간 및 공간 복잡도

- **시간 복잡도**: O(m × n)  
  → 이중 for문으로 dp 테이블 전체를 한 번씩 채움  
- **공간 복잡도**: O(m × n)  
  → (m+1)×(n+1) 크기의 dp 테이블 사용  

### 공간 최적화
1차원 배열 2개(`prev`, `curr`)만 써서 O(n)까지 줄일 수도 있습니다.  
```python
def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    prev = list(range(n+1))  # dp[0][*]
    for i in range(1, m+1):
        curr = [i] + [0]*n
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = min(prev[j] + 1,    # delete
                              curr[j-1] + 1,  # insert
                              prev[j-1] + 1)  # replace
        prev = curr
    return prev[n]
```

이상으로 **Edit Distance** 문제의 핵심 아이디어와 풀이 방법을 정리했습니다. 추가 질문이 있으면 언제든 말씀해주세요!

---

### ❓ 질문 (User)
Leetcode 72. Edit Distance 문제에 대해서 설명해줘.

### 💡 답변 (Assistant)
DP 테이블을 실제로 채워 나가는 과정을 “한 칸씩” 짚어보겠습니다. 예제로 `word1 = "horse"`, `word2 = "ros"`를 사용해 보죠.  

1. **반복문 구조**  
   ```python
   for i in range(1, m+1):      # word1 쪽 인덱스 1부터 m까지
       for j in range(1, n+1):  # word2 쪽 인덱스 1부터 n까지
           # (i,j) 셀을 결정
   ```
   여기서 `i`는 `word1`에서 고려 중인 “끝 위치” 길이, `j`는 `word2`에서 고려 중인 “끝 위치” 길이입니다.

2. **문자 비교부터 시작**  
   ```python
   if word1[i-1] == word2[j-1]:
       dp[i][j] = dp[i-1][j-1]
   ```
   - 예를 들어 `i=2, j=2`인 경우, `word1[1]`(두 번째 글자)와 `word2[1]`(두 번째 글자)을 비교합니다.
   - 같으면 둘 다 마지막 글자를 건너뛴 상태(`i-1, j-1`)의 연산 횟수를 그대로 가져옵니다.

3. **다른 문자일 때 가능한 세 연산**  
   ```python
   else:
       dp[i][j] = min(
           dp[i-1][j]   + 1,   # 삭제(delete)
           dp[i][j-1]   + 1,   # 삽입(insert)
           dp[i-1][j-1] + 1    # 교체(replace)
       )
   ```
   - **삭제(delete)**: `word1`의 마지막 문자 (`word1[i-1]`)를 삭제한 뒤, `i-1, j` 상태에서 오는 경우  
   - **삽입(insert)**: `word2`의 마지막 문자 (`word2[j-1]`)를 `word1`에 삽입한 뒤, `i, j-1` 상태에서 오는 경우  
   - **교체(replace)**: `word1[i-1]`를 `word2[j-1]`로 바꾼 뒤, `i-1, j-1` 상태에서 오는 경우  

4. **칼럼별·로우별 채워 보기**  
   - **i=1, j=1** (`h`→`r`):  
     - 같지 않으므로  
       - delete: `dp[0][1] +1 = 1+1 = 2`  
       - insert: `dp[1][0] +1 = 1+1 = 2`  
       - replace: `dp[0][0] +1 = 0+1 = 1`  
     - → `dp[1][1] = 1`  
   - **i=1, j=2** (`h`→`ro`):  
     - `h` vs `o` 다르므로  
       - delete: `dp[0][2]+1 = 2+1 = 3`  
       - insert: `dp[1][1]+1 = 1+1 = 2`  
       - replace: `dp[0][1]+1 = 1+1 = 2`  
     - → `dp[1][2] = 2`  
   - **i=2, j=1** (`ho`→`r`):  
     - `o` vs `r` 다르므로  
       - delete: `dp[1][1]+1 = 1+1 = 2`  
       - insert: `dp[2][0]+1 = 2+1 = 3`  
       - replace: `dp[1][0]+1 = 1+1 = 2`  
     - → `dp[2][1] = 2`  

   이와 같이 **각 칸마다**  
   1) 문자 일치 여부 확인  
   2) 일치하면 `dp[i-1][j-1]` 그대로,  
   3) 불일치면 세 연산 중 최솟값+1  
   
   을 적용해 나가면, 최종적으로 `dp[5][3] = 3`이 됩니다.

5. **시각적–수치적 흐름**  

   |   i\j   |  0   |  1(`r`) | 2(`o`) | 3(`s`) |
   |:-------:|:----:|:-------:|:------:|:------:|
   | **0**   |  0   |   1     |   2    |   3    |
   | **1**(`h`) |  1   | **1**   |   2    |   3    |
   | **2**(`o`) |  2   |   2     | **1**  |   2    |
   | **3**(`r`) |  3   | **2**   |   2    | **2**  |
   | **4**(`s`) |  4   |   3     |   3    | **2**  |
   | **5**(`e`) |  5   |   4     |   4    | **3**  |

   - **굵은 숫자**는 “일치”로 `dp[i-1][j-1]`를 쓴 경우  
   - 최종 `dp[5][3] = 3`이 바로 정답입니다.

이처럼 **“한 칸씩”** `i`, `j`를 순회하며  
- 일치 시 대각선(↖) 값 그대로  
- 불일치 시 세 방향(←, ↑, ↖) 중 최솟값+1  
를 적용하는 것이 DP 채우기의 핵심입니다. 추가 질문이나 다른 예제가 필요하시면 알려주세요!

---

### ❓ 질문 (User)
DP 채우기 부분을 조금 더 자세하게 설명해주ㅓ
