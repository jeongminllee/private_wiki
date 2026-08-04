---
type: Error Note
title: "UFuncTypeError 해결법"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-04-16)"
tags: [errors, chatgpt-export]
timestamp: 2026-04-16
status: active
---

# UFuncTypeError 해결법

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-04-16

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
이 에러는 꽤 핵심적인 문제를 정확히 짚고 있어요.  
한 줄로 요약하면:

> **문자열(dtype `<U1`)끼리 `-` 연산을 하려고 해서 발생한 오류**입니다.

---

## 🔍 에러 메시지 해석

```
UFuncTypeError: ufunc 'subtract' did not contain a loop with signature matching types (dtype('<U1'), dtype('<U1')) -> None
```

이걸 분해해보면:

- `ufunc 'subtract'`  
  → NumPy 내부의 **벡터화된 뺄셈 연산**

- `dtype('<U1')`  
  → **길이 1짜리 유니코드 문자열**
  - 예: `'1'`, `'a'`, `'5'`

- `did not contain a loop with signature matching`  
  → 해당 타입(문자열)에 대해 **뺄셈 연산 정의가 없다**

👉 즉,

```
"1" - "2"  ❌ (문자열)
1 - 2      ✅ (숫자)
```

---

## 💥 언제 이런 에러가 발생하냐?

대표적인 케이스:

### 1. CSV / 데이터셋 읽었는데 숫자가 문자열로 들어온 경우

```python
import numpy as np

a = np.array(['1', '2', '3'])
b = np.array(['4', '5', '6'])

a - b   # ❌ 에러 발생
```

---

### 2. pandas에서 object → numpy 변환 시

```python
df['col1'] - df['col2']   # 둘 다 문자열이면 에러
```

---

## ✅ 해결 방법

핵심은 **숫자로 캐스팅 (type conversion)** 입니다.

---

### ✔️ 방법 1: numpy에서 변환

```python
a = a.astype(int)
b = b.astype(int)

a - b   # 정상 동작
```

또는 float:

```python
a = a.astype(float)
```

---

### ✔️ 방법 2: pandas에서 변환

```python
df['col1'] = df['col1'].astype(int)
df['col2'] = df['col2'].astype(int)
```

또는 안전하게:

```python
df['col1'] = pd.to_numeric(df['col1'], errors='coerce')
```

👉 `errors='coerce'` → 변환 불가 값은 NaN 처리

---

## ⚠️ 실무에서 자주 걸리는 함정

너 지금까지 했던 작업 흐름 보면 (Parquet, dtype 문제 등):

👉 거의 100% 이 상황일 가능성 높음

- CSV → pandas 읽을 때
- object dtype 그대로 유지됨
- numpy 연산 들어가면서 폭발

---

## 🔧 디버깅 팁 (중요)

이거 바로 확인하면 원인 확정됨:

```python
print(a.dtype)
print(type(a[0]))
```

또는 pandas:

```python
df.info()
```

👉 `object` or `<U1` 나오면 바로 의심

---

## 🧠 한 단계 더 (왜 `<U1`인가?)

- `<U1` = Unicode string length 1
- `<U10` = 문자열 길이 최대 10

👉 즉, numpy가 **숫자가 아니라 문자열 배열로 인식**한 것

---

## 🚀 정리

- 원인: 문자열 배열에 대해 수치 연산 시도
- 해결: `astype(int)` 또는 `pd.to_numeric`
- 핵심: **dtype 확인이 먼저다**

---

원하면  
👉 "왜 pandas는 숫자를 문자열로 읽는지"  
👉 "Parquet 변환에서 dtype 깨지는 구조"  

이거까지 연결해서 설명해줄게.  
지금 너 상황 보면 이거 한 번 정리해두면 꽤 큰 레벨업 포인트야.

---

### ❓ 질문 (User)
UFuncTypeError: ufunc 'subtract' did not contain a loop with signature matching types (dtype('<U1'), dtype('<U1')) -> None

### ❓ 질문 (User)
A1	A2	A3	A4	A5	A6	A7	A8	A9	A10	A11	A12	A13	A14	A15
0	1	65.0	168	2	4	4	39	0	0	1	1	2	32	161	0
1	0	72.0	123	2	8	4	5	0	0	1	0	2	53	1	0
2	0	142.0	52	1	4	4	31	0	0	1	1	2	98	1	0
3	0	60.0	169	1	5	3	1	1	1	12	1	2	1	1	1
4	1	44.0	134	2	6	4	46	1	1	15	0	2	18	68	1


