---
type: Reference
title: "GPT-5.2 출시 전망 기사와 공식 발표 대조"
description: "2025년 12월 9일 출시설과 경쟁 구도 보도를 실제 12월 11일 OpenAI 발표 및 공개 사양과 분리한 기록"
resource: "https://www.aitimes.com/news/articleView.html?idxno=204566"
notion: "https://app.notion.com/p/ab81a73cf20b82319aaf01ea1d3aa4a9"
tags: [reading, openai, gpt-5-2, fact-check, release]
timestamp: 2026-07-24
status: summarized
---

# 당시 보도

2025년 12월 6일 AI타임스 기사는 익명 소식통을 인용한 보도를 바탕으로 OpenAI가 GPT-5.2를 12월 9일 출시할 예정이며, Gemini 3의 압박 때문에 원래 월말 계획을 앞당겼다고 전했다. `Shallotpeat`, `Garlic`이라는 내부 project와 경쟁 모델보다 추론·coding 성능이 높다는 주장도 함께 실렸다.

이 내용은 출시 전 보도였다. 기사 자체도 GPT-5.2에 대해 알려진 내용이 거의 없다고 밝혔으며, 일정·내부 code name·경쟁 압력과 사내 성능 평가는 당시 OpenAI가 확인한 공식 정보가 아니었다.

# 실제 발표

OpenAI는 기사에서 예측한 9일이 아니라 2025년 12월 11일 GPT-5.2를 공식 발표하고 ChatGPT와 API에 순차 배포했다. 제품군은 Instant, Thinking, Pro로 나뉘었으며 API에서는 `gpt-5.2-chat-latest`, `gpt-5.2`, `gpt-5.2-pro`라는 이름을 사용했다.

공식 발표는 전문 지식 작업, coding, long-context reasoning, vision과 tool calling 개선을 강조했다. 예를 들어 GPT-5.2 Thinking은 OpenAI가 공개한 설정에서 SWE-Bench Pro 55.6%, SWE-bench Verified 80.0%를 기록했다. 이 수치는 vendor evaluation이므로 다른 모델과 비교할 때 harness, reasoning effort, 도구 사용과 제외 문항을 함께 확인해야 한다.

# 교훈

출시 전 경쟁 보도는 당시 시장 분위기와 예상 일정을 이해하는 자료로는 유용하지만, 제품 사양의 근거로 재사용하면 안 된다. 공개 후에는 날짜, model name, availability와 benchmark를 공식 release로 갱신하고, 확인되지 않은 내부 code name과 “정상 탈환” 같은 평가는 별도 주장으로 남겨야 한다.

# 출처

- [2025년 12월 6일 AI타임스 기사](https://www.aitimes.com/news/articleView.html?idxno=204566)
- [OpenAI의 GPT-5.2 공식 발표](https://openai.com/index/introducing-gpt-5-2/)
- [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

