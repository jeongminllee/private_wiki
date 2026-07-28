---
type: Project
title: "CandleView: 프로그래밍 가능한 금융 시계열 chart engine"
description: "캔들, 보조지표와 drawing tool을 제공하고 AI 분석 service를 연결할 수 있는 TypeScript chart project"
resource: "https://discuss.pytorch.kr/t/candleview-ai-feat/8507"
notion: "https://app.notion.com/p/b461a73cf20b8279a4ea81e365e8d6fe"
tags: [reading, visualization, time-series, finance, typescript]
timestamp: 2026-07-24
status: summarized
---

# 기능

CandleView는 OHLCV 금융 시계열을 candlestick으로 표시하고 MA, EMA, Bollinger Bands, Ichimoku, VWAP, RSI, MACD 등 보조지표와 Fibonacci·Gann·trend line drawing tool을 제공한다. Timeframe, theme, locale, screenshot과 command interface도 지원한다.

2025년 소개 글은 React component와 여러 LLM provider를 통한 자연어 chart 분석·예측을 핵심으로 설명했다. 현재 repository는 engine core, React와 Vue package를 분리하고 `@candleview/core`를 설치하는 구조이며 AI service용 proxy scaffold를 별도 영역으로 둔다. 문서와 package 구조가 변했으므로 과거 예제를 그대로 실행하지 않는다.

# 보안과 해석

LLM에 OHLCV를 전달해 만든 추세·위험 설명은 통계적 예측이나 투자 자문으로 검증된 결과가 아니다. API key를 browser에 넣지 말고 server-side proxy, rate limit과 data minimization을 사용한다. 사용자 입력 data가 외부 model provider로 전송되는 범위도 명시한다.

# 라이선스

Repository는 AGPL-3.0이다. Network service에 포함할 때 source 공개 의무가 application 전체에 미치는 범위를 법률·license 담당자와 검토한다. PyTorchKR 글도 AI로 정리한 2차 소개임을 밝히므로 현재 README와 release를 우선한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/candleview-ai-feat/8507)
- [CandleView 저장소](https://github.com/0xhappyboy/candleview)
