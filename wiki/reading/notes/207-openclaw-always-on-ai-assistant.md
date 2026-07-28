---
type: Reference
title: "OpenClaw 열풍이 보여준 상시 실행형 개인 AI 비서"
description: "메신저, 장기 기억과 컴퓨터 실행 권한을 결합한 개인 AI 에이전트의 매력과 보안·비용 위험"
resource: https://share.google/WfVuU3BL3dILIAlv5
resource_aliases: [https://brunch.co.kr/@sungdairi/19]
notion: https://app.notion.com/p/64d1a73cf20b83b29ba1012ed7e13caa
tags: [reading, ai-agents, openclaw, security]
timestamp: 2026-07-24
status: summarized
---

# 글의 관점

이 글은 당시 여러 이름으로 불리던 OpenClaw 계열 도구의 인기를 “질문에 답하는 chatbot”에서 “기억하고 먼저 행동하는 상시 실행형 비서”로의 전환으로 설명한다. 메신저로 요청을 받고 개인 computer에서 browser, file, email과 외부 API를 조작하는 경험이 핵심이다.

# 무엇이 달라지는가

- 대화가 끝나도 file 기반 memory에 작업 맥락을 남긴다.
- 사용자가 요청할 때만 답하지 않고 schedule과 event에 따라 먼저 실행할 수 있다.
- coding, 예약, monitoring처럼 결과가 필요한 일을 tool로 직접 수행한다.
- 저전력 소형 computer를 계속 켜 두는 개인 server 방식과 잘 맞는다.

# 위험과 운영 원칙

강한 실행 권한은 prompt injection, 잘못된 결제·메시지, secret 노출과 예상 밖 API 비용으로 바로 이어질 수 있다. 별도 OS account나 container, tool allowlist, 금액·수신자별 승인, secret 분리, 비용 한도와 action log가 필요하다. 글에 소개된 바이럴 사례와 비용 수치는 원출처를 다시 확인하지 않은 사례가 포함될 수 있으므로 제품 능력의 증거로 그대로 받아들이면 안 된다.

# 출처

- [원문: 실리콘밸리가 미쳐버린 AI 도구, 클로드봇](https://brunch.co.kr/@sungdairi/19)
- [저장된 Google 공유 링크](https://share.google/WfVuU3BL3dILIAlv5)
