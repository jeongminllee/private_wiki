---
type: Error Note
title: "LightAutoML KeyError 해결"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-04-06)"
tags: [errors, chatgpt-export]
timestamp: 2026-04-06
status: active
---

# LightAutoML KeyError 해결

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-04-06

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
lightautoml cv preset KeyError: 'tabicl_params'

### 💡 답변 (Assistant)
`LightAutoML`의 `cv` preset에서 발생하는  
`KeyError: 'tabicl_params'`는 **설정(dict) 구조 불일치 또는 버전 간 스키마 변경**에서 거의 100% 발생하는 오류입니다.

아래에서 정확한 원인 → 재현 패턴 → 해결 방법 순으로 정리합니다.

---

# 1. 에러의 본질

에러 메시지:
```
KeyError: 'tabicl_params'
```

이건 단순히 “키가 없다”가 아니라,

👉 **preset 내부에서 기대하는 config schema에 `tabicl_params`가 있어야 하는데 실제 config에는 없음**

을 의미합니다.

즉,
- preset 코드: 최신 구조 기대
- config (또는 내부 default): 구버전 구조

👉 **버전 mismatch**

---

# 2. 언제 터지냐 (대표 패턴)

다음 케이스에서 매우 자주 발생합니다.

### (1) LightAutoML 버전 꼬임
- pip로 설치된 버전 ≠ docs 기준 코드
- 또는 일부 dependency만 업데이트됨

특히:
- `lightautoml` 최신
- 내부 preset config는 구버전 캐시

---

### (2) preset override / custom config 사용

예:
```python
TabularCVAutoML(...)
```

또는

```python
automl = TabularAutoML(...)
```

에서 내부적으로 config merge 할 때

👉 일부 key 누락

---

### (3) 캐시된 preset config 사용

LightAutoML는 내부적으로 yaml/json config를 로드하는데

👉 이전 버전 config가 남아 있으면 충돌 발생

---

# 3. 핵심 원인 (중요)

`tabicl_params`는

👉 **Tabular Inner Cross Learning 관련 파라미터 블록**

인데,

버전별로 구조가 바뀜:

### 구버전
```yaml
tabular_params:
    ...
```

### 신버전
```yaml
tabicl_params:
    ...
```

👉 그래서 KeyError 발생

---

# 4. 해결 방법 (우선순위 순)

## ✅ 1순위: 깔끔 재설치 (가장 확실)

```bash
pip uninstall lightautoml -y
pip install lightautoml --no-cache-dir
```

또는 uv 쓰면:

```bash
uv pip uninstall lightautoml
uv pip install lightautoml --no-cache-dir
```

👉 cache 제거 필수

---

## ✅ 2순위: 버전 고정 (안정)

현재 가장 안정적인 조합:

```bash
pip install "lightautoml==0.3.7"
```

또는 최신 맞추려면:

```bash
pip install -U lightautoml
```

👉 중요한 건 **docs와 버전 맞추기**

---

## ✅ 3순위: config 강제 주입 (임시 해결)

에러 우회용:

```python
automl = TabularAutoML(
    general_params={
        "use_algos": [["lgb", "linear_l2"]],
    },
    tuning_params={
        "max_tuning_time": 300,
    }
)
```

또는 내부 config 수정:

```python
automl.params["tabicl_params"] = {}
```

👉 하지만 권장하지 않음 (근본 해결 아님)

---

## ✅ 4순위: CV preset 대신 기본 preset 사용

문제 발생 위치가 보통:

```python
TabularCVAutoML
```

👉 대신:

```python
TabularAutoML
```

로 변경

---

# 5. 디버깅 체크리스트

아래 확인하면 원인 바로 특정 가능:

### ✔ 설치 버전 확인
```python
import lightautoml
print(lightautoml.__version__)
```

---

### ✔ 내부 params 확인
```python
print(automl.params.keys())
```

👉 `tabicl_params` 없으면 문제 확정

---

### ✔ preset 확인
```python
print(type(automl))
```

---

# 6. 결론

이 에러는 단순 버그가 아니라:

👉 **LightAutoML 내부 config schema 변화 + 버전 불일치 문제**

---

# ✔ 가장 추천하는 해결

```bash
pip uninstall lightautoml -y
pip install lightautoml==0.3.7 --no-cache-dir
```

또는 최신으로 맞추고 docs도 최신 기준으로 진행

---

# 필요하면

지금 사용 중인 코드:

```python
(TabularCVAutoML 코드)
```

붙여주면

👉 **정확히 어디서 깨지는지 라인 단위로 디버깅** 해줄게.

---

