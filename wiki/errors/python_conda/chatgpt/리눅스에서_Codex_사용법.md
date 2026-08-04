---
type: Error Note
title: "리눅스에서 Codex 사용법"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-07-26)"
tags: [errors, chatgpt-export]
timestamp: 2026-07-26
status: active
---

# 리눅스에서 Codex 사용법

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-07-26

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
리눅스 환경에서는 codex 어떻게 쓰는지 찾아서 알려줘

### 💡 답변 (Assistant)
최신 공식 문서를 기준으로 확인해볼게요. `openai-docs` 스킬을 사용해서 리눅스에서 Codex를 설치하고 로그인한 뒤 실제로 프로젝트에서 쓰는 흐름까지 정리하겠습니다.

---

### 💡 답변 (Assistant)
리눅스에서는 보통 **Codex CLI**를 터미널에서 사용합니다. 공식 데스크톱 앱은 현재 macOS·Windows 중심이고, Linux는 CLI 또는 VS Code 확장이 가장 자연스럽습니다.

## 1. Ubuntu에서 설치

이전에 사용한다고 했던 Ubuntu 24.04 기준입니다.

```bash
sudo apt update
sudo apt install -y curl git bubblewrap

curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

설치 확인:

```bash
codex --version
```

만약 `codex: command not found`가 나오면:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

계속 적용하려면:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

OpenAI도 Linux에서는 위의 독립 실행형 설치 방식을 우선 안내합니다. Node.js나 npm을 별도로 설치할 필요가 없다는 장점이 있습니다. [Codex CLI 공식 설치 문서](https://developers.openai.com/codex/cli)

## 2. 로그인

### 일반 데스크톱 Linux

```bash
codex login
```

브라우저가 열리면 현재 사용 중인 ChatGPT 계정으로 로그인합니다. ChatGPT 구독에 포함된 Codex 사용량을 이용하려면 이 방식이 편합니다.

로그인 확인:

```bash
codex login status
```

### SSH 서버처럼 브라우저가 없는 환경

```bash
codex login --device-auth
```

화면에 표시되는 주소와 코드를 로컬 PC 브라우저에서 입력하면 됩니다.

### API 키로 사용

```bash
export OPENAI_API_KEY="발급받은_API_KEY"
printenv OPENAI_API_KEY | codex login --with-api-key
unset OPENAI_API_KEY
```

API 키 로그인은 ChatGPT 구독 사용량이 아니라 **OpenAI API 사용량으로 별도 과금**됩니다. 개인적인 로컬·서버 작업은 ChatGPT 로그인, CI/CD 자동화는 API 키 방식이 일반적입니다. [Codex 인증 공식 문서](https://developers.openai.com/codex/auth)

## 3. 프로젝트에서 실행

Codex는 실행한 디렉터리를 작업공간으로 인식합니다.

```bash
cd ~/projects/my-project
git status
codex
```

실행 후 다음처럼 자연어로 요청하면 됩니다.

```text
이 프로젝트 구조를 분석하고 실행 방법을 알려줘.
```

```text
pytest를 실행해서 실패 원인을 찾고 수정해줘.
수정 전에는 어떤 파일을 바꿀지 먼저 설명해줘.
```

```text
현재 변경사항을 리뷰해줘. 버그와 보안 문제를 우선해서 확인해.
```

처음 사용하는 저장소라면 `/init`을 실행해 `AGENTS.md`를 만드는 것도 좋습니다.

```text
/init
```

`AGENTS.md`에는 프로젝트 전용 규칙을 적습니다.

```markdown
# Project instructions

- Python 3.12를 사용한다.
- 패키지 관리는 uv를 사용한다.
- 모든 함수에 타입 어노테이션을 작성한다.
- 수정 후 uv run pytest를 실행한다.
- 사용자가 요청하지 않은 대규모 리팩터링은 하지 않는다.
```

## 4. 자주 사용하는 명령

| 명령 | 용도 |
|---|---|
| `codex` | 대화형 Codex 실행 |
| `codex "요청 내용"` | 첫 요청과 함께 실행 |
| `codex resume` | 이전 작업 이어서 진행 |
| `codex review` | 현재 코드 변경사항 리뷰 |
| `codex exec "요청"` | 비대화형으로 한 번 실행 |
| `codex doctor` | 설치·인증·설정 문제 진단 |
| `codex logout` | 로그인 정보 삭제 |

Codex 화면 안에서는 다음 명령이 유용합니다.

| 슬래시 명령 | 기능 |
|---|---|
| `/init` | `AGENTS.md` 생성 |
| `/status` | 현재 모델·권한·작업 디렉터리 확인 |
| `/permissions` | 파일 수정·명령 실행 권한 조정 |
| `/model` | 모델과 추론 수준 선택 |
| `/review` | 변경사항 검토 |
| `/exit` | 종료 |

전체 CLI 명령은 [Codex CLI 명령어 문서](https://developers.openai.com/codex/developer-commands)에서 확인할 수 있습니다.

## 5. 처음에는 이 권한으로 실행하는 것을 추천

```bash
codex \
  --sandbox workspace-write \
  --ask-for-approval on-request
