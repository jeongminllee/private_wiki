---
type: Reference
title: "Agentic Data Scientist: 계획·코딩·검토를 분리한 데이터과학 멀티에이전트"
description: "Google ADK와 Claude Agent SDK로 분석 계획, 실행, 기준 검사와 반성을 반복하는 적응형 데이터과학 프레임워크"
resource: "https://github.com/K-Dense-AI/agentic-data-scientist"
notion: "https://app.notion.com/p/d7a1a73cf20b825c9d9e01724a451623"
tags: [reading, data-science, multi-agent, google-adk]
timestamp: 2026-07-24
status: summarized
---

# 작업 구조

데이터 분석을 한 에이전트의 긴 대화로 처리하지 않고 계획과 실행을 분리한 오픈소스 프레임워크다. Google ADK가 전체 흐름을 오케스트레이션하고 Claude Agent SDK가 코드 작성과 실행을 맡는다. plan maker, reviewer, parser, coding agent, review agent, criteria checker, stage reflector와 summary agent가 각 단계의 결과를 점검한다.

`orchestrated` 모드는 여러 검토와 반성 단계를 사용하고, `simple` 모드는 비용과 복잡도를 줄인다. 출력 파일은 기본적으로 `./agentic_output`에 남기며 임시 저장 옵션도 있다. Context7 MCP와 과학 작업용 Claude Skills를 연결할 수 있다.

# 운영 조건

Claude Code 설치와 함께 계획·검토용 OpenRouter API key, 코딩 에이전트용 Anthropic API key가 필요하다. 네트워크 접근은 기본 활성화되어 있으며 `DISABLE_NETWORK_ACCESS=true`로 fetch와 search를 끌 수 있다. 민감한 원자료를 클라우드 모델에 보내는지, 생성 코드가 외부 endpoint에 접근하는지 실행 전에 확인해야 한다.

# 연구 품질과의 차이

여러 에이전트가 서로 검토한다고 해서 통계적 타당성이 독립적으로 검증되는 것은 아니다. 같은 모델 계열과 prompt가 공통 편향을 반복할 수 있다. 실제 연구에서는 사전에 고정한 train/test 분할, 데이터·코드 provenance, 가정과 제외 기준, seed와 환경 잠금, 외부 사람의 검토가 여전히 필요하다.

이 도구는 분석 loop와 산출물 관리를 자동화하는 데 유용하지만 결론의 권위를 자동 생성하지 않는다. 특히 p-hacking, leakage, multiple testing과 인과 해석은 별도 검증 체크리스트로 다뤄야 한다. 라이선스는 MIT다.

# 출처

- [Agentic Data Scientist 저장소](https://github.com/K-Dense-AI/agentic-data-scientist)
