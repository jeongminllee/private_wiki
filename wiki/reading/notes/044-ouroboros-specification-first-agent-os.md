---
type: Reference
title: "Ouroboros: 명세 우선 Agent OS"
description: "불변 명세, 실행 기록, 다단계 평가를 중심으로 여러 AI 에이전트 런타임을 묶는 오픈 소스 프로젝트"
resource: https://github.com/Q00/ouroboros/blob/main/README.ko.md
notion: https://app.notion.com/p/3791a73cf20b81c4a979ee8b2cb58310
tags: [reading, ai-agent, specification, orchestration]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Ouroboros는 에이전트에게 대략적인 목표를 던지고 결과만 기다리는 방식 대신, 실행 전에 명세를 확정하고 모든 단계를 재생·관찰·평가할 수 있게 만들려는 Agent OS 프로젝트다. 특정 모델이나 코딩 도구 하나보다 여러 에이전트 런타임을 MCP와 CLI로 연결하는 실행 계층에 가깝다.

# 핵심 흐름

1. 인터뷰를 통해 목표, 제약, 성공 조건을 구체화한다.
2. 이를 실행 중 임의로 바뀌지 않는 seed specification으로 만든다.
3. 명세를 작은 과제로 분해해 적합한 에이전트에 배정한다.
4. 결과를 기계적 검사, 의미 평가, 다중 모델 합의의 세 단계로 확인한다.
5. 실행 기록과 평가를 바탕으로 다음 버전의 시스템과 명세를 개선한다.

중심 가치는 specification-first, local-first, replayable, observable, policy-bound로 정리된다. 즉 에이전트의 자율성을 무제한으로 넓히기보다 행동의 경계와 완료 증거를 먼저 고정하려는 설계다.

# 적용 관점

오래 걸리는 코드 마이그레이션, 연구 파이프라인, 여러 모델을 쓰는 반복 작업처럼 결과 재현과 책임 추적이 필요한 곳에 맞는다. 현재 wiki의 대규모 읽기 자료 처리처럼 “원문을 추측하지 않는다”, “중복 URL은 합친다”, “실패 이유를 남긴다”를 명세와 평가 규칙으로 옮길 수도 있다.

# 주의할 점

저장소의 성능과 안정성 주장은 프로젝트 자체 설명이며 독립 검증과 구분해야 한다. 불변 명세는 실행 중 목표가 몰래 바뀌는 것을 막지만, 요구가 정당하게 변하는 작업에서는 변경 절차가 오히려 병목이 될 수 있다. 설치 스크립트, 에이전트 권한, 모델로 수행하는 의미 평가의 오판 가능성도 검토해야 한다.

# 출처

- [Ouroboros 한국어 README](https://github.com/Q00/ouroboros/blob/main/README.ko.md)
- [Ouroboros 저장소](https://github.com/Q00/ouroboros)
- [Notion 원본 항목](https://app.notion.com/p/3791a73cf20b81c4a979ee8b2cb58310)