A1     category
A2      float64
A3        uint8
A4     category
A5     category
A6     category
A7        uint8
A8     category
A9     category
A10       uint8
A11    category
A12    category
A13       uint8
A14       uint8
A15       int64
이게 데이터.head()와 dtypes() 결과야. 어떻게 수정할지 알려줘.

### 💡 답변 (Assistant)
좋아요. 지금 보여준 `head()`와 `dtypes()`를 보면, **에러의 직접 원인을 거의 특정할 수 있습니다.**

핵심은 이거예요:

- `UFuncTypeError: subtract ... dtype('<U1')`
- 즉, **어딘가에서 문자열 1글자짜리 값끼리 뺄셈이 일어났다**
- 그런데 현재 `dtypes()`에는 문자열 타입이 직접 보이지 않음
- 그래서 실제 문제는 보통 둘 중 하나입니다.

## 먼저 눈에 띄는 이상점

당신이 올린 `head()`는 이런 식이죠:

```python
0	1	65.0	168	2	4	4	39	0	0	1	1	2	32	161	0
1	0	72.0	123	2	8	4	5	0	0	1	0	2	53	1	0
...
```

열 이름은 `A1 ~ A15`인데, `dtypes()`는

```python
A1     category
A2      float64
A3        uint8
A4     category
...
A15       int64
```

입니다.

그런데 `head()` 첫 행을 보면:

- `A1 = 1`
- `A2 = 65.0`
- `A3 = 168`

처럼 보이는데, `dtypes()`에서는
- `A1 = category`
- `A2 = float64`
- `A3 = uint8`

이라서, **열 의미가 직관적으로 잘 안 맞습니다.**

즉 지금 해야 할 건 단순히 “뺄셈 에러 해결”이 아니라, 먼저 **각 열이 진짜 숫자인지 / category인지 / 문자열이 숨어 있는지 점검**하는 겁니다.

---

## 가장 가능성 높은 원인

### 1. `category` 열에 대해 수치 연산을 했다
`category`는 겉으로 숫자처럼 보여도 내부적으로는 범주형입니다.

예를 들어:

```python
df["A1"] - df["A4"]
```

이런 연산을 하면 문제가 날 수 있어요.

특히 범주형이 문자열 카테고리로 들어가 있으면 내부적으로 NumPy가 문자열처럼 처리하다가 `subtract`에서 터질 수 있습니다.

---

### 2. train/test 중 한쪽이 문자열로 읽혔다
예를 들어 `X_train`은 숫자인데 `X_test`는 문자열이면:

```python
X_train - X_test
```

같은 연산에서 이 에러가 납니다.

또는 sklearn 내부에서 거리 계산, 평균 계산, 정규화 등을 하다가도 납니다.

---

### 3. category를 `.values` 또는 `numpy.array()`로 넘기는 과정에서 문자열 배열이 됐다
예:

```python
np.array(df["A1"])
```

이게 기대와 다르게 문자열 배열이 될 수 있습니다.

---

# 어떻게 수정할까

지금은 **연산에 사용할 열은 전부 숫자형으로 통일**하는 게 가장 안전합니다.

## 방법 1: category 열을 숫자 코드로 바꾸기

현재 `category`인 열들:

- A1
- A4
- A5
- A6
- A8
- A9
- A11
- A12

이 열들이 실제로 범주형 변수라면, 모델에 넣기 전에 숫자로 바꿔야 합니다.

```python
cat_cols = df.select_dtypes(include=["category"]).columns

for col in cat_cols:
    df[col] = df[col].cat.codes
```

이렇게 하면 category가 정수 코드로 바뀝니다.

예를 들어:
- category 값이 `['low', 'mid', 'high']`였다면
- `0, 1, 2` 같은 숫자로 바뀝니다.

---

## 방법 2: 전체를 숫자형으로 강제 변환

연산 전에 한 번 더 안전하게:

```python
df = df.apply(pd.to_numeric, errors="raise")
```

이렇게 하면 숫자로 바꿀 수 없는 값이 있으면 바로 에러가 나서 어느 열이 문제인지 찾기 쉽습니다.

조금 더 안전하게 보려면:

```python
for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except Exception as e:
        print(f"{col} 변환 실패: {e}")
```

