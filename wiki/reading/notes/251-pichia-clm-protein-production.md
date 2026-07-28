---
type: Paper Note
title: "Pichia-CLM: 단백질 의약품 생산을 위한 종 특이적 codon 최적화"
description: "효모 발현량을 높이도록 DNA 서열을 설계하는 MIT 연구의 방법, 실험 결과와 한계"
resource: https://news.mit.edu/2026/new-ai-model-could-cut-costs-developing-protein-drugs-0216
notion: https://app.notion.com/p/b3b1a73cf20b832b83e581cab3dc30ba
tags: [paper, protein, language-model, biotechnology]
timestamp: 2026-07-24
status: summarized
---

# 한 줄 요약

Pichia-CLM은 같은 단백질을 만드는 여러 synonymous DNA 서열 중 산업용 효모 *Komagataella phaffii*가 더 잘 발현할 후보를 설계해, 단순한 빈도 기반 codon 최적화보다 높은 생산량을 보인 연구다.

# 문제

하나의 amino acid는 여러 codon으로 표현될 수 있다. 단백질 서열이 같아도 host organism에 맞춘 DNA 선택에 따라 발현량이 달라진다. 기존 도구는 자주 쓰이는 codon을 골라 바꾸는 경우가 많지만, local pattern과 멀리 떨어진 위치 사이의 관계까지 충분히 반영하기 어렵다.

# 방법

연구팀은 NCBI에서 얻은 약 5,000개의 *K. phaffii* natural protein에 대응하는 amino-acid·DNA pair로 encoder-decoder model을 학습했다. model은 목표 protein sequence를 받아 여러 DNA 후보를 만들며, 반복 서열 회피와 amino-acid property 같은 종 특이적 pattern을 학습한다.

# 실험

Human growth hormone, serum albumin과 trastuzumab을 포함한 여섯 protein을 실제 효모에서 생산했다. 네 가지 상용 codon-optimization tool과 비교했을 때 Pichia-CLM 설계가 다섯 protein에서 가장 높은 생산량, 나머지 하나에서 두 번째 결과를 보였다고 MIT News는 설명한다.

# 해석과 한계

실험은 단순 benchmark를 넘어 wet-lab validation을 했다는 점이 강하다. 다만 “개발 비용을 줄일 수 있다”는 표현은 가능성에 대한 추론이며, 연구가 전체 의약품 개발 비용 절감률을 직접 측정한 것은 아니다. model은 특정 효모에 맞춰졌으므로 다른 host에는 별도 종 특이적 data와 검증이 필요하다.

# 출처

- [MIT News](https://news.mit.edu/2026/new-ai-model-could-cut-costs-developing-protein-drugs-0216)

