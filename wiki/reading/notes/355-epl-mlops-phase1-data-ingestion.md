---
type: Study Note
title: "EPL 예측 MLOps Phase 1: 재현 가능한 데이터 수집"
description: "Football-Data의 시즌별 CSV URL을 관리하고 검증·병합해 raw dataset을 만드는 sports ML pipeline 단계"
resource: "https://medium.com/data-ai-and-beyond/building-a-full-stack-mlops-system-predicting-the-2025-2026-english-premier-league-season-phase-c9c1d4f83187"
notion: "https://app.notion.com/p/f7c1a73cf20b82a68bc401fa33ac587a"
tags: [reading, mlops, data-ingestion, sports-analytics, python]
timestamp: 2026-07-24
status: summarized
---

# 목표

연재의 첫 구현 단계는 EPL 경기 결과·배당 archive인 Football-Data의 여러 시즌 CSV를 반복 수집하는 것이다. URL 목록을 별도 data file로 관리하고 ingestion component가 내려받아 schema를 확인한 뒤 하나의 historical dataset으로 병합한다.

# 재현 가능한 ingestion

공개 companion repository의 현재 구조에는 URL catalog, ingested data, validator·merger 역할의 component와 공통 logger가 분리돼 있다. 수집 단계는 원본을 보존하고 season·source metadata를 추가하며, HTTP 실패와 schema 변화가 전체 병합을 조용히 오염시키지 않게 중단·기록해야 한다.

# 주의

Medium 전문은 member wall 뒤였지만 공개 도입부와 연결된 source repository에서 구현 범위를 확인했다. Repository의 현재 code는 article 발행 당시보다 뒤 단계까지 발전했으므로 세부 command는 commit history에서 article 시점과 대조해야 한다. Betting odds는 target leakage와 시점 leakage를 특히 조심한다.

# 관련 문서

- [초기 project 구성](357-epl-mlops-initial-setup.md)
- [Phase 2 cleaning과 transformation](356-epl-mlops-phase2-data-cleaning.md)

# 출처

- [Phase 1 article](https://medium.com/data-ai-and-beyond/building-a-full-stack-mlops-system-predicting-the-2025-2026-english-premier-league-season-phase-c9c1d4f83187)
- [Soca-Scores 저장소](https://github.com/Jnyambok/Soca-Scores)
