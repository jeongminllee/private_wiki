---
type: Concept
title: "CSV에서 Parquet 변환 분석"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-02-02)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-02-02
status: active
---

# CSV에서 Parquet 변환 분석

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-02-02

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
나는 지금 캐글에서 csv 파일을 가지고 데이터 분석을 하려고 해. 
csv파일을 parquet 파일로 저장한 후 parquet 파일을 중심으로 데이터 분석을 해보려고 하는데, 사용법과 주의할 점에 대해서 알려줘. 그리고 어떤 장단점이 있는지도 알려줘.

### 💡 답변 (Assistant)
좋은 접근입니다. **Kaggle 환경 + CSV → Parquet 전환 → Parquet 중심 분석**은 실무 데이터 파이프라인과도 잘 맞고, 성능 체감도 분명합니다. 아래를 **실제 Kaggle 노트북 기준**으로 정리하겠습니다.

---

## 1. 왜 CSV → Parquet로 바꾸는가 (전제 정리)

### CSV의 본질적 한계
- **행 기반(row-based)** 텍스트 포맷
- 스키마 없음 (타입 추론 매번 필요)
- 압축 효율 낮음
- 필요한 컬럼만 읽기 어려움 (항상 전체 스캔)

### Parquet의 본질
- **열 기반(columnar) 바이너리 포맷**
- 스키마 포함 (dtype 고정)
- 강력한 압축 (Snappy, Gzip 등)
- **Column pruning / Predicate pushdown** 가능

👉 분석 반복이 많을수록 Parquet가 압도적으로 유리

---

## 2. Kaggle에서 기본 사용법 (실전 코드)

### 2.1 CSV → Parquet 변환

```python
import pandas as pd

df = pd.read_csv("/kaggle/input/your-dataset/data.csv")

df.to_parquet(
    "/kaggle/working/data.parquet",
    engine="pyarrow",
    compression="snappy"
)
```

✔ Kaggle에는 **pyarrow 기본 설치**되어 있음  
✔ `snappy`는 속도/압축 균형이 가장 좋음

---

### 2.2 Parquet 로드

```python
df = pd.read_parquet(
    "/kaggle/working/data.parquet",
    engine="pyarrow"
)
```

### 특정 컬럼만 읽기 (중요!)

```python
df = pd.read_parquet(
    "/kaggle/working/data.parquet",
    columns=["user_id", "price", "timestamp"]
)
```

➡ **대용량 데이터에서 속도 차이가 극적**

---

## 3. Parquet 중심 분석 시 권장 패턴

### 3.1 1회만 CSV → Parquet
```text
[Raw CSV]
   ↓ (1회)
[Parquet]
   ↓
[EDA / Feature Engineering / Modeling]
```

- CSV를 매번 읽지 말 것
- Parquet를 **단일 신뢰 소스(single source of truth)** 로 사용

---

### 3.2 dtype 명시 후 저장 (중요)

CSV → Parquet 시 자동 dtype에 의존하면 문제 생김

```python
df = pd.read_csv(
    "/kaggle/input/data.csv",
    dtype={
        "user_id": "int32",
        "price": "float32",
        "category": "category"
    }
)

df.to_parquet("/kaggle/working/data.parquet")
```

✔ Parquet는 dtype을 그대로 저장 → 이후 분석 일관성 확보

---

### 3.3 Chunk 처리 → Parquet 병합 (대용량일 때)

```python
chunks = pd.read_csv("data.csv", chunksize=1_000_000)

for i, chunk in enumerate(chunks):
    chunk.to_parquet(
        f"/kaggle/working/part_{i}.parquet"
    )
```

➡ 이후 pyarrow / dask / polars에서 병렬 처리 가능

---

## 4. Kaggle에서 특히 주의할 점 ⚠️

### 4.1 `/kaggle/working` 용량 제한
- 약 **20GB**
- Parquet는 작아지지만, 중간 산출물 주의

➡ 중간 결과는 필요 없으면 삭제
```python
import os
os.remove("temp.parquet")
```

---

### 4.2 Parquet은 사람이 읽을 수 없음
- 디버깅 불편
- CSV처럼 바로 열어 확인 불가

➡ **EDA 초반엔 CSV + 후반 Parquet**이 현실적

---

### 4.3 Pandas만 쓰면 Parquet 장점의 50%만 사용
- 진짜 장점은:
  - column pruning
  - filter pushdown
  - 병렬 읽기

