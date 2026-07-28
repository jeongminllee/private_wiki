---
type: Reference
title: "InkOS: 장편소설의 상태를 분리해 관리하는 10-agent 집필 pipeline"
description: "창작·사실 추출·연속성 감사·수정을 역할별 agent와 구조화된 상태 파일로 나누는 TypeScript CLI"
resource: https://discuss.pytorch.kr/t/inkos-10-ai-cli/9450
notion: https://app.notion.com/p/8401a73cf20b8325b672011ebae9e03b
tags: [reading, ai-agents, creative-writing, multi-agent]
timestamp: 2026-07-24
status: summarized
---

# 핵심 설계

InkOS는 장편소설 전체를 하나의 거대한 prompt에 넣는 대신 작업을 10개 역할로 나눈 TypeScript CLI다. Radar가 시장 경향을 보고, Planner와 Composer가 장별 의도와 필요한 맥락을 준비하며, Architect와 Writer가 구조와 본문을 만든다. Observer와 Reflector는 새 사실을 구조화된 상태로 반영하고, Normalizer·Auditor·Reviser가 분량 조정, 33개 항목의 연속성 검사와 수정을 맡는다.

장기 기억은 캐릭터 행렬, 자원 원장, 미회수 복선과 감정선 등을 담은 7개 truth file로 관리한다. Zod schema로 JSON 구조를 검증하고 Node.js 22 이상에서는 SQLite 기반 temporal database와 의미 검색을 이용한다. 따라서 매 chapter에 전체 원고를 다시 보내기보다 현재 장면에 필요한 사실만 골라 넣는다.

# 실제 workflow

`inkos write next`가 compose, draft, audit, revise, human review 순서를 실행한다. OpenAI, Anthropic과 OpenAI-compatible API를 지원하고 Writer에는 고성능 모델, Auditor에는 저렴한 모델을 배정하는 식으로 역할별 routing이 가능하다. 사람의 승인 gate가 있으므로 완전 자동 출판보다는 반복 가능한 편집 pipeline에 가깝다.

소개 글은 개발자가 중국어 소설 31장, 452,191단어를 생성해 33차원 continuity audit를 100% 통과했다고 전한다. 이는 프로젝트 자체 검증이며 문학적 완성도, 사실 정확성이나 독자 평가를 독립적으로 입증한 결과는 아니다. 같은 agent가 만든 기준으로 같은 결과를 검사하면 오류가 공유될 수도 있으므로 중요한 설정과 복선은 사람이 별도로 대조해야 한다.

# 활용 판단

가장 재사용할 만한 아이디어는 “agent 수”보다 서술 상태를 typed data로 외부화하고, 생성과 감사를 분리하며, 각 단계 사이에 사람이 승인한다는 구조다. API 비용은 역할 수와 재시도 횟수에 따라 빠르게 커질 수 있으므로 짧은 장으로 모델 조합별 비용·수정률·사람이 발견한 불일치를 먼저 측정한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/inkos-10-ai-cli/9450)
- [InkOS 저장소](https://github.com/Narcooo/inkos)