이렇게 하면 문제 열을 바로 찾을 수 있습니다.

---

## 방법 3: category를 원-핫 인코딩하기
모델 종류에 따라 category를 코드값으로 두기보다 원-핫 인코딩이 더 적절할 수 있습니다.

```python
df_encoded = pd.get_dummies(df, drop_first=False)
```

이렇게 하면 전부 숫자형 열로 바뀝니다.

다만 지금 에러 해결이 우선이면, 먼저 `cat.codes`가 더 빠릅니다.

---

# 지금 바로 점검해야 할 코드

이걸 먼저 실행해보세요.

```python
print(df.dtypes)
print()
print(df.select_dtypes(include=["object"]).columns)
print(df.select_dtypes(include=["category"]).columns)
```

그리고 각 열 내부 값 타입도 확인:

```python
for col in df.columns:
    print(col, df[col].dtype, df[col].iloc[0], type(df[col].iloc[0]))
```

이걸 보면
- category지만 값은 int처럼 보이는지
- 실제로 문자열이 섞였는지
- object 열이 숨어 있는지

바로 확인됩니다.

---

# 추천 수정 코드

가장 실전적인 방식으로 정리하면 이렇습니다.

```python
import pandas as pd
import numpy as np

# 1. category 열 찾기
cat_cols = df.select_dtypes(include=["category"]).columns

# 2. category -> 숫자 코드
for col in cat_cols:
    df[col] = df[col].cat.codes

# 3. 전체 숫자형 확인
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="raise")

# 4. 최종 dtype 확인
print(df.dtypes)
```

이후 모델 입력 전에는:

```python
X = df.drop(columns=["A15"])   # 예: A15가 타깃이면
y = df["A15"]

print(X.dtypes)
print(y.dtypes)
```

---

# 왜 이 수정이 필요한가

지금 `head()`만 보면 값들이 숫자처럼 보여서 헷갈리는데,  
`dtype`이 `category`면 **숫자처럼 보여도 수치 연산용 숫자라고 보장되지 않습니다.**

즉:

- 눈으로는 `1`, `2`, `4`처럼 보임
- 하지만 내부적으로는 범주형
- NumPy/sklearn 연산에서 문자열/카테고리로 흘러가면
- `subtract` 에러 발생

이 구조예요.

---

# 특히 sklearn/거리계산에서 자주 터지는 경우

이런 코드에서 자주 납니다:

```python
pairwise_distances(X)
scaler.fit_transform(X)
X_train - X_test
```

왜냐하면 내부적으로 전부 숫자 배열이어야 하는데, category/object/string이 섞이면 바로 터집니다.

그래서 모델 넣기 전 최종 확인은 꼭 하세요:

```python
print(X.dtypes)
print(X.to_numpy().dtype)
```

`X.to_numpy().dtype`가 `object`로 나오면 아직 정리가 안 된 겁니다.  
가능하면 `int64`, `float64` 같은 숫자 dtype이어야 합니다.

---

# 당신 데이터 기준으로 바로 권장하는 방향

지금 상태에서는 우선 이렇게 가는 게 좋습니다.

```python
cat_cols = ["A1", "A4", "A5", "A6", "A8", "A9", "A11", "A12"]

for col in cat_cols:
    df[col] = df[col].cat.codes

df = df.apply(pd.to_numeric, errors="raise")
```

그 다음 연산하세요.

---

# 추가로 확인할 것

만약 이걸 했는데도 같은 에러가 나면, 문제는 `df` 자체가 아니라 **연산 직전에 만든 다른 변수**일 가능성이 큽니다.

예를 들어:

- `X_train`
- `X_test`
- `dataset`
- `dataset[0].reshape(...)`
- `np.array(...)`로 따로 만든 배열

이 변수들 dtype도 봐야 합니다.

```python
print(X_train.dtype if hasattr(X_train, "dtype") else X_train.dtypes)
print(X_test.dtype if hasattr(X_test, "dtype") else X_test.dtypes)
```

---

원하시면 다음 메시지에서  
당신이 실제로 연산하는 코드까지 붙여주면, **어느 줄에서 무엇을 어떻게 바꿔야 하는지** 바로 짚어서 수정해드릴게요.

---

### 💡 답변 (Assistant)
좋은 판단이에요. 방향 자체는 맞습니다.  
다만 **“그냥 다 uint8로 바꾸자”는 건 약간 위험**해서, 데이터 범위를 보고 **정확하게 최적 dtype을 선택**하는 게 핵심입니다.

