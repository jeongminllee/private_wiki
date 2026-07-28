---
type: Reference
title: "text2sql-framework: 실행하며 스키마를 탐색하는 Text-to-SQL 에이전트"
description: "LLM에 execute_sql 도구 하나를 주고 스키마 탐색, 쿼리 검증과 자기 수정을 반복하게 하는 SDK"
resource: https://github.com/Text2SqlAgent/text2sql-framework
notion: https://app.notion.com/p/d261a73cf20b828f9764818d4dd53a4e
tags: [reading, ai-agents, sql, text-to-sql]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`text2sql-framework`는 미리 스키마를 임베딩하거나 semantic layer를 만들기보다 LLM이 `execute_sql`을 반복 호출하며 테이블을 찾고, 쿼리를 시험하고, 오류를 고쳐 최종 SQL을 반환하게 한다.

# 작동 방식

1. 데이터베이스의 테이블 목록을 조회한다.
2. 후보 테이블의 column과 type을 직접 검사한다.
3. SQL을 실행하고 오류와 결과 모양을 읽는다.
4. 잘못된 테이블·join·aggregation을 수정한다.
5. 검증된 SQL과 결과 데이터를 함께 반환한다.

PostgreSQL, MySQL, SQLite, SQL Server, Snowflake 등 SQLAlchemy driver가 있는 DB를 지원하고 dialect별 schema 조회 방법을 바꾼다.

# 업무 규칙과 개선 루프

스키마에서 알 수 없는 “순매출은 환불 제외”, “이 column은 고객 등급” 같은 지식은 `scenarios.md`에 둔다. 에이전트는 제목만 본 뒤 필요할 때 `lookup_example`로 관련 규칙을 가져온다. 전체 trace를 JSONL로 남기고 MCP 분석기가 반복 실패를 찾아 새 scenario를 제안할 수 있다.

# 보고된 평가

저장소는 Spider dev의 20개 DB를 합친 80-table 환경에서 무작위 20문항 중 zero-shot 19개를 맞혔고, 모호한 집계 규칙 한 줄을 추가한 뒤 20개를 맞혔다고 보고한다. 전체 Spider 10,000여 문항 평가가 아니고 작은 자체 표본이므로 일반 성능으로 해석하면 안 된다.

# 보안과 운영

자연어 질의를 운영 DB에 바로 연결하면 민감정보 노출과 쓰기 쿼리 위험이 있다. read-only 계정, 허용 schema, statement timeout, row limit, 비용 제한, 실행 전 SQL parser 검사와 감사 log를 기본으로 둬야 한다.

# 출처

- [Text2SqlAgent/text2sql-framework](https://github.com/Text2SqlAgent/text2sql-framework)

