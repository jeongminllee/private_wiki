---
type: Concept
title: "Similar LeetCode Problems"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2024-07-07)"
tags: [algorithms, chatgpt-export]
timestamp: 2024-07-07
status: active
---

# Similar LeetCode Problems

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-07-07

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
프로그래머스 '주식 가격' 문제와 유사한 문제를 leetcode 에서 찾아줘

### 💡 답변 (Assistant)
If you're looking for problems on LeetCode similar to the "주식 가격" (Stock Prices) problem from Programmers, there are a couple of relevant ones you can check out:

1. **Stock Price Fluctuation**:
   - This problem involves maintaining and querying the latest stock prices along with their historical fluctuations. It requires designing a data structure that supports updates to stock prices and efficiently retrieves the current, maximum, and minimum prices.
   - You can find it [here](https://leetcode.com/problems/stock-price-fluctuation/)【5†source】.

2. **Online Stock Span**:
   - This problem focuses on calculating the stock span, which is the number of consecutive days leading up to the current day for which the stock price was less than or equal to the current day's price.
   - You can find it [here](https://leetcode.com/problems/online-stock-span/)【6†source】.

These problems should provide a good challenge and are conceptually similar to the stock price tracking and analysis involved in the "주식 가격" problem.

---

### ❓ 질문 (User)
'''
def solution(prices):
    length = len(prices)
    answer = [i for i in range (length - 1, -1, -1)]
    
    stack = [0]
    for i in range (1, length):
        while stack and prices[stack[-1]] > prices[i]:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer
'''
이 풀이가 답인 문제를 leetcode에서 찾아줘

### 💡 답변 (Assistant)
The problem you are referring to in your solution closely resembles the "Stock Span Problem" on LeetCode, specifically the "Online Stock Span" problem.

In this problem, you need to calculate the span of stock prices for all given days. The span of the stock's price on a given day is defined as the maximum number of consecutive days (starting from today and going backwards) during which the price of the stock was less than or equal to today's price. This is essentially what your provided solution does by maintaining a stack to track indices and calculating the span based on the current and previous prices.

You can find this problem on LeetCode here: [Online Stock Span](https://leetcode.com/problems/online-stock-span/)【12†source】【15†source】. This problem involves similar logic and implementation strategies involving stacks and iterating through the prices list to determine spans.

---
