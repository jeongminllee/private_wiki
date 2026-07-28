---
type: Reference
title: "ZeroClaw: Rust 기반 초경량 로컬 AI 에이전트"
description: "작은 단일 바이너리, 교체 가능한 구성요소, 로컬 메모리와 실행 격리를 지향하는 에이전트 런타임"
resource: https://discuss.pytorch.kr/t/zeroclaw-100-rust/9166
notion: https://app.notion.com/p/2df1a73cf20b834b97a5814a6d826040
tags: [reading, ai-agents, rust, local-first]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

ZeroClaw는 Rust로 작성된 로컬 우선 AI 에이전트 런타임이다. 모델, 메시지 채널, 도구, 메모리를 trait 기반 인터페이스로 분리하고 작은 단일 실행 파일로 저사양 장치에서도 동작하는 것을 목표로 한다.

# 주요 구성

- 릴리스 빌드가 약 8.8MB이고 런타임 메모리가 5MB 미만이라는 수치를 프로젝트가 제시한다.
- OpenAI·Anthropic·Gemini API와 Ollama·LM Studio 같은 로컬 endpoint를 교체할 수 있다.
- Slack, Discord, Telegram, WhatsApp 등 메시지 채널과 daemon·gateway 모드를 지원한다.
- SQLite에 대화와 문서를 저장하고 벡터·키워드 검색을 결합한다.
- workspace 격리, 명령 allowlist, pairing code, 로컬 비밀정보 저장을 보안 장치로 둔다.

# 확인할 점

작은 런타임의 메모리와 에이전트가 호출하는 모델의 메모리는 별개다. “OpenClaw보다 메모리 99% 절감” 같은 수치는 프로젝트가 정한 비교 조건에 의존하므로 같은 모델·도구·작업으로 재측정해야 한다. 로컬 실행도 메시지 채널이나 클라우드 모델을 연결하면 데이터가 외부로 나갈 수 있다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/zeroclaw-100-rust/9166)
- [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)

