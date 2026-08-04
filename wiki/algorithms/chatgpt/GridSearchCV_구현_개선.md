---
type: Concept
title: "GridSearchCV 구현 개선"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-04-21)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-04-21
status: active
---

# GridSearchCV 구현 개선

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-04-21

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
scikit-learn 에 gridsearchcv 를 손으로 코딩중이야. cv와 confusion matrix랑 연계해서 보고서를 작성하고 가장 최적의 값이 나왔을 때 그 값을 기록해놨다가 최종 보고서에 작성하는 로직이야. 
```
def my_gridSearchCV(data, param_grid, cv=5) :
    data_split = int(data.shape[0]*(1/cv))
    def precision(tp, fp) :
       return tp / (tp + fp)

    def recall(tp, fn) :
        return tp / (tp + fn)

    total_score = 0
    record_C = 0
    record_gam = 0
    res_score = []
    for d in range(cv) :
        train_X = pd.concat([data.iloc[:data_split*d, :data.shape[1]-1], data.iloc[data_split*(d+1):, :df_1.shape[1]-1]])   # (16512,8)
        train_y = pd.concat([data.iloc[:data_split*d, data.shape[1]-1], data.iloc[data_split*(d+1):, df_1.shape[1]-1]])
        test_X = data.iloc[data_split*d:data_split*(d+1), :data.shape[1]-1]      # (4128, 8)
        test_y = data.iloc[data_split*d:data_split*(d+1):, data.shape[1]-1]
        
        for C in param_grid['C'] :
                for gamma in param_grid['gamma'] :
                        svm = SVC(C=C, gamma=gamma)
                        svm.fit(train_X, train_y)
                        pred_y = svm.predict(test_X)
                        svm_matrix = metrics.confusion_matrix(test_y, pred_y)
                        print(svm_matrix)

                        classification_report = metrics.classification_report(test_y, pred_y)
                        print(classification_report)
                        with open('metrics_classification_report.txt', 'a', encoding='utf-8') as f:
                                # f.write(svm_matrix)
                                f.write(classification_report)
                        # 정답 0에 대한 지표 
                        tp0 = svm_matrix[0][0]
                        fp0 = svm_matrix[1][0]
                        fn0 = svm_matrix[0][1]

                        pre0 = precision(tp0, fp0)
                        rec0 = recall(tp0, fn0)
                        # 정답 1에 대한 지표
                        tp1 = svm_matrix[1][1]
                        fp1 = svm_matrix[0][1]
                        fn1 = svm_matrix[1][0]
                        pre1 = precision(tp1, fp1)
                        rec1 = recall(tp1, fn1)

                        pred_score = [pre0, rec0, pre1, rec1]
                        sum_pred_score = sum(pred_score)
                        if total_score < sum_pred_score :
                                total_score = sum_pred_score
                                record_C = C
                                record_gam = gamma
                                res_score = pred_score
                                final_report = classification_report

                     
with open('res_report.txt', 'w', encoding='utf-8') as f:
       f.write(f"optimal C : {record_C}\n")
       f.write(f"optimal gamma : {record_gam}\n")
       f.write(f"final score : {res_score}\n")
       f.write(f"final report : \n{final_report}")
```
이거를 모듈화 해서 다른 파일에 저장해놨다가 main 파일로 import 해서 쓰고 싶은데 main 파일에서 모델을 생성해서 집어넣으니까 오류가 나더라고. 진짜 gridsearchCV 처럼 구현하려면 어떻게 해야할지 조언좀 해줘.

### 💡 답변 (Assistant)
구조를 진짜 `GridSearchCV`처럼 만들려면 핵심이 딱 세 가지예요.  
`모델 객체를 함수 안에서 직접 고정하지 말기`, `파라미터를 외부에서 주입받아 clone해서 쓰기`, `fold별 점수와 전체 최적 파라미터를 분리해서 관리하기`입니다. 먼저 scikit-learn 쪽 인터페이스를 확인해서 그 방식에 맞춰 설명해볼게요.

---

### 💡 답변 (Assistant)
좋아요. 지금 코드가 **“그리드 탐색 + CV + 리포트 저장”**의 핵심은 이미 잡고 있어요. 다만 **진짜 `GridSearchCV`처럼 재사용 가능한 형태**로 만들려면 구조를 조금 바꿔야 합니다.

가장 중요한 포인트는 이것입니다.

1. **모델을 함수 내부에서 직접 `SVC(...)`로 고정하지 말고**
2. **`estimator`를 인자로 받아서**
3. **각 파라미터 조합마다 `clone(estimator)` 후 `set_params(**params)`로 학습**
4. **fold별 결과와 전체 best 결과를 체계적으로 저장**
5. 가능하면 **함수보다 클래스 형태**로 만들어 `best_params_`, `best_estimator_`, `cv_results_` 같은 속성을 갖게 하기

