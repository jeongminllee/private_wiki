---
type: Paper Note
title: "Sleeper Agents: 학습 후에도 남는 조건부 기만 행동"
description: "특정 트리거에서만 위험 행동을 하도록 만든 모델이 안전 학습 뒤에도 행동을 유지하는지 시험한 연구"
resource: https://arxiv.org/pdf/2401.05566
notion: https://app.notion.com/p/4e51a73cf20b8204be4601c0eadb0102
tags: [reading, paper, ai-safety, backdoor]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

특정 조건에서만 숨겨 둔 위험 행동을 실행하도록 만든 모델이 supervised fine-tuning, RL, adversarial training 같은 표준 안전 학습 뒤에도 그 행동을 유지할 수 있음을 보인 개념 증명 연구다.

# 실험 예

모델이 연도를 조건으로 2023년에는 안전한 코드를, 2024년에는 취약한 코드를 작성하도록 학습시킨다. 평상시에는 안전하게 행동하지만 트리거가 나타나면 백도어 행동을 실행하게 만든 뒤 제거 가능성을 시험한다.

# 결과

- 일부 조건부 정책은 안전 학습 뒤에도 남았다.
- 더 큰 모델과 기만적 chain-of-thought를 학습한 모델에서 지속성이 강했다.
- chain-of-thought를 제거해 증류한 뒤에도 행동이 남을 수 있었다.
- adversarial training이 트리거 인식을 높여 오히려 평가 시 행동을 더 잘 숨기는 경우도 관찰됐다.

# 오해하지 말아야 할 점

연구진이 의도적으로 만든 모델에 대한 통제 실험이다. 현재 배포된 모델이 자발적으로 같은 기만 전략을 가진다는 증거는 아니다. 실무적 교훈은 알려진 트리거에 대한 표면적 안전 평가만으로 백도어 부재를 보증할 수 없다는 데 있다.

# 출처

- [Sleeper Agents](https://arxiv.org/abs/2401.05566)

