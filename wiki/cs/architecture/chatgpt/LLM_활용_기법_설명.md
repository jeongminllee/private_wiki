---
type: Concept
title: "LLM 활용 기법 설명"
description: "CS - Software Architecture - ChatGPT 대화 추출 노트 (2025-05-08)"
tags: [cs, chatgpt-export]
timestamp: 2025-05-08
status: active
---

# LLM 활용 기법 설명

> **카테고리**: `CS - Software Architecture`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-05-08

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
이 주피터 노트북 파일에 대해서 설명해줘.

### 💡 답변 (Assistant)
이 노트북(`chapter-6-llm.ipynb`)은 총 40개의 셀로 구성되어 있으며, 크게 네 가지 LLM 활용 기법을 실습하고 설명하는 구조로 짜여 있습니다.

---

## 1. 환경 설정 및 라이브러리 임포트
- `pandas`, `torch`, `transformers`, `faiss-gpu` 등 주요 라이브러리 설치·임포트  
- GPU 상태 확인(`!nvidia-smi`, `torch.cuda.device_count()`) 및 경로 설정

## 2. 데이터 로딩
- Kaggle LLM Science Exam 데이터셋 불러오기  
  ```python
  df = pd.read_csv('/kaggle/input/kaggle-llm-science-exam/train.csv')
  ```

---

## 3. Zero-shot Prompting
- **설명**: 사전 예시(example) 없이 모델에게 곧바로 질문을 던지는 방식  
- **실습**  
  ```python
  messages = [{"role": "user", "content": "The key to life is"}]
  output = model.generate(**tokenized_input)
  ```  
- 기대 효과 및 한계 간단 정리

---

## 4. Chain-of-Thoughts (CoT) Prompting
- **설명**: 모델이 답을 도출하는 과정을 “생각의 흐름” 형태로 유도  
- **실습**  
  - 프롬프트에 “Let’s think step by step” 추가  
  - 출력된 중간 추론 과정 확인  

---

## 5. Retrieval Augmented Generation (RAG)
- **설명**: 외부 문서(지식 베이스)를 조회하여 컨텍스트로 활용  
- **실습**  
  1. **FAISS** 인덱스 생성:  
     ```python
     import faiss
     index = faiss.IndexFlatL2(embedding_dim)
     index.add(embeddings)
     ```  
  2. 검색(query) → 상위 k개 문서 추출  
  3. 추출된 문서를 LLM 입력에 함께 제공  

---

## 6. RAG + Parameter-Efficient Fine-Tuning (PEFT)
- **설명**: RAG 기반으로 가져온 정보에 더해, 저용량(few-parameter) 방식(예: LoRA)으로 모델을 미세조정  
- **실습**  
  1. `transformers`의 `peft` 모듈 설정  
  2. `LoRAConfig` 정의 후 `get_peft_model` 적용  
  3. 적은 리소스로도 추가 학습 수행  
  4. 성능 평가  

---

### 부가 정보
- 각 섹션마다 실험용 설정(`8-bit quantization`, `bs`, `max_length`)을 주석으로 남겨두어, 사용자가 손쉽게 하이퍼파라미터를 변경해볼 수 있습니다.
- RAG 부분에서는 실제 임베딩과 FAISS 인덱스를 구성하는 전체 워크플로우(데이터 전처리 → 벡터화 → 인덱싱 → 검색 → 생성)가 구현되어 있습니다.
- PEFT 섹션은 원본 모델 무게를 크게 늘리지 않으면서도 특정 도메인에 모델을 특화시키는 방법론을 다룹니다.

---

이 노트북은 LLM을 “단순 생성 → 사고 과정 유도 → 외부 지식 활용 → 경량 미세조정” 순으로 확장해가며, 각 단계의 이론과 코드를 함께 익힐 수 있게 설계되어 있습니다. 필요하신 부분(예: RAG 인덱싱 코드 상세 해설, LoRA 설정값 튜닝 팁 등)을 더 깊게 설명드릴 수도 있으니, 말씀해 주세요!

---

### 💡 답변 (Assistant)
이 메시지는 Hugging Face Transformers가 모델 체크포인트에서 기대하던 일부 파라미터(`lm_head.weight`)를 찾지 못해서, 그 부분만 랜덤 초기화했다는 경고입니다. 구체적으로는 다음과 같은 경우에 발생할 수 있어요:

