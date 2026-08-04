---
type: Setup Guide
title: "Docker 컨테이너 정지 명령"
description: "Infra - Cloud & DevOps - ChatGPT 대화 추출 노트 (2024-07-06)"
tags: [infra, chatgpt-export]
timestamp: 2024-07-06
status: active
---

# Docker 컨테이너 정지 명령

> **카테고리**: `Infra - Cloud & DevOps`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-07-06

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
docker 컨테이너를 정지시키는 명령어 알려줘

### 💡 답변 (Assistant)
Docker 컨테이너를 정지시키는 명령어는 다음과 같습니다:

```sh
docker stop <컨테이너_ID 또는 컨테이너_이름>
```

예를 들어, 컨테이너 ID가 `abc123`인 컨테이너를 정지시키려면 다음과 같이 입력합니다:

```sh
docker stop abc123
```

또는 컨테이너 이름이 `my_container`인 컨테이너를 정지시키려면 다음과 같이 입력합니다:

```sh
docker stop my_container
```

정지된 컨테이너를 다시 시작하려면 `docker start <컨테이너_ID 또는 컨테이너_이름>` 명령어를 사용합니다.

---
