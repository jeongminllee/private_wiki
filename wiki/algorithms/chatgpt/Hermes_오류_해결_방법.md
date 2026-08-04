---
type: Concept
title: "Hermes 오류 해결 방법"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-06-11)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-06-11
status: active
---

# Hermes 오류 해결 방법

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-11

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
hermes agent 돌리고 있는데
```
⚠️  API call failed (attempt 1/3): CodeAssistError [HTTP 404]
   🔌 Provider: google-gemini-cli  Model: gemini-3.5-flash
   🌐 Endpoint: cloudcode-pa://google
   📝 Error: HTTP 404: Code Assist 404: Requested entity was not found. is not available at cloudcode-pa.googleapis.com. It may have been renamed or retired. Check hermes_cli/models.py for the current list.
   ⏱️  Elapsed: 2.77s  Context: 2 msgs, ~8,945 tokens
⏳ Retrying in 2.3s (attempt 1/3)...
⚠️  API call failed (attempt 2/3): CodeAssistError [HTTP 404]
   🔌 Provider: google-gemini-cli  Model: gemini-3.5-flash
   🌐 Endpoint: cloudcode-pa://google
   📝 Error: HTTP 404: Code Assist 404: Requested entity was not found. is not available at cloudcode-pa.googleapis.com. It may have been renamed or retired. Check hermes_cli/models.py for the current list.
   ⏱️  Elapsed: 6.88s  Context: 2 msgs, ~8,945 tokens
⏳ Retrying in 5.3s (attempt 2/3)...
⚠️  API call failed (attempt 3/3): CodeAssistError [HTTP 404]
   🔌 Provider: google-gemini-cli  Model: gemini-3.5-flash
   🌐 Endpoint: cloudcode-pa://google
   📝 Error: HTTP 404: Code Assist 404: Requested entity was not found. is not available at cloudcode-pa.googleapis.com. It may have been renamed or retired. Check hermes_cli/models.py for the current list.
   ⏱️  Elapsed: 14.70s  Context: 2 msgs, ~8,945 tokens
❌ API failed after 3 retries — HTTP 404: Code Assist 404: Requested entity was not found. is not available at cloudcode-pa.googleapis.com. It may have been renamed or retired. Check hermes_cli/models.py for the current list.
   💀 Final error: HTTP 404: Code Assist 404: Requested entity was not found. is not available at cloudcode-pa.googleapis.com. It may have been renamed or retired. Check hermes_cli/models.py for the current list.
 ─  ⚕ Hermes  ─────────────────────────────────────────────────────────────────────────────────────────────────────────

     API call failed after 3 retries: HTTP 404: Code Assist 404: Requested entity was not found. is not available
     at cloudcode-pa.googleapis.com. It may have been renamed or retired. Check hermes_cli/models.py for the
     current list.
```
이런 오류가 나오네. 나한테 이런 오류를 해결할 수 있는 방법을 알려줘.

### 💡 답변 (Assistant)
원인상 **Hermes 자체 런타임 문제가 아니라, `google-gemini-cli` provider가 요청한 모델명 `gemini-3.5-flash`를 Code Assist endpoint에서 찾지 못하는 문제**로 보입니다. 모델명/provider/인증 경로를 같이 확인하는 순서로 잡아볼게요.

---

### 💡 답변 (Assistant)
이 오류의 핵심은 이겁니다.

`provider: google-gemini-cli`가 **Google AI Studio Gemini API가 아니라 Cloud Code Assist backend**인 `cloudcode-pa.googleapis.com` 쪽으로 요청을 보내고 있고, 그 endpoint에서 현재 계정/권한/지역/모델목록 기준으로 `gemini-3.5-flash`를 찾지 못해서 404가 난 겁니다. Hermes 공식 문서도 `google-gemini-cli` OAuth provider는 Gemini CLI/Cloud Code Assist backend를 쓰며, 안정적인 공식 경로는 API key 기반 `provider: gemini`라고 설명합니다. citeturn849607view0

## 가장 권장하는 해결책: `google-gemini-cli` 말고 `gemini` provider로 바꾸기

Hermes 설정을 API key 기반 Gemini provider로 바꾸세요.

### 1. Google AI Studio API key 준비

Google AI Studio에서 API key를 만든 다음 `~/.hermes/.env`에 넣습니다.

```bash
mkdir -p ~/.hermes
nano ~/.hermes/.env
```

아래 중 하나를 추가합니다.

```bash
GOOGLE_API_KEY=여기에_본인_API_KEY
```

또는

```bash
GEMINI_API_KEY=여기에_본인_API_KEY
```

Hermes 문서상 `gemini` provider는 둘 다 확인합니다. citeturn849607view0

### 2. Hermes 모델 설정 다시 하기

```bash
hermes model
```

