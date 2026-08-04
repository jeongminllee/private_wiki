---
type: Concept
title: "ASCII Art 덧셈 구현"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2025-03-03)"
tags: [cs, chatgpt-export]
timestamp: 2025-03-03
status: active
---

# ASCII Art 덧셈 구현

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-03-03

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
아래는 파이썬으로 구현한 코드입니다. 이 코드는 입력으로 주어진 7줄의 ASCII art에서 각 숫자와 '+' 기호를 인식하여, 두 정수를 더한 후 결과를 다시 ASCII art 형식으로 출력합니다.

```python
# 미리 정의된 ASCII art 패턴: 0~9와 +
DIGITS = {
    '0': [
        "xxxxx",
        "x...x",
        "x...x",
        "x...x",
        "x...x",
        "x...x",
        "xxxxx"
    ],
    '1': [
        "....x",
        "....x",
        "....x",
        "....x",
        "....x",
        "....x",
        "....x"
    ],
    '2': [
        "xxxxx",
        "....x",
        "....x",
        "xxxxx",
        "x....",
        "x....",
        "xxxxx"
    ],
    '3': [
        "xxxxx",
        "....x",
        "....x",
        "xxxxx",
        "....x",
        "....x",
        "xxxxx"
    ],
    '4': [
        "x...x",
        "x...x",
        "x...x",
        "xxxxx",
        "....x",
        "....x",
        "....x"
    ],
    '5': [
        "xxxxx",
        "x....",
        "x....",
        "xxxxx",
        "....x",
        "....x",
        "xxxxx"
    ],
    '6': [
        "xxxxx",
        "x....",
        "x....",
        "xxxxx",
        "x...x",
        "x...x",
        "xxxxx"
    ],
    '7': [
        "xxxxx",
        "....x",
        "....x",
        "....x",
        "....x",
        "....x",
        "....x"
    ],
    '8': [
        "xxxxx",
        "x...x",
        "x...x",
        "xxxxx",
        "x...x",
        "x...x",
        "xxxxx"
    ],
    '9': [
        "xxxxx",
        "x...x",
        "x...x",
        "xxxxx",
        "....x",
        "....x",
        "xxxxx"
    ],
    '+': [
        ".....",
        "..x..",
        "..x..",
        "xxxxx",
        "..x..",
        "..x..",
        "....."
    ]
}

# 역으로 ASCII art에서 문자로 매핑하기 위한 딕셔너리 생성
ART_TO_CHAR = {tuple(art): char for char, art in DIGITS.items()}

import sys

def main():
    # 7줄 입력받기
    lines = [sys.stdin.readline().rstrip("\n") for _ in range(7)]
    n = len(lines[0])
    # 한 글자(숫자 또는 +)의 폭은 5, 글자 사이에는 1열의 점이 있음.
    # 전체 글자 수는 (n + 1) // 6
    num_chars = (n + 1) // 6

    expression = ""
    for i in range(num_chars):
        # 각 문자 영역는 시작열: i*6, 끝열: i*6+5
        char_art = [line[i*6:i*6+5] for line in lines]
        # char_art를 튜플로 만들어 매핑 딕셔너리에서 문자 찾기
        ch = ART_TO_CHAR.get(tuple(char_art))
        if ch is None:
            # 알 수 없는 문자가 있을 경우 (문제 조건상 없으므로)
            ch = "?"
        expression += ch

    # expression은 "a+b" 형태임
    a_str, b_str = expression.split('+')
    result = str(int(a_str) + int(b_str))

    # 결과를 ASCII art로 변환
    result_art = [""] * 7
    for idx, digit in enumerate(result):
        if idx > 0:
            # 글자 사이에 한 열의 점 추가
            for r in range(7):
                result_art[r] += "."
        digit_art = DIGITS[digit]
        for r in range(7):
            result_art[r] += digit_art[r]

    # 결과 출력
    for line in result_art:
        print(line)

if __name__ == '__main__':
    main()
```

### 코드 설명

1. **패턴 정의:**  
   `DIGITS` 딕셔너리에 0~9와 '+'에 해당하는 7×5 ASCII art 패턴을 저장합니다.

