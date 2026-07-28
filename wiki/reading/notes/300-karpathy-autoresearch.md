---
type: Reference
title: "Karpathy autoresearch: 한 GPU에서 5분짜리 LLM 실험을 반복하는 autonomous research loop"
description: "agent가 train.py를 바꾸고 val_bpb 개선 여부로 유지·폐기하는 작고 비교 가능한 야간 실험 환경"
resource: https://github.com/karpathy/autoresearch
notion: https://app.notion.com/p/58d1a73cf20b82b6993301d8ccab31b9
tags: [reading, ai-agents, llm-training, automated-research]
timestamp: 2026-07-24
status: summarized
---

# 실험 loop

`autoresearch`는 AI agent에게 작지만 실제로 학습되는 GPT code를 주고 밤새 실험하게 하는 repository다. Agent는 `train.py`의 architecture, optimizer, batch와 hyperparameter를 수정하고 정확히 5분간 학습한다. Validation bits per byte(`val_bpb`)가 낮아지면 변경을 유지하고, 나빠지면 되돌린 뒤 다음 가설을 시험한다.

핵심 file은 세 개다. `prepare.py`는 data, BPE tokenizer, dataloader와 evaluation을 고정한다. `train.py`는 model, Muon·AdamW optimizer와 training loop를 담고 agent만 수정한다. `program.md`는 agent가 지킬 연구 절차이며 사람이 개선하는 가벼운 skill 역할을 한다.

# 설계가 주는 것

한 실험의 wall-clock budget과 metric을 고정해 같은 GPU 안에서 약 12회/시간, 야간 약 100회의 시도를 비교할 수 있다. 수정 대상을 한 file로 제한하므로 diff와 failure를 검토하기도 쉽다. 연구 자동화에서 자유도를 무한히 주는 대신 search space, budget, objective와 변경 경계를 명확히 두는 사례다.

# 해석의 한계

결과는 동일 machine 안에서는 비교 가능하지만 다른 GPU나 kernel 환경과 직접 비교할 수 없다. 5분 objective를 최적화하다 보면 startup이 빠른 구성, 짧은 horizon에 유리한 hyperparameter나 evaluation noise에 과적합할 수 있다. 가장 낮은 `val_bpb`가 downstream usefulness나 장기 학습 성능을 자동 보장하지 않는다.

공식 기본 환경은 한 장의 NVIDIA GPU이며 H100에서 시험됐다. 작은 GPU나 Mac에서는 dataset entropy, vocabulary, sequence length, evaluation token, depth와 batch를 낮춘 fork가 필요하다.

# 안전한 운영

README의 “disable all permissions”는 승인을 없애라는 의미의 표현이지만, 실제로 unattended agent에 unrestricted shell을 주는 것은 위험하다. Network·credential이 없는 container, 전용 GPU quota, disk limit와 timeout에서 실행하고 각 experiment의 patch, command, seed, metric과 crash를 append-only log로 남긴다. 자동 개선은 결과를 낳는 loop이지 과학적 타당성을 대신하는 장치는 아니다.

# 출처

- [autoresearch 저장소](https://github.com/karpathy/autoresearch)

