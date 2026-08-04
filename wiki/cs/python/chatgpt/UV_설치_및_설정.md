---
type: Concept
title: "UV 설치 및 설정"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2026-03-26)"
tags: [cs, chatgpt-export]
timestamp: 2026-03-26
status: active
---

# UV 설치 및 설정

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-03-26

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
uv python 세팅 도와줘. 지금 우분투 환경으로 새로 설치를 했어. uv 인스톨 부터 진행할거야. 지금 우분투에 설치되어 있는건 아무것도 없어. 단순히 네트워크 연결과 sudo apt update, sudo apt upgrade 정도만 진행했어. 해당 프로젝트는 현재 pyproject.toml 파일을 가지고 환경설정을 할 생각이야. 이 점 유의해줘.
uv 를 써본적 있고 지금도 쓰고 있는데 오랜만에 세팅해서 그런지 헷갈리는게 많네. 차근차근 설명해줘.

### 💡 답변 (Assistant)
좋아요.  
지금 상황이면 **우분투를 거의 깨끗한 상태에서 시작**하는 거라서, 오히려 uv 기준으로 깔끔하게 세팅하기 좋습니다.

핵심은 이겁니다.

1. **uv 먼저 설치**
2. **uv가 관리하는 Python 설치**
3. **프로젝트 폴더에서 `pyproject.toml` 기준으로 환경 동기화**
4. **`uv run` 중심으로 실행**
5. 필요할 때만 `.venv` 활성화

uv 공식 문서 기준으로, Linux에서는 설치 스크립트로 uv를 설치할 수 있고, 프로젝트에서는 `uv sync`로 `pyproject.toml` 기반 환경을 만들고 맞출 수 있습니다. 또 uv는 자체적으로 Python 버전을 설치/관리할 수 있고, 기본적으로 uv가 관리하는 Python을 선호합니다. citeturn622509search0turn622509search1turn622509search4turn622509search6turn622509search7

---

## 0. 먼저 방향을 정하자

지금처럼 새 우분투라면 저는 이렇게 권합니다.

- **시스템 Python/apt Python에 최대한 의존하지 않기**
- **프로젝트 Python은 uv가 관리**
- **패키지 설치는 `pip install` 대신 `uv sync` / `uv add` 위주**
- **실행은 `python ...`보다 `uv run ...` 위주**

이렇게 하면 나중에 환경 꼬임이 훨씬 적습니다. uv는 프로젝트의 `pyproject.toml`과 lock 파일을 기준으로 의존성을 관리할 수 있습니다. citeturn622509search1turn622509search7

---

## 1. uv 설치

우분투에서 가장 무난한 방법은 공식 설치 스크립트입니다. 공식 문서에 나온 Linux 설치 명령은 아래와 같습니다. citeturn622509search0turn622509search2

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`curl`이 없다면 공식 문서에는 `wget` 방식도 있습니다. citeturn622509search0

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

설치 후에는 새 셸을 열거나, 현재 셸에 PATH를 다시 반영해야 할 수 있습니다.  
보통 다음으로 확인합니다.

```bash
uv --version
```

### 만약 `uv: command not found`가 뜨면
설치 스크립트가 PATH 설정까지 유도해주지만, 새 셸을 안 열면 반영이 안 되는 경우가 있습니다. 우선 아래를 해보세요.

```bash
source ~/.bashrc
uv --version
```

우분투에서 zsh를 쓰면 `~/.zshrc`를 다시 읽으면 됩니다.

```bash
source ~/.zshrc
uv --version
```

---

## 2. 시스템에 Python이 없어도 괜찮은가?

네.  
uv는 **자체적으로 Python 버전 설치와 관리**를 지원합니다. 공식 가이드에도 `uv python install` 흐름이 있습니다. 또 uv는 기본적으로 시스템 Python보다 **uv가 관리하는 Python을 선호**합니다. citeturn622509search6turn622509search4

그래서 지금처럼 “아무것도 없는 우분투”라면, 굳이 먼저 `sudo apt install python3`를 중심으로 갈 필요가 없습니다.

---

## 3. Python 설치

보통 프로젝트에서 쓸 버전을 먼저 설치합니다. 예를 들어 Python 3.12를 쓰고 싶으면:

