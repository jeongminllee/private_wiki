---
type: Reference
title: "SmallCode: 소형 로컬 모델용 코딩 에이전트"
description: "7B~20B 로컬 언어 모델의 도구 호출과 긴 작업 한계를 하네스 설계로 보완하는 코딩 에이전트"
resource: https://discuss.pytorch.kr/t/smallcode-7b-20b-llm/10281
notion: https://app.notion.com/p/3681a73cf20b8103b19cdf519eb7c987
tags: [reading, coding-agent, local-ai, small-language-model]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

SmallCode는 LM Studio, Ollama나 OpenAI 호환 로컬 서버의 7B~20B 모델을 코딩 에이전트로 쓰기 위한 하네스다. 작은 모델이 긴 계획과 정확한 도구 형식에서 흔들리는 문제를 모델 크기만 키우지 않고 작업 분해, 파서, 메모리와 루프 제어로 보완한다.

# 설계 아이디어

- 컨텍스트 예산을 관리하고 현재 작업에 필요한 파일만 넣는다.
- JSON, YAML, XML, Hermes와 일반 텍스트 등 여러 도구 호출 형식을 허용한다.
- 큰 요청을 TODO 목록으로 나누고 작은 패치부터 적용한다.
- 필요한 도구만 두 단계로 노출해 선택 부담을 줄인다.
- 작업 메모리와 반복 행동 감지로 진행 정지와 무한 루프를 찾는다.
- 모델별 프롬프트와 도구 능력을 profile로 분리한다.

BoneScript라는 실행 계층은 여러 백엔드 작업을 한 번의 구조화된 동작으로 묶어 도구 호출 횟수를 줄이려 한다. 제한된 모델에서는 하네스가 외부 작업 기억과 절차적 구조를 대신 제공한다는 관점이 핵심이다.

# 적용 관점

민감한 저장소를 외부 모델에 보내기 어렵거나, 반복 비용을 낮추고 싶은 개인 환경에서 시험할 만하다. 작은 버그 수정과 테스트 추가처럼 완료 조건이 분명한 작업부터 성공률, 사람 수정량, 토큰과 시간을 측정한다.

# 주의할 점

여러 형식을 관대하게 해석하는 파서는 잘못된 모델 출력을 의도한 명령처럼 실행할 위험이 있다. 쓰기·실행 권한을 격리하고 패치 검토와 테스트를 강제해야 한다. 선택 설정에 따라 클라우드 모델로 escalation할 수 있으므로 완전 로컬이 필요한 경우 경로를 명시적으로 차단한다.

# 출처

- [저장된 PyTorchKR 소개](https://discuss.pytorch.kr/t/smallcode-7b-20b-llm/10281)
- [Notion 원본 항목](https://app.notion.com/p/3681a73cf20b8103b19cdf519eb7c987)

