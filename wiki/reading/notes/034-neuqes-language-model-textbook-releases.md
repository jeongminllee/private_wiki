---
type: Reference
title: "neuqes-101 언어모델 교재 릴리스"
description: "BERT와 GPT부터 정렬 학습과 Diffusion LM까지 확장되는 한국어 중심 교재의 버전별 변화"
resource: https://github.com/yoon-gu/neuqes-101/releases
notion: https://app.notion.com/p/3861a73cf20b81459537de0c7cad20f2
tags: [reading, textbook, language-model, release-notes]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

저장 당시 항목은 `v0.6.1`이었지만 릴리스 페이지에는 이후 `v0.6.2`가 올라와 있다. 이 자료는 특정 PDF 한 번보다 계속 갱신되는 한국어 언어모델 교재 프로젝트로 보는 편이 맞다. 34개 장에 걸쳐 머신러닝 기초, BERT와 GPT, 지도 미세조정, 선호 정렬, Diffusion LM을 연결한다.

# 버전 흐름

## v0.6.0

기존 1~31장의 머신러닝, BERT, GPT, 언어모델 학습·정렬 내용을 유지하면서 32~34장에 Diffusion LM을 추가했다. Diffusion LM의 기본 개념, sampling, 한국어 생성 안정화가 새 축이다.

## v0.6.1

1~34장을 통합 PDF로 묶고 한국어 우선 색인을 강화했다. loss, output head, tokenizer, task, 학습, 평가, 하드웨어, Hugging Face API처럼 실제 공부 중 다시 찾기 쉬운 관점으로 색인을 정리했다. GRPO와 Diffusion 관련 용어도 보강했다.

## v0.6.2

확인 시점의 최신 릴리스다. 1~34장, 약 1,024쪽 규모이며 CJK 인쇄 환경의 줄바꿈 문제와 사실 오류를 수정했다. 내용 확장뿐 아니라 실제 PDF 읽기·인쇄 품질을 다듬는 유지보수 릴리스에 가깝다.

# 활용 방법

처음부터 1,000쪽을 순서대로 읽기보다 WikiDocs의 Colab 실습과 함께 주제별로 왕복하는 편이 좋다.

- BERT·GPT 구조를 이해할 때는 tokenizer, loss, output head 색인을 함께 본다.
- 학습 실습 뒤에는 평가와 하드웨어 장을 확인해 실험 비용과 재현 조건을 정리한다.
- SFT, DPO, GRPO는 같은 데이터와 목표에서 무엇이 달라지는지 표로 비교한다.
- Diffusion LM은 autoregressive LM과 sampling 절차, 오류 형태, 한국어 토큰화 차이를 비교한다.

# 주의할 점

교재가 계속 수정되므로 개별 버전 파일보다 릴리스 페이지를 기준으로 최신판과 변경 내역을 확인해야 한다. 최신 기법의 설명은 빠르게 오래될 수 있으므로 논문과 공식 라이브러리 문서를 병행한다.

# 관련 문서

- [Hugging Face로 시작하는 언어모델 실습서](035-hugging-face-language-models-wikidocs.md)

# 출처

- [neuqes-101 릴리스](https://github.com/yoon-gu/neuqes-101/releases)
- [neuqes-101 저장소](https://github.com/yoon-gu/neuqes-101)

