---
type: Reference
title: "Git, Docker, Redis를 직접 만들며 배우기"
description: "익숙한 시스템의 작은 호환 구현을 만들며 프로토콜, 저장 구조, 격리와 동시성을 학습하는 프로젝트 목록"
resource: https://news.hada.io/topic?id=25462
notion: https://app.notion.com/p/85f1a73cf20b82f28dd801aa0d68fd55
tags: [reading, systems, learning, project-ideas]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`Build Your Own` 프로젝트는 완제품과 경쟁하려는 시도보다 일상적으로 쓰는 도구의 최소 동작을 직접 구현해 내부 원리를 배우는 방법이다. 프레임워크 사용법을 익힌 다음 단계에서 프로토콜, 파일 포맷, 메모리, 동시성과 운영체제 경계를 만날 수 있다.

# 프로젝트별 핵심

- **Redis**: RESP 같은 네트워크 프로토콜, 메모리 자료구조, 만료와 동시 요청
- **Git**: content-addressed object, tree와 commit, snapshot, pack과 파일 시스템
- **SQLite**: 페이지 저장, B-tree 인덱스, query execution과 트랜잭션
- **Docker**: Linux namespace, cgroup, root filesystem과 프로세스 격리
- **DNS·BitTorrent·Shell**: 네트워크 프로토콜, 분산 조각 교환, 프로세스와 pipe

# 진행 방법

전체 제품을 복제하지 말고 호환 가능한 한 조각을 고른다. 예를 들어 Redis는 `PING`, `SET`, `GET`과 만료, Git은 blob·tree·commit 읽기부터 시작한다. 공식 프로토콜 문서와 테스트 벡터를 기준으로 삼고, 실제 도구를 black-box oracle로 비교한다.

각 단계에는 입력/출력 예제, 실패 조건, 성능 측정과 “생략한 기능”을 기록한다. 구현을 끝낸 뒤 원 프로젝트의 코드를 읽으면 설계 선택의 이유가 더 잘 보인다.

# 주의할 점

학습 구현을 보안이나 데이터 신뢰성이 필요한 운영 환경에 쓰면 안 된다. Docker나 데이터베이스는 보이지 않는 경계 사례가 매우 많다. 목표를 “완성품 제작”이 아니라 내부 모델을 얻는 것으로 제한해야 중도 포기를 줄일 수 있다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=25462)
- [CodeCrafters Build Your Own](https://codecrafters.io/blog/programming-project-ideas)
- [Notion 원본 항목](https://app.notion.com/p/85f1a73cf20b82f28dd801aa0d68fd55)

