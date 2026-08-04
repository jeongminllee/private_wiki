---
type: Concept
title: LLM 생명주기 환경 설계
description: 개발·학습·서빙·평가 환경을 먼저 함께 검증하고, 의존성 충돌이 확인된 역할만 의도적으로 분리하는 설계 원칙
tags: [llm-infrastructure, mlops, finetuning, serving, evaluation, docker]
timestamp: 2026-07-28
status: active
---

# Summary

LLM 프로젝트의 환경 설계 목표는 모든 역할을 무조건 하나의 Python 환경에 넣는 것도, 처음부터 전부 별도 환경으로 나누는 것도 아니다.

핵심 원칙은 다음과 같다.

> 개발 → 학습 → 산출물 저장 → 새 process 재로드 → 실제 framework 서빙 → 평가까지 full training 전에 하나의 호환성 체인으로 검증한다. 하나의 환경에서 안정적으로 동작하면 통합하고, 실제 의존성 충돌이나 운영 경계가 확인된 역할만 분리한다.

환경이 여러 개라면 차이는 우연히 생긴 것이 아니라 이유, version, artifact와 interface contract가 기록된 **의도적인 차이**여야 한다.

# Why it matters

대형 모델의 full training은 수일이 걸릴 수 있다. 학습이 끝난 뒤 처음으로 vLLM 같은 실제 서빙 framework를 설치하면 다음 위험을 뒤늦게 발견할 수 있다.

- PyTorch, Transformers, CUDA 관련 package version 충돌
- tokenizer와 chat template 불일치
- LoRA adapter 저장 형식이나 rank 지원 문제
- 학습에서는 load되지만 serving framework에서는 지원되지 않는 architecture
- dtype, quantization, tensor parallel 설정 차이
- 평가 runner와 실제 API output contract 불일치

따라서 loss나 학습 완료만 확인해서는 end-to-end 성공을 보장할 수 없다. 실제 서비스 경로와 같은 API를 통해 smoke test와 평가를 통과해야 한다.

# Key Ideas

## 환경 통일과 역할 분리는 반대말이 아니다

실무에서 “환경을 통일한다”는 말은 보통 다음을 고정한다는 뜻이다.

- OS와 CUDA runtime 계열
- Python version과 package lock 또는 image tag
- Git commit
- base model revision
- adapter/checkpoint hash
- tokenizer와 chat template
- request/response schema
- 평가 데이터와 metric definition

반면 학습과 서빙을 반드시 같은 process나 동일한 최종 container에 넣어야 한다는 뜻은 아니다.

```text
공통 기반과 계약
├─ 개발·unit test
├─ 학습·checkpoint 생성
├─ serving API
└─ 외부 평가 runner
```

각 역할은 같은 model artifact와 계약을 사용하면서도 package나 권한, 자원 요구가 다르면 별도 process, virtual environment 또는 container로 실행할 수 있다.

## Docker는 재현성을 제공하지만 모든 역할을 하나로 합치지는 않는다

Docker를 사용하면 하나의 거대한 image에 학습·서빙·평가 package를 모두 설치할 수 있다. 작은 연구 환경에서는 이해와 실행이 단순하다는 장점이 있다.

규모가 커지면 하나의 Dockerfile에서 공통 base와 역할별 target을 만드는 방식이 더 안정적이다.

```text
Dockerfile
├─ base: CUDA, Python, 공통 코드와 계약
├─ training: LLaMA-Factory, PEFT, DeepSpeed
├─ serving: vLLM 또는 SGLang
└─ evaluation: challenge builder와 evaluator
```

이 구조는 기반과 version 정책을 통일하면서 불필요한 package, 권한과 변경 범위를 줄인다. serving framework만 바꿀 때 학습 image 전체를 다시 검증하지 않아도 된다.

## Kubernetes는 dependency 통합 도구가 아니라 실행 단위 조정 도구다

Kubernetes는 서로 다른 container를 하나의 환경으로 합치는 것이 아니라, 역할별 image를 Job, Pod, Service로 실행하고 network와 resource를 관리한다.

```text
Training Job
    ↓ immutable adapter
Artifact Storage
    ↓
Serving Pod ← HTTP ← Evaluation Job
                    ← NuriLab
```

단일 B200 서버와 작은 팀에서는 Kubernetes가 필수는 아니다. 먼저 virtual environment 또는 Docker Compose로 같은 경계를 검증하고, 여러 node, rollout, autoscaling, self-healing이 실제로 필요할 때 도입한다.

## 공유해야 하는 것은 환경보다 artifact와 contract다

학습과 서빙 환경을 분리해도 base model과 adapter를 복제할 필요는 없다.

```text
공유 또는 immutable artifact
├─ base model revision
├─ adapter/checkpoint + SHA-256
├─ tokenizer/chat template
└─ evaluation manifest

안정된 interface
└─ OpenAI-compatible HTTP API + JSON output contract
```

평가 runner는 challenge만 serving API에 전달하고 gold는 별도 process에 보관한다. 이는 환경 분리뿐 아니라 label 누출 방지와 평가 독립성을 위한 trust boundary다.

# 세 가지 환경 전략

