---
type: Concept
title: "Claude Code 다중 에이전트 코드 리뷰의 구조와 평가 기준"
description: "PR별 전문 agent를 병렬 실행해 bug를 검증·정렬하고 고신호 review를 만드는 research preview"
resource: "https://news.hada.io/topic?id=27362"
notion: "https://app.notion.com/p/e621a73cf20b838cad4a016016a4534a"
tags: [reading, code-review, multi-agent, claude-code]
timestamp: 2026-07-24
status: summarized
---

# 구조

Claude Code Code Review는 PR마다 agent team을 만들어 여러 관점에서 bug를 찾게 한다. 각 finding을 다른 agent가 검증하고 severity를 정렬한 뒤, 하나의 요약과 필요한 inline comment로 합친다. PR 크기에 따라 투입 effort를 늘리며 최종 merge 판단은 사람에게 남긴다.

# 공개된 수치

Anthropic 내부에서는 coding output이 약 200% 늘어 review가 bottleneck이 됐다고 설명한다. 실질적 review comment가 달린 비율이 16%에서 54%로 증가했고, 1,000줄 초과 PR은 84%에서 평균 7.5개 문제, 50줄 미만은 31%에서 평균 0.5개를 찾았다고 보고한다. 표시된 false positive는 1% 미만, 평균 실행은 약 20분, 비용은 PR당 15~25달러로 제시됐다.

# 평가 방법

Vendor 자체 수치이므로 comment 수만으로 성공을 판단하지 않는다. 사람이 수용한 finding 비율, escaped defect, review latency, 수정 후 regression, PR 크기별 비용을 함께 측정한다. 동일 PR을 기존 사람 review나 단일 agent와 blind comparison하는 것이 좋다.

# 한계

사용자가 false positive로 표시하지 않으면 통계에 잡히지 않는 편향이 있다. 여러 agent가 같은 잘못된 전제를 공유할 수도 있고 보안·domain invariant는 별도 reviewer가 필요하다. 기능과 가격은 research preview 시점 정보다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27362)
