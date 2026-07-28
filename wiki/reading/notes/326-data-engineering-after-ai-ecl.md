---
type: Concept
title: "AI 이후 데이터 엔지니어링: ETL에서 ECL로"
description: "데이터 이동보다 의미의 정의·검증·전파를 중심에 두는 Extract, Contextualize, Link 제안"
resource: "https://www.dataengineeringweekly.com/p/data-engineering-after-ai"
notion: "https://app.notion.com/p/f251a73cf20b83f5a65501f94090e07a"
tags: [reading, data-engineering, metadata, data-contract, ai]
timestamp: 2026-07-24
status: summarized
---

# 제안

글은 데이터 엔지니어링의 어려운 부분이 이동 자체보다 의미라고 보고 ETL을 `Extract, Contextualize, Link(ECL)`로 다시 바라본다. Extract에는 여전히 신뢰성, 지연, 규모와 실패 처리가 필요하다. Contextualize는 `revenue`, timestamp, null처럼 조직마다 다른 의미를 명시하고, Link는 entity와 context를 여러 system에 걸쳐 연결한다.

# 두 가지 경로

통제 가능한 producer boundary에서는 schema, 품질, 소유자, 의미, version과 실패 동작을 executable data contract로 조기에 고정한다. Wiki에 계약을 써 두기만 해서는 runtime 보장이 되지 않는다.

외부·legacy source처럼 조기 계약이 어려우면 event-driven agent가 schema, sample, 통계와 lineage를 조사해 versioned inference를 만든다. 높은 confidence는 자동 검토, 중간은 사람 확인, 낮은 것은 추가 조사로 보내고 검증된 결과를 Context Store에 둔다. 발견된 의미가 안정되면 prescribed contract로 승격할 수 있다.

# 실무적 해석

Context는 metadata, lineage와 provenance를 통해 데이터와 함께 이동해야 한다. 이를 맡는 Context Architect는 계약뿐 아니라 부서 간 정의 충돌과 책임 소재를 조정한다. AI는 초안을 만들 수 있지만 의미의 최종 책임은 domain owner에게 남는다.

# 한계

ECL은 완성된 표준이나 제품이 아니라 방향 제안이다. Tacit knowledge를 구조화하고, 상충하는 정의를 governance하며, inference의 품질을 측정하는 문제가 남는다. 기존 medallion·ETL을 이름만 바꾸기보다 context가 transformation 뒤에도 실제로 보존되는지 검증해야 한다.

# 출처

- [Data Engineering After AI](https://www.dataengineeringweekly.com/p/data-engineering-after-ai)
