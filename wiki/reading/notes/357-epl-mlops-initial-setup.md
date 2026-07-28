---
type: Project
title: "EPL 경기 예측 Full-stack MLOps project 초기 구성"
description: "축구 경기 결과 예측을 data ingestion부터 monitoring까지 확장하기 위한 modular repository와 logging 설계"
resource: "https://medium.com/data-ai-and-beyond/building-a-full-stack-mlops-system-predicting-the-2025-2026-english-premier-league-season-1960fb160e30"
notion: "https://app.notion.com/p/8971a73cf20b82c49bf98191744f9710"
tags: [reading, mlops, project-structure, sports-analytics]
timestamp: 2026-07-24
status: summarized
---

# 목표와 초기 범위

작성자는 과거 실패했던 축구 경기 예측 project를 production MLOps 관점에서 다시 만든다. Initial setup은 data, experiment, source component, model, deployment, pipeline, config, test와 log directory를 나누고 공통 logger·exception 처리를 마련한다.

# 전체 lifecycle

계획된 흐름은 `수집 → 정제·DB → EDA → feature engineering·store → training·evaluation → deployment → monitoring → 재학습`이다. 현재 public repository는 Football-Data source, Neon PostgreSQL, Feast, MLflow, XGBoost model 5개, FastAPI와 Streamlit까지 확장돼 있다.

# 평가 설계

Match result는 win/draw/loss multiclass, goal은 regression 또는 threshold classification으로 분리한다. Random split은 미래 정보 leakage를 만들 수 있으므로 time-series split과 season-based backtest를 사용한다. Accuracy뿐 아니라 class별 성능, Brier score와 calibration을 보고 bookmaker odds 같은 강한 baseline과 비교한다.

# 확인 범위

Medium 본문은 member-only였으나 공개 도입부와 연결된 repository에서 구조와 현재 상태를 확인했다. README의 목표 metric은 달성 결과가 아니며 betting 수익성을 보장하지 않는다.

# 출처

- [Initial setup article](https://medium.com/data-ai-and-beyond/building-a-full-stack-mlops-system-predicting-the-2025-2026-english-premier-league-season-1960fb160e30)
- [Soca-Scores 저장소](https://github.com/Jnyambok/Soca-Scores)