➡ 가능하면 아래 고려
- `pyarrow.dataset`
- `polars`
- `dask`

---

## 5. 장단점 정리 (실무 기준)

### ✅ 장점

| 항목 | 설명 |
|----|----|
| 속도 | 대용량에서 3~10배 빠름 |
| 저장 공간 | CSV 대비 30~70% 감소 |
| 타입 안정성 | dtype 유지 |
| 부분 로드 | 필요한 컬럼만 읽기 |
| 확장성 | Spark, Dask, Polars 호환 |

---

### ❌ 단점

| 항목 | 설명 |
|----|----|
| 가독성 | 텍스트가 아님 |
| 스키마 변경 | 컬럼 추가/삭제가 번거로움 |
| 소규모 데이터 | 체감 효과 적음 |
| Pandas 한계 | 완전한 columnar 이점 활용 어려움 |

---

## 6. Kaggle 데이터 분석 추천 스택 (현실적)

| 단계 | 도구 |
|----|----|
| CSV → Parquet | pandas + pyarrow |
| EDA | pandas |
| 대용량 EDA | polars |
| Feature Eng | pandas / polars |
| Modeling | sklearn / xgboost |
| 재현성 | Parquet 고정 |

---

## 7. 언제 Parquet를 쓰는 게 “과한가”?

- 데이터 < **50MB**
- 분석 1~2회만 하고 끝
- 컬럼 수 적음 (<10)

➡ 이 경우 CSV 유지가 더 단순

---

## 핵심 요약 (면접/실무용 문장)

> “CSV는 교환용 포맷이고, Parquet는 분석 및 처리용 포맷이다.  
> 반복 분석, 대용량, 컬럼 중심 접근이 필요할수록 Parquet의 장점이 커진다.”

---

원하시면 다음으로:
- **pandas vs polars vs dask 기준 비교**
- **Parquet + feature store 관점**
- **Kaggle 메모리 초과 방지 전략**

중 어떤 걸 더 깊게 볼지 말해 주세요.

---

### ❓ 질문 (User)
ArrowInvalid: ("Could not convert '5190142' with type str: tried to convert to int64", 'Conversion failed for column ID with type object')

### 💡 답변 (Assistant)
이 에러는 **CSV → Parquet 변환 과정에서 dtype 불일치가 발생했을 때 가장 흔히 나오는 Arrow 오류**입니다.  
메시지를 그대로 해석하면 원인이 명확합니다.

---

## 에러 메시지 해부

```text
ArrowInvalid:
("Could not convert '5190142' with type str:
 tried to convert to int64",
 'Conversion failed for column ID with type object')
```

### 핵심 의미
- `ID` 컬럼이 **object(str)** 로 들어와 있음
- Parquet 저장 시 **int64로 변환하려고 시도**
- 그런데 문자열 → 정수 변환이 **어떤 행에서 실패**

⚠️ `'5190142'` 자체는 문제 없어 보이지만  
**같은 컬럼에 숫자가 아닌 값이 섞여 있다는 뜻**입니다.

---

## 실제로 흔한 원인 TOP 5

### 1️⃣ 숫자 + 공백 / 숨은 문자
```text
"5190142 "
" 5190142"
```

### 2️⃣ 결측치 문자열
```text
""
"NA"
"null"
"None"
```

### 3️⃣ 실수 형태 문자열
```text
"5190142.0"
```

### 4️⃣ 일부 행에 문자 섞임
```text
"A5190142"
"5190142-1"
```

### 5️⃣ CSV 파싱 단계에서 dtype 추론 실패
- 일부 값 때문에 pandas가 `object`로 결정

---

## 1단계: 문제 값 정확히 확인 (가장 중요)

```python
df["ID"].apply(type).value_counts()
```

또는

```python
df[df["ID"].apply(lambda x: not str(x).isdigit())]["ID"].head(20)
```

👉 **이걸 안 보면 감으로 고치다 계속 터집니다**

---

## 2단계: 안전한 해결 패턴 (권장)

### ✅ 가장 안정적인 방법: `to_numeric`

```python
df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
```

- 변환 불가 → `NaN`
- Arrow 에러 100% 방지

이후 정책 선택:

```python
# 결측 제거
df = df.dropna(subset=["ID"])

# 또는 nullable integer
df["ID"] = df["ID"].astype("Int64")
```

---

