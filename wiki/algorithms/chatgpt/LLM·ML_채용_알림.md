---
type: Concept
title: "LLM·ML 채용 알림"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-07-26)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-07-26
status: active
---

# LLM·ML 채용 알림

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-07-26

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
I want alerts when high-fit LLM/NLP engineering or ML infrastructure roles appear, especially roles valuing Python, PyTorch, HuggingFace Transformers, Linux, GitHub, model tuning, benchmarks, and latest-paper reading. Include why each role fits and what to prepare.

### 💡 답변 (Assistant)
좋습니다. 알림 조건을 정확히 맞추기 위해 아래 세 가지만 정해주세요.

genui{"ask_user_input":{"questions":[{"question":"어느 지역의 채용을 볼까요?","options":["한국 내 채용","글로벌 원격근무","한국·글로벌 모두"],"type":"single_select","free_text_placeholder":"희망 국가·도시를 입력하세요"},{"question":"어떤 경력 수준까지 포함할까요?","options":["신입·주니어","경력 1–5년","경력 무관","인턴·계약직도 포함"],"type":"multi_select","free_text_placeholder":"제외할 경력 조건을 적어주세요"},{"question":"얼마나 자주 확인할까요?","options":["매일 아침","평일 아침","주 2회","새 공고 발견 시"],"type":"single_select","free_text_placeholder":"원하는 요일과 시간을 적어주세요"}]}}

---

### ❓ 질문 (User)
> 어느 지역의 채용을 볼까요?
한국·글로벌 모두

> 어떤 경력 수준까지 포함할까요?
신입·주니어, 경력 무관, 인턴·계약직도 포함

> 얼마나 자주 확인할까요?
매일 아침

### 💡 답변 (Assistant)
설정했습니다. 매일 아침 **한국 시간 오전 8시 전후**에 한국·글로벌 채용을 확인합니다.

새롭게 발견된 고적합 공고가 있을 때만 알림을 보내며, 각 공고에는 다음을 포함합니다.

- 직무·회사·지역·원격 여부·고용 형태·요구 경력
- 지원 링크와 게시일 또는 마감일
- 현재 기술 스택과 잘 맞는 이유
- 부족할 수 있는 요건
- 지원 전 준비할 프로젝트, 학습 주제, 이력서 보완점

이전에 안내한 공고는 중복해서 보내지 않고, 적합한 신규 공고가 없는 날에는 알림을 보내지 않습니다.

---

### 💡 답변 (Assistant)
## 오늘 확인된 고적합 공고

### 1. Upstage — AI Engineer, LLM Inference Internship  
**적합도: 9.6/10 · 최우선 지원 권장**

- **근무:** 한국, 리모트
- **형태:** 3개월 인턴, 정규직 전환형
- **경력:** 신입
- **마감:** 상시채용
- **지원:** **[인턴] AI Engineer - LLM Inference** citeturn247615search3

LLM 서빙의 latency·throughput·cost 최적화, Solar 모델 벤치마크·평가 자동화, CI 파이프라인, 모니터링과 관측 가능성 구축을 담당합니다. vLLM·SGLang, KV-cache offloading, speculative decoding, expert parallelism 등 최신 추론 기술도 직접 다룹니다. citeturn284732view1

**잘 맞는 이유:** 현재 진행 중인 B200 다중 GPU, vLLM 로컬 서빙, 모델 추론·파인튜닝 계획과 거의 정확히 일치합니다. Python·PyTorch·Linux 경험에 더해, 제한된 GPU 환경에서 성능과 비용을 함께 고민해온 점도 강한 지원 신호가 됩니다.

**부족할 수 있는 부분:** C++/CUDA/Triton 기반 커널 최적화, 분산 추론 벤치마킹 결과가 포트폴리오에 아직 명시적으로 드러나지 않을 가능성이 큽니다.

**지원 전 준비:**
- vLLM으로 동일 모델의 tensor parallel 1·2·4 GPU 비교
- TTFT, TPOT, throughput, GPU memory를 표와 그래프로 정리
- prefix caching·quantization·speculative decoding 중 하나를 적용한 전후 비교
- `pytest` 기반 벤치마크 회귀 테스트와 GitHub Actions 구성

---

### 2. Anlatan — Machine Learning Engineer  
**적합도: 9.1/10 · 글로벌 지원 권장**

- **근무:** 글로벌 원격
- **형태:** 정규직
- **경력:** 연차 기준 미표기
- **게시일:** 공고문 미표기, 2026년 7월 27일 현재 지원 페이지 활성
- **지원:** **Machine Learning Engineer** citeturn485012view0

분산 학습 스택에서 LLM·이미지 모델을 학습하고, 새 아키텍처와 알고리즘을 구현하며, 모델 파인튜닝과 제품 적용을 반복하는 역할입니다. Python·PyTorch, NLP 모델 학습 경험, 최신 논문을 읽고 PyTorch로 정확히 재현하는 능력을 직접 요구합니다. Kubernetes·SLURM·분산 컴퓨팅·Triton은 우대 조건입니다. citeturn485012view0

**잘 맞는 이유:** 사용자가 지정한 Python, PyTorch, 최신 논문 독해, 모델 튜닝, Linux, 대규모 GPU 실험이라는 조건이 가장 직접적으로 명시된 글로벌 공고입니다. 석사 연구에서 수치해석과 실험 결과를 체계적으로 분석한 경험도 논문 재현 업무와 연결할 수 있습니다.

**부족할 수 있는 부분:** 실제 LLM 논문 재현 결과, SLURM 기반 멀티노드 학습, 오픈소스 PR이 핵심 증거로 요구될 가능성이 있습니다.

**지원 전 준비:**
- 최근 LLM 논문 한 편을 골라 최소 재현 프로젝트 제작
- `transformers`·`accelerate` 또는 FSDP/DeepSpeed로 다중 GPU 학습
- 실험 설정, seed, 데이터, 성능 차이와 실패 원인을 README에 기록
- 논문 원 결과와 재현 결과를 비교한 기술 보고서 첨부

---

### 3. Upstage — AI Research Engineer, Post-training Internship  
**적합도: 7.8/10 · 연구 포트폴리오 보강 후 지원**

- **근무:** 원격 중심
- **형태:** 체험형 인턴, 3~6개월
- **경력:** 경력 무관
- **마감:** 공식 페이지에서 현재 모집 중
- **지원:** **AI Research Engineer - Post-training Internship** citeturn247615search1turn247615search4

수학·코드·일반 추론·도구 사용을 위한 강화학습, agentic tool-use 데이터 합성, reward model, DPO·RLHF·RLVR 등 LLM post-training을 연구합니다. 특정 문제에서 최고 성능을 달성한 파인튜닝 경험과 ML/NLP 국제학회 출판 기록을 강하게 선호합니다. citeturn247615search4

**잘 맞는 이유:** Hugging Face와 PyTorch를 기반으로 모델 튜닝을 배우려는 방향, Kaggle·벤치마크 실험 경험, 제한된 컴퓨팅에서 성능을 끌어올리려는 성향과 잘 맞습니다.

**가장 큰 간극:** ML/NLP 1저자 논문과 검증된 LLM post-training 성과가 사실상 높은 진입장벽입니다. 현재 상태에서는 합격 가능성보다 도전적 지원에 가깝습니다.

**지원 전 준비:**
- 7B~14B 모델 대상 SFT → DPO 또는 GRPO 실험
- 베이스 모델·SFT·선호학습 모델을 동일 벤치마크로 비교
- 데이터 생성·필터링·오염 검사 과정 문서화
- 실패 실험까지 포함한 4~6페이지 연구형 리포트 작성