```

이렇게 하면 Codex가 현재 프로젝트 내부는 수정할 수 있지만, 작업공간 밖을 건드리거나 추가 권한이 필요한 작업은 확인을 요청합니다.

분석만 시키고 싶다면:

```bash
codex --sandbox read-only
```

`--yolo` 또는 `--dangerously-bypass-approvals-and-sandbox`는 승인과 샌드박스를 해제하므로, 격리된 컨테이너가 아니라면 사용하지 않는 편이 안전합니다. [Codex 샌드박스·승인 문서](https://developers.openai.com/codex/agent-approvals-security)

## 6. Ubuntu 24.04에서 샌드박스 경고가 나오는 경우

먼저 다음을 설치합니다.

```bash
sudo apt install -y bubblewrap
```

그래도 user namespace 또는 AppArmor 경고가 나오면:

```bash
sudo apt install -y apparmor-profiles apparmor-utils

sudo install -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict

sudo apparmor_parser -r \
  /etc/apparmor.d/bwrap-userns-restrict
```

Ubuntu 24.04에서는 이 AppArmor 설정이 추가로 필요할 수 있습니다. [Linux 샌드박스 공식 문서](https://developers.openai.com/codex/concepts/sandboxing)

## 가장 간단한 전체 흐름

```bash
sudo apt update
sudo apt install -y curl git bubblewrap

curl -fsSL https://chatgpt.com/codex/install.sh | sh

export PATH="$HOME/.local/bin:$PATH"

codex login

cd ~/projects/my-project
codex
```

결론적으로, 지금 사용하는 Ubuntu 머신에서는 **프로젝트 디렉터리로 이동한 다음 `codex`를 실행하는 방식**으로 쓰면 됩니다. 원격 GPU 서버에서 사용한다면 로그인만 `codex login --device-auth`로 바꾸면 됩니다.

---

### ❓ 질문 (User)
그냥 vscode 터미널에서 codex 치니까 바로 뭐 나오는데 이건 왜이런거야

### 💡 답변 (Assistant)
`codex` 명령이 이미 설치되어 있고 VS Code 터미널의 `PATH`에서 발견된 상태라는 뜻입니다. 어느 설치본이 실행된 것인지 확인하면 이유가 바로 드러납니다.

---

### 💡 답변 (Assistant)
정상이에요. `codex` 명령이 이미 설치되어 있고, VS Code 터미널이 그 실행 파일을 `PATH`에서 찾은 것입니다. 다시 설치할 필요 없습니다.

어디에 설치된 Codex인지 확인해보세요.

```bash
command -v codex
codex --version
codex login status
```

더 자세히 보려면:

```bash
type -a codex
readlink -f "$(command -v codex)"
```

경로에 따라 설치 출처를 대략 알 수 있습니다.

- `~/.local/bin/codex` → 공식 설치 스크립트로 설치
- `~/.nvm/.../bin/codex` → npm으로 설치
- `/usr/local/bin/codex` → 시스템 전역 설치
- VS Code 확장 디렉터리 → 확장에 포함된 실행 파일일 가능성

로그인 과정도 안 나왔다면 Codex IDE 확장이나 이전 CLI 사용 때 저장한 인증정보가 남아 있기 때문일 가능성이 큽니다. CLI와 VS Code 확장은 인증정보와 `~/.codex/config.toml` 설정을 공유합니다. [공식 인증 문서](https://developers.openai.com/codex/auth)

화면에 다음과 비슷한 내용이 떴다면 이미 사용할 준비가 끝난 상태입니다.

```text
OpenAI Codex
model: ...
directory: ...
```

이제 프로젝트 폴더에서 실행하면 됩니다.

```bash
cd 프로젝트경로
codex
```

그리고 다음처럼 요청하면 됩니다.

```text
이 프로젝트 구조를 분석하고 실행 방법을 알려줘.
```

```text
테스트를 실행해서 실패 원인을 분석하고 수정해줘.
```

즉, **VS Code라서 특별히 실행된 것이 아니라, VS Code 터미널도 일반 Linux 셸이기 때문에 이미 설치된 `codex`를 찾아 실행한 것**입니다. 화면이 제대로 열렸다면 그대로 사용하면 됩니다.

---