---

# 🔍 현재 데이터 기준 분석

당신이 준 샘플을 보면:

```
A2 → float (예: 65.0, 72.0, 142.0)
나머지 → 정수처럼 보임
```

하지만 여기서 중요한 건:

👉 **정수의 범위 (min/max)**

예를 들어:

- `uint8` → 0 ~ 255
- `int8` → -128 ~ 127
- `uint16` → 0 ~ 65535

---

## ⚠️ 실제 값 확인 (중요)

샘플에서 이미 힌트 있음:

```
A3 = 168
A14 = 161
```

👉 이건 `uint8` 범위 (0~255) 안에 있음 → OK

하지만 문제는 **전체 데이터**입니다.  
샘플만 보고 결정하면 안 됩니다.

---

# ✅ 안전한 dtype 전략 (추천)

## 1️⃣ 먼저 범위 확인

이거 반드시 먼저 하세요:

```python
df.describe()
```

또는 더 정확하게:

```python
for col in df.columns:
    print(col, df[col].min(), df[col].max())
```

---

## 2️⃣ dtype 선택 기준

### ✔️ A2 (float)

```python
df["A2"] = df["A2"].astype("float32")
```

- float64 → float32로 줄이면 메모리 절약
- 대부분 ML에서는 float32면 충분

---

### ✔️ 나머지 정수형

#### 경우 1: 값이 0~255

```python
df[col] = df[col].astype("uint8")
```

#### 경우 2: 값이 255 초과

```python
df[col] = df[col].astype("uint16")
```

#### 경우 3: 음수 포함

```python
df[col] = df[col].astype("int16")
```

---

# 🚀 자동으로 처리하는 코드 (추천)

이건 실전에서 많이 쓰는 패턴입니다:

```python
for col in df.columns:
    if col == "A2":
        df[col] = df[col].astype("float32")
    else:
        min_val = df[col].min()
        max_val = df[col].max()

        if min_val >= 0:
            if max_val <= 255:
                df[col] = df[col].astype("uint8")
            elif max_val <= 65535:
                df[col] = df[col].astype("uint16")
            else:
                df[col] = df[col].astype("uint32")
        else:
            if min_val >= -128 and max_val <= 127:
                df[col] = df[col].astype("int8")
            elif min_val >= -32768 and max_val <= 32767:
                df[col] = df[col].astype("int16")
            else:
                df[col] = df[col].astype("int32")
```

---

# ⚠️ 중요한 포인트 2가지

## 1. category 먼저 처리해야 함

지금 dtype 보면:

```
A1, A4, A5 ... → category
```

👉 이 상태에서 `.astype(uint8)` 하면 안 됩니다.

먼저:

```python
cat_cols = df.select_dtypes(include=["category"]).columns
for col in cat_cols:
    df[col] = df[col].cat.codes
```

그 다음 dtype 변환

---

## 2. ML/NumPy 호환성

👉 사실 대부분의 ML 라이브러리는 내부에서 float64로 다시 바꿈

그래서:

- 메모리 최적화 목적 → uint8, float32 좋음
- 연산 안정성 → float32/float64 통일이 더 안전

👉 그래서 실무에서는 이런 선택도 많이 합니다:

```python
df = df.astype("float32")
```

(단순하고 안전)

---

# 🎯 결론 (당신 상황 기준 최적 전략)

### ✔️ 가장 안전한 방식

```python
# 1. category → 숫자
for col in df.select_dtypes(include=["category"]).columns:
    df[col] = df[col].cat.codes

# 2. 타입 변환
df["A2"] = df["A2"].astype("float32")

for col in df.columns:
    if col != "A2":
        df[col] = df[col].astype("uint8")  # 범위 확인 후!
```

---

### ✔️ 더 안정적인 ML용 방식

```python
df = df.astype("float32")
```

👉 이건 dtype 문제 100% 방지

---

# 🔥 핵심 요약

- 방향은 맞음 (float32 + uint8)
- 하지만 반드시 **값 범위 확인 후 적용**
- category는 먼저 `.cat.codes`
- ML 안정성까지 고려하면 `float32 통일`도 좋은 선택

---

원하면 다음 단계로  
👉 “메모리 최적화 vs 모델 성능 trade-off”  
👉 “왜 CatBoost/XGBoost에서 dtype이 중요해지는지”  

