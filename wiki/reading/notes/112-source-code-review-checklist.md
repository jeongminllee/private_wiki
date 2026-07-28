---
type: Reference
title: "소스코드 검토 체크리스트"
description: "가독성·구조·오류 처리와 입력 검증·권한·비밀정보를 함께 확인하는 코드 리뷰 기준"
resource: https://www.youtube.com/watch?v=IGXDHv9Xn6k
notion: https://app.notion.com/p/1471a73cf20b8279a2d1019d31ed8c1c
tags: [reading, code-review, clean-code, application-security]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

코드 리뷰를 형식과 이름만 보는 clean code 점검, 그리고 외부 입력과 권한 경계를 보는 secure coding 점검으로 나눈다. checklist는 사고를 돕는 출발점이며, 실제 요구와 threat model, 실행 가능한 테스트를 대신하지 않는다.

# 품질 체크

- formatter와 프로젝트 convention이 일관적인가?
- 이름이 역할과 단위를 드러내고 함수가 한 가지 책임에 집중하는가?
- 함수 인자와 중첩이 불필요하게 많지 않고 중복이 제거됐는가?
- 주석이 코드의 반복이 아니라 이유와 제약을 설명하는가?
- exception과 null·empty·boundary case를 의도적으로 처리하는가?
- 자원과 transaction이 성공·실패 양쪽에서 확실히 정리되는가?

# 보안 체크

- 모든 외부 입력을 형식, 길이, 범위와 허용 목록으로 검증하는가?
- SQL injection, XSS, path traversal과 위험한 file upload를 막는가?
- 인증뿐 아니라 객체·행 단위 authorization을 서버에서 검사하는가?
- secret을 코드와 log에 남기지 않고 password는 검증된 hash로 저장하는가?
- 전송 구간 암호화, 현대적 암호 알고리즘과 안전한 key 관리가 있는가?
- 오류 응답이 stack trace, 내부 경로나 개인정보를 노출하지 않는가?

# 도구 사용

원자료에 언급된 FindBugs는 현재 Java 생태계에서 SpotBugs로 이어졌고, 언어별 linter·SAST·dependency scanner는 계속 바뀐다. 도구 이름보다 formatter, type checker, static analysis, test와 secret scan을 CI에서 자동 실행하는 원칙이 중요하다.

# 출처

- [YouTube 원본 영상](https://www.youtube.com/watch?v=IGXDHv9Xn6k)
- [체크리스트 텍스트 정리](https://blog.skby.net/%EC%86%8C%EC%8A%A4%EC%BD%94%EB%93%9C-%EC%B2%B4%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%8A%B8/)
- [Notion 원본 항목](https://app.notion.com/p/1471a73cf20b8279a2d1019d31ed8c1c)
