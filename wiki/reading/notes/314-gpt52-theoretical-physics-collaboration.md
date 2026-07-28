---
type: Paper Note
title: "GPT-5.2와 이론물리학: single-minus gluon 진폭 공식을 찾고 검증한 협업"
description: "특수 운동량 영역에서 0이 아닌 글루온 tree amplitude의 패턴을 모델이 일반화하고 연구진이 분석적으로 검증한 사례"
resource: "https://news.hada.io/topic?id=26684"
notion: "https://app.notion.com/p/12f1a73cf20b8272945001348489ec8e"
tags: [reading, physics, ai-for-science, research]
timestamp: 2026-07-24
status: summarized
---

# 발견한 내용

연구의 제목은 “Single-minus gluon tree amplitudes are nonzero”다. 하나의 음의 helicity gluon과 나머지 양의 helicity gluon으로 이뤄진 tree-level amplitude는 일반적인 운동량에서 0으로 알려져 있었지만, 연구진은 half-collinear라는 특수한 운동량 공간에서 0이 아닌 값을 갖는 공식을 제시했다.

인간 연구진이 작은 입자 수의 복잡한 Feynman diagram 식을 제공하자 GPT-5.2 Pro가 이를 단순한 형태로 바꾸고 일반화 패턴을 찾았다. 이후 scaffolded 내부 모델이 약 12시간 추론해 같은 공식을 독립적으로 도출하고 형식적 증명을 만들었다. 연구진은 Berends-Giele recursion과 soft theorem으로 일관성을 점검했다.

# 이 사례가 보여 주는 것

LLM은 전문가가 정의한 문제와 계산 결과 사이에서 식을 단순화하고 후보 일반식을 탐색하는 데 유용할 수 있다. 사람이 일일이 조작하기 어려운 symbolic expression에서 패턴 후보를 빨리 만들고, 다시 분석적 증명과 물리적 consistency check로 걸러내는 협업 구조다. 후속으로 graviton amplitude 확장도 연구 중이라고 한다.

# 과장하지 말아야 할 부분

모델이 아무 문제 설정 없이 독자적으로 물리학을 발명한 사례는 아니다. 문제, 작은 사례와 검증 기준은 세계적 수준의 연구진이 제공했다. 유사 결과의 선행 연구 가능성도 토론에서 제기됐다. 현재 preprint 단계이므로 학술지 심사, 독립 검산과 선행문헌 비교가 남아 있다.

따라서 핵심은 “AI가 과학자를 대체했다”가 아니라, 장시간 추론 모델이 전문가의 계산·패턴 탐색을 확대하고 검증 가능한 conjecture를 만드는 도구가 됐다는 점이다.

# 출처

- [GeekNews 정리와 OpenAI 원문 링크](https://news.hada.io/topic?id=26684)
