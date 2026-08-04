---
type: Concept
title: "연립방정식 LaTeX 사용법"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-05-12)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-05-12
status: active
---

# 연립방정식 LaTeX 사용법

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-12

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
수학에서 연립방정식을 **왼쪽 중괄호로 묶고 2줄로 쓰는 형태**는 LaTeX에서 보통 `cases` 환경을 씁니다.

```latex
\[
\begin{cases}
x + y = 3 \\
2x - y = 1
\end{cases}
\]
```

결과는 이런 형태입니다.

\[
\begin{cases}
x + y = 3 \\
2x - y = 1
\end{cases}
\]

핵심은 다음입니다.

```latex
\begin{cases}
첫 번째 식 \\
두 번째 식
\end{cases}
```

여기서 `\\`는 **줄바꿈**입니다.

만약 식을 등호 기준으로 정렬하고 싶다면 `aligned`를 같이 쓰면 더 깔끔합니다.

```latex
\[
\left\{
\begin{aligned}
x + y &= 3 \\
2x - y &= 1
\end{aligned}
\right.
\]
```

결과:

\[
\left\{
\begin{aligned}
x + y &= 3 \\
2x - y &= 1
\end{aligned}
\right.
\]

정리하면:

```latex
\begin{cases}
...
\end{cases}
```

는 간단한 연립방정식에 좋고,

```latex
\left\{
\begin{aligned}
...
\end{aligned}
\right.
```

는 등호 정렬까지 하고 싶을 때 좋습니다.

---

### ❓ 질문 (User)
수학에서 연립방정식을 사용할 때 보면 2줄로 쓰잖아. latex 로는 어떻게 쓰는지 알려줘
