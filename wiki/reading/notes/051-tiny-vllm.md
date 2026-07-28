---
type: Reference
title: "tiny-vllm: C++/CUDA로 배우는 LLM 추론 엔진"
description: "Llama 3.2 1B의 로딩부터 KV cache, continuous batching, PagedAttention까지 직접 구현하는 교육용 프로젝트"
resource: https://discuss.pytorch.kr/t/tiny-vllm-c-cuda-vllm-llm/10455
notion: https://app.notion.com/p/3721a73cf20b81cd8622f6e58ea04e42
tags: [reading, llm-inference, cuda, systems]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

tiny-vllm은 대형 추론 프레임워크의 코드를 바로 읽기 전에 LLM 서빙의 핵심 부품을 작은 C++/CUDA 구현으로 따라가게 하는 교육용 저장소다. Llama 3.2 1B을 대상으로 가중치 로딩, forward pass, 토큰 생성, KV cache와 배칭을 단계적으로 구현한다.

# 학습 순서

1. `safetensors` 가중치와 tokenizer 설정을 읽는다.
2. embedding, RMSNorm, RoPE, grouped-query attention, MLP를 연결한다.
3. logits와 sampling으로 한 토큰씩 생성한다.
4. 과거 key/value를 재계산하지 않도록 KV cache를 넣는다.
5. 여러 요청을 함께 처리하는 static/continuous batching으로 확장한다.
6. 메모리 단편화를 줄이는 PagedAttention의 목적과 구조를 구현한다.

커스텀 CUDA 커널, online softmax, 메모리 배치까지 직접 다루므로 모델 수식과 실제 GPU 실행 사이의 간격을 이해하기 좋다. 토큰 하나의 지연과 전체 처리량이 왜 다른 최적화 문제인지도 코드 수준에서 확인할 수 있다.

# 활용 방법

각 단계에서 참조 구현과 출력 오차를 비교하고, Nsight로 kernel launch, 메모리 전송, 점유율을 관찰한다. 처음부터 최적화를 좇기보다 단일 요청의 정확성을 만든 뒤 KV cache, batch size, sequence length를 한 변수씩 바꾸는 편이 학습에 유리하다.

# 주의할 점

생산용 vLLM의 대체품이 아니다. 지원 모델과 하드웨어가 제한적이고, 저장소 시점에 따라 배칭이나 PagedAttention 장이 미완성일 수 있다. 동시 요청 격리, OOM 복구, 양자화, 분산 실행, 보안 같은 운영 기능도 별도로 필요하다.

# 출처

- [tiny-vllm GitHub 저장소](https://github.com/jmaczan/tiny-vllm)
- [저장된 PyTorchKR 소개](https://discuss.pytorch.kr/t/tiny-vllm-c-cuda-vllm-llm/10455)
- [Notion 원본 항목](https://app.notion.com/p/3721a73cf20b81cd8622f6e58ea04e42)

