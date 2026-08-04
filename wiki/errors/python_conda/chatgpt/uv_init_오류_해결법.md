---
type: Error Note
title: "uv init 오류 해결법"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2025-10-13)"
tags: [errors, chatgpt-export]
timestamp: 2025-10-13
status: active
---

# uv init 오류 해결법

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-10-13

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
python 토탈 패키지 uv 로 세팅을 새롭게 해보려고 해. 
내가 하려고 하는 projects 폴더를 Programs Files\projects 디렉토리로 완성한 후 uv init을 시행하니까 os error 5 로 액세스가 거부되었습니다 라는 에러 메시지가 나오고 있어. 
해결방법을 알려줘.

### 💡 답변 (Assistant)
원인부터 짚고 갈게요.  
`C:\Program Files`는 Windows가 “관리자만 쓰기 가능”으로 보호하는 영역이라, 일반 권한 셸에서 그 안에 파일/폴더를 만들거나 수정하려 하면 `OSError: [Errno 5] Access is denied`가 납니다. `uv init`는 `pyproject.toml`, `.venv/` 등 여러 파일을 생성하려 하므로 권한이 막히는 거예요. (또한 경로에 공백이 있으니 따옴표로 감싸야 합니다.)

아래 중 하나로 해결하세요 — **1번을 가장 권장**합니다.

---

### 1) 사용자 홈 아래에 프로젝트 만들기 (권장)
관리자 권한 없이도 쓸 수 있는 위치로 옮겨 작업하세요.
```powershell
# PowerShell (일반 권한)
mkdir "$HOME\dev\projects"
cd "$HOME\dev\projects"
uv init myapp
```
이미 만든 폴더가 있다면 그 폴더로 이동만 하면 됩니다.

---

### 2) 꼭 Program Files를 써야 한다면 (비권장)
#### A. 관리자 권한 셸에서 실행
```powershell
# Windows Terminal / PowerShell을 '관리자 권한으로 실행'
cd "C:\Program Files\projects"
uv init
```
> 단점: 생성된 파일/폴더의 소유권이 꼬이기 쉽고, 매번 관리자 권한이 필요할 수 있어요.

#### B. 해당 폴더에 현재 사용자 ‘수정(Modify)’ 권한 부여
GUI 경로: 폴더 우클릭 → 속성(Properties) → 보안(Security) → 편집(Edit) → 사용자 선택 → “수정(Modify)” 체크 → 적용.  

CLI로 한 번에 주려면 (관리자 권한 셸):
```powershell
# 폴더가 없다면 먼저 생성
New-Item -ItemType Directory -Path "C:\Program Files\projects" -Force

# 현재 사용자에 Modify 권한 부여 (OI/CI는 하위 파일/폴더에 상속)
icacls "C:\Program Files\projects" /grant "$env:USERNAME:(OI)(CI)M"
```

---

### 3) 자주 생기는 실수 체크
- **경로 오타**: 폴더명은 `Program Files`입니다. `Programs Files`(s 붙음)로 만들면 엉뚱한 위치가 생겨 혼란이 옵니다.  
- **따옴표**: 공백 있는 경로는 항상 따옴표로 감싸세요.  
  ```powershell
  cd "C:\Program Files\projects"
  ```
- **권한 진단**: 아래가 실패하면 권한 문제입니다.
  ```powershell
  echo test > "C:\Program Files\projects\write_test.txt"
  ```

---

### (보너스) uv 기본 워크플로 빠르게 점검
```powershell
cd "$HOME\dev\projects\myapp"   # 권장 경로 사용
uv init                         # pyproject.toml 생성
uv venv --seed                  # .venv 만들고 pip 등 시드
uv add requests                 # 패키지 설치
uv run python -c "import requests; print(requests.__version__)"
```

필요하면 지금 작업 중인 정확한 경로와 실행한 명령어를 알려줘. 그 상태에서 가장 안전한 방법으로 바로잡아 줄게!

---