## 3단계: Parquet 저장 (정석 루트)

```python
df.to_parquet(
    "/kaggle/working/data.parquet",
    engine="pyarrow",
    compression="snappy"
)
```

✔ 이 시점에서 에러 나면 **다른 컬럼도 같은 문제 있음**

---

## ⚠️ 절대 비추천 (하지만 많이들 함)

```python
df["ID"] = df["ID"].astype(int)  # ❌
```

이건:
- 공백
- NaN
- 실수 문자열  
하나라도 있으면 바로 죽습니다.

---

## 컬럼이 여러 개인 경우 (실전 패턴)

```python
int_cols = ["ID", "user_id", "order_id"]

for col in int_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
```

---

## CSV → Parquet 변환 시 Best Practice (중요)

### ✅ 변환 전 검증 루틴
```python
df.info()
df.isnull().sum()
```

### ✅ dtype 명시 로드 (가능하면)
```python
df = pd.read_csv(
    "data.csv",
    dtype={"ID": "string"}  # 먼저 string으로 고정
)

df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
```

---

## 왜 Parquet에서 이게 더 엄격하게 터지나?

- CSV: **느슨함** (문자든 숫자든 일단 읽음)
- Parquet: **스키마 강제**
- Arrow: **벡터화 + 타입 안정성 최우선**

👉 이 에러는 **Parquet의 단점이 아니라 장점의 부작용**

---

## 한 문장 요약 (실무용)

> “ArrowInvalid 오류는 대부분 CSV 단계에서 object로 들어온 컬럼에 숫자·문자가 섞여 있어 Parquet의 엄격한 타입 시스템이 이를 거부하면서 발생한다.”

---

원하시면 다음을 바로 도와줄 수 있습니다:
- **문제 행만 자동 추출하는 디버깅 코드**
- **dtype 자동 정규화 함수**
- **대규모 CSV 안전 변환 템플릿**

다음 단계로 뭐가 필요한지 말해 주세요.

---

### ❓ 질문 (User)
df.info() 결과 object로 나오는데 이대로 하면 안되나?

### 💡 답변 (Assistant)
짧게 답하면 **“object 상태로도 Parquet 저장은 가능하지만, 분석 목적이라면 그대로 두는 건 비권장”**입니다.  
왜 그런지 **정확한 기준**으로 설명하겠습니다.

---

## 1. 결론부터 (명확한 기준)

### ✅ 가능은 하다
```python
df.info()
# ID   object
```

이 상태에서도:
```python
df.to_parquet(...)
```
**성공할 수도 있습니다.**

### ❌ 하지만 하면 손해다
- 성능 ↓
- 메모리 ↑
- Parquet 장점 절반 포기

---

## 2. object 타입이 실제로 의미하는 것

`object`는 **타입이 아니라 “모르겠다”는 신호**입니다.

| 실제 데이터 | pandas dtype |
|-----------|-------------|
| "5190142" | object |
| 5190142 | int64 |
| "A123" | object |
| 5190142, "", "NA" 섞임 | object |

즉, `object` =  
> “문자일 수도 있고 숫자일 수도 있는데 내가 확신이 없다”

---

## 3. object 상태로 Parquet 저장 시 무슨 일이 벌어지나

### 3.1 Arrow가 하는 일
- 내부적으로 **string / binary 컬럼**으로 저장
- **숫자 컬럼 최적화 전부 무효**

### 3.2 잃는 것들

| 항목 | 손실 |
|----|----|
| Column pruning | ❌ 부분적 |
| Predicate pushdown | ❌ |
| 압축 효율 | ❌ |
| 정렬 기반 연산 | ❌ |
| 메모리 locality | ❌ |

➡ **“Parquet 모양의 CSV”가 됨**

---

## 4. 언제 object 그대로 둬도 되는가 (예외)

### ✔ 진짜 문자열 ID일 때
```text
user_00123
A-5190142
```

이 경우:
```python
df["ID"] = df["ID"].astype("string")
```

👉 `object` ❌, `string` ⭕  
(pandas nullable string dtype)

---

### ✔ 로그 / 텍스트 / 카테고리 값일 때
- URL
- 설명 텍스트
- 코드값 (숫자처럼 보이지만 의미는 문자열)

---

## 5. 언제 반드시 바꿔야 하는가 (당신 케이스)

에러 메시지:
```text
tried to convert to int64
Conversion failed for column ID with type object
```

