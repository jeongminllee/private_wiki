---
type: Concept
title: "LM Studio API 오류"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-06-12)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-06-12
status: active
---

# LM Studio API 오류

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-12

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
로그상 핵심은 Hermes가 LM Studio의 OpenAI-compatible streaming 응답을 기다렸는데, 서버가 SSE 스트림을 열었다가 정상 종료 신호 없이 빈 스트림으로 끝냈다는 점입니다. 원인을 “모델 문제 / 컨텍스트 길이 / LM Studio 서버 설정 / Hermes 파서 호환성” 순서로 좁혀보겠습니다.

---

### ❓ 질문 (User)
⚠️  API call failed (attempt 1/3): RuntimeError
   🔌 Provider: lmstudio  Model: openai/gpt-oss-20b
   🌐 Endpoint: http://127.0.0.1:1234
   📝 Error: Provider returned an empty stream with no finish_reason (possible upstream error or malformed SSE response).
   ⏱️  Elapsed: 0.33s  Context: 2 msgs, ~9,366 tokens
⏳ Retrying in 2.7s (attempt 1/3)...
⚠️  API call failed (attempt 2/3): RuntimeError
   🔌 Provider: lmstudio  Model: openai/gpt-oss-20b
   🌐 Endpoint: http://127.0.0.1:1234
   📝 Error: Provider returned an empty stream with no finish_reason (possible upstream error or malformed SSE response).
   ⏱️  Elapsed: 3.16s  Context: 2 msgs, ~9,366 tokens
⏳ Retrying in 5.7s (attempt 2/3)...
⚠️  API call failed (attempt 3/3): RuntimeError
   🔌 Provider: lmstudio  Model: openai/gpt-oss-20b
   🌐 Endpoint: http://127.0.0.1:1234
   📝 Error: Provider returned an empty stream with no finish_reason (possible upstream error or malformed SSE response).
   ⏱️  Elapsed: 9.02s  Context: 2 msgs, ~9,366 tokens
❌ API failed after 3 retries — Provider returned an empty stream with no finish_reason (possible upstream error or malformed SSE response).
   💀 Final error: Provider returned an empty stream with no finish_reason (possible upstream error or malformed SSE response).
 ─  ⚕ Hermes  ─────────────────────────────────────────────────────────────────────────────────────────────────────────

     API call failed after 3 retries: Provider returned an empty stream with no finish_reason (possible upstream
     error or malformed SSE response).

### 💡 답변 (Assistant)
이 오류는 **Hermes 자체 로직 실패라기보다, LM Studio 쪽 OpenAI-compatible API가 Hermes가 기대하는 streaming 형식으로 응답을 못 준 상황**에 가깝습니다.

핵심 메시지:

```text
Provider returned an empty stream with no finish_reason
possible upstream error or malformed SSE response
```

즉 Hermes가 LM Studio에 요청을 보냈고, LM Studio가 **SSE streaming 응답을 시작했지만 토큰도 거의 안 주고, `finish_reason`도 없이 종료**한 것입니다. LM Studio의 OpenAI-compatible API는 보통 `http://localhost:1234/v1` 형태의 base URL을 쓰고, `stream: true`일 때 SSE로 응답합니다. citeturn612525search2turn612525search9

---

## 1순위로 볼 원인

로그에서 가장 수상한 부분은 이것입니다.

```text
Provider: lmstudio
Model: openai/gpt-oss-20b
Endpoint: http://127.0.0.1:1234
Context: 2 msgs, ~9,366 tokens
```

가능성이 높은 순서로 보면:

1. **Hermes 설정의 LM Studio endpoint가 `/v1` 없이 잡혀 있음**
2. **LM Studio에서 `openai/gpt-oss-20b` 모델이 제대로 로드되지 않았거나 이름이 다름**
3. **streaming 응답 호환성 문제**
4. **컨텍스트 길이 / VRAM 부족 / 모델 런타임 크래시**
5. **tool calling 또는 reasoning 출력 형식을 LM Studio가 제대로 OpenAI 형식으로 파싱하지 못함**

LM Studio 공식 문서의 OpenAI-compatible 예시는 base URL을 `http://localhost:1234/v1`로 설정합니다. citeturn612525search2  
그래서 Hermes 설정에 endpoint가 `http://127.0.0.1:1234`로만 들어가 있다면, 먼저 `http://127.0.0.1:1234/v1`로 바꿔보세요.

---

## 바로 해볼 해결 순서

### 1. LM Studio 서버가 정상 응답하는지 확인

터미널에서:

```bash
curl http://127.0.0.1:1234/v1/models
```

정상이라면 로드 가능한 모델 목록이 JSON으로 나와야 합니다.

그다음 non-streaming 테스트:

```bash
curl http://127.0.0.1:1234/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"openai/gpt-oss-20b\",\"messages\":[{\"role\":\"user\",\"content\":\"hello\"}],\"stream\":false}"
```

