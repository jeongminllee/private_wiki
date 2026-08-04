---
type: Concept
title: "Wandb 경고 해결 방법"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-08-24)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-08-24
status: active
---

# Wandb 경고 해결 방법

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-08-24

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
좋은 소식: 이건 **에러가 아니라 경고(Warning)** 입니다.  
의미는 간단해요 — 현재 W&B에 기록되는 **실험 이름(`run_name`)** 이 **체크포인트 폴더(`TrainingArguments.output_dir`)** 와 **같은 문자열**로 설정되어 있어서, UI에서 이름이 경로처럼 보이거나 여러 실험이 뒤섞여 보일 수 있다는 알림이에요. 학습은 정상 진행됩니다.

# 해결 방법(원하는 방식 골라서 하나만 적용하세요)

### 1) `TrainingArguments.run_name`을 명시적으로 다르게 지정
```python
from transformers import TrainingArguments
from datetime import datetime

args = TrainingArguments(
    output_dir="./outputs/exp1",         # 체크포인트 저장 경로
    run_name=f"exp1-{datetime.now():%Y%m%d-%H%M%S}",  # W&B에서 보일 실험 이름
    report_to=["wandb"],                 # W&B로 로깅
    # ... 나머지 인자들
)
```

### 2) W&B 환경변수로 이름 지정
```python
import os
os.environ["WANDB_PROJECT"] = "my-project"
os.environ["WANDB_NAME"]    = "exp1-bert-bs16"
# 그런 다음 Trainer/TrainingArguments 사용
```

### 3) 직접 `wandb.init()`에서 이름 지정 (Hugging Face 콜백 쓰는 경우 비추지만 가능)
```python
import wandb
wandb.init(project="my-project", name="exp1-bert-bs16")
```

### 4) W&B를 쓰지 않을 때(완전히 끄기)
```python
import os
os.environ["WANDB_DISABLED"] = "true"
# 또는
args = TrainingArguments(..., report_to=[])  # W&B, TB 등 로깅 비활성화
```

> Kaggle에선 `output_dir`가 보통 `/kaggle/working/...` 같은 경로인데, 이게 그대로 실험 이름으로 뜨면 보기 불편해요. **`run_name`만 사람이 읽기 좋은 짧은 이름**으로 바꿔주면 경고가 사라지고, W&B 대시보드도 깔끔해집니다.

---

### ❓ 질문 (User)
나는 캐글에서 코드를 돌려보고 있어.
wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
이런 오류 메시지가 떴는데 무슨 에러 메시지인지 알려주고, 해결 방법을 알ㄹㅕ줘

### 💡 답변 (Assistant)
GPU가 안 도는 건 보통 아래 네 가지 중 하나예요.

1) 런타임이 CPU임(Kaggle 설정에서 GPU 미선택)  
2) PyTorch가 CUDA를 못 봄(버전/드라이버 불일치 등)  
3) Trainer 설정이 CPU로 강제됨(`no_cuda=True`)  
4) GPU는 보이지만 **데이터 적재가 느려** GPU가 놀고 있음(작은 배치/단일 워커/빈번한 평가·저장)

아래 순서대로 점검 + 수정해보세요.

---

## 0) 빠른 점검
노트북 맨 위에 한 번 찍어보세요.
```python
import torch, platform
print("CUDA available:", torch.cuda.is_available())
print("GPU count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU name:", torch.cuda.get_device_name(0))
```
- `CUDA available: True` 가 떠야 Trainer가 자동으로 GPU를 씁니다.  
- Kaggle에서 **Settings → Accelerator → GPU(T4)** 로 켜고 런타임 재시작 필수.

---

## 1) Trainer 설정을 “GPU 친화”로 바꾸기
- **혼동 주의**: `TrainingArguments`의 올바른 키는 `evaluation_strategy` 입니다. `eval_strategy`는 인식되지 않습니다.
- 혼합정밀(FP16/BF16), 데이터로더 워커, 핀 메모리를 켜서 **GPU 대기 시간을 줄이기**가 핵심입니다.

