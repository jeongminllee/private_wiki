---
type: Reference
title: "Parcae 공식 구현: 안정적인 looped language model의 학습·평가·배포"
description: "반복 block의 안정화와 scaling law 연구를 재현하고 pretrained checkpoint를 쓰는 repository 안내"
resource: https://github.com/sandyresearch/parcae
notion: https://app.notion.com/p/9811a73cf20b839f9f5701e3a9c0bccc
tags: [reading, llm, recurrent-depth, research-code]
timestamp: 2026-07-24
status: summarized
---

# 프로젝트

Parcae는 소수의 block을 여러 번 통과시키는 looped language model을 안정적으로 학습하기 위한 architecture와 구현이다. 같은 parameter를 반복 사용해 parameter 수와 수행 compute를 분리하고, compute-optimal 조건에서는 recurrence 횟수와 training data를 함께 늘려야 한다는 scaling law를 연구한다.

공식 repository는 가벼운 model 사용과 연구 재현을 분리한다. Pretrained model만 쓰려면 `parcae-lm` package에서 Hugging Face weight를 읽거나 built-in config로 140M model 등을 만들 수 있다. 직접 학습하려면 repository, Python 3.11+, PyTorch 2.4+가 필요하며 Docker와 Slurm launch script를 권장한다.

# 포함된 실험 경로

FineWeb-Edu 100B·350B token과 Huginn data download, GPT-4 style BPE tokenizer 학습·압축률 평가, YAML 기반 140M·370M·770M·1.3B Parcae와 같은 크기의 GPT baseline training이 준비돼 있다. Evaluation script는 Hugging Face checkpoint와 local checkpoint를 같은 task config로 평가한다.

이 구조는 논문의 표를 읽는 데서 끝나지 않고 model 생성, recurrence 설정, data와 baseline을 직접 맞춰 볼 수 있게 한다. 다만 대규모 결과를 재현하려면 여러 GPU와 상당한 data·compute가 필요하며, package quick start만 실행한 결과를 논문 전체 재현으로 간주하면 안 된다.

Loop 횟수가 늘면 latency도 늘기 때문에 parameter 효율과 serving throughput은 별도 축이다. 동일 parameter 수, 동일 FLOPs, 동일 wall-clock 중 무엇을 맞췄는지 명시하고 downstream accuracy와 memory를 함께 측정해야 한다.

연구 주장과 scaling law는 [Parcae 논문 정리](166-parcae-stable-looped-language-models.md), 배포된 model 목록은 [Parcae model collection 정리](225-parcae-model-collection.md)와 함께 본다.

# 출처

- [Parcae 공식 저장소](https://github.com/sandyresearch/parcae)
- [Parcae 논문](https://arxiv.org/abs/2604.12946)
