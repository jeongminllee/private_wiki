---
type: Reference
title: "베테랑 개발자의 바이브 코딩 경험 2: 역할과 태도"
description: "AI 코딩의 생산성·인지 부채·심리와 개발자 역할 변화를 2주 실험에서 돌아본 글"
resource: https://yozm.wishket.com/magazine/detail/3473/
notion: https://app.notion.com/p/aa11a73cf20b8261bd3d813cdbff94ff
tags: [reading, vibe-coding, software-engineering, career]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

40년 경력의 개발자가 AI assistant만으로 약 5천 줄 규모의 Python 프로젝트를 만든 경험의 후반부다. 반복적이고 잘 알려진 문제에서는 큰 속도 향상을 얻지만, 생성량이 많아질수록 숨어 있는 bug와 기술 부채를 사람이 모두 검토하기 어려워진다고 본다.

# 개발자의 역할

AI는 prototype, 아이디어 탐색, architecture 실험과 migration에서 시니어의 선택지를 넓힐 수 있다. 동시에 결과를 맹신하면 언어와 구조를 직접 배우는 과정이 사라진다. 핵심은 AI 코드를 단순히 신뢰하는 빠른 방식과, 코드를 읽고 이해하며 배우는 느린 방식 사이의 긴장을 의식적으로 관리하는 것이다.

# 자연어는 코드가 될 수 있는가

자연어는 강력한 고수준 interface지만 본질적으로 맥락 의존적이고 모호하다. 형식 문법, type system, operational semantics, reference implementation과 test suite가 하는 일을 모두 대체하기 어렵다. 대화는 의도를 탐색하고 명세를 만들 수 있지만, 최종 동작은 executable test와 검증된 코드로 고정해야 한다.

# 실험의 한계

단일 개발자, 익숙한 언어, command-line 기반 소규모 프로젝트였고 Git, 병렬 agent, team workflow와 복잡한 full stack은 거의 다루지 않았다. 모델과 editor가 비공개로 계속 바뀌고 출력도 확률적이므로 생산성 수치를 일반화할 수 없다.

# 관련 문서

- [1편: 기술적 협업과 검증](117-veteran-vibe-coding-part-1.md)

# 출처

- [요즘IT 번역 2편](https://yozm.wishket.com/magazine/detail/3473/)
- [Notion 원본 항목](https://app.notion.com/p/aa11a73cf20b8261bd3d813cdbff94ff)
