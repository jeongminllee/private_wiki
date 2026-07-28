---
type: Reference
title: "Omni: 사내 자료를 한곳에서 찾는 업무용 AI 검색 플랫폼"
description: "여러 SaaS와 로컬 파일을 통합 검색하는 Omni의 검색 구조, 권한 처리와 self-hosting 검토 사항"
resource: https://news.hada.io/topic?id=27390
notion: https://app.notion.com/p/8561a73cf20b82dda44e017d361b6ca4
tags: [reading, enterprise-search, rag, self-hosting]
timestamp: 2026-07-24
status: summarized
---

# 무엇을 해결하나

Omni는 Google Drive·Gmail·Slack·Confluence·Jira·HubSpot·Fireflies, 웹과 로컬 파일처럼 흩어진 업무 자료를 연결해 검색하고 질문하게 하는 오픈소스 플랫폼이다. 사용자가 어느 서비스에 문서가 있는지 기억하지 못해도 하나의 검색면에서 찾는 것이 목표다.

# 구조

검색은 BM25 keyword search와 `pgvector` semantic search를 결합한다. Postgres와 ParadeDB를 중심으로 두 검색 방식을 한 database에 두고, Rust가 connector·indexing·search를, Python이 AI orchestration을, SvelteKit이 UI를 맡는다. Docker 기반 local deployment와 AWS·GCP용 Terraform 구성이 제공된다.

여러 model provider를 선택할 수 있고, 작업 실행 환경에는 Docker network 격리, Landlock, resource limit와 read-only root filesystem 같은 sandbox 장치가 소개된다.

# 가장 중요한 운영 조건

사내 검색에서는 model 성능보다 권한 보존이 먼저다. source system의 ACL과 group membership이 index에 정확히 동기화되지 않으면 검색 결과나 생성 답변을 통해 접근 권한이 없는 정보가 노출될 수 있다. connector별 증분 동기화, 삭제 전파, 권한 변경 지연과 audit log를 실제 조직 데이터로 시험해야 한다.

# 주의할 점

Self-hosting은 검색 index를 직접 관리한다는 뜻이지 모든 data가 자동으로 내부에만 머문다는 뜻은 아니다. remote LLM이나 embedding API를 선택하면 prompt와 retrieved context가 외부 provider로 전송될 수 있다. 배포 전에 data flow, retention policy와 provider별 enterprise setting을 확인해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27390)