이건 **“숫자로 쓰려고 했다는 뜻”**입니다.

➡ 즉,
- 조인 키
- 정렬
- 그룹핑
- 수치 분석

에 쓰일 컬럼

👉 이 경우 object 유지 ❌

---

## 6. 가장 안전한 실무 패턴 (추천)

### Step 1. 의도를 명확히 한다
```python
# ID는 숫자다
```

### Step 2. 강제 변환 (실패 허용)
```python
df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
```

### Step 3. 정책 결정
```python
# 1) 잘못된 행 제거
df = df.dropna(subset=["ID"])

# 2) nullable int
df["ID"] = df["ID"].astype("Int64")
```

---

## 7. df.info()에서 이렇게 보이면 “좋은 상태”

```text
ID            Int64
user_id       int32
price       float32
category    category
```

➡ 이 상태가 **Parquet 최적화 100% 활용 상태**

---

## 8. 한 줄 요약 (면접/실무용)

> “object dtype은 분석용 타입이 아니라 임시 상태다.  
> Parquet 기반 분석에서는 의미에 맞는 명시적 dtype으로 정규화해야 한다.”

---

## 선택 가이드 (빠른 판단표)

| 상황 | 그대로 둬도 됨? |
|----|----|
| 숫자로 연산/조인 | ❌ |
| 사람이 읽는 코드 | ❌ |
| 실제 문자열 ID | ⭕ (string으로 변경 권장) |
| 로그/텍스트 | ⭕ |
| CSV → Parquet 분석 파이프라인 | ❌ |

---

원하시면 다음으로:
- **object → 최적 dtype 자동 변환 함수**
- **문제 행만 정확히 찍어내는 디버깅 코드**
- **Kaggle 메모리 초과 안 나는 Parquet 파이프라인**

어디까지 정리해볼지 말씀 주세요.

---

### ❓ 질문 (User)
그러면 지금 문제는 object 타입으로 나온 모든 데이터들을 각각에 적합한 데이터 타입으로 바꿔야된다는거야?

### 💡 답변 (Assistant)
정확히 짚으셨습니다.  
**결론부터 말하면 “object로 나온 모든 컬럼을 무조건 바꿔야 하는 건 아니고, ‘의미가 명확한 컬럼’만 반드시 바꿔야 합니다.”**  
아래를 기준으로 판단하면 됩니다.

---

## 1. 핵심 원칙 (이 한 줄이 기준입니다)

> **object는 ‘임시 상태’이고,  
> Parquet 중심 분석에서는 “의미가 수치/범주/시간으로 명확한 컬럼만” 타입을 확정하면 된다.**

---

## 2. object 컬럼을 3가지로 분류하자

### ① 반드시 바꿔야 하는 object (필수)

**“사람이 봐도 숫자 / 시간인 컬럼”**

| 예시 | 바꿔야 하는 타입 |
|---|---|
| ID, user_id, order_id | Int64 / int32 |
| price, amount | float32 / float64 |
| age, count | int |
| created_at, timestamp | datetime64 |

📌 이걸 안 바꾸면:
- 지금 같은 ArrowInvalid 에러 발생
- Parquet 성능 반토막

---

### ② 바꾸는 게 강력히 권장되는 object

**“범주형 값이 반복되는 컬럼”**

| 예시 | 권장 타입 |
|---|---|
| category | category |
| status (OK/FAIL) | category |
| gender | category |

```python
df["category"] = df["category"].astype("category")
```

✔ 메모리 크게 절약  
✔ groupby / value_counts 빨라짐

---

### ③ 굳이 안 바꿔도 되는 object (예외)

**“진짜 문자열”**

| 예시 |
|---|
| 설명 텍스트 |
| URL |
| free-text 로그 |
| 리뷰 내용 |

👉 이 경우도 `object`보다는

```python
df["text"] = df["text"].astype("string")
```

이게 더 낫습니다 (nullable + Arrow 친화적)

---

## 3. 절대 하면 안 되는 오해 ❌

> ❌ “object니까 전부 바꿔야 한다”

이건 아닙니다.  
**텍스트 컬럼까지 int/float로 억지 변환하면 데이터 깨집니다.**

---

## 4. 실무에서 쓰는 판단 절차 (그대로 쓰세요)

### Step 1. object 컬럼 목록 뽑기
```python
obj_cols = df.select_dtypes(include="object").columns
obj_cols
```

---

