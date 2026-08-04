---
type: Concept
title: "Modal 프레임워크 설명"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2026-07-26)"
tags: [cs, chatgpt-export]
timestamp: 2026-07-26
status: active
---

# Modal 프레임워크 설명

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-07-26

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
혹시 modal 이라는 사이트, 프레임워크 알아? https://modal.com/docs/guide/cuda

### 💡 답변 (Assistant)
네, 알아요. 링크의 CUDA 가이드와 Modal 공식 문서를 기준으로, 이게 정확히 어떤 서비스인지와 지금 하시는 GPU·LLM 작업에 어떻게 쓸 수 있는지 확인해볼게요.

---

### 💡 답변 (Assistant)
네, 알아요. **Modal은 단순한 Python 프레임워크라기보다, Python 코드로 클라우드 GPU와 컨테이너를 실행·배포하는 서버리스 AI 인프라 플랫폼**입니다.

쉽게 비유하면 다음을 하나로 묶어 놓은 느낌입니다.

> GPU 클라우드 + Docker 이미지 + 서버리스 함수 + 자동 확장 + API 배포

예를 들어 아래처럼 작성하면 A100이 장착된 컨테이너가 클라우드에서 실행됩니다.

```python
import modal

app = modal.App()

image = modal.Image.debian_slim().pip_install("torch")

@app.function(
    gpu="A100",
    image=image,
)
def check_gpu() -> bool:
    import torch

    return torch.cuda.is_available()
```

실행은 로컬 터미널에서 합니다.

```bash
pip install modal
modal setup
modal run app.py
```