선택 흐름은 대략 이렇게 가면 됩니다.

```text
More providers...
→ Google AI Studio
→ 사용 가능한 Gemini 모델 선택
```

Hermes 공식 문서도 이 경로를 “lowest-risk official API path”로 권장합니다. citeturn849607view0

### 3. 직접 config를 고치는 방법

`~/.hermes/config.yaml`을 열어서 현재 이런 식으로 되어 있을 가능성이 큽니다.

```yaml
model:
  default: gemini-3.5-flash
  provider: google-gemini-cli
  base_url: cloudcode-pa://google
```

이걸 아래처럼 바꿔보세요.

```yaml
model:
  default: gemini-3.5-flash
  provider: gemini
  base_url: https://generativelanguage.googleapis.com/v1beta
```

`gemini-3.5-flash` 자체는 Gemini API 공식 모델 ID가 맞습니다. Google 문서에도 model code가 `gemini-3.5-flash`로 되어 있습니다. citeturn779323view0  
문제는 **모델명이 틀렸다기보다, 지금 Hermes가 잘못된 provider/backend 조합으로 호출하고 있다는 점**에 가깝습니다.

## 빠른 진단 명령어

아래 순서대로 확인하세요.

```bash
hermes doctor
```

Hermes 문서 기준으로 `hermes doctor`는 API key 존재 여부, OAuth credential 존재 여부, provider credential 해석 가능 여부를 확인합니다. citeturn849607view0

현재 설정 확인:

```bash
cat ~/.hermes/config.yaml
cat ~/.hermes/.env
```

특히 이 값들이 있으면 주의하세요.

```bash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

Hermes 문서에서는 OpenAI-compatible endpoint override가 있으면 제거하거나 native endpoint로 바꾸라고 안내합니다. citeturn849607view0

바꿀 값:

```bash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

또는 아예 `GEMINI_BASE_URL` 줄을 삭제해도 됩니다.

## 그래도 `google-gemini-cli` OAuth를 꼭 쓰고 싶다면

가능은 하지만 권장도는 낮습니다. Google Code Assist 쪽은 계정/라이선스/대기열/릴리즈 채널 영향을 받습니다. Google 문서상 Gemini Code Assist에서 Gemini 3 계열 접근은 구독 종류와 preview channel 설정에 따라 달라집니다. 예를 들어 Gemini Code Assist for individuals는 일부 waitlist 사용자에게 제공된다고 되어 있습니다. citeturn849607view2

즉, `google-gemini-cli` provider를 계속 쓰면 아래 문제가 생길 수 있습니다.

```text
모델은 공식 Gemini API에는 존재함
하지만 Cloud Code Assist backend에서는 내 계정에 안 열려 있음
→ HTTP 404 Requested entity was not found
```

그래서 OAuth를 계속 쓸 경우에는 Hermes 안에서 모델을 바꿔보세요.

```text
/model gemini-3-flash-preview
/model gemini-flash-latest
/model gemini-3-pro-preview
/model gemini-pro-latest
```

Hermes 문서에도 `/model`로 세션 중 모델 변경이 가능하다고 안내되어 있습니다. citeturn849607view0

다만 지금 로그의 `cloudcode-pa://google` 404는 재시도해도 해결될 종류가 아닙니다. 실제로 Hermes GitHub issue에도 같은 형태의 `CodeAssistError [HTTP 404]`, `cloudcode-pa.googleapis.com`, `Check hermes_cli/models.py` 오류가 보고되어 있습니다. citeturn849607view1

## 내가 추천하는 최종 수정안

가장 깔끔하게는 이렇게 하세요.

```bash
# 1. Hermes 최신화
pipx upgrade hermes-agent 2>/dev/null || pip install -U hermes-agent

# 2. API key 저장
mkdir -p ~/.hermes
nano ~/.hermes/.env
```

`~/.hermes/.env`:

```bash
GOOGLE_API_KEY=본인_API_KEY
```

`~/.hermes/config.yaml`:

```yaml
model:
  default: gemini-3.5-flash
  provider: gemini
  base_url: https://generativelanguage.googleapis.com/v1beta
```

그 다음:

```bash
hermes doctor
hermes chat
```

## 결론

현재 에러의 직접 원인은:

```text
provider: google-gemini-cli
endpoint: cloudcode-pa://google
model: gemini-3.5-flash
```

이 조합에서 **Cloud Code Assist가 해당 모델을 네 계정에 제공하지 않거나, Hermes의 OAuth provider 모델 매핑이 현재 Code Assist backend와 맞지 않기 때문**입니다.

실전 해결은:

```text
google-gemini-cli → gemini
cloudcode-pa://google → https://generativelanguage.googleapis.com/v1beta
OAuth → GOOGLE_API_KEY
```

로 바꾸는 것입니다. 이게 제일 안정적입니다.

---
