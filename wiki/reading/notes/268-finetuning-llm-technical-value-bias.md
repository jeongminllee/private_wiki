---
type: Reference
title: "QLoRA로 LLM의 기술 비교를 시장성 중심에서 작동 원리 중심으로 보정하기"
description: "삼성 기술 블로그의 특허 비교 편향 탐지, 학습 데이터 재작성과 token·attention 분석"
resource: https://techblog.samsung.com/blog/article/75
notion: https://app.notion.com/p/9741a73cf20b825f8fcb0141b13d3513
tags: [reading, qlora, llm-evaluation, bias]
timestamp: 2026-07-24
status: summarized
---

# 발견한 문제

저자 팀은 특허 기술을 기능적 목적(FP), 기술적 고유성(TU), 전략적 가치(SV) 세 축으로 비교하게 했다. 수천 건을 분석하자 최종 판단 이유의 약 78%가 기술 구조보다 시장성·비용 같은 SV 표현에 기대는 경향이 나타났고, prompt를 바꾸는 것만으로 크게 줄지 않았다.

# 보정 과정

1. 세 축의 승자 판단이 일관되면서 최종 설명만 SV에 치우친 사례를 선별
2. LLM으로 FP·TU 중심 설명을 다시 만들고 전문가가 기술 용어와 구조를 검토
3. 입력에는 각 축의 승자·이유를, 출력에는 기술 중심 overall reason을 넣어 학습 data 구성
4. 4-bit base model과 LoRA adapter를 쓰는 QLoRA로 parameter-efficient fine-tuning

# 보고된 변화

Fine-tuning 뒤 FP·TU를 근거로 최종 이유를 쓰는 비율이 40% 이상 증가했다. Token 생성 확률은 FP `+0.0282`, TU `+0.0328`, SV `-0.0423`으로 변했고, attention 분석에서도 FP·TU 관련 token의 평균 attention이 오르고 SV는 소폭 줄었다고 보고한다.

# 해석할 때 주의할 점

출력 어휘와 attention 변화는 목표한 표현 방식이 학습됐다는 증거지만, 기술 판단 자체가 더 정확해졌다는 완전한 증명은 아니다. Attention weight를 곧바로 내부 reasoning의 원인으로 해석하기도 어렵다. Holdout domain의 expert blind review, winner accuracy, calibration과 business value를 부당하게 무시하는 새 편향까지 평가해야 한다.

가장 재사용할 만한 원칙은 model을 바로 fine-tune하기 전에 실제 업무 output을 taxonomy로 분해하고, 어떤 편향을 어떤 metric으로 바꿀지 먼저 정의했다는 점이다.

# 출처

- [Samsung Tech Blog](https://techblog.samsung.com/blog/article/75)

