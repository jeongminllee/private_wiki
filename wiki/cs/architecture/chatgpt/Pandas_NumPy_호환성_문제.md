---
type: Concept
title: "Pandas NumPy 호환성 문제"
description: "CS - Software Architecture - ChatGPT 대화 추출 노트 (2025-08-28)"
tags: [cs, chatgpt-export]
timestamp: 2025-08-28
status: active
---

# Pandas NumPy 호환성 문제

> **카테고리**: `CS - Software Architecture`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-08-28

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject

File "/Users/ijeongmin/Desktop/projects/daegu-lec/solar_rag.py", line 155, in <module>
    st.write(result["context"])
File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/streamlit/runtime/metrics_util.py", line 443, in wrapped_func
    result = non_optional_func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/streamlit/elements/write.py", line 462, in write
    elif dataframe_util.is_dataframe_like(arg):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/streamlit/dataframe_util.py", line 294, in is_dataframe_like
    return determine_data_format(obj) in {
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/streamlit/dataframe_util.py", line 1161, in determine_data_format
    import pandas as pd
File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/pandas/__init__.py", line 46, in <module>
    from pandas.core.api import (
File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/pandas/core/api.py", line 1, in <module>
    from pandas._libs import (
File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/pandas/_libs/__init__.py", line 18, in <module>
    from pandas._libs.interval import Interval
File "interval.pyx", line 1, in init pandas._libs.interval

### 💡 답변 (Assistant)
이 에러는 **pandas C 확장 모듈이 컴파일될 때 쓴 NumPy 헤더(ABI)와, 지금 실행 중인 NumPy 바이너리의 ABI가 서로 달라서** 생긴 전형적인 충돌이에요. 간단히 말해, **서로 다른 버전 조합(또는 pip/conda 혼용)** 때문에 “기대 크기 96, 실제 88” 같은 불일치가 발생한 거예요.

좋아요—바로 해결 가이드 드릴게요. (중간에 “임시 우회”도 있어요.)


# 0) 급한 불 끄기(임시 우회)
`st.write(result["context"])`가 dict/list 같은 “DataFrame 비슷한” 객체를 만나면 Streamlit이 내부적으로 `pandas`를 import하려다 터집니다. **에러를 일단 피하려면**:

```python
# DataFrame 자동 판별을 피하고 안전하게 출력
st.json(result["context"])         # JSON 구조로 보여주기
# 또는
st.code(result["context"], language="json")  # 코드 블록으로 보여주기
# 또는
st.markdown(f"```\n{result['context']}\n```")
```

이건 근본 해결은 아니지만, 당장 앱이 죽는 건 막을 수 있어요.


# 1) 현재 상태 점검 (꼭 실행)
아래 한 줄로 Python/NumPy/Pandas 버전과 설치 위치를 확인하세요.

```bash
python -c "import sys, numpy as np, pandas as pd; \
print('PY', sys.version); \
print('NP', np.__version__, np.__file__); \
print('PD', pd.__version__, pd.__file__)"
```

그리고 **패키지 일관성 검사**:

- pip 환경일 때
  ```bash
  python -m pip check
  ```
- conda 환경일 때
  ```bash
  conda list | egrep 'python|numpy|pandas|streamlit|pyarrow|scipy'
  ```

> 핵심 신호  
> - NumPy와 Pandas가 **서로 다른 설치 경로(예: 하나는 conda, 하나는 pip)** 이면 위험 신호  
> - 아주 오래되거나 아주 최신 조합이 섞여 있어도 위험 신호


# 2) 안정 조합으로 재설치 (혼용 금지!)
가장 중요한 원칙: **하나의 패키지 관리자만 쓰세요.** (pip만 or conda만)

## A) conda만 사용하는 방법(Anaconda/Miniconda 추천)
현재 환경 이름이 `projx` 인 듯합니다.

```bash
conda activate projx

# 가능하면 전체를 일치화
conda install -y -c conda-forge "numpy>=2.1,<2.2" "pandas>=2.2,<2.3" "streamlit>=1.36" "pyarrow" "scipy"
```

그래도 꼬였다면 **새 환경**이 가장 빠릅니다. (특히 macOS 10.15라면 호환성 이유로 새 환경 권장)

```bash
conda create -y -n solar-rag python=3.11 -c conda-forge \
  numpy pandas streamlit pyarrow scipy

conda activate solar-rag
# 나머지 의존성(pip로 받는 라이브러리들) 설치
pip install openai upstage
```

> 팁: macOS 10.15(Catalina)는 신형 바이너리 휠 지원이 드문 편이라, **conda-forge** 채널이 더 잘 맞는 경우가 많습니다. 또한 Python **3.12**보다 **3.11**이 제3자 패키지 호환이 넓어 안전합니다.

## B) pip만 사용하는 방법(가상환경 venv/conda+pip 혼용 금지)
```bash
# 같은 환경에서
python -m pip uninstall -y pandas numpy
python -m pip cache purge

# 호환되는 버전 쌍으로 강제 재설치 (예시)
python -m pip install --no-binary=:all: --no-cache-dir numpy==2.1.1
python -m pip install --no-cache-dir pandas==2.2.2 streamlit pyarrow scipy
```

> 왜 pandas도 같이 재설치?  
> pandas의 C확장(.so/.pyd)은 **설치 시점의 NumPy 헤더**를 기준으로 컴파일됩니다.  
> NumPy만 업데이트하면 pandas 바이너리가 **예전 헤더**를 들고 있어 충돌해요.  
> 그래서 둘을 **항상 같은 타이밍에** 재설치해야 합니다.


# 3) 아키텍처/경로 꼬임 점검 (맥 한정 팁)
- Intel Mac(10.15.7)이면 `platform.machine()`이 `x86_64`여야 정상입니다:
  ```bash
  python -c "import platform; print(platform.machine())"
  ```
- `sys.path`에 **환경 밖 경로**가 끼어 있지 않은지 확인:
  ```bash
  python -c "import sys; print('\n'.join(sys.path))"
  ```

예를 들어 `/Library/...`나 다른 파이썬 배포의 `site-packages`가 껴 있다면 그게 섞여서 문제를 유발할 수 있어요.


# 4) Streamlit 사용 시 주의
- `st.write()`는 pandas가 설치되어 있고 “DataFrame처럼 보이는 객체”를 넣으면 자동으로 `DataFrame`으로 취급하려고 합니다.  
  **특정 환경에서 pandas 문제가 재발**한다면 `st.dataframe()`을 명시적으로 쓰거나, 텍스트/JSON 전용 출력으로 강제하세요.
- 진짜 표를 보여줄 거라면:
  ```python
  import pandas as pd
  df = pd.DataFrame(result["context"])  # context 구조에 맞게 변환
  st.dataframe(df)
  ```


# 5) 그래도 안 풀리면 공유해 주세요
아래 출력 3줄만 붙여 주시면, 버전 호환을 **정확히** 맞춰드릴게요.
```bash
python -c "import sys, numpy as np, pandas as pd; \
print(sys.version); print('numpy', np.__version__, np.__file__); \
print('pandas', pd.__version__, pd.__file__)"
```

---

요약: **pip/conda 혼용 없이** NumPy와 Pandas를 **같이 재설치**(또는 새 환경 생성)하면 대부분 해결됩니다. 급하면 `st.json(...)`으로 우회하시고요.

---