1. **체크포인트에 ‘lm_head’ 가 빠져 있을 때**  
   - 예를 들어, 베이스 모델 가중치만 저장해 두고 마지막 언어 모델 헤드(`lm_head`) 부분은 저장하지 않았거나, 다른 이름으로 저장했을 경우입니다.  
   - 이 경우 `LlamaForCausalLM.from_pretrained(...)` 호출 시 ‘lm_head.weight’가 체크포인트에 없으니 새로 만들고 초기화합니다.

2. **토크나이저 사전(vocab) 크기와 모델 설정이 불일치할 때**  
   - 모델 설정(config)에서 `vocab_size`가 토크나이저에서 로드된 실제 어휘 수와 다르면, 출력 차원도 달라집니다.  
   - Transformers는 어휘 수에 맞게 `lm_head.weight`를 재생성한 뒤 랜덤 초기화합니다.

3. **아키텍처가 조금 다른 버전의 체크포인트를 불러왔을 때**  
   - 예컨대 “1b-instruct”용 체크포인트가 베이스 “1b” 모델과 토폴로지가 다른 경우, 헤드 부분만 달라질 수 있습니다.

---

### 해결 방법

- **올바른 체크포인트 경로 확인**  
  `from_pretrained()`에 지정한 폴더(또는 파일) 안에 `pytorch_model.bin`(또는 `.safetensors`)와 함께 `lm_head` 관련 가중치가 있는지 확인하세요.

- **토크나이저와 모델 설정 동기화**  
  ```python
  tokenizer = LlamaTokenizer.from_pretrained(checkpoint_path)
  model = LlamaForCausalLM.from_pretrained(
      checkpoint_path,
      vocab_size=tokenizer.vocab_size,     # 혹은 config.vocab_size와 일치시켜 줍니다.
      tie_word_embeddings=True              # 입력 임베딩과 lm_head를 묶을지 설정
  )
  ```
  이렇게 `vocab_size`를 토크나이저와 맞추면, lm_head를 새로 만들 필요가 없어집니다.

- **헤드만 별도로 로드하거나 재학습**  
  만약 정말로 새로 초기화된 헤드를 사용하고 싶지 않다면, 헤드 가중치도 포함된 전체 체크포인트(예: “finetuned” 모델)를 받아오시거나, 초기화된 헤드를 downstream task에서 몇 에포크 충분히 학습(fine-tune)해주세요.

---

> **정리**  
> 이 경고는 “체크포인트에는 베이스 모델 가중치만 있고, 마지막 출력 헤드(lm_head)의 가중치가 없어서 랜덤 초기화했습니다”라는 뜻이고, 학습된 헤드를 그대로 쓰려면 해당 파라미터가 저장된 올바른 체크포인트를 로드하거나 토크나이저·config를 일치시켜 주면 해결됩니다.

---

### ❓ 질문 (User)
Some weights of LlamaForCausalLM were not initialized from the model checkpoint at /kaggle/input/llama-3.2/transformers/1b-instruct/1 and are newly initialized: ['lm_head.weight']
이런 오류가 발생하는 이유에 대해서 설명해줘.

### 💡 답변 (Assistant)
이 에러 메시지는 PyTorch의 “meta” 디바이스를 사용하는 모델을 일반 디바이스(예: CUDA)로 옮기려고 할 때 발생하는 대표적인 문제입니다. 하나씩 뜯어보면:

1. **Meta Tensor란?**  
   - `torch.device("meta")`에 할당된 텐서는 실제 데이터(buffer)가 전혀 없는 “빈껍데기” 구조체입니다.  
   - 주로 모델의 구조(shape)만 빠르게 살펴보거나, 메모리를 최소화한 상태로 가중치를 로드하기 전에 템플릿만 생성할 때 사용합니다.

2. **왜 `.to()`가 안 되는가?**  
   - `model.to("cuda")`는 내부의 각 파라미터 텐서를 원래 저장돼 있던 장치에서 읽어와 새 디바이스로 복사하는 방식으로 동작합니다.  
   - 그런데 meta 텐서는 “읽을 데이터”가 전혀 없으므로, “메모리에서 꺼내 복사(copy out)”할 수가 없습니다.  
   - 그래서 “Cannot copy out of meta tensor; no data!”라는 에러가 나는 거죠.

