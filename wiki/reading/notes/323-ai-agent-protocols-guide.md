---
type: Concept
title: "AI 에이전트 프로토콜 6종의 역할과 경계"
description: "MCP, A2A, UCP, AP2, A2UI, AG-UI를 도구·협업·상거래·결제·UI 계층으로 구분한 개발자 가이드"
resource: "https://developers.googleblog.com/developers-guide-to-ai-agent-protocols/"
notion: "https://app.notion.com/p/9561a73cf20b83f8bfed8120f48efab4"
tags: [reading, ai-agent, protocol, mcp, interoperability]
timestamp: 2026-07-24
status: summarized
---

# 핵심 구분

Google의 예제는 식당 공급망 agent에 여섯 protocol을 붙이며 각각이 해결하는 경계를 보여 준다.

| Protocol | 주된 연결 | 역할 |
|---|---|---|
| MCP | agent ↔ tool/data | tool 정의와 호출, resource discovery |
| A2A | agent ↔ agent | Agent Card를 통한 capability discovery와 원격 협업 |
| UCP | 구매자 ↔ 판매자 | 상품 탐색부터 checkout까지의 상거래 lifecycle |
| AP2 | agent ↔ 결제 체계 | 사용자의 결제 의도·승인·영수증을 mandate로 감사 가능하게 기록 |
| A2UI | agent → user interface | 제한된 primitive로 안전한 선언형 UI 구조 전달 |
| AG-UI | backend agent ↔ frontend | 실행·도구·텍스트 상태를 typed SSE event로 streaming |

# 설계 시사점

MCP를 붙였다고 agent 간 협업이나 결제 권한이 생기는 것은 아니다. A2A의 `/.well-known/agent-card.json`, UCP discovery, AP2의 `IntentMandate → PaymentMandate → PaymentReceipt`, A2UI의 구조·데이터 분리, AG-UI의 event stream처럼 각 계층의 계약을 따로 설계해야 한다.

# 한계

Protocol 채택만으로 인증, 신뢰, 권한 정책, version 호환성, 장애 복구와 observability가 해결되지는 않는다. 특히 상거래·결제 계층은 idempotency, 사용자 동의와 감사 로그를 application 수준에서도 검증해야 한다. 글의 API와 성숙도는 2026년 3월 시점이므로 구현 전 최신 공식 specification을 다시 확인한다.

# 출처

- [Developer's Guide to AI Agent Protocols](https://developers.googleblog.com/developers-guide-to-ai-agent-protocols/)
