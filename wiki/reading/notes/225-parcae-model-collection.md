---
type: Reference
title: "Parcae 모델 컬렉션: 안정적인 반복형 언어 모델 4종"
description: "같은 block을 반복 적용하는 looped language model의 140M·370M·770M·1.3B 공개 weight와 tokenizer"
resource: https://huggingface.co/collections/SandyResearch/parcae
notion: https://app.notion.com/p/1861a73cf20b826290c681a7dd0210aa
tags: [reading, llm, looped-models, model-weights]
timestamp: 2026-07-24
status: summarized
---

# 컬렉션 구성

SandyResearch의 Parcae collection은 안정적인 looped model family의 공개 weight를 모은 페이지다. `parcae-140m`, `370m`, `770m`, `1.3b` 네 크기와 전용 tokenizer를 제공한다.

# 활용

반복형 모델은 서로 다른 layer를 길게 쌓는 대신 일부 block을 여러 번 적용해 parameter 재사용과 계산 깊이를 분리하려 한다. 이 collection은 architecture 설명보다 checkpoint 접근점에 가깝기 때문에 model card의 license, base data, inference code와 권장 반복 횟수를 확인한 뒤 사용해야 한다.

# 연결 문서

논문의 방법, 안정성 조건과 실험 해석은 [Parcae: 안정적인 반복형 언어 모델](166-parcae-stable-looped-language-models.md)에 정리되어 있다. 이 문서는 별도 URL인 Hugging Face 배포 목록을 추적한다.

# 출처

- [Parcae model collection](https://huggingface.co/collections/SandyResearch/parcae)

