---
type: Concept
title: "Modal 프레임워크 튜토리얼"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2026-07-26)"
tags: [cs, chatgpt-export]
timestamp: 2026-07-26
status: active
---

# Modal 프레임워크 튜토리얼

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-07-26

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
modal 프레임워크 설명 대화를 이어나가고싶어.

### 💡 답변 (Assistant)
좋아. 이전 대화에서는 **Modal을 로컬 GPU 없이도 필요한 순간에만 클라우드 GPU를 실행하는 Python 기반 서버리스 컴퓨팅 플랫폼**으로 보고 있었어.

네 상황과 특히 잘 맞는 이유는 다음이었지.

- 단순 CUDA·PyTorch·LLM 테스트를 빠르게 실행
- 서버를 상시 운영하지 않고 실행한 만큼만 크레딧 사용
- Dockerfile이나 복잡한 인프라 설정 없이 Python 코드로 환경 정의
- 이미 받은 크레딧이 있고 약 1년 뒤 만료되므로 실험용으로 적극 활용
- 나중에는 모델 서빙, 배치 추론, 파인튜닝 같은 작업까지 확장 가능

학습 순서는 이렇게 가는 게 가장 자연스러워.

1. Modal CLI 설치 및 로그인
2. CPU 함수 하나 실행
3. GPU에서 `torch.cuda` 확인
4. 로컬 코드를 Modal GPU로 실행
5. 파일·모델 캐시를 위한 Volume 사용
6. Hugging Face 모델 추론
7. 웹 API 형태로 배포
8. vLLM 서빙이나 파인튜닝 실험

우선 가장 작은 GPU 테스트는 대략 이런 형태야.

```python
import modal

app = modal.App("gpu-test")

image = modal.Image.debian_slim().pip_install("torch")


@app.function(
    image=image,
    gpu="T4",
    timeout=600,
)
def check_gpu() -> None:
    import torch

    print(f"CUDA available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")


@app.local_entrypoint()
def main() -> None:
    check_gpu.remote()
```

실행은 다음처럼 해.

```bash
modal setup
modal run gpu_test.py
```

여기서 핵심은 `check_gpu()`가 네 컴퓨터에서 실행되는 것이 아니라, `check_gpu.remote()` 호출을 통해 **Modal이 생성한 원격 GPU 컨테이너에서 실행된다**는 점이야.

다음 단계는 이 흐름 그대로 **Modal 설치부터 GPU 확인까지 실제 튜토리얼 형태로 진행**하면 돼.

---
