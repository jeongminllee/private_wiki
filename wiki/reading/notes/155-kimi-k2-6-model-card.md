---
type: Reference
title: "Kimi K2.6 모델 카드"
description: "장기 코딩, 멀티모달 입력, 도구 사용과 대규모 에이전트 오케스트레이션을 겨냥한 1T MoE 모델"
resource: https://huggingface.co/moonshotai/Kimi-K2.6
notion: https://app.notion.com/p/1961a73cf20b8278903f81f124f2df30
tags: [reading, kimi, multimodal, moe, ai-agents]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Kimi K2.6은 코딩과 에이전트 작업에 초점을 둔 네이티브 멀티모달 오픈 모델이다. 모델 카드는 장시간 코딩, 시각 입력 기반 UI 생성, 능동적 백그라운드 실행, 다수 하위 에이전트의 병렬 조정을 주요 능력으로 제시한다.

# 모델 구조

| 항목 | 값 |
| --- | ---: |
| 전체 파라미터 | 1T |
| 활성 파라미터 | 32B |
| 컨텍스트 길이 | 256K |
| 전문가 수 | 384 |
| 토큰당 선택 전문가 | 8 |
| 비전 인코더 | MoonViT, 400M |

# 배포와 사용

- 공식 API는 OpenAI·Anthropic 호환 인터페이스를 제공한다.
- 자체 배포는 vLLM, SGLang, KTransformers가 권장된다.
- 네이티브 INT4 양자화를 제공한다.
- Thinking과 Instant 모드의 권장 샘플링 값이 다르다.
- 이미지와 영상 입력을 지원하지만 영상 입력은 공식 API에서만 실험적으로 제공된다고 안내한다.

# 주의

모델 카드의 벤치마크와 300개 하위 에이전트 실험은 제작자의 자체 보고다. 실제 선택에서는 한국어 품질, 코드 저장소 규모, 도구 호출 성공률, GPU 메모리와 라이선스를 같은 조건에서 비교해야 한다.

# 관련 문서

- [Kanana 사전학습](122-kanana-llm-pretraining.md)
- [GLM-4.7-Flash GGUF 로컬 실행](148-glm-4-7-flash-gguf-local-deployment.md)

# 출처

- [Moonshot AI Kimi K2.6 모델 카드](https://huggingface.co/moonshotai/Kimi-K2.6)

