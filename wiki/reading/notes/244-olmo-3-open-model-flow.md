---
type: Reference
title: "Olmo 3: 가중치를 넘어 학습 전 과정을 공개하는 오픈 모델"
description: "Ai2가 공개한 Olmo 3 모델군, Dolma 3 데이터와 단계별 checkpoint가 재현성에 주는 의미"
resource: https://news.hada.io/topic?id=24530&utm_source=discord&utm_medium=bot&utm_campaign=2358
notion: https://app.notion.com/p/3001a73cf20b8372900f81cd23f041c2
tags: [reading, open-model, llm, reproducibility]
timestamp: 2026-07-24
status: summarized
---

# 핵심

Ai2의 Olmo 3는 최종 weight만 배포하는 데서 그치지 않고 dataset, training recipe, code와 중간 checkpoint까지 공개하는 “model flow”를 지향한다. 결과물을 사용할 수 있는 open-weight model보다 학습 과정의 추적·검증·수정 가능성을 넓히려는 프로젝트다.

# 공개 범위

- 7B와 32B 규모의 Base·Think model, 7B Instruct와 RL Zero 계열
- 약 9.3조 token 규모의 Dolma 3 corpus와 Dolci post-training data
- pretraining 단계, supervised fine-tuning, DPO와 RLVR의 중간 checkpoint
- 65K context 지원과 학습·평가 toolchain
- 학습 자료와 model response의 관련 흔적을 탐색하는 OlmoTrace

이런 구성은 연구자가 특정 학습 단계의 효과를 비교하거나, 공개 recipe에서 data·optimizer·post-training 부분만 바꿔 실험하는 데 유용하다.

# 해석할 때 주의할 점

소개 글의 benchmark 수치는 model size, prompt와 evaluation harness가 같은 조건인지 확인해야 한다. OlmoTrace가 보여주는 것은 training data와 output 사이의 matching·influence 단서이지, 어떤 문장이 특정 답을 직접 일으켰다는 완전한 causal attribution은 아니다.

투명성이 높아지면 corpus의 품질 문제와 유해·민감 내용도 함께 드러날 수 있다. 공개 data를 그대로 재학습하기보다 license, 개인정보, contamination과 filtering policy를 별도로 검토해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=24530&utm_source=discord&utm_medium=bot&utm_campaign=2358)

