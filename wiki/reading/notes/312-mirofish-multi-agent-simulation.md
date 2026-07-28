---
type: Reference
title: "MiroFish: 현실 자료로 가상 사회를 만드는 멀티에이전트 시뮬레이션"
description: "seed 자료에서 관계 그래프와 persona를 만들고 다수 에이전트의 상호작용을 보고서와 대화형 세계로 제공하는 엔진"
resource: "https://github.com/666ghj/MiroFish"
notion: "https://app.notion.com/p/0511a73cf20b83ec8e1d81e64aef6255"
tags: [reading, multi-agent, simulation, graphrag]
timestamp: 2026-07-24
status: summarized
---

# 동작 방식

뉴스, 정책 초안, 분석 보고서나 소설 같은 seed 자료에서 가상 사회를 구성하고 다수 에이전트의 상호작용을 시뮬레이션하는 프로젝트다. 각 agent에 persona, 장기 기억과 행동 규칙을 주고 사용자가 중간 변수를 넣어 이후 전개를 관찰한다. 결과는 예측 보고서와 개별 agent 또는 ReportAgent와 대화할 수 있는 세계로 제공된다.

파이프라인은 네 단계로 볼 수 있다.

1. Seed에서 entity와 관계를 뽑아 GraphRAG와 개인·집단 기억을 만든다.
2. Persona와 환경 설정을 agent에 주입한다.
3. 두 platform에서 병렬 simulation을 돌리고 시간에 따라 memory를 갱신한다.
4. ReportAgent가 사후 환경을 탐색해 보고서를 만들고 추가 질문을 받는다.

실행에는 Node.js 18+, Python 3.11~3.12와 `uv`가 필요하다. OpenAI SDK 호환 LLM endpoint와 Zep Cloud key를 설정하며, source 설치와 Docker Compose를 모두 지원한다. 프로젝트는 높은 token 소비를 경고하며 처음에는 40 round 미만을 권한다. Simulation core는 CAMEL-AI의 OASIS를 사용한다.

# “예측”을 읽는 기준

에이전트 사회는 가능한 시나리오를 탐색하는 sandbox이지 미래를 통계적으로 예측하는 검증된 모형은 아니다. Persona 생성, seed의 누락, LLM의 공통 편향과 상호작용 규칙이 결과를 크게 좌우한다. 정책·금융 의사결정에서는 여러 seed와 parameter에 대한 민감도 분석, 실제 관측자료를 이용한 calibration, 반대 가설과 인간 전문가 검토가 필요하다.

외부 문서를 cloud LLM과 Zep에 보내므로 개인정보와 기밀 자료를 넣기 전에 데이터 흐름을 확인해야 한다. 라이선스는 AGPL-3.0이다.

# 출처

- [MiroFish 저장소](https://github.com/666ghj/MiroFish)
