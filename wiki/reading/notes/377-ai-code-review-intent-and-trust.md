---
type: Reference
title: "AI 시대 코드 리뷰: Diff에서 의도와 신뢰 체계로"
description: "사람 review의 필요와 처리량 한계를 함께 인정하고 다층 검증으로 code 신뢰를 구축하는 essay"
resource: "https://flowkater.io/posts/2026-03-08-ai-code-review/"
notion: "https://app.notion.com/p/3e21a73cf20b83bb86b501a6d70aa09f"
tags: [reading, code-review, ai-coding, trust, software-engineering]
timestamp: 2026-07-24
status: summarized
---

# Thesis, antithesis, synthesis

첫 관점은 사람이 code 책임을 지는 한 review가 필요하다는 것이다. 그러나 AI가 PR 생산 빈도를 크게 올리면 숙련 reviewer가 모든 line을 읽는 방식은 확장되지 않는다. 저자는 이 충돌의 해법으로 code 자체보다 spec, 의도와 수용 기준을 먼저 검토하는 `intent review`를 제안한다.

# 신뢰를 여러 층으로 쌓기

한 gate가 모든 오류를 잡는다고 가정하지 않는다. 여러 agent의 독립 시도, test와 type check 같은 결정론적 guardrail, 사람이 미리 정한 acceptance criteria, 세분화된 permission, 생성 agent와 다른 adversarial reviewer를 겹친다. Context-first review로 과거 PR과 architecture를 먼저 모으고, finding을 severity별로 나누며, security·database·performance 같은 expert agent를 필요한 변경에만 붙인다.

# 해석상의 주의

AI reviewer들이 서로 승인했다고 correctness가 증명되지는 않는다. 동일 model과 context를 쓰면 같은 잘못된 전제를 공유할 수 있다. Spec이 source of truth가 되려면 versioning, executable test와 실제 사용자 outcome이 연결되어야 한다. Tribal knowledge와 규제 판단은 자동화된 문서만으로 대체되지 않는다.

실무에서는 변경 risk에 따라 review budget을 배분하는 방식으로 읽는 것이 안전하다. Low-risk boilerplate는 자동화 비중을 높이고, 권한·결제·data loss처럼 영향이 큰 code는 사람이 의도와 implementation을 모두 이해한다.

# 관련 문서

- [GeekNews 토론 중심 정리](376-ai-code-review-geeknews-discussion.md)

# 출처

- [Flowkater 원문](https://flowkater.io/posts/2026-03-08-ai-code-review/)
