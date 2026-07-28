---
type: Reference
title: "AI 대학원 면접 학습 카드 앱"
description: "통계·확률·선형대수 등 기본 개념 135개와 면접 질문 98개를 학습 상태와 함께 관리하는 공개 web app"
resource: "https://ai-learning-study-card.vercel.app/"
notion: "https://app.notion.com/p/24d1a73cf20b832abe1401655d6e556f"
tags: [reading, ai, interview, study-app, machine-learning]
timestamp: 2026-07-24
status: summarized
---

# 앱 구성

AI 대학원 면접 준비를 위한 browser 기반 학습 앱이다. 첫 화면 기준으로 기본 개념 135개와 면접 질문 98개를 제공하며, 내용은 6개 학습 분야로 나뉜다. 기본 개념 영역은 통계, 확률, 선형대수 등 이론을 복습하고, 질문 영역은 실제 면접에서 설명하는 연습에 초점을 둔다.

학습 항목은 다섯 단계의 상태로 추적할 수 있다. 별도 account나 server 동기화보다 browser storage를 활용하는 구조로 보이므로, 다른 기기·browser로 이동하거나 site data를 지우면 진척이 유지되는지 먼저 확인해야 한다.

# 활용 방법

카드를 읽는 데서 끝내지 말고 질문을 본 뒤 소리 내어 답하고, 정의·직관·수식·예시·한계를 한 세트로 설명한다. 틀린 항목은 상태만 바꾸지 말고 왜 막혔는지 짧게 적고 관련 교재나 구현으로 되돌아간다. 면접 답변은 암기된 문장보다 가정과 trade-off를 설명할 수 있어야 한다.

# 제한

개인 제작 학습 도구의 정답과 범위가 대학원별 interview syllabus를 보장하지 않는다. 수식, 최신 model 정보와 논쟁적인 설명은 ISL 같은 교재, 강의 note와 원 논문으로 교차 검증해야 한다. 현재 공개 첫 화면과 두 학습 mode는 확인했지만 source repository와 content 검수 이력은 site에서 식별하지 못했다.

# 관련 문서

- [An Introduction to Statistical Learning](362-introduction-to-statistical-learning.md)

# 출처

- [AI 면접 학습 앱](https://ai-learning-study-card.vercel.app/)