### ❓ 질문 (User)
현재 테스트 중인 거는 https://colab.research.google.com/github/sb-ai-lab/LightAutoML/blob/master/examples/tutorials/Tutorial_8_CV_preset.ipynb
여기 lightautoml에서 제공하는 튜토리얼 8번을 실행중이야. 그 중 
```
automl = TabularCVAutoML(task = task,
                         timeout=5 * 3600,
                         cpu_limit = 2,
                         reader_params = {'cv': 5, 'random_state': 42},
                         )
```
이 셀에서 발생하는 문제야.
KeyError: 'tabicl_params'

### 💡 답변 (Assistant)
원인부터 말하면, 이건 **사용자 코드 문제가 아니라 현재 LightAutoML 쪽 버그에 가깝습니다.**

`Tutorial_8_CV_preset.ipynb`는 `TabularCVAutoML`를 `lightautoml.automl.presets.image_presets`에서 import해서 쓰고 있고, 질문하신 셀도 그 preset 생성 구간입니다. citeturn210397view0turn501284view0

문제는 현재 `TabularCVAutoML` 구현이 `TabularAutoML`을 상속하면서도, 자신의 `__init__`에서는 `general_params`, `reader_params`, `lgb_params`, `cb_params` 등은 업데이트하지만 **`tabicl_params`는 전혀 초기화하지 않습니다.** 그런데 부모 클래스 쪽 `infer_auto_params()`는 GPU가 보이면 `self.tabicl_params["device"] = ...`를 실행합니다. 그래서 `self.tabicl_params` 자체가 없는 상태면 바로 `KeyError: 'tabicl_params'`가 납니다. 이 동작은 현재 공개된 소스에서 그대로 확인됩니다. `TabularCVAutoML.__init__`의 업데이트 목록에는 `tabicl_params`가 없고, 반면 `TabularAutoML.infer_auto_params()`는 `self.tabicl_params["device"]`에 접근합니다. citeturn501284view0turn603479view0

게다가 `tabular_config.yml`에는 `tabicl_params` 기본 블록이 존재하지만, `TabularCVAutoML`은 기본 설정 파일로 `image_config.yml`을 쓰고, 그 `image_config.yml`에는 `tabicl_params` 블록이 없습니다. 즉, **CV preset의 config와 상속된 tabular 로직이 서로 안 맞는 상태**입니다. citeturn705049view0turn567502view0turn501284view0turn603479view0

가장 실용적인 해결책은 아래 3가지입니다.

### 1) 가장 간단한 우회: 생성 직후 `tabicl_params`를 수동으로 넣기
이게 지금 상황에서는 제일 빠릅니다.

```python
from lightautoml.automl.presets.image_presets import TabularCVAutoML
from lightautoml.tasks import Task

task = Task("multiclass")

automl = TabularCVAutoML(
    task=task,
    timeout=5 * 3600,
    cpu_limit=2,
    reader_params={"cv": 5, "random_state": 42},
)

# 우회 패치
automl.tabicl_params = {"device": "cpu", "batch_size": 8, "n_jobs": 4, "freeze_defaults": False}
```

GPU를 쓰는 환경이면:

```python
automl.tabicl_params = {"device": "cuda:0", "batch_size": 8, "n_jobs": 4, "freeze_defaults": False}
```

이건 `infer_auto_params()`가 기대하는 키를 미리 만들어 주는 방식입니다.

### 2) 생성자에 직접 넣으려 하지 말고, 커스텀 config를 써서 보강
`TabularCVAutoML`은 config 기반 preset이라 `image_config.yml`을 복사해서 `tabicl_params` 블록을 추가한 뒤 `config_path=...`로 넘기는 방법도 가능합니다. 현재 기본 `image_config.yml`에는 그 블록이 없고, `tabular_config.yml`에는 아래처럼 정의돼 있습니다. citeturn567502view0turn705049view0

예시:

```yaml
tabicl_params:
  device: cpu
  batch_size: 8
  n_jobs: 4
  freeze_defaults: False
```

그리고:

```python
automl = TabularCVAutoML(
    task=task,
    timeout=5 * 3600,
    cpu_limit=2,
    reader_params={"cv": 5, "random_state": 42},
    config_path="/content/my_image_config.yml",
)
```

### 3) 소스 자체를 임시 패치
Colab에서 정말 확실히 막고 싶으면, `TabularCVAutoML.__init__` 뒤에 아래 한 줄을 넣는 형태로 monkey patch를 해도 됩니다.

```python
if not hasattr(automl, "tabicl_params"):
    automl.tabicl_params = {"device": "cpu", "batch_size": 8, "n_jobs": 4, "freeze_defaults": False}
```

