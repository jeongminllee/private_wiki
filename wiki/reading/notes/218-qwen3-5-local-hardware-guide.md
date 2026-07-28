---
type: Reference
title: "Qwen 3.5 로컬 실행: 모델 크기·양자화·하드웨어 선택"
description: "소비자 GPU와 Apple Silicon에서 Qwen 3.5 계열을 실행할 때 필요한 memory와 성능 trade-off"
resource: https://wikidocs.net/blog/@jaehong/8843/
notion: https://app.notion.com/p/98a1a73cf20b8297909a8141e7845385
tags: [reading, local-llm, qwen, quantization]
timestamp: 2026-07-24
status: summarized
---

# 모델 선택 지도

글은 Qwen 3.5의 MoE 계열 35B-A3B·122B-A10B·397B-A17B와 dense 27B, small 0.8B·2B·4B·9B를 구분한다. `A3B`는 전체 35B weight 중 token마다 약 3B가 활성화된다는 뜻으로 계산량은 줄지만 전체 weight를 저장할 memory는 여전히 필요하다.

# 글이 제시한 memory 기준

- 9B 4-bit: 약 6.5GB
- 27B 4-bit: 약 17GB
- 35B-A3B 4-bit: 약 22GB
- 397B-A17B: 3-bit 약 192GB, 4-bit 약 256GB

이는 weight 중심의 대략치다. 실제로는 context 길이에 따른 KV cache, multimodal projector, runtime overhead와 GPU·system RAM 간 offloading도 포함해야 한다.

# 성능 trade-off

작은 9B는 16GB GPU에서 빠르게 실행할 수 있고, 35B-A3B는 더 높은 품질을 노리지만 긴 context에서 이전 세대보다 느릴 수 있다. Unsloth Dynamic quantization은 중요한 layer를 높은 bit로 보존해 크기와 품질을 절충한다. thinking mode는 정확도를 높일 수 있지만 속도와 token을 더 쓴다.

# 실제 적용 시 주의

글 작성 시점에는 분리된 vision file 때문에 Ollama 호환성이 부족해 최신 llama.cpp 계열 backend가 필요하다고 설명한다. model·runtime 지원은 빠르게 변하므로 현재 공식 compatibility를 다시 확인해야 한다. 환각이 중요한 coding 작업은 local model로 초안을 만들고 stronger hosted model이나 test suite로 검증하는 혼합 workflow가 현실적이다.

# 출처

- [Qwen 3.5를 내 컴퓨터에서 돌리기](https://wikidocs.net/blog/@jaehong/8843/)

