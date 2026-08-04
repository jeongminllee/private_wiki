---
type: Setup Guide
title: "GitHub 비공개 저장소 접근"
description: "Infra - Linux & Remote - ChatGPT 대화 추출 노트 (2026-07-20)"
tags: [infra, chatgpt-export]
timestamp: 2026-07-20
status: active
---

# GitHub 비공개 저장소 접근

> **카테고리**: `Infra - Linux & Remote`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-07-20

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
깃허브에 private 해놓고 링크를 통해서만 접속 가능하게 할 수 있나?

### 💡 답변 (Assistant)
깃허브의 현재 접근 권한 모델을 기준으로, “링크를 아는 사람만” 가능한지와 가장 가까운 대안을 구분해서 확인하겠습니다.

---

### 💡 답변 (Assistant)
**GitHub의 비공개 저장소를 “링크를 아는 사람만 로그인 없이 접근”하도록 만드는 기능은 없습니다.**

### 가장 안전한 방법: Private 저장소 + Collaborator 초대

1. 저장소를 `Private`로 설정
2. 저장소의 `Settings`
3. `Collaborators`
4. `Add people`
5. 상대방의 GitHub 아이디 또는 이메일로 초대

상대방은 GitHub에 로그인하고 초대를 수락해야 저장소 링크로 접속할 수 있습니다. 단순히 URL만 전달받은 사람은 접근할 수 없습니다. citeturn132734view1

주의할 점은 **개인 계정 소유 저장소에서는 Collaborator에게 읽기 전용 권한을 줄 수 없다는 것**입니다. 초대된 Collaborator는 코드를 읽을 뿐만 아니라 `push`할 수 있는 쓰기 권한도 갖습니다. citeturn132734view3

### 상대방에게 읽기만 허용하려면

조직을 하나 만든 뒤 다음 형태로 운영하는 것이 좋습니다.

```text
GitHub Organization
└── Private Repository
    └── 상대방 권한: Read
```

Organization 저장소는 `Read`, `Triage`, `Write`, `Maintain`, `Admin`처럼 세분화된 권한을 설정할 수 있습니다. citeturn132734view0

### 정말 “URL을 아는 사람만” 열리게 하려면

`Secret Gist`가 비슷하게 동작합니다.

```text
Secret Gist URL → URL을 아는 사람은 누구나 열람
```

하지만 Secret Gist는 **비공개가 아닙니다**. 검색 결과에는 노출되지 않지만, URL이 유출되거나 추측되면 누구든 볼 수 있으므로 민감한 코드, 토큰, 회사 자료에는 적합하지 않습니다. citeturn132734view2

따라서 목적별 권장 방식은 다음과 같습니다.

- 특정 개발자와 협업: **개인 Private 저장소 + Collaborator**
- 코드 수정은 못 하게 하고 열람만 허용: **Organization + Private 저장소 + Read 권한**
- 보안이 중요하지 않은 짧은 코드 공유: **Secret Gist**
- 로그인 없이 링크와 비밀번호로 공유: GitHub 대신 별도의 파일 공유나 자체 웹 서버 필요

참고로 접근 권한을 나중에 제거하더라도, 상대방이 이미 로컬에 `clone`한 저장소 사본까지 회수할 수는 없습니다. citeturn132734view3

---
