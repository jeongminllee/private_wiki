---
type: Concept
title: "PyCharm 디버깅 필터 설정"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2025-01-25)"
tags: [cs, chatgpt-export]
timestamp: 2025-01-25
status: active
---

# PyCharm 디버깅 필터 설정

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-01-25

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
pycharm 에서 debug 할 때 Protected Attributes 속성을 가진 변수들이 창에 나와서 보기가 불편해. 이 부분을 제거하고 내가 작성한 코드에 있는 변수만 보게하는 세팅 알려줘

### 💡 답변 (Assistant)
PyCharm에서 디버그 중 **Protected Attributes**(`_`로 시작하는 변수)나 불필요한 내부 속성이 디버그 창에 나타나는 경우, 필터를 설정해 원하는 변수만 보이도록 할 수 있습니다. 다음 단계에 따라 설정하세요:

---

### 1. **Debugger Variables 탭에서 필터 사용**
1. 디버깅 중에 PyCharm의 **Variables 창**을 열어둡니다.
2. 오른쪽 상단의 **Settings 아이콘**(톱니바퀴)을 클릭합니다.
3. 팝업 메뉴에서 **"Show Protected Members"** 옵션을 **비활성화**합니다.
   - 이 설정을 끄면 `_`로 시작하는 Protected Attributes가 디버그 창에 표시되지 않습니다.

---

### 2. **Debugger 필터를 커스터마이즈**
1. 디버깅 중 **Variables 창**의 톱니바퀴를 다시 클릭합니다.
2. **"View Options" → "Customize Data Views"**를 선택합니다.
3. **Custom View 옵션**을 설정하여 특정 변수만 포함하거나 제외할 수 있습니다.
   - 예를 들어, 특정 클래스에서 생성된 사용자 정의 변수만 보이게 하려면 해당 클래스 필터를 적용할 수 있습니다.

---

### 3. **Variables 탭에서 관심 있는 변수만 표시**
1. 디버깅 중 특정 변수만 보고 싶다면, **Watch 창**을 사용하세요.
2. Variables 창에서 관심 있는 변수를 **오른쪽 클릭 → "Add to Watches"**로 추가합니다.
3. 이후 Watch 창에서 필터링된 변수를 볼 수 있습니다.

---

### 4. **내부 속성 제외 (Optional)**
PyCharm의 디버거는 Python 객체의 내부 속성(`__`로 시작하거나 끝나는 속성)도 표시합니다. 이를 제외하려면:
1. **Settings** → **Build, Execution, Deployment** → **Debugger**로 이동합니다.
2. **Data Views** 탭에서 **"Show object attributes"** 설정을 **비활성화**합니다.

---

### 요약
- Protected Attributes를 제외하려면: **"Show Protected Members" 비활성화**
- 특정 변수만 보려면: **Watch 창** 또는 **Custom Data Views 사용**
- 내부 속성을 제거하려면: **Debugger Settings → Data Views 조정**

이 설정 후 디버깅 화면이 훨씬 깔끔해질 거예요! 😊

---

### ❓ 질문 (User)
AbstractSet = {_SpecialGenericAlias} typing.AbstractSet
Any = {_AnyMeta} typing.Any
AnyStr = {TypeVar} ~AnyStr
AsyncContextManager = {_SpecialGenericAlias} typing.AsyncContextManager
AsyncGenerator = {_SpecialGenericAlias} typing.AsyncGenerator
AsyncIterable = {_SpecialGenericAlias} typing.AsyncIterable
AsyncIterator = {_SpecialGenericAlias} typing.AsyncIterator
Awaitable = {_SpecialGenericAlias} typing.Awaitable
ByteString = {_DeprecatedGenericAlias} typing.ByteString
Callable = {_CallableType} typing.Callable
ChainMap = {_SpecialGenericAlias} typing.ChainMap
ClassVar = {_SpecialForm} typing.ClassVar
Collection = {_SpecialGenericAlias} typing.Collection
Concatenate = {_SpecialForm} typing.Concatenate
Container = {_SpecialGenericAlias} typing.Container
ContextManager = {_SpecialGenericAlias} typing.ContextManager
Coroutine = {_SpecialGenericAlias} typing.Coroutine
Counter = {_SpecialGenericAlias} typing.Counter

디버그 창에 이런 변수들이 숨겨졌으면 좋겠어

### 💡 답변 (Assistant)
PyCharm 디버거에서 위와 같은 Python의 **`typing` 모듈 관련 변수**나 내부 속성들이 표시되지 않도록 필터링하려면, 아래 방법을 통해 설정할 수 있습니다.

---

### 1. **"Show Debugger Variables" 설정 변경**
이 변수들은 내부적으로 Python의 타입 힌팅(`typing`)에서 생성된 내부 객체입니다. PyCharm에서는 이를 숨기기 위해 다음 설정을 적용합니다.

1. **Variables 창**에서 **톱니바퀴 아이콘(설정)** 클릭.
2. **"Show Variables from Synthetic Frames"** 옵션을 **비활성화**.
   - 이 옵션을 끄면 내부적으로 생성된 시스템 변수나 Python 구현 관련 변수가 사라집니다.

---

### 2. **Variables 필터링 추가**
이 설정을 적용하면 특정 모듈이나 네임스페이스의 변수를 숨길 수 있습니다.

1. **Settings (환경설정)** → **Build, Execution, Deployment** → **Debugger**로 이동.
2. **Data Views** 탭을 선택.
3. **"Skip synthetic variables"** 또는 **"Hide debugger objects"**를 체크.

---

### 3. **Custom Watch를 활용한 필터링**
1. 디버깅 중에 **Variables 창**에 있는 타입 힌트 관련 변수를 **오른쪽 클릭**.
2. **"Add to Watches"**를 선택하여, 관심 있는 변수만 Watch 창에 추가.
3. 이후 Variables 창을 숨기고 Watch 창에서 필요한 변수만 확인.

---

### 4. **코드로 필터링 추가 (고급)**
PyCharm에서 디버깅 중 특정 네임스페이스(예: `typing`)의 객체를 필터링할 수도 있습니다.

#### 방법
1. **Settings** → **Build, Execution, Deployment** → **Debugger** → **Stepping**으로 이동.
2. **"Do not step into scripts"** 항목에 `typing` 모듈을 추가.
   - 예: `Add...` 클릭 후 `typing` 입력.

---

### 5. **Typing 모듈 속성 직접 숨기기**
내부 변수를 숨기려면, Variables 창에서 다음 방법으로 직접 필터를 적용하세요:
1. 디버깅 중 **톱니바퀴 아이콘 → Customize Data View**.
2. `"Do not show variables matching pattern"`에서 다음과 같은 필터를 추가:
   ```
   typing.*
   ```
3. 적용 후, `typing` 모듈과 관련된 변수들이 자동으로 제외됩니다.

---

### 결과
이 설정을 적용하면 `typing.AbstractSet`, `typing.Any`, `typing.Callable` 등과 같은 내부 속성이 디버그 창에서 깔끔하게 숨겨질 겁니다!

---
