---
type: Reference
title: "Hermes Agent 사용 관점: 기억 유지와 경험의 skill화가 드러나는 시점"
description: "자기 학습 loop, cross-session memory, 다중 channel과 실행 backend를 소개하고 초기 체감 차이를 토론한 GeekNews 글"
resource: https://news.hada.io/topic?id=28101
notion: https://app.notion.com/p/4ab1a73cf20b8231aea7813566f00e68
tags: [reading, ai-agents, memory, self-improvement]
timestamp: 2026-07-24
status: summarized
---

# 소개된 기능

Hermes Agent는 IDE 안의 coding copilot보다 장시간 실행되는 개인 agent를 지향한다. 작업 중 복잡한 절차를 skill로 만들고 개선하며, Honcho 기반 사용자 model과 FTS5 recall을 이용해 session 사이의 기억을 누적한다. 40개 이상의 tool, MCP, scheduler, parallel subagent와 Python RPC를 제공한다.

CLI 외에도 Telegram, Discord, Slack, WhatsApp, Signal과 email을 gateway로 연결하고 local, Docker, SSH와 serverless backend에서 실행할 수 있다. OpenRouter·OpenAI·Kimi 계열 등 여러 model을 바꿔 쓸 수 있어 interface, memory와 실행 환경을 특정 model에서 분리한다.

# 토론에서 드러난 현실

댓글에서는 처음 설치한 백지 상태라면 OpenClaw 같은 다른 personal-agent 도구와 차이를 체감하기 어렵다는 의견이 나온다. memory와 self-modification의 이점은 여러 session과 실패·재시작을 거쳐 기록이 쌓여야 나타난다는 것이다. 한 사용자는 session context replay 덕분에 model fallback이나 restart 후 기억 유실이 적었다고 평가했다.

반대로 agent가 자기 workspace의 source를 수정해 만든 local 변경과 upstream update 사이의 관리가 명확하지 않아, update 때 변경이 reset될 수 있다는 실제 문제도 제기됐다. “스스로 개선한다”는 기능은 변경 이력, rollback과 upstream merge 정책이 없으면 재현성과 공급망 위험을 키울 수 있다.

# 운영 원칙

Message channel을 연결하면 prompt injection이 shell·credential·외부 발송으로 이어질 수 있다. channel별 sender allowlist, 격리된 execution backend, 최소 권한 secret, human approval과 audit log를 먼저 둔다. 자동 생성된 skill은 일반 code change처럼 diff·test·version을 검토하고, remote install script도 실행 전에 내용을 확인한다.

공식 저장소 구조와 설치 중심의 정리는 [Hermes Agent 공식 저장소 중심 정리](248-hermes-agent-self-improving-assistant.md)에 있다. 이 문서는 URL별 보존 원칙에 따라 GeekNews의 요약과 사용자 토론을 따로 남긴다.

# 출처

- [GeekNews 소개와 토론](https://news.hada.io/topic?id=28101)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)

