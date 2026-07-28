---
type: Reference
title: "Kanana-2 30B-A3B Thinking 모델과 개인 벤치마크 해석"
description: "카카오의 MoE 추론 모델 사양과 영상 제작자의 14문항 실험을 분리해 읽는 정리"
resource: https://www.youtube.com/watch?v=BRz_IEJDSfk
notion: https://app.notion.com/p/c0a1a73cf20b823b8cc20102ebaf4493
tags: [reading, llm, moe, benchmark, kanana]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

영상은 카카오의 공개 모델 `kanana-2-30B-A3B-Thinking`을 로컬 GPU에서 직접 시험한다. 공식 사양과 제작자의 소규모 체감 실험은 구분해야 한다. 전자는 모델 구조에 관한 사실이고, 후자는 특정 하드웨어·추론 설정·14개 질문에서 얻은 사례다.

# 모델 구조

- 전체 parameter는 30B지만 한 token 처리에 약 3B가 활성화되는 MoE(Mixture of Experts) 구조다.
- 48개 layer, 128개 expert 중 6개 routed expert와 2개 shared expert를 사용한다.
- attention은 MLA(Multi-head Latent Attention), context length는 32,768 token이다.
- Base, Instruct, Thinking 변형이 공개되어 있으며 이 영상은 숙고 과정을 출력하는 Thinking 모델을 다룬다.
- 모델 카드의 비교표는 Qwen3-30B-A3B 계열과 여러 benchmark를 비교하지만, benchmark마다 우열이 섞여 있다.

# 영상의 실험 결과

제작자는 H100/H200 환경에서 수학·추론·코딩 등 14개 질문을 던져 8개를 통과했다고 평가한다. 긴 사고가 같은 지점을 반복하거나 출력 제한에 걸리는 사례, 코딩 문제에서 약한 사례와 느린 생성 속도를 보고한다.

이 결과를 “모델 정확도 57%”로 일반화하면 안 된다. 문항 수가 작고 채점 기준, prompt, sampling parameter, serving engine과 maximum token 설정이 공식 benchmark와 다르다. 대신 실제 배포 전에 한국어 품질, reasoning loop, latency와 truncation을 자신의 task set으로 확인해야 한다는 사례로 읽는 편이 정확하다.

# 직접 평가할 때

1. 업무에서 자주 쓰는 질문을 난이도와 유형별로 최소 수십 개 고정한다.
2. 정답뿐 아니라 latency, token 수, 반복, 형식 준수와 실패 복구를 기록한다.
3. 같은 quantization·sampling·context 조건으로 대조 모델과 비교한다.
4. Thinking 출력이 긴 모델은 `max_tokens` 부족과 parser 호환성을 따로 점검한다.

# 출처

- [YouTube 실험 영상](https://www.youtube.com/watch?v=BRz_IEJDSfk)
- [카카오 공식 Hugging Face 모델 카드](https://huggingface.co/kakaocorp/kanana-2-30b-a3b-thinking)
- [Notion 원본 항목](https://app.notion.com/p/c0a1a73cf20b823b8cc20102ebaf4493)
