---
type: Reference
title: "Hugging Face로 시작하는 언어모델 실습서"
description: "Colab 무료 환경에서 BERT, GPT, 정렬 학습, Diffusion LM을 직접 구현하며 배우는 34장 교재"
resource: https://wikidocs.net/book/20340
notion: https://app.notion.com/p/3861a73cf20b81cf995fc884c1c5b12e
tags: [reading, course, hugging-face, language-model]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

황윤구·유창민의 한국어 실습 교재로, Colab 무료 버전에서 작은 데이터와 모델을 직접 돌리며 언어모델의 구성 요소를 익히도록 설계되어 있다. 사전학습 모델 사용법만 보여주지 않고 tokenizer와 BERT·GPT를 from scratch로 만드는 과정, SFT·DPO·GRPO, Diffusion LM까지 34장으로 이어진다.

# 학습 흐름

## 데이터와 BERT

Hugging Face `datasets`와 tokenizer 사용법에서 시작해 회귀, 이진·다중 클래스, 멀티라벨 분류를 BERT로 실습한다. Yelp, KLUE-YNAT, NSMC 같은 데이터셋을 사용하며 한국어 BERT와 tokenizer 학습도 다룬다. 이후 작은 BERT를 처음부터 사전학습하고 downstream task에 미세조정해, “모델 호출” 뒤의 구조를 확인한다.

## GPT와 생성

Wikitext, TinyStories 및 한국어 자료를 이용해 autoregressive GPT를 구현하고 사전학습·지속 사전학습·미세조정을 연결한다. 작은 모델에서 데이터 전처리, causal mask, next-token loss, sampling이 실제 생성 품질에 어떤 영향을 주는지 실험할 수 있다.

## 정렬과 Diffusion LM

지도 미세조정(SFT), 직접 선호 최적화(DPO), 그룹 상대 정책 최적화(GRPO)를 단계적으로 소개한다. 마지막 32~34장은 토큰을 순차 생성하는 GPT와 다른 Diffusion LM의 학습·sampling·한국어 안정화 문제를 다룬다.

# 추천 학습법

1. 각 장의 Colab을 먼저 그대로 실행해 기준 결과를 남긴다.
2. 데이터 크기, tokenizer, learning rate 중 하나만 바꿔 차이를 기록한다.
3. 사전학습 모델과 scratch 모델의 성능뿐 아니라 시간과 메모리를 비교한다.
4. SFT·DPO·GRPO는 데이터 형식, 보상 신호, 실패 사례를 같은 표에 정리한다.
5. 실행 결과와 교재 버전을 함께 기록해 라이브러리 업데이트에 따른 차이를 구분한다.

# 주의할 점

무료 Colab은 GPU 종류와 세션 시간이 일정하지 않아 그대로 재현되지 않을 수 있다. 예제의 작은 데이터에서 잘 작동한 설정이 실제 규모에서도 최적이라는 뜻은 아니다. `transformers`, `datasets`, `trl` API는 빠르게 바뀌므로 교재 버전과 패키지 버전을 함께 확인한다.

# 관련 문서

- [neuqes-101 언어모델 교재 릴리스](034-neuqes-language-model-textbook-releases.md)
- [Grouped Query Attention](11-grouped-query-attention.md)
- [All RL Algorithms from Scratch](18-all-rl-algorithms-from-scratch.md)

# 출처

- [WikiDocs 교재](https://wikidocs.net/book/20340)
- [neuqes-101 릴리스](https://github.com/yoon-gu/neuqes-101/releases)

