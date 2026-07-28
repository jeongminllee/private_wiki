---
type: Reference
title: "잠자는 동안 실행되는 코딩 에이전트를 검증하는 파이프라인"
description: "구현 전에 수용 기준을 쓰고 독립 브라우저 에이전트와 판정 단계로 결과를 검증하는 접근"
resource: https://news.hada.io/topic?id=27414
notion: https://app.notion.com/p/c591a73cf20b823da27001a48f044af9
tags: [reading, coding-agent, testing, acceptance-criteria]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

장시간 자율 실행하는 코딩 에이전트의 병목은 코드 생성이 아니라 “완료됐다고 믿을 근거”다. 같은 에이전트가 자신의 구현 의도에 맞춰 테스트를 만들면 원래 요구를 잘못 이해한 문제를 함께 놓칠 수 있으므로, 구현 전에 사람이 관찰 가능한 수용 기준을 정하고 별도 과정이 검증하게 한다.

# 네 단계 파이프라인

1. **Pre-flight**: 개발 서버, 인증 session과 spec 존재 여부를 deterministic script로 확인한다.
2. **Planner**: spec과 변경 파일을 읽고 각 수용 기준의 검증 방법을 계획한다.
3. **Browser agents**: 기준별로 독립 실행해 실제 화면을 조작하고 screenshot과 관찰 증거를 남긴다.
4. **Judge**: 증거를 모아 `pass`, `fail`, `needs-human-review`로 판정한다.

프론트엔드는 Playwright, 백엔드는 status code·header·response body를 확인하는 `curl`이나 contract test를 사용할 수 있다. 실패한 기준과 실제 관찰을 보고하므로 사람은 전체 diff보다 실패와 고위험 변경에 집중할 수 있다.

# 좋은 수용 기준

“로그인이 된다”가 아니라 유효한 계정의 redirect와 cookie, 잘못된 비밀번호의 정확한 error, 빈 필드의 동작, 반복 실패 후 rate limit처럼 외부에서 pass/fail을 판단할 수 있게 쓴다.

# 한계

잘못된 spec은 완벽하게 구현해도 잘못된 결과를 만든다. 에이전트가 test를 우회하거나 의미 없는 test를 추가하는 reward hacking도 남는다. 인증·결제·데이터 삭제·권한 변경은 evidence 기반 자동 검증과 별개로 인간 review와 좁은 권한, rollback 수단이 필요하다.

# 출처

- [GeekNews 정리와 토론](https://news.hada.io/topic?id=27414)
- [원문](https://www.claudecodecamp.com/p/i-m-building-agents-that-run-while)
- [검증 도구 저장소](https://github.com/opslane/verify)
- [Notion 원본 항목](https://app.notion.com/p/c591a73cf20b823da27001a48f044af9)
