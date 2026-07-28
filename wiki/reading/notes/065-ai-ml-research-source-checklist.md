---
type: Reference
title: "AI/ML 자료 조사 출처 체크리스트"
description: "논문 원문, 커뮤니티 주목도, 구현체를 분리해 조사하도록 저장해 둔 개인 메모"
notion: https://app.notion.com/p/0b81a73cf20b83199b070155c8a357b4
tags: [reading, research, source-evaluation, personal-note]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

이 항목은 외부 링크가 아니라 AI/ML 자료를 조사할 때 사용할 출처 목록을 메모한 것이다. 하나의 검색 결과만 요약하지 않고 이론과 원문, 관심도와 토론, 코드와 재현 결과를 서로 다른 층으로 확인하자는 체크리스트로 정리할 수 있다.

# 세 층

## 1. 이론과 원문

- `arxiv.org`: `cs.CL`, `cs.LG`, `cs.AI` 등에서 논문 본문과 버전 이력을 확인한다.
- `openreview.net`: ICLR, NeurIPS, ICML 등의 제출본, 리뷰와 저자 답변을 확인한다.

논문 제목과 초록만 옮기지 말고 데이터, 비교군, 평가 절차, ablation, 한계와 코드 링크를 먼저 본다.

## 2. 주목도와 비판

- Hugging Face Papers: 최근 관심이 모인 논문을 찾는 탐색 창구
- Reddit의 `r/MachineLearning`, `r/LocalLLaMA`: 재현 경험, 하드웨어 조건과 비판을 찾는 보조 자료

인기와 정확성은 다르다. 커뮤니티 반응은 후보를 고르는 신호이지 논문의 결론을 검증하는 증거가 아니다.

## 3. 구현과 재현

- Papers with Code: 과제, 데이터셋, 지표와 공개 구현 연결
- GitHub 공식 저장소: commit, release, issue, 설치 재현성, 라이선스와 유지보수 상태 확인

# 권장 조사 순서

원문에서 주장을 적고, 공식 코드로 실행 가능성을 확인한 뒤, 독립 구현과 토론에서 실패 조건을 찾는다. 최종 노트에는 확인된 사실, 저자 주장, 커뮤니티 해석과 개인 판단을 구분한다.

# 출처

- [Notion 원본 메모](https://app.notion.com/p/0b81a73cf20b83199b070155c8a357b4)