PowerShell이면 이쪽이 더 편합니다.

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:1234/v1/chat/completions" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{
    "model": "openai/gpt-oss-20b",
    "messages": [{"role": "user", "content": "hello"}],
    "stream": false
  }'
```

여기서도 실패하면 Hermes 문제가 아니라 **LM Studio 서버 / 모델 로딩 / 모델명 문제**입니다.

---

### 2. Hermes의 LM Studio endpoint를 `/v1` 포함으로 수정

Hermes 설정 파일에서 LM Studio provider 부분이 대략 이런 식이면:

```yaml
endpoint: http://127.0.0.1:1234
```

이렇게 바꿔보세요.

```yaml
endpoint: http://127.0.0.1:1234/v1
```

혹은 Hermes가 내부적으로 `/v1`을 붙이는 구조라면 중복될 수 있으니, 둘 다 테스트해보는 게 좋습니다. 다만 OpenAI-compatible client 기준으로는 `/v1`이 들어가는 쪽이 정석입니다. citeturn612525search2

---

### 3. 모델명을 LM Studio에 표시되는 정확한 identifier로 바꾸기

LM Studio에서 모델 이름이 `openai/gpt-oss-20b`로 보이더라도 API identifier가 다를 수 있습니다. 먼저:

```bash
curl http://127.0.0.1:1234/v1/models
```

출력에서 실제 `id` 값을 확인하세요.

예를 들어 이렇게 나오면:

```json
{
  "id": "gpt-oss-20b"
}
```

Hermes 설정도:

```yaml
model: gpt-oss-20b
```

로 맞춰야 합니다.

---

### 4. streaming을 꺼서 테스트

현재 오류는 streaming SSE 쪽에서 발생합니다. LM Studio는 streaming을 SSE로 보내고, 일부 OpenAI-compatible 클라이언트는 provider별 streaming 차이에 민감합니다. LM Studio bug tracker에도 streaming + tool call 파싱 관련 이슈가 보고된 적이 있습니다. citeturn612525search1turn612525search9

Hermes 설정에서 가능하다면:

```yaml
stream: false
```

또는 비슷한 옵션을 꺼보세요.

만약 non-streaming에서는 정상인데 streaming에서만 실패한다면 원인은 거의 확실히 **LM Studio streaming 응답 형식과 Hermes parser의 호환성 문제**입니다.

---

### 5. 컨텍스트를 줄여서 테스트

로그에:

```text
Context: 2 msgs, ~9,366 tokens
```

라고 되어 있습니다. 9k 토큰 자체가 엄청 큰 건 아니지만, 로컬 모델에서는 다음 조건에 따라 실패할 수 있습니다.

```text
모델 context length 설정이 낮음
VRAM 부족
KV cache 부족
GPU offload 부족
LM Studio가 모델을 JIT 로딩하다가 실패
prompt template 문제
```

먼저 아주 짧은 프롬프트로 테스트하세요.

```text
hello
```

이건 되는데 Hermes 작업만 실패하면, `max_context`, `context_length`, `max_tokens`, `tools`, `reasoning_effort` 쪽 문제일 가능성이 큽니다.

---

## 내가 추천하는 Hermes 설정 방향

LM Studio + Hermes 조합이면 우선 이렇게 단순화해서 테스트하세요.

```yaml
provider: lmstudio
base_url: http://127.0.0.1:1234/v1
model: 실제 /v1/models 에서 나온 id
stream: false
max_tokens: 1024
temperature: 0.2
```

그다음 정상 동작하면 하나씩 올립니다.

```yaml
stream: true
max_tokens: 4096
context_length: 8192 또는 16384
```

---

## 특히 Windows라면 추가 체크

Windows에서 Hermes Desktop streaming 응답이 중간에 잘리는 문제가 보고된 이슈도 있습니다. 해당 이슈는 Python의 Windows ProactorEventLoop와 HTTPX streaming 연결 호환성을 원인 후보로 언급합니다. citeturn612525search11

그래서 Windows 환경이라면 우회 순서는 이렇습니다.

```text
1. stream: false
2. LM Studio 최신 버전 업데이트
3. Hermes 최신 버전 업데이트
4. 가능하면 WSL/Linux 쪽에서 Hermes 실행
5. LM Studio 서버는 Windows에서 켜고 Hermes만 WSL에서 붙여보기
```

WSL에서 Windows LM Studio에 붙을 때는 `127.0.0.1` 대신 Windows host IP가 필요할 수 있습니다.

---

## 결론

이번 오류는 이전의 `gemini-3.5-flash 404`처럼 “모델 이름이 사라짐” 문제와는 다릅니다. 이번에는 **LM Studio가 Hermes에게 정상적인 streaming completion을 끝까지 반환하지 못한 문제**입니다.

가장 먼저 이 3개만 해보세요.

```bash
curl http://127.0.0.1:1234/v1/models
```

Hermes endpoint:

```text
http://127.0.0.1:1234/v1
```

그리고 임시로:

```yaml
stream: false
```

이 3개로 해결되면, 원인은 거의 **LM Studio OpenAI-compatible streaming 호환성** 쪽입니다.

---
