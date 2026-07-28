---
type: Reference
title: Transformer Lab
description: 로컬 실험부터 GPU 클러스터 학습·평가까지 연결하는 오픈소스 AI 연구 환경
resource: https://github.com/transformerlab/transformerlab-app
notion: https://app.notion.com/p/39b1a73cf20b81418cdfeb2a7e8feee9
tags: [reading, repository, ml-platform, llm]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Transformer Lab은 모델 다운로드, 채팅, 파인튜닝, 평가와 배포 실험을 한 인터페이스에서 수행하는 오픈소스 연구 환경이다. 개인용 로컬 실행과 팀용 클러스터 오케스트레이션을 모두 겨냥한다.

# 핵심 내용

- 로컬에서는 macOS, Linux, Windows WSL2에서 개인 데이터와 모델 실험을 관리한다.
- MLX, vLLM, Ollama, Hugging Face 계열 실행 환경과 CUDA, ROCm, MLX 하드웨어를 폭넓게 지원한다.
- full fine-tuning, LoRA, QLoRA, RLHF, 하이퍼파라미터 탐색과 모델 형식 변환을 제공한다.
- 평가에는 LLM judge, 레드팀과 플러그인 기반 확장을 포함한다.
- 팀 환경에서는 Slurm과 SkyPilot을 이용한 클라우드·클러스터 작업, 실험 추적, 모델 레지스트리, 체크포인트 복구를 다룬다.

# 왜 읽을 만한가

노트북과 개별 스크립트로 흩어진 연구 작업을 어느 수준까지 플랫폼화할 수 있는지 살펴볼 수 있다. 로컬 실험이 커졌을 때 클러스터 실행과 결과 추적을 이어 가는 구조가 특히 유용하다.

# 적용 아이디어

- 작은 모델 하나로 로컬 학습, 평가, 결과 내보내기까지 짧은 검증을 수행한다.
- 현재 LLaMA-Factory 기반 흐름과 데이터 추적, 재현성, 체크포인트 복구 경험을 비교한다.
- 팀 기능을 검토할 때 Slurm 연동과 기존 스토리지·레지스트리 구조의 충돌 여부를 먼저 본다.

# 주의할 점

AGPL-3.0 라이선스가 배포 방식에 미치는 영향을 검토해야 한다. 빠른 설치 명령은 실행 전에 스크립트를 읽고, 지원 기능이 각 백엔드에서 동일한지 작은 실험으로 확인하는 편이 좋다.

# 출처

- [GitHub 저장소](https://github.com/transformerlab/transformerlab-app)
- [Notion 원본 항목](https://app.notion.com/p/39b1a73cf20b81418cdfeb2a7e8feee9)