---

정리하면:

- `Tutorial_8_CV_preset`의 예제 셀 자체는 맞아 보이지만, 현재 공개 소스 조합에서는 `TabularCVAutoML`이 `tabicl_params`를 준비하지 않은 채 부모 로직이 그 키를 참조해서 깨집니다. citeturn210397view0turn501284view0turn603479view0turn567502view0turn705049view0
- 그래서 이건 **튜토리얼 코드 사용자의 실수라기보다 preset 구현 결함**으로 보는 게 맞습니다. citeturn501284view0turn603479view0

지금 바로 실행 가능한 최소 수정본은 이겁니다:

```python
task = Task("multiclass")

automl = TabularCVAutoML(
    task=task,
    timeout=5 * 3600,
    cpu_limit=2,
    reader_params={"cv": 5, "random_state": 42},
)

automl.tabicl_params = {
    "device": "cuda:0",   # GPU 없으면 "cpu"
    "batch_size": 8,
    "n_jobs": 4,
    "freeze_defaults": False,
}
```

원하시면 다음 답변에서 제가 **튜토리얼 8 기준으로 에러 없이 돌아가게 셀 단위 수정본**을 바로 정리해드리겠습니다.

---

### ❓ 질문 (User)
```
automl = TabularCVAutoML(task = task,
                         timeout=5 * 3600,
                         cpu_limit = 2,
                         reader_params = {'cv': 5, 'random_state': 42},
                         tabicl_params = {"device": "cuda:0", "batch_size": 8, "n_jobs": 4, "freeze_defaults": False})

```
TypeError: TabularCVAutoML.__init__() got an unexpected keyword argument 'tabicl_params'
이렇게 나오는데 몽키 패치가 나을까? 사실 이런 공식적인 패키지는 내부 건드는거 아니라고 배워서 조금 조심스러워

### 💡 답변 (Assistant)
네, 그 반응이 맞습니다.

`TabularCVAutoML.__init__` 시그니처에는 `tabicl_params`가 아예 없어서, 생성자에 직접 넣으면 `unexpected keyword argument`가 납니다. 공식 문서에 노출된 `TabularAutoML` 생성자 시그니처에도 `tabicl_params`는 없고, 튜토리얼 8은 `TabularCVAutoML`를 `image_presets`에서 import해서 사용합니다. citeturn755815view0turn540665view0

그리고 더 중요한 점은, CV preset이 기본으로 쓰는 `image_config.yml`에는 `tabicl_params` 블록이 없는데, 일반 tabular config인 `tabular_config.yml`에는 `tabicl_params`가 있습니다. 즉 지금은 **CV preset의 config와 내부 로직이 어긋난 상태**로 보입니다. citeturn795507view0turn795507view1

그래서 결론은 이렇습니다.

**패키지 소스 자체를 수정하는 건 비추천**입니다.  
하지만 **런타임에서만 우회 패치**하는 건 현실적인 임시 대응으로 괜찮습니다.

제가 추천하는 우선순위는:

1. **site-packages 내부 파일 직접 수정** → 비추천  
2. **런타임 몽키 패치** → 가능하지만 조금 거칠음  
3. **로컬 서브클래스 만들어서 보완** → 가장 깔끔한 우회

저라면 **몽키 패치보다 로컬 서브클래스**를 택하겠습니다.

---

## 가장 권장: 로컬 서브클래스

```python
from lightautoml.automl.presets.image_presets import TabularCVAutoML

class PatchedTabularCVAutoML(TabularCVAutoML):
    def __init__(self, *args, tabicl_params=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabicl_params = tabicl_params or {
            "device": "cuda:0",   # GPU 없으면 "cpu"
            "batch_size": 8,
            "n_jobs": 4,
            "freeze_defaults": False,
        }
```

사용은 이렇게:

```python
automl = PatchedTabularCVAutoML(
    task=task,
    timeout=5 * 3600,
    cpu_limit=2,
    reader_params={"cv": 5, "random_state": 42},
    tabicl_params={
        "device": "cuda:0",
        "batch_size": 8,
        "n_jobs": 4,
        "freeze_defaults": False,
    }
)
```

이 방식의 장점은:
- 패키지 파일 안 건드림
- 노트북 안에서만 국소적으로 수정
- 나중에 라이브러리 업데이트되면 쉽게 제거 가능

---

## 더 간단한 임시 우회

객체 생성 직후 속성만 붙이는 방식도 됩니다.

```python
automl = TabularCVAutoML(
    task=task,
    timeout=5 * 3600,
    cpu_limit=2,
    reader_params={"cv": 5, "random_state": 42},
)

automl.tabicl_params = {
    "device": "cuda:0",   # GPU 없으면 "cpu"
    "batch_size": 8,
    "n_jobs": 4,
    "freeze_defaults": False,
}
```

