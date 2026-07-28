---
type: Setup Guide
title: "AWS·Kubernetes·Ray 기반 확장형 Agentic RAG pipeline"
description: "LangGraph, hybrid retrieval과 CPU control plane·GPU data plane을 Terraform·EKS로 배포하는 end-to-end 예제"
resource: "https://levelup.gitconnected.com/building-a-scalable-production-grade-agentic-rag-pipeline-1168dcd36260?gi=b29ab687d2e1"
notion: "https://app.notion.com/p/6081a73cf20b83999a8d817014648cb9"
tags: [reading, rag, kubernetes, ray, aws, langgraph]
timestamp: 2026-07-24
status: summarized
---

# 구조

Platform은 HTTP·state·agent orchestration을 맡는 CPU control plane과 inference·embedding·graph extraction을 맡는 autoscaling GPU data plane을 분리한다. LangGraph planner가 direct answer, retrieval 또는 code tool을 선택하고 query rewriting·HyDE를 수행한다. Qdrant dense vector와 Neo4j relationship graph를 결합해 hybrid retrieval한다.

# 배포 흐름

Terraform으로 VPC, EKS, S3, RDS와 IAM을 만들고 Kubernetes에 Karpenter, KubeRay, secret·ingress controller를 설치한다. Ray Serve는 BGE-M3 embedding과 vLLM model service를 제공한다. FastAPI control plane은 streaming endpoint와 인증을 담당한다.

S3 event가 ingestion job을 시작하면 Ray Data가 PDF·DOCX·HTML을 parsing·chunking하고 embedding과 `(subject, predicate, object)` 추출을 분산 실행한다. Vector는 Qdrant, node와 edge는 Neo4j에 쓴다. Health check와 end-to-end request 뒤 spot instance와 scale-to-zero로 비용을 조정한다.

# 주의

README의 예시 password, cluster version과 model은 그대로 production에 쓰지 않는다. Public subnet, secret rotation, network policy, backup, PII 삭제와 prompt injection 방어를 설계해야 한다. Spot·scale-to-zero 절감률과 70B model startup은 지역, quota와 image cache에 크게 좌우된다. 전체 stack이 크므로 규모가 작을 때는 managed service나 단순 pipeline과 총비용을 비교한다.

# 출처

- [원문](https://levelup.gitconnected.com/building-a-scalable-production-grade-agentic-rag-pipeline-1168dcd36260)
- [scalable-rag-pipeline 저장소](https://github.com/FareedKhan-dev/scalable-rag-pipeline)
