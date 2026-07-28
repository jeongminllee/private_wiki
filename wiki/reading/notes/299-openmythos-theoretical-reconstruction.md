---
type: Reference
title: "OpenMythos: Claude 내부 구조가 아닌 recurrent-depth 가설의 공개 구현"
description: "Prelude·반복 block·Coda, MLA/GQA와 sparse MoE를 결합한 독립적 theoretical reconstruction"
resource: https://github.com/kyegomez/OpenMythos
notion: https://app.notion.com/p/8da1a73cf20b82e1ac2981d46184008b
tags: [reading, llm-architecture, recurrent-depth, pytorch]
timestamp: 2026-07-24
status: summarized
---

# 정확한 정체

OpenMythos는 공개 연구와 추측을 바탕으로 만든 community project다. Anthropic과 관련이 없고 Claude의 proprietary architecture를 입수하거나 재현했다는 증거가 아니라는 disclaimer가 첫머리에 있다. 이름 때문에 내부 구조 유출이나 공식 replica로 오해해서는 안 된다.

# 구현된 가설

Model은 입력을 처리하는 `Prelude`, 같은 recurrent block을 최대 `max_loop_iters`만큼 반복하는 본체, 출력을 정리하는 `Coda`의 세 단계로 구성된다. Attention은 MLA와 GQA를 바꿔 쓸 수 있고 feed-forward는 routed expert와 shared expert를 함께 쓰는 sparse MoE다. 입력 난이도나 계산 budget에 따라 반복 깊이를 바꾸는 compute-adaptive reasoning을 실험하기 위한 구조다.

Python package로 설치해 작은 config를 만들고 forward·generation을 실행할 수 있으며, optional Flash Attention 2와 FineWeb-Edu용 training script도 제공한다. 1B부터 1T까지 preconfigured scale 이름이 있지만 config가 존재한다는 것과 그 크기의 pretrained checkpoint·검증 결과가 있다는 것은 다르다. 거대한 variant를 실용 model로 오해하면 안 된다.

# 연구용으로 볼 때

재사용할 부분은 Claude 추측이 아니라 recurrent-depth, sparse MoE, MLA/GQA 조합을 한 codebase에서 비교할 수 있다는 점이다. 동일 parameter 수에서 loop 수별 latency·memory·정확도와 gradient stability를 측정하고, fixed-depth baseline과 총 FLOPs를 맞춰야 architecture 자체의 효과를 볼 수 있다.

Repository의 수치와 stability check는 구현 검증의 출발점이지 frontier model의 training recipe나 성능을 입증하지 않는다. README 밖의 test coverage, 실제 공개 checkpoint, dataset license와 experiment log를 확인한 뒤 연구 결과로 인용한다.

# 출처

- [OpenMythos 저장소](https://github.com/kyegomez/OpenMythos)