Modal이 코드를 컨테이너로 만들고, 적절한 클라우드 GPU에서 실행하며, 요청량에 따라 컨테이너 수도 자동 조정합니다. 사용자는 AWS 계정이나 Kubernetes 클러스터를 직접 구성하지 않아도 됩니다. [Modal 공식 소개](https://modal.com/docs/guide)

링크해주신 CUDA 문서에서 중요한 내용은 다음과 같습니다.

- NVIDIA 드라이버와 CUDA Driver API는 Modal 호스트에 이미 설치되어 있음
- `torch`처럼 CUDA 의존성을 포함하는 패키지는 보통 `pip_install()`만으로 사용 가능
- `flash-attn`, TensorRT-LLM처럼 컴파일 환경이 필요한 라이브러리는 `nvidia/cuda:*devel*` 기반 이미지를 사용하는 것이 안전함
- 컨테이너 CUDA 버전은 호스트 드라이버가 지원하는 버전보다 높으면 안 됨  
  [Modal CUDA 가이드](https://modal.com/docs/guide/cuda)

특히 지금 하시는 LLM 작업과 잘 맞습니다. Modal은 현재 T4부터 A100, H100/H200, B200/B300까지 지정할 수 있고, 다음처럼 한 노드에서 여러 GPU도 요청할 수 있습니다.

```python
@app.function(gpu="B200:4")
def run_distributed_job() -> None:
    ...
```

지원 GPU에 따라 한 컨테이너에서 최대 8장까지 붙일 수 있습니다. 다만 3장 이상은 할당 대기시간이 길어질 수 있고, 멀티노드는 아직 제한적인 단계입니다. [Modal GPU 가이드](https://modal.com/docs/guide/gpu)

또한 vLLM을 OpenAI 호환 API로 배포하는 공식 예제가 있어서, 예전에 계획하셨던 **Hugging Face 모델 + vLLM + 필요할 때만 GPU 실행** 구조를 만들기에 상당히 편합니다. 모델 가중치는 `Modal Volume`에 저장해 매번 다시 다운로드하지 않을 수 있습니다. [Modal vLLM 예제](https://modal.com/docs/examples/vllm_inference)

다만 현재 가지고 계신 B200 서버를 대체하는 것보다는 다음 용도로 더 매력적입니다.

- 로컬 GPU가 없어진 이후 단기 실험
- 모델별 H100·H200·B200 성능 비교
- 간헐적으로 사용하는 vLLM API
- 배치 추론과 파인튜닝 작업
- 인프라 관리 없이 빠르게 PoC 배포

반대로 GPU를 계속 24시간 사용하는 서비스라면 서버리스 비용이 불리할 수 있고, NCCL·네트워크·드라이버를 아주 세밀하게 만지는 분산학습 실험은 자체 서버보다 자유도가 낮습니다. 즉, **상시 대규모 학습 클러스터보다는 GPU를 필요할 때 코드 한 줄로 빌려 쓰는 AI 개발 환경**에 가깝습니다.

---

### ❓ 질문 (User)
단순 테스트를 위해서라면 나한테 딱 부합하는 서비스를 제공하는 업체인거 같아서. 마침 크레딧을 받아놓은게 있거든. 1년뒤면 만료라 후딱 써버려야해서.

### 💡 답변 (Assistant)
맞아요. **“GPU가 항상 필요한 건 아니지만, 필요할 때 강한 GPU로 이것저것 실험해 보고 싶다”**는 지금 상황에 Modal이 상당히 잘 맞아요. 특히 크레딧까지 있다면 더 그렇고요.

다만 무작정 비싼 B200부터 태우기보다는, 크레딧을 다음처럼 쓰는 게 남는 장사입니다.

- **L4/L40S**: 개발·디버깅, 작은 모델 API 테스트
- **A100/H100**: vLLM 서빙과 파인튜닝 실습
- **H200/B200**: 70B 이상 모델, 긴 컨텍스트, 처리량 벤치마크
- **멀티 GPU**: Tensor Parallel, 분산 추론·학습 경험
- **Modal 기능**: Volume, Secret, 자동 확장, scale-to-zero, API 배포까지 경험

첫 프로젝트로는 이 구성이 좋겠습니다.

1. Hugging Face 모델을 Modal Volume에 미리 다운로드
2. vLLM으로 OpenAI 호환 API 배포
3. L40S → H100 → H200/B200 순서로 성능 비교
4. TTFT, tokens/s, 동시 요청 처리량, 비용을 기록
5. 마지막으로 2~4 GPU Tensor Parallel과 LoRA 파인튜닝 실험

특히 Hugging Face 토큰도 코드나 서버 환경파일에 직접 남기지 않고 `modal.Secret`으로 관리할 수 있습니다.

```python
@app.function(
    gpu="H100",
    secrets=[modal.Secret.from_name("huggingface-secret")],
)
def run_model() -> None:
    ...
```

주의할 점은 **모델 다운로드와 컨테이너 초기화 시간을 매번 반복하지 않는 것**입니다. 모델은 Volume에 캐시하고, 개발 단계에서는 저렴한 GPU나 CPU로 이미지 빌드를 검증한 다음 고가 GPU를 붙여야 크레딧 낭비가 적습니다.

크레딧 금액만 알려주시면 제가 그 금액을 기준으로:

- 1년 동안의 실험 로드맵
- GPU별 예상 사용시간
- vLLM·파인튜닝·분산처리 배분
- 첫 번째 Modal 프로젝트 코드

까지 현실적으로 설계해드릴 수 있어요. Modal을 제대로 써보면 단순 클라우드 GPU 사용뿐 아니라 **AI 서비스 배포와 GPU 비용 최적화 경험**도 함께 가져갈 수 있습니다.

---

### ❓ 질문 (User)
나중에 이거 관련해서 사용방법 좀 알려주라

### 💡 답변 (Assistant)
물론이죠. 나중에 시작할 때 **계정 설정부터 첫 GPU 실행, Modal Volume·Secret, vLLM API 배포, 멀티 GPU와 비용 관리**까지 단계별로 같이 진행하죠.

그때 크레딧 금액과 해보고 싶은 모델만 알려주시면, 낭비 없이 실습 순서부터 잡아드릴게요.

---