---

### 4. Modal — Member of Technical Staff, ML Training Systems  
**현재 적합도: 6.5/10 · 장기 목표 적합도: 9.3/10**

- **근무:** 뉴욕 또는 샌프란시스코, 대면 근무
- **형태:** 정규직
- **경력:** 고성능 코드 작성 경력 5년 이상
- **공고 상태:** 2026년 7월 27일 공식 채용 페이지 활성
- **지원:** **Member of Technical Staff - ML Training Systems** citeturn743796search0turn743796search1

PyTorch와 Hugging Face 계열 학습 프레임워크, 학습 병목 최적화, Linux 커널·파일시스템·컨테이너 이해를 요구합니다. 프로덕션 ML 모델 학습 경험과 오픈소스 기여를 특히 중시합니다. citeturn743796search3

**잘 맞는 이유:** 최근 관심을 보인 Modal, 대규모 GPU 학습, ML 인프라, Linux, 분산 시스템이라는 장기 경력 방향과 완전히 일치합니다.

**현실적인 장애물:** 5년 이상의 고성능 시스템 개발 경력과 미국 현지 대면 근무 조건 때문에 지금 당장의 우선 지원처로는 적합하지 않습니다.

**준비 방향:** Modal에서 B200 학습 작업을 실행하고, 데이터 로딩·GPU utilization·checkpoint I/O 병목을 분석한 공개 프로젝트를 만드는 것이 가장 강한 연결고리가 됩니다.

## 이번 지원 우선순위

**Upstage LLM Inference → Anlatan → Upstage Post-training → Modal**

가장 먼저 준비할 포트폴리오는 **“vLLM 기반 멀티 GPU 추론 벤치마크 및 최적화”**입니다. 하나의 프로젝트로 Upstage Inference, Anlatan, Modal 세 공고에 공통으로 요구되는 Python·PyTorch·Linux·분산 실행·벤치마크·최신 기술 이해를 동시에 증명할 수 있습니다.

---

### 💡 답변 (Assistant)
## 새로 확인된 고적합 공고 — 2026년 7월 28일

이전에 안내한 Upstage·Anlatan·Modal 공고는 제외했습니다. 이번에는 **한국 2건, 글로벌 2건**이 새롭게 확인됐습니다.

### 1. ENERZAi — AI 최적화 Researcher
**적합도: 9.5/10 · 국내 최우선 지원 권장**

- **근무지:** 서울 강남구 역삼동
- **고용 형태:** 정규직
- **경력:** 경력 무관·신입 지원 가능
- **학력:** 학사 이상, 졸업예정자 가능
- **마감:** **2026년 8월 7일**
- **지원:** ENERZAi 공식 채용 페이지 및 공고 citeturn871944search10turn871944search6

LLM 최적화, 딥러닝 연산 그래프 최적화, 추론 엔진 개발을 담당합니다. Python과 PyTorch 경험이 기본 요건이며, TensorRT·ONNX Runtime·TFLite, Perf·vTune·Nsight Systems, CUDA·OpenCL 등의 성능 분석 및 가속 경험을 우대합니다. citeturn871944search5turn871944search2

**잘 맞는 이유:**  
사용자의 B200 다중 GPU 실험, vLLM 서빙, Linux 환경 운영, 모델 성능 측정 관심을 가장 직접적으로 활용할 수 있는 국내 포지션입니다. 특히 단순 모델 개발이 아니라 **latency·throughput·메모리·하드웨어 특성을 함께 다루는 ML 시스템 엔지니어링**이라는 점에서 장기 목표와 매우 가깝습니다.

**부족할 수 있는 부분:**  
프로파일러를 이용한 병목 분석, ONNX/TensorRT 변환, 컴퓨터 아키텍처와 연산 그래프 최적화 경험이 이력서에 명시적으로 드러나지 않을 수 있습니다.

**지원 전 준비:**

1. PyTorch 모델을 `torch.compile`, ONNX Runtime, TensorRT로 각각 실행
2. latency, throughput, peak memory, 정확도 변화를 표로 비교
3. Nsight Systems 또는 PyTorch Profiler로 병목 구간 분석
4. 결과를 GitHub README와 2페이지 기술 보고서로 정리

---

### 2. ENERZAi — ML Engineer / Researcher
**적합도: 9.1/10 · 모델 최적화 연구 지향**

- **근무지:** 서울 강남구
- **고용 형태:** 정규직
- **경력:** JobKorea 기준 경력 무관, 일부 플랫폼에는 1년 이상으로 표기가 달라 공식 지원 페이지 확인 필요
- **학력:** 학사 이상
- **마감:** 채용 시 마감
- **지원:** 공식 채용 페이지 citeturn369463search2turn369463search17turn369463search11

초경량 Transformer 언어 모델 설계·학습, QAT·PTQ와 ultra-low-bit 양자화, STT·LLM·TTS 기반 온디바이스 에이전트, CPU·GPU·NPU 환경의 모델 가속을 연구합니다. 실제 하드웨어에서 가속되도록 추론 엔진 팀과 통합하는 업무도 포함됩니다. citeturn369463search8turn369463search5

**잘 맞는 이유:**  
PyTorch 모델 학습과 파인튜닝뿐 아니라 모델 압축, 추론 효율, 실험 결과 분석과 문서화 능력을 함께 평가하는 포지션입니다. 목재물리 석사 과정에서 수행한 수치분석·실험 설계 경험도 “연구 가설 수립 → 실험 → 결과 해석” 역량으로 연결할 수 있습니다.

**부족할 수 있는 부분:**  
양자화 알고리즘의 수학적 이해, QAT 구현, 온디바이스 하드웨어와 STT/TTS 모델 경험이 부족할 수 있습니다.

**지원 전 준비:**

- 소형 Transformer 모델에 FP16·INT8·4bit 양자화를 적용
- 원본 대비 정확도·모델 크기·latency·메모리 사용량 비교
- PTQ와 QAT의 차이를 실제 실험으로 설명
- 양자화로 성능이 저하된 레이어와 원인을 분석한 보고서 작성

---

### 3. Perplexity — Search Machine Learning Engineer Internship
**적합도: 8.9/10 · 글로벌 NLP 인턴 최우선**

- **근무지:** 런던 또는 베오그라드
- **근무 방식:** 대면 근무
- **고용 형태:** 풀타임 인턴
- **기간:** 12~24주
- **경력:** 관련 프로젝트·연구 경험 중심, 기존 인턴 경력은 필수 아님
- **게시 상태:** 베오그라드 공고는 약 1일 전 신규 게시, 런던 공고도 공식 페이지에서 모집 중
- **지원:** 런던·베오그라드 공식 공고 citeturn804855search0turn804855search1turn619788search8

검색 retrieval·ranking·classification 모델 개발, LLM 기반 평가 모델, RAG 파이프라인, 검색 품질 실험과 배포·모니터링을 담당합니다. Python 및 PyTorch·TensorFlow·JAX 프로젝트 경험을 요구하며, 정보검색·추천·NLP와 오프라인 평가·A/B 테스트 경험을 우대합니다. citeturn804855search3turn804855search11

**잘 맞는 이유:**  
Hugging Face Transformers, NLP, 벤치마크, 모델 평가라는 핵심 기술이 거의 정확히 일치합니다. 논문을 읽고 구현하는 능력과 실험 결과를 정량적으로 비교하는 습관도 높은 평가를 받을 수 있습니다.

**가장 큰 장애물:**  
런던 또는 베오그라드 대면 근무이므로 취업비자·인턴 비자와 체류 가능 여부를 먼저 확인해야 합니다. 검색·랭킹 모델 포트폴리오도 별도로 필요합니다.

