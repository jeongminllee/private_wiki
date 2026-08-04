---
type: Error Note
title: "OpenML 데이터셋 오류"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-04-20)"
tags: [errors, chatgpt-export]
timestamp: 2026-04-20
status: active
---

# OpenML 데이터셋 오류

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-04-20

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
코드 흐름을 보면 `ValueError: too many values to unpack (expected 4)`는 LightAutoML 쪽보다 먼저, `OpenML dataset.get_data(...)` 반환값 개수에서 터졌을 가능성이 매우 큽니다. 최신 문서를 확인해서 정확히 짚겠습니다.

---

### ❓ 질문 (User)
데이터 분석 중 target value 가 1 또는 2로만 구성되어있는 int 타입의 데이터가 들어왔어. 
```
total_dataset = \
['australian', 'blood-transfusion-service-center', 'credit-g', 'kc1', 'jasmine', 'kr-vs-kp', 'sylvine', 'phoneme', 'christine',
'guillermo', 'riccardo', 'amazon_employee_access', 'nomao', 'bank-marketing', 'adult', 'kddcup09_appetency', 'apsfailure',
'numerai28.6', 'higgs', 'MiniBooNE', 'car', 'cnae-9', 'connect-4', 'dilbert', 'fabert', 'fashion-mnist', 'helena', 'jannis',
'jungle_chess_2pcs_raw_endgame_complete', 'mfeat-factors', 'robert', 'segment', 'shuttle', 'vehicle', 'volkert']


# Get dataset by name
dataset = openml.datasets.get_dataset(total_dataset[1])
# Other data formats can be requested (e.g. numpy)
# Target features, feature names and types are also returned
print(dataset)X, y, is_categorical, feat_names = dataset.get_data( 
    dataset_format="dataframe", target=dataset.default_target_attribute)N_THREADS = 8           # the number of vCPUs 
N_FOLDS = 10            # K-FOLD 10회 실시
TIMEOUT = 2 * 60 * 60   # 2시간 뒤에 킬
RANDOM_STATE = 42       # 난수 고정
TEST_SIZE = 0.2         # 테스트 케이스 분류
TARGET_NAME = 'Class'

y = y.astype('int64')
y = pd.to_numeric(y)


df = pd.concat([X, y], axis=1)

for col in df.columns :
    if df[col].dtype != 'float64':
        df[col] = df[col].astype('int32')
    else :
        df[col] = df[col].astype('float32')
print(df.dtypes)
print('Object/String columns:', df.select_dtypes(include=['object', 'string']).columns.tolist())
print('Target dtype after:', df[TARGET_NAME].dtype)
print('Target value counts:')
print(df[TARGET_NAME].value_counts())
print(df.columns)# 난수 및 스레드 
np.random.seed(RANDOM_STATE)
torch.set_num_threads(N_THREADS)

# train test split
train_data, test_data = train_test_split(
    df,
    test_size=TEST_SIZE,
    stratify=df[TARGET_NAME],
    random_state=RANDOM_STATE
)

print(train_data.info())task = Task('binary')   # binary : auc 자동으로 설정됨. 
# Australian 데이터셋 분류
roles = {
    'target' : TARGET_NAME,
}RD = ReportDeco(output_path='tabularAutoML_model_report_blood_transfusion') 

automl_rd = RD(
    TabularAutoML(
        task = task,
        timeout = TIMEOUT,
        cpu_limit = N_THREADS,
        reader_params = {'n_jobs': N_THREADS, 'cv': N_FOLDS, 'random_state': RANDOM_STATE},
        general_params= {'use_algos':'auto'}
    )
)

out_of_fold_predictions = automl_rd.fit_predict(train_data, roles = roles, verbose=1)
```
ValueError: too many values to unpack (expected 4)
이런 오류를 주더라고. 
뭐가 문제일까?

### 💡 답변 (Assistant)
문제의 핵심은 **타깃값이 1/2인 int라서가 아니라, `OpenML`의 `get_data()` 호출부**일 가능성이 가장 큽니다.

최신 OpenML 문서 기준으로 `dataset.get_data()`는 **4개만 반환**합니다.

- `X`
- `y`
- `categorical_indicator`
- `attribute_names` citeturn398451view1turn839594view0

그래서 원칙적으로는 이 줄 자체는 맞습니다.

```python
X, y, is_categorical, feat_names = dataset.get_data(
    target=dataset.default_target_attribute
)
```

