---
type: Decision Note
title: AegisLM EMBER2024 ELF Classifier 절대평가
description: train 26,000건·test 6,000건의 자체 temporal LightGBM과 공식 공개 모델이 낮은 FPR의 시간 안정성 gate에 실패한 결정
tags: [aegislm, phase-f, ember2024, malware, lightgbm, evaluation]
timestamp: 2026-07-31
status: active
---

# Summary

EMBER2024 ELF static feature를 안전하게 materialize해 독립 classifier로
평가했지만 자체 temporal LightGBM과 공식 공개 모델 모두 사전 등록한
절대 gate를 통과하지 못했다. NuriLab static-signal 연결과 Qwen SFT
혼합은 보류한다.

# 확정한 데이터

- train: raw 52,000행 → `(week_id, sha256)` 26,000관측치
- test: raw 12,000행 → 6,000관측치
- fit: weeks 0–43, 22,000건
- calibration: weeks 44–51, 4,000건
- test: weeks 52–63, 6,000건
- raw executable 다운로드·실행: 0
- model-visible label·file hash 누출: 0

# 절대평가 결과

| 모델 | Precision | Recall | FPR | ROC AUC | 주별 최대 FPR | 판정 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 자체 temporal LightGBM | 0.9793 | 0.9293 | 0.0197 | 0.9854 | 0.056 | FAIL |
| 공식 EMBER2024 ELF 모델 | 0.9002 | 0.9897 | 0.1097 | 0.9929 | 0.208 | FAIL |

자체 모델은 test label을 사용한 진단용 oracle에서도 FPR 1%에서 recall이
87.53%라 aggregate gate를 넘지 못했다. 공식 모델은 oracle aggregate에서
recall 91.4%였지만 주별 최대 FPR 4.8%로 주별 gate에 실패했다. test
oracle threshold는 배포나 승인에 사용할 수 없다.

# 해석

- AUC가 높아도 낮은 FPR과 시간 안정성을 충족했다는 뜻은 아니다.
- 자체 모델은 calibration만 조정해서 해결할 수 없다.
- 공식 모델은 ranking 여지는 있지만 배포 가능한 calibration과 주별
  안정성이 입증되지 않았다.
- EMBER2024 static feature를 NuriLab의 결정론적 신호로 채택할 근거가
  아직 없다.

# 다음 결정

1. FP가 집중된 weeks 56·57·59·61의 label-blind feature drift를 감사한다.
2. FP/FN의 feature 분포와 시간 변화를 분리한다.
3. drift 근거가 확인된 경우에만 최근 week를 fit에 포함하고 독립
   calibration을 유지한 temporal remediation을 한 번 실행한다.
4. 재실행도 같은 gate에 실패하면 EMBER2024 ELF classifier 경로를
   `research_hold`로 종료한다.

# Related Concepts

- [EMBER2024 benchmark 공급 결정](aegislm_ember2024_benchmark_decision_20260731.md)
- [Phase F 연구 계획](aegislm_phase_f_experiment_plan_20260728.md)
- [프로젝트 정본 결정문](../repos/AegisLM-B200/docs/experiments/decisions/phase-f/PHASE_F_EMBER2024_CLASSIFIER_BASELINE_DECISION_20260731.md)
- [LLM 생명주기 환경 설계](../../../infra/llm-lifecycle-environment-design.md)

# Citations

- [EMBER2024 repository](https://github.com/FutureComputing4AI/EMBER2024)
- [EMBER2024 dataset](https://huggingface.co/datasets/joyce8/EMBER2024)
- [EMBER2024 paper](https://arxiv.org/abs/2506.05074)
