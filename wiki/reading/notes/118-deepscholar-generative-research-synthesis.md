---
type: Reference
title: "DeepScholar: 생성형 연구 종합과 평가"
description: "논문 검색·관련 연구 작성 파이프라인과 지식 종합·검색·검증 가능성을 함께 측정하는 benchmark"
resource: https://deep-scholar.vercel.app/
notion: https://app.notion.com/p/ff91a73cf20b8226bd4c01c5d9da64fe
tags: [reading, deep-research, research-agent, benchmark]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

UC Berkeley와 Stanford 연구진의 DeepScholar 프로젝트는 연구 질문에서 관련 논문을 찾고 인용이 포함된 related work를 만드는 open-source reference pipeline과 이를 평가하는 live benchmark를 함께 제공한다. 단순 정답보다 장문 연구 종합의 품질을 측정하려는 시도다.

# Benchmark 구조

최근 고품질 arXiv 논문에서 query와 사람이 쓴 related work를 가져와 평가 자료를 계속 갱신한다. 평가는 `knowledge synthesis`, `retrieval quality`, `verifiability` 세 축을 다룬다. dataset 생성 script, LLM judge 기반 evaluation suite와 LOTUS 위의 `DeepScholar-base`가 공개되어 있다.

# 성능 주장을 읽는 법

저장소는 DeepScholar-base가 자체 benchmark에서 OpenAI DeepResearch와 경쟁력 있는 성능을 내면서 2배 빠르다고 보고한다. 이는 저자들의 평가 설정과 related-work task 안의 결과다. 모든 주제에서 더 정확하거나 비용이 낮다는 뜻은 아니며, 서로 다른 모델·검색 API와 judge 선택이 결과에 영향을 준다.

# 사용 전 점검

Python 3.10 환경과 OpenAI·Tavily API key가 필요해 완전한 local-only 도구는 아니다. 생성된 인용이 실제 문장을 지지하는지, 빠진 핵심 논문은 없는지, 논문 버전·철회·출판 상태가 맞는지 사람이 확인해야 한다. 초안 작성 보조와 문헌 후보 탐색에는 유용하지만 연구 책임을 위임할 수는 없다.

# 출처

- [DeepScholar 실행 화면](https://deep-scholar.vercel.app/)
- [GitHub 저장소](https://github.com/guestrin-lab/deepscholar)
- [UC Berkeley 프로젝트 설명](https://sky.cs.berkeley.edu/project/deepscholar-bench/)
- [논문](https://arxiv.org/abs/2508.20033)
- [Notion 원본 항목](https://app.notion.com/p/ff91a73cf20b8226bd4c01c5d9da64fe)
