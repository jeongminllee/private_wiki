---
type: Reference
title: "Claw3D: 자가 호스팅 AI 에이전트를 위한 3D 가상 사무실"
description: "에이전트 실행 상태, 협업과 외부 업무 흐름을 3D 공간에서 관찰·조작하는 시각화 계층"
resource: "https://github.com/iamlukethedev/Claw3D"
notion: "https://app.notion.com/p/9b61a73cf20b8394bbec01625a73d6c2"
tags: [reading, ai-agents, visualization, openclaw]
timestamp: 2026-07-24
status: summarized
---

# 무엇을 만드는가

Claw3D는 AI 에이전트 자체를 구현하는 엔진이 아니라, 자가 호스팅 에이전트를 3D 가상 사무실에서 관찰하고 상호작용하는 시각화 계층이다. OpenClaw Gateway, Hermes adapter, 사용자 정의 HTTP runtime과 데모 gateway를 연결할 수 있다. 프로젝트는 OpenClaw와 공식 관계가 없는 비공식 도구다.

사용자는 에이전트가 어느 작업에 붙어 있는지 보고, stand-up, GitHub·Jira 작업, PR review, QA log 등을 공간 안에서 확인할 수 있다. 환경 builder, agent skill gym, 오래된 session을 정리하는 janitor 같은 운영 기능도 포함한다. 실제 runtime 상태는 backend가 관리하고, 화면 관련 선호는 local UI에 남으며, adapter와 proxy가 서로 다른 agent runtime을 연결한다.

# 설계상 의미

텍스트 로그만 있는 멀티에이전트 시스템은 현재 누가 무엇을 하고 있고 어디서 막혔는지 파악하기 어렵다. 공간 은유는 상태, 역할과 상호작용을 한눈에 보여 줄 수 있다. 다만 3D 표현이 원인 분석이나 정확한 trace를 대신하지는 않는다. 운영 화면은 탐색과 상황 인식에 쓰고, 세부 진단은 구조화 로그·trace·metric으로 내려가야 한다.

# 보안 주의

시각화 계층에는 prompt, 승인 요청, 작업 로그, 외부 서비스 상태와 실행 명령이 모이기 쉽다. Gateway 인증, WebSocket origin, 원격 실행 권한과 로그 마스킹을 별도로 점검해야 한다. 인터넷에 그대로 노출하면 단순 대시보드보다 훨씬 큰 공격 표면이 된다. 라이선스는 MIT다.

# 출처

- [Claw3D 저장소](https://github.com/iamlukethedev/Claw3D)