2. **역매핑 생성:**  
   `ART_TO_CHAR`는 입력받은 7×5 문자 블록을 해당 문자(숫자 또는 '+')로 변환하는 데 사용됩니다.

3. **입력 처리:**  
   7줄의 입력을 읽고, 각 문자는 5열씩 잘라서 인식합니다. 각 문자의 시작 열은 `i*6` (문자 사이의 구분점 포함)로 계산합니다.

4. **덧셈 수행:**  
   인식된 표현식(a+b)을 파싱하여 정수형으로 변환한 후 덧셈을 수행합니다.

5. **출력 생성:**  
   결과값의 각 숫자에 대해 해당하는 ASCII art를 얻고, 문자 사이에 점 하나의 열을 추가하여 최종 7줄의 결과를 출력합니다.

이 코드를 실행하면 문제에서 요구하는 대로 입력에 해당하는 ASCII art 덧셈 결과를 출력할 수 있습니다.

---

### ❓ 질문 (User)
문제
Nowadays, there are smartphone applications that instantly translate text and even solve math problems if you just point your phone’s camera at them. Your job is to implement a much simpler functionality reminiscent of the past – add two integers written down as ASCII art.

An ASCII art is a matrix of characters, exactly 7 rows high, with each individual character either a dot or the lowercase letter x.

An expression of the form a + b is given, where both a and b are positive integers. The expression is converted into ASCII art by writing all the expression characters (the digits of a and b as well as the + sign) as 7 × 5 matrices, and concatenating the matrices together with a single column of dot characters between consecutive individual matrices. The exact matrices corresponding to the digits and the + sign are as folows:

xxxxx  ....x  xxxxx  xxxxx  x...x  xxxxx  xxxxx  xxxxx  xxxxx  xxxxx  .....
x...x  ....x  ....x  ....x  x...x  x....  x....  ....x  x...x  x...x  ..x..
x...x  ....x  ....x  ....x  x...x  x....  x....  ....x  x...x  x...x  ..x..
x...x  ....x  xxxxx  xxxxx  xxxxx  xxxxx  xxxxx  ....x  xxxxx  xxxxx  xxxxx
x...x  ....x  x....  ....x  ....x  ....x  x...x  ....x  x...x  ....x  ..x..
x...x  ....x  x....  ....x  ....x  ....x  x...x  ....x  x...x  ....x  ..x..
xxxxx  ....x  xxxxx  xxxxx  ....x  xxxxx  xxxxx  ....x  xxxxx  xxxxx  .....
Given an ASCII art for an expression of the form a + b, find the result of the addition and write it out in the ASCII art form.

입력
Input consists of exactly 7 lines and contains the ASCII art for an expression of the form a + b, where both a and b are positive integers consisting of at most 9 decimal digits and written without leading zeros.

출력
Output 7 lines containing ASCII art corresponding to the result of the addition, without leading zeros.

예제 입력 1 
....x.xxxxx.xxxxx.x...x.xxxxx.xxxxx.xxxxx.......xxxxx.xxxxx.xxxxx
....x.....x.....x.x...x.x.....x.........x...x...x...x.x...x.x...x
....x.....x.....x.x...x.x.....x.........x...x...x...x.x...x.x...x
....x.xxxxx.xxxxx.xxxxx.xxxxx.xxxxx.....x.xxxxx.xxxxx.xxxxx.x...x
....x.x.........x.....x.....x.x...x.....x...x...x...x.....x.x...x
....x.x.........x.....x.....x.x...x.....x...x...x...x.....x.x...x
....x.xxxxx.xxxxx.....x.xxxxx.xxxxx.....x.......xxxxx.xxxxx.xxxxx
예제 출력 1 
....x.xxxxx.xxxxx.xxxxx.x...x.xxxxx.xxxxx
....x.....x.....x.x.....x...x.x.........x
....x.....x.....x.x.....x...x.x.........x
....x.xxxxx.xxxxx.xxxxx.xxxxx.xxxxx.....x
....x.x.........x.....x.....x.....x.....x
....x.x.........x.....x.....x.....x.....x
....x.xxxxx.xxxxx.xxxxx.....x.xxxxx.....x

파이썬 코드로 구현해줘