| 전략 | 적합한 상황 | 장점 | 위험 |
| --- | --- | --- | --- |
| 단일 통합 환경 | 초기 PoC, dependency가 모두 호환됨 | 단순한 설치와 실행 | package 충돌 영향 범위가 큼 |
| 공통 base + 역할별 target | 장기 연구와 제품화 | 재현성과 격리를 함께 확보 | image·version 관리가 추가됨 |
| 완전 별도 환경 | 조직·보안·hardware·release 주기가 다름 | 장애와 권한 경계가 명확 | drift와 중복 관리 위험 |

기본 선택은 **통합 환경 후보를 먼저 end-to-end preflight하고, 실패 원인이 증명된 경우에만 분리**하는 것이다.

# Full training 전 생명주기 preflight

다음 검증을 100 step 수준의 작은 실행에서 먼저 끝낸다.

1. target serving framework를 모델 선정 단계에서 함께 정한다.
2. CUDA, Python, PyTorch, Transformers, PEFT, 학습 framework와 serving framework의 version matrix를 만든다.
3. config parse와 데이터 1 batch tokenization을 확인한다.
4. 실제 sequence length, batch, LoRA target으로 100 step 학습한다.
5. adapter/checkpoint를 저장한다.
6. 기존 학습 process를 종료하고 새 process에서 재로드한다.
7. 실제 vLLM/SGLang server에 adapter를 올린다.
8. `/v1/models`와 Chat Completions 요청을 확인한다.
9. held-out smoke와 output schema/safety 검사를 실행한다.
10. checkpoint resume, peak VRAM, step/request 시간, 예상 full-run 시간을 기록한다.

이 전체 경로가 동일 환경에서 통과하면 통합 상태로 full training을 시작한다. 실패하면 원인을 다음처럼 분류한다.

| 실패 유형 | 우선 조치 |
| --- | --- |
| Package resolver/version 충돌 | 공통 base 위에 training/serving target 분리 |
| Model architecture 미지원 | serving framework/version 또는 모델 후보 변경 |
| Chat template/output 차이 | template와 API contract 동결 후 재검증 |
| OOM/처리량 미달 | parallelism, dtype, quantization, 모델 규모 재검토 |
| 평가 parse/schema 실패 | prompt와 contract 수정 후 새 blind run |

# AegisLM-B200에서 얻은 교훈

## 확인된 사실

- Qwen3-Coder-Next 80B full training은 검증된 LLaMA-Factory 학습 환경에서 수일간 실행됐다.
- 해당 학습 virtual environment에는 실제 adapter 서빙에 사용할 vLLM이 설치돼 있지 않았다.
- 서빙 framework까지 포함한 end-to-end preflight는 full training 전에 완료되지 않았다.

## 이번 실행의 결정

학습 막바지에 vLLM을 기존 환경에 추가하면 package가 실제로 충돌하는지는 아직 확인되지 않았다. 하지만 이미 장시간 검증된 학습 환경을 변경할 필요가 없으므로, 이번에는 별도 `.venv-serving`을 위험 완화 조치로 사용한다.

```text
.venv
├─ 기존 학습 환경 보존
├─ challenge 생성
└─ 평가

.venv-serving
└─ vLLM + base model + LoRA adapter
```

이는 “학습과 서빙은 항상 분리해야 한다”는 장기 원칙이 아니다. full training 전에 통합 호환성을 확인하지 못한 현재 run을 안전하게 마무리하기 위한 예외적 선택이다.

## 다음 모델부터의 결정

- 통합 환경을 기본 후보로 구성한다.
- 100-step 학습만 성공했다고 full run을 시작하지 않는다.
- adapter 저장·새 process 재로드·실제 serving·smoke 평가까지 통과해야 한다.
- 동일 환경에서 모두 통과하면 그대로 사용한다.
- 충돌이 확인되면 공통 base와 contract를 유지하고 문제 역할만 분리한다.
- Docker는 검증된 version matrix가 나온 뒤 고정한다.
- Kubernetes는 단일 서버를 넘어선 운영 요구가 생길 때 검토한다.

# 실행 전 체크리스트

- [ ] 최종 serving framework를 모델과 함께 선정했는가?
- [ ] 학습과 serving package version을 한 표에서 검토했는가?
- [ ] 100-step adapter를 실제 serving framework에서 load했는가?
- [ ] 학습 때와 같은 tokenizer/chat template를 사용했는가?
- [ ] API를 통한 held-out smoke가 통과했는가?
- [ ] 평가 gold가 inference process와 분리됐는가?
- [ ] checkpoint save/reload/resume가 새 process에서 성공했는가?
- [ ] 환경을 분리했다면 구체적인 충돌과 version 차이를 기록했는가?
- [ ] model과 adapter는 hash로 동결하고 serving에서 읽기 전용으로 사용하는가?
- [ ] full training 예상 시간에 serving·평가 시간도 포함했는가?

# Related Concepts

- [네트워크와 배포: Docker에서 Kubernetes까지](../reading/notes/131-networking-deployment-docker-kubernetes.md)
- [vLLM과 Triton Inference Server로 LLM 서빙하기](../reading/notes/062-vllm-triton-serving.md)
- [Qwen3-Coder-Next 80B B200 2-GPU 실행 기록](../projects/Fine_Tuned/training/qwen3_coder_next_80b_2gpu_run_20260720.md)
- [AegisLM B200 운영·hand-off 기록](../projects/Fine_Tuned/b200/aegislm_b200_2gpu_rebuild.md)

# Citations

- 이번 AegisLM-B200 환경 결정과 대화에서 도출한 운영 교훈
- AegisLM-B200 학습·평가 문서와 실행 기록
