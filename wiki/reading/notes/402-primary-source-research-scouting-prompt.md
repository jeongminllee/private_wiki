---
type: Command Note
title: "1차 출처 기반 최신 연구 탐색 프롬프트"
description: "최근 논문 3~5개를 원문, 코드, benchmark와 재현 가능성 기준으로 선별하고 과장 없이 비교하기 위한 조사 명령문"
notion: "https://app.notion.com/p/1d81a73cf20b83d9960f01c9bd2f0e5f"
tags: [reading, prompt, research, literature-review, fact-check]
timestamp: 2026-07-24
status: summarized
---

# 용도

관심 분야의 최신 논문을 빠르게 훑되 2차 요약의 과장을 줄이기 위한 프롬프트다. 원본 메모의 `Recency`, `Impact`, `Reproducibility` 기준은 유지하면서, 같은 실험 조건이 아닌 benchmark 수치를 억지로 비교하지 않도록 검증 절차를 보강했다.

# 개선한 프롬프트

```text
역할
당신은 기술 문헌을 검증하는 senior research engineer다. 기관이나 직함을
연기하는 문장보다, 아래 출처 우선순위와 검증 규칙을 엄격히 따른다.

조사 주제: {관심 주제}
검색 기준일: {YYYY-MM-DD}
기간: 최근 {1개월/3개월/1년}
적용 환경: {하드웨어, 데이터, 언어, 제품 제약}

출처 우선순위
1. 논문 원문과 version history
2. 저자의 project page, 공식 code와 model card
3. conference review와 저자 답변
4. 독립 재현·비판 자료
보도 기사와 SNS는 후보 발견에만 사용하고 핵심 근거로 삼지 않는다.

선정 기준
- 기간 안에 최초 공개되거나 실질적으로 개정된 논문
- 명확한 문제 정의와 기존 방법 대비 기술적 delta가 있는 연구
- baseline, dataset, metric, compute budget이 공개된 연구
- 가능하면 code, weight, demo, license가 확인되는 연구
- 화제성만 있고 원문이나 검증 가능한 결과가 없는 항목은 제외

3~5개를 선정하고 각 논문을 다음 형식으로 작성하라.

### [영문 논문 제목]
- Source: arXiv/OpenReview/DOI | official code | project page
- Version: 최초 공개일, 확인한 version과 확인일
- One-liner: 해결한 문제와 접근법을 한 문장으로
- Key delta: architecture, objective, data, training 또는 inference의 변화
- Evidence: 주요 수치와 정확한 dataset·metric·baseline·evaluation setting
- Efficiency: parameter, FLOPs, latency, throughput, memory, 학습 자원 중 공개된 값
- Reproducibility: code/weight/data/license, 설치·평가 가능 여부
- Practicality: High/Medium/Low, 적용 조건과 예상 병목
- Limitations: 저자가 밝힌 한계, 빠진 ablation, 비교의 공정성, 독립 재현 여부
- Confidence: 확인된 사실과 아직 저자 주장에 머문 내용을 구분

마지막에 다음을 추가하라.
- 논문 간 직접 비교가 가능한 항목과 불가능한 항목
- 지금 재현할 1순위와 최소 실험 계획
- 찾지 못했거나 접근할 수 없었던 1차 출처
- 모든 수치 옆의 근거 링크

정보가 없으면 추측하지 말고 "미공개" 또는 "확인 필요"라고 쓴다.
```

# 사용할 때 주의할 점

- “SOTA”는 동일한 dataset, split, metric, model scale와 tool budget에서 비교됐는지 확인해야 한다.
- 최근 업데이트는 새 연구가 아니라 typo 수정일 수 있으므로 version diff를 본다.
- GitHub 주소가 있다는 사실과 재현 가능하다는 평가는 다르다. commit, dependency, checkpoint, license와 issue를 확인한다.
- 논문 저자의 benchmark는 독립 검증이 아니다. 보고된 결과와 재현된 결과를 분리한다.
- 실무 적용성은 모델 성능만이 아니라 data 권리, serving 비용, latency, 유지보수와 실패 허용 범위로 판단한다.

# 출처

- [Notion 원본 프롬프트](https://app.notion.com/p/1d81a73cf20b83d9960f01c9bd2f0e5f)

