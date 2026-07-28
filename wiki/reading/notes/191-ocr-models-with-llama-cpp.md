---
type: Command Note
title: "llama.cpp로 소형 OCR 모델을 로컬 실행하기"
description: "4GB급 GPU나 CPU에서 GGUF OCR 모델을 CLI와 OpenAI 호환 서버로 실행하는 방법"
resource: https://huggingface.co/blog/ggml-org/using-ocr-models-with-llama-cpp
notion: https://app.notion.com/p/c5d1a73cf20b8219a00e81b8a6c6df92
tags: [reading, ocr, llama-cpp, local-ai]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`llama.cpp`는 LightOnOCR, Qianfan-OCR, GLM-OCR, DeepSeek-OCR, Dots.OCR, HunyuanOCR 같은 소형 OCR 모델을 GGUF로 실행할 수 있다. 일부 모델은 4GB VRAM GPU나 CPU에서도 동작하므로 문서를 외부 API에 보내지 않는 로컬 OCR 파이프라인을 만들 수 있다.

# 빠른 실행

테스트용 CLI:

```bash
llama-cli -hf ggml-org/GLM-OCR-GGUF -p "OCR" --image invoice.png
```

애플리케이션 연동에는 서버가 편하다.

```bash
llama-server -hf ggml-org/GLM-OCR-GGUF
```

기본 `http://localhost:8080/v1/chat/completions`에 이미지 URL 또는 base64 data URL과 프롬프트를 보내면 된다.

# 모델 선택과 프롬프트

- `OCR`, `OCR markdown`, `OCR HTML table`처럼 모델 카드가 권장하는 형식을 사용한다.
- 기본 Q8_0은 품질과 속도의 균형점이고 F16은 메모리를 더 쓰지만 품질이 나아질 수 있다.
- 일반 VLM을 쓸 때는 “설명 없이 Markdown OCR 결과만 출력”처럼 형식을 명확히 지정한다.
- 언어, 표, 수식, 손글씨별로 작은 검증 세트를 만들어 character error rate와 구조 보존률을 비교한다.

# 환각 대응

OCR 모델도 이미지에 없는 글자를 생성할 수 있다. 온도를 `0.1`로 낮추거나 `top-k 1`을 사용하고, 입력 해상도와 기울기를 보정하며, F16이나 다른 모델과 비교한다. 금액·날짜·정답처럼 중요한 값은 원본 이미지 좌표와 함께 사람이 대조해야 한다.

# 출처

- [Using OCR models with llama.cpp](https://huggingface.co/blog/ggml-org/using-ocr-models-with-llama-cpp)

