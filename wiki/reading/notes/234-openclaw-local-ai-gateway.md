---
type: Reference
title: "OpenClaw: 로컬에서 모델·메신저·도구를 연결하는 AI Gateway"
description: "개인 computer 또는 server에서 여러 LLM과 communication channel을 연결해 실제 작업을 수행하는 open-source assistant"
resource: https://discuss.pytorch.kr/t/openclaw-ai-clawdbot-moltbot/8849
notion: https://app.notion.com/p/a261a73cf20b83f69c3981eb36d588f4
tags: [reading, openclaw, ai-agents, self-hosted]
timestamp: 2026-07-24
status: summarized
---

# 역할

OpenClaw은 개인 장비나 server에서 실행되며 WhatsApp, Telegram, Discord 같은 channel과 Claude, GPT, local model을 연결하는 agent gateway다. 대화만 생성하지 않고 file, browser, calendar와 system tool을 사용해 행동하는 것을 목표로 한다.

# SaaS chatbot과의 차이

사용자는 model, memory, channel과 tool을 직접 조합하고 data·log의 저장 위치를 통제한다. 반대로 설치, update, uptime, API 비용과 보안 정책도 직접 책임진다. self-hosted라는 사실만으로 입력이 외부에 나가지 않는 것은 아니며 remote model API를 쓰면 prompt와 첨부 자료가 provider로 전송될 수 있다.

# 안전한 시작

처음에는 read-only tool과 단일 channel로 시작하고 sender allowlist, separate OS account·container, secret vault, 민감 action 승인, 비용 한도와 audit log를 추가해야 한다. 프로젝트 명칭과 package가 여러 번 바뀐 시기의 문서는 오래된 설치 주소를 포함할 수 있으므로 현재 공식 repository와 release를 확인한다.

# 연결 문서

사용 사례와 위험은 [OpenClaw 열풍이 보여준 상시 실행형 개인 AI 비서](207-openclaw-always-on-ai-assistant.md), Claude 기능 비교는 [Claude와 OpenClaw이 만나는 지점](208-claude-and-openclaw-agent-features.md)에 정리되어 있다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/openclaw-ai-clawdbot-moltbot/8849)

