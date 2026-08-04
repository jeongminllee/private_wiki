---
type: Error Note
title: "AutoGluon 리포트 저장 방법"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-06-14)"
tags: [errors, chatgpt-export]
timestamp: 2026-06-14
status: active
---

# AutoGluon 리포트 저장 방법

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-14

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
AutoGluon 쪽은 버전별로 문서 구조가 조금씩 바뀌어서, 공식 문서 기준으로 “리포트/진단 결과를 어디서 뽑는지”를 확인해서 정리해볼게요. 핵심은 AutoGluon에 별도 “Report Generator” 메뉴가 있는지보다, 학습 결과를 저장하는 API와 HTML/PDF 리포트에 가까운 진단 기능이 어디 있는지입니다.

---

### ❓ 질문 (User)
아마존에서 개발한 AutoGluon을 활용할 생각이야. 근데 여기서 내가 원하는건 모델링도 모델링인데 리포트를 저장해서 가지고 있고 싶어. 다른 모델들은 보니까 report generator 가 있던데 AutoGluon 에는 안보여서 말이야. https://auto.gluon.ai/stable/index.html
여기 가서 report 를 얻으려면 어떻게 해야 하는지, 어느 부분에 들어가서 확인이 가능한지에 대해서 알려줘.

### 💡 답변 (Assistant)
결론부터 말하면 **AutoGluon Tabular에는 H2O AutoML 같은 “원클릭 HTML report generator”가 기본 메인 기능으로 보이진 않습니다.** 대신 공식적으로는 아래 기능들을 조합해서 리포트를 저장하는 방식이 맞습니다.

## 어디서 확인하면 되나?

공식 문서에서 이 경로로 보면 됩니다.

**AutoGluon Docs → Tabular Prediction → API Reference → `TabularPredictor`**

여기서 특히 봐야 할 항목은 4개입니다.

1. **`TabularPredictor.fit_summary()`**  
   학습 후 전체 요약을 출력하고, `verbosity > 1`이면 요약 plot을 생성해서 `predictor.path` 폴더에 저장할 수 있습니다. 반환값은 `dict`입니다. 공식 문서에도 “fit()으로 생성된 모델들의 summary를 출력하고, summary plot을 `predictor.path` 폴더에 저장할 수 있다”고 되어 있습니다. citeturn319521view0

2. **`TabularPredictor.leaderboard()`**  
   학습된 모델별 성능표를 `pandas.DataFrame`으로 반환합니다. validation/test score, 학습 시간, 추론 시간, stack level 등이 들어갑니다. citeturn319521view1

3. **`TabularPredictor.feature_importance()`**  
   feature importance를 `DataFrame`으로 반환합니다. permutation importance 기반이고, 어떤 feature를 섞었을 때 성능이 얼마나 떨어지는지를 기준으로 중요도를 계산합니다. citeturn319521view2

4. **`log_to_file=True` / `load_log()`**  
   `TabularPredictor` 생성 시 `log_to_file=True`를 주면 학습 로그를 파일로 저장할 수 있습니다. `log_file_path="auto"`이면 기본적으로 `predictor_path/logs/predictor_log.txt`에 저장됩니다. citeturn582042search0turn582042search5

---

## 가장 실용적인 사용 방식

```python
from autogluon.tabular import TabularPredictor
from pathlib import Path
import json

label = "target"
save_path = "ag_models/my_experiment"

predictor = TabularPredictor(
    label=label,
    path=save_path,
    eval_metric="accuracy",      # 회귀면 "root_mean_squared_error", "r2" 등
    log_to_file=True,
    verbosity=3,
).fit(
    train_data,
    presets="good_quality",
    time_limit=600,
)
```

여기서 중요한 건 `path=save_path`입니다. AutoGluon은 predictor, 모델 파일, 로그, summary plot 등을 이 폴더 아래에 저장합니다. 공식 문서상 `path`를 지정하지 않으면 `AutogluonModels/ag-[TIMESTAMP]` 형태의 폴더가 자동 생성됩니다. 같은 path로 다시 fit하면 이전 결과가 덮어써질 수 있으니 실험마다 다른 path를 쓰는 게 좋습니다. citeturn319521view4

---

## 리포트용 결과 저장 코드

