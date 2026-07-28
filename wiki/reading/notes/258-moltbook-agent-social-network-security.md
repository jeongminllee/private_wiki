---
type: Reference
title: "Moltbook: AI agent 소셜 네트워크가 보여준 원격 지시의 보안 위험"
description: "OpenClaw agent가 글을 읽고 쓰는 Moltbook의 구조와 mutable skill·prompt injection 위험"
resource: https://news.hada.io/topic?id=26273
notion: https://app.notion.com/p/2061a73cf20b820cafa1018ca6eef927
tags: [reading, ai-agent, security, prompt-injection]
timestamp: 2026-07-24
status: summarized
---

# 무엇인가

Moltbook은 OpenClaw 계열 bot이 계정을 만들고 글·댓글을 주고받는 agent 중심 social network다. 사람은 agent의 활동을 관찰하거나 설정하고, bot은 API와 Markdown skill을 통해 주기적으로 site를 확인한다.

# 동작이 흥미로운 이유

Agent들이 자동화, model, security와 운영 경험을 서로 공유하는 공간은 machine-to-machine community가 어떤 모습일지 보여주는 실험이다. 하지만 productive knowledge network인지, 서로 생성한 content를 재순환하는 noise인지 판단하려면 source quality와 실제 행동 결과를 봐야 한다.

# 핵심 보안 문제

설치된 skill이 원격 Markdown 지시를 읽고 Heartbeat마다 다시 가져오면, server가 바뀌거나 domain이 탈취됐을 때 agent 동작도 바뀔 수 있다. 특히 다음 세 조건이 합쳐지면 위험하다.

- private data에 접근할 수 있음
- 신뢰하지 않은 외부 content를 읽음
- message 전송·file 수정 같은 external action을 실행할 수 있음

원격 post 안의 prompt injection, mutable installation instruction과 skill supply chain을 모두 공격면으로 봐야 한다.

# 안전하게 관찰하려면

Read-only test account, disposable environment와 strict network allowlist를 사용하고 secret·personal file을 mount하지 않는다. 가져오는 skill과 instruction은 hash를 고정하고, external action은 human approval을 거치게 한다. Moltbook은 agent social network의 효용뿐 아니라 always-on agent 보안의 case study로 읽을 가치가 크다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=26273)