**지원 전 준비:**

- Hugging Face 기반 bi-encoder 검색 모델 구축
- cross-encoder reranker 추가
- Recall@K, MRR, NDCG, latency 측정
- RAG 적용 전후 답변 정확도와 검색 실패 사례 분석
- 영어 README와 실험 재현 명령어 제공

---

### 4. Perplexity — Search Backend Infra Engineer Internship
**적합도: 8.0/10 · ML 인프라 전환용 유력 후보**

- **근무지:** 세르비아 베오그라드
- **근무 방식:** 대면
- **고용 형태:** 풀타임 인턴
- **게시 상태:** 공식 채용 페이지 활성, 최근 신규 노출
- **지원:** 공식 공고 citeturn496086search0turn619788search5

고성능 검색 시스템을 위한 인프라, AWS 기반 클라우드 시스템, CI/CD, 테스트·릴리스 자동화, Linux 서비스와 컨테이너의 디버깅·최적화를 담당합니다. 주요 언어는 Rust·Go·C++이며 Linux와 클라우드 인프라 경험은 우대 요소입니다. citeturn804855search5turn619788search13

**잘 맞는 이유:**  
Linux, GitHub, 테스트 자동화, 모델 서빙과 운영 환경에 관심이 크기 때문에 ML 인프라 진입 경로로 적합합니다. pytest 기반 코딩테스트 환경, vLLM 서버 운영과 GPU 모니터링 경험도 연결할 수 있습니다.

**부족할 수 있는 부분:**  
Python 중심 경력만으로는 부족하며 Rust·Go·C++ 중 하나를 실제 프로젝트에서 사용했다는 증거가 필요합니다. AWS와 네트워크·분산 시스템 기초도 보강해야 합니다.

**지원 전 준비:**

- Go 또는 Rust로 간단한 검색·추론 API 작성
- Docker 패키징과 GitHub Actions 테스트 구성
- 동시 요청 부하 테스트와 latency percentile 측정
- Prometheus 기반 기본 모니터링 추가
- 장애 상황과 성능 개선 과정을 README에 기록

## 지원 우선순위

**ENERZAi AI 최적화 Researcher → ENERZAi ML Engineer/Researcher → Perplexity Search ML Internship → Perplexity Backend Infra Internship**

이번 공고 중에서는 **ENERZAi AI 최적화 Researcher가 현재 기술 수준, 국내 근무 가능성, ML 인프라 장기 목표를 모두 고려했을 때 가장 현실적이고 강한 기회**입니다. 마감일이 **2026년 8월 7일**이므로 해당 포지션용 포트폴리오와 이력서 수정을 먼저 진행하는 것이 좋습니다.

---

### 💡 답변 (Assistant)
## 새로 확인된 고적합 공고 — 2026년 7월 29일

이전에 안내한 Upstage·Anlatan·Modal·ENERZAi·Perplexity 공고는 제외했습니다. 이번에는 **42dot의 신규 LLM 엔지니어 공고 2건**이 높은 적합도로 확인됐습니다.

### 1. 42dot — LLM Engineer (LLM Training)
**적합도: 9.3/10 · 이번 주 최우선 지원 권장**

- **근무지:** 판교 Software Dream Center
- **근무 형태:** 정규직·풀타임
- **요구 경력:** 딥러닝·NLP 경력 3년 이상, **석사 신입 지원 가능**
- **게시일:** **2026년 7월 22일**
- **마감:** 별도 기한 미표기, 현재 공식 페이지에서 지원 가능
- **지원:** 42dot 공식 채용 공고 citeturn932206view2

Pre-training과 post-training의 학습 효율 향상, Self-Refine 학습 구조 설계가 핵심 업무입니다. Python·PyTorch 기반 모델 설계·학습·평가·최적화, GPU LLM 학습 및 트러블슈팅, Slurm·DDP·Horovod와 같은 분산 학습 경험을 요구합니다. Docker·Kubernetes, GPU 클러스터 학습 파이프라인, SFT·PEFT 경험은 우대사항입니다. citeturn932206view2

**잘 맞는 이유**

현재 보유한 B200 다중 GPU 환경, PyTorch·Hugging Face 경험, 대규모 모델을 직접 학습·서빙해보려는 계획과 가장 밀접합니다. 특히 제한된 GPU 수에서 학습 효율과 메모리 사용량을 비교하고 실험을 기록하려는 방향은 이 직무의 핵심인 **학습 파이프라인 최적화와 GPU 트러블슈팅**으로 연결할 수 있습니다.

**부족할 수 있는 부분**

가장 큰 위험은 석사 전공이 AI·NLP가 아니라는 점입니다. 공고에는 석사 신입 지원 가능이라고 명시돼 있지만, 딥러닝·NLP 연구개발 경험을 별도로 요구하므로 학위 자체보다 **LLM 학습 결과를 증명하는 프로젝트**가 중요합니다. Slurm·DDP 기반 분산 학습, 실제 LLM post-training, Docker·Kubernetes 운영 결과도 명확한 포트폴리오가 필요합니다.

**지원 전 준비**

- 7B~14B 모델을 대상으로 LoRA 또는 QLoRA SFT 수행
- 1·2·4 GPU DDP/FSDP 설정별 tokens/s, VRAM, 학습 시간 비교
- gradient accumulation, activation checkpointing, FlashAttention 적용 전후 분석
- W&B 또는 MLflow를 활용한 실험 추적
- Docker 실행 환경과 재현 명령어 제공
- OOM, NCCL timeout, 데이터 로딩 병목을 어떻게 해결했는지 문서화

이 프로젝트는 **모델 성능 자체보다 학습 시스템을 어떻게 측정하고 개선했는지**가 중요합니다.

---

### 2. 42dot — LLM Engineer (Reinforcement Learning)
**적합도: 8.6/10 · 도전적이지만 지원 가치 높음**

- **근무지:** 판교 Software Dream Center
- **근무 형태:** 정규직·풀타임
- **요구 경력:** 딥러닝·NLP 경력 3년 이상, **석사 신입 지원 가능**
- **게시일:** **2026년 7월 22일**
- **마감:** 별도 기한 미표기, 현재 공식 페이지에서 지원 가능
- **지원:** 42dot 공식 채용 공고 citeturn932206view3

Direct Alignment, PPO·GRPO·DPO를 활용한 학습 효율 향상, reward hacking 방지, Self-Refine 구조, 외부 API와 도구를 스스로 선택하는 LLM 학습을 담당합니다. Python·PyTorch, GPU 기반 LLM 학습·트러블슈팅, Slurm·DDP·Horovod 경험을 요구하고 SFT·PEFT와 GPU 클러스터 운영 경험을 우대합니다. citeturn932206view3

**잘 맞는 이유**

PyTorch·Hugging Face를 활용한 모델 튜닝 관심, 최신 논문을 읽고 구현하려는 학습 방향, 에이전트와 tool-use에 대한 관심이 직무와 잘 맞습니다. 다중 GPU를 사용할 수 있는 현재 환경은 post-training 알고리즘을 직접 비교하는 포트폴리오를 만들기에 강한 장점입니다.

**부족할 수 있는 부분**

PPO·GRPO·DPO, reward model, preference dataset, KL regularization 등 alignment 학습 경험이 아직 핵심 경력으로 드러나지 않습니다. 또한 학습 결과를 단순 loss가 아니라 정확성·안정성·reward hacking 관점에서 평가한 증거가 필요합니다.

**지원 전 준비**

