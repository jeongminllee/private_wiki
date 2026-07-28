---
type: Reference
title: "PaperOrchestra 한국어 개요: 논문 초안을 역할별 에이전트로 작성하기"
description: "실험 log와 idea summary를 문헌 조사, 도표, section 작성과 검토 단계로 분리하는 논문 작성 framework 소개"
resource: https://md-share-cf.pages.dev/view/docs/PaperOrchestra%20-%20Google%20AI%20%EC%9E%90%EB%8F%99%20%EB%85%BC%EB%AC%B8%20%EC%9E%91%EC%84%B1%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC_9a079b.md
notion: https://app.notion.com/p/9ce1a73cf20b82f0b2200130e22353d0
tags: [reading, ai-agents, research, paper-writing]
timestamp: 2026-07-24
status: summarized
---

# 핵심 내용

PaperOrchestra는 연구 아이디어와 실험이 이미 존재한다는 전제에서, 흩어진 사전 작성 자료를 학회 형식의 논문 초안으로 조립한다. 한 agent에게 모든 일을 맡기지 않고 outline, plot, literature review, section writing, refinement 역할을 분리한다.

# 파이프라인

1. idea summary와 numeric experimental log로 논문 구조를 계획한다.
2. diagram과 statistical plot을 생성하거나 기존 figure를 배치한다.
3. web search로 후보 논문을 찾고 Semantic Scholar API로 존재·관련성을 확인한다.
4. venue별 LaTeX template에 section을 작성한다.
5. simulated peer review를 바탕으로 반복 수정해 PDF를 만든다.

# 이 소개를 읽을 때의 기준

자동화 대상은 연구 자체보다 이미 수행된 연구의 서술과 편집이다. 인용이 실제 존재해도 주장을 뒷받침하는지는 사람이 확인해야 하며, 실험 해석·새로움·저자 책임을 agent에 넘길 수 없다. 공식 연구와 benchmark의 자세한 내용은 [PaperOrchestra 연구 노트](227-paperorchestra-research-paper-writing.md)에 연결했다.

# 출처

- [저장된 한국어 소개](https://md-share-cf.pages.dev/view/docs/PaperOrchestra%20-%20Google%20AI%20%EC%9E%90%EB%8F%99%20%EB%85%BC%EB%AC%B8%20%EC%9E%91%EC%84%B1%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC_9a079b.md)

