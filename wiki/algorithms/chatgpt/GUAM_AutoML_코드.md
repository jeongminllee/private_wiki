---
type: Concept
title: "GUAM AutoML 코드"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-06-17)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-06-17
status: active
---

# GUAM AutoML 코드

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-17

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
# %% [code]
"""GUAM AutoML — S6E6, RealMLP(NN) + XGB 다양성 블렌드 (리더보드 1위 레시피).

리더보드 1위(0.9697) = RealMLP + XGB + CatBoost 블렌드. GUAM 으로 재현:
  - NNGPU(RealMLP-lite): 범주 임베딩 + PBLD + robust + NTP (OOF 0.959 단독)
  - BoostXGB: TargetEncoder + balanced (LB 0.96613 단독)
  - 동일 stratified fold → WeightedBlender(balanced accuracy) 로 결합.
다른 모델군이라 블렌드가 단독을 능가할 것으로 기대.

FE: arithmetic·colors(numeric) · num→cat·interaction·orig cats(NN 임베딩 코드)
    · TargetEncoder one-vs-rest(XGB numeric). 전부 GPU.
푸시: kaggle kernels push -p references/허성/kaggle-s6e6-automl
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, List

import numpy as np

WORK = Path("/kaggle/working")
N_FOLDS = 5
TARGET = "class"


def sh(cmd: str, cwd: str | None = None) -> None:
    print(f"\n$ {cmd}", flush=True)
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def section(title: str) -> None:
    print(f"\n{'─' * 60}\n◆ {title}\n{'─' * 60}", flush=True)


sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
import cudf  # noqa: E402
import cupy as cp  # noqa: E402

INPUT = Path("/kaggle/input")
src_root = sorted(INPUT.rglob("pyproject.toml"))[0].parent
repo = WORK / "GUAM"
if not repo.exists():
    shutil.copytree(src_root, repo)
sh("pip install -e ./GUAM -q", cwd=str(WORK))
sys.path.insert(0, str(repo))

import guam  # noqa: E402
from guam.automl.blend import WeightedBlender  # noqa: E402
from guam.ml_algo.boost_xgb import BoostXGB  # noqa: E402
from guam.ml_algo.nn import NNGPU  # noqa: E402
from guam.validation.base import CustomIterator  # noqa: E402


def balanced_accuracy(target: Any, pred_2d: Any) -> float:
    y = cp.asarray(target).reshape(-1).astype("int64")
    p = cp.argmax(cp.asarray(pred_2d), axis=1).astype("int64")
    u = cp.unique(y)
    return sum(float((p[y == c] == c).mean()) for c in u.tolist()) / int(u.shape[0])


def stratified_fold_ids(target: Any, n_folds: int) -> np.ndarray:
    from sklearn.model_selection import StratifiedKFold

    y = cp.asnumpy(cp.asarray(target))
    ids = np.empty(len(y), dtype="int32")
    for f, (_, val) in enumerate(
        StratifiedKFold(n_folds, shuffle=True, random_state=42).split(y, y)
    ):
        ids[val] = f
    return ids


def enc(train: cudf.DataFrame, test: cudf.DataFrame, col: str) -> None:
    n = len(train)
    codes = (
        cudf.concat([train[col], test[col]], ignore_index=True)
        .astype("category")
        .cat.codes.astype("int32")
    )
    train[col] = codes.iloc[:n].reset_index(drop=True)
    test[col] = codes.iloc[n:].reset_index(drop=True)


# ── FE ──────────────────────────────────────────────────────────
section("FE: arithmetic·colors + cat codes(NN) + TargetEncoder(XGB)")
COMP = next(INPUT.rglob("train.csv")).parent
train, test = guam.read(COMP / "train.csv"), guam.read(COMP / "test.csv")
label_src = train[TARGET].copy()
bands = ["u", "g", "r", "i", "z"]
orig_num = ["alpha", "delta", *bands, "redshift"]
cat_codes: List[str] = []

for df in (train, test):
    df["g_rs"] = (df["g"] / (df["redshift"] + 1e-6)).astype("float32")
    df["i_rs"] = (df["i"] / (df["redshift"] + 1e-6)).astype("float32")
    df["dist_mod"] = (6.0 * cp.log10(cp.abs(df["redshift"].to_cupy()) + 1e-6)).astype(
        "float32"
    )
    for a, b in [("u", "g"), ("g", "r"), ("i", "z"), ("r", "z"), ("u", "z")]:
        df[f"c_{a}_{b}"] = (df[a] - df[b]).astype("float32")

orig_cats = [c for c in test.columns if train[c].dtype == "object" and c != TARGET]
for col in orig_num:
    train[f"{col}_cat"] = cp.floor(train[col].to_cupy())
    test[f"{col}_cat"] = cp.floor(test[col].to_cupy())
    enc(train, test, f"{col}_cat")
    cat_codes.append(f"{col}_cat")
for col in orig_cats:
    enc(train, test, col)
    cat_codes.append(col)
for a, b in [("alpha_cat", "delta_cat"), ("u_cat", "z_cat")]:
    name = f"x_{a}_{b}"
    train[name] = train[a].astype("str") + "_" + train[b].astype("str")
    test[name] = test[a].astype("str") + "_" + test[b].astype("str")
    enc(train, test, name)
    cat_codes.append(name)

# TargetEncoder one-vs-rest (XGB 용 numeric) — orig cats 대상
target_codes = label_src.astype("category").cat.codes.astype("int32")
n_classes = int(target_codes.max()) + 1
fold_ids = stratified_fold_ids(target_codes, N_FOLDS)
from cuml.preprocessing import TargetEncoder  # noqa: E402

te_cols: List[str] = []
for k in range(n_classes - 1):
    y_bin = (target_codes == k).astype("float32")
    for col in orig_cats:
        try:
            te = TargetEncoder(
                n_folds=N_FOLDS, smooth=20, split_method="customize", output_type="cupy"
            )
            tr = te.fit_transform(train[col], y_bin, fold_ids=cp.asarray(fold_ids))
        except Exception:  # noqa: BLE001
            te = TargetEncoder(n_folds=N_FOLDS, smooth=20, output_type="cupy")
            tr = te.fit_transform(train[col], y_bin)
        train[f"te_{col}_{k}"] = cudf.Series(cp.asarray(tr).reshape(-1))
        test[f"te_{col}_{k}"] = cudf.Series(
            cp.asarray(te.transform(test[col])).reshape(-1)
        )
        te_cols.append(f"te_{col}_{k}")

train[TARGET] = label_src
print(f"train {train.shape} | cat codes(NN) {len(cat_codes)} | TE(XGB) {len(te_cols)}")

# ── Dataset + 매핑 ──────────────────────────────────────────────
reader = guam.CudfReader(task="multiclass")
train_ds, test_ds = reader.fit_read(train, target=TARGET, drop=["id"]), None
test_ds = reader.read(test)
pair = cudf.DataFrame(
    {"code": cudf.Series(train_ds.target), "label": label_src.reset_index(drop=True)}
)
uniq = pair.drop_duplicates(subset="code").sort_values("code")
code_to_label = dict(
    zip(uniq["code"].to_arrow().to_pylist(), uniq["label"].to_arrow().to_pylist())
)
iterator = CustomIterator(train_ds, folds=fold_ids.tolist())

# ── NN(RealMLP) + XGB(TE) OOF ───────────────────────────────────
section(f"NNGPU(RealMLP) + BoostXGB · {N_FOLDS}-fold")
oof_list: List[Any] = []
algos: List[Any] = []
builders = [
    (
        "nn_realmlp",
        lambda: NNGPU(
            default_params={"hidden": 256, "n_layers": 4, "max_epochs": 120},
            class_weight="balanced",
            n_seeds=3,
            cat_features=cat_codes,
        ),
    ),
    (
        "boost_xgb",
        lambda: BoostXGB(
            default_params={"n_estimators": 800, "eta": 0.05, "max_depth": 8},
            class_weight="balanced",
        ),
    ),
]
for name, build in builders:
    algo = build()
    t0 = time.time()
    oof = algo.fit_predict(iterator)
    bac = balanced_accuracy(oof.target, oof.data.to_cupy())
    print(f"  {name:11s} OOF BAC={bac:.5f} | {time.time() - t0:.1f}s", flush=True)
    oof_list.append(oof)
    algos.append(algo)

section("WeightedBlender (RealMLP + XGB)")
blender = WeightedBlender(score_func=balanced_accuracy, greater_is_better=True)
oof_blend = blender.fit_predict(oof_list)
blend_bac = balanced_accuracy(oof_list[0].target, oof_blend.data.to_cupy())
print(f"weights: {[round(float(w), 3) for w in blender.weights.tolist()]}")
print(f"BLEND OOF BAC={blend_bac:.5f}", flush=True)

# ── submission ──────────────────────────────────────────────────
test_blend = blender.predict([a.predict(test_ds) for a in algos])
codes = cp.argmax(test_blend.data.to_cupy(), axis=1).get()
labels = np.array([code_to_label[int(c)] for c in codes])
sub = guam.read(COMP / "sample_submission.csv")
sub[TARGET] = cudf.Series(labels)
sub.to_csv(WORK / "submission.csv", index=False)
print(sub[TARGET].value_counts())
print(
    f"\n✅ GUAM RealMLP+XGB 블렌드 — BLEND OOF BAC {blend_bac:.5f} (XGB+TE LB 0.96613 대비)",
    flush=True,
)
```
이거 우리팀에서 만든 프레임워크를 kaggle 에서 테스트해보려고 작성한 테스트 코드야. 엔비디아 T4에서 돌아가도록 설정해놔서 나는 돌려보면 되는줄 알았는데, terminal 에 index error와 syntaxerror 가 발생하는거 때문에 테스트를 못해보고 있어. 해결방법을 알려줘.

### 💡 답변 (Assistant)
코드만 보면 “IndexError”는 발생 위치를 거의 특정할 수 있습니다. “SyntaxError”는 실행 방식이나 Python 버전 문제일 가능성이 커서, 우선 재현 가능한 방어 패치까지 같이 정리해볼게요.

---

### 💡 답변 (Assistant)
IndexError 쪽은 특히 `/kaggle/input`에서 프레임워크 소스 입력을 찾는 부분부터 확인하고, SyntaxError는 노트북/스크립트 변환 과정에서 `__future__` 위치가 밀렸는지 함께 보겠습니다.

---

### 💡 답변 (Assistant)
원인은 GPU/T4 설정 문제가 아니라 **파일 탐색/실행 방식 문제**일 가능성이 큽니다. 이 코드에서 바로 터질 수 있는 `IndexError`는 거의 확실히 여기입니다.

```python
src_root = sorted(INPUT.rglob("pyproject.toml"))[0].parent
```

`/kaggle/input` 안에 **GUAM 소스 repo가 Kaggle Dataset 형태로 attach되어 있지 않으면** `sorted(...)`가 빈 리스트가 되고 `[0]`에서 `IndexError: list index out of range`가 납니다.

`SyntaxError`는 코드 로직보다는 보통 아래 중 하나입니다.

1. `.py` 파일에 마크다운 코드펜스 ``` 를 그대로 넣음  
2. Python 파일을 `python kernel.py`가 아니라 shell에서 직접 실행함  
3. `from __future__ import annotations` 앞에 실제 코드가 들어감  
4. 파일이 UTF-8이 아니라 CP949 같은 인코딩으로 저장됨  
5. Kaggle script 파일이 아니라 노트북/메타데이터 구조가 꼬임

아래처럼 고치면 두 문제를 대부분 제거할 수 있습니다.

---

## 1. 맨 위 import 부분을 더 안전하게 수정

`from __future__ import annotations`는 이 코드에서 꼭 필요하지 않습니다. 삭제하고 `Optional`을 쓰는 쪽이 Kaggle/터미널 실행에서 덜 민감합니다.

```python
# -*- coding: utf-8 -*-
"""GUAM AutoML — S6E6, RealMLP(NN) + XGB 다양성 블렌드."""

import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, List, Optional

import numpy as np

WORK = Path("/kaggle/working")
N_FOLDS = 5
TARGET = "class"


def sh(cmd: str, cwd: Optional[str] = None) -> None:
    print(f"\n$ {cmd}", flush=True)
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def section(title: str) -> None:
    print(f"\n{'─' * 60}\n◆ {title}\n{'─' * 60}", flush=True)
```

특히 `.py` 파일에는 아래처럼 코드펜스를 절대 포함하면 안 됩니다.

```text
```python
...
```
```

`# %% [code]`는 주석이라 괜찮지만, Kaggle script로 돌릴 거면 없어도 됩니다.

---

## 2. `pyproject.toml` 탐색 부분 교체

기존 코드:

```python
INPUT = Path("/kaggle/input")
src_root = sorted(INPUT.rglob("pyproject.toml"))[0].parent
repo = WORK / "GUAM"
if not repo.exists():
    shutil.copytree(src_root, repo)
```

이 부분을 아래로 교체하세요.

```python
INPUT = Path("/kaggle/input")


def find_guam_source(input_root: Path) -> Path:
    candidates = []

    for pyproject in input_root.rglob("pyproject.toml"):
        root = pyproject.parent

        # GUAM repo root인지 확인: pyproject.toml + guam/ 패키지 디렉터리
        if (root / "guam").is_dir():
            candidates.append(root)

    if not candidates:
        visible_inputs = "\n".join(str(p) for p in sorted(input_root.iterdir()))
        raise FileNotFoundError(
            "GUAM source repo를 /kaggle/input 아래에서 찾지 못했습니다.\n"
            "Kaggle Notebook 오른쪽 Add input에서 GUAM repo를 Dataset으로 추가해야 합니다.\n"
            "필요 구조: /kaggle/input/<dataset-slug>/pyproject.toml "
            "그리고 /kaggle/input/<dataset-slug>/guam/\n\n"
            f"현재 /kaggle/input 내용:\n{visible_inputs}"
        )

    return sorted(candidates, key=lambda p: len(str(p)))[0]


src_root = find_guam_source(INPUT)
print(f"GUAM source: {src_root}", flush=True)

repo = WORK / "GUAM"

# 이전 실패 실행의 반쯤 복사된 GUAM 폴더를 재사용하지 않도록 매번 새로 복사
if repo.exists():
    shutil.rmtree(repo)

shutil.copytree(src_root, repo)

sh("pip install -e ./GUAM -q", cwd=str(WORK))
sys.path.insert(0, str(repo))
```

이렇게 하면 `IndexError` 대신, GUAM 소스 Dataset이 안 붙어 있을 때 명확한 `FileNotFoundError`가 뜹니다.

Kaggle에서 필요한 입력은 최소 2개입니다.

```text
/kaggle/input/playground-series-s6e6/
    train.csv
    test.csv
    sample_submission.csv

/kaggle/input/<your-guam-dataset>/
    pyproject.toml
    guam/
    ...
```

즉, competition data만 attach하면 현재 코드는 절대 시작 못 합니다. GUAM 프레임워크 소스도 별도 Dataset으로 붙어 있어야 합니다.

---

## 3. competition 데이터 경로도 안전하게 수정

기존 코드:

```python
COMP = next(INPUT.rglob("train.csv")).parent
```

이건 GUAM repo 안에 테스트용 `train.csv`가 있으면 엉뚱한 파일을 잡을 수 있습니다. 아래로 바꾸는 게 안전합니다.

```python
def find_comp_root(input_root: Path) -> Path:
    candidates = []

    for train_csv in input_root.rglob("train.csv"):
        root = train_csv.parent
        if (root / "test.csv").exists() and (root / "sample_submission.csv").exists():
            candidates.append(root)

    if not candidates:
        visible_inputs = "\n".join(str(p) for p in sorted(input_root.iterdir()))
        raise FileNotFoundError(
            "competition data root를 찾지 못했습니다. "
            "train.csv, test.csv, sample_submission.csv가 같은 폴더에 있어야 합니다.\n\n"
            f"현재 /kaggle/input 내용:\n{visible_inputs}"
        )

    # 가능하면 playground-series-s6e6 폴더 우선
    candidates = sorted(
        candidates,
        key=lambda p: ("playground-series-s6e6" not in str(p), len(str(p))),
    )
    return candidates[0]


COMP = find_comp_root(INPUT)
print(f"Competition data: {COMP}", flush=True)
```

그리고 기존의 이 줄을:

```python
COMP = next(INPUT.rglob("train.csv")).parent
```

위 함수 호출로 교체하면 됩니다.

---

## 4. 전체적으로 바꿔야 하는 핵심 부분

아래 순서로 초반부를 구성하세요.

```python
# -*- coding: utf-8 -*-
"""GUAM AutoML — S6E6, RealMLP(NN) + XGB 다양성 블렌드."""

import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, List, Optional

import numpy as np

WORK = Path("/kaggle/working")
INPUT = Path("/kaggle/input")
N_FOLDS = 5
TARGET = "class"


def sh(cmd: str, cwd: Optional[str] = None) -> None:
    print(f"\n$ {cmd}", flush=True)
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def section(title: str) -> None:
    print(f"\n{'─' * 60}\n◆ {title}\n{'─' * 60}", flush=True)


def find_guam_source(input_root: Path) -> Path:
    candidates = []

    for pyproject in input_root.rglob("pyproject.toml"):
        root = pyproject.parent
        if (root / "guam").is_dir():
            candidates.append(root)

    if not candidates:
        visible_inputs = "\n".join(str(p) for p in sorted(input_root.iterdir()))
        raise FileNotFoundError(
            "GUAM source repo를 /kaggle/input 아래에서 찾지 못했습니다.\n"
            "Kaggle Notebook의 Add input에서 GUAM repo를 Dataset으로 추가하세요.\n\n"
            f"현재 /kaggle/input 내용:\n{visible_inputs}"
        )

    return sorted(candidates, key=lambda p: len(str(p)))[0]


def find_comp_root(input_root: Path) -> Path:
    candidates = []

    for train_csv in input_root.rglob("train.csv"):
        root = train_csv.parent
        if (root / "test.csv").exists() and (root / "sample_submission.csv").exists():
            candidates.append(root)

    if not candidates:
        visible_inputs = "\n".join(str(p) for p in sorted(input_root.iterdir()))
        raise FileNotFoundError(
            "competition data root를 찾지 못했습니다.\n"
            "train.csv, test.csv, sample_submission.csv가 같은 폴더에 있어야 합니다.\n\n"
            f"현재 /kaggle/input 내용:\n{visible_inputs}"
        )

    return sorted(
        candidates,
        key=lambda p: ("playground-series-s6e6" not in str(p), len(str(p))),
    )[0]


section("GPU / RAPIDS check")
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")

import cudf  # noqa: E402
import cupy as cp  # noqa: E402

src_root = find_guam_source(INPUT)
print(f"GUAM source: {src_root}", flush=True)

repo = WORK / "GUAM"
if repo.exists():
    shutil.rmtree(repo)
shutil.copytree(src_root, repo)

sh("pip install -e ./GUAM -q", cwd=str(WORK))
sys.path.insert(0, str(repo))

import guam  # noqa: E402
from guam.automl.blend import WeightedBlender  # noqa: E402
from guam.ml_algo.boost_xgb import BoostXGB  # noqa: E402
from guam.ml_algo.nn import NNGPU  # noqa: E402
from guam.validation.base import CustomIterator  # noqa: E402

COMP = find_comp_root(INPUT)
print(f"Competition data: {COMP}", flush=True)
```

그다음 기존 코드에서 이 줄은 제거하세요.

```python
INPUT = Path("/kaggle/input")
src_root = sorted(INPUT.rglob("pyproject.toml"))[0].parent
repo = WORK / "GUAM"
if not repo.exists():
    shutil.copytree(src_root, repo)
sh("pip install -e ./GUAM -q", cwd=str(WORK))
sys.path.insert(0, str(repo))
```

그리고 이 줄도 제거하세요.

```python
COMP = next(INPUT.rglob("train.csv")).parent
```

이미 위에서 `COMP = find_comp_root(INPUT)`로 잡았기 때문입니다.

---

## 5. SyntaxError별 대응

### 케이스 A: 에러 화살표가 ``` 를 가리킴

파일에 마크다운 코드펜스가 들어간 겁니다.

잘못된 예:

```text
```python
import numpy as np
```
```

실제 `.py` 파일에는 아래처럼 순수 Python만 있어야 합니다.

```python
import numpy as np
```

---

### 케이스 B: 에러가 `from __future__ import annotations`를 가리킴

`from __future__` 앞에 코드가 들어간 겁니다. 이 코드에서는 필요 없으니 아예 삭제하세요.

삭제 후:

```python
from typing import Any, List, Optional
```

그리고 함수 시그니처는 이렇게 바꾸세요.

```python
def sh(cmd: str, cwd: Optional[str] = None) -> None:
```

---

### 케이스 C: `SyntaxError: Non-UTF-8 code starting ...`

한글 주석/문자 때문에 파일 인코딩이 꼬인 겁니다. 파일 첫 줄에 이걸 넣고, 파일을 UTF-8로 저장하세요.

```python
# -*- coding: utf-8 -*-
```

한글 주석, `—`, `·`, `◆`, `─`, `✅` 자체는 UTF-8 Python 파일에서는 문제 없습니다.

---

### 케이스 D: shell에서 Python 코드를 직접 실행함

아래처럼 하면 안 됩니다.

```bash
sh kernel.py
```

또는 터미널에 Python 코드를 그대로 붙여넣으면 shell 문법으로 해석돼서 깨집니다.

실행은 이렇게 해야 합니다.

```bash
python kernel.py
```

Kaggle Notebook이면 그냥 code cell로 실행하면 됩니다.

---

## 6. Kaggle에서 실제로 확인할 체크리스트

먼저 아주 짧은 셀로 입력 구조를 확인하세요.

```python
from pathlib import Path

for p in sorted(Path("/kaggle/input").iterdir()):
    print(p)
```

여기 출력에 최소한 아래 둘이 보여야 합니다.

```text
/kaggle/input/playground-series-s6e6
/kaggle/input/<your-guam-source-dataset>
```

그리고 GUAM Dataset 안에는 다음이 있어야 합니다.

```text
pyproject.toml
guam/
```

없으면 `src_root = sorted(INPUT.rglob("pyproject.toml"))[0].parent` 방식은 무조건 실패합니다.

---

## 7. 추가로 곧 만날 수 있는 문제 하나

이 부분도 반복 실행 시 문제가 될 수 있습니다.

```python
if not repo.exists():
    shutil.copytree(src_root, repo)
```

처음 실행하다가 중간에 실패하면 `/kaggle/working/GUAM`이 반쯤 복사된 상태로 남을 수 있습니다. 다음 실행에서는 `repo.exists()`가 `True`라서 복사를 건너뛰고, 깨진 소스를 그대로 씁니다.

그래서 테스트 중에는 이게 더 안전합니다.

```python
if repo.exists():
    shutil.rmtree(repo)
shutil.copytree(src_root, repo)
```

프레임워크 코드를 수정해서 다시 Dataset으로 올린 뒤 재실행할 때도 이 방식이 맞습니다.

---

## 결론

가장 먼저 고칠 줄은 이겁니다.

```python
src_root = sorted(INPUT.rglob("pyproject.toml"))[0].parent
```

이걸 방어적인 `find_guam_source()`로 바꾸세요. 그리고 `.py` 파일에서 마크다운 코드펜스 제거, `from __future__ import annotations` 제거, UTF-8 저장까지 적용하면 현재 말한 `IndexError`와 `SyntaxError`는 대부분 해결됩니다.

그다음에야 실제 NNGPU/XGB 학습 단계로 넘어갈 수 있습니다.

---

### ❓ 질문 (User)
그러면 캐글에 있는 데이터셋 말고 어떤 부분이 들어가야 되는거야? 지금 개발중인 프레임워크를 넣는 방법이 있어?

### 💡 답변 (Assistant)
네. 지금 필요한 건 **캐글 competition 데이터셋**이 아니라, 우리팀이 개발 중인 **GUAM 프레임워크 소스코드 자체**입니다.

현재 코드의 이 부분이 그걸 찾고 있어요.

```python
src_root = sorted(INPUT.rglob("pyproject.toml"))[0].parent
```

즉 Kaggle 안에서 아래 구조를 찾는 겁니다.

```text
/kaggle/input/<guam-source-dataset>/
├── pyproject.toml
├── guam/
│   ├── __init__.py
│   ├── automl/
│   ├── ml_algo/
│   └── validation/
└── ...
```

Kaggle competition 데이터만 있으면 보통 이런 구조입니다.

```text
/kaggle/input/playground-series-s6e6/
├── train.csv
├── test.csv
└── sample_submission.csv
```

그래서 `pyproject.toml`을 못 찾고 `IndexError`가 난 겁니다.

---

## 방법 1. 가장 추천: GUAM repo를 압축해서 Kaggle Dataset으로 올리기

개발 중인 프레임워크를 Kaggle에서 테스트하려면, **코드 repo를 private Kaggle Dataset으로 만들어 Add Input** 하면 됩니다. Kaggle Notebook은 오른쪽 `Input` 패널에서 `Add Input` 버튼으로 접근 가능한 Dataset을 추가할 수 있습니다. citeturn549124search1

로컬에서 GUAM 프로젝트 폴더가 이런 구조라고 가정하겠습니다.

```text
GUAM/
├── pyproject.toml
├── guam/
│   ├── __init__.py
│   ├── automl/
│   ├── ml_algo/
│   └── validation/
├── README.md
└── ...
```

이 폴더 전체를 zip으로 묶습니다.

```bash
zip -r guam-source.zip GUAM \
  -x "GUAM/.git/*" \
  -x "GUAM/.venv/*" \
  -x "GUAM/__pycache__/*" \
  -x "GUAM/**/__pycache__/*" \
  -x "GUAM/.pytest_cache/*"
```

그다음 Kaggle에서:

1. `Datasets`로 이동
2. `New Dataset` 또는 `Create Dataset`
3. `guam-source.zip` 업로드
4. 가능하면 **Private**으로 유지
5. Notebook으로 돌아와서 오른쪽 `Add Input`
6. 방금 만든 `guam-source` Dataset 추가

Kaggle Dataset은 Notebook output에서 만들 수도 있고, Dataset 페이지에서 직접 생성할 수도 있습니다. Kaggle 공식 문서에서도 Notebook output 파일로 Dataset을 만들거나 Dataset을 생성하는 흐름을 안내합니다. citeturn549124search0

---

## 중요한 포인트: zip 내부 구조

가장 안전한 구조는 zip을 풀었을 때 바로 `pyproject.toml`과 `guam/`이 보이는 형태입니다.

좋은 구조:

```text
/kaggle/input/guam-source/
├── pyproject.toml
├── guam/
└── README.md
```

또는 이것도 괜찮습니다.

```text
/kaggle/input/guam-source/GUAM/
├── pyproject.toml
├── guam/
└── README.md
```

왜냐하면 내가 앞에서 준 `find_guam_source()` 함수는 `/kaggle/input` 아래를 재귀적으로 뒤져서 `pyproject.toml + guam/` 조합을 찾기 때문입니다.

---

## 방법 2. GitHub에서 직접 clone하기

GUAM repo가 GitHub에 있고, Kaggle Notebook에서 Internet이 켜져 있다면 이것도 가능합니다.

```python
from pathlib import Path
import subprocess
import sys

WORK = Path("/kaggle/working")
repo = WORK / "GUAM"

if repo.exists():
    subprocess.run(f"rm -rf {repo}", shell=True, check=True)

subprocess.run(
    "git clone https://github.com/<org-or-user>/GUAM.git /kaggle/working/GUAM",
    shell=True,
    check=True,
)

subprocess.run(
    "pip install -e /kaggle/working/GUAM -q",
    shell=True,
    check=True,
)

sys.path.insert(0, str(repo))
```

단, competition Notebook에서는 인터넷이 꺼져 있거나 제한될 수 있습니다. 그래서 **재현성** 기준으로는 private Kaggle Dataset 방식이 더 안정적입니다.

---

## 방법 3. wheel 파일로 만들어서 올리기

프레임워크가 어느 정도 안정되어 있으면 repo 전체보다 wheel을 올리는 방식도 좋습니다.

로컬에서:

```bash
pip install build
python -m build
```

그러면 보통 생깁니다.

```text
dist/
├── guam-0.1.0-py3-none-any.whl
└── guam-0.1.0.tar.gz
```

이 `dist/*.whl`을 Kaggle Dataset으로 올린 뒤 Notebook에서:

```python
!pip install /kaggle/input/guam-wheel/guam-0.1.0-py3-none-any.whl -q
```

이 방식은 깔끔하지만, 지금처럼 개발 중이고 자주 바뀌는 프레임워크라면 매번 wheel 빌드 → 업로드가 조금 번거롭습니다. 지금은 **repo 전체 Dataset 업로드**가 더 편합니다.

---

## 지금 코드 기준으로 Kaggle Input에는 총 2개가 필요함

최종적으로 `/kaggle/input`은 대략 이렇게 보여야 합니다.

```text
/kaggle/input/
├── playground-series-s6e6/
│   ├── train.csv
│   ├── test.csv
│   └── sample_submission.csv
│
└── guam-source/
    ├── pyproject.toml
    ├── guam/
    ├── README.md
    └── ...
```

그러면 코드에서:

```python
COMP = find_comp_root(INPUT)
```

는 competition 데이터를 찾고,

```python
src_root = find_guam_source(INPUT)
```

는 GUAM 프레임워크 소스를 찾습니다.

---

## Kaggle에서 바로 확인하는 셀

Notebook 맨 위에 이걸 한 번 실행해보세요.

```python
from pathlib import Path

for p in sorted(Path("/kaggle/input").rglob("pyproject.toml")):
    print("pyproject:", p)

for p in sorted(Path("/kaggle/input").rglob("train.csv")):
    print("train.csv:", p)
```

정상이라면 최소 이런 식으로 나와야 합니다.

```text
pyproject: /kaggle/input/guam-source/pyproject.toml
train.csv: /kaggle/input/playground-series-s6e6/train.csv
```

`pyproject:`가 아무것도 안 나오면 GUAM 프레임워크가 Kaggle에 아직 안 들어간 상태입니다.

---

## 내 추천 구조

지금 상황에서는 이게 제일 좋습니다.

```text
GUAM repo 로컬에서 정리
→ zip 생성
→ Kaggle Private Dataset 생성
→ Notebook Add Input
→ /kaggle/working/GUAM 으로 복사
→ pip install -e ./GUAM
→ competition data로 테스트
```

즉, Kaggle에는 **데이터셋 1개만 넣는 게 아니라**, 다음 두 종류의 input을 붙여야 합니다.

```text
1. 대회 데이터
2. 우리팀 프레임워크 소스코드
```

지금 발생한 `IndexError`는 2번이 없어서 생긴 문제라고 보면 됩니다.

---

### ❓ 질문 (User)
$ zip -r guam-source.zip GUAM-main\
> -x "GUAM-main/.git/*"\
> -x "GUAM-main/.venv/*\
> -x "GUAM-main/__pycache__/"\
> -x "GUAM-main/**/__pycache__/*"\
> -x "GUAM-main/.pytest_cache/*"\
> -x "GUAM-main/*.md"\
> -x "GUAM-main/docs"\
> -x "GUAM-main/images"\
> -x "GUAM-main/references"\
> -x "GUAM-main/experiments"
git bash 에 이렇게 작성했는데 이 뒤로 안넘어가.

### 💡 답변 (Assistant)
`>` 프롬프트가 뜬 건 **Git Bash가 아직 명령어가 끝나지 않았다고 판단해서 계속 입력을 기다리는 상태**입니다.

지금 명령에서 가장 큰 문제는 여기입니다.

```bash
-x "GUAM-main/.venv/*\
```

따옴표가 닫히지 않았습니다. 그래서 Bash가 계속 다음 줄을 기다립니다.

일단 지금 상태에서는 `Ctrl + C` 눌러서 빠져나오세요.

그다음 아래처럼 다시 입력하세요.

```bash
zip -r guam-source.zip GUAM-main \
  -x "GUAM-main/.git/*" \
  -x "GUAM-main/.venv/*" \
  -x "GUAM-main/__pycache__/*" \
  -x "GUAM-main/**/__pycache__/*" \
  -x "GUAM-main/.pytest_cache/*" \
  -x "GUAM-main/*.md" \
  -x "GUAM-main/docs/*" \
  -x "GUAM-main/images/*" \
  -x "GUAM-main/references/*" \
  -x "GUAM-main/experiments/*"
```

중요한 차이는 이겁니다.

```bash
GUAM-main \
```

여기처럼 `GUAM-main` 뒤에 **공백 하나를 두고 `\`** 를 써야 합니다.

네가 쓴 건:

```bash
GUAM-main\
```

이렇게 붙어 있어서 Bash 입장에서는 줄바꿈을 없애고 다음 줄의 `-x`와 이어 붙일 수 있습니다. 안전하게 항상 `공백 + \` 형태로 쓰세요.

---

더 안전하게 한 줄로 쓰면 이렇게입니다.

```bash
zip -r guam-source.zip GUAM-main -x "GUAM-main/.git/*" "GUAM-main/.venv/*" "GUAM-main/__pycache__/*" "GUAM-main/**/__pycache__/*" "GUAM-main/.pytest_cache/*" "GUAM-main/*.md" "GUAM-main/docs/*" "GUAM-main/images/*" "GUAM-main/references/*" "GUAM-main/experiments/*"
```

압축이 끝난 뒤 확인:

```bash
ls -lh guam-source.zip
```

그리고 zip 안에 `pyproject.toml`이 들어갔는지 확인:

```bash
unzip -l guam-source.zip | grep pyproject.toml
```

정상이라면 이런 식으로 나와야 합니다.

```text
GUAM-main/pyproject.toml
```

그리고 `guam/` 패키지도 있어야 합니다.

```bash
unzip -l guam-source.zip | grep "GUAM-main/guam/__init__.py"
```

이게 나오면 Kaggle에 올릴 준비가 된 겁니다.

---

### ❓ 질문 (User)
╰─> See above for output.
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> See above for output.
note: This is an issue with the package mentioned above, not pip.
hint: See above for details.
CalledProcessError

### 💡 답변 (Assistant)
이 에러는 `pip install -e ./GUAM` 단계에서 난 겁니다. 지금 로그 조각만 보면 핵심 원인은 “소스 압축에서 필요한 메타데이터 파일을 빼버린 것”일 가능성이 큽니다.

---

### 💡 답변 (Assistant)
지금 에러는 이 줄에서 난 겁니다.

```python
sh("pip install -e ./GUAM -q", cwd=str(WORK))
```

즉, Kaggle에서 GUAM 소스는 찾았지만, **패키지 설치용 metadata 생성 단계에서 실패**한 상태입니다.

가장 유력한 원인은 네가 zip 만들 때 이 옵션을 넣은 것입니다.

```bash
-x "GUAM-main/*.md"
```

이게 `README.md`를 압축에서 제외합니다. 그런데 `pyproject.toml`에 보통 이런 설정이 들어 있습니다.

```toml
readme = "README.md"
```

그러면 `pip install -e` 할 때 `README.md`를 읽어서 package metadata를 만들려고 하는데, 파일이 없어서:

```text
metadata-generation-failed
CalledProcessError
```

가 납니다.

---

## 해결 1. 다시 압축할 때 `.md` 파일 제외하지 마세요

Git Bash에서 다시 압축하세요.

```bash
rm -f guam-source.zip

zip -r guam-source.zip GUAM-main \
  -x "GUAM-main/.git/*" \
  -x "GUAM-main/.venv/*" \
  -x "GUAM-main/__pycache__/*" \
  -x "GUAM-main/**/__pycache__/*" \
  -x "GUAM-main/.pytest_cache/*" \
  -x "GUAM-main/docs/*" \
  -x "GUAM-main/images/*" \
  -x "GUAM-main/references/*" \
  -x "GUAM-main/experiments/*"
```

여기서 중요한 점은 이 줄을 제거한 것입니다.

```bash
-x "GUAM-main/*.md"
```

`README.md`는 남겨야 합니다.

---

## 해결 2. zip 안에 필요한 파일이 있는지 확인

압축 후 Git Bash에서 확인하세요.

```bash
unzip -l guam-source.zip | grep "GUAM-main/pyproject.toml"
unzip -l guam-source.zip | grep "GUAM-main/README.md"
unzip -l guam-source.zip | grep "GUAM-main/guam/__init__.py"
```

최소한 이 세 개가 보여야 합니다.

```text
GUAM-main/pyproject.toml
GUAM-main/README.md
GUAM-main/guam/__init__.py
```

---

## 해결 3. Kaggle Dataset을 새 버전으로 업데이트

zip을 다시 만들었다고 Kaggle Notebook에 자동 반영되지 않습니다.

해야 할 일은:

1. Kaggle Dataset 페이지로 이동
2. 기존 `guam-source` Dataset에 새 버전 업로드
3. Notebook으로 돌아감
4. 가능하면 `Restart Session`
5. 오른쪽 Input에서 새 버전이 붙었는지 확인
6. 다시 실행

Notebook에서 확인:

```python
from pathlib import Path

for p in sorted(Path("/kaggle/input").rglob("pyproject.toml")):
    print("pyproject:", p)

for p in sorted(Path("/kaggle/input").rglob("README.md")):
    print("README:", p)

for p in sorted(Path("/kaggle/input").rglob("__init__.py")):
    if "/guam/" in str(p):
        print("guam init:", p)
```

---

## 만약 그래도 같은 에러가 나면

그때는 `README.md` 말고 다른 metadata 문제가 있는 겁니다. Kaggle 셀에서 아래처럼 `-q`를 빼고 실행하세요.

```python
!cd /kaggle/working && pip install -e ./GUAM -v
```

여기서 진짜 원인이 위쪽에 나옵니다. 예를 들면:

```text
FileNotFoundError: README.md
```

또는:

```text
LookupError: setuptools-scm was unable to detect version
```

이런 식으로 나올 수 있습니다.

---

## 추가 가능성: `setuptools-scm` 문제

만약 로그에 이런 말이 있으면:

```text
setuptools-scm was unable to detect version
```

그건 zip 만들 때 `.git`을 제외해서 발생한 겁니다. `pyproject.toml`이 Git 태그에서 버전을 읽도록 되어 있으면 `.git`이 없을 때 metadata 생성이 실패할 수 있습니다.

그 경우 임시 해결은 Kaggle에서 설치 전에 환경변수를 주는 것입니다.

```python
import os
os.environ["SETUPTOOLS_SCM_PRETEND_VERSION"] = "0.0.0"
```

그리고 다시:

```python
sh("pip install -e ./GUAM -q", cwd=str(WORK))
```

또는 셸 명령으로:

```python
!cd /kaggle/working && SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0 pip install -e ./GUAM
```

---

## 당장 가장 먼저 할 것

현재 상황에서는 이 순서가 제일 빠릅니다.

```bash
rm -f guam-source.zip

zip -r guam-source.zip GUAM-main \
  -x "GUAM-main/.git/*" \
  -x "GUAM-main/.venv/*" \
  -x "GUAM-main/__pycache__/*" \
  -x "GUAM-main/**/__pycache__/*" \
  -x "GUAM-main/.pytest_cache/*" \
  -x "GUAM-main/docs/*" \
  -x "GUAM-main/images/*" \
  -x "GUAM-main/references/*" \
  -x "GUAM-main/experiments/*"
```

그리고 확인:

```bash
unzip -l guam-source.zip | grep README.md
unzip -l guam-source.zip | grep pyproject.toml
unzip -l guam-source.zip | grep "guam/__init__.py"
```

`README.md`가 들어갔으면 Kaggle에 다시 올리고 실행하세요. 지금 에러는 이걸로 해결될 가능성이 높습니다.

---

### ❓ 질문 (User)
$ pip install -e ./GUAM -q
An error occurred checking for data source updates.
DatasetVersion with VersionId=16889698 and DatasetId=10709177 not mounted to session 327811027
Error: DatasetVersion with VersionId=16889698 and DatasetId=10709177 not mounted to session 327811027
ModuleNotFoundError

### 💡 답변 (Assistant)
이건 `pip` 문제가 아니라 **Kaggle Notebook 세션에 방금 올린 Dataset 버전이 제대로 mount되지 않은 상태**입니다.

핵심 메시지는 이거예요.

```text
DatasetVersion with VersionId=16889698 and DatasetId=10709177 not mounted to session
```

즉, 현재 세션에서 `/kaggle/input/guam-source...`가 깨졌거나, 새 버전으로 업데이트한 Dataset이 아직 현재 Notebook 세션에 붙지 않았습니다. Kaggle Notebook은 오른쪽 패널에서 Dataset을 Add Input으로 붙여서 쓰는 구조라, Dataset 버전을 새로 올린 뒤에는 세션/입력 상태가 꼬일 수 있습니다. citeturn533282view0turn164076search0

---

## 1. 먼저 Kaggle 세션을 새로 시작하세요

Kaggle Notebook에서:

```text
Run → Restart Session
```

또는 우측 상단/하단의 세션 재시작 버튼을 눌러주세요.

그다음 오른쪽 `Input` 패널에서:

1. 기존 `guam-source` Dataset 제거
2. 다시 `Add Input`
3. 새로 업로드한 `guam-source` Dataset 추가
4. Notebook 다시 실행

이걸 안 하면 Notebook이 예전 Dataset Version ID를 계속 잡고 있어서 저런 에러가 납니다.

---

## 2. Kaggle 셀에서 mount 확인

재시작 후 첫 셀에 이걸 실행하세요.

```python
from pathlib import Path

print("Top-level /kaggle/input:")
for p in sorted(Path("/kaggle/input").iterdir()):
    print(" ", p)

print("\npyproject.toml:")
for p in sorted(Path("/kaggle/input").rglob("pyproject.toml")):
    print(" ", p)

print("\nGUAM package:")
for p in sorted(Path("/kaggle/input").rglob("guam/__init__.py")):
    print(" ", p)
```

정상이면 이런 식으로 나와야 합니다.

```text
/kaggle/input/guam-source/GUAM-main/pyproject.toml
/kaggle/input/guam-source/GUAM-main/guam/__init__.py
```

아무것도 안 나오면 아직 Dataset이 Notebook에 안 붙은 겁니다.

---

## 3. `pip install -e ./GUAM` 바로 치면 안 됩니다

Kaggle input은 보통 `/kaggle/input/...` 아래에 있고, 현재 작업 디렉터리는 다릅니다. 그래서 먼저 `/kaggle/working/GUAM`으로 복사해야 합니다.

Kaggle Notebook 셀에서 아래를 실행하세요.

```python
from pathlib import Path
import shutil
import subprocess
import sys

INPUT = Path("/kaggle/input")
WORK = Path("/kaggle/working")

src_candidates = [
    p.parent
    for p in INPUT.rglob("pyproject.toml")
    if (p.parent / "guam").is_dir()
]

if not src_candidates:
    raise FileNotFoundError(
        "GUAM 소스를 찾지 못했습니다. "
        "/kaggle/input 아래에 pyproject.toml과 guam/ 폴더가 있어야 합니다."
    )

src_root = src_candidates[0]
print("GUAM source:", src_root)

repo = WORK / "GUAM"

if repo.exists():
    shutil.rmtree(repo)

shutil.copytree(src_root, repo)
print("Copied to:", repo)

subprocess.run(
    [sys.executable, "-m", "pip", "install", "-e", str(repo)],
    check=True,
)
```

그다음 확인:

```python
import guam

print("guam imported:", guam)
```

---

## 4. 터미널에서 직접 한다면 이 순서

Kaggle Terminal에서 바로:

```bash
pip install -e ./GUAM -q
```

이렇게 하면 현재 위치에 `GUAM` 폴더가 없을 수 있습니다.

먼저 확인:

```bash
pwd
ls -al
ls -al /kaggle/input
```

그리고 GUAM 소스 위치 찾기:

```bash
find /kaggle/input -name pyproject.toml
find /kaggle/input -path "*/guam/__init__.py"
```

예를 들어 결과가 이렇게 나왔다고 하면:

```text
/kaggle/input/guam-source/GUAM-main/pyproject.toml
```

그다음:

```bash
cd /kaggle/working
rm -rf GUAM
cp -r /kaggle/input/guam-source/GUAM-main GUAM
python -m pip install -e ./GUAM
python -c "import guam; print(guam)"
```

---

## 5. `ModuleNotFoundError`는 후속 증상입니다

지금 흐름은 이렇게 된 겁니다.

```text
Dataset mount 실패
→ GUAM 소스를 못 읽음
→ pip install 실패
→ import guam 실패
→ ModuleNotFoundError
```

그러니까 `ModuleNotFoundError`부터 고치는 게 아니라, 먼저 이걸 해결해야 합니다.

```text
DatasetVersion ... not mounted to session
```

---

## 최종 체크 순서

Kaggle에서 아래 순서대로 하세요.

```text
1. Restart Session
2. 오른쪽 Input에서 guam-source 제거
3. guam-source Dataset 다시 Add Input
4. /kaggle/input에 pyproject.toml, guam/__init__.py 있는지 확인
5. /kaggle/working/GUAM으로 복사
6. python -m pip install -e /kaggle/working/GUAM
7. import guam 확인
```

가장 중요한 건 이겁니다.

```bash
find /kaggle/input -name pyproject.toml
```

이 명령에서 아무것도 안 나오면 아직 Kaggle에 GUAM 프레임워크가 제대로 붙지 않은 상태입니다.

---

### ❓ 질문 (User)
ModuleNotFoundError 가 나와

### 💡 답변 (Assistant)
`ModuleNotFoundError`는 “어떤 모듈을 못 찾았는지”에 따라 원인이 갈립니다. 다만 지금 흐름상 1순위는 `guam` 소스가 현재 Python 경로에 안 잡힌 경우입니다.

---

### 💡 답변 (Assistant)
좋아요. 지금은 `ModuleNotFoundError`가 **정상적인 후속 증상**입니다.

앞에서 이미 이 에러가 있었죠.

```text
DatasetVersion ... not mounted to session
```

즉 흐름이 이렇게 된 겁니다.

```text
GUAM Dataset mount 실패
→ /kaggle/input에서 GUAM 소스를 못 읽음
→ pip install -e ./GUAM 실패
→ import guam 실패
→ ModuleNotFoundError
```

먼저 아래 셀을 Kaggle Notebook 맨 위에서 실행해보세요.

---

## 1. 현재 Kaggle에 GUAM 소스가 보이는지 확인

```python
from pathlib import Path

print("=== /kaggle/input ===")
for p in sorted(Path("/kaggle/input").iterdir()):
    print(p)

print("\n=== pyproject.toml ===")
for p in sorted(Path("/kaggle/input").rglob("pyproject.toml")):
    print(p)

print("\n=== guam package ===")
for p in sorted(Path("/kaggle/input").rglob("guam/__init__.py")):
    print(p)
```

정상이라면 최소한 이런 게 나와야 합니다.

```text
/kaggle/input/guam-source/GUAM-main/pyproject.toml
/kaggle/input/guam-source/GUAM-main/guam/__init__.py
```

만약 아무것도 안 나오면, 아직 Kaggle Notebook에 GUAM Dataset이 제대로 붙지 않은 겁니다.

이 경우:

```text
1. Restart Session
2. 오른쪽 Input 패널에서 guam-source 제거
3. 다시 Add Input
4. 새로 올린 guam-source Dataset 추가
5. 위 확인 셀 다시 실행
```

---

## 2. GUAM을 다시 복사하고 설치하는 셀

위 확인에서 `pyproject.toml`과 `guam/__init__.py`가 보이면, 아래 셀을 그대로 실행하세요.

```python
from pathlib import Path
import shutil
import subprocess
import sys

INPUT = Path("/kaggle/input")
WORK = Path("/kaggle/working")

# GUAM repo root 찾기
src_candidates = [
    p.parent
    for p in INPUT.rglob("pyproject.toml")
    if (p.parent / "guam").is_dir()
]

if not src_candidates:
    raise FileNotFoundError(
        "GUAM 소스를 찾지 못했습니다. "
        "/kaggle/input 아래에 pyproject.toml과 guam/ 폴더가 있어야 합니다."
    )

src_root = src_candidates[0]
print("GUAM source:", src_root)

# /kaggle/working/GUAM으로 깨끗하게 복사
repo = WORK / "GUAM"

if repo.exists():
    shutil.rmtree(repo)

shutil.copytree(src_root, repo)
print("Copied to:", repo)

# 같은 Python 커널에 설치
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-e", str(repo)],
    check=True,
)
```

그다음 바로 확인:

```python
import guam

print("GUAM import success")
print(guam)
```

---

## 3. 만약 `No module named 'guam'`이면

이 경우는 거의 확실히 설치가 안 된 겁니다.

확인:

```python
import sys
from pathlib import Path

print(sys.executable)
print(Path("/kaggle/working/GUAM").exists())
print(Path("/kaggle/working/GUAM/pyproject.toml").exists())
print(Path("/kaggle/working/GUAM/guam/__init__.py").exists())
```

모두 `True`가 나와야 합니다.

임시 우회 방법도 있습니다. 설치가 꼬였지만 소스 폴더가 정상이라면:

```python
import sys
sys.path.insert(0, "/kaggle/working/GUAM")

import guam
print("GUAM import success")
```

다만 이건 `pip install -e`를 완전히 대체하는 방법은 아닙니다. 의존성 설치가 필요한 경우에는 다시 실패할 수 있습니다.

---

## 4. 만약 `No module named 'cudf'`이면

이건 GUAM 문제가 아니라 RAPIDS 환경 문제입니다.

예:

```text
ModuleNotFoundError: No module named 'cudf'
```

또는:

```text
ModuleNotFoundError: No module named 'cuml'
```

이 경우 확인:

```python
import sys
print(sys.executable)

try:
    import cudf
    print("cudf OK", cudf.__version__)
except Exception as e:
    print("cudf error:", repr(e))

try:
    import cuml
    print("cuml OK", cuml.__version__)
except Exception as e:
    print("cuml error:", repr(e))
```

`cudf`, `cuml`이 없으면 현재 Kaggle 환경에 RAPIDS가 없는 상태입니다. 이 경우 코드는 GUAM 설치 전에 이미 여기서 터집니다.

```python
import cudf
import cupy as cp
from cuml.preprocessing import TargetEncoder
```

---

## 5. 지금 가장 중요한 체크

`ModuleNotFoundError` 메시지에서 정확히 이 부분을 봐야 합니다.

```text
ModuleNotFoundError: No module named '???'
```

### 경우별 원인

| 에러 | 의미 |
|---|---|
| `No module named 'guam'` | GUAM 소스가 설치/경로등록 안 됨 |
| `No module named 'cudf'` | RAPIDS 환경 없음 |
| `No module named 'cuml'` | RAPIDS cuML 없음 |
| `No module named 'xgboost'` | XGBoost 의존성 없음 |
| `No module named 'sklearn'` | scikit-learn 없음 |
| `No module named 'setuptools_scm'` | 패키지 metadata 빌드 의존성 없음 |

---

## 6. Kaggle에서 내가 추천하는 최종 설치 셀

일단 아래 셀 하나로 바꿔서 쓰세요.

```python
from pathlib import Path
import os
import shutil
import subprocess
import sys

INPUT = Path("/kaggle/input")
WORK = Path("/kaggle/working")

# setuptools-scm 사용하는 프로젝트일 때 .git 없이도 버전 생성되도록 방어
os.environ.setdefault("SETUPTOOLS_SCM_PRETEND_VERSION", "0.0.0")

src_candidates = [
    p.parent
    for p in INPUT.rglob("pyproject.toml")
    if (p.parent / "guam").is_dir()
]

if not src_candidates:
    print("Current /kaggle/input:")
    for p in sorted(INPUT.iterdir()):
        print(" ", p)
    raise FileNotFoundError("GUAM repo root를 찾지 못했습니다.")

src_root = src_candidates[0]
repo = WORK / "GUAM"

print("Using GUAM source:", src_root)

if repo.exists():
    shutil.rmtree(repo)

shutil.copytree(src_root, repo)

print("Installing GUAM...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-e", str(repo)],
    check=True,
)

sys.path.insert(0, str(repo))

import guam

print("✅ GUAM import success:", guam)
```

이 셀이 성공해야 기존 AutoML 테스트 코드를 실행할 수 있습니다.

---

## 결론

지금은 모델 코드 문제가 아니라 **GUAM 프레임워크가 현재 Kaggle 세션에 제대로 mount/install되지 않은 상태**입니다.

먼저 이것만 성공시키면 됩니다.

```python
import guam
```

이게 성공한 다음에야 아래 단계로 넘어갈 수 있습니다.

```python
import cudf
import cupy as cp
from cuml.preprocessing import TargetEncoder
from guam.ml_algo.nn import NNGPU
from guam.ml_algo.boost_xgb import BoostXGB
```

---

### ❓ 질문 (User)
니가 추천해준 방법 다 해봤는데, 1번은 다 맞는 경로를 내 놨어. 3번도 역시 모두 True 가 나왔고,

### 💡 답변 (Assistant)
여기까지 확인됐으면 Dataset mount나 복사 문제는 아닙니다. 이제 남은 원인은 거의 “설치는 실패했는데 조용히 지나갔거나”, “`guam` 내부에서 다른 의존성을 못 찾는 경우”입니다.

---

### 💡 답변 (Assistant)
그럼 이제 **mount/copy 문제는 해결된 상태**입니다. 남은 문제는 거의 두 가지입니다.

```text
1. pip install -e 단계가 실제로는 실패했다.
2. guam은 찾았지만, guam 내부에서 import하는 다른 패키지가 없어서 ModuleNotFoundError가 난다.
```

지금부터는 `pip install`보다 먼저 **직접 import 진단**을 해보는 게 빠릅니다.

---

## 1. 이 셀을 그대로 실행해보세요

```python
import sys
import traceback
from pathlib import Path

repo = Path("/kaggle/working/GUAM")

print("repo exists:", repo.exists())
print("pyproject exists:", (repo / "pyproject.toml").exists())
print("guam init exists:", (repo / "guam" / "__init__.py").exists())

sys.path.insert(0, str(repo))

try:
    import guam
    print("✅ import guam success")
    print("guam file:", guam.__file__)
except Exception:
    print("❌ import guam failed")
    traceback.print_exc()
```

여기서 핵심은 마지막 traceback입니다.

---

## 2. 결과별 해석

### 경우 A. 이렇게 나오면

```text
ModuleNotFoundError: No module named 'guam'
```

이건 이상합니다. 왜냐하면 네가 이미:

```text
/kaggle/working/GUAM/guam/__init__.py
```

가 `True`라고 확인했기 때문입니다.

이 경우는 보통 `sys.path.insert()`가 import 전에 안 들어갔거나, 다른 셀에서 커널 상태가 꼬인 겁니다.

해결:

```python
import sys
sys.path.insert(0, "/kaggle/working/GUAM")

import guam
print(guam.__file__)
```

이게 되면 `pip install -e` 없이도 일단 소스 import는 됩니다.

---

### 경우 B. 이렇게 나오면

```text
ModuleNotFoundError: No module named 'xxx'
```

여기서 `xxx`가 `guam`이 아니라면, 문제는 GUAM 설치가 아니라 **GUAM 내부 의존성 누락**입니다.

예를 들어:

```text
ModuleNotFoundError: No module named 'cuml'
```

이면 RAPIDS/cuML 문제고,

```text
ModuleNotFoundError: No module named 'setuptools_scm'
```

이면 패키지 metadata 빌드 문제고,

```text
ModuleNotFoundError: No module named 'sklearn'
```

이면 scikit-learn 의존성 문제입니다.

이 경우 `No module named '???'`에서 `???`가 진짜 원인입니다.

---

## 3. `pip install -e`는 이렇게 다시 실행하세요

지금처럼:

```bash
pip install -e ./GUAM -q
```

말고, Kaggle Notebook 안에서 아래처럼 실행하세요.

```python
import subprocess
import sys

subprocess.run(
    [sys.executable, "-m", "pip", "install", "-e", "/kaggle/working/GUAM", "-v"],
    check=False,
)
```

중요한 차이:

```python
sys.executable -m pip
```

를 쓰면 **현재 Kaggle Notebook 커널의 Python에 설치**합니다.

반대로 Terminal에서 그냥:

```bash
pip install -e ./GUAM
```

하면 Notebook 커널과 다른 Python/pip을 건드릴 수 있습니다. 그러면 terminal에서는 설치한 것 같은데 Notebook에서는 계속 `ModuleNotFoundError`가 납니다.

---

## 4. 당장 우회해서 테스트만 돌리는 방법

개발 중인 프레임워크를 Kaggle에서 테스트하는 목적이면, 일단 `pip install -e`를 빼고 소스 경로를 직접 추가해도 됩니다.

기존 코드의 이 부분:

```python
sh("pip install -e ./GUAM -q", cwd=str(WORK))
sys.path.insert(0, str(repo))
```

를 아래처럼 바꾸세요.

```python
sys.path.insert(0, str(repo))

import guam
print("GUAM loaded from:", guam.__file__)
```

즉, 당장 이렇게 갑니다.

```python
# sh("pip install -e ./GUAM -q", cwd=str(WORK))  # 일단 주석 처리
sys.path.insert(0, str(repo))

import guam
```

이 방식은 `guam/` 폴더가 `/kaggle/working/GUAM/guam`에 존재하면 바로 작동합니다.

단, GUAM 내부에서 필요한 외부 패키지가 없으면 그때는 다시:

```text
ModuleNotFoundError: No module named '외부패키지명'
```

이 나옵니다. 그 패키지만 따로 처리하면 됩니다.

---

## 5. `setuptools_scm` 에러일 때

만약 traceback에 이게 보이면:

```text
ModuleNotFoundError: No module named 'setuptools_scm'
```

또는:

```text
LookupError: setuptools-scm was unable to detect version
```

설치 전에 아래를 넣으세요.

```python
import os
os.environ["SETUPTOOLS_SCM_PRETEND_VERSION"] = "0.0.0"
```

그리고 다시:

```python
import subprocess
import sys

subprocess.run(
    [sys.executable, "-m", "pip", "install", "-e", "/kaggle/working/GUAM", "--no-build-isolation", "-v"],
    check=False,
)
```

`--no-build-isolation`을 붙이면 Kaggle 현재 환경에 있는 패키지로 metadata를 만들기 때문에, build isolation 때문에 생기는 문제를 줄일 수 있습니다.

---

## 6. 내가 추천하는 현재 코드 수정

프레임워크 설치 부분을 일단 이렇게 바꾸세요.

```python
src_root = find_guam_source(INPUT)
print(f"GUAM source: {src_root}", flush=True)

repo = WORK / "GUAM"

if repo.exists():
    shutil.rmtree(repo)

shutil.copytree(src_root, repo)

# editable install은 일단 생략하고 소스 경로 직접 등록
sys.path.insert(0, str(repo))

try:
    import guam
    print("✅ GUAM import success:", guam.__file__, flush=True)
except Exception:
    import traceback
    traceback.print_exc()
    raise
```

그리고 그 아래 기존 import를 이어가면 됩니다.

```python
from guam.automl.blend import WeightedBlender
from guam.ml_algo.boost_xgb import BoostXGB
from guam.ml_algo.nn import NNGPU
from guam.validation.base import CustomIterator
```

---

## 7. 다음에 확인해야 할 것

지금 가장 중요한 정보는 이 한 줄입니다.

```text
ModuleNotFoundError: No module named '???'
```

`???`가 무엇인지에 따라 답이 달라집니다.

하지만 네가 말한 것처럼:

```text
/kaggle/input 경로 정상
/kaggle/working/GUAM 존재 True
pyproject.toml True
guam/__init__.py True
```

라면, 이제는 `pip install -e`를 고집하지 말고 먼저:

```python
sys.path.insert(0, "/kaggle/working/GUAM")
import guam
```

로 우회하는 게 맞습니다. 이게 성공하면 GUAM 소스는 정상이고, 그다음 발생하는 `ModuleNotFoundError`는 GUAM 내부 의존성 문제입니다.

---