- 동일 베이스 모델에 SFT → DPO 또는 GRPO를 순차 적용
- Base·SFT·DPO/GRPO 모델을 동일 벤치마크로 비교
- 학습 reward와 실제 정답률이 어긋나는 사례 분석
- 데이터 생성·필터링·중복 제거 과정을 문서화
- LoRA rank, learning rate, KL 계수에 따른 결과 비교
- 간단한 tool-use 데이터셋으로 API 선택 정확도 평가

## 지원 우선순위

**LLM Training → Reinforcement Learning**

두 공고 모두 지원할 수 있지만, 현재 경력에서는 **LLM Training이 더 현실적**입니다. 먼저 분산 학습·SFT·PEFT·GPU 성능 분석을 중심으로 이력서를 구성하고, Reinforcement Learning 지원서에는 DPO·GRPO 실험과 최신 post-training 논문 재현 계획을 별도로 강조하는 전략이 좋습니다.

---

### 💡 답변 (Assistant)
## 새로 확인된 고적합 공고 — 2026년 7월 30일

기존에 안내한 Upstage·Anlatan·Modal·ENERZAi·Perplexity·42dot 공고는 제외했습니다. 이번에는 **최근 게시된 글로벌 공고 3건**이 확인됐습니다.

### 1. Brain Co. — Early Career Machine Learning Engineer, Applied AI

**종합 적합도: 8.9/10 · 이번 회차 최우선 지원 후보**

- **근무지:** 미국 샌프란시스코 베이 지역
- **근무 방식:** 하이브리드
- **고용 형태:** 정규직·풀타임
- **요구 경력:** Applied ML·AI 관련 **0~2년**
- **게시일:** **2026년 7월 27일경**
- **마감:** 별도 기한 미표기
- **지원:** Brain Co. 공식 채용 공고 citeturn282709search0turn282709search2

LLM 기반 시스템을 실제 산업 문제에 적용하고, 데이터 파이프라인과 모델을 성능·정확도 관점에서 최적화하는 역할입니다. GenAI 애플리케이션, 에이전트·추론 워크플로·RAG 경험과 PyTorch·JAX·TensorFlow 중 하나의 구현 경험을 요구하며, 최신 ML·AI 기술을 지속해서 파악하는 능력도 명시돼 있습니다. citeturn724807search5turn282709search6

**잘 맞는 이유**

Python·PyTorch·Hugging Face 기반 실험 경험과 LLM 에이전트, RAG, 모델 서빙에 대한 관심을 직접 활용할 수 있습니다. 석사 과정에서 수행한 수치분석과 실험 설계 경험도 모델 실패 원인 분석, 평가 지표 설계, 결과 해석 역량으로 연결하기 좋습니다.

**부족할 수 있는 부분**

가장 큰 간극은 프로덕션 환경에 배포된 GenAI 시스템 사례입니다. 고객·정부기관과 직접 소통하는 성격도 있어 영어 기술 설명 능력과 요구사항을 제품으로 전환한 경험이 중요합니다. 미국 하이브리드 근무가 가능한지와 취업비자 지원 여부도 먼저 확인해야 합니다.

**지원 전 준비**

- 문서 기반 RAG 또는 에이전트 시스템을 FastAPI로 배포
- 검색 정확도, 답변 정확도, latency, 비용을 정량 평가
- 실패 사례와 개선 과정을 영어 README로 정리
- “연구 문제를 실제 사용 가능한 시스템으로 바꾼 경험” 중심으로 석사 연구와 ML 프로젝트를 연결

---

### 2. NVIDIA — Deep Learning Software Engineer, Inference  
**New College Grad 2026**

**기술 적합도: 9.7/10 · 지원 자격 확인 후 최우선 도전**

- **근무지:** 미국 캘리포니아·텍사스·뉴욕·워싱턴 등 원격 근무지
- **고용 형태:** 정규직·풀타임
- **대상:** 관련 분야 석사·박사 재학 또는 최근 졸업자, 이에 준하는 경험
- **게시일:** **2026년 7월 29일로 표시**
- **마감:** 별도 기한 미표기
- **지원:** NVIDIA 공식 채용 공고 citeturn769681search0turn311441search0

GPU 가속 추론·모델 서빙 소프트웨어를 개발하고 LLM을 포함한 딥러닝 모델의 성능을 분석·최적화합니다. 특히 **PyTorch, vLLM, SGLang** 같은 오픈소스 프로젝트에 직접 기여하는 업무가 명시돼 있어 사용자의 관심 기술과 매우 정확하게 일치합니다. citeturn237166search0turn787311search1

**잘 맞는 이유**

현재 진행하려는 B200 다중 GPU, vLLM 서빙, tensor parallelism, latency·throughput 벤치마크가 사실상 이 직무의 사전 포트폴리오에 해당합니다. 모델을 단순 실행하는 수준보다 GPU 메모리와 병목을 분석하고 재현 가능한 실험으로 기록하려는 방향도 강점입니다.

**부족할 수 있는 부분**

`New College Grad 2026` 조건이 가장 큰 위험입니다. 사용자의 석사 졸업 시점이 2019년이므로, “recently completed” 또는 동등 경력 조건에 포함되는지를 채용팀에 확인한 뒤 지원하는 편이 안전합니다. C++·CUDA와 오픈소스 코드베이스 기여 경험도 추가로 요구될 가능성이 높습니다.

**지원 전 준비**

- 동일 모델을 vLLM·SGLang·Transformers로 각각 서빙
- 1·2·4 GPU의 TTFT, TPOT, tokens/s, VRAM 비교
- prefix caching·speculative decoding·quantization 중 두 가지 적용
- 성능 회귀를 확인하는 `pytest` 벤치마크 작성
- vLLM 또는 SGLang에 이슈 분석, 문서 수정, 작은 PR 중 하나 제출

---

### 3. NVIDIA — Deep Learning Software Engineer, TensorRT Performance  
**New College Grad 2026**

**기술 적합도: 9.1/10 · ML 인프라·최적화 지향 도전 지원**

- **근무지:** 미국 산타클라라 또는 캘리포니아 원격
- **고용 형태:** 정규직·풀타임
- **대상:** 학사·석사·박사 또는 이에 준하는 경험
- **게시일:** **2026년 7월 25일경**
- **마감:** 별도 기한 미표기
- **지원:** NVIDIA 공식 채용 공고 citeturn769681search2turn311441search1

NVIDIA 추론 생태계의 성능을 분석하고 개선하는 역할입니다. C++와 Python 소프트웨어 엔지니어링 능력, PyTorch·JAX·TensorFlow·ONNX 같은 프레임워크 및 추론 라이브러리 경험을 요구합니다. citeturn939307search1turn237166search2

**잘 맞는 이유**

모델 튜닝뿐 아니라 ONNX·TensorRT 변환, GPU 프로파일링, latency·메모리 최적화까지 다루므로 장기 목표인 ML 인프라 엔지니어링에 매우 가깝습니다. B200 환경을 사용할 수 있는 현재 시점에 관련 실험을 만들면 차별화된 포트폴리오가 될 수 있습니다.

**부족할 수 있는 부분**

C++ 역량과 CUDA 커널·TensorRT 내부 동작에 대한 이해가 핵심 간극입니다. 이 직무 역시 신입 졸업자 트랙이므로 졸업 시점 관련 자격을 먼저 확인해야 합니다.

**지원 전 준비**

- PyTorch 모델을 ONNX와 TensorRT 엔진으로 변환
- FP32·FP16·INT8별 정확도, latency, throughput, VRAM 비교
- Nsight Systems와 PyTorch Profiler로 CPU·GPU 병목 분석
- dynamic batching과 입력 shape 변화에 따른 성능 측정
- 결과를 재현 가능한 Docker 환경과 기술 보고서로 공개

