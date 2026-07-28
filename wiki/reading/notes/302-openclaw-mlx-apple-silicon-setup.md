---
type: Reference
title: "OpenClaw MLX Setup: Apple Silicon에서 로컬 모델을 자동 구성하는 방법"
description: "Mac 메모리에 맞는 MLX 모델 선택부터 OpenAI 호환 서버와 OpenClaw 설정까지 자동화한 설치 스크립트"
resource: "https://github.com/jkf87/openclaw-mlx-setup"
notion: "https://app.notion.com/p/8401a73cf20b827ab418012ac4a7aa82"
tags: [reading, local-llm, mlx, openclaw]
timestamp: 2026-07-24
status: summarized
---

# 핵심 흐름

Apple Silicon Mac에서 OpenClaw가 로컬 LLM을 사용하도록 구성하는 자동 설치 프로젝트다. 스크립트가 시스템 메모리를 확인하고, `mlx-lm`을 설치하고, Hugging Face에서 적절한 MLX 모델을 받은 뒤 `mlx_lm.server`를 포트 8080의 OpenAI 호환 API로 실행한다. 이어서 OpenClaw 루트 설정인 `openclaw.json`을 수정하고 연결까지 시험한다.

README의 기본 선택은 8GB에서 Qwen3 4B 4-bit, 16GB에서 8B, 32GB에서 14B, 64GB 이상에서 32B다. 모델 크기는 각각 대략 2.5GB, 4.9GB, 8.5GB, 19GB로 제시된다. 구조는 `Hugging Face MLX 모델 → mlx_lm.server → OpenClaw → Telegram 또는 에이전트`로 단순하다.

# 실무에서 볼 지점

서버가 한 번에 한 요청을 처리하는 단일 스레드 구조라 동시 사용량이 늘면 병목이 된다. 기본 컨텍스트는 8,192이며 Qwen3의 내부 사고 태그가 응답에 노출되지 않도록 `enable_thinking: false`를 둔다. 빠른 개인용 설치에는 편하지만, 병렬 요청·자동 재시작·모니터링·접근 제어가 필요한 서비스 환경은 별도 구성이 필요하다.

요구사항은 M1~M4, 최소 8GB 메모리, Python 3.10 이상과 OpenClaw다. README의 속도 수치는 프로젝트 측 측정이며 Mac 세대, 메모리 대역폭, 양자화와 프롬프트 길이에 따라 달라진다.

# 안전하게 적용하기

스크립트는 모델을 다운로드하고 Python 패키지를 설치하며 사용자 설정 파일을 바꾼다. 실행 전에 다운로드 출처, 변경되는 `openclaw.json`, 바인딩 주소와 인증 여부를 읽어야 한다. 로컬 네트워크 밖으로 포트를 열지 말고 설정을 먼저 백업하는 것이 좋다. 라이선스는 MIT다.

# 출처

- [openclaw-mlx-setup 저장소](https://github.com/jkf87/openclaw-mlx-setup)
