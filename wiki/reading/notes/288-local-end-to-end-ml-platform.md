---
type: Reference
title: "로컬에서 만드는 end-to-end ML platform: model 파일에서 운영 안전망까지"
description: "fraud detection 예제로 experiment, registry, feature, validation, drift, serving과 CI/CD를 연결하는 실습"
resource: https://www.freecodecamp.org/news/build-end-to-end-ml-platform-locally-from-experiment-tracking-to-cicd/
notion: https://app.notion.com/p/b961a73cf20b82d58c5381e68b3ad2df
tags: [reading, mlops, mlflow, cicd]
timestamp: 2026-07-24
status: summarized
---

# 출발점

글은 credit-card fraud binary classifier를 `pickle`로 저장하고 FastAPI에서 읽는 최소 구현부터 시작한다. 이 방식은 빠르지만 어떤 data·parameter로 만든 model인지 재현하기 어렵고, version·rollback, training-serving feature 일치, 입력 검증, drift 감지와 배포 전 test가 없다.

# 구성요소별 역할

각 도구는 다른 failure mode를 맡는다.

- MLflow는 parameter, metric과 artifact를 기록하고 model version에 `champion` alias를 붙여 rollback 가능하게 한다.
- Feast는 training과 online serving이 같은 feature 정의를 쓰게 해 training-serving skew를 줄인다.
- Great Expectations는 amount, hour, schema 같은 data 조건을 prediction 전에 검사한다.
- Evidently는 입력 분포 변화와 성능 저하를 report로 감시한다.
- FastAPI는 registry의 champion model을 읽어 prediction API를 제공한다.
- Docker는 실행 환경을 고정하고 GitHub Actions는 data·model threshold test와 build를 자동화한다.

전체 흐름은 data validation, feature 계산, training·tracking, registry promotion, serving, drift monitoring, retraining과 CI/CD gate를 순서대로 잇는다. 장애 대응 절에서는 false-positive 급증, 점진적 성능 하락과 upstream schema 변경을 구분해 조사하도록 한다.

# 실습과 운영의 차이

“로컬에서 production-grade component를 경험한다”는 의미이지 이 구성을 그대로 production에 배포하면 완성된다는 뜻은 아니다. 예시는 local SQLite와 file store를 쓰고 Kubernetes 없이 한 machine에서 동작한다. 실제 운영에는 authentication, secret 관리, persistent storage, backup, alert delivery, high availability, feature freshness, data lineage와 배포 전략이 더 필요하다.

도구를 모두 설치하는 것이 목적이 아니라 재현·일관성·입력 품질·환경 변화·배포 위험 중 현재 팀의 가장 큰 실패 지점을 먼저 막는 것이 핵심이다. 작은 project라면 MLflow와 test부터 시작하고, feature reuse나 drift 문제가 실제로 생길 때 나머지를 추가하는 편이 운영 부담을 줄인다.

# 출처

- [freeCodeCamp 실습 글](https://www.freecodecamp.org/news/build-end-to-end-ml-platform-locally-from-experiment-tracking-to-cicd/)
- [예제 저장소](https://github.com/sandeepmb/freecodecamp-local-ml-platform)

