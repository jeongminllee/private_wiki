---
type: Reference
title: "무신사의 AI 코드 리뷰 프로세스"
description: "Claude Code Action을 조직 공용 Composite Action으로 발전시킨 리뷰 자동화 운영 사례"
resource: https://techblog.musinsa.com/%EB%AC%B4%EC%8B%A0%EC%82%AC%EC%9D%98-ai-%EC%BD%94%EB%93%9C-%EB%A6%AC%EB%B7%B0-%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4-%EA%B5%AC%EC%B6%95%EA%B8%B0-3ddb3c674e56
notion: https://app.notion.com/p/5e61a73cf20b83819acb01ccabf95717
tags: [reading, code-review, github-actions, claude-code]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

무신사는 `anthropics/claude-code-action`을 개별 repository에 붙이는 수준에서 시작해, token과 prompt·review logic을 중앙 관리하는 조직 공용 AI review platform으로 발전시켰다. 핵심은 모델 자체보다 여러 팀이 적은 YAML로 채택할 수 있는 운영 구조와 comment noise 관리다.

# 구축 흐름

1. GitHub Secret과 workflow로 작은 팀에서 inline comment와 Suggestion을 시험한다.
2. 공통 logic을 Composite Action에 묶고 input으로 팀별 추가 규칙을 받는다.
3. 빠르게 갱신되는 `main`과 안정적인 `v1.x` 같은 version track을 분리한다.
4. 장황한 지시를 줄이는 minimalist prompting으로 중복·형식적 comment를 줄인다.
5. bot comment는 정리하되 사람이 답했거나 resolved된 thread는 대화 이력으로 보존한다.

# 운영 체크

중앙 prompt 변경은 조직 전체 repository에 영향을 주므로 canary와 version pinning, rollback이 필요하다. token 권한은 pull request가 secret과 배포 환경에 접근하지 못하도록 최소화하고 fork PR과 prompt injection을 별도로 다룬다. AI suggestion은 자동 merge하지 않고 test, ownership과 human approval을 유지한다.

# 비판적으로 볼 점

홍보성 재정리 페이지의 “생산성 200%” 같은 표현은 측정 기준이 확인되지 않아 채택하지 않았다. 실제 효과는 review lead time, false positive, 사람이 수정한 comment 비율과 defect escape를 비교해야 한다.

# 출처

- [무신사 기술 블로그 원문](https://techblog.musinsa.com/%EB%AC%B4%EC%8B%A0%EC%82%AC%EC%9D%98-ai-%EC%BD%94%EB%93%9C-%EB%A6%AC%EB%B7%B0-%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4-%EA%B5%AC%EC%B6%95%EA%B8%B0-3ddb3c674e56)
- [Notion 원본 항목](https://app.notion.com/p/5e61a73cf20b83819acb01ccabf95717)