### Step 2. 컬럼별 “의미”로 분류
```text
ID → 숫자
price → 숫자
created_at → 시간
category → 범주
description → 텍스트
```

(이건 자동화 못 합니다. 사람이 결정해야 합니다.)

---

### Step 3. 패턴별 변환

#### 숫자
```python
df["ID"] = pd.to_numeric(df["ID"], errors="coerce").astype("Int64")
```

#### 날짜/시간
```python
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
```

#### 범주
```python
df["category"] = df["category"].astype("category")
```

#### 텍스트
```python
df["description"] = df["description"].astype("string")
```

---

## 5. “모든 object를 자동 변환”하고 싶다면 (현실적인 선)

완전 자동은 위험하지만, **보조용으로는 가능**

```python
for col in obj_cols:
    # 숫자 시도
    converted = pd.to_numeric(df[col], errors="ignore")
    if not converted.equals(df[col]):
        df[col] = converted
```

⚠️ 최종 결정은 사람이 해야 합니다.

---

## 6. 지금 당신 상황을 정확히 요약하면

- ❌ 문제의 본질: object 자체
- ✅ 진짜 원인:  
  **숫자로 쓰일 컬럼(ID)이 object로 남아 있음**

👉 따라서
- 모든 object를 바꿀 필요 ❌
- **ID / price / timestamp 같은 핵심 컬럼만 먼저 정규화** ⭕
- 그다음 Parquet 저장

---

## 7. 실무/면접용 한 문장

> “object 컬럼은 전부 변환 대상이 아니라, 의미가 수치·시간·범주로 명확한 컬럼만 명시적으로 dtype을 확정해야 한다.”

---

원하시면 다음을 바로 만들어줄 수 있습니다:
- **object 컬럼 자동 분류 체크리스트**
- **Parquet 저장 전 dtype 검증 함수**
- **Kaggle용 안전 변환 템플릿**

다음 단계로 뭘 할지 정해볼까요?

---

### ❓ 질문 (User)
print(df["Smart Location"].unique())의 결과로
===
['Amsterdam, Netherlands' 'Antwerpen, Belgium' 'Antwerp, Belgium' ...
 'sant elm, Spain' 'villa verde bajo, Spain' 'Centro, Spain']
===
여기서 ... 부분을 전부 보고 싶은데 하는 방법 알려줘.

### 💡 답변 (Assistant)
이건 **pandas가 출력 길이를 제한해서 생기는 현상**입니다.  
데이터가 잘린 게 아니라 **“출력만 축약”**된 상태예요.

아래 방법 중 **목적에 맞는 것 하나만** 쓰면 됩니다.

---

## 1️⃣ 가장 간단한 방법 (권장)

```python
for v in df["Smart Location"].unique():
    print(v)
```

✔ 절대 안 잘림  
✔ 실제 값 전부 확인 가능  
✔ 디버깅용으로 가장 정확

---

## 2️⃣ 출력 옵션을 임시로 풀기

```python
import pandas as pd

pd.set_option("display.max_seq_items", None)
print(df["Smart Location"].unique())
```

🔹 `unique()` 결과는 numpy array라서  
`max_seq_items`가 출력 제한에 영향 줍니다.

⚠️ 세션 전체에 적용됨 (끝나면 원복 권장)

```python
pd.reset_option("display.max_seq_items")
```

---

## 3️⃣ 리스트로 변환해서 보기

```python
list(df["Smart Location"].unique())
```

✔ 짧으면 OK  
❌ 길면 여전히 보기 힘들 수 있음

---

## 4️⃣ 개수 + 일부 샘플 같이 보기 (실무용)

```python
values = df["Smart Location"].unique()

print("고유값 개수:", len(values))
print("앞 20개:")
for v in values[:20]:
    print(v)
```

---

## 5️⃣ 정렬해서 보기 (강력 추천)

지금 데이터처럼
- 대소문자 섞임 (`Amsterdam` vs `sant elm`)
- 표현 통일 안 됨 (`Antwerp` vs `Antwerpen`)

이럴 땐 정렬이 필수입니다.

```python
for v in sorted(df["Smart Location"].unique()):
    print(v)
```

👉 이러면 **정규화 필요성도 바로 보입니다**

---

## 6️⃣ 만약 너무 많다면 (EDA 패턴)

```python
df["Smart Location"].nunique()
```

```python
df["Smart Location"].value_counts().head(30)
```

