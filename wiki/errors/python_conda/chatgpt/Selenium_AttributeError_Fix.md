---
type: Error Note
title: "Selenium AttributeError Fix"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2024-12-07)"
tags: [errors, chatgpt-export]
timestamp: 2024-12-07
status: active
---

# Selenium AttributeError Fix

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-12-07

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
파이썬에서 에러 메시지가 자꾸 떠. AttributeError: 'WebDriver' object has no attribute 'find_Element_By_XPath 이 메시지가 의미하는 게 뭔지 알려 줘.알려준 후, 이 코드가 무슨 작업을 수행하는지 알려주고, 어떻게 하면 런타임 에러가 발생하지 않게 코드를 짤 수 있는지 알려줘. 마지막으로, 각 라인마다 주석을 달아줘.

### 💡 답변 (Assistant)
`AttributeError: 'WebDriver' object has no attribute 'find_Element_By_XPath'`라는 에러 메시지는 Python의 Selenium 라이브러리에서 더 이상 지원되지 않는 메서드를 호출할 때 발생합니다. Selenium 4에서는 `find_element_by_xpath`와 같은 "by_" 접두사가 붙은 메서드가 제거되었고, 대신 `find_element(By.XPATH, ...)` 형태를 사용해야 합니다.

### 이 에러 메시지가 의미하는 것
- **문제**: 코드가 Selenium 4의 새로운 메서드 구조를 사용하지 않고, 더 이상 존재하지 않는 구식 메서드를 호출하고 있습니다.
- **원인**: 라이브러리 업데이트 후 API가 변경되었기 때문입니다.

### 코드의 작업
다음은 일반적으로 문제의 코드를 추정한 예입니다:
```python
from selenium import webdriver

driver = webdriver.Chrome()  # 크롬 웹드라이버를 시작
driver.get("http://example.com")  # 주어진 URL로 이동
element = driver.find_Element_By_XPath("//div[@id='example']")  # 특정 요소를 찾음
```
이 코드는 Selenium을 사용해 브라우저를 열고 `http://example.com`으로 이동한 후, XPath로 특정 요소를 찾으려고 시도합니다.

### 수정 방법
Selenium 4에 맞게 코드를 수정하면 다음과 같이 작성할 수 있습니다:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

# 크롬 웹드라이버를 시작
driver = webdriver.Chrome()

# 주어진 URL로 이동
driver.get("http://example.com")

# By.XPATH를 사용해 요소를 찾음
element = driver.find_element(By.XPATH, "//div[@id='example']")
```

### 수정된 코드에 주석 추가
```python
from selenium import webdriver  # Selenium 라이브러리에서 webdriver 모듈을 가져옴
from selenium.webdriver.common.by import By  # 요소를 찾는 데 필요한 By 클래스 가져옴

driver = webdriver.Chrome()  # Chrome 브라우저를 제어하는 WebDriver 객체 생성
driver.get("http://example.com")  # 브라우저에서 주어진 URL로 이동

# By.XPATH를 사용하여 id가 'example'인 div 요소를 찾음
element = driver.find_element(By.XPATH, "//div[@id='example']")
```

이렇게 하면 코드가 최신 Selenium 4에서 제대로 작동하고 런타임 에러가 발생하지 않습니다.

---
