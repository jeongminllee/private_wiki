---
type: Reference
title: "AI 시대 개발자에게 필요한 비프로그래밍 역량"
description: "문제 정의, 읽기·쓰기·듣기·말하기, 질문과 문서화가 coding보다 상위의 개발 역량이라는 PyCon Korea 발표 정리"
resource: "https://yozm.wishket.com/magazine/detail/3479/"
notion: "https://app.notion.com/p/8301a73cf20b838eb8c401d81c3f9f30"
tags: [reading, career, problem-definition, communication, python]
timestamp: 2026-07-24
status: summarized
---

# 개발의 출발점

LLM은 주어진 문제의 풀이와 code 생성을 도울 수 있지만, 무엇을 왜 해결해야 하는지는 조직의 맥락에서 사람이 정의해야 한다. 작성자는 RAG 성능 평가를 예로 든다. 단순히 “성능을 평가한다”가 아니라 hallucination 유형, retrieval 정확도, citation 정확도, 실패 사례를 어떻게 출력해 model 개선으로 연결할지까지 정해야 구현 가능한 문제가 된다.

# 언어와 문서화 역량

좋은 문제 정의에는 기획서, architecture, API spec, policy, RFP를 읽는 능력이 필요하다. 연차가 높아질수록 team, 다른 직군과 고객의 말을 듣고, 질문하고, 결정 사항을 정확히 쓰고 말하는 일이 커진다. 정의되지 않은 빈칸을 임의로 채우지 않고 적절한 사람에게 정확한 질문을 던지는 것도 개발 역량이다.

작성자는 context를 충분히 담은 flowchart를 먼저 만들고, 이를 task와 architecture로 구체화하는 방식을 제안한다. Jira ticket의 As-is에는 문제 정의를, To-be에는 문제 풀이를 넣으면 담당자와 reviewer가 같은 기준으로 결과를 판단할 수 있다. 문서는 완료 후 보관물이 아니라 구현 전후에 계속 갱신하는 coordination 도구다.

# 남는 결론

AI가 code 작성 비중을 높여도 개발자는 결과의 목적, 제약과 품질을 책임져야 한다. 특정 programming language 숙련을 버리라는 뜻이 아니라, code가 해결책이 되도록 만드는 문제 정의와 communication의 가치가 더 커진다는 주장이다.

# 출처

- [요즘IT 원문](https://yozm.wishket.com/magazine/detail/3479/)
- [PyCon Korea 2025 발표 프로그램](https://2025.pycon.kr/)
