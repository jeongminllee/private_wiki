---
type: Reference
title: "GLM-4.7-Flash GGUF 로컬 실행"
description: "30B-A3B MoE 모델의 GGUF 양자화와 llama.cpp·Ollama 기반 로컬 배포 포인트"
resource: https://huggingface.co/unsloth/GLM-4.7-Flash-GGUF
notion: https://app.notion.com/p/ed21a73cf20b83f689c90194b88d3b5b
tags: [reading, local-llm, gguf, glm, inference]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Unsloth가 배포한 GLM-4.7-Flash의 GGUF 양자화 저장소다. 원 모델은 전체 30B, 토큰당 약 3B가 활성화되는 MoE 구조로 소개되며, 비교적 가벼운 로컬 배포에서 추론·코딩·도구 사용 성능을 노린다.

# 실행 선택지

`llama.cpp`에서는 저장소와 양자화 이름을 지정해 서버나 CLI를 실행할 수 있다.

```bash
llama-server -hf unsloth/GLM-4.7-Flash-GGUF:UD-Q4_K_XL
llama-cli -hf unsloth/GLM-4.7-Flash-GGUF:UD-Q4_K_XL
```

Ollama도 Hugging Face의 GGUF를 직접 가리키는 방식을 안내한다.

```bash
ollama run hf.co/unsloth/GLM-4.7-Flash-GGUF:UD-Q4_K_XL
```

# 운영 포인트

- 저장소는 과거 `llama.cpp` 버그로 반복 출력과 품질 저하가 있었으며 수정된 파일을 다시 받으라고 안내한다.
- 일반 대화와 도구 호출은 권장 샘플링 값이 다르다.
- GGUF 양자화는 메모리를 줄이지만 품질과 속도는 양자화 종류, 컨텍스트 길이, 하드웨어에 따라 달라진다.
- 모델 카드의 자체 벤치마크는 실제 한국어 업무 데이터로 다시 검증해야 한다.

# 관련 문서

- [로컬 RAG 구축](125-building-a-local-rag.md)
- [Transformer Lab](14-transformerlab.md)

# 출처

- [Unsloth GLM-4.7-Flash-GGUF 모델 카드](https://huggingface.co/unsloth/GLM-4.7-Flash-GGUF)

