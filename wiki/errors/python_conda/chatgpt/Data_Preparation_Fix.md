---
type: Error Note
title: "Data Preparation Fix"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-05-14)"
tags: [errors, chatgpt-export]
timestamp: 2026-05-14
status: active
---

# Data Preparation Fix

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-14

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
Assessment: Enhancing Data Science Outcomes With Efficient Workflow
In this notebook, you will utilize what you've learned in this workshop to complete an assessment. The assessment has been divided into a couple of steps to guide your development. You will be graded based on the performance of your classification model. Note that this coding portion does not give partial credit - it shows up as either 0 or 60 points.Step 1: Data Preparation 
The first step is to prepare the data.

Instructions:
1.1 Modify the <FIXME> only and execute the below cell to import data from the given parquet files.
1.2 Execute the cell below to persist the data in memory and preview the dask_cudf.DataFrame.
1.3 Modify the <FIXME> only and execute the cell below to check for null values.

```
# 1.1
data_dir='data'
ddf=dask_cudf.read_parquet(data_dir)

print(f'Total of {len(ddf)} records split across {ddf.npartitions} partitions. ')

# 1.2
# DO NOT CHANGE THIS CELL
# persist data
ddf=ddf.persist()
wait(ddf)

print(f'Columns: {ddf.columns}')

ddf.head()

# 1.3
ddf.<<<<FIXIT>>>>
```

### 💡 답변 (Assistant)
1.3의 `<FIXIT>`에는 **null 값 개수를 확인하는 코드**를 넣으면 됩니다.

정답은 보통 이렇게 작성하면 됩니다.

```python
ddf.isnull().sum()
```

즉 전체 셀은:

```python
# 1.3
ddf.isnull().sum()
```

다만 Dask는 lazy execution이라 결과가 바로 계산되지 않을 수 있습니다. 실제 값을 확실히 보려면 보통은 아래처럼 `.compute()`까지 붙입니다.

```python
ddf.isnull().sum().compute()
```

그래서 assessment 환경에서 `<FIXIT>`만 수정 가능하고 결과를 바로 확인해야 한다면 가장 안전한 답은:

```python
isnull().sum().compute()
```

전체 코드:

```python
# 1.3
ddf.isnull().sum().compute()
```

의미는 다음과 같습니다.

```python
ddf.isnull()
```

각 셀이 null이면 `True`, 아니면 `False`로 바꿉니다.

```python
.sum()
```

컬럼별로 `True`의 개수를 셉니다. Python에서 `True`는 1, `False`는 0처럼 계산됩니다.

```python
.compute()
```

Dask 연산을 실제로 실행해서 결과를 가져옵니다.

정리하면, `<FIXIT>`에 넣을 값은:

```python
isnull().sum().compute()
```

---

### ❓ 질문 (User)
Step 2: Feature Engineering
Next, we will perform some feature engineering.

Instructions:
2.1 Modify the <FIXME>s only and execute the below cell to target_encode the brand feature.
2.2 Modify the <FIXME>s only and execute the cell below to create a relative_price_brand feature. In case a price is small or 0, please introduce an epsilon to avoid division by zero.
2.3 Execute the cell below to persist the data in memory.

이게 무슨말이지?

### 💡 답변 (Assistant)
좋아요. Step 2는 쉽게 말하면 **원본 데이터에 새로운 의미 있는 컬럼을 추가해서 모델 성능을 높이는 단계**입니다.

여기서는 크게 두 가지 feature를 만듭니다.

---

## Step 2 전체 의미

### 2.1 `brand` feature를 target encoding 하라

`brand`는 아마 상품 브랜드 컬럼일 가능성이 큽니다.

예를 들어 데이터가 이렇게 있다고 해볼게요.

| brand | target |
|---|---:|
| Nike | 1 |
| Nike | 0 |
| Apple | 1 |
| Apple | 1 |
| Samsung | 0 |

여기서 `target`이 분류 정답값이라고 하면, **브랜드별 target 평균값**을 계산해서 브랜드를 숫자로 바꾸는 것이 target encoding입니다.

예를 들면:

| brand | target 평균 |
|---|---:|
| Nike | 0.5 |
| Apple | 1.0 |
| Samsung | 0.0 |

그러면 원래 문자열이던 `brand`를 이런 숫자 feature로 바꿀 수 있습니다.

```python
brand_target_mean
```

같은 새 컬럼을 만드는 것입니다.

즉, **"이 브랜드는 과거 데이터에서 target=1일 확률이 어느 정도였는가?"** 를 feature로 만드는 작업입니다.

---

## 2.2 `relative_price_brand` feature를 만들라

이건 **해당 상품의 가격이 같은 브랜드 평균 가격 대비 얼마나 비싼지/싼지**를 나타내는 feature입니다.

예를 들어:

| brand | price |
|---|---:|
| Nike | 100 |
| Nike | 200 |
| Nike | 300 |

Nike의 평균 가격은:

```python
(100 + 200 + 300) / 3 = 200
```

각 상품의 상대 가격은:

```python
상품 가격 / 해당 브랜드 평균 가격
```

입니다.

| brand | price | brand 평균 price | relative_price_brand |
|---|---:|---:|---:|
| Nike | 100 | 200 | 0.5 |
| Nike | 200 | 200 | 1.0 |
| Nike | 300 | 200 | 1.5 |

해석하면:

```python
relative_price_brand = 0.5
```

브랜드 평균보다 싸다.

```python
relative_price_brand = 1.0
```

브랜드 평균과 비슷하다.

```python
relative_price_brand = 1.5
```

브랜드 평균보다 비싸다.

---

## epsilon을 넣으라는 말의 의미

문제에서 말한 부분:

> In case a price is small or 0, please introduce an epsilon to avoid division by zero.

이 말은 **0으로 나누는 오류를 방지하기 위해 아주 작은 값을 더하라**는 뜻입니다.

예를 들어 브랜드 평균 가격이 0이면:

```python
price / brand_mean_price
```

에서 분모가 0이 됩니다.

그러면 오류가 납니다.

그래서 보통 이렇게 합니다.

```python
epsilon = 1e-5
relative_price_brand = price / (brand_mean_price + epsilon)
```

`1e-5`는 `0.00001`이라는 아주 작은 값입니다.

---

## 2.3 persist 하라

Dask는 연산을 바로 실행하지 않고, 일단 계산 계획만 만들어 둡니다. 이것을 **lazy evaluation**이라고 합니다.

그래서 feature engineering을 한 뒤에는:

```python
ddf = ddf.persist()
wait(ddf)
```

처럼 데이터를 메모리에 올려서 이후 학습 단계에서 빠르게 쓰도록 합니다.

즉, 2.3은 **새로 만든 feature들이 포함된 데이터를 GPU 메모리/메모리에 유지하라**는 뜻입니다.

---

## 정리하면

Step 2에서 하라는 일은 이것입니다.

| 단계 | 해야 할 일 | 의미 |
|---|---|---|
| 2.1 | `brand` target encoding | 브랜드를 target 평균값 기반 숫자로 변환 |
| 2.2 | `relative_price_brand` 생성 | 상품 가격이 같은 브랜드 평균 대비 어느 정도인지 계산 |
| 2.3 | persist | 계산 결과를 메모리에 고정 |

핵심은 이겁니다.

```python
brand 문자열 자체를 모델에 넣기 어렵기 때문에 숫자로 바꾸고,
price도 단순 가격이 아니라 브랜드 기준 상대 가격으로 바꿔서
모델이 더 좋은 패턴을 학습하게 만드는 단계
```

예를 들어 문제 코드 셀을 보여주면 `<FIXME>`에 들어갈 값을 같이 맞춰드릴 수 있습니다.

---

### ❓ 질문 (User)
```
# 2.1
def target_encoding(df, cat): 
    te_df=df.groupby(cat)['target'].agg('count').reset_index()
    te_df.columns=[cat, cat+'_TE']
    df=df.merge(te_df, on=cat)
    return df

ddf=target_encoding(ddf, 'brand')
ddf.head()
```
그럼 여기에서 어떻게 바꿔?

### 💡 답변 (Assistant)
여기서 핵심은 이 부분이 잘못됐습니다.

```python
te_df=df.groupby(cat)['target'].agg('count').reset_index()
```

`count`는 **브랜드별 데이터 개수**를 세는 것입니다.  
하지만 **target encoding**은 보통 **브랜드별 target 평균값**을 넣는 방식입니다.

따라서 `count`를 `mean`으로 바꿔야 합니다.

```python
# 2.1
def target_encoding(df, cat): 
    te_df = df.groupby(cat)['target'].agg('mean').reset_index()
    te_df.columns = [cat, cat + '_TE']
    df = df.merge(te_df, on=cat)
    return df

ddf = target_encoding(ddf, 'brand')
ddf.head()
```

즉, 바꿀 부분은 딱 여기입니다.

```python
.agg('count')
```

을

```python
.agg('mean')
```

으로 변경합니다.

---

## 왜 `mean`인가?

예를 들어 데이터가 이렇게 있다고 해볼게요.

| brand | target |
|---|---:|
| Nike | 1 |
| Nike | 0 |
| Nike | 1 |
| Apple | 1 |
| Apple | 1 |

브랜드별 target 평균은:

| brand | brand_TE |
|---|---:|
| Nike | 0.6667 |
| Apple | 1.0000 |

이 값은 의미상:

```python
Nike 브랜드는 target=1일 가능성이 약 66.7%
Apple 브랜드는 target=1일 가능성이 100%
```

처럼 해석할 수 있습니다.

반면 `count`를 쓰면:

| brand | brand_TE |
|---|---:|
| Nike | 3 |
| Apple | 2 |

이건 단순히 **브랜드가 몇 번 등장했는지**입니다.  
이건 target encoding이 아니라 **frequency/count encoding**에 가깝습니다.

그래서 assessment에서 “target_encode the brand feature”라고 했다면 정답 방향은:

```python
agg('mean')
```

입니다.

---

### ❓ 질문 (User)
# 2.2
def relative_price(df, cat): 
    epsilon=1e-5
    avg_price_df=df.groupby(cat)['price'].agg().reset_index()
    avg_price_df.columns=[cat, 'avg_price_'+cat]
    df=df.merge(avg_price_df, on=cat)
    df['relative_price_'+cat]=df['price']/(df['avg_price_'+cat] + epsilon)
    df=df.drop(columns=['avg_price_'+cat])
    return df

ddf=relative_price(ddf, 'brand')
ddf.head()

그럼 이거는

### 💡 답변 (Assistant)
이 코드에서는 거의 다 맞게 작성했는데, **가장 중요한 부분 하나가 비어 있습니다.**

문제는 여기입니다.

```python
avg_price_df=df.groupby(cat)['price'].agg().reset_index()
```

`agg()` 안에 어떤 집계 함수를 쓸지 지정해야 합니다.  
`relative_price_brand`는 **브랜드별 평균 가격 대비 현재 상품 가격**을 의미하므로 `mean`을 넣어야 합니다.

정답 코드는 이렇게 됩니다.

```python
# 2.2
def relative_price(df, cat): 
    epsilon = 1e-5
    avg_price_df = df.groupby(cat)['price'].agg('mean').reset_index()
    avg_price_df.columns = [cat, 'avg_price_' + cat]
    df = df.merge(avg_price_df, on=cat)
    df['relative_price_' + cat] = df['price'] / (df['avg_price_' + cat] + epsilon)
    df = df.drop(columns=['avg_price_' + cat])
    return df

ddf = relative_price(ddf, 'brand')
ddf.head()
```

즉, `<FIXME>`에 들어갈 핵심은:

```python
'mean'
```

입니다.

---

왜 `mean`이냐면, 브랜드별 평균 가격을 구해야 하기 때문입니다.

예를 들어:

| brand | price |
|---|---:|
| A | 100 |
| A | 200 |
| A | 300 |

브랜드 A의 평균 가격은:

```python
(100 + 200 + 300) / 3 = 200
```

그러면 각 행의 `relative_price_brand`는:

```python
price / 브랜드 평균 price
```

입니다.

| price | avg_price_brand | relative_price_brand |
|---:|---:|---:|
| 100 | 200 | 0.5 |
| 200 | 200 | 1.0 |
| 300 | 200 | 1.5 |

해석하면:

```python
relative_price_brand < 1
```

브랜드 평균보다 싸다.

```python
relative_price_brand == 1
```

브랜드 평균과 비슷하다.

```python
relative_price_brand > 1
```

브랜드 평균보다 비싸다.

따라서 이 문제에서는 `agg()`를 아래처럼 고치면 됩니다.

```python
.agg('mean')
```

---

### 💡 답변 (Assistant)
이 코드에서는 여기만 고치면 됩니다.

```python
avg_price_df=df.groupby(cat)['price'].agg().reset_index()
```

`agg()` 안이 비어 있어서 **무엇을 집계할지 지정되지 않은 상태**입니다.  
`relative_price_brand`는 **브랜드별 평균 가격 대비 현재 가격의 비율**이므로 `mean`을 넣어야 합니다.

정답 형태는 아래입니다.

```python
# 2.2
def relative_price(df, cat): 
    epsilon = 1e-5
    avg_price_df = df.groupby(cat)['price'].agg('mean').reset_index()
    avg_price_df.columns = [cat, 'avg_price_' + cat]
    df = df.merge(avg_price_df, on=cat)
    df['relative_price_' + cat] = df['price'] / (df['avg_price_' + cat] + epsilon)
    df = df.drop(columns=['avg_price_' + cat])
    return df

ddf = relative_price(ddf, 'brand')
ddf.head()
```

즉 `<FIXME>` 또는 고쳐야 할 핵심은:

```python
.agg('mean')
```

입니다.

의미는 이겁니다.

```python
avg_price_df = df.groupby('brand')['price'].agg('mean').reset_index()
```

브랜드별 평균 가격을 계산합니다.

예를 들어:

| brand | price |
|---|---:|
| A | 100 |
| A | 200 |
| B | 50 |

이면 브랜드별 평균 가격은:

| brand | avg_price_brand |
|---|---:|
| A | 150 |
| B | 50 |

그다음:

```python
df['relative_price_brand'] = df['price'] / (df['avg_price_brand'] + epsilon)
```

현재 상품 가격을 같은 브랜드의 평균 가격으로 나눕니다.

예를 들어 A 브랜드 상품 가격이 100이면:

```python
100 / 150 = 0.6667
```

A 브랜드 평균보다 싼 상품입니다.

A 브랜드 상품 가격이 200이면:

```python
200 / 150 = 1.3333
```

A 브랜드 평균보다 비싼 상품입니다.

따라서 이 문제에서 바꿀 부분은 거의 확실히:

```python
agg()
```

를

```python
agg('mean')
```

으로 바꾸는 것입니다.

---