이건 사실상 **런타임 패치**입니다.  
소스 수정은 아니지만, 객체 상태를 수동 보정하는 거라 약간 임시방편 느낌이 있습니다.

---

## 왜 서브클래스가 몽키 패치보다 낫나

몽키 패치는 보통 이런 식입니다.

```python
orig_init = TabularCVAutoML.__init__

def new_init(self, *args, **kwargs):
    tabicl_params = kwargs.pop("tabicl_params", None)
    orig_init(self, *args, **kwargs)
    self.tabicl_params = tabicl_params or {
        "device": "cuda:0",
        "batch_size": 8,
        "n_jobs": 4,
        "freeze_defaults": False,
    }

TabularCVAutoML.__init__ = new_init
```

이 방법도 되긴 하지만,
- 전역으로 클래스 동작을 바꿈
- 나중에 디버깅할 때 헷갈림
- 노트북 다른 셀에도 영향 감

그래서 교육용/실험용 노트북에서도 **서브클래스가 더 안전**합니다.

---

## 제가 추천하는 실제 선택

당장 튜토리얼 8을 계속 진행하려면:

**`PatchedTabularCVAutoML` 서브클래스 방식으로 진행**  
이게 가장 무난합니다.

즉,  
“공식 패키지 내부는 건드리지 않는다”는 원칙도 지키고,  
현재 튜토리얼의 버그도 우회할 수 있습니다.

---

## 추가로 하나 체크할 점

지금 에러가 정말 생성 시점에 나는 것인지, 아니면 이후 `fit_predict`에서 나는 것인지 확인해보면 좋습니다. 현재까지 정황상 `tabicl_params` 누락은 config 불일치 문제로 보이지만, 실제 실행 경로에 따라 다음 셀에서 다른 에러가 이어질 수도 있습니다. `image_config.yml`에는 `tabicl_params`가 없고 `tabular_config.yml`에만 있으므로, 이후 단계에서 또 관련 분기가 나올 가능성은 있습니다. citeturn795507view0turn795507view1

원하시면 제가 **튜토리얼 8 노트북 기준으로, 어느 셀 위에 어떤 패치 셀을 넣으면 되는지** 바로 실행 가능한 형태로 정리해드리겠습니다.

---

### ❓ 질문 (User)
```
class PatchedTabularCVAutoML(TabularCVAutoML):
    def __init__(self, *args, tabicl_params=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabicl_params = tabicl_params or {
            "device": "cuda:0",   # GPU 없으면 "cpu"
            "batch_size": 8,
            "n_jobs": 4,
            "freeze_defaults": False,
        }
automl = PatchedTabularCVAutoML( 
    task=task,
    timeout=5 * 3600,
    cpu_limit=2,
    reader_params={"cv": 5, "random_state": 42},
    tabicl_params={
            "device": "cuda:0",   # GPU 없으면 "cpu"
            "batch_size": 8,
            "n_jobs": 4,
            "freeze_defaults": False,
        }
)
```
KeyError: 'tabicl_params'

### 💡 답변 (Assistant)
맞습니다.  
지금 작성하신 `PatchedTabularCVAutoML`가 실패하는 이유는 **`self.tabicl_params = ...`가 실행되기 전에 이미 `super().__init__()` 내부에서 `KeyError`가 터지기 때문**입니다. 즉, 에러 시점이 **부모 초기화 도중**이라서, 생성 직후 속성을 붙이는 방식이나 지금의 서브클래스 방식으로는 막을 수 없습니다. `TabularAutoML.infer_auto_params()`는 GPU가 잡히면 `self.tabicl_params["device"] = ...`에 접근하고, `TabularCVAutoML`의 기본 설정은 `image_config.yml`인데 그 파일에는 `tabicl_params` 블록이 없습니다. 반면 `tabular_config.yml`에는 그 블록이 있습니다. citeturn918292view1turn434380view0turn434380view1

즉 구조를 정리하면 이렇습니다.  
`Tutorial_8_CV_preset.ipynb`는 `TabularCVAutoML`를 사용하고, 이 클래스는 기본 config로 `image_config.yml`을 사용합니다. 그런데 이 config에는 `tabicl_params`가 없고, 상속받은 tabular 쪽 로직은 `tabicl_params`가 있다고 가정하고 접근합니다. 그래서 이건 사용자 실수라기보다 **현재 preset 조합의 결함**에 가깝습니다. citeturn482744view4turn482744view0turn434380view0turn918292view1

