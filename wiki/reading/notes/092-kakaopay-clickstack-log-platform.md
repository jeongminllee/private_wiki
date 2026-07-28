---
type: Reference
title: "일 41TB 로그를 처리하는 카카오페이증권 ClickStack 아키텍처"
description: "OpenSearch 중심 파이프라인을 OpenTelemetry, Kafka, ClickHouse, S3와 HyperDX로 재설계한 사례"
resource: https://tech.kakaopay.com/post/pallas-v2-log-platform/
notion: https://app.notion.com/p/deb1a73cf20b83f889a681ed646367c3
tags: [reading, observability, clickhouse, opentelemetry, data-infra]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

카카오페이증권의 로그가 3년 동안 일 100GB에서 41TB, 200억 건 이상으로 늘자 수집부터 장기 조회까지 전체 경로를 다시 설계한 사례다. 회사 측 측정으로 유입 지연은 수 분~수 시간에서 20초 이내로, 비용은 기존의 14.4%로 줄었다.

# 기존 병목

- OpenSearch 비용이 로그량과 함께 크게 증가했다.
- Fluentd의 chunk 처리에서 memory 사용과 지연이 커졌다.
- 서비스별 Kafka topic이 300개 이상으로 늘어 운영이 복잡해졌다.
- 2,000개가 넘는 column을 Athena table로 관리하기 어려웠다.

# 새 구조

실시간 경로는 IDC에서 OpenTelemetry가 로그를 수집·batch 처리하고 Kafka를 거쳐 6 shard와 replica로 구성한 ClickHouse에 저장한다. 개발자는 HyperDX와 Grafana로 조회한다.

장기 데이터는 자체 Python 도구 `ssak3`가 ClickHouse에서 꺼내 Parquet+ZSTD로 S3에 보낸다. IDC에는 최근 9일을 두고, AWS ClickHouse는 필요할 때 S3의 장기 로그를 조회한다. 양쪽 cluster를 복제하는 대신 S3를 중심으로 한 단방향 archive를 택했다.

# 중요한 설계 결정

- OTLP와 batch 전송으로 message별 JSON key 반복 비용을 줄였다.
- Kafka topic을 300개에서 18개로 통합하되 partition·consumer와 log governance를 함께 재설계했다.
- ClickHouse의 Buffer·Store·Distributed·View 역할과 접근 권한을 나눴다.
- archive watermark에 `pending/processing/completed/failed`와 마지막 offset을 기록해 실패 지점부터 재시도한다.
- storage engine 교체만이 아니라 수집 format, topic, merge, retention과 사용자 조회 경험을 함께 바꿨다.

# 적용 판단

41TB 규모의 결과를 작은 환경에 그대로 복사할 필요는 없다. 먼저 query pattern, hot/cold retention, ingest latency, column cardinality와 총비용을 측정하고, 기존 pipeline의 가장 앞쪽 병목부터 하나씩 검증한다.

# 출처

- [카카오페이 기술 블로그 원문](https://tech.kakaopay.com/post/pallas-v2-log-platform/)
- [ClickStack 공식 소개](https://clickhouse.com/use-cases/observability)
- [Notion 원본 항목](https://app.notion.com/p/deb1a73cf20b83f889a681ed646367c3)