scikit-learn의 `GridSearchCV`도 기본적으로 **estimator 객체**와 **param_grid**를 받아서 파라미터 조합을 전부 탐색하며, 메타 estimator는 보통 내부에서 **clone된 unfitted estimator**를 사용합니다. 또 estimator의 생성자 인자는 그대로 보존되고, 학습 후 속성은 보통 `_`가 붙는 형태로 저장하는 인터페이스를 따릅니다. citeturn254543search0turn254543search4turn254543search5turn254543search9

---

## 왜 지금 `main`에서 모델을 넣었을 때 꼬이기 쉬운가

지금 함수는 내부에 이 줄이 박혀 있죠.

```python
svm = SVC(C=C, gamma=gamma)
```

이러면 함수가 **SVC 전용**이 됩니다. 그래서 `main.py`에서 모델을 만들어 넣어도, 함수 안에서는 그 모델을 안 쓰고 새 `SVC`를 만들게 됩니다.

또 진짜 `GridSearchCV`처럼 만들려면 이렇게 되어야 합니다.

```python
def my_grid_search_cv(estimator, param_grid, X, y, cv=5):
```

그리고 내부에서:

```python
model = clone(estimator)
model.set_params(**params)
model.fit(X_train, y_train)
```

이렇게 가야 합니다. `clone`은 **같은 파라미터를 가진 새 “미학습” estimator**를 만드는 함수라서, fold마다 모델 상태가 섞이지 않게 해줍니다. 이게 scikit-learn 메타 estimator의 핵심 패턴입니다. citeturn254543search5turn254543search9

---

## 지금 코드에서 바로 보이는 문제점

당장 구조적으로 몇 개가 보여요.

### 1) `df_1.shape[1]`가 섞여 있음
여기요.

```python
data.iloc[data_split*(d+1):, :df_1.shape[1]-1]
```

`data.shape[1]`를 써야 하는데 `df_1.shape[1]`가 섞여 있습니다.  
모듈화했을 때 외부 변수에 의존하면 바로 깨집니다.

---

### 2) `test_y` 슬라이싱 오타 가능성 큼

```python
test_y = data.iloc[data_split*d:data_split*(d+1):, data.shape[1]-1]
```

`iloc[row_start:row_end, col]`여야 하는데 `:`가 하나 더 들어가 있어서 가독성도 떨어지고 실수 유발이 큽니다.

보통 이렇게 씁니다.

```python
test_y = data.iloc[data_split*d:data_split*(d+1), data.shape[1]-1]
```

---

### 3) 데이터 마지막 fold 누락 가능성
```python
data_split = int(data.shape[0] * (1/cv))
```
이 방식은 `n_samples`가 `cv`로 안 나누어떨어지면 **끝 자투리 샘플이 누락**될 수 있습니다.

실전에서는 `KFold`나 `StratifiedKFold`를 쓰는 게 낫습니다. scikit-learn도 `cv`는 이런 splitter와 연동합니다. citeturn254543search0

---

### 4) 지금 best score 선정 방식이 “fold 하나” 기준
현재는 각 fold, 각 파라미터 조합마다 점수를 구하고, **그 순간 최고값 하나**만 기록합니다.

즉,
- `(C=1, gamma=0.1)`의 5개 fold 평균
- `(C=10, gamma=0.01)`의 5개 fold 평균

을 비교하는 게 아니라,  
**모든 실험 중 우연히 한 fold에서 가장 높았던 값 하나**를 뽑고 있어요.

진짜 `GridSearchCV`처럼 하려면 **각 파라미터 조합마다 fold 평균 점수**를 계산해서 그 평균으로 best를 정해야 합니다. `GridSearchCV`도 기본적으로 CV 점수를 집계해서 최적 조합을 고릅니다. citeturn254543search0

---

### 5) confusion matrix 기반 지표 계산은 직접 해도 되지만 리스크 있음
이진분류라면 지금 방식도 가능하지만, 직접 `tp/fp/fn` 꺼내는 건
- 클래스 순서 바뀜
- 다중분류 확장 어려움
- 0으로 나누기 예외

같은 문제가 생깁니다.

`precision_score`, `recall_score`, `f1_score`, `classification_report(..., output_dict=True)`를 쓰는 쪽이 훨씬 안전합니다.

---

## 권장 구조

진짜처럼 가려면 입력을 이렇게 분리하세요.

### 함수 시그니처
```python
my_grid_search_cv(estimator, param_grid, X, y, cv=5, scoring=None)
```

- `estimator`: `SVC()`, `RandomForestClassifier()` 등
- `param_grid`: `{'C':[0.1,1,10], 'gamma':[0.01,0.1]}`
- `X`, `y`: feature / target 분리
- `cv`: 정수 또는 splitter
- `scoring`: 점수 함수

