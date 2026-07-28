---
type: Reference
title: "Cohere North Mini Code"
description: "30B 전체·3B 활성 MoE 구조로 로컬 및 에이전틱 코딩을 겨냥한 Cohere의 공개 가중치 모델"
resource: https://cohere.com/blog/north-mini-code
notion: https://app.notion.com/p/3811a73cf20b815f9c15c5f4a13bc519
tags: [reading, coding-model, mixture-of-experts, local-ai]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

North Mini Code는 Cohere의 첫 에이전틱 코딩 모델이다. Mixture of Experts 구조로 전체 파라미터는 30B지만 토큰마다 약 3B가 활성화된다. 저장소 수준 코드 변경, 터미널 도구 사용, 코드 생성에 맞춰 학습했으며 공개 가중치와 Apache 2.0 라이선스를 제공한다.

# 주요 사양

- 모델 ID: `north-mini-code-1-0`
- 전체/활성 파라미터: 30B / 3B
- 입력 컨텍스트: 256K
- 최대 출력: 64K
- 제공 형식: Hugging Face의 BF16, FP8, W4A16 가중치
- 사용 경로: Cohere Chat V2 API, Model Vault, OpenRouter, 로컬·온프레미스 배포
- 목표 작업: repo 수준 에이전틱 소프트웨어 엔지니어링, 터미널 작업, 과학 코드와 알고리즘 생성

특정 에이전트 하네스 하나에만 맞추지 않고 여러 하네스에서 학습했다고 설명한다. OpenCode에 최적화했지만 SWE-Agent 등 다른 실행 구조에서도 사용할 수 있다는 주장이다.

# 성능 주장의 해석

Cohere는 유사 크기 공개 모델과의 코딩·터미널 벤치마크에서 경쟁력 있는 결과와 Artificial Analysis Coding Index 33.4를 제시한다. 내부 비교에서는 동일 하드웨어·동시성 조건에서 Devstral Small 2보다 최대 2.8배 높은 출력 처리량과 약 30% 나은 inter-token latency를 보고한다. 일부 경쟁 모델 점수와 누락된 벤치마크는 Cohere가 직접 측정했으므로 독립 재현 결과와 구분해야 한다.

# 실제 도입 관점

3B 활성 파라미터는 계산 효율을 뜻하지만 전체 30B 가중치를 메모리에 올려야 하는 MoE 특성을 고려해야 한다. 공식 표의 최소 하드웨어는 FP8 또는 FP4에서 H100 1장으로 제시되어 있어 일반 소비자 GPU에서 “가볍게” 실행된다는 뜻은 아니다. 양자화별 VRAM, context 길이에 따른 KV cache, tool-call 형식, 한국어 코드 설명 품질을 실제 환경에서 측정해야 한다.

평가할 때는 작은 사내 저장소 복제본에서 버그 수정, 테스트 작성, 다중 파일 리팩터링, 터미널 복구 작업을 고정 세트로 만들고 성공률·토큰·지연·사람 수정량을 함께 기록하는 것이 좋다.

# 주의할 점

제품 발표의 처리량과 성능 수치는 공급자 측 측정이다. 256K 컨텍스트와 64K 출력 한도를 항상 유효하게 쓰는 것은 아니며 긴 컨텍스트에서는 속도와 메모리 비용이 커진다. 공개 가중치 라이선스와 별개로 학습 데이터, 생성 코드의 라이선스, 배포 보안은 사용자가 검토해야 한다.

# 출처

- [Cohere 발표 글](https://cohere.com/blog/north-mini-code)
- [공식 모델 문서](https://docs.cohere.com/docs/north-mini-code-1.0)
- [릴리스 노트](https://docs.cohere.com/changelog/north-mini-code-1-0)

