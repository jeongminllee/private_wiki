---
type: Reference
title: "NemoClaw: OpenClaw에 NVIDIA model과 sandbox를 결합한 agent stack"
description: "Nemotron, OpenShell과 Agent Toolkit을 묶은 NemoClaw preview의 구성과 보안 검증 항목"
resource: https://news.hada.io/topic?id=27569
notion: https://app.notion.com/p/6af1a73cf20b829e826c816fe78cd188
tags: [reading, ai-agent, nvidia, sandbox]
timestamp: 2026-07-24
status: summarized
---

# 구성

NemoClaw는 OpenClaw agent에 NVIDIA의 Nemotron model, OpenShell sandbox와 Agent Toolkit을 결합한 early-preview stack이다. GeForce RTX workstation부터 DGX급 system까지 NVIDIA hardware에서 local 또는 hybrid agent를 배포하는 흐름을 제공한다.

# 목표

- agent의 file·network·tool 접근을 policy로 제한
- sensitive data를 local model에 두고 필요한 요청만 cloud로 routing
- Nemotron model과 NVIDIA inference stack을 기본 경로로 사용
- 설치와 onboarding을 단순화해 OpenClaw ecosystem을 NVIDIA 환경에 연결

소개된 quick start는 install script를 `curl`로 받아 실행한 뒤 `nemoclaw onboard`로 초기 설정하는 방식이다.

# 실제 검토 포인트

“Secure”라는 이름만으로 안전성을 가정하면 안 된다. Sandbox escape, secret mount, outbound network allowlist, tool별 permission, prompt injection과 audit log를 위협 model에 맞춰 시험해야 한다. Privacy router도 어떤 data를 local·cloud로 분류하는지, 잘못 분류했을 때 fail-closed인지 확인해야 한다.

또한 shell에서 remote install script를 바로 실행하는 방식은 편리하지만 supply-chain 위험이 있다. production에서는 script를 먼저 내려받아 hash·내용을 검토하고 version을 고정하는 편이 낫다. Early preview이므로 API 안정성, 지원 hardware와 운영 비용도 도입 전 재확인해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27569)

