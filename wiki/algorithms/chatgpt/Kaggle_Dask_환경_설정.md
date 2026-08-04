---
type: Concept
title: "Kaggle Dask 환경 설정"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-02-05)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-02-05
status: active
---

# Kaggle Dask 환경 설정

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-02-05

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
https://wikidocs.net/263103
dataset : Bank Account Fraud Dataset Suite (NeurIPS 2022)
환경 : kaggle notebook
gpu : t4*2

---
```
cmd = "hostname --all-ip-addresses"
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
IPADDR = str(output.decode()).split()[0]

cluster = LocalCUDACluster(ip=IPADDR, silence_logs=logging.ERROR)
client = Client(cluster)
```

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
/kaggle/input/bank-account-fraud-dataset-neurips-2022/Base.csv
/kaggle/input/bank-account-fraud-dataset-neurips-2022/Variant IV.csv
/kaggle/input/bank-account-fraud-dataset-neurips-2022/Variant V.csv
/kaggle/input/bank-account-fraud-dataset-neurips-2022/Variant I.csv
/kaggle/input/bank-account-fraud-dataset-neurips-2022/Variant III.csv
/kaggle/input/bank-account-fraud-dataset-neurips-2022/Variant II.csv
add Codeadd Markdown
!pip install dask_ml
Collecting dask_ml
  Downloading dask_ml-2025.1.0-py3-none-any.whl.metadata (6.0 kB)
Collecting dask-glm>=0.2.0 (from dask_ml)
  Downloading dask_glm-0.4.0-py3-none-any.whl.metadata (2.4 kB)
Requirement already satisfied: dask>=2025.1.0 in /usr/local/lib/python3.12/dist-packages (from dask[array,dataframe]>=2025.1.0->dask_ml) (2025.5.0)
Requirement already satisfied: distributed>=2025.1.0 in /usr/local/lib/python3.12/dist-packages (from dask_ml) (2025.5.0)
Requirement already satisfied: multipledispatch>=0.4.9 in /usr/local/lib/python3.12/dist-packages (from dask_ml) (1.0.0)
Requirement already satisfied: numba>=0.51.0 in /usr/local/lib/python3.12/dist-packages (from dask_ml) (0.60.0)
Requirement already satisfied: numpy>=1.24.0 in /usr/local/lib/python3.12/dist-packages (from dask_ml) (2.0.2)
Requirement already satisfied: packaging in /usr/local/lib/python3.12/dist-packages (from dask_ml) (26.0rc2)
Requirement already satisfied: pandas>=2.0 in /usr/local/lib/python3.12/dist-packages (from dask_ml) (2.2.2)
Requirement already satisfied: scikit-learn>=1.6.1 in /usr/local/lib/python3.12/dist-packages (from dask_ml) (1.6.1)
Requirement already satisfied: scipy in /usr/local/lib/python3.12/dist-packages (from dask_ml) (1.15.3)
Requirement already satisfied: click>=8.1 in /usr/local/lib/python3.12/dist-packages (from dask>=2025.1.0->dask[array,dataframe]>=2025.1.0->dask_ml) (8.3.1)
Requirement already satisfied: cloudpickle>=3.0.0 in /usr/local/lib/python3.12/dist-packages (from dask>=2025.1.0->dask[array,dataframe]>=2025.1.0->dask_ml) (3.1.1)
Requirement already satisfied: fsspec>=2021.09.0 in /usr/local/lib/python3.12/dist-packages (from dask>=2025.1.0->dask[array,dataframe]>=2025.1.0->dask_ml) (2025.10.0)
Requirement already satisfied: partd>=1.4.0 in /usr/local/lib/python3.12/dist-packages (from dask>=2025.1.0->dask[array,dataframe]>=2025.1.0->dask_ml) (1.4.2)
Requirement already satisfied: pyyaml>=5.3.1 in /usr/local/lib/python3.12/dist-packages (from dask>=2025.1.0->dask[array,dataframe]>=2025.1.0->dask_ml) (6.0.3)
Requirement already satisfied: toolz>=0.10.0 in /usr/local/lib/python3.12/dist-packages (from dask>=2025.1.0->dask[array,dataframe]>=2025.1.0->dask_ml) (0.12.1)
Collecting sparse>=0.15 (from dask-glm>=0.2.0->dask_ml)
  Downloading sparse-0.17.0-py2.py3-none-any.whl.metadata (5.3 kB)