## 이번 지원 우선순위

**Brain Co. → NVIDIA Inference → NVIDIA TensorRT Performance**

Brain Co.는 경력 조건이 **0~2년**으로 명확해 현재 가장 현실적입니다. NVIDIA 두 공고는 기술적으로는 거의 최상급 적합도를 보이지만, **2026 New College Grad 지원 자격을 확인한 후** 포트폴리오 준비 시간을 투입하는 것이 좋습니다.

---

### 💡 답변 (Assistant)
## 새로 확인된 고적합 공고 — 2026년 7월 31일

기존에 안내한 Upstage·Anlatan·Modal·ENERZAi·Perplexity·42dot·Brain Co.·NVIDIA 공고는 제외했습니다. 이번에는 **Nota AI의 신규 ML 최적화 인턴 2건**이 확인됐습니다.

### 1. Nota AI — NetsPresso Quantization Engineer Intern

**종합 적합도: 9.4/10 · 이번 회차 최우선 지원 권장**

- **근무지:** 서울 강남구 파르나스타워
- **근무 형태:** 대면 중심
- **고용 형태:** 체험형 인턴
- **근무 기간:** 6개월, 이후 협의 가능
- **요구 경력:** 석·박사 졸업자·졸업예정자 또는 학사 후 관련 경력 2년 이상
- **게시·접수 시작:** **2026년 7월 29~30일**로 채널별 표기 차이
- **마감:** 채용 시 마감
- **지원:** Nota AI 공식 채용 페이지 연결 공고 citeturn457116view0turn457116view1

PTQ·QAT·모델 압축 알고리즘을 연구하고, LLM·VLM·Diffusion 모델을 실제 하드웨어에서 가속하기 위한 양자화 파이프라인을 설계하는 포지션입니다. PyTorch·ExecuTorch·ONNX 이해를 요구하며, TensorRT·AIMET·llama.cpp·vLLM·SGLang 활용 경험과 오픈소스 기여를 우대합니다. citeturn457116view0turn457116view1

**잘 맞는 이유**

현재 사용 가능한 B200 다중 GPU 환경, PyTorch·Linux 경험, vLLM 기반 로컬 서빙 계획, 모델 성능을 latency·throughput·VRAM 관점에서 비교하려는 방향이 직무와 매우 가깝습니다. 석사 과정의 수치분석·실험 설계 경험도 양자화 전후의 정확도 저하 원인을 분석하고 실험 결과를 설명하는 역량으로 연결할 수 있습니다.

**부족할 수 있는 부분**

가장 큰 간극은 전공이 컴퓨터공학·전자공학 계열이 아니라는 점과, PTQ·QAT 또는 ONNX·TensorRT 기반 최적화 결과가 아직 포트폴리오에 명확히 드러나지 않는다는 점입니다. 공고는 양자화나 모델 압축 분야의 실질적 연구·개발 경험을 요구합니다. citeturn457116view1

**지원 전 준비**

- 공개 7B급 언어 모델에 FP16·INT8·INT4 양자화를 각각 적용
- 정확도 또는 perplexity, TTFT, TPOT, tokens/s, VRAM을 동일 조건으로 비교
- vLLM과 llama.cpp 또는 ONNX Runtime 중 두 개 이상의 런타임 비교
- 양자화 후 성능이 크게 저하되는 레이어나 태스크의 원인 분석
- 실행 명령어·환경 파일·원시 결과가 포함된 GitHub 저장소 공개
- 결과를 3~4페이지 분량의 기술 보고서로 정리

---

### 2. Nota AI — NetsPresso AI Research Engineer Intern

**종합 적합도: 8.7/10 · 기술적으로 매우 적합하지만 도전적**

- **근무지:** 서울 강남구 파르나스타워
- **근무 형태:** 대면 중심
- **고용 형태:** 체험형 인턴
- **근무 기간:** 6개월
- **경력 표기:** 경력 무관
- **게시·접수 시작:** **2026년 7월 24일**
- **마감:** 채용 시 마감
- **지원:** Nota AI 공식 채용 페이지 citeturn778955search0turn235891view0

업스테이지 컨소시엄에서 개발하는 LLM·VLM 파운데이션 모델의 경량화와 추론 최적화를 담당합니다. MoE 양자화·프루닝, TensorRT-LLM·vLLM·SGLang·ONNX Runtime, CUDA·Triton 커널, KV-cache 최적화, continuous batching, speculative decoding, GPU·NPU별 latency·throughput·memory 평가가 주요 업무입니다. citeturn235891view0

**잘 맞는 이유**

사용자가 현재 구상 중인 **B200 멀티 GPU 기반 대형 모델 서빙·파인튜닝·벤치마킹 프로젝트**와 업무 범위가 거의 그대로 겹칩니다. 모델을 단순 실행하는 것이 아니라 하드웨어 특성, 메모리, 추론 프레임워크, 병목을 함께 분석하는 포지션이라는 점에서 ML 인프라 장기 목표와도 매우 잘 맞습니다.

**부족할 수 있는 부분**

공고상 경력은 무관이지만 실제 기술 기준은 높습니다. 관련 분야 석사 또는 동등한 연구 역량과 함께, MoE 양자화·프루닝·추론 최적화를 프로젝트에 즉시 적용할 수 있는 수준을 요구합니다. CUDA·Triton, NPU SDK, custom operator, top-tier 논문·오픈소스 실적도 우대 요소입니다. citeturn235891view0

**지원 전 준비**

- 공개 MoE 모델 하나를 선정해 FP16과 저비트 양자화 결과 비교
- vLLM에서 tensor parallel 설정별 throughput·메모리·통신 병목 측정
- prefix caching 또는 speculative decoding을 적용한 전후 비교
- PyTorch Profiler나 Nsight Systems로 병목 구간 시각화
- OOM·NCCL·지원되지 않는 연산자 문제를 해결한 과정을 기술 문서로 기록
- 최신 MoE 양자화 논문 한 편을 선정해 핵심 알고리즘과 재현 결과 정리

## 지원 우선순위

**Quantization Engineer Intern → AI Research Engineer Intern**

첫 번째 포지션은 양자화 실험과 모델 최적화 프로젝트를 빠르게 보강하면 지원 논리를 만들 수 있습니다. 두 번째 포지션은 기술 방향은 가장 잘 맞지만, MoE·CUDA/Triton·추론 프레임워크 수준의 실증 결과가 필요해 도전 지원에 가깝습니다.

이번 글로벌 검색에서는 기술적으로 관련된 후보들이 있었지만, **박사과정 재학생 필수** 또는 **프로덕션 ML 경력 8년 이상** 조건인 공고는 현재 지원 적합도가 낮아 제외했습니다. citeturn778955search9turn197701view0

---

### 💡 답변 (Assistant)
## 새로 확인된 고적합 공고 — 2026년 8월 1일

이전에 안내한 공고는 제외했습니다. 이번에는 **국내 신입 포지션 1건과 글로벌 초기 경력 포지션 1건**이 확인됐습니다.

### 1. 마키나락스 — Forward Deployed Engineer, LLM 신입

**적합도: 9.3/10 · 현재 가장 현실적인 지원 후보**

- **근무지:** 서울
- **고용 형태:** 정규직
- **경력:** 신입
- **마감:** 공식 페이지에 별도 기한 미표기, 2026년 8월 1일 현재 지원 페이지 활성
- **지원:** 마키나락스 공식 채용 공고 citeturn268547search0turn268547search2

