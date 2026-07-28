---
type: Reference
title: "Step 3.5 Flash: 희소 MoE로 속도와 에이전트 성능을 함께 노리기"
description: "196B 중 11B를 활성화하고 256K 문맥과 고속 생성을 지원하는 오픈 가중치 추론 모델"
resource: https://news.hada.io/topic?id=26834
notion: https://app.notion.com/p/feb1a73cf20b828e9fb301583e811acd
tags: [reading, llm, mixture-of-experts, ai-agents]
timestamp: 2026-07-24
status: summarized
---

# 모델 개요

Step 3.5 Flash는 전체 196B parameter 중 token마다 11B만 활성화하는 sparse MoE 모델이다. 3:1 비율의 sliding-window attention과 full attention, head-wise gated attention을 사용해 256K context에서 연산량을 줄인다.

# 보고된 성능과 활용

- NVIDIA Hopper에서 최대 350 token/s, 일반 작업에서 100~300 token/s를 보고한다.
- SWE-bench Verified 74.4%, Terminal-Bench 2.0 51.0%를 제시한다.
- Python과 여러 MCP tool을 이용하는 분석, research, codebase wiki 생성 사례를 공개했다.
- INT4 GGUF가 있어 충분한 통합 memory를 가진 Mac이나 GPU system에서 로컬 실행할 수 있다.
- 장기 reasoning 안정화를 위해 표본을 이진 필터링하는 MIS-PO 강화학습 방법을 소개한다.

# 해석할 때 주의할 점

전체 parameter 수가 곧 실행 memory가 작다는 뜻은 아니다. MoE는 token당 계산량을 줄이지만 모든 expert weight를 올릴 memory는 여전히 크다. 벤치마크와 속도는 제공자가 선택한 hardware, prompt, tool 환경에 의존하므로 자신의 coding harness에서 completion rate, 반복 loop, tool-call 오류와 비용을 재측정해야 한다. 사용자 토론에는 무한 reasoning loop와 chat template 설정 문제가 보고되어 있다.

# 출처

- [GeekNews 정리와 토론](https://news.hada.io/topic?id=26834)

