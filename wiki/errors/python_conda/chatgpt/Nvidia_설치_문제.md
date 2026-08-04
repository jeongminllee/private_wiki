---
type: Error Note
title: "Nvidia 설치 문제"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-06-26)"
tags: [errors, chatgpt-export]
timestamp: 2026-06-26
status: active
---

# Nvidia 설치 문제

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-26

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
nvidia cosmos3 uv sync --all-extras --group=cu130-train 한 이후에도 pip install retinaface 를 하라고 하네. 이거 왜 설치가 안되는거야? pyproject.toml 가봐도 있어서 설치가 된거 같은데 말이지.

### 💡 답변 (Assistant)
`pyproject.toml`에 있다는 것과 실제 실행 환경에서 import 가능한 것은 별개일 수 있어요. `uv`의 group/extras 적용, 설치된 패키지명, import명, 실행 환경 mismatch를 함께 확인해볼게요.

---

### 💡 답변 (Assistant)
가장 가능성 높은 결론은 **설치가 안 된 게 아니라, “현재 실행 중인 Python/노트북 커널”이 `packages/cosmos3/.venv`가 아니거나, `retinaface` import 과정에서 OpenCV/system library가 터져서 메시지가 잘못 “pip install retinaface”처럼 보이는 상황**입니다.

NVIDIA Cosmos3 README 기준으로 `uv sync --all-extras --group=cu130-train`은 **반드시 `packages/cosmos3` 안에서** 실행해야 하고, 그 결과 venv는 `packages/cosmos3/.venv`에 만들어집니다. 실행도 `source .venv/bin/activate` 하거나 `.venv/bin/python`, `.venv/bin/torchrun`을 직접 써야 한다고 되어 있습니다. citeturn277811view0

그리고 `pyproject.toml`을 보면 `retinaface`가 아니라 **`retinaface-py`**가 `[project.optional-dependencies].guardrail` 아래에 들어 있습니다. 즉 Cosmos가 의도한 패키지는 `pip install retinaface` 쪽이 아니라 `retinaface-py` 쪽입니다. `cu130-train` group 자체는 torch/transformer-engine/triton 같은 CUDA 학습 의존성만 추가하고, `retinaface-py`는 `--all-extras`로 들어오는 guardrail extra 쪽입니다. citeturn958032view0

더 중요한 포인트가 하나 있어요. NVIDIA 문서에 **“`uv sync --all-extras` alone is not enough for guardrails”**라고 직접 적혀 있습니다. Framework guardrail은 기본으로 켜지고, video guardrail path가 RetinaFace를 통해 OpenCV를 import하는데, headless 서버나 minimal container에서는 `libgl1`, `libglib2.0-0`, `libxcb1` 같은 system library가 없어서 `cv2` import가 실패할 수 있습니다. 이 경우 실제 원인은 Python package 미설치가 아니라 **OpenCV의 native shared library 누락**인데, 상위 코드가 “retinaface 설치하라”는 식으로 뭉뚱그려 말할 수 있습니다. citeturn277811view1

확인은 이렇게 해보세요.

```bash
cd packages/cosmos3

# 1) 지금 진짜 Cosmos venv Python으로 실행되는지 확인
.venv/bin/python - <<'PY'
import sys
print(sys.executable)
PY

# 2) Cosmos가 선언한 패키지가 설치되어 있는지 확인
.venv/bin/python - <<'PY'
import importlib.metadata as md

for name in ["retinaface-py", "retina-face", "retinaface"]:
    try:
        print(name, md.version(name))
    except md.PackageNotFoundError:
        print(name, "NOT INSTALLED")
PY

# 3) 실제 import traceback 확인
.venv/bin/python - <<'PY'
import traceback
try:
    import cv2
    print("cv2 OK:", cv2.__version__)
except Exception:
    print("cv2 FAILED")
    traceback.print_exc()

try:
    import retinaface
    print("retinaface OK:", retinaface.__file__)
except Exception:
    print("retinaface FAILED")
    traceback.print_exc()
PY
```

여기서 `retinaface-py`가 보이는데 `cv2 FAILED`가 뜨면, 이건 pip 문제가 아니라 system package 문제입니다. NVIDIA가 제시한 패키지를 설치하세요.

```bash
apt-get update
apt-get install -y --no-install-recommends \
  curl ffmpeg git-lfs libgl1 libglib2.0-0 libx11-dev libxcb1 tree wget
```

일반 host에서 root가 아니면 앞에 `sudo` 붙이면 됩니다.

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  curl ffmpeg git-lfs libgl1 libglib2.0-0 libx11-dev libxcb1 tree wget
```

설치 후 다시:

```bash
cd packages/cosmos3
source .venv/bin/activate
python -c "import cv2; print(cv2.__version__)"
python -c "import retinaface; print(retinaface.__file__)"
```

만약 노트북에서 에러가 나는 거라면, 거의 확실히 커널이 다른 Python을 보고 있는 겁니다. 노트북 셀에서 이걸 찍어보세요.

```python
import sys
print(sys.executable)
```

출력이 `.../packages/cosmos3/.venv/bin/python`이 아니면 `uv sync`로 설치한 환경을 쓰고 있지 않은 겁니다.

그리고 `pip install retinaface`는 조심하는 게 좋아요. PyPI에는 이름이 비슷한 패키지가 여러 개 있습니다. `retinaface-py`는 PyTorch 구현이고 설치명도 `retinaface-py`입니다. citeturn391847view0 반면 `retina-face`는 TensorFlow 기반 패키지이고 설치명은 `retina-face`, import는 `from retinaface import RetinaFace`입니다. citeturn391847view1 Cosmos `pyproject.toml`은 명시적으로 `retinaface-py`를 요구하므로, 무작정 `pip install retinaface`를 하면 다른 구현이 들어와서 더 헷갈릴 수 있습니다.

정리하면 우선순위는 이겁니다.

```bash
cd packages/cosmos3
source .venv/bin/activate
which python
python -c "import sys; print(sys.executable)"
python -c "import cv2; print(cv2.__version__)"
python -c "import importlib.metadata as md; print(md.version('retinaface-py'))"
python -c "import retinaface; print(retinaface.__file__)"
```

여기서 `cv2`가 깨지면 apt 패키지 문제, `which python`이 `.venv/bin/python`이 아니면 환경 문제, `retinaface-py` 자체가 없으면 `uv sync`를 `packages/cosmos3`가 아닌 다른 위치에서 실행했거나 `--all-extras`가 실제로 적용되지 않은 겁니다.

---