```bash
uv python install 3.12
```

설치된 버전 확인:

```bash
uv python list
```

공식 문서에 따르면 uv는 버전 지정 설치를 지원하고, 필요하면 `python`/`python3` 기본 실행 파일 설치도 옵션으로 할 수 있습니다. 다만 기본적으로는 버전별 실행 파일 중심입니다. citeturn622509search6

### 추천
당장 시스템 전체 기본 `python` 명령까지 건드릴 필요는 없습니다.  
처음에는 그냥 **프로젝트 안에서만 uv가 해당 Python을 쓰게** 하는 게 제일 깔끔합니다.

---

## 4. 프로젝트 폴더로 이동

이미 `pyproject.toml`이 있다고 했으니, 새 프로젝트를 만드는 게 아니라 **기존 프로젝트를 복원**하는 흐름입니다.

```bash
cd /path/to/your/project
ls
```

여기서 보통 이런 파일이 있는지 확인합니다.

```bash
pyproject.toml
uv.lock        # 있으면 좋음
README.md
src/           # src 레이아웃이면
```

---

## 5. `pyproject.toml` 확인 포인트

`pyproject.toml`에 최소한 보통 이런 정보가 있습니다.

```toml
[project]
name = "your-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    ...
]
```

중요한 건 두 가지입니다.

- `requires-python`
- `dependencies`

uv는 프로젝트 의존성을 `pyproject.toml`에서 읽고, `uv sync`로 환경을 맞춥니다. 의존성은 직접 `pyproject.toml`을 수정할 수도 있고 `uv add`로 관리할 수도 있습니다. citeturn622509search7turn622509search3

### 특히 확인할 것
`requires-python = ">=3.12"` 같은 조건이 있으면, 그에 맞는 Python을 uv가 써야 합니다.

---

## 6. 가장 중요한 명령: `uv sync`

프로젝트 루트에서 아래를 실행합니다.

```bash
uv sync
```

이 명령으로 보통 다음이 한 번에 됩니다.

- 프로젝트용 가상환경 생성
- `pyproject.toml` 기준 의존성 설치
- `uv.lock`이 있으면 lock 기준으로 재현성 있게 설치

uv 공식 프로젝트 가이드에서도 프로젝트 작업의 기본 흐름으로 `uv sync`를 안내합니다. citeturn622509search1

### Python 버전까지 명확히 지정하고 싶으면
예를 들어 이 프로젝트를 3.12로 맞추고 싶다면:

```bash
uv sync --python 3.12
```

그러면 uv가 해당 버전을 사용해 `.venv`를 구성합니다.  
새 환경 세팅 초반에는 이 방식이 꽤 명확합니다.

---

## 7. 가상환경은 어디에 생기나?

보통 프로젝트 안에 `.venv`가 생깁니다.

확인:

```bash
ls -a
```

여기서 `.venv`가 보이면 정상입니다.

---

## 8. 실행은 어떻게 하나?

uv 프로젝트에서 가장 깔끔한 방식은 **굳이 activate하지 않고** `uv run`을 쓰는 겁니다.

예:

```bash
uv run python --version
uv run python main.py
uv run pytest
uv run ruff check .
```

공식 가이드도 프로젝트 명령 실행에서 `uv run` 중심 흐름을 보여주고, 가상환경을 활성화하지 않아도 프로젝트 환경으로 실행할 수 있게 설명합니다. citeturn622509search1

### 활성화가 꼭 필요할 때만
원하면 활성화도 가능합니다.

```bash
source .venv/bin/activate
```

그 후엔 평소처럼:

```bash
python --version
pytest
```

하지만 저는 초반엔 **`uv run` 습관**을 추천합니다.  
셸 상태에 덜 의존해서 헷갈림이 적습니다.

---

## 9. 지금 네 상황에 가장 추천하는 실제 순서

새 우분투 + 기존 프로젝트 + `pyproject.toml` 기준이라면, 저는 아래 순서를 권합니다.

```bash
# 1) uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) 셸 반영
source ~/.bashrc

# 3) uv 확인
uv --version

# 4) Python 설치
uv python install 3.12

# 5) 프로젝트로 이동
cd /path/to/project

# 6) 환경 생성 및 의존성 동기화
uv sync --python 3.12

# 7) 동작 확인
uv run python --version
uv run python -c "import sys; print(sys.executable)"
```