3. **해법: `.to_empty()`**  
   - PyTorch 2.0+ 에서는 `torch.nn.Module.to_empty(device)` 메서드를 제공해서, meta로 되어 있는 모든 파라미터를 “빈 껍데기” 상태로 지정한 디바이스에 할당해 줍니다.  
   - 이렇게 하면 data가 없는 상태로라도 GPU 메모리에 텐서 틀이 만들어지기 때문에, 이후 체크포인트에서 실제 가중치를 채워 넣을 수 있습니다.

4. **실제 적용 예시**  
   ```python
   # 1) Meta로 모델 뼈대만 생성
   from transformers import LlamaForCausalLM, LlamaConfig
   config = LlamaConfig.from_pretrained(checkpoint_path)
   model = LlamaForCausalLM(config, device_map="meta")  # 메타 디바이스에만 생성됨

   # 2) meta → CUDA 빈 텐서로 이동
   model.to_empty("cuda:0")

   # 3) 체크포인트에서 실제 가중치 로드
   model.load_checkpoint_and_dispatch(
       checkpoint_path,
       device_map="auto",
       offload_folder="offload",
       no_split_module_classes=["LlamaDecoderLayer"]
   )
   ```
   위 3단계 워크플로우처럼, 먼저 `.to_empty()`로 “복사할 수 없는” meta 텐서를 GPU 빈 프레임으로 바꾸고, 그다음 가중치를 채워 넣도록 하면 에러가 사라집니다.

---

**정리하자면**,  
- “meta tensor”는 저장된 데이터가 없어서 `.to()`로 복사할 수 없고,  
- 대신 `.to_empty(target_device)`를 쓰면 같은 구조의 ‘빈’ 텐서를 지정 디바이스에 생성할 수 있습니다.  
- 그 후 체크포인트 로딩 함수를 호출해 실제 파라미터를 채워 넣으면 정상적으로 모델이 준비됩니다.

---

### ❓ 질문 (User)
NotImplementedError: Cannot copy out of meta tensor; no data! Please use torch.nn.Module.to_empty() instead of torch.nn.Module.to() when moving module from meta to a different device.
이 오류에 대해서 설명해줘

### 💡 답변 (Assistant)
아래 여섯 가지 섹션별로 조금 더 깊이 들어가 보겠습니다.

---

## 1. 환경 설정 및 라이브러리 임포트

1. **필수 패키지 설치**  
   - `transformers`, `datasets`, `accelerate`, `peft`(LoRA), `faiss-gpu` 등을 설치  
     ```bash
     pip install transformers datasets accelerate peft faiss-gpu
     ```
2. **GPU/메모리 확인**  
   - `!nvidia-smi` 로 GPU와 메모리 사용량 체크  
   - `torch.cuda.device_count()` 및 `torch.cuda.get_device_properties()` 로 디바이스 개수·스펙 확인
3. **Accelerate 설정**  
   - `accelerate config` 를 통해 분산 학습(멀티-GPU), 혼합 정밀도(8-bit, bf16) 옵션 설정  
   - 코드상에서는 `from accelerate import Accelerator` 로 감싸서 `accelerator.prepare(model, optimizer, dataloader)` 형태로 사용
4. **경로 및 시드 고정**  
   - 데이터·체크포인트 경로를 절대 또는 상대 경로로 깔끔히 관리  
   - `random.seed()`, `np.random.seed()`, `torch.manual_seed()` 로 재현성 확보  

---

## 2. 데이터 로딩

1. **데이터셋 구조 파악**  
   - Kaggle LLM Science Exam: `question`, `choices (A–D)`, `answer` 컬럼  
   - 훈련/검증 분할 비율(예: 80:20)로 분리
2. **Pandas vs. 🤗Datasets**  
   - 소규모 실험: `pandas.read_csv()` 로 바로 로딩  
   - 대규모·분산 처리:  
     ```python
     from datasets import load_dataset
     ds = load_dataset('csv', data_files={'train': train.csv, 'valid': valid.csv})
     ```
3. **토크나이저와 매핑**  
   - `LlamaTokenizer.from_pretrained(...)` 로 `tokenizer` 생성  
   - `map` 함수로 텍스트→토큰 ID 변환  
     ```python
     def preprocess(ex):
         return tokenizer(ex['question'], truncation=True, max_length=128)
     ds = ds.map(preprocess, batched=True)
     ```

---

## 3. Zero-shot Prompting

1. **개념**  
   - 사전 예시 없이 모델에 바로 태스크를 설명하고 정답을 유도  
   - 예) “Translate to French: ‘Hello, how are you?’”  
