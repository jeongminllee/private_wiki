---
type: Reference
title: "Data Science with RAPIDS LAB Season 2: GPU 데이터 과학 학습 모임"
description: "모두의연구소와 NVIDIA의 RAPIDS 기반 데이터 처리·분석 LAB 페이지를 읽기 위한 기록"
resource: https://modulabs.co.kr/labs/641
notion: https://app.notion.com/p/efa1a73cf20b8325ac9281b88a31602e
tags: [reading, rapids, gpu, data-science]
timestamp: 2026-07-24
status: summarized
---

# 무엇인가

저장된 페이지는 모두의연구소의 “NVIDIA - Data Science with RAPIDS LAB Season2” 프로그램이다. NVIDIA RAPIDS 생태계를 이용해 GPU 기반 데이터 처리와 data-science workflow를 함께 학습하는 LAB 형태의 모임으로 분류된다.

# RAPIDS를 배우는 이유

RAPIDS는 CUDA 기반 dataframe·machine-learning 도구를 제공해 pandas·scikit-learn 중심 workflow의 일부를 GPU로 가속한다. 핵심은 API 이름만 익히는 것이 아니라 다음을 판단하는 능력이다.

- dataset 크기와 연산이 GPU 전송 비용을 상쇄하는가
- CPU library와 결과·dtype·결측치 semantics가 같은가
- GPU memory에 data와 intermediate result가 들어가는가
- preprocessing부터 training까지 pipeline을 얼마나 GPU에 유지할 수 있는가

# 활용 방법

이 자료는 현재 모집 공고라기보다 저장 당시의 program archive로 보는 편이 안전하다. 참여 가능 여부, 일정, 비용, curriculum과 제공 GPU 환경은 페이지의 최신 상태를 다시 확인해야 한다. 독학 자료로 활용한다면 cuDF로 dataframe 처리, cuML로 기본 model 학습, CPU baseline과 end-to-end runtime 비교 순으로 작은 project를 만드는 것이 좋다.

# 확인 범위

2026-07-24 확인 당시 사이트 응답이 불안정해 세부 회차·운영진·일정을 안정적으로 추출하지 못했다. 따라서 program 제목과 RAPIDS 학습 주제 외의 모집 세부사항은 이 문서에 확정적으로 옮기지 않았다.

# 출처

- [모두의연구소 LAB](https://modulabs.co.kr/labs/641)

