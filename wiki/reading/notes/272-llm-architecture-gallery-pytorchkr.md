---
type: Reference
title: "LLM Architecture Gallery 한국어 안내: model card의 구조 필드 읽기"
description: "GPT-2부터 2026 open-weight model까지 architecture diagram과 models.yml을 활용하는 법"
resource: https://discuss.pytorch.kr/t/llm-llm-architecture-gallery-sebastian-raschka-gpt-2-llm/9241
notion: https://app.notion.com/p/5171a73cf20b83ab9e4281fb7dce275a
tags: [reading, llm-architecture, visualization, open-weight]
timestamp: 2026-07-24
status: summarized
---

# 자료의 구성

PyTorchKR 글은 Sebastian Raschka의 LLM Architecture Gallery를 한국어로 따라 읽는다. 각 model에 parameter 수, release date, decoder type, attention, normalization, expert 구성, figure와 원 논문·config link가 붙는다.

Source data는 GitHub의 `models.yml`에서 관리되므로 web card의 숫자를 machine-readable metadata와 대조할 수 있다. Diagram은 Transformer block 안에서 normalization, residual, attention과 FFN·MoE가 어떤 순서로 놓이는지 비교하는 데 유용하다.

# 비교할 핵심 필드

- **Dense vs sparse MoE**: 모든 parameter를 쓰는지 일부 expert만 활성화하는지
- **MHA·GQA·MLA**: query·key·value 공유와 KV cache trade-off
- **Global·sliding·linear attention**: 긴 context 비용과 정보 전달 범위
- **Pre-norm·post-norm·QK-Norm**: 학습 안정성을 위한 normalization 위치
- **Active parameter**: 총 model size와 token당 compute를 분리해서 보기

DeepSeek V3/R1처럼 같은 base architecture에 reasoning training만 달라진 model도 있고, Qwen3.5·Nemotron 3처럼 attention과 state-space block을 섞은 hybrid도 있다.

# 한계

시각화가 복잡한 implementation을 이해하기 쉽게 만들지만 kernel, routing loss, tokenizer와 training recipe까지 담지는 못한다. 2026 model 정보는 빠르게 바뀌므로 `models.yml`, model card와 technical report의 revision을 함께 확인해야 한다.

# 관련 자료

- [GeekNews의 흐름 요약](271-llm-architecture-gallery-geeknews.md)
- [공식 gallery 정리](274-llm-architecture-gallery-official.md)
- [PyTorchKR 원문](https://discuss.pytorch.kr/t/llm-llm-architecture-gallery-sebastian-raschka-gpt-2-llm/9241)

