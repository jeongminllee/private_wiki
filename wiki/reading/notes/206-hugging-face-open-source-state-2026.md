---
type: Reference
title: "Hugging Face 2026 오픈소스 AI 생태계 현황"
description: "모델·데이터셋 성장, 참여 집중도, 기업 도입과 파생 모델 생태계를 Hugging Face 지표로 분석한 보고서"
resource: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026
notion: https://app.notion.com/p/52f1a73cf20b83e7a14b0138000a9693
tags: [reading, open-source, ai-ecosystem, hugging-face]
timestamp: 2026-07-24
status: summarized
---

# 핵심 수치

Hugging Face는 2025년 말 기준 생태계가 사용자 1,300만 명, 공개 모델 200만 개 이상, 공개 dataset 50만 개 이상으로 성장했다고 집계한다. 사용자, 모델과 dataset repository 수가 한 해 동안 거의 두 배가 됐고, 단순 다운로드보다 fine-tuned model, adapter, benchmark와 application 같은 파생 산출물의 생성이 늘었다.

# 성장과 집중

양적 성장은 고르게 분포하지 않는다. 모델 약 절반은 누적 download가 200회 미만이고, 가장 많이 다운로드된 상위 200개 모델이 전체 download의 49.6%를 차지한다. 따라서 “모델 수”만으로 생태계의 건강성을 판단하기보다 재사용, 파생 모델, 언어·도메인별 community의 지속성을 함께 봐야 한다.

# 기업과 연구 생태계

- Fortune 500의 30% 이상이 Hugging Face verified account를 유지한다.
- 대기업의 repository 생성이 늘었고 NVIDIA가 특히 강한 기여자로 나타났다.
- robotics와 AI for Science처럼 목적이 뚜렷한 하위 생태계가 성장한다.
- 공개 weight는 downstream customization과 deployment 선택권을 늘리지만, 공개성의 정의와 data provenance는 별도로 따져야 한다.

# 해석 시 주의

이 보고서는 Hugging Face 내부 활동을 중심으로 한 생태계 관측이다. 다른 registry, private deployment와 API-only model은 충분히 반영되지 않으며 download 수는 실제 사용량이나 품질을 그대로 뜻하지 않는다.

# 출처

- [State of Open Source on Hugging Face: Spring 2026](https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026)

