---
type: Reference
title: "Solar-GLM weight 분석 재검토: 높은 cosine similarity만으로 파생 관계를 말할 수 없다"
description: "LayerNorm 평균 방향이 cosine을 부풀리는 문제를 Pearson·known-derived pair·독립 model control로 검증한 분석"
resource: https://github.com/sionic-ai/solar-vs-glm
notion: https://app.notion.com/p/a261a73cf20b827b9e2281c9a67a114d
tags: [reading, llm, model-forensics, statistics]
timestamp: 2026-07-24
status: summarized
---

# 문제 제기

이 repository는 Solar와 GLM의 LayerNorm weight cosine similarity가 약 0.99라는 이유로 한 모델이 다른 모델에서 파생됐다는 기존 해석을 재검토한다. LayerNorm scale `γ`는 많은 차원이 양수이고 공통 평균 방향을 가질 수 있어, 세부 pattern이 달라도 raw cosine이 높아질 수 있다.

# 비교 방법

각 vector에서 평균을 뺀 뒤 Pearson correlation을 계산하면 Solar-GLM은 약 `r=0.01`로 떨어진다. 같은 index layer뿐 아니라 47×47 모든 layer pair를 비교해도 뚜렷한 diagonal이나 offset pattern이 나타나지 않았다.

방법이 실제 파생 관계를 잡을 수 있는지 확인하기 위해 GLM-4.5-Air에서 SFT한 것으로 알려진 INTELLECT-3를 positive control로 사용했다. 이 pair는 LayerNorm 값이 조금 변했어도 correlation이 거의 1을 유지했다. 같은 hidden dimension의 독립 model Phi와 비교한 값은 Solar-GLM처럼 거의 0이었다.

# 결론의 범위

분석이 지지하는 결론은 “LayerNorm cosine 0.99만으로 Solar가 GLM에서 파생됐다고 판단할 수 없다”는 것이다. 반대로 이 결과만으로 두 모델이 완전히 독립적으로 개발됐음을 증명한 것도 아니다. Repository도 HuRef의 parameter direction, REEF의 CKA representation similarity 같은 더 강한 fingerprinting을 추가로 적용해야 한다고 제안한다.

모델 계보는 기술 분석과 reputational claim이 만나는 민감한 문제다. 단일 metric을 출처 규명이나 복제 판정으로 확대하지 말고 tokenizer, architecture, 여러 weight family, activation representation, training record와 공개 설명을 함께 봐야 한다. 재현할 때는 정확한 checkpoint revision과 dtype conversion도 고정한다.

Solar Open 100B 자체의 구조와 성능 주장은 [기술 보고서 정리](150-solar-open-100b-technical-report.md)에서 따로 다룬다.

# 출처

- [Solar-GLM Derivation Analysis Revisited](https://github.com/sionic-ai/solar-vs-glm)

