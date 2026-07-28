---
type: Reference
title: "당근의 시맨틱 캐싱 도입과 LLM 비용 25% 절감"
description: "의미가 비슷한 채팅 요청을 재사용해 연간 LLM 호출 비용을 줄인 설계와 검증 과정"
resource: https://medium.com/daangn/%EC%97%B0%EA%B0%84-llm-%ED%98%B8%EC%B6%9C-%EB%B9%84%EC%9A%A9-25-%EC%A0%88%EA%B0%90-%EC%9D%B8%ED%84%B4%EC%9D%B4-%EB%8F%84%EC%A0%84%ED%95%9C-%EC%8B%9C%EB%A7%A8%ED%8B%B1-%EC%BA%90%EC%8B%B1-%EB%8F%84%EC%9E%85-%EA%B8%B0%EB%A1%9D-af3de9a74d0c
notion: https://app.notion.com/p/bb11a73cf20b83f7b479814916c9a823
tags: [reading, llm, semantic-cache, cost-optimization, kubernetes]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

당근의 채팅 AI 메시지 추천 기능에서 표현은 다르지만 의미가 비슷한 요청의 응답을 재사용한 사례다. 단순 문자열 캐시 대신 임베딩 유사도를 사용하는 시맨틱 캐시를 도입해 온라인에서 약 25%의 캐시 적중률과 연간 약 2.16억 원의 절감 가능성을 확인했다.

# 문제

LLM 호출 비용은 연간 약 8~9억 원 수준이었고, 중고거래 대화에는 의미가 반복되지만 문장이 정확히 같지 않은 요청이 많았다. 정확히 같은 키만 찾는 캐시는 이런 반복을 활용하지 못한다.

# 설계

- 메인 서버와 분리한 add-on 서버를 gRPC로 연결했다.
- 문장을 임베딩하고 코사인 유사도로 재사용 가능성을 판단했다.
- 발화 데이터를 전처리한 뒤 PCA와 DBSCAN으로 패턴을 군집화해 캐시 후보를 만들었다.
- 벡터 저장소를 서비스에 내장하고 서버를 수평 확장할 수 있게 구성했다.

# 검증 결과

- 오프라인 실험에서 유사도 임계값 0.65일 때 29.55% 적중률을 확인했다.
- 온라인에서는 약 25% 적중률을 관찰했다.
- 임베딩 생성 병목은 Kubernetes replica 확장으로 완화했다.
- 기사 기준 캐시 운영비는 LLM 호출비보다 매우 작았다.

# 주의

캐시 적중률만 높이면 서로 다른 의도를 같은 요청으로 판단해 잘못된 응답을 재사용할 수 있다. 비용 절감과 함께 거짓 양성, 개인정보 보존 기간, 오래된 응답 무효화, 모델·프롬프트 버전별 캐시 분리를 측정해야 한다.

# 출처

- [당근 기술 블로그 원문](https://medium.com/daangn/%EC%97%B0%EA%B0%84-llm-%ED%98%B8%EC%B6%9C-%EB%B9%84%EC%9A%A9-25-%EC%A0%88%EA%B0%90-%EC%9D%B8%ED%84%B4%EC%9D%B4-%EB%8F%84%EC%A0%84%ED%95%9C-%EC%8B%9C%EB%A7%A8%ED%8B%B1-%EC%BA%90%EC%8B%B1-%EB%8F%84%EC%9E%85-%EA%B8%B0%EB%A1%9D-af3de9a74d0c)