여기서 마지막 줄이 중요합니다.  
실제로 **어떤 Python 실행 파일이 쓰이는지** 확인할 수 있습니다.

---

## 10. `uv.lock` 파일이 있으면?

아주 좋습니다.  
그 경우 `uv sync`가 훨씬 재현성 있게 환경을 맞춰줍니다. uv는 프로젝트 환경 관리에서 lock 기반 동기화를 지원합니다. citeturn622509search1turn622509search7

실무적으로는:

- `pyproject.toml`만 있으면: 의존성 해석 후 설치
- `pyproject.toml` + `uv.lock` 있으면: 더 고정된 환경 복원

이라고 이해하면 됩니다.

---

## 11. 패키지를 추가하고 싶으면

기존 `pyproject.toml`을 직접 수정해도 되지만, uv는 `uv add`도 지원합니다. 공식 문서에 따르면 `uv add`와 `uv remove`로 프로젝트 의존성을 수정할 수 있습니다. citeturn622509search7

예:

```bash
uv add pandas
uv add scikit-learn
uv add --dev pytest ruff
```

그럼 `pyproject.toml`과 lock이 함께 갱신됩니다.

---

## 12. 네가 헷갈리기 쉬운 포인트 정리

### A. `uv python install`과 `uv sync`의 차이
- `uv python install 3.12`
  - **Python 자체를 설치**
- `uv sync`
  - 프로젝트용 **가상환경과 패키지 의존성**을 맞춤

즉:
- Python 설치 = 엔진 준비
- sync = 프로젝트 환경 조립

---

### B. activate 꼭 해야 하나?
아니요.  
uv에서는 `uv run ...`이면 충분한 경우가 많습니다. 공식 가이드도 활성화 없이 작업 가능한 흐름을 보여줍니다. citeturn622509search1

---

### C. `pip install -r requirements.txt`처럼 해야 하나?
이번에는 **아니요**.  
네가 이미 `pyproject.toml` 기준으로 갈 거라고 했으니, 중심 명령은 `uv sync`입니다. uv는 `pyproject.toml` 표준 의존성 정의를 지원합니다. citeturn622509search3turn622509search7

---

### D. 시스템 Python이 섞이지 않을까?
가능하면 프로젝트에서는 아래처럼 확인하면 됩니다.

```bash
uv run python -c "import sys; print(sys.executable)"
```

출력 경로가 프로젝트 `.venv` 안을 가리키면 정상입니다.

---

## 13. 문제 생겼을 때 가장 먼저 보는 것

### 1) uv 자체 확인
```bash
uv --version
which uv
```

### 2) Python 설치 확인
```bash
uv python list
```

### 3) 프로젝트 환경 확인
```bash
uv run python --version
uv run python -c "import sys; print(sys.executable)"
```

### 4) 의존성 다시 맞추기
```bash
uv sync
```

### 5) 완전히 다시 만들기
프로젝트 안에서 `.venv`를 지우고 다시:

```bash
rm -rf .venv
uv sync --python 3.12
```

---

## 14. 네 상황에 맞는 권장 운영 방식

앞으로는 이렇게 쓰면 됩니다.

### 프로젝트 처음 받을 때
```bash
cd project
uv sync
```

### 실행할 때
```bash
uv run python main.py
```

### 테스트
```bash
uv run pytest
```

### 린트/포맷
```bash
uv run ruff check .
uv run black .
```

### 새 패키지 추가
```bash
uv add <패키지명>
uv add --dev <패키지명>
```

---

## 15. 지금 바로 네가 하면 되는 최소 명령만 추리면

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version

uv python install 3.12

cd /path/to/project
uv sync --python 3.12

uv run python --version
uv run python -c "import sys; print(sys.executable)"
```

---

원하면 다음 답변에서 바로 이어서  
**“네 프로젝트의 `pyproject.toml`을 기준으로 정확히 어떤 명령을 순서대로 쳐야 하는지”** 형태로, 예시 파일 구조까지 넣어서 더 구체적으로 정리해드릴게요.

---
