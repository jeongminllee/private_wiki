---
type: Error Note
title: "SVC Parameter Optimization."
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2023-06-28)"
tags: [errors, chatgpt-export]
timestamp: 2023-06-28
status: active
---

# SVC Parameter Optimization.

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-06-28

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from scipy.stats import loguniform

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

# 데이터 로드
digits = load_digits()

# 독립 변수, 종속 변수 데이터
x = digits.data
y = digits.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


params = {
    "C" : loguniform(1e-4, 100),
    "kernel" : ["linear", "poly", "rbf", "sigmoid"],
    "gamma" : ["scale", "auto"] + list(loguniform(1e-4, 10).rvs(10)),
    "degree" : range(1,6),
    "coef0" : loguniform(1e-4, 10).rvs(10)
}

svm_model = SVC()

random_search = RandomizedSearchCV(svm_model, params, n_iter=100, cv=5, verbose=2, n_jobs=-1)

random_search.fit(x_train, y_train)

print(random_search.best_params_)

# 최적 모델 저장
best_model = random_search.best_estimator_

# 테스트 데이터에 대한 예측 수행
y_pred = best_model.predict(x_test)

print("ACC >> ", accuracy_score(y_test, y_pred))

UnicodeEncodeError: 'ascii' codec can't encode characters in position 18-20: ordinal not in range(128)

### 💡 답변 (Assistant)
The error you encountered, `UnicodeEncodeError: 'ascii' codec can't encode characters in position 18-20: ordinal not in range(128)`, suggests that there is an issue with encoding some characters in your code. This error typically occurs when there are non-ASCII characters present in your code or in the data you're working with.

To resolve this issue, you can try the following steps:

1. Check for non-ASCII characters: Look for any non-ASCII characters in your code, comments, or variable names. Replace them with ASCII equivalents or remove them if they are not necessary.

2. Encoding declaration: Add the following encoding declaration at the top of your Python script, before any non-ASCII characters are used:

```python
# -*- coding: utf-8 -*-
```

This declaration ensures that the Python interpreter understands the encoding used in your script.

3. Data encoding: If your data contains non-ASCII characters, make sure the data is encoded properly. You can use the `encode()` or `decode()` methods to handle encoding and decoding as needed.

Make sure to apply these steps to all relevant files and code snippets, including the code you provided and any additional code files you may be using.

Here's an updated version of your code with the encoding declaration added:

```python
# -*- coding: utf-8 -*-

from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from scipy.stats import loguniform

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

# 데이터 로드
digits = load_digits()

# 독립 변수, 종속 변수 데이터
x = digits.data
y = digits.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


params = {
    "C" : loguniform(1e-4, 100),
    "kernel" : ["linear", "poly", "rbf", "sigmoid"],
    "gamma" : ["scale", "auto"] + list(loguniform(1e-4, 10).rvs(10)),
    "degree" : range(1,6),
    "coef0" : loguniform(1e-4, 10).rvs(10)
}

svm_model = SVC()

random_search = RandomizedSearchCV(svm_model, params, n_iter=100, cv=5, verbose=2, n_jobs=-1)

random_search.fit(x_train, y_train)

print(random_search.best_params_)

# 최적 모델 저장
best_model = random_search.best_estimator_

# 테스트 데이터에 대한 예측 수행
y_pred = best_model.predict(x_test)

print("ACC >> ", accuracy_score(y_test, y_pred))
```

Make sure to save your code file with the appropriate encoding to avoid any issues.

---

### ❓ 질문 (User)
plz, write Korean?

### 💡 답변 (Assistant)
아래는 인코딩 선언을 추가한 한국어로 된 코드입니다.

```python
# -*- coding: utf-8 -*-

from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from scipy.stats import loguniform

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

# 데이터 로드
digits = load_digits()

# 독립 변수, 종속 변수 데이터
x = digits.data
y = digits.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


params = {
    "C" : loguniform(1e-4, 100),
    "kernel" : ["linear", "poly", "rbf", "sigmoid"],
    "gamma" : ["scale", "auto"] + list(loguniform(1e-4, 10).rvs(10)),
    "degree" : range(1,6),
    "coef0" : loguniform(1e-4, 10).rvs(10)
}

svm_model = SVC()

random_search = RandomizedSearchCV(svm_model, params, n_iter=100, cv=5, verbose=2, n_jobs=-1)

random_search.fit(x_train, y_train)

print(random_search.best_params_)

# 최적 모델 저장
best_model = random_search.best_estimator_

# 테스트 데이터에 대한 예측 수행
y_pred = best_model.predict(x_test)

print("정확도 >> ", accuracy_score(y_test, y_pred))
```

이 코드는 한국어 주석과 출력문을 포함하고 있습니다. 주의해야 할 점은 코드 파일을 적절한 인코딩으로 저장하여 문제가 없도록 해야 합니다.

---

### ❓ 질문 (User)
코드 말고 chat 이 말한 The error 부터 Korean 으로 해줘

### 💡 답변 (Assistant)
발생한 오류인 `UnicodeEncodeError: 'ascii' codec can't encode characters in position 18-20: ordinal not in range(128)`는 코드의 일부나 사용 중인 데이터에 ASCII 이외의 문자가 포함되어 있는 경우 발생하는 오류입니다.

이 문제를 해결하기 위해 다음과 같은 단계를 시도해볼 수 있습니다:

1. ASCII 이외의 문자 확인: 코드, 주석 또는 변수 이름에서 ASCII 이외의 문자가 있는지 확인합니다. ASCII와 동등한 문자로 대체하거나 필요하지 않은 경우 삭제합니다.

2. 인코딩 선언: Python 스크립트의 맨 위에 다음 인코딩 선언을 추가합니다. 단, ASCII 이외의 문자를 사용하기 전에 선언되어야 합니다.

```python
# -*- coding: utf-8 -*-
```

이 선언은 Python 인터프리터가 스크립트에서 사용된 인코딩을 올바르게 이해할 수 있도록 합니다.

3. 데이터 인코딩: 데이터에 ASCII 이외의 문자가 포함되어 있는 경우, 데이터를 올바르게 인코딩해야 합니다. 인코딩 및 디코딩에 필요한 `encode()` 또는 `decode()` 메서드를 사용합니다.

해당 단계를 코드 및 모든 관련 파일에 적용하십시오. 아래에는 인코딩 선언이 추가된 코드의 한국어 버전을 제공합니다:

```python
# -*- coding: utf-8 -*-

from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from scipy.stats import loguniform

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

# 데이터 로드
digits = load_digits()

# 독립 변수, 종속 변수 데이터
x = digits.data
y = digits.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


params = {
    "C" : loguniform(1e-4, 100),
    "kernel" : ["linear", "poly", "rbf", "sigmoid"],
    "gamma" : ["scale", "auto"] + list(loguniform(1e-4, 10).rvs(10)),
    "degree" : range(1,6),
    "coef0" : loguniform(1e-4, 10).rvs(10)
}

svm_model = SVC()

random_search = RandomizedSearchCV(svm_model, params, n_iter=100, cv=5, verbose=2, n_jobs=-1)

random_search.fit(x_train, y_train)

print(random_search.best_params_)

# 최적 모델 저장
best_model = random_search.best_estimator_

# 테스트 데이터에 대한 예측 수행
y_pred = best_model.predict(x_test)

print("정확도 >> ", accuracy_score(y_test, y_pred))
```

관련 파일 및 코드 조각에 적절한 인코딩이 적용되

---
