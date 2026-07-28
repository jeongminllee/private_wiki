---
type: Paper Note
title: "AI Co-Mathematician: 장기 수학 연구를 위한 agent workspace"
description: "문헌 탐색, 계산, 증명, 반례와 실패 가설을 stateful multi-agent workspace에서 관리하는 Google의 수학 연구 시스템"
resource: "https://arxiv.org/html/2605.06651v1"
notion: "https://app.notion.com/p/c281a73cf20b8274b5a601d26228f771"
tags: [reading, paper, mathematics, ai-agent, multi-agent]
timestamp: 2026-07-24
status: summarized
---

# 문제

수학 연구는 완성된 증명만 만드는 일이 아니다. 질문을 고치고, 문헌을 찾고, 작은 계산과 simulation으로 감을 잡고, 반례와 실패한 가설을 추적하는 장기적 탐색이다. 일반 chat은 state가 일시적이고 theorem prover는 좁은 작업에 특화되어 있어, 연구자가 도구 사이의 맥락을 수동으로 연결해야 한다.

# 시스템 설계

AI Co-Mathematician은 중앙 project coordinator와 병렬 workstream·specialist agent가 비동기로 일하는 workspace다. 사용자는 실행 중에도 방향을 바꾸거나 hard constraint를 추가할 수 있고, agent가 막히면 숨기지 않고 도움을 요청한다. High-level 전략과 low-level log를 progressive disclosure로 나누며, claim의 version, source, 논쟁 상태와 실패 경로를 보존한다.

결과는 chat 답변이 아니라 과정, citation, internal artifact와 margin note가 연결된 working paper다. Code는 test와 reviewer 승인 전에는 완료할 수 없고, report도 여러 reviewer가 승인해야 끝난다. 합의하지 못하면 unfinished 상태와 이유를 사용자에게 보여준다.

# 초기 결과와 benchmark

소수의 전문 수학자와 진행한 case study에서 open problem의 proof 초안, Stirling coefficient conjecture 수정, Hamiltonian system lemma와 문헌 탐색을 지원했다. 일부 proof는 아직 상세한 human review 중이며 개별 성공 사례는 통제 비교가 아니다.

Epoch AI가 blind 방식으로 평가한 FrontierMath Tier 4에서는 공개 sample 2개를 제외한 48문제 중 23개, 48%를 맞혔다. 기반 Gemini 3.1 Pro의 19%보다 높았지만 호출 수와 token에 제한이 없었고 자체 tool을 사용해 기존 harness보다 inference cost가 클 가능성이 있다.

# 중요한 한계

반복 review가 진실이 아니라 reviewer가 더는 오류를 찾지 못하는 잘못된 합의로 수렴할 수 있다. 반대로 agent 간 이견이 끝나지 않아 reasoning이 점점 hallucination으로 악화되기도 한다. 매끄러운 LaTeX가 엄밀성을 과대평가하게 만들고, 빠른 proof 생성이 느린 human peer review에 큰 부담을 줄 위험도 있다.

이 연구의 핵심은 autonomous mathematician보다, 실패와 uncertainty를 숨기지 않고 사람이 개입할 수 있는 연구 운영 환경에 있다. 최종 정당화와 학계의 이해는 여전히 전문 수학자의 검증을 필요로 한다.

# 출처

- [arXiv HTML v1](https://arxiv.org/html/2605.06651v1)
- [arXiv abstract](https://arxiv.org/abs/2605.06651)