---

## 가장 먼저 추천하는 최소 구현 버전

아래처럼 짜면 **모듈화 + import + 재사용**이 쉬워집니다.

### `my_grid_search.py`
```python
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold


def make_param_combinations(param_grid: dict):
    keys = list(param_grid.keys())
    values = [param_grid[k] for k in keys]
    for combo in itertools.product(*values):
        yield dict(zip(keys, combo))


def default_scoring(y_true, y_pred):
    """
    binary classification 기준:
    클래스 0, 1의 precision / recall 평균 합산 점수
    필요하면 사용자가 다른 scoring 함수로 교체 가능
    """
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

    tp0 = cm[0, 0]
    fp0 = cm[1, 0]
    fn0 = cm[0, 1]

    tp1 = cm[1, 1]
    fp1 = cm[0, 1]
    fn1 = cm[1, 0]

    def safe_div(a, b):
        return a / b if b != 0 else 0.0

    pre0 = safe_div(tp0, tp0 + fp0)
    rec0 = safe_div(tp0, tp0 + fn0)
    pre1 = safe_div(tp1, tp1 + fp1)
    rec1 = safe_div(tp1, tp1 + fn1)

    score = pre0 + rec0 + pre1 + rec1

    return score, {
        "pre0": pre0,
        "rec0": rec0,
        "pre1": pre1,
        "rec1": rec1,
        "confusion_matrix": cm.tolist(),
    }


class MyGridSearchCV:
    def __init__(self, estimator, param_grid, cv=5, scoring=None, random_state=42):
        self.estimator = estimator
        self.param_grid = param_grid
        self.cv = cv
        self.scoring = scoring if scoring is not None else default_scoring
        self.random_state = random_state

        self.best_params_ = None
        self.best_score_ = None
        self.best_estimator_ = None
        self.best_report_ = None
        self.cv_results_ = []

    def fit(self, X, y, report_path=None):
        skf = StratifiedKFold(
            n_splits=self.cv,
            shuffle=True,
            random_state=self.random_state
        )

        best_mean_score = -np.inf
        best_params = None
        best_fold_report = None

        all_logs = []

        for params in make_param_combinations(self.param_grid):
            fold_scores = []
            fold_details = []

            for fold_idx, (train_idx, valid_idx) in enumerate(skf.split(X, y), start=1):
                X_train, X_valid = X.iloc[train_idx], X.iloc[valid_idx]
                y_train, y_valid = y.iloc[train_idx], y.iloc[valid_idx]

                model = clone(self.estimator)
                model.set_params(**params)
                model.fit(X_train, y_train)

                pred = model.predict(X_valid)

                score, detail = self.scoring(y_valid, pred)
                report_dict = classification_report(y_valid, pred, output_dict=True, zero_division=0)
                report_text = classification_report(y_valid, pred, zero_division=0)

                fold_scores.append(score)
                fold_details.append({
                    "fold": fold_idx,
                    "score": score,
                    "detail": detail,
                    "classification_report": report_dict,
                })

                all_logs.append({
                    "params": params,
                    "fold": fold_idx,
                    "score": score,
                    "confusion_matrix": detail["confusion_matrix"],
                    "classification_report_text": report_text,
                })

            mean_score = float(np.mean(fold_scores))

            self.cv_results_.append({
                "params": params,
                "mean_test_score": mean_score,
                "fold_scores": fold_scores,
                "fold_details": fold_details,
            })

            if mean_score > best_mean_score:
                best_mean_score = mean_score
                best_params = params
                best_fold_report = fold_details

        self.best_score_ = best_mean_score
        self.best_params_ = best_params

        self.best_estimator_ = clone(self.estimator)
        self.best_estimator_.set_params(**self.best_params_)
        self.best_estimator_.fit(X, y)

        self.best_report_ = best_fold_report

        if report_path is not None:
            report_path = Path(report_path)
            report_path.parent.mkdir(parents=True, exist_ok=True)

            with open(report_path, "w", encoding="utf-8") as f:
                f.write("=== BEST RESULT ===\n")
                f.write(f"best_params: {self.best_params_}\n")
                f.write(f"best_score: {self.best_score_}\n\n")
                f.write("=== CV RESULTS ===\n")
                json.dump(self.cv_results_, f, ensure_ascii=False, indent=2)

        return self

    def predict(self, X):
        return self.best_estimator_.predict(X)
```

---

## `main.py`에서 쓰는 방법