➡ “정리해야 할 컬럼인지” 판단 가능

---

## 핵심 요약

| 목적 | 방법 |
|---|---|
| 전부 보기 | `for v in unique(): print(v)` |
| 옵션으로 해결 | `pd.set_option("display.max_seq_items", None)` |
| 정리/비교 | `sorted(unique())` |
| 분포 확인 | `value_counts()` |

---

### 실무 한 줄 팁
> **“unique() 출력이 잘리면 데이터 문제가 아니라 출력 옵션 문제다.”**

다음으로는:
- **Smart Location 정규화 (대소문자 / 국가명 통일)**
- **city / country 분리**
- **category로 변환해 Parquet 최적화**

이 중 어떤 걸 해볼까요?

---

### ❓ 질문 (User)
```df["Location"]```
```Amsterdam, Netherlands```
이런 식으로 되어있는 시리즈 혹은 데이터프레임 중에서 뒤에 있는 Netherlands 값인 데이터만 보고싶어. 
예를 들어 df["Location"][-1] == "Netherlands" 인 애들만 보여줘. 라는 걸 하고싶은거지.

### 💡 답변 (Assistant)
의도가 **아주 명확**합니다 👍  
`"Amsterdam, Netherlands"` 같은 문자열에서 **콤마 뒤의 국가(country)만 기준으로 필터링**하고 싶은 거죠.

아래를 **안전성 → 가독성 → 성능** 순으로 정리해 드릴게요.

---

## ✅ 가장 정석적이고 안전한 방법 (권장)

### 1️⃣ country 컬럼을 만들어서 필터링

```python
df["country"] = df["Location"].str.split(",").str[-1].str.strip()

df[df["country"] == "Netherlands"]
```

### 왜 이게 정답인가?
- 가독성 최고
- 디버깅 쉬움
- 이후 `groupby`, `value_counts`, `category` 변환 가능
- Parquet 저장에도 유리

---

## 2️⃣ 한 줄로 바로 필a (임시 분석용)

```python
df[df["Location"].str.split(",").str[-1].str.strip() == "Netherlands"]
```

✔ 바로 동작  
❌ 반복 사용엔 비추 (가독성 ↓)

---

## 3️⃣ 정규식으로 필터링 (콤마 유무 불안할 때)

```python
df[df["Location"].str.extract(r",\s*(.+)$")[0] == "Netherlands"]
```

✔ 포맷이 조금 깨져도 대응  
❌ 직관성은 낮음

---

## 4️⃣ 대소문자 섞인 경우 (실무에서 자주 나옴)

```python
df[
    df["Location"]
    .str.split(",")
    .str[-1]
    .str.strip()
    .str.lower() == "netherlands"
]
```

---

## 5️⃣ 방어 코드 (결측치/이상치 포함)

```python
country = (
    df["Location"]
    .astype("string")
    .str.split(",")
    .str[-1]
    .str.strip()
)

df[country == "Netherlands"]
```

---

## 6️⃣ df["Location"][-1]에 대한 정확한 짚고 넘어가기

```python
df["Location"][-1]
```

이건:
- ❌ “마지막 요소”
- ❌ “뒤 문자열”

입니다.

👉 **문자열의 뒤가 아니라 Series의 인덱싱**입니다.  
지금 쓰고 싶은 건 **문자열 처리(str accessor)** 입니다.

---

## 7️⃣ 실무적으로 더 좋은 구조 (강력 추천)

한 번만 분리해 두세요.

```python
df[["city", "country"]] = (
    df["Location"]
    .str.split(",", n=1, expand=True)
    .apply(lambda s: s.str.strip())
)
```

이제부터는:

```python
df[df["country"] == "Netherlands"]
```

✔ 빠름  
✔ 실수 없음  
✔ Parquet 저장 시 category로 최적화 가능

```python
df["country"] = df["country"].astype("category")
```

---

## 한 문장 요약

> `df["Location"][-1]`은 인덱싱이고,  
> 원하는 건 `str.split().str[-1].str.strip()`이다.

---

원하시면 다음으로:
- **국가명 표준화 (Netherlands vs The Netherlands)**
- **city / country 자동 정규화 함수**
- **이 컬럼을 Parquet 최적 구조로 바꾸는 방법**

어디까지 가볼까요?

---