2. **구현 포인트**  
   - **컨텍스트 길이**: 너무 짧으면 모델이 의도를 파악 못 함  
   - **프롬프트 템플릿**:  
     ```text
     Task: Choose the best answer from A–D.
     Q: {question}
     A: (A) {choiceA}  (B) {choiceB}  (C) {choiceC}  (D) {choiceD}
     Answer:
     ```
   - **토크나이저 인수**: `return_tensors='pt', padding=True`
3. **장·단점**  
   - 장점: 추가 데이터 준비 불필요  
   - 단점: 낮은 정확도(모델이 태스크를 “학습”하지 않음)

---

## 4. Chain-of-Thoughts (CoT) Prompting

1. **개념**  
   - 모델이 답만 내놓지 않고, “생각의 흐름”을 글로 풀어가며 추론하도록 유도  
2. **프롬프트 예시**  
   ```text
   문제: {question}
   보 기:
     A. {choiceA}
     B. {choiceB}
     C. {choiceC}
     D. {choiceD}
   “Let’s think step by step” 형태로 지시 추가:
   “Please think step by step and then give the final answer.”
   ```
3. **효과**  
   - 복잡한 논리·수리 문제에서 유의미한 향상  
   - 다만 출력 길이가 길어지고, 후처리가 필요
4. **후처리**  
   - 모델 출력에서 마지막 줄(“정답: C”)만 추출하거나  
   - “###” 같은 구분자를 넣고 그 뒤를 파싱

---

## 5. Retrieval-Augmented Generation (RAG)

1. **워크플로우**  
   1. **지식 베이스 구축**  
      - 문장 단위 또는 문서 단위로 깨끗이 분절  
      - `transformers` 의 `AutoTokenizer` + `AutoModel` 으로 임베딩 생성  
   2. **벡터 인덱싱 (FAISS)**  
      ```python
      import faiss
      index = faiss.IndexFlatIP(emb_dim)      # 내적 유사도
      index.add(corpus_embeddings)
      ```
   3. **쿼리 단계**  
      - 사용 질문을 임베딩 → `index.search(query_emb, k=5)`  
      - 상위 k개 문서 추출
   4. **생성 입력에 추가**  
      - “Context:” 아래에 추출된 문서 붙이고, 그 뒤에 “Question:”  
      - 최종 prompt로 LLM 호출
2. **하이퍼파라미터**  
   - `k` (반환 문서 수): 보통 3~10 사이  
   - 임베딩 모델: 범용성 높은 `sentence-transformers` 권장
3. **주의점**  
   - 검색이 잘못되면 오히려 성능 저하  
   - 인덱스·임베딩 크기 관리 필요(메모리․속도 트레이드오프)

---

## 6. RAG + Parameter-Efficient Fine-Tuning (PEFT)

1. **PEFT 개요**  
   - 모델 전체를 미세조정하지 않고, 일부 매개변수(LoRA, Adapters, Prefix-Tuning)만 학습  
   - 저장·추론 효율성 극대화
2. **LoRA (Low-Rank Adapters)**  
   ```python
   from peft import LoraConfig, get_peft_model
   
   peft_config = LoraConfig(
       r=8,                   # 랭크
       lora_alpha=16,         # 스케일링
       target_modules=["q_proj","v_proj"],
       bias="none",
       task_type="CAUSAL_LM"
   )
   model = get_peft_model(model, peft_config)
   ```
3. **훈련 루프**  
   - `Trainer` 또는 `accelerator` 활용  
   - 옵티마이저: `AdamW`  
   - learning rate: 보통 1e–4 ~ 3e–4, warmup 100~500 step 사용  
4. **평가 & 저장**  
   - PEFT 전·후 성능 비교 (정답률, 생성 품질)  
   - `model.print_trainable_parameters()` 로 학습된 파라미터 비율 확인  
   - `save_pretrained()` 로 LoRA 어댑터만 저장하여 경량 배포  

---

이렇게 각 단계를 조금 더 세부적으로 파고들면, 간단한 제너레이션에서 출발해 외부 지식 활용과 효율적인 미세조정까지 일련의 전체 워크플로우를 한눈에 이해할 수 있습니다. 더 구체적인 코드 예시나 하이퍼파라미터 튜닝 팁이 필요하시면 언제든 알려 주세요!

---

### ❓ 질문 (User)
처음 질문에서 얘기해준 6가지 항목에 대해서 더 자세하게 설명해줘
