---
type: Reference
title: "OmniCoder-9B의 agent trajectory 증류 실험"
description: "프론티어 coding agent의 작업 trajectory 42만 5천 건을 9B model에 LoRA로 학습한 사례와 benchmark 해석"
resource: "https://wikidocs.net/blog/@jaehong/9417/"
notion: "https://app.notion.com/p/a3a1a73cf20b831694f901a658117ce8"
tags: [reading, coding-agent, distillation, lora, local-llm]
timestamp: 2026-07-24
status: summarized
---

# 접근법

OmniCoder-9B는 Qwen3.5-9B를 기반으로 frontier model이 coding agent에서 수행한 약 42만 5천 trajectory를 LoRA 학습한 model이다. Final code만 모방하지 않고 file 읽기, error 진단, LSP feedback 반영, 작은 diff 적용 같은 도구 사용 과정을 학습한다.

Article에 따르면 LoRA rank 64, alpha 32, Axolotl과 H200 4대 DDP를 사용했고 sample packing efficiency는 99.35%였다. 262K native context와 hybrid Gated Delta Network 기반 model이라는 점도 긴 repository context 처리에 유리한 요소로 제시한다.

# 결과 해석

보고된 Terminal-Bench 2.0 점수는 base model 14.6%에서 23.6%로 9%p, 상대 61% 상승했다. GPQA Diamond pass@1은 83.8%, AIME 2025 pass@5는 90%였다. 다만 Terminal-Bench 절대 성공률은 여전히 약 4분의 1이고 SWE-bench 결과가 없어 production coding agent와 직접 비교하기 어렵다.

9B model은 4-bit에서 16GB급 VRAM으로 실행 가능하다는 장점이 있지만, local 실행 가능성과 reliable autonomy는 다른 문제다. Domain repository의 test와 보안 sandbox를 붙여 실제 task success, latency와 intervention rate를 측정해야 한다.

# 데이터 출처 위험

Article은 Claude, GPT와 Gemini 계열 출력 trajectory를 사용했다고 설명한다. 각 provider의 출력물을 경쟁 model training에 이용하는 행위는 이용 약관과 충돌할 수 있다. Model license가 permissive하더라도 training data의 수집 권한, 개인정보와 secret 포함 여부는 별도 검토 대상이다.

# 관련 문서

- [On-Policy Distillation survey](382-on-policy-distillation-survey.md)

# 출처

- [위키독스 분석 글](https://wikidocs.net/blog/@jaehong/9417/)
- [Tesslate model page](https://huggingface.co/Tesslate/OmniCoder-9B)