### ❓ 질문 (User)
만약 데이터에 Netherlands 로만 되어 있으면 좋은데, The Netherlands 라던지 UK, United Kindom 등 특정 국가들을 부르는 방법들이 여러가지 잖아. The 같은 전치사만 붙으면야 구하기 쉬울텐데 말이지. 이럴땐 어떻게 하는게 좋을까.

### 💡 답변 (Assistant)
이 질문은 **데이터 정규화의 정석적인 난관**을 정확히 짚은 겁니다.  
결론부터 말하면 **“규칙으로 해결할 수 있는 것”과 “사전(dict)로 해결해야 하는 것”을 분리**해야 합니다.

---

## 1. 핵심 결론 (실무 기준)

> **국가명 정규화는  
> (1) 규칙 기반 전처리 +  
> (2) 명시적 매핑 테이블  
> 이 두 단계를 조합하는 게 정답이다.**

하나만으로는 절대 안정적이지 않습니다.

---

## 2. 1단계: 규칙으로 커버 가능한 것 (자동 처리)

### 2.1 대소문자 / 공백 / 관사 제거

```python
country = (
    df["country"]
    .astype("string")
    .str.lower()
    .str.strip()
)
```

### 2.2 관사 제거 (the)

```python
country = country.str.replace(r"^the\s+", "", regex=True)
```

- `The Netherlands` → `netherlands`
- `the united states` → `united states`

✔ 이 단계는 **무조건 해도 됨**

---

## 3. 여기서부터가 핵심 문제

### ❌ 규칙으로 절대 해결 안 되는 케이스

| 표기 | 실제 국가 |
|---|---|
| UK | United Kingdom |
| U.K. | United Kingdom |
| Great Britain | United Kingdom |
| England | United Kingdom (⚠️ 정치적으로 민감) |
| Holland | Netherlands |
| Korea | South Korea |
| Republic of Korea | South Korea |

👉 **이건 언어 문제가 아니라 도메인 지식 문제**

---

## 4. 2단계: 명시적 매핑 테이블 (정답 루트)

### 4.1 최소 매핑 dict 만들기 (실무용)

```python
COUNTRY_MAP = {
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "great britain": "United Kingdom",
    "england": "United Kingdom",
    "holland": "Netherlands",
    "republic of korea": "South Korea",
    "korea": "South Korea",
}
```

적용:

```python
def normalize_country(x):
    if pd.isna(x):
        return x

    x = x.lower().strip()
    x = x.replace("the ", "", 1)

    return COUNTRY_MAP.get(x, x.title())


df["country_norm"] = df["country"].apply(normalize_country)
```

---

## 5. 왜 “dict 기반”이 필수인가 (중요)

국가명 문제는:
- NLP 문제가 아님
- 정규표현식 문제가 아님
- **표준화 문제**

즉,
> **“이 표현은 저 국가를 의미한다”는 선언이 필요**

이 선언이 바로 **매핑 테이블**입니다.

---

## 6. 실무에서 가장 좋은 구조 (강력 추천)

### 6.1 원본 보존 + 정규화 컬럼 분리

```python
df["country_raw"] = df["country"]
df["country_norm"] = normalize_country(df["country"])
```

❗ 원본 덮어쓰지 마세요  
(나중에 반드시 감사/디버깅 필요)

---

## 7. 규모가 커지면 이렇게 간다

### 옵션 A: ISO 코드 기반 (최종 형태)

```text
Netherlands → NL
United Kingdom → GB
South Korea → KR
```

이후 분석은 **코드 기준**으로만 수행

---

### 옵션 B: pycountry 사용 (보조용)

```python
import pycountry

def to_iso(name):
    try:
        return pycountry.countries.lookup(name).alpha_2
    except LookupError:
        return None
```

⚠️ 단점:
- UK, Holland 같은 별칭 약함
- 실무에서는 **dict + pycountry 혼합**이 현실적

---

## 8. 당신 상황에 딱 맞는 추천 전략

지금 데이터 특성상 (Smart Location / Location):

### ✅ 추천 파이프라인
1. Location → city / country 분리
2. country 소문자 + 관사 제거
3. **핵심 국가만 dict 매핑**
4. 정규화된 country 컬럼 생성
5. `category`로 변환
6. Parquet 저장

---

## 9. 한 문장 요약 (면접/실무)

> “국가명 표준화는 규칙 기반 정제 후, 도메인 지식을 담은 매핑 테이블로 마무리하는 것이 가장 안정적이다.”

---