### 패치한 함수 예시
아래처럼 몇 줄만 추가/수정해 보세요(주석 달아둠).

```python
def load_trainer_for_train(model, news_train_dataset, news_val_dataset):
    """학습(train)을 위한 huggingface trainer 설정"""
    import os, math, torch
    from transformers import TrainingArguments, Trainer, EarlyStoppingCallback
    from transformers.optimization import get_cosine_with_hard_restarts_schedule_with_warmup

    # (선택) 안전하게 한 번 CUDA로 올려둠 — Trainer가 어차피 옮기지만 확인용
    if torch.cuda.is_available():
        model.to("cuda")

    # 혼합정밀 설정: A100/RTX30 계열이면 bf16, 그 외엔 fp16 권장
    use_bf16 = torch.cuda.is_available() and torch.cuda.get_device_capability(0)[0] >= 8
    use_fp16 = torch.cuda.is_available() and not use_bf16

    training_args = TrainingArguments(
        output_dir=os.path.join(args.save_path, "results"),
        save_total_limit=args.save_limit,
        save_steps=args.save_step,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=2,
        warmup_steps=args.warmup_steps,
        weight_decay=args.weight_decay,
        logging_dir=os.path.join(args.save_path, "logs"),
        logging_steps=args.logging_step,

        # ✅ 올바른 키 이름
        evaluation_strategy="steps",
        eval_steps=args.eval_step,
        load_best_model_at_end=True,

        # ✅ GPU 사용 보장 / 혼합정밀 / 데이터로더 튜닝
        no_cuda=not torch.cuda.is_available(),   # 기본은 False지만 명시
        fp16=use_fp16,
        bf16=use_bf16,
        dataloader_num_workers=max(2, (os.cpu_count() or 4) // 2),
        dataloader_pin_memory=True,
        gradient_accumulation_steps=getattr(args, "grad_accum_steps", 1),
    )

    # (선택) PyTorch 2.x + CUDA면 fused AdamW가 더 빠름
    try:
        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=args.lr, betas=(0.9, 0.999), eps=1e-08,
            weight_decay=args.weight_decay,
            fused=True,   # 지원 안 되면 except로
        )
    except TypeError:
        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=args.lr, betas=(0.9, 0.999), eps=1e-08,
            weight_decay=args.weight_decay,
        )

    # 총 스텝 정확히 계산(스케줄러에 중요)
    steps_per_epoch = math.ceil(len(news_train_dataset) / (args.batch_size * getattr(args, "grad_accum_steps", 1)))
    total_steps = steps_per_epoch * args.epochs

    scheduler = get_cosine_with_hard_restarts_schedule_with_warmup(
        optimizer,
        num_warmup_steps=args.warmup_steps,
        num_training_steps=total_steps,
    )

    MyCallback = EarlyStoppingCallback(early_stopping_patience=3, early_stopping_threshold=0.001)

    print("--- Set training arguments Done ---")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=news_train_dataset,
        eval_dataset=news_val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[MyCallback],
        optimizers=(optimizer, scheduler),
    )

    # 확인용 출력
    print("--- Set Trainer Done ---")
    print("Trainer device:", trainer.args.device)
    try:
        print("Model device:", next(model.parameters()).device)
    except StopIteration:
        pass

    return trainer
```

---

## 2) 여전히 GPU 사용률이 낮다면(0~10%로 보일 때)
GPU가 “안 쓰는” 게 아니라 **기다리는** 경우가 많습니다. 다음을 적용해 보세요.

- **데이터로더 병렬화**: `dataloader_num_workers`를 CPU 개수의 절반 이상으로.  
- **핀 메모리**: `dataloader_pin_memory=True`.  
- **배치 크게**: 메모리 허용 한도까지 `per_device_train_batch_size`를 키우거나 `gradient_accumulation_steps`로 **유효 배치**를 키우세요.  
- **평가/저장 빈도 줄이기**: `eval_steps`, `save_steps`, `logging_steps`를 너무 촘촘히 두면 IO/CPU가 병목입니다(예: 1000 스텝 이상 권장).  
- **토큰화 사전 수행**: 매 step마다 동적 토큰화/전처리를 하면 CPU가 병목. **Dataset을 미리 토큰화**해두세요.  
- **혼합정밀**: 위 코드처럼 `fp16=True`(T4/P100) 또는 `bf16=True`(A100/4090 등).  
- **TF32 허용(앙페어 이상)**:
  ```python
  import torch
  torch.backends.cuda.matmul.allow_tf32 = True
  torch.backends.cudnn.allow_tf32 = True
  ```

