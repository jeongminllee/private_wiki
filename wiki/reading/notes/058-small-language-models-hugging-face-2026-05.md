---
type: Reference
title: "2026년 5월 Hugging Face 소형 언어 모델 목록"
description: "7B 미만 모델을 작업 유형과 배포 제약에 따라 고르기 위한 시점 고정 비교 목록"
resource: https://www.kdnuggets.com/best-small-language-models-on-hugging-face-right-now
notion: https://app.notion.com/p/3681a73cf20b8124a38adc4758236ae1
tags: [reading, small-language-model, hugging-face, local-ai]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

이 글은 2026년 5월을 기준으로 7B 미만 공개 모델을 모은 선택 가이드다. 하나의 “최고 모델”을 정하기보다 언어, 추론, 멀티모달, 모바일, 라이선스와 하드웨어 제약에 따라 후보를 좁히는 출발점으로 유용하다.

# 소개된 후보

- **Qwen3.5 4B**: 다국어와 범용 작업 후보
- **Phi-4-mini 3.8B**: 영어 중심 추론과 지시 수행 후보
- **Gemma 3 4B IT**: 수학·코드와 멀티모달 생태계 후보
- **Gemma 3n E4B**: 모바일과 엣지 실행을 고려한 후보
- **Llama 3.2 3B Instruct**: 넓은 도구·배포 생태계가 장점
- **SmolLM3 3B**: 학습 정보와 공개성을 중시할 때 검토
- **DeepSeek-R1-Distill-Qwen 1.5B**: 작은 크기의 추론 실험 후보
- **Qwen3 0.6B**: 자원이 매우 제한된 단순 작업 후보

# 선택 방법

모델 카드의 평균 벤치마크보다 자신의 작업 세트를 먼저 만든다. 한국어 지시, 코드 수정, JSON 도구 호출, 긴 문맥 회수처럼 실제 입력을 사용하고 정확성, 지연, VRAM, 에너지, 실패 후 복구를 함께 측정한다. 같은 모델도 양자화 방식과 런타임에 따라 품질과 속도가 크게 달라진다.

# 주의할 점

목록은 게시 시점의 스냅샷이다. 다운로드 수, 인기와 “현재 최고”라는 표현은 빠르게 낡는다. 각 모델의 공식 카드에서 라이선스, 컨텍스트 길이, 지원 언어, 학습 제한과 상업 이용 조건을 다시 확인해야 한다. 작은 파라미터 수만으로 실제 메모리나 응답 품질을 예측하지 않는다.

# 출처

- [KDnuggets 원문](https://www.kdnuggets.com/best-small-language-models-on-hugging-face-right-now)
- [Notion 원본 항목](https://app.notion.com/p/3681a73cf20b8124a38adc4758236ae1)