산업 현장의 문제를 정의하고 LLM·VLM을 활용해 지능형 분석과 자동화 시스템을 만드는 역할입니다. 주요 업무에는 AI Agent 개발, RAG와 fine-tuning을 통한 모델 성능 개선, 산업 데이터 분석, 실제 적용 사례 확대가 포함됩니다. Python 능력과 최신 AI·LLM 연구 동향에 대한 이해를 요구하며, LLM 학습·평가, RAG 파이프라인 평가, 데이터 파이프라인, 코드 리뷰 경험을 우대합니다. citeturn268547search0turn268547search2

**잘 맞는 이유**

사용자의 Python·PyTorch·Hugging Face 경험, 논문과 최신 기술을 지속적으로 학습하는 습관, LLM 서빙·파인튜닝·에이전트 개발 관심을 직접 활용할 수 있습니다. 목재물리 연구에서 실제 데이터를 분석하고 문제를 수치적으로 정의한 경험도 **도메인 문제 정의 → 데이터 분석 → 모델 적용**이라는 FDE 업무 흐름과 연결하기 좋습니다.

특히 이 포지션은 특정 알고리즘 연구 실적보다, 다양한 도메인의 문제를 이해하고 LLM 기술을 실제 시스템으로 구현하는 능력을 중시합니다. 순수 NLP 연구직보다 현재 경력을 설득력 있게 전환하기 쉬운 포지션입니다.

**부족할 수 있는 부분**

- 실제 사용자를 대상으로 운영한 RAG·Agent 시스템 사례
- LLM 평가 지표와 회귀 테스트를 자동화한 경험
- 고객 또는 현업 담당자의 모호한 요구사항을 기술 문제로 구조화한 사례
- Docker·API·배포·모니터링을 포함한 프로덕션 수준 프로젝트

**지원 전 준비**

공지문·기술문서·연구자료를 입력받아 행동 항목을 추출하는 에이전트를 포트폴리오로 구성하는 것이 좋습니다. 이전에 구상한 **공지 → 행동카드 변환 에이전트**를 활용하면 직무 연관성이 높습니다.

구체적으로는 다음 결과가 필요합니다.

1. 문서 수집과 청킹, embedding, retrieval 파이프라인
2. 해야 할 일·담당자·기한·우선순위 구조화
3. 변경된 공지를 입력했을 때 기존 카드 업데이트
4. 추출 정확도·누락률·hallucination 평가
5. FastAPI와 Docker 기반 실행 환경
6. 실패 사례와 개선 내용을 포함한 README

외부 채용 플랫폼에는 과거 **2026년 7월 21일 마감**으로 표시된 기록도 있지만, 회사 공식 지원 페이지는 현재 활성 상태입니다. 재공고 또는 상시채용 전환 가능성이 있으므로 공식 페이지를 기준으로 빠르게 지원하는 편이 안전합니다. citeturn268547search0turn268547search3

---

### 2. Nuance Labs — Member of Technical Staff, Model Optimization and Inference (New Grad)

**기술 적합도: 9.6/10 · 자격 조건 확인이 필요한 도전 지원**

- **근무지:** 미국 워싱턴주 시애틀
- **근무 방식:** 주 5일 대면
- **고용 형태:** 정규직
- **대상:** 학사·석사·박사 졸업 예정자 또는 최근 졸업자
- **게시:** 약 1개월 전
- **마감:** 별도 기한 미표기, 2026년 8월 1일 현재 공식 페이지 활성
- **비자:** O-1·H-1B·영주권 스폰서십 명시
- **지원:** Nuance Labs 공식 채용 공고 citeturn927636view0turn563517search0

LLM·음성·Diffusion 모델의 end-to-end 추론 최적화, KV-cache 압축과 eviction, memory-efficient attention, batching, 양자화, latency·throughput 프로파일링을 담당합니다. vLLM·SGLang·TensorRT-LLM 경험을 연구·개인 프로젝트 수준에서도 인정하며, Python·PyTorch를 핵심 요건으로 두고 CUDA·Triton과 오픈소스 기여를 우대합니다. citeturn927636view0

**잘 맞는 이유**

사용자가 계획한 B200 멀티 GPU 실험, vLLM 서빙, tensor parallelism, quantization, TTFT·TPOT·throughput·VRAM 벤치마킹이 공고 업무와 거의 일치합니다. 프로덕션 경험이 없어도 연구나 개인 프로젝트 수준의 vLLM·SGLang 경험을 인정한다고 명시한 점도 유리합니다. citeturn927636view0

**가장 큰 위험**

공고는 CS·ML 관련 학위의 졸업 예정자 또는 최근 졸업자를 대상으로 합니다. 사용자의 석사 졸업 시점이 2019년이고 전공도 목재물리이므로, 형식적인 New Grad 기준에서는 불리할 가능성이 큽니다. 다만 공고가 학위보다 시스템 직관과 기술 역량을 강조하므로, 강한 추론 최적화 프로젝트가 있다면 도전 지원 가치는 있습니다. citeturn927636view0

**지원 전 준비**

- 동일 LLM을 Transformers·vLLM·SGLang으로 서빙
- 1·2·4 GPU에서 TTFT, TPOT, tokens/s, p95 latency 측정
- FP16·AWQ·GPTQ 또는 INT8·INT4 결과 비교
- prefix caching, continuous batching, speculative decoding 중 최소 1개 실험
- PyTorch Profiler 또는 Nsight Systems 병목 분석
- 성능 회귀를 탐지하는 `pytest` 벤치마크
- vLLM·SGLang의 문서 수정, 이슈 재현 또는 소규모 PR

## 지원 우선순위

**마키나락스 신입 FDE–LLM → Nuance Labs Model Optimization**

마키나락스는 신입 조건과 사용자의 현재 경험을 함께 고려했을 때 즉시 지원할 가치가 높습니다. Nuance Labs는 기술 방향은 거의 완벽하게 맞지만, 졸업 시점과 전공 조건 때문에 **B200·vLLM 벤치마크 포트폴리오를 완성한 뒤 제출하는 도전 카드**로 보는 것이 적절합니다.

---

### 💡 답변 (Assistant)
## 새로 확인된 고적합 공고 — 2026년 8월 2일

기존에 안내한 Upstage·Anlatan·Modal·ENERZAi·Perplexity·42dot·NVIDIA·Nota AI·마키나락스 등의 공고는 제외했습니다. 이번에는 **국내 신규·재게시 공고 3건**을 선별했습니다.

### 1. 토스 — AI Engineer (Model)

**적합도: 9.4/10 · 이번 회차 최우선 지원 후보**

- **근무지:** 서울
- **고용 형태:** 정규직
- **요구 경력:** 연차 기준 미표기, LLM/VLM 모델을 직접 학습하고 개선한 경험 요구
- **게시 시점:** LinkedIn 기준 약 2주 전
- **마감:** 별도 기한 미표기, 2026년 8월 2일 현재 공식 지원 페이지 활성
- **지원:** 토스 공식 채용 공고 citeturn697024view3turn843240search0

실제 서비스 데이터를 이용한 학습 데이터 구축부터 post-training, continual learning, 성능·비용·latency를 고려한 학습 전략, 사내·범용 benchmark 구축까지 담당합니다. DeepSpeed·FSDP·Megatron 기반 분산 학습, synthetic-data 파이프라인, LLM 평가 자동화, Transformers·vLLM 오픈소스 기여 경험을 우대합니다. citeturn697024view3

**잘 맞는 이유**

