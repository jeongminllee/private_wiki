---
type: Reference
title: "LLM 위키 완벽 가이드"
description: "원본 자료, 검증된 지식, 실제 산출물의 세 계층으로 개인 LLM 위키를 구축하고 운영하는 한국어 안내서"
resource: https://wikidocs.net/book/19830
notion: https://app.notion.com/p/3671a73cf20b81899848e89221a12d82
tags: [reading, knowledge-management, llm-wiki, wikidocs]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

박승규의 WikiDocs 책으로, 개발자뿐 아니라 일반 사용자가 자신의 자료를 LLM과 함께 축적·검증·재사용하는 과정을 설명한다. 도구 설치보다 “자료를 모아 답을 얻고, 확인된 답을 다시 지식으로 돌려보내는 운영 순환”에 초점을 둔다.

# 세 계층

1. **Source material**: 글, 영상, 메모, PDF처럼 변형하지 않은 원본 자료
2. **Organized knowledge**: 출처를 확인하고 개념별로 연결한 지식 문서
3. **Outputs**: 글, 보고서, 계획, 답변처럼 지식을 사용해 만든 결과물

원본과 해석을 분리하면 잘못된 요약을 다시 확인할 수 있고, 같은 자료에서 다른 목적의 문서를 만들 수 있다. 현재 저장소의 `raw/`, `wiki/`, 실제 작업 산출물 구분과 직접 연결되는 구조다.

# 책의 흐름

전체 여덟 장은 필요성, 세 계층, 방법과 도구 선택, 첫 위키 만들기, ingest, 질의와 검증, 업무 산출물 만들기, 유지보수와 감사 순서로 구성된다. 처음부터 거대한 분류 체계를 설계하기보다 작은 자료 묶음을 처리하고, 실제 질문에서 드러난 연결과 규칙을 다시 반영하게 한다.

# 현재 wiki에 적용

Notion 링크는 source 목록으로 보존하고, URL 중복을 정리한 뒤 각각을 재작성 요약으로 만든다. 접근 실패도 삭제하지 않고 이유와 복구 조건을 기록한다. 진행 현황, index와 log를 함께 유지하면 수백 개 자료를 중간에 멈췄다가도 이어갈 수 있다.

# 관련 문서

- [llm-wiki GitHub 스킬](033-llm-wiki-knowledge-graph-skill.md)
- [읽기 자료 전체 처리 현황](../progress.md)

# 출처

- [LLM 위키 완벽 가이드](https://wikidocs.net/book/19830)
- [Notion 원본 항목](https://app.notion.com/p/3671a73cf20b81899848e89221a12d82)

