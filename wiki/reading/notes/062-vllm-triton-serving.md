---
type: Reference
title: "vLLM과 Triton Inference Server로 LLM 서빙하기"
description: "PagedAttention 기반 생성 엔진을 Triton의 모델 관리와 운영 인터페이스에 연결하는 입문 실습"
resource: https://ariz1623.tistory.com/367
notion: https://app.notion.com/p/2e71a73cf20b826b8e02014ae37c9829
tags: [reading, llm-inference, vllm, triton]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

글은 vLLM을 LLM 생성 실행 엔진으로, NVIDIA Triton Inference Server를 여러 모델의 배포·상태·API·메트릭을 관리하는 서빙 계층으로 소개한다. vLLM을 단독 실행하는 예제와 Triton의 vLLM backend를 Docker로 올리는 흐름을 함께 보여준다.

# 역할 구분

vLLM은 KV cache를 고정된 연속 메모리로 잡는 대신 블록 단위로 관리하는 PagedAttention과 요청 배칭으로 생성 처리량을 높인다. 오프라인에서는 `LLM`과 `SamplingParams`로 여러 프롬프트를 생성하고, 온라인에서는 OpenAI 호환 서버나 비동기 엔진으로 요청을 처리할 수 있다.

Triton은 모델 repository, HTTP/gRPC endpoint, 동적 배칭, GPU 배치와 Prometheus 메트릭 같은 운영 표면을 제공한다. vLLM backend에서는 새 요청을 vLLM의 비동기 엔진에 전달하고 실제 inflight batching과 KV cache 관리는 vLLM이 담당한다.

# 실습 흐름

1. vLLM 단독으로 모델이 정확히 로드되고 생성되는지 확인한다.
2. 모델 이름, tensor parallel 크기와 GPU 메모리 사용률을 설정한다.
3. 공식 Triton vLLM 이미지와 model repository를 고정 버전으로 실행한다.
4. 생성 endpoint를 호출하고 latency, time-to-first-token, inter-token latency, 처리량과 GPU 메모리를 기록한다.
5. 동시성, 입력·출력 길이와 batch 분포를 실제 트래픽에 맞춰 부하 시험한다.

# 시점과 주의점

원문은 2024년 12월 글이므로 Python, CUDA, 이미지 태그와 지원 기능이 현재와 다를 수 있다. “C++라서 Python보다 빠르다”나 특정 배수의 성능처럼 넓은 표현은 모델·backend·하드웨어 조건 없이 일반화할 수 없다. 현재 공식 문서와 고정된 컨테이너 버전을 우선한다.

# 출처

- [저장된 실습 글](https://ariz1623.tistory.com/367)
- [vLLM 공식 문서](https://docs.vllm.ai/)
- [Triton vLLM backend](https://github.com/triton-inference-server/vllm_backend)
- [Notion 원본 항목](https://app.notion.com/p/2e71a73cf20b826b8e02014ae37c9829)