---

## 3) 모니터링 팁
학습 중 셀에서:
```bash
!nvidia-smi
```
또는 파이썬:
```python
import torch
print("on:", next(model.parameters()).device, "mem:", torch.cuda.memory_allocated()/1e9, "GB")
```
- 사용률이 들쭉날쭉해도 **메모리 점유가 꾸준**하면 GPU는 쓰이고 있는 겁니다.  
- W&B/로깅이 빈번하면 그래프상 사용률이 자주 0으로 내려갈 수 있어요.

---

## 4) 마지막 체크리스트
- Kaggle에서 **GPU 켜기 + 런타임 재시작**  
- `evaluation_strategy`(맞는 키)로 수정  
- `no_cuda=False`(기본값이지만 명시)  
- `fp16` 또는 `bf16` 켜기  
- 데이터로더 워커/핀메모리/배치 조정

위대로 적용하면 GPU가 정상적으로 돌아갈 거예요. 필요하면 현재 `args` 값(배치, eval/save 주기 등)을 알려주시면, **메모리 한도 안에서 최적의 설정**으로 바로 튜닝해 드릴게요.

---

### ❓ 질문 (User)
```
def load_trainer_for_train(model,news_train_dataset,news_val_dataset):
    """학습(train)을 위한 huggingface trainer 설정"""
    training_args = TrainingArguments(
        output_dir=args.save_path + "results",  # output directory
        save_total_limit=args.save_limit,  # number of total save model.
        save_steps=args.save_step,  # model saving step.
        num_train_epochs=args.epochs,  # total number of training epochs
        learning_rate=args.lr,  # learning_rate
        per_device_train_batch_size=args.batch_size,  # batch size per device during training
        per_device_eval_batch_size=2,  # batch size for evaluation
        warmup_steps=args.warmup_steps,  # number of warmup steps for learning rate scheduler
        weight_decay=args.weight_decay,  # strength of weight decay
        logging_dir=args.save_path + "logs",  # directory for storing logs
        logging_steps=args.logging_step,  # log saving step.
        eval_strategy="steps",  # evaluation strategy to adopt during training
            # `no`: No evaluation during training.
            # `steps`: Evaluate every `eval_steps`.
            # `epoch`: Evaluate every end of epoch.
        eval_steps=args.eval_step,  # evaluation step.
        load_best_model_at_end=True,
    )

    ## Add callback & optimizer & scheduler
    MyCallback = EarlyStoppingCallback(
        early_stopping_patience=3, early_stopping_threshold=0.001
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        betas=(0.9, 0.999),
        eps=1e-08,
        weight_decay=args.weight_decay,
        amsgrad=False,
    )
    print("--- Set training arguments Done ---")

    trainer = Trainer(
        model=model,  # the instantiated 🤗 Transformers model to be trained
        args=training_args,  # training arguments, defined above
        train_dataset=news_train_dataset,  # training dataset
        eval_dataset=news_val_dataset,  # evaluation dataset
        compute_metrics=compute_metrics,  # define metrics function
        callbacks=[MyCallback],
        optimizers=(
            optimizer,
            get_cosine_with_hard_restarts_schedule_with_warmup(
                    optimizer,
                    num_warmup_steps=args.warmup_steps,
                    num_training_steps=len(news_train_dataset) * args.epochs,
            ),
        ),
    )
    print("--- Set Trainer Done ---")

    return trainer
```
여기서 gpu 활용을 안하는 거 같애. 그래픽카드 사용량이 올라가질 않아. gpu를 활용해서 트레이닝 하고 싶어
