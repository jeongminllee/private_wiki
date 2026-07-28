---
type: Reference
title: "Unsloth Studio: 로컬 모델 실행·학습 웹 UI"
description: "데이터 준비, LoRA·강화학습, 비교 평가와 GGUF 내보내기를 한 화면에 묶는 오픈소스 도구"
resource: https://news.hada.io/topic?id=27606
notion: https://app.notion.com/p/f071a73cf20b82d282b3814919377080
tags: [reading, llm, fine-tuning, local-ai]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Unsloth Studio는 텍스트·비전·오디오·임베딩 모델의 로컬 실행, 데이터 준비, 학습, 결과 비교, 내보내기를 웹 UI로 묶는다. `llama.cpp`와 Hugging Face 생태계를 사용하고 복잡한 파인튜닝 설정의 진입 장벽을 낮추려 한다.

# 주요 기능

- GGUF와 safetensors 모델을 불러와 로컬 채팅과 추론을 실행한다.
- PDF, CSV, JSONL을 학습 데이터셋으로 변환하고 정제·확장하는 Data Recipes를 제공한다.
- LoRA, 4bit·16bit·FP8 학습, full fine-tuning, GRPO를 지원한다.
- 훈련 손실과 GPU 사용률을 추적하고 기본 모델과 학습 모델의 출력을 나란히 비교한다.
- 결과를 safetensors 또는 GGUF로 내보내 vLLM, Ollama, LM Studio 등에 연결한다.

# 성능 주장과 현재 제약

프로젝트는 최대 2배 빠른 학습과 70% 적은 VRAM 등 여러 최적화 수치를 제시한다. 모델, GPU, batch, context 길이에 따라 달라지므로 자신의 데이터로 재측정해야 한다. 공개 초기 사용자들은 macOS 설치와 UI 오류를 보고했고, 당시 GPU 학습은 NVIDIA 중심이며 MLX·AMD·Intel 지원은 준비 중이었다.

# 라이선스

핵심 Unsloth 패키지는 Apache 2.0이고 Studio UI 등 일부 선택 구성요소는 AGPL-3.0이다. 사내 배포 전 사용하는 구성요소별 라이선스를 확인해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27606)
- [Unsloth Studio](https://unsloth.ai/docs/new/studio)