이거까지 이어서 설명해줄게.

---

### ❓ 질문 (User)
데이터를 보니까 A2는 float, 나머지는 전부 int 로 바꾸면 될 거 같은데 float32, uint8 로 바꾸면 되지 않을까?

### 💡 답변 (Assistant)
좋습니다. `pd.set_option`은 **pandas의 출력 방식과 동작을 제어하는 전역 설정 API**입니다.  
데이터 분석할 때 “왜 출력이 잘려 보이지?” 같은 문제를 해결하는 핵심 도구라서 반드시 익혀두는 게 좋아요.

---

# 🔧 `pd.set_option` 개념

```python
pd.set_option("옵션명", 값)
```

👉 pandas의 내부 설정 값을 바꿔서  
- 출력 형태
- 표시 개수
- 포맷
- 동작 방식

을 제어합니다.

---

# 📌 가장 많이 쓰는 옵션 (실전 핵심)

## 1️⃣ 컬럼 전부 보기

```python
pd.set_option("display.max_columns", None)
```

👉 열이 많을 때 잘리는 문제 해결

---

## 2️⃣ 행 전부 보기

```python
pd.set_option("display.max_rows", None)
```

👉 전체 데이터 확인할 때 (단, 데이터 크면 위험 ⚠️)

---

## 3️⃣ 출력 너비 제한 해제

```python
pd.set_option("display.width", None)
```

👉 줄바꿈 없이 한 줄로 출력

---

## 4️⃣ 컬럼 내용 길이 제한 해제

```python
pd.set_option("display.max_colwidth", None)
```

👉 긴 문자열 (텍스트 데이터) 잘림 방지

---

## 5️⃣ float 출력 형식 지정

```python
pd.set_option("display.float_format", "{:.2f}".format)
```

👉 소수점 자리 제한

예:
```python
3.141592 → 3.14
```

---

## 6️⃣ scientific notation 끄기

```python
pd.set_option("display.float_format", "{:.6f}".format)
```

👉 `1.23e+08` → `123000000.000000`

---

# 🔍 옵션 확인 / 초기화

## 현재 설정 확인

```python
pd.get_option("display.max_rows")
```

---

## 전체 옵션 보기

```python
pd.describe_option()
```

---

## 특정 옵션 검색

```python
pd.describe_option("max_rows")
```

---

## 옵션 초기화

```python
pd.reset_option("display.max_rows")
```

👉 기본값으로 복구

---

## 모든 옵션 초기화

```python
pd.reset_option("^display")
```

👉 display 관련 옵션 전부 리셋

---

# 🚀 실전 추천 세팅 (강력)

데이터 분석 시작할 때 거의 기본으로 쓰는 세팅입니다:

```python
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.float_format", "{:.4f}".format)
```

👉 이거 한 번 설정하면 디버깅 생산성 확 올라갑니다.

---

# ⚠️ 주의할 점

## 1. 전역(global) 적용

```python
pd.set_option(...)
```

👉 이후 모든 pandas 출력에 영향을 줌

---

## 2. 너무 큰 데이터 출력 위험

```python
pd.set_option("display.max_rows", None)
```

👉 수십만 행이면 Jupyter 터질 수 있음

---

# 🎯 `UFuncTypeError` 디버깅과 연결

지금 당신 상황에서는 이 옵션이 매우 유용합니다.

특히:

```python
pd.set_option("display.max_columns", None)
```

👉 숨겨진 열까지 전부 확인 가능

그리고:

```python
df.head()
df.dtypes
```

👉 dtype 문제 (category / object) 바로 발견 가능

---

# 💡 고급 팁 (컨텍스트 옵션)

일시적으로만 옵션 적용:

```python
with pd.option_context("display.max_rows", 10):
    print(df)
```

👉 블록 안에서만 적용됨 (깔끔한 방식)

---

# 🔥 한 줄 요약

- `pd.set_option` = pandas 출력/동작 제어 도구
- 디버깅, 데이터 확인, 시각화 가독성에 필수
- 특히 **dtype 문제 추적할 때 매우 중요**

---

원하면  
👉 “pandas display 옵션 전체 구조 (display / mode / io)”  
👉 “대용량 데이터에서 안전하게 출력하는 방법”  

이것도 이어서 정리해줄게.

---

### ❓ 질문 (User)
pd.set_option에 대해서 알려줘
