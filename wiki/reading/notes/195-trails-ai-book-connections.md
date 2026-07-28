---
type: Reference
title: "Trails: AI로 100권의 책 사이 연결 찾기"
description: "여러 책의 개념을 40여 개 주제 경로로 연결해 탐색하는 distant reading 실험"
resource: https://news.hada.io/topic?id=25730
notion: https://app.notion.com/p/ed91a73cf20b82f4a3ed01780bcfafd5
tags: [reading, books, knowledge-graph, ai-agents]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Trails는 Claude Code로 100권의 책을 분석해 40여 개의 주제별 연결을 만든 웹 프로젝트다. 한 권씩 요약하는 대신 서로 다른 분야에서 되풀이되는 패턴을 찾아 새로운 읽기 경로를 제안한다.

# 연결 예

- **Useful Lies**: 자기기만, 진화심리학, 집단을 위한 거짓말
- **Invisible Crack**: 작은 결함의 누적, 금속 피로, 점진적 변화가 만든 파국
- **Ideas Mate**: 모방, 지식 확산, 오픈소스가 혁신을 촉진하는 방식
- **Desperate Pivots**: 위기가 조직의 방향 전환을 만드는 과정
- **Expert Intuition**: 암묵지, 경험, 빠른 전문가 판단
- **Proxy Trap**: 지표를 목표로 삼을 때 원래 목적을 잃는 문제

# 가치와 한계

대규모 텍스트를 멀리서 읽으며 후보 관계를 발견하는 distant reading 도구로는 흥미롭다. 그러나 댓글에서 지적되듯 단어가 비슷하다는 이유로 의미 없는 연결이 생기고, 책의 한 단락을 전체 주장으로 오해할 수 있다. 각 trail은 결론이 아니라 “두 원문을 함께 읽어볼 질문”으로 사용해야 한다.

# 내 wiki에 적용할 점

자동 cross-link에는 연결 근거 문장과 출처 위치, 관계 유형을 함께 저장해야 한다. 사람이 승인하지 않은 의미 관계를 본문 사실처럼 표시하지 않는 것이 중요하다.

# 관련 문서

- [llm-wiki 지식 그래프 방식](033-llm-wiki-knowledge-graph-skill.md)

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=25730)
- [Trails](https://trails.pieterma.es/)

