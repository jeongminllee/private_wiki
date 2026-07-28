---
type: Paper Note
title: "Solar Open 100B 기술 보고서"
description: "한국어 데이터 부족을 합성 데이터, 점진적 커리큘럼, 분리형 강화학습으로 다룬 이중언어 MoE 모델"
resource: https://huggingface.co/upstage/Solar-Open-100B/blob/main/solar-open-technical-report.pdf
notion: https://app.notion.com/p/a111a73cf20b82f0a403012f8eabf6d5
tags: [paper, solar-open, korean-llm, moe, reinforcement-learning]
timestamp: 2026-07-24
status: summarized
---

# One-line Summary

Solar Open은 한국어처럼 공개 데이터가 부족한 언어에서 경쟁력 있는 개방형 모델을 만들기 위해 합성 데이터, 언어별 토크나이저, 학습 커리큘럼, 확장 가능한 RL을 하나의 방법론으로 묶은 102.6B MoE 모델이다.

# Problem

영어와 중국어 이외의 언어는 대규모 고품질 데이터와 전면적 벤치마크가 부족하다. 보고서는 한국어가 색인된 웹 콘텐츠에서 차지하는 비율을 약 0.8%로 보고, 단순 수집만으로는 양과 품질을 모두 확보하기 어렵다고 진단한다.

# Method

- 총 19.7T 규모의 사전학습 말뭉치와 4.5T 합성 토큰을 구성했다.
- 낮은 품질의 넓은 데이터에서 높은 품질의 전문 데이터로 이동하는 점진적 커리큘럼을 사용했다.
- 한국어를 과표집한 196,608 어휘의 BPE 토크나이저를 설계했다.
- 데이터 생성, 보상 계산, 학습을 분리하고 중간 결과를 캐시하는 SnapPO 강화학습 프레임워크를 제안했다.

# Architecture

| 항목 | 값 |
| --- | ---: |
| 전체 파라미터 | 102.6B |
| 토큰당 활성 파라미터 | 12B |
| 컨텍스트 길이 | 131,072 |
| 레이어 | 48 |
| 전체 전문가 | 129 |
| 라우팅 전문가 | 128 |
| 토큰당 선택 전문가 | 8 |

# Key Findings

보고서의 평가에서는 한국어 일반 지식, 선호도, 의료·법률·금융과 영어 지식·수학 과제에서 비교 모델과 경쟁력 있는 성능을 제시한다. 특히 한국어 토큰 압축 효율은 전역 모델보다 유리하다고 보고한다.

# My Understanding

핵심은 “한국어 데이터를 더 모았다”가 아니라 데이터 부족 문제를 학습 전 단계의 시스템 설계로 다룬 점이다. 합성 데이터의 비율을 높이면서도 품질 임계값과 도메인 분포를 단계별로 조절했고, 한국어 추론 비용에 직접 영향을 주는 토크나이저까지 함께 최적화했다.

# Open Questions

- 합성 데이터가 장기적으로 만드는 편향과 오류 누적은 어떻게 감시하는가
- 자체 보고 벤치마크가 실제 한국어 업무와 얼마나 일치하는가
- 12B 활성 파라미터 모델의 현실적인 서빙 비용과 처리량은 어느 정도인가
- Upstage Solar 라이선스가 구체적인 상업 사용 시나리오에 어떤 제약을 주는가

# Citations

- [Solar Open Technical Report](https://huggingface.co/upstage/Solar-Open-100B/blob/main/solar-open-technical-report.pdf)
- [Solar Open 100B 모델 카드](https://huggingface.co/upstage/Solar-Open-100B)