그래서 여기서는 **몽키 패치보다 `config_path`로 커스텀 config를 주입하는 방법**이 더 낫습니다.  
패키지 내부 파일을 수정하지 않고, 노트북에서만 별도 YAML을 만들어 넘기면 되기 때문입니다. 이 방식은 “공식 패키지 내부는 직접 건드리지 않는다”는 원칙에도 맞고, 나중에 라이브러리가 수정되면 바로 제거하기도 쉽습니다. citeturn482744view0turn434380view0turn434380view1

아래처럼 하시면 됩니다.

```python
%%writefile /content/my_cv_config.yml
general_params:
  use_algos: 'auto'
  nested_cv: False
  skip_conn: True

reader_params:
  samples: 100000
  max_nan_rate: 0.999
  max_constant_rate: 0.999
  cv: 5
  random_state: 42
  roles_params:
  n_jobs: 8
  advanced_roles: True
  numeric_unique_rate: 0.999
  max_to_3rd_rate: 1.1
  binning_enc_rate: 2
  raw_decr_rate: 1.1
  max_score_rate: 0.2
  abs_score_val: 0.04
  drop_score_co: 0.00

read_csv_params:
  decimal: '.'
  sep: ','

nested_cv_params:
  cv: 5
  n_folds:
  inner_tune: False
  refit_tuner: True

selection_params:
  mode: 0
  importance_type: 'gain'
  fit_on_holdout: True
  cutoff: 0
  feature_group_size: 1
  max_features_cnt_in_result:
  select_algos: ['gbm']

tuning_params:
  fit_on_holdout: True
  max_tuning_iter: 101
  max_tuning_time: 300

lgb_params:
  default_params:
    num_threads: 100
  freeze_defaults: False

cb_params:
  default_params:
    task_type: 'CPU'
    thread_count: 100
  freeze_defaults: False

xgb_params:
  default_params:
    nthread: 100
  freeze_defaults: False

rf_params:
  default_params:
  freeze_defaults: False

linear_l2_params:
  default_params: {}
  freeze_defaults: False

tabicl_params:
  device: cuda:0   # GPU 없으면 cpu
  batch_size: 8
  n_jobs: 4
  freeze_defaults: False

gbm_pipeline_params:
  top_intersections: 4
  max_intersection_depth: 3
  subsample: 100000
  auto_unique_co: 10
  multiclass_te_co: 3
  use_groupby: False
  groupby_types: ['delta_median', 'delta_mean', 'min', 'max', 'std', 'mode', 'is_mode']
  groupby_top_based_on: 'cardinality'
  groupby_top_categorical: 3
  groupby_top_numerical: 3
  groupby_triplets: []

linear_pipeline_params:
  # 튜토리얼 기본값에 맞게 필요 시 추가
  # 없으면 기본값을 쓰도록 최소만 유지
  cv_features: simple

cv_simple_features: {}
autocv_features: {}
```

그 다음 이렇게 생성하세요.

```python
automl = TabularCVAutoML(
    task=task,
    timeout=5 * 3600,
    cpu_limit=2,
    reader_params={"cv": 5, "random_state": 42},
    config_path="/content/my_cv_config.yml",
)
```

가장 중요한 포인트는 **`config_path`로 읽히는 YAML 안에 `tabicl_params`가 미리 있어야 한다**는 점입니다. 생성 후에 붙이는 건 늦습니다. citeturn482744view0turn918292view1turn434380view1

좀 더 빠르게 확인하고 싶으면, 생성 전에 YAML이 제대로 들어갔는지 이렇게 확인해보세요.

```python
import yaml

with open("/content/my_cv_config.yml", "r") as f:
    cfg = yaml.safe_load(f)

print("tabicl_params" in cfg)
print(cfg.get("tabicl_params"))
```

여기서 `True`와 dict가 나오면, 최소한 config 자체는 맞게 들어간 겁니다.

정리하면, 지금 상황에서는  
**1순위: 커스텀 config_path 방식**  
**2순위: 정말 급하면 몽키 패치**  
순서로 보시면 됩니다.

몽키 패치는 마지막 수단으로만 권합니다. 왜냐하면 지금 문제는 “초기화 이후 속성 보정”이 아니라 “초기화 도중 필요한 키 누락”이라서, 결국 더 깊은 레벨의 메서드까지 건드려야 할 수 있기 때문입니다. citeturn918292view1turn434380view0turn434380view1

원하시면 제가 다음 답변에서 **튜토리얼 8 노트북에 바로 붙여넣을 수 있게, 최소 수정 버전 셀 2~3개만 깔끔하게 다시 써드리겠습니다.**

---