## 다음 단계로 추천

원하시면 바로:
- **국가명 정규화 전용 함수 (재사용 가능)**
- **ISO 코드까지 포함한 표준화 파이프라인**
- **이걸 Parquet + category로 최적화하는 구조**

어디까지 만들어볼지 말씀 주세요.

---

### ❓ 질문 (User)
이렇게 데이터를 막 바꾸는 경우에는 새로운 인덱스? 칼럼? 으로 저장하는 것이 좋은 선택지겠지?

### 💡 답변 (Assistant)
네. **이 경우에는 “무조건 새 컬럼으로 저장”하는 게 정답에 가깝습니다.**  
이건 취향 문제가 아니라 **데이터 엔지니어링/분석 쪽에서 거의 합의된 원칙**입니다.

아래를 기준으로 판단하면 됩니다.

---

## 1. 핵심 원칙 (이 한 줄이면 충분)

> **의미를 해석하거나 규칙을 적용해 바꾼 값은 절대 원본을 덮어쓰지 않는다.**

국가명 정규화처럼:
- 규칙 적용
- 사전 매핑
- 도메인 해석

이 들어간 순간 → **파생 데이터(derived data)** 입니다.

---

## 2. 왜 새 컬럼이 정답인가 (이유 5가지)

### ① 되돌릴 수 있음 (Reproducibility)
- 매핑 실수
- 요구사항 변경
- 기준 국가 변경

→ 원본 있으면 재생성 가능  
→ 원본 없으면 **데이터 신뢰도 붕괴**

---

### ② 디버깅/감사 가능
```python
df[df["country_raw"] != df["country_norm"]]
```

이 한 줄이 가능해짐  
(이건 실무에서 진짜 중요합니다)

---

### ③ 분석 의도 명확
```text
country_raw   → 수집된 그대로
country_norm  → 정규화 후 (분석 기준)
```

누가 봐도 의미가 분리됨

---

### ④ 파이프라인 분리
- ingestion 단계: raw
- cleaning 단계: norm
- modeling 단계: norm만 사용

👉 데이터 파이프라인 교과서 구조

---

### ⑤ Parquet / Feature Store / ML 친화적
- raw: string
- norm: category / ISO code

ML에 쓰는 건 **항상 norm**

---

## 3. 인덱스 vs 컬럼? (중요한 질문)

### ❌ 인덱스로 두는 건 비추천
- 의미 데이터는 인덱스가 아님
- 조인/필터 불편
- Parquet에서 인덱스는 애매

> **인덱스는 “정렬/식별용”이지 “의미 정보”가 아니다**

---

### ✅ 컬럼이 정답
```text
location_raw
country_raw
country_norm
country_iso
```

---

## 4. 추천 네이밍 컨벤션 (실무용)

| 목적 | 컬럼명 |
|---|---|
| 원본 | `*_raw` |
| 규칙 정제 | `*_clean` |
| 표준화 | `*_norm` |
| 코드화 | `*_code` / `*_iso` |

예시:
```text
Location
country_raw
country_norm
country_iso
```

---

## 5. 실제 예시 (당신 케이스 기준)

```python
df["country_raw"] = (
    df["Location"]
    .str.split(",", n=1)
    .str[-1]
    .str.strip()
)

df["country_norm"] = df["country_raw"].apply(normalize_country)
```

이후 분석은:
```python
df[df["country_norm"] == "Netherlands"]
```

---

## 6. “그럼 언제 덮어써도 되나?” (예외)

### ✔ 완전히 무손실 변환
- 공백 trim
- 대소문자 통일
- 명백한 typo 수정 (사전 검증된 경우)

그마저도 **raw 컬럼 삭제는 마지막 단계**에서만.

---

## 7. 실무/면접용 한 문장 정리

> “해석이나 매핑이 들어간 데이터는 파생 컬럼으로 분리하고, 원본은 항상 보존한다.”

---

## 8. 한 단계 더 나아가면 (추천)

- `country_norm` → `category`
- `country_iso` → ML feature
- Parquet 저장 시:
  ```python
  df.to_parquet("clean.parquet")
  ```

---

원하시면 다음으로:
- **컬럼 설계 템플릿 (raw/clean/norm 구조)**
- **국가명 정규화 전체 파이프라인 코드**
- **이 구조를 그대로 Kaggle → 실무로 가져가는 법**

다음에 어디까지 확장해볼까요?

---