```python
report_dir = Path(save_path) / "report"
report_dir.mkdir(parents=True, exist_ok=True)

# 1. fit summary
fit_summary = predictor.fit_summary(verbosity=3, show_plot=False)

with open(report_dir / "fit_summary.json", "w", encoding="utf-8") as f:
    json.dump(fit_summary, f, ensure_ascii=False, indent=2, default=str)

# 2. leaderboard
leaderboard = predictor.leaderboard(test_data, extra_info=True)
leaderboard.to_csv(report_dir / "leaderboard.csv", index=False)

# 3. feature importance
feature_importance = predictor.feature_importance(test_data)
feature_importance.to_csv(report_dir / "feature_importance.csv")

# 4. evaluation
evaluation = predictor.evaluate(test_data)

with open(report_dir / "evaluation.json", "w", encoding="utf-8") as f:
    json.dump(evaluation, f, ensure_ascii=False, indent=2, default=str)

# 5. training log
logs = TabularPredictor.load_log(predictor_path=save_path)

with open(report_dir / "training_log.txt", "w", encoding="utf-8") as f:
    f.writelines(logs)
```

이렇게 하면 최소한 아래 파일들이 생깁니다.

```text
ag_models/my_experiment/
├── models/
├── logs/
│   └── predictor_log.txt
├── predictor.pkl
└── report/
    ├── fit_summary.json
    ├── leaderboard.csv
    ├── feature_importance.csv
    ├── evaluation.json
    └── training_log.txt
```

---

## HTML 리포트처럼 만들고 싶으면?

AutoGluon 자체에서 “완성된 HTML report”를 바로 만들어주는 기능보다는, 위 결과들을 모아서 직접 HTML/Markdown으로 저장하는 방식이 깔끔합니다.

```python
html = f"""
<h1>AutoGluon Training Report</h1>

<h2>Best Model</h2>
<p>{predictor.model_best}</p>

<h2>Evaluation</h2>
<pre>{evaluation}</pre>

<h2>Leaderboard</h2>
{leaderboard.to_html(index=False)}

<h2>Feature Importance</h2>
{feature_importance.to_html()}
"""

with open(report_dir / "report.html", "w", encoding="utf-8") as f:
    f.write(html)
```

이러면 브라우저로 열 수 있는 `report.html`이 생깁니다.

---

## 주의할 점

`presets="optimize_for_deployment"`를 쓰면 리포트용 정보가 줄어듭니다. 공식 문서에 따르면 이 preset은 사용하지 않는 모델과 학습 산출물을 삭제해서 디스크 사용량을 줄이지만, 그 결과 `leaderboard()`와 `fit_summary()`가 덜 informative해질 수 있습니다. 즉, **리포트를 남기는 목적이면 처음 학습할 때는 `optimize_for_deployment`를 피하는 게 좋습니다.** citeturn319521view5

추천 흐름은 이겁니다.

```python
# 1단계: 분석/리포트용 학습
predictor = TabularPredictor(
    label=label,
    path="ag_models/exp_001",
    log_to_file=True,
).fit(train_data, presets="good_quality")

# 2단계: 리포트 저장
# leaderboard, fit_summary, feature_importance 저장

# 3단계: 배포용 복사본 따로 최적화
# 원본은 보존하고, 배포용만 save_space/delete_models 적용
```

정리하면, AutoGluon에서 “report”를 찾으려면 문서상 `Report Generator`가 아니라 **`TabularPredictor.fit_summary`, `leaderboard`, `feature_importance`, `load_log`, `path/logs`** 쪽을 봐야 합니다. 리포트 파일로 보관하려면 이 결과들을 `csv/json/html/txt`로 직접 저장하는 방식이 가장 안정적입니다.

---

### 💡 답변 (Assistant)
네, **방향은 맞습니다.** 지금 코드대로 작성하면 `report/` 폴더에 아래 파일들이 저장되고, 마지막에 `report.html`도 생성됩니다.

```text
report/
├── fit_summary.json
├── leaderboard.csv
├── feature_importance.csv
├── evaluation.json
├── training_log.txt
└── report.html
```

다만 실전에서는 몇 가지를 조금 보완하는 게 좋습니다.

## 1. 필요한 import가 있어야 함

맨 위에 이건 있어야 합니다.

```python
from pathlib import Path
import json
from autogluon.tabular import TabularPredictor
```

## 2. `save_path`는 predictor 학습할 때 쓴 `path`와 같아야 함

예를 들어 학습을 이렇게 했다면,

```python
save_path = "ag_models/my_experiment"

predictor = TabularPredictor(
    label="target",
    path=save_path,
    log_to_file=True,
).fit(train_data)
```

