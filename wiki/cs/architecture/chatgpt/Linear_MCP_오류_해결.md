---
type: Concept
title: "Linear MCP 오류 해결"
description: "CS - Software Architecture - ChatGPT 대화 추출 노트 (2026-06-04)"
tags: [cs, chatgpt-export]
timestamp: 2026-06-04
status: active
---

# Linear MCP 오류 해결

> **카테고리**: `CS - Software Architecture`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-04

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
먼저 오류 메시지의 핵심인 **`Unsupported entity reference`**가 Linear 쪽 식별자 문제인지, MCP 서버/클라이언트 간 포맷 문제인지 분리해서 보겠습니다. Codex + Linear MCP 조합에서는 “무엇을 참조했는지”가 거의 항상 원인 후보예요.

---

### ❓ 질문 (User)
Error code: INVALID_ARGUMENT; Error: RuntimeException: Error calling MCP
        tool: [TextContent(type='text', text='Error: Unsupported entity
        reference', annotations=None, meta=None)]

코덱스 사용중 linear 앱에 접근 하려니까 이런 오류가 나타났어. 해결방법 알려줘.

### 💡 답변 (Assistant)
이 오류는 **Linear 연결 자체가 완전히 실패했다기보다는, Codex가 Linear MCP tool을 호출할 때 “참조값/인자 형식”을 잘못 넘긴 상황**에 가깝습니다.

특히 메시지의 핵심은 이것입니다.

```text
INVALID_ARGUMENT
Error calling MCP tool
Error: Unsupported entity reference
```

즉, Linear MCP가 기대하는 `issue id`, `team id`, `project id`, `assignee id`, `parent id` 같은 **엔티티 참조값**이 아닌 값을 넘겼을 가능성이 큽니다. 예를 들어 `LIN-123` 같은 사람이 보는 이슈 키를 내부 ID가 필요한 필드에 넣거나, `me`, `Foundation`, `In Review` 같은 이름 문자열을 그대로 넣으면 이런 류의 오류가 날 수 있습니다.

---

## 1. 먼저 설정이 맞는지 확인

Linear 공식 문서 기준으로 Codex CLI에서는 아래처럼 추가하는 방식이 권장됩니다. citeturn127912view0

```bash
codex mcp add linear --url https://mcp.linear.app/mcp
codex mcp login linear
```

`~/.codex/config.toml`에는 최소한 이렇게 들어가 있어야 합니다.

```toml
[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
```

Linear 쪽 문서에서는 처음 MCP를 쓰는 경우 `rmcp_client` 기능을 켜야 한다고 안내합니다. citeturn127912view1

```toml
[features]
rmcp_client = true

[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
```

설정 후 다시 로그인하세요.

```bash
codex mcp login linear
```

---

## 2. 읽기부터 테스트

바로 “이슈 생성/수정”을 시도하지 말고, 먼저 읽기 동작이 되는지 확인하세요.

Codex에게 이렇게 시켜보세요.

```text
Linear MCP가 연결되어 있는지 확인해줘.
내 Linear teams 목록을 조회하고, 각 team의 name과 id를 보여줘.
```

그다음:

```text
Linear에서 최근 issue 5개를 조회하고, issue key, title, internal id를 보여줘.
```

여기서 **조회는 되는데 생성/수정만 실패**한다면, 연결 문제보다는 tool call 인자 직렬화 또는 잘못된 entity reference 문제일 가능성이 큽니다. 실제로 Cursor 쪽 Linear MCP 사례에서도 읽기 도구는 성공하지만 생성 도구에서 인자가 누락되거나 JSON이 망가지는 문제가 보고되었고, 원인은 `arguments` 객체가 비거나 잘못 전달되는 쪽으로 설명되어 있습니다. citeturn127912view2

---

## 3. 가장 흔한 원인: `LIN-123` 같은 issue key를 잘못된 필드에 넣음

Linear에는 보통 두 종류의 식별자가 있습니다.

```text
사람이 보는 이슈 키: LIN-123, FND-34
내부 엔티티 ID: uuid 형태 또는 Linear API가 반환하는 id
```

문제는 MCP tool에 따라 `issueId`, `parentId`, `teamId`, `projectId` 같은 필드가 **사람이 보는 키가 아니라 내부 id**를 요구할 수 있다는 점입니다.

따라서 Codex에게 바로 이렇게 시키면 실패할 수 있습니다.

```text
Linear에 parentId를 LIN-123으로 해서 새 이슈 만들어줘
```

대신 이렇게 시키는 게 안전합니다.

```text
먼저 Linear에서 LIN-123 이슈를 조회해서 내부 id를 확인해.
그 다음 그 내부 id를 parentId로 사용해서 새 이슈를 만들어.
team도 이름이 아니라 team id를 조회해서 사용해.
모든 MCP tool call은 arguments 객체 안에 명시적인 JSON 값으로 넣어.
```

---

## 4. Codex에 붙여 넣을 “안전 프롬프트”

Codex에게 Linear 작업을 시킬 때 아래 문장을 먼저 넣어보세요.

```text
Linear MCP를 호출할 때는 사람이 보는 이름이나 issue key를 내부 id가 필요한 필드에 직접 넣지 마라.

작업 순서:
1. 먼저 필요한 team, project, issue, assignee, state를 조회한다.
2. 조회 결과에서 MCP가 반환한 실제 id 값을 사용한다.
3. issue key 예: LIN-123, FND-34는 먼저 조회용으로만 사용한다.
4. parentId, teamId, projectId, assigneeId, stateId에는 조회된 내부 id만 넣는다.
5. Linear MCP tool call은 반드시 arguments 객체 안에 모든 인자를 넣는다.
6. "me", "current user", 팀 이름, 상태 이름을 id 필드에 직접 넣지 않는다.
```

생성 요청은 이렇게 구체화하세요.

```text
Linear에서 새 이슈를 만들어줘.

단, 바로 생성하지 말고:
1. team "Backend"의 team id를 먼저 조회해.
2. assignee가 필요하면 내 Linear user id를 먼저 조회해.
3. parent issue가 있으면 "LIN-123"을 먼저 조회해서 내부 id를 가져와.
4. 그 다음 create issue tool을 호출해.

title: ...
description: ...
teamId: 조회한 team id 사용
parentId: 조회한 parent issue 내부 id 사용
assigneeId: 조회한 user id 사용
```

---

## 5. `arguments` 누락/직렬화 문제 우회

최근 MCP 클라이언트들에서 자동 tool call 시 인자가 비거나 깨지는 문제가 보고된 사례가 있습니다. 해당 사례에서는 `CallMcpTool` 호출 시 반드시 `arguments` 객체에 모든 값을 넣으라는 규칙을 추가하고, Auto 모델 대신 다른 모델을 써보는 것이 우회책으로 제시되었습니다. citeturn127912view2

Codex 설정이나 프로젝트 규칙 파일에 이런 규칙을 넣어보세요.

```text
When calling Linear MCP tools, always pass all parameters inside the arguments object.
Never call a Linear MCP tool with missing, empty, or top-level-only arguments.
Do not pass human-readable issue keys, names, or "me" into fields ending with Id.
Resolve them first by querying Linear, then use the returned id.
```

---

## 6. 그래도 안 되면 재인증/재등록

설정 문제 가능성도 있으니 한 번 깔끔하게 다시 연결해보는 것도 좋습니다.

```bash
codex mcp login linear
```

안 되면 `~/.codex/config.toml`에서 Linear MCP 설정을 확인한 뒤, 다시 추가합니다.

```bash
codex mcp add linear --url https://mcp.linear.app/mcp
codex mcp login linear
```

Linear 공식 문서도 CLI/IDE Extension 모두 같은 설정을 공유한다고 설명합니다. citeturn127912view1

---

## 결론

지금 오류의 1순위 원인은 이것입니다.

```text
Codex가 Linear MCP tool에 잘못된 entity reference를 넘김
예: teamId에 팀 이름, parentId에 LIN-123, assigneeId에 me 같은 값
```

해결 방향은:

```text
조회 → 내부 id 확인 → 그 id로 생성/수정
```

그리고 Codex에게 **“Linear MCP 호출 시 반드시 arguments 객체를 채우고, id 필드에는 조회된 실제 id만 넣어라”**고 명시하면 성공률이 확 올라갈 가능성이 큽니다.

---