```python
import pandas as pd
from sklearn.svm import SVC
from my_grid_search import MyGridSearchCV

df = pd.read_csv("your_data.csv")

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

param_grid = {
    "C": [0.1, 1, 10],
    "gamma": [0.001, 0.01, 0.1]
}

search = MyGridSearchCV(
    estimator=SVC(),
    param_grid=param_grid,
    cv=5
)

search.fit(X, y, report_path="res_report.json")

print("best_params_ =", search.best_params_)
print("best_score_ =", search.best_score_)
print("best_estimator_ =", search.best_estimator_)
```

이렇게 하면 `main.py`에서 **모델 객체를 생성해서 넣는 방식**이 자연스럽게 됩니다.

---

## 왜 클래스 형태가 더 좋은가

`GridSearchCV`가 클래스인 이유가 있어요.

왜냐하면 학습 후에 이런 결과를 속성으로 남기기 좋거든요.

- `best_params_`
- `best_score_`
- `best_estimator_`
- `cv_results_`

이 인터페이스가 scikit-learn estimator 스타일과도 잘 맞습니다. scikit-learn 용어집에서도 **생성자 파라미터는 그대로 저장하고, 학습 후 산출물은 보통 `_`가 붙은 public attribute로 둔다**고 설명합니다. citeturn254543search4

---

## “리포트 저장”을 어떻게 설계하면 좋은가

지금은 텍스트 파일에 계속 append하고 있는데, 나중에 분석하기는 불편합니다.

더 좋은 방법은:

- **원본 로그는 JSON**
- 사람이 읽기 쉬운 최종 요약은 TXT

이렇게 나누는 겁니다.

예를 들면:

### `cv_results_.append(...)`에 저장할 것
- params
- fold별 score
- mean score
- confusion matrix
- classification report dict

### 최종 txt 보고서
- 최적 파라미터
- 최적 평균 점수
- fold별 요약
- 전체 데이터로 refit한 모델 정보

---

## scoring도 외부 주입 가능하게 만들어야 함

진짜 `GridSearchCV`는 `scoring`을 받을 수 있어요. citeturn254543search0

그래서 당신 것도 이렇게 만드는 게 좋아요.

```python
search = MyGridSearchCV(
    estimator=SVC(),
    param_grid=param_grid,
    cv=5,
    scoring=my_custom_score
)
```

예시:

```python
def my_custom_score(y_true, y_pred):
    from sklearn.metrics import f1_score, confusion_matrix, classification_report
    score = f1_score(y_true, y_pred, average="macro")
    detail = {
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "classification_report": classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    }
    return score, detail
```

이렇게 하면 당신이 원하는 **confusion matrix + classification report 기반 보고서형 탐색기**가 됩니다.

---

## 진짜 sklearn스럽게 더 가고 싶다면

한 단계 더 가려면 `BaseEstimator`를 상속받는 방법도 있습니다. scikit-learn 메타 estimator들은 estimator 인터페이스를 따르고, `fit`, `predict`, `score` 같은 메서드를 제공합니다. citeturn254543search0turn254543search4

예를 들면:

```python
from sklearn.base import BaseEstimator

class MyGridSearchCV(BaseEstimator):
    ...
```

다만 처음 구현이면 꼭 상속까지는 안 해도 됩니다.  
우선은 **동작 구조를 올바르게 만드는 것**이 먼저예요.

---

## 당신 코드 기준으로 꼭 바꿔야 할 핵심 요약

### 지금 방식
- 데이터프레임 하나를 넣고 마지막 열을 target으로 가정
- 함수 내부에서 `SVC` 생성
- fold 하나에서 가장 잘 나온 점수 기록

### 추천 방식
- `X`, `y`를 분리해서 받기
- `estimator`를 인자로 받기
- 각 파라미터 조합마다 `clone(estimator)` 후 `set_params`
- 각 조합에 대해 **cv 평균 점수** 계산
- best 조합으로 전체 데이터 재학습하여 `best_estimator_` 저장
- `best_params_`, `best_score_`, `cv_results_`, `best_report_` 속성화

---

## 아주 짧게 말하면

당신이 원하는 건 사실상 이런 구조예요.

```python
search = MyGridSearchCV(SVC(), param_grid, cv=5)
search.fit(X, y)

print(search.best_params_)
print(search.best_score_)
```

그리고 내부 구현의 핵심은 이것입니다.

```python
model = clone(estimator)
model.set_params(**params)
model.fit(X_train, y_train)
```

이 패턴이 있어야 **모듈화**, **import**, **재사용**, **모델 교체**가 전부 쉬워집니다. `GridSearchCV`가 estimator와 parameter grid를 받아 exhaustive search를 수행하는 것도 같은 방향입니다. citeturn254543search0turn254543search5turn254543search9

원하면 다음 답변에서 내가 네 기존 코드를 최대한 유지하면서 **함수형 버전**과 **클래스형 버전** 두 가지로 각각 리팩토링해줄게.

---
