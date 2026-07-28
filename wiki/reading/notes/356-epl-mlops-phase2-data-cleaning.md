---
type: Study Note
title: "EPL 예측 MLOps Phase 2: 정제·변환과 database 적재"
description: "여러 시즌의 경기 schema를 통일하고 결측·형식을 정리해 model과 feature store가 쓸 dataset으로 만드는 단계"
resource: "https://medium.com/data-ai-and-beyond/building-a-full-stack-mlops-system-predicting-the-2025-2026-english-premier-league-season-phase-8760a79ddfe1"
notion: "https://app.notion.com/p/1b61a73cf20b83da8bab01c8c62e5ad2"
tags: [reading, mlops, data-cleaning, sports-analytics, database]
timestamp: 2026-07-24
status: summarized
---

# 역할

Phase 2는 ingestion으로 합친 EPL raw data를 model이 일관되게 읽을 수 있도록 cleaning·transformation하고 database에 적재한다. 시즌마다 달라진 column, date와 numeric type, team 이름, duplicate와 null 정책을 명시적으로 다뤄야 한다.

현재 공개 repository는 cleaned dataset을 Neon PostgreSQL에 적재하고 이후 feature engineering과 Feast feature store로 넘기는 흐름을 제공한다. Raw·ingested·cleaned·processed layer를 나누고 각 단계는 독립 module로 실행한다.

# 검증 기준

행 수와 고유 match key, season별 coverage, team mapping, target distribution과 null report를 before·after로 남긴다. 미래 경기 정보나 최종 시즌 통계를 과거 row에 넣지 않도록 event time을 기준으로 transformation한다. Database constraint와 data validation test가 notebook의 육안 확인을 대신해야 한다.

# 확인 범위

Medium 전문은 member wall로 제한됐지만 공개 intro, phase 연결과 저자의 public repository에서 pipeline을 보완했다. Article 시점의 정확한 code line과 현재 repository가 다를 수 있다.

# 관련 문서

- [Phase 1 data ingestion](355-epl-mlops-phase1-data-ingestion.md)

# 출처

- [Phase 2 article](https://medium.com/data-ai-and-beyond/building-a-full-stack-mlops-system-predicting-the-2025-2026-english-premier-league-season-phase-8760a79ddfe1)
- [Soca-Scores 저장소](https://github.com/Jnyambok/Soca-Scores)