사용자가 계획 중인 B200 다중 GPU 실험, Hugging Face 기반 모델 튜닝, vLLM 서빙, 정량 벤치마크와 거의 정확히 연결됩니다. 석사 연구에서 수행한 가설 설정·수치분석·반복 실험도 이 공고가 강조하는 **가설 → 실험 → 결과 분석 → 개선** 사이클로 설명하기 좋습니다.

**부족할 수 있는 부분**

- 데이터 생성부터 학습·평가까지 완결한 LLM 프로젝트
- SFT·DPO·RL·LoRA·양자화 간 선택 근거와 비교 실험
- DeepSpeed·FSDP 기반 분산 학습 결과
- 오픈소스 이슈 해결 또는 PR 기록

**지원 전 준비**

7B~14B 한국어 모델 하나를 선정해 `Base → SFT → DPO`를 수행하고, 태스크 성능과 학습 비용을 비교하는 프로젝트가 가장 효과적입니다. 1·2·4 GPU별 tokens/s, VRAM, 학습 시간과 OOM·NCCL 문제 해결 과정까지 기록해야 합니다. 평가에는 범용 benchmark와 직접 만든 도메인 benchmark를 함께 사용하고, vLLM 배포 결과도 추가하는 것이 좋습니다.

---

### 2. 토스증권 — ML Engineer (LLM)

**적합도: 9.0/10 · NLP 엔지니어 전환에 가장 현실적인 후보**

- **근무지:** 서울
- **고용 형태:** 정규직
- **요구 경력:** 연차 기준 미표기, LLM/NLP 모델 개발·운영 경험 요구
- **최근 노출:** LinkedIn 기준 **2026년 8월 1일경**
- **마감:** 별도 기한 미표기, 공식 페이지에서 현재 지원 가능
- **지원:** 토스증권 공식 채용 공고 citeturn697024view4turn843240search2

분류·정보 추출·요약·번역 모델을 직접 학습하고, fine-tuning·실험 설계·평가·서빙·모니터링까지 담당합니다. 뉴스와 공시를 이용한 종목 매칭·산업 분류·중요도 판별, 다국어 번역과 임베딩 모델도 업무에 포함됩니다. citeturn697024view4

**잘 맞는 이유**

Python·PyTorch·Hugging Face 경험을 가장 직접적으로 보여줄 수 있는 전형적인 NLP/LLM 엔지니어 직무입니다. 토스의 모델 포지션보다 분산 학습이나 대규모 post-training 요구가 낮고, 문제 정의·데이터 구축·모델 학습·운영의 전체 흐름을 강조하므로 현재 경력 전환 단계에서는 오히려 지원 논리를 만들기 쉽습니다.

**부족할 수 있는 부분**

- 실제 서비스에서 운영한 NLP 모델
- 금융·증권 텍스트와 다국어 데이터 경험
- 데이터 분포 변화나 모델 성능 저하를 감지한 경험
- 모델 성능을 제품 지표와 연결한 사례

**지원 전 준비**

한국거래소 공시나 공개 금융 뉴스를 이용해 다음 파이프라인을 구현하는 것이 좋습니다.

1. 종목·산업 분류 및 핵심 정보 추출
2. 한국어·영어 뉴스 요약 또는 번역
3. Hugging Face 모델 fine-tuning
4. F1, ROUGE, BERTScore와 오류 유형 평가
5. FastAPI·Docker 기반 서빙
6. 데이터 변화와 성능 저하를 감지하는 모니터링

모델 정확도뿐 아니라 **사용자가 정보를 찾는 시간이나 잘못된 분류가 얼마나 감소했는지**를 지표로 제시하면 강해집니다.

---

### 3. FuriosaAI — Machine Learning Engineer (Agentic AI)

**적합도: 8.8/10 · 기술적으로 강하게 맞는 도전 지원**

- **근무지:** 서울 HQ
- **근무 방식:** 하이브리드
- **고용 형태:** 정규직·풀타임
- **요구 경력:** 연차 기준 미표기
- **최근 노출:** LinkedIn 기준 **2026년 7월 30일경**
- **마감:** 별도 기한 미표기, 공식 페이지에서 현재 지원 가능
- **지원:** FuriosaAI 공식 채용 공고 citeturn611360search0turn180825search2

Planning·tool use·memory·reasoning·self-improvement를 포함하는 agent behavior, multi-agent orchestration, 자동 실행·검증·평가 시스템, LLM-as-a-Judge와 benchmark, SFT·RL 기반 post-training을 연구하고 구현합니다. 최신 논문을 빠르게 이해해 실제 시스템으로 옮기는 능력을 기본 요건으로 명시합니다. citeturn697024view2

**잘 맞는 이유**

최근 구상한 **공지 → 행동카드 에이전트**, 에이전트 평가와 최신 논문 학습에 대한 관심, PyTorch 기반 실험 경험이 직무 방향과 잘 맞습니다. 단순 API wrapper가 아니라 실행 결과를 평가하고 스스로 개선하는 시스템을 만든다는 점도 사용자의 에이전트 개발 목표와 연결됩니다.

**가장 큰 위험**

공고는 컴퓨터공학 또는 유관 분야 학사 학위를 기본 요건으로 둡니다. 사용자의 석사 전공이 목재물리이므로 형식적인 전공 요건에서 불리할 수 있습니다. 이를 상쇄하려면 학위보다 강한 **agent 구현·평가·post-training 결과**가 필요합니다. citeturn697024view2

**지원 전 준비**

기존 공지 행동카드 아이디어를 다음 구조로 고도화하는 것이 가장 적합합니다.

- 공지 분석·계획·도구 실행·검증을 담당하는 다중 agent
- 변경 공지 입력 시 기존 카드와 충돌 탐지
- 추출 정확도, tool-selection accuracy, 완료율, hallucination rate 평가
- LLM-as-a-Judge와 규칙 기반 평가의 상관관계 비교
- 실패 trajectory 저장 및 재시도 전략
- LangGraph 또는 Google ADK 기반 구현
- 작은 SFT 또는 preference optimization 실험

## 지원 우선순위

**토스 AI Engineer (Model) → 토스증권 ML Engineer (LLM) → FuriosaAI Agentic AI**

토스 AI Engineer는 기술 적합도가 가장 높고, 토스증권은 현재 경력에서 가장 현실적인 NLP 전환 경로입니다. FuriosaAI는 방향은 매우 잘 맞지만 전공 요건 때문에, 완성도 높은 에이전트 평가 프로젝트를 갖춘 뒤 도전 지원하는 전략이 적절합니다.

---

### 💡 답변 (Assistant)
## 새로 확인된 고적합 공고 — 2026년 8월 3일

기존에 안내한 **토스 AI Engineer (Model)** 및 토스증권 **ML Engineer (LLM)**은 제외했습니다. 이번에는 2026년 8월 2일 전후 LinkedIn에 새롭게 노출된 **ML·LLM 플랫폼 공고 3건**을 확인했습니다. 공식 채용 페이지도 현재 지원 가능한 상태입니다. citeturn601937search5turn601937search11turn601937search12

### 1. 토스뱅크 — ML Engineer (ML/LLM Ops)

**기술 적합도: 9.7/10 · 현재 방향과 가장 정확히 일치**

- **근무지:** 서울
- **고용 형태:** 정규직
- **요구 경력:** 연차 기준 미표기
- **최근 노출:** 2026년 8월 2일 전후
- **마감:** 별도 기한 미표기
- **지원:** 토스뱅크 공식 채용 페이지 citeturn601937search2turn154976view0

ML 모델과 LLM의 **학습·검증·배포·서빙·모니터링 전 과정**을 플랫폼화하는 역할입니다. MLflow, Airflow, JupyterHub, Kubeflow, Triton Inference Server, vLLM, SGLang, TensorRT-LLM, Vector Database를 활용하며, 온프레미스와 AWS·GCP가 결합된 하이브리드 GPU 인프라도 다룹니다. citeturn154976view0

