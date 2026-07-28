---
type: Reference
title: "OpenGenerativeUI: 대화에서 실행 가능한 시각 자료 만들기"
description: "LLM이 chart, diagram, simulation과 3D widget용 HTML을 만들고 sandbox iframe에 렌더링하는 framework"
resource: https://news.hada.io/topic?id=27570
notion: https://app.notion.com/p/2ea1a73cf20b82b287cc81ac21716060
tags: [reading, generative-ui, frontend, ai-agents]
timestamp: 2026-07-24
status: summarized
---

# 개념

OpenGenerativeUI는 text answer 대신 질문에 맞는 chart, algorithm visualization, diagram, form, simulation이나 3D scene을 실시간 생성한다. agent가 response 형태를 결정하고 frontend가 생성된 HTML을 sandbox iframe 안에서 표시한다.

# 구성

Next.js 16·React 19 frontend와 LangGraph·CopilotKit 기반 Python agent를 사용한다. 요청 유형에 따라 SVG, HTML, Chart.js, Three.js와 D3.js를 고르는 decision matrix가 있고, loading skeleton, responsive height와 theme를 처리한다.

# 보안과 제품 품질

iframe은 격리의 시작점일 뿐이다. 생성 HTML의 script, network, storage와 top navigation 권한을 `sandbox`·CSP로 제한하고 외부 URL allowlist를 둬야 한다. 시각화는 데이터 단위, axis, accessibility와 mobile layout을 자동 test해야 하며, 생성 코드가 그럴듯하게 보이는 것과 수치가 정확한 것은 구분해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27570)
- [CopilotKit/OpenGenerativeUI](https://github.com/CopilotKit/OpenGenerativeUI)

