---
type: Concept
title: "Trailing Zeroes 설명"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2025-05-07)"
tags: [cs, chatgpt-export]
timestamp: 2025-05-07
status: active
---

# Trailing Zeroes 설명

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-05-07

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
the number of trailing zeroes 에 대해서 설명해줘

### 💡 답변 (Assistant)
"The number of trailing zeroes"는 보통 **어떤 수의 끝에 연속으로 붙어 있는 0의 개수**를 의미합니다. 특히 **팩토리얼(factorial)**과 관련된 문제에서 자주 등장하는 개념입니다.

### 예시:
`100!` (100 팩토리얼)은 `100 × 99 × 98 × ... × 1` 인데, 이 수는 매우 크고, 끝에 0이 여러 개 붙어 있습니다.  
이때 **끝에 붙은 0의 개수**를 구하는 것이 "the number of trailing zeroes" 문제입니다.

---

### 왜 0이 생길까?

10 = 2 × 5 이기 때문에, 곱셈 결과로 10이 만들어질 때마다 뒤에 0이 하나 붙습니다.  
그러므로 `n!`에서 뒤에 0이 몇 개 붙는지를 알려면, **2와 5가 몇 쌍 만들어지는지를 세면 됩니다.**

하지만 주의할 점은:
- 2는 짝수마다 나와서 수가 매우 많습니다.
- 5는 상대적으로 적기 때문에, **5의 개수**만 세면 됩니다.

---

### 공식을 정리하면:

`n!`의 trailing zeroes 수는:

\[
\left\lfloor \frac{n}{5} \right\rfloor + \left\lfloor \frac{n}{25} \right\rfloor + \left\lfloor \frac{n}{125} \right\rfloor + \cdots
\]

즉, `n`을 5로 나눈 몫, 25로 나눈 몫, 125로 나눈 몫... 을 계속 더합니다.

---

### 예제:  
**n = 100**

\[
\left\lfloor \frac{100}{5} \right\rfloor = 20 \\
\left\lfloor \frac{100}{25} \right\rfloor = 4 \\
\left\lfloor \frac{100}{125} \right\rfloor = 0
\]

총: **20 + 4 = 24**

→ `100!`의 뒤에는 **0이 24개** 붙습니다.

---

필요하다면 이 내용을 코드로도 보여줄 수 있어요. Python 예제가 필요할까요?

---
