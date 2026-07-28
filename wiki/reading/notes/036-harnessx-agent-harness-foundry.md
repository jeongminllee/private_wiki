---
type: Paper Note
title: "HarnessX: 조합하고 진화시키는 에이전트 하네스"
description: "도구·메모리·제어 흐름을 typed primitive로 표현하고 실행 트레이스로 하네스와 모델을 함께 개선하는 연구"
resource: https://discuss.pytorch.kr/t/harnessx-feat-xiaomi/10740
notion: https://app.notion.com/p/3851a73cf20b81ffb403e8fd3009d9cb
tags: [paper, ai-agent, harness, reinforcement-learning]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

HarnessX는 에이전트의 시스템 프롬프트, 도구, 메모리, 제어 흐름을 조합 가능한 typed primitive로 만들고, 실행 트레이스에서 실패 원인을 읽어 하네스와 모델 정책을 함께 개선하려는 프레임워크다.

# 문제

같은 언어모델도 어떤 도구를 주고, 메모리를 어떻게 불러오며, 언제 재시도하고, 결과를 어떻게 검증하는지에 따라 성능이 크게 달라진다. 그러나 하네스는 사람이 경험적으로 고정하는 경우가 많고, 모델을 학습한 뒤 하네스를 따로 조정하면 두 요소가 서로 맞지 않을 수 있다.

# 방법

HarnessX는 하네스 요소를 타입이 있는 기본 단위와 치환 가능한 구성으로 표현한다. AEGIS라는 다중 에이전트 진화 엔진이 실행 트레이스를 읽고 다음 역할을 수행한다.

- `Digester`가 실행 기록과 실패를 압축한다.
- `Planner`가 어떤 하네스 요소를 바꿀지 계획한다.
- `Evolver`가 프롬프트, 도구 사용, 메모리, 제어 흐름의 후보를 만든다.
- `Critic`이 변경의 타당성과 결과를 평가한다.

하네스 변화와 GRPO 기반 모델 업데이트가 shared replay를 통해 같은 경험을 사용하도록 해, 외부 실행 구조와 내부 정책을 함께 적응시키려 한다.

# 결과와 의미

논문은 ALFWorld, GAIA, WebShop, tau3, SWE-bench Verified에서 평균 14.5%, 최대 44%의 향상을 보고한다. 중요한 주장은 특정 프롬프트 하나가 아니라, 실행 트레이스로부터 하네스 구성 자체를 최적화할 수 있다는 것이다. 하네스를 코드와 설정으로 명시하면 비교, 롤백, 재사용도 쉬워진다.

# 적용 아이디어

현재 wiki 작업에서는 수집기, 중복 판정, 원문 추출기, 요약 템플릿, 링크 검사기를 하네스의 구성 요소로 볼 수 있다. 배치별 실패를 기록한 뒤 어떤 추출기와 검증 순서가 효과적이었는지 비교할 수 있다. 단 자동으로 전체 파이프라인을 바꾸기 전에 고정된 샘플 세트에서 기존 버전과 새 버전을 비교해야 한다.

# 주의할 점

논문 결과는 저자들이 선택한 벤치마크와 평가 환경의 결과다. 소개 글 확인 시점에는 코드 공개가 향후 계획으로 언급되어 재현 가능성을 별도 확인해야 한다. 하네스와 모델을 동시에 바꾸면 어느 변경이 효과를 냈는지 식별하기 어려우므로 ablation과 버전별 평가가 중요하다.

# 관련 문서

- [AI Agent Harness와 Loop Engineering](20-agent-harness-loop-engineering.md)
- [2026년 6월 15~21일 논문 흐름](028-ai-ml-papers-2026-06-15-21.md)

# 출처

- [PyTorchKR 소개 글](https://discuss.pytorch.kr/t/harnessx-feat-xiaomi/10740)
- [arXiv 논문](https://arxiv.org/abs/2606.14249)

