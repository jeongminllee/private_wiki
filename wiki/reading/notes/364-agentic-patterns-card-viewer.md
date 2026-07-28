---
type: Reference
title: "Agentic Patterns Snippets 카드 뷰어"
description: "AI agent 설계 패턴 99개를 ASCII diagram과 짧은 설명으로 탐색하는 비공식 카드형 뷰어"
resource: "https://news.hada.io/topic?id=25637"
notion: "https://app.notion.com/p/6db1a73cf20b82fc8964010412560f34"
tags: [reading, agent, design-patterns, reference, viewer]
timestamp: 2026-07-24
status: summarized
---

# 자료의 성격

이 자료는 `awesome-agentic-patterns`에 수록된 99개 pattern을 ASCII diagram과 요약 카드로 빠르게 훑도록 만든 비공식 viewer다. 긴 문서를 처음부터 읽기보다, context 관리, routing·planning, tool use, memory, multi-agent collaboration, evaluation·safety 같은 문제 영역에서 후보 pattern을 찾는 색인으로 유용하다.

# 활용 방법

Pattern은 정답 recipe가 아니라 설계 vocabulary다. 먼저 system의 실제 failure mode를 기록하고 관련 카드 몇 개를 고른 다음, canonical 문서와 source를 읽어 전제와 trade-off를 확인한다. 이후 latency, cost, success rate, human escalation과 recovery를 측정하는 작은 실험으로 채택 여부를 결정한다.

# 주의점

Viewer는 원본과 수동으로 동기화되어 최신 pattern이 늦게 반영될 수 있다. 일부 Mermaid 표현에는 syntax 오류가 보고되었다. 원작자도 canonical repository와 공식 site를 별도로 안내했으므로, 설계 결정이나 인용에는 원본을 기준으로 삼아야 한다.

# 출처

- [GeekNews 소개와 제작자·원작자 토론](https://news.hada.io/topic?id=25637)
- [카드 뷰어](https://esc5221.github.io/awesome-agentic-patterns)
- [Canonical repository](https://github.com/nibzard/awesome-agentic-patterns)
- [Agentic Patterns 공식 사이트](https://agentic-patterns.com/)
