---
type: Reference
title: IBM AssetOpsBench
description: 산업 설비 운영과 유지보수용 AI 에이전트를 구축하고 평가하는 공개 프레임워크
resource: https://github.com/IBM/AssetOpsBench
notion: https://app.notion.com/p/39b1a73cf20b81ccb908f3d2a7248ac0
tags: [reading, repository, ai-agent, benchmark, industry]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

AssetOpsBench는 제조·설비 운영에서 쓰는 도메인 에이전트를 만들고 오케스트레이션하며 평가하는 통합 프레임워크다. 단순 질의응답보다 센서 조회, 고장 분석, 시계열 예측과 작업 지시서 생성처럼 실제 유지보수 흐름을 MCP 도구로 구성한다.

# 핵심 내용

- 현재 README 기준 9개 자산 유형과 141개 이상의 시나리오를 제공한다.
- IoT, 고장 모드·센서 관계, 시계열 기반 모델, 작업 지시, 진동 분석용 MCP 서버를 둔다.
- 전문 에이전트가 각 도메인 도구를 맡고 상위 오케스트레이터가 작업을 분배한다.
- Plan-Execute, Deep Agent, Claude Agent, OpenAI Agent 등 여러 에이전트 방식을 비교할 수 있다.
- 평가는 답변뿐 아니라 도구 선택, 절차, 도메인 적합성 등을 여러 차원에서 보고 LLM judge도 사용한다.

# 왜 읽을 만한가

일반적인 웹 검색 에이전트와 달리 전문 도구 스키마와 실제 업무 절차가 성능을 어떻게 좌우하는지 볼 수 있다. 도메인 에이전트 벤치마크를 설계할 때 시나리오와 도구 호출을 함께 평가하는 좋은 참고점이다.

# 적용 아이디어

- 보안 분석 에이전트에도 센서 대신 로그·샘플·탐지 규칙·티켓 도구를 분리한 MCP 구조를 적용해 본다.
- 최종 답변 점수와 별도로 올바른 도구, 인자, 순서, 실패 복구를 평가한다.
- LLM judge 결과 일부를 사람이 재평가해 판정 일치도를 측정한다.

# 주의할 점

Notion에 저장된 제목은 460개 이상의 시나리오라고 적혀 있지만 현재 README는 141개 이상으로 표시한다. 저장소가 빠르게 바뀌고 리더보드도 진행 중이므로 실험 시 커밋을 고정해야 한다.

# 출처

- [GitHub 저장소](https://github.com/IBM/AssetOpsBench)
- [Notion 원본 항목](https://app.notion.com/p/39b1a73cf20b81ccb908f3d2a7248ac0)
