---
type: Reference
title: "무신사의 온프레미스·AWS 하이브리드 AI 인프라 구축기"
description: "GPU 수급과 비용 문제에서 출발해 EKS Hybrid Node, Cilium, 관측과 추론 routing을 조정한 과정"
resource: https://medium.com/musinsa-tech/%EC%9A%B0%EB%A6%AC%EB%8A%94-%EB%8B%AC%EC%97%90-%EA%B0%80%EA%B8%B0%EB%A1%9C-%ED%96%88%EC%8A%B5%EB%8B%88%EB%8B%A4-hybrid%EC%9D%B8%ED%94%84%EB%9D%BC%EB%B6%80%ED%84%B0-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-%EC%B5%9C%EC%A0%81%ED%99%94%EA%B9%8C%EC%A7%80-%EB%AC%B4%EC%8B%A0%EC%82%AC-ai-infra%EA%B5%AC%EC%B6%95%EA%B8%B0-3ffe4831c0a4
notion: https://app.notion.com/p/14c1a73cf20b8234a87401337771d274
tags: [reading, ai-infrastructure, kubernetes, hybrid-cloud, mlops]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

무신사가 AI 학습·추론 비용과 GPU 확보 문제를 해결하려고 온프레미스 GPU를 AWS 운영 환경과 결합한 기록이다. 처음부터 완성된 reference architecture를 적용한 것이 아니라 RTX 4090 조달, 전력·냉방, EKS Hybrid Node와 network 문제를 단계적으로 검증했다.

# 해결하려던 문제

- H100 같은 GPU를 원하는 시점에 확보하기 어렵고 cloud GPU의 지속 비용이 컸다.
- 사내 GPU를 쓰려면 전력·냉방·공간과 hardware failure를 직접 책임져야 했다.
- AWS workload와 온프레미스 node를 한 운영 체계로 묶을 때 CNI, autoscaling과 traffic path가 복잡해졌다.
- training, inference와 telemetry traffic이 함께 늘면서 network와 log 비용도 병목이 됐다.

# 주요 선택

EKS Hybrid Node로 AWS control plane과 온프레미스 compute를 연결하고, Cilium과 NLB를 포함한 network path를 조정했다. Karpenter·Auto Mode와 hybrid node 사이의 동작 차이를 직접 검증했으며, OpenTelemetry 설정과 log volume도 비용 관점에서 다뤘다. 추론 traffic은 Gateway API Inference Extension 등을 검토해 model server의 부하와 failover를 고려했다.

# 수치 해석

회사 소개는 기존 대비 최대 약 95% 수준의 비용 절감과 무중단 failover를 결과로 제시한다. 이는 무신사의 workload, hardware 조달가와 cloud 요금 조건에서 나온 사례다. 온프레미스의 인건비·전력·상면·감가상각·spare 장비와 장애 대응까지 포함한 TCO를 계산해야 다른 조직에도 유리한지 판단할 수 있다.

# 실무 교훈

하이브리드는 “싼 GPU를 연결하는 일”이 아니라 ownership을 옮기는 일이다. 먼저 작은 inference workload로 network, scheduling, observability와 failover를 검증하고, 비용 상한·성능 SLO·cloud fallback 조건을 숫자로 정한 뒤 범위를 넓힌다.

# 출처

- [무신사 기술 글 원문](https://medium.com/musinsa-tech/%EC%9A%B0%EB%A6%AC%EB%8A%94-%EB%8B%AC%EC%97%90-%EA%B0%80%EA%B8%B0%EB%A1%9C-%ED%96%88%EC%8A%B5%EB%8B%88%EB%8B%A4-hybrid%EC%9D%B8%ED%94%84%EB%9D%BC%EB%B6%80%ED%84%B0-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-%EC%B5%9C%EC%A0%81%ED%99%94%EA%B9%8C%EC%A7%80-%EB%AC%B4%EC%8B%A0%EC%82%AC-ai-infra%EA%B5%AC%EC%B6%95%EA%B8%B0-3ffe4831c0a4)
- [무신사 공식 LinkedIn 소개](https://kr.linkedin.com/posts/musinsacom_%EC%9A%B0%EB%A6%AC%EB%8A%94-%EB%8B%AC%EC%97%90-%EA%B0%80%EA%B8%B0%EB%A1%9C-%ED%96%88%EC%8A%B5%EB%8B%88%EB%8B%A4-hybrid%EC%9D%B8%ED%94%84%EB%9D%BC%EB%B6%80%ED%84%B0-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-%EC%B5%9C%EC%A0%81%ED%99%94%EA%B9%8C%EC%A7%80-activity-7406573798855999488-OP7t)
- [Notion 원본 항목](https://app.notion.com/p/14c1a73cf20b8234a87401337771d274)