**잘 맞는 이유**

사용자가 현재 다루는 B200 GPU 환경, Linux, PyTorch, vLLM 서빙, 다중 GPU 벤치마크 경험을 하나의 직무에서 모두 활용할 수 있습니다. 특히 모델 자체보다 **GPU 워크로드의 성능·가용성·비용을 측정하고 개선하는 역할**이라는 점에서 장기 목표인 ML 인프라와 가장 가깝습니다.

**부족할 수 있는 부분**

- Kubernetes 기반 서비스 배포·운영 경험
- AWS·GCP 및 EKS·GKE 경험
- Terraform·Helm·Argo CD 기반 배포 자동화
- Prometheus·Grafana·OpenTelemetry 관측 환경
- 실제 서비스 수준의 장애 대응과 가용성 설계

연차 제한은 없지만 요구되는 운영 범위가 넓어, 실질적으로는 **프로덕션 경험을 가진 지원자가 유리한 공고**입니다. citeturn154976view0

**지원 전 준비**

B200 서버에서 다음 구조의 소형 LLMOps 플랫폼을 구축하는 것이 가장 효과적입니다.

1. vLLM 또는 SGLang 모델 서버
2. FastAPI 기반 LLM Gateway
3. Prometheus·Grafana 기반 TTFT, TPOT, tokens/s, GPU 사용률 관측
4. MLflow 실험 추적
5. Kubernetes·Helm 기반 배포
6. 부하 증가 시 replica 확장 또는 장애 시 fallback
7. 운영 중 발생한 OOM·NCCL·latency 문제와 해결 과정 기록

이력서에는 기술 목록보다 **처리량, 지연 시간, GPU 활용률, 비용, 장애율이 얼마나 개선됐는지**를 숫자로 적는 것이 중요합니다.

---

### 2. 토스증권 — ML Engineer (Platform)

**기술 적합도: 9.3/10 · LLM 서빙과 백엔드를 연결하는 현실적 후보**

- **근무지:** 서울
- **고용 형태:** 정규직
- **요구 경력:** 연차 기준 미표기, 프로덕션 API·서빙 경험 요구
- **최근 노출:** 2026년 8월 2일 전후
- **마감:** 별도 기한 미표기
- **지원:** 토스증권 공식 채용 페이지 citeturn601937search5turn154976view2

FastAPI 기반 LLM API Gateway, 인증·라우팅·트래픽 제어·Circuit Breaker·Fallback을 개발하며, Kubernetes에서 vLLM·SGLang·Triton 모델 서버를 운영합니다. H100·B300 GPU 클러스터와 Kubeflow 기반 공통 ML 플랫폼도 업무 범위에 포함됩니다. citeturn154976view2

**잘 맞는 이유**

Python, FastAPI, Linux, LLM 서빙을 모두 활용할 수 있으며, 모델 연구보다 **모델을 안정적인 서비스로 만드는 엔지니어링**에 가깝습니다. 사용자가 그동안 겪은 SSH, CUDA, Jupyter kernel crash, GPU 메모리, 로컬 LLM API 문제들도 장애 분석 경험으로 재구성할 수 있습니다.

**부족할 수 있는 부분**

- 대규모 요청을 처리하는 API 서버 운영
- Nginx·Kong·LiteLLM·Envoy AI Gateway 경험
- Kafka·Elasticsearch 기반 로그 파이프라인
- Prometheus·Grafana 모델 서빙 대시보드
- Circuit Breaker, rate limiting, fallback 설계

공고는 Python을 인정하지만 단순 FastAPI 구현을 넘어 **대용량 트래픽과 장애 격리 경험**을 요구합니다. citeturn154976view2

**지원 전 준비**

두 개의 서로 다른 모델 서버를 대상으로 하는 LLM Gateway를 구현하는 것이 좋습니다.

- vLLM 서버 2개에 weighted routing
- 요청별 timeout·retry·fallback
- 동시 요청 제한과 rate limiting
- p50·p95·p99 latency 측정
- 모델 서버 장애 시 자동 우회
- Prometheus·Grafana 모니터링
- Locust 또는 k6 부하 테스트
- Docker Compose 버전과 Kubernetes 버전 모두 제공

현재 경험을 가장 빠르게 실무형 포트폴리오로 변환할 수 있는 공고입니다.

---

### 3. 토스증권 — ML Engineer (Infra)

**기술 적합도: 9.8/10 · 현재 지원은 도전적, 장기 목표로는 최상**

- **근무지:** 서울
- **고용 형태:** 정규직
- **요구 경력:** 연차 기준 미표기, 대규모 Kubernetes ML 인프라 운영 경험 필수
- **최근 노출:** 2026년 8월 2일 전후
- **마감:** 별도 기한 미표기
- **지원:** 토스증권 공식 채용 페이지 citeturn601937search12turn154976view1

InfiniBand로 연결된 H100·B300 GPU 클러스터와 400Gbps급 스토리지를 Kubernetes에서 운영합니다. GPU 자원 할당·자동 확장·통합 관측, Nsight와 PyTorch Profiler 기반 병목 분석, MIG·MPS 활용률 최적화가 핵심 업무입니다. 기술 스택에는 Python, Kubernetes, Kubeflow, Argo CD, Helm, vLLM, SGLang, Prometheus, Grafana, DCGM과 Nsight가 명시돼 있습니다. citeturn154976view1

**잘 맞는 이유**

현재 B200 다중 GPU를 직접 다루고 있고, GPU를 최대한 활용하며 학습·서빙 감각을 익히려는 목표와 업무 자체는 거의 완벽하게 일치합니다. 특히 GPU·CPU·메모리·네트워크·스토리지 병목을 함께 분석하는 역할은 사용자가 지향하는 ML 시스템 엔지니어의 정점에 가깝습니다.

**가장 큰 간극**

- 대규모 Kubernetes 클러스터 운영
- InfiniBand·NVLink·고성능 스토리지 튜닝
- 라이브 서비스 장애 대응
- GPU quota·스케줄링·멀티테넌시
- MIG·MPS 및 DCGM 기반 GPU 관측
- 오픈소스 플랫폼 내부 코드 수정 경험

이 공고는 연차를 명시하지 않았지만, 요구사항상 **즉시 전력 수준의 인프라 엔지니어**를 찾는 것으로 판단됩니다. citeturn154976view1

**지원 전 준비**

현재 B200 환경에서 다음 실험을 남기면 장기적으로 강한 포트폴리오가 됩니다.

- 1·2·4 GPU tensor parallel 성능 비교
- NCCL topology와 통신량 분석
- 데이터 로딩·스토리지 병목 측정
- Nsight Systems와 PyTorch Profiler 결과 비교
- DCGM Exporter 기반 GPU 관측
- GPU utilization이 낮아지는 원인과 개선 결과
- MIG 또는 MPS를 활용한 다중 사용자 워크로드 실험
- OOM·NCCL timeout·GPU hang 대응 문서

## 이번 지원 우선순위

**토스뱅크 ML/LLM Ops → 토스증권 ML Platform → 토스증권 ML Infra**

세 공고 모두 기술 방향은 매우 잘 맞지만, 현재 합격 현실성은 **ML/LLM Ops와 ML Platform이 상대적으로 높습니다.** ML Infra는 지금 바로 지원해볼 수는 있으나, 대규모 Kubernetes 운영 경험이 핵심 간극이므로 장기 목표 공고로 관리하는 것이 적절합니다.

---