리포트 만들 때도 같은 `save_path`를 써야 합니다.

```python
report_dir = Path(save_path) / "report"
```

## 3. 지금 코드에서 제일 주의할 부분

이 부분입니다.

```python
feature_importance = predictor.feature_importance(test_data)
```

`feature_importance()`는 permutation importance라서 **데이터를 실제로 여러 번 예측해보면서 계산**합니다. 그래서 데이터가 크면 시간이 꽤 걸릴 수 있습니다.

처음에는 이렇게 일부 샘플만 넣어도 됩니다.

```python
feature_importance = predictor.feature_importance(test_data.sample(1000, random_state=42))
```

또는 데이터가 작으면 그대로 써도 됩니다.

## 4. `leaderboard(test_data, extra_info=True)`도 좋음

이건 리포트에 아주 유용합니다.

```python
leaderboard = predictor.leaderboard(test_data, extra_info=True)
```

`extra_info=True`를 쓰면 모델별 학습 시간, 예측 시간, stack level, ancestor/descendant 정보 등이 더 들어가서 리포트용으로 좋습니다.

## 5. 조금 더 정리한 최종 코드

아래처럼 함수로 만들어두는 걸 추천합니다.

```python
from pathlib import Path
import json
from autogluon.tabular import TabularPredictor


def save_autogluon_html_report(
    predictor,
    test_data,
    save_path,
    report_name="report.html",
    feature_importance_sample_size=1000,
):
    report_dir = Path(save_path) / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    # 1. fit summary
    fit_summary = predictor.fit_summary(verbosity=3, show_plot=False)

    with open(report_dir / "fit_summary.json", "w", encoding="utf-8") as f:
        json.dump(fit_summary, f, ensure_ascii=False, indent=2, default=str)

    # 2. leaderboard
    leaderboard = predictor.leaderboard(test_data, extra_info=True)
    leaderboard.to_csv(report_dir / "leaderboard.csv", index=False)

    # 3. feature importance
    if len(test_data) > feature_importance_sample_size:
        fi_data = test_data.sample(feature_importance_sample_size, random_state=42)
    else:
        fi_data = test_data

    feature_importance = predictor.feature_importance(fi_data)
    feature_importance.to_csv(report_dir / "feature_importance.csv")

    # 4. evaluation
    evaluation = predictor.evaluate(test_data)

    with open(report_dir / "evaluation.json", "w", encoding="utf-8") as f:
        json.dump(evaluation, f, ensure_ascii=False, indent=2, default=str)

    # 5. training log
    logs = TabularPredictor.load_log(predictor_path=save_path)

    with open(report_dir / "training_log.txt", "w", encoding="utf-8") as f:
        f.writelines(logs)

    # 6. HTML report
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>AutoGluon Training Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }}
            h1, h2 {{
                color: #333;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 30px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            pre {{
                background-color: #f8f8f8;
                padding: 15px;
                border: 1px solid #ddd;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <h1>AutoGluon Training Report</h1>

        <h2>Best Model</h2>
        <p>{predictor.model_best}</p>

        <h2>Evaluation</h2>
        <pre>{json.dumps(evaluation, ensure_ascii=False, indent=2, default=str)}</pre>

        <h2>Leaderboard</h2>
        {leaderboard.to_html(index=False)}

        <h2>Feature Importance</h2>
        {feature_importance.to_html()}

        <h2>Saved Files</h2>
        <ul>
            <li>fit_summary.json</li>
            <li>leaderboard.csv</li>
            <li>feature_importance.csv</li>
            <li>evaluation.json</li>
            <li>training_log.txt</li>
        </ul>
    </body>
    </html>
    """

    report_path = report_dir / report_name

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    return report_path
```

사용은 이렇게 하면 됩니다.

```python
report_path = save_autogluon_html_report(
    predictor=predictor,
    test_data=test_data,
    save_path=save_path,
)

print(f"Report saved to: {report_path}")
```

## 정리하면

네, 지금 작성한 코드로도 됩니다.  
다만 더 안정적으로 쓰려면:

```python
feature_importance()`는 샘플링해서 계산
HTML에는 CSS 조금 추가
전체 코드는 함수로 묶기
```

이렇게 바꾸는 게 좋습니다.

실전에서는 학습이 끝난 직후에 아래 한 줄만 실행하는 구조가 가장 깔끔합니다.

```python
save_autogluon_html_report(predictor, test_data, save_path)
```

---

### ❓ 질문 (User)
그러면 html 리포트처럼 만들고 싶다고 하면, 
```
report_dir = Path(save_path) / "report"
report_dir.mkdir(parents=True, exist_ok=True)

