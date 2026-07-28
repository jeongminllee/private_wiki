---
type: Reference
title: "Codex의 플러그인, Sites, 시각적 주석"
description: "코딩 밖의 반복 업무를 패키징하고 내부 앱을 배포하며 화면 요소에 직접 피드백하는 Codex 기능 발표"
resource: https://discuss.pytorch.kr/t/openai-codex/10521
notion: https://app.notion.com/p/3771a73cf20b81a0a5a0ef4a6dd2c072
tags: [reading, codex, plugins, internal-tools]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

2026년 6월 발표는 Codex를 코드 작성 도구에서 역할별 업무 실행 환경으로 넓히는 세 기능을 묶었다. 플러그인은 지침과 연결 앱, 템플릿, 작업 흐름을 재사용 가능한 묶음으로 만들고, Sites는 JavaScript/TypeScript 기반 내부 앱을 생성·배포하며, 시각적 주석은 브라우저 화면의 특정 요소를 가리켜 수정 요청을 전달한다.

# 기능별 의미

- **플러그인**: 조직이나 개인의 반복 작업을 스킬, 앱, 템플릿과 함께 배포한다. 연결된 앱의 기존 권한을 사용하며 플러그인 설치 자체가 원본 시스템의 새 권한을 주는 것은 아니다.
- **Sites**: 대화에서 만든 앱을 저장된 버전으로 관리하고 공유 URL에 배포한다. 간단한 대시보드, 승인 도구, 추적기처럼 업무 데이터와 연결된 내부 도구에 적합하다.
- **시각적 주석**: DOM 요소나 화면 영역을 지목해 “여기를 바꿔 달라”는 피드백을 맥락과 함께 보낸다. 디자인 수정의 좌표와 대상을 말로 설명하는 비용을 줄인다.

# 사용할 때 확인할 것

플러그인은 무엇을 자동화하는지뿐 아니라 어떤 변경에서 승인을 요구하는지 정해야 한다. Sites의 배포 URL은 시험용 미리보기처럼 보여도 실제 공유 가능한 배포이므로 접근 제어, 비밀 값, 데이터 범위와 버전 확인이 필요하다. 시각적 주석도 의도를 완전히 설명하지 않으므로 수정 후 반응형 화면과 동작을 별도로 검증한다.

# 시점 주의

저장된 글은 2026년 6월의 발표 시점을 반영한다. 이후 앱 디렉터리와 플러그인 디렉터리의 명칭과 제공 방식이 바뀌었으므로 실제 사용법과 요금제·지역별 가용성은 현재 공식 문서를 우선해야 한다.

# 출처

- [OpenAI 플러그인 도움말](https://help.openai.com/en/articles/20001256-plugins-in-codex)
- [OpenAI 비즈니스 릴리스 노트](https://help.openai.com/en/articles/10128477-chatgpt-enterprise-edu-release-notes)
- [저장된 PyTorchKR 소개](https://discuss.pytorch.kr/t/openai-codex/10521)
- [Notion 원본 항목](https://app.notion.com/p/3771a73cf20b81a0a5a0ef4a6dd2c072)