Requirement already satisfied: pyarrow>=14.0.1 in /usr/local/lib/python3.12/dist-packages (from dask[array,dataframe]>=2025.1.0->dask_ml) (22.0.0)
Requirement already satisfied: jinja2>=2.10.3 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (3.1.6)
Requirement already satisfied: locket>=1.0.0 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (1.0.0)
Requirement already satisfied: msgpack>=1.0.2 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (1.1.2)
Requirement already satisfied: psutil>=5.8.0 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (5.9.5)
Requirement already satisfied: sortedcontainers>=2.0.5 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (2.4.0)
Requirement already satisfied: tblib>=1.6.0 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (3.1.0)
Requirement already satisfied: tornado>=6.2.0 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (6.5.1)
Requirement already satisfied: urllib3>=1.26.5 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (2.6.3)
Requirement already satisfied: zict>=3.0.0 in /usr/local/lib/python3.12/dist-packages (from distributed>=2025.1.0->dask_ml) (3.0.0)
Requirement already satisfied: llvmlite<0.44,>=0.43.0dev0 in /usr/local/lib/python3.12/dist-packages (from numba>=0.51.0->dask_ml) (0.43.0)
Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.12/dist-packages (from pandas>=2.0->dask_ml) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.12/dist-packages (from pandas>=2.0->dask_ml) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.12/dist-packages (from pandas>=2.0->dask_ml) (2025.2)
Requirement already satisfied: joblib>=1.2.0 in /usr/local/lib/python3.12/dist-packages (from scikit-learn>=1.6.1->dask_ml) (1.5.3)
Requirement already satisfied: threadpoolctl>=3.1.0 in /usr/local/lib/python3.12/dist-packages (from scikit-learn>=1.6.1->dask_ml) (3.6.0)
Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.12/dist-packages (from jinja2>=2.10.3->distributed>=2025.1.0->dask_ml) (3.0.3)
Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/dist-packages (from python-dateutil>=2.8.2->pandas>=2.0->dask_ml) (1.17.0)
Downloading dask_ml-2025.1.0-py3-none-any.whl (149 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 150.0/150.0 kB 3.1 MB/s eta 0:00:00a 0:00:01
Downloading dask_glm-0.4.0-py3-none-any.whl (21 kB)
Downloading sparse-0.17.0-py2.py3-none-any.whl (259 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 259.4/259.4 kB 9.9 MB/s eta 0:00:00
Installing collected packages: sparse, dask-glm, dask_ml
Successfully installed dask-glm-0.4.0 dask_ml-2025.1.0 sparse-0.17.0
add Codeadd Markdown
# For GPU array computation
import cupy as cp

# Default DASK Libraries and set use GPU's
import dask
import dask_cudf
import dask.dataframe as dd
dask.config.set({"dataframe.backend": "cudf"})

# Set for Multi GPU use
from dask_cuda        import LocalCUDACluster
from dask.distributed import Client, wait, progress

import dask_ml
from dask_ml.wrappers        import ParallelPostFit

# Import cuml RandomForest
from cuml.ensemble import RandomForestClassifier as RF
from cuml.dask.ensemble import RandomForestClassifier as RF_Dask

add Codeadd Markdown
arrow_upwardarrow_downwarddelete
cmd = "hostname --all-ip-addresses"
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
IPADDR = str(output.decode()).split()[0]

cluster = LocalCUDACluster(ip=IPADDR, silence_logs=logging.ERROR)
client = Client(cluster)

---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
/tmp/ipykernel_55/1422492026.py in <cell line: 0>()
      1 cmd = "hostname --all-ip-addresses"
----> 2 process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
      3 output, error = process.communicate()
      4 IPADDR = str(output.decode()).split()[0]
      5 

NameError: name 'subprocess' is not defined

---
이 문제를 어떻게 하면 해결할 수 있을까?

### 💡 답변 (Assistant)
에러의 **직접 원인**과 **카글(Kaggle) + Dask CUDA 환경에서의 구조적 주의점**을 나눠서 설명하겠습니다.

---

## 1️⃣ 에러의 직접 원인 (즉시 해결 가능)

에러 메시지:

```text
NameError: name 'subprocess' is not defined
```

원인은 단순합니다.  
`subprocess` 모듈을 **import 하지 않았기 때문**입니다.

### ✅ 최소 수정

```python
import subprocess
```

을 `cmd = "hostname --all-ip-addresses"` **이전**에 추가하면 됩니다.

```python
import subprocess

cmd = "hostname --all-ip-addresses"
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
IPADDR = str(output.decode()).split()[0]
```

이것만으로 **NameError 자체는 해결**됩니다.

---

## 2️⃣ 하지만… Kaggle + LocalCUDACluster에서의 중요한 함정 ⚠️

여기서 끝내면 **다음 단계에서 더 큰 문제**를 만날 가능성이 큽니다.  
왜냐하면 **Kaggle Notebook 환경은 일반적인 멀티 노드/멀티 IP 환경이 아니기 때문**입니다.

### 🔍 Kaggle 환경의 특징

- 컨테이너 기반 단일 노드
- 외부 IP 바인딩이 필요 없음
- `hostname --all-ip-addresses`가 **불필요하거나 오히려 문제를 유발**함
- `LocalCUDACluster(ip=...)` 지정은 대부분 필요 없음

---

## 3️⃣ Kaggle에서 권장되는 올바른 패턴 (중요)

### ❌ 불필요한 방식 (지금 코드)

```python
IPADDR = str(output.decode()).split()[0]
cluster = LocalCUDACluster(ip=IPADDR, silence_logs=logging.ERROR)
```

### ✅ Kaggle에서의 권장 방식

```python
from dask_cuda import LocalCUDACluster
from dask.distributed import Client

cluster = LocalCUDACluster(
    silence_logs=logging.ERROR
)
client = Client(cluster)

client
```

👉 **IP 지정 제거**  
👉 Dask가 내부적으로 loopback (`127.0.0.1`) 사용  
👉 Kaggle에서 가장 안정적

---

## 4️⃣ T4 × 2 환경에서 꼭 확인해야 할 것

Kaggle에서 GPU 2개가 제대로 잡히는지 확인하세요.

```python
cluster
```

또는

```python
client.scheduler_info()["workers"].keys()
```

정상이라면 예:

```text
tcp://127.0.0.1:XXXXX
tcp://127.0.0.1:YYYYY
```

그리고 GPU 확인:

```python
import cupy as cp
cp.cuda.runtime.getDeviceCount()
```

👉 `2`가 나오면 정상

---

## 5️⃣ 정리 (핵심만)

### 즉각적인 에러 원인
- `import subprocess` 누락

### 구조적으로 더 좋은 해결책
- Kaggle에서는 **IPADDR 자체를 쓰지 말 것**
- `LocalCUDACluster()`를 **디폴트 설정으로 사용**

### 최종 추천 코드

```python
from dask_cuda import LocalCUDACluster
from dask.distributed import Client
import logging

cluster = LocalCUDACluster(
    silence_logs=logging.ERROR
)
client = Client(cluster)
client
```

---

다음 단계로 원하시면:
- **cudf / dask_cudf로 CSV 로딩 최적화**
- **Bank Account Fraud Dataset에 맞는 RF_Dask 파이프라인**
- **클래스 불균형 처리 전략 (NeurIPS 데이터 특성 기반)**

중 어떤 걸 먼저 볼지 말해 주세요.

---