# 1. fit summary
fit_summary = predictor.fit_summary(verbosity=3, show_plot=False)

with open(report_dir / "fit_summary.json", "w", encoding="utf-8") as f:
    json.dump(fit_summary, f, ensure_ascii=False, indent=2, default=str)

# 2. leaderboard
leaderboard = predictor.leaderboard(test_data, extra_info=True)
leaderboard.to_csv(report_dir / "leaderboard.csv", index=False)

# 3. feature importance
feature_importance = predictor.feature_importance(test_data)
feature_importance.to_csv(report_dir / "feature_importance.csv")

# 4. evaluation
evaluation = predictor.evaluate(test_data)

with open(report_dir / "evaluation.json", "w", encoding="utf-8") as f:
    json.dump(evaluation, f, ensure_ascii=False, indent=2, default=str)

# 5. training log
logs = TabularPredictor.load_log(predictor_path=save_path)

with open(report_dir / "training_log.txt", "w", encoding="utf-8") as f:
    f.writelines(logs)
html = f"""
<h1>AutoGluon Training Report</h1>

<h2>Best Model</h2>
<p>{predictor.model_best}</p>

<h2>Evaluation</h2>
<pre>{evaluation}</pre>

<h2>Leaderboard</h2>
{leaderboard.to_html(index=False)}

<h2>Feature Importance</h2>
{feature_importance.to_html()}
"""

with open(report_dir / "report.html", "w", encoding="utf-8") as f:
    f.write(html)