다만, 최신 문서의 `get_data()` 시그니처를 보면 **`dataset_format="dataframe"` 인자는 더 이상 보이지 않고**, 데이터프레임 형태를 기본으로 반환하는 형태로 문서화되어 있습니다. 즉 지금 쓰는 코드가 **설치된 OpenML 버전과 예전 예제가 섞인 상태**일 가능성이 큽니다. OpenML은 `get_data`의 반환 타입 동작이 버전별로 정리된 이력이 있습니다. citeturn839594view0turn398451view2

가장 먼저 이렇게 바꿔보세요.

```python
X, y, is_categorical, feat_names = dataset.get_data(
    target=dataset.default_target_attribute
)
```

그리고 바로 아래를 찍어보면 원인이 거의 확정됩니다.

```python
tmp = dataset.get_data(target=dataset.default_target_attribute)
print(type(tmp))
print(len(tmp))
print(tmp)
```

이렇게 하면 실제로 지금 환경의 `openml`이 몇 개를 반환하는지 바로 확인됩니다.

추가로 코드에서 같이 점검할 부분이 몇 개 있습니다.

첫째, `TARGET_NAME = 'Class'`를 하드코딩한 것이 위험합니다.  
지금 불러온 데이터셋은 `blood-transfusion-service-center`인데, 실제 타깃 컬럼명이 항상 `'Class'`라고 보장되지 않습니다. `dataset.default_target_attribute`를 그대로 쓰는 편이 안전합니다. citeturn398451view1turn246745search1

즉 이렇게 바꾸는 게 좋습니다.

```python
TARGET_NAME = dataset.default_target_attribute

X, y, is_categorical, feat_names = dataset.get_data(
    target=TARGET_NAME
)

y = pd.to_numeric(y).astype("int64")
df = pd.concat([X, y], axis=1)
```

둘째, binary 분류에서 **타깃이 1/2인 것 자체는 큰 문제는 아니지만**, 라이브러리에 따라 **0/1로 맞춰두면 더 안전**합니다. 특히 AutoML 파이프라인에서는 라벨 인코딩이 들어가더라도 미리 정규화해 두는 편이 디버깅이 쉽습니다.

```python
y = pd.to_numeric(y).astype("int64")
if set(y.unique()) == {1, 2}:
    y = y.map({1: 0, 2: 1}).astype("int32")
```

셋째, 지금 dtype 일괄 변환도 조금 거칠 수 있습니다.

```python
for col in df.columns:
    if df[col].dtype != 'float64':
        df[col] = df[col].astype('int32')
    else:
        df[col] = df[col].astype('float32')
```

이 로직은 `bool`, `category`, nullable integer, 혹은 특수한 object 컬럼이 있으면 예상치 못한 변환 문제를 만들 수 있습니다. 더 안전하게는 이렇게 나누는 편이 낫습니다.

```python
for col in df.columns:
    if pd.api.types.is_float_dtype(df[col]):
        df[col] = df[col].astype("float32")
    elif pd.api.types.is_integer_dtype(df[col]):
        df[col] = df[col].astype("int32")
```

정리하면, 우선순위는 이겁니다.

1. `get_data()`에서 `dataset_format="dataframe"` 제거  
2. `tmp = dataset.get_data(...)` 후 `len(tmp)` 확인  
3. `TARGET_NAME = dataset.default_target_attribute`로 변경  
4. binary target이면 `1/2 -> 0/1`로 매핑  
5. 그 다음에도 에러가 나면 그때는 LightAutoML 내부 입력 형식 문제를 보시면 됩니다

추천 수정본은 아래처럼 쓰면 됩니다.

```python
dataset = openml.datasets.get_dataset(total_dataset[1])

TARGET_NAME = dataset.default_target_attribute

X, y, is_categorical, feat_names = dataset.get_data(
    target=TARGET_NAME
)

y = pd.to_numeric(y).astype("int64")

if set(y.unique()) == {1, 2}:
    y = y.map({1: 0, 2: 1}).astype("int32")

df = pd.concat([X, y.rename(TARGET_NAME)], axis=1)

for col in df.columns:
    if pd.api.types.is_float_dtype(df[col]):
        df[col] = df[col].astype("float32")
    elif pd.api.types.is_integer_dtype(df[col]):
        df[col] = df[col].astype("int32")

print(df.dtypes)
print("Object/String columns:", df.select_dtypes(include=["object", "string"]).columns.tolist())
print("Target dtype after:", df[TARGET_NAME].dtype)
print("Target value counts:")
print(df[TARGET_NAME].value_counts())
```

제 판단으로는 가장 유력한 원인은 **`openml` 버전 차이로 인한 `get_data()` 호출 방식 불일치**입니다.  
원하시면 제가 다음 답변에서 **이 코드를 LightAutoML 기준으로 끝까지 한 번 정리해서, 바로 실행 가능한 형태로 다시 써드릴게요.**

---
