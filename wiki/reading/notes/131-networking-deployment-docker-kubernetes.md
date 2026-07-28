---
type: Reference
title: "네트워크와 배포: Docker에서 Kubernetes까지"
description: "IP·port·DNS·방화벽부터 container packaging과 선언형 orchestration으로 이어지는 학습 지도"
resource: https://f-lab.kr/insight/understanding-network-and-deployment-20251215
notion: https://app.notion.com/p/a101a73cf20b837baa1781a06c022c8d
tags: [reading, networking, docker, kubernetes]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

애플리케이션이 local에서 실행되는 것과 사용자가 안정적으로 접근하는 것은 다른 문제다. 배포를 이해하려면 먼저 process가 어떤 interface와 port에서 listen하고, DNS와 route, firewall·load balancer를 거쳐 packet이 어떻게 도달하는지 추적할 수 있어야 한다.

# 단계별 학습

1. `IP`, subnet, route, DNS, TCP/UDP, port와 HTTP/TLS를 익힌다.
2. host에서 process를 실행하고 `curl`, `ss` 또는 `netstat`, DNS lookup과 log로 통신을 추적한다.
3. Docker image에 runtime과 dependency를 고정하고 volume, network, environment와 secret을 분리한다.
4. Docker Compose로 API·DB 등 여러 service를 한 host에서 재현한다.
5. 실제로 여러 node, self-healing, rollout과 autoscaling이 필요할 때 Kubernetes를 배운다.

# 선언형 운영

Compose와 Kubernetes manifest는 실행 절차보다 원하는 상태를 적고 controller가 현재 상태와의 차이를 줄이게 한다. 이 방식은 재현성과 review를 높이지만, 잘못된 선언을 자동으로 반복할 수도 있다. health check, resource limit, observability, rollback과 secret 관리가 함께 필요하다.

# 보완해서 읽기

원문은 입문 개요이며 “Kubernetes는 대규모 환경에 필수” 같은 표현은 과하다. 작은 서비스는 managed platform, VM이나 Compose가 더 단순하고 안전할 수 있다. 도구보다 traffic, availability, team skill과 운영 비용을 기준으로 선택한다.

# 출처

- [F-Lab 원문](https://f-lab.kr/insight/understanding-network-and-deployment-20251215)
- [Notion 원본 항목](https://app.notion.com/p/a101a73cf20b837baa1781a06c022c8d)