```
이렇게 작성하면 되는건가??

### 💡 답변 (Assistant)
아래처럼 **리포트 생성 전용 함수**로 분리해서 쓰면 깔끔합니다.  
학습이 끝난 뒤 `save_autogluon_html_report(...)`만 호출하면 `csv/json/txt/html` 리포트가 한 번에 저장됩니다.

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from autogluon.tabular import TabularPredictor


def save_json(data: Any, path: Path) -> None:
    """Python 객체를 JSON 파일로 저장한다."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def save_text(lines: list[str], path: Path) -> None:
    """문자열 리스트를 텍스트 파일로 저장한다."""
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def sample_dataframe(
    df: pd.DataFrame,
    sample_size: int | None = 1000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    feature importance 계산용 샘플 데이터를 만든다.

    AutoGluon feature_importance는 permutation importance 방식이라
    데이터가 크면 시간이 오래 걸릴 수 있다.
    """
    if sample_size is None:
        return df

    if len(df) <= sample_size:
        return df

    return df.sample(n=sample_size, random_state=random_state)


def build_html_report(
    predictor: TabularPredictor,
    evaluation: dict[str, Any],
    leaderboard: pd.DataFrame,
    feature_importance: pd.DataFrame,
) -> str:
    """AutoGluon 학습 결과를 HTML 문자열로 변환한다."""
    evaluation_json: str = json.dumps(
        evaluation,
        ensure_ascii=False,
        indent=2,
        default=str,
    )

    best_model: str | None = predictor.model_best

    html: str = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>AutoGluon Training Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #222;
        }}

        h1 {{
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}

        h2 {{
            margin-top: 40px;
            color: #333;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
            margin-bottom: 30px;
            font-size: 14px;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}

        th {{
            background-color: #f2f2f2;
        }}

        tr:nth-child(even) {{
            background-color: #fafafa;
        }}

        pre {{
            background-color: #f8f8f8;
            padding: 15px;
            border: 1px solid #ddd;
            overflow-x: auto;
        }}

        .summary-box {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            padding: 15px;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <h1>AutoGluon Training Report</h1>

    <h2>Best Model</h2>
    <div class="summary-box">
        <strong>{best_model}</strong>
    </div>

    <h2>Evaluation</h2>
    <pre>{evaluation_json}</pre>

    <h2>Leaderboard</h2>
    {leaderboard.to_html(index=False)}

    <h2>Feature Importance</h2>
    {feature_importance.to_html()}

    <h2>Saved Files</h2>
    <ul>
        <li>fit_summary.json</li>
        <li>leaderboard.csv</li>
        <li>feature_importance.csv</li>
        <li>evaluation.json</li>
        <li>training_log.txt</li>
        <li>report.html</li>
    </ul>
</body>
</html>
"""
    return html


def save_autogluon_html_report(
    predictor: TabularPredictor,
    test_data: pd.DataFrame,
    save_path: str | Path,
    report_dir_name: str = "report",
    report_file_name: str = "report.html",
    feature_importance_sample_size: int | None = 1000,
    random_state: int = 42,
) -> Path:
    """
    AutoGluon TabularPredictor 학습 결과를 리포트 파일로 저장한다.

    저장 파일:
        - fit_summary.json
        - leaderboard.csv
        - feature_importance.csv
        - evaluation.json
        - training_log.txt
        - report.html

    Args:
        predictor:
            학습이 완료된 AutoGluon TabularPredictor 객체.

        test_data:
            평가용 데이터프레임.
            label column이 포함되어 있어야 evaluate, leaderboard 계산이 가능하다.

        save_path:
            predictor 학습 시 사용한 path.
            예: "ag_models/my_experiment"

        report_dir_name:
            리포트 저장 폴더명.

        report_file_name:
            HTML 리포트 파일명.

        feature_importance_sample_size:
            feature importance 계산에 사용할 샘플 개수.
            None이면 전체 test_data를 사용한다.

        random_state:
            샘플링 재현성을 위한 seed.

    Returns:
        생성된 HTML 리포트 파일 경로.
    """
    predictor_path: Path = Path(save_path)
    report_dir: Path = predictor_path / report_dir_name
    report_dir.mkdir(parents=True, exist_ok=True)

    # 1. Fit summary
    fit_summary: dict[str, Any] = predictor.fit_summary(
        verbosity=3,
        show_plot=False,
    )
    save_json(fit_summary, report_dir / "fit_summary.json")

    # 2. Leaderboard
    leaderboard: pd.DataFrame = predictor.leaderboard(
        data=test_data,
        extra_info=True,
    )
    leaderboard.to_csv(
        report_dir / "leaderboard.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # 3. Feature importance
    feature_importance_data: pd.DataFrame = sample_dataframe(
        df=test_data,
        sample_size=feature_importance_sample_size,
        random_state=random_state,
    )

    feature_importance: pd.DataFrame = predictor.feature_importance(
        data=feature_importance_data,
    )
    feature_importance.to_csv(
        report_dir / "feature_importance.csv",
        encoding="utf-8-sig",
    )

    # 4. Evaluation
    evaluation: dict[str, Any] = predictor.evaluate(data=test_data)
    save_json(evaluation, report_dir / "evaluation.json")

    # 5. Training log
    logs: list[str] = TabularPredictor.load_log(
        predictor_path=str(predictor_path),
    )
    save_text(logs, report_dir / "training_log.txt")

    # 6. HTML report
    html: str = build_html_report(
        predictor=predictor,
        evaluation=evaluation,
        leaderboard=leaderboard,
        feature_importance=feature_importance,
    )

    report_path: Path = report_dir / report_file_name

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    return report_path
```

사용 예시는 이렇게 하면 됩니다.

```python
from autogluon.tabular import TabularPredictor

label: str = "target"
save_path: str = "ag_models/my_experiment"

predictor: TabularPredictor = TabularPredictor(
    label=label,
    path=save_path,
    eval_metric="accuracy",
    log_to_file=True,
    verbosity=3,
).fit(
    train_data=train_data,
    presets="good_quality",
    time_limit=600,
)

report_path: Path = save_autogluon_html_report(
    predictor=predictor,
    test_data=test_data,
    save_path=save_path,
    feature_importance_sample_size=1000,
)

print(f"Report saved to: {report_path}")
```

생성 결과는 이런 구조가 됩니다.

```text
ag_models/my_experiment/
├── models/
├── logs/
│   └── predictor_log.txt
├── predictor.pkl
└── report/
    ├── fit_summary.json
    ├── leaderboard.csv
    ├── feature_importance.csv
    ├── evaluation.json
    ├── training_log.txt
    └── report.html
```

핵심은 이 부분입니다.

```python
report_path: Path = save_autogluon_html_report(
    predictor=predictor,
    test_data=test_data,
    save_path=save_path,
)
```

학습이 끝난 뒤 이 함수만 실행하면, 브라우저에서 열 수 있는 `report.html`까지 같이 생성됩니다.

---

### ❓ 질문 (User)
전체 코드를 깔끔하게 작성해줘. 작성할때, 타입 어노테이션 을 포함해야해.
