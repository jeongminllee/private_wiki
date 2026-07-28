---
type: Reference
title: "LLM으로 소프트웨어를 만드는 Architect-Developer-Reviewer 흐름"
description: "서로 다른 모델에 설계·구현·리뷰 역할과 권한을 나눠 품질을 관리하는 개인 워크플로"
resource: https://news.hada.io/topic?id=27576
notion: https://app.notion.com/p/9021a73cf20b83fb8a6a01194c7ee42d
tags: [reading, coding-agent, multi-agent, code-review]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Stavros Korokithakis가 수만 줄 규모의 개인 프로젝트를 LLM으로 만들며 정리한 workflow다. 코드를 거의 읽지 않더라도 기술과 architecture를 잘 아는 영역에서는 높은 품질을 유지할 수 있었다고 주장하며, 설계·구현·검토를 서로 다른 agent와 model에 분리한다.

# 역할 분리

- `Architect`: 사람이 직접 대화하는 강한 model. 목표, 제약, trade-off를 질문하고 file·function 수준 plan을 만든다.
- `Developer`: 더 저렴한 model. 승인된 plan만 구현하고 고수준 결정을 임의로 바꾸지 않는다.
- `Reviewer`: 다른 회사의 model 1~3개가 plan과 diff를 독립 검토한다.
- 다시 Architect가 review 의견을 선별하고 수정 여부를 결정한다.

# 왜 다른 모델인가

같은 model은 자기 결과에 동의하는 경향과 같은 blind spot을 공유할 수 있다. 독립 model을 쓰면 서로 다른 실패를 찾을 가능성이 커진다. 역할별 read-only와 write 권한을 나누는 것도 사고 범위를 줄인다.

# 실무에 옮길 때

사람이 plan을 명시적으로 승인하기 전에는 구현을 시작하지 않게 한다. 변경을 작은 task로 나누고 test, lint, security scan과 실제 QA를 agent 의견과 별도로 실행한다. model review가 여러 번 겹쳐도 같은 잘못된 가정을 공유할 수 있으므로 중요한 domain rule과 acceptance test는 사람이 소유한다.

# 한계

결함률이 손코딩보다 낮다는 평가는 저자의 체감이며 통제된 비교가 아니다. 저자도 모르는 mobile 기술에서는 architecture가 빠르게 나빠졌다고 밝힌다. workflow의 핵심은 agent 수보다 사람이 판단할 수 있는 domain에서 명확한 계획과 독립 검증을 두는 것이다.

# 출처

- [원문](https://www.stavros.io/posts/how-i-write-software-with-llms/)
- [GeekNews 한국어 정리와 토론](https://news.hada.io/topic?id=27576)
- [Notion 원본 항목](https://app.notion.com/p/9021a73cf20b83fb8a6a01194c7ee42d)
