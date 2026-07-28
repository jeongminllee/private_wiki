---
type: Reference
title: "Sweep Next-Edit 1.5B: 로컬에서 다음 코드 수정을 예측하기"
description: "Qwen2.5-Coder 기반 소형 모델로 사용자의 다음 편집을 예측하는 오픈 가중치 코드 자동완성 모델"
resource: https://news.hada.io/topic?id=26047
notion: https://app.notion.com/p/d561a73cf20b82ac9292013f48045af2
tags: [reading, ai-coding, local-llm, code-completion]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Sweep Next-Edit는 커서 뒤의 코드만 이어 쓰는 대신 최근 편집 문맥을 보고 사용자가 다음에 바꿀 위치와 내용을 예측하는 1.5B 모델이다. Qwen2.5-Coder를 기반으로 하고 Apache 2.0으로 공개되었다.

# 모델과 실행

- Q8_0 GGUF 형식이며 context length는 8,192 token이다.
- speculative decoding을 사용하고 로컬 노트북에서 500ms 이하 지연을 목표로 한다.
- `llama-cpp-python`과 Hugging Face Hub를 설치한 뒤 제공된 `run_model.py`로 실행할 수 있다.
- 공개 글은 next-edit benchmark에서 네 배 이상 큰 모델보다 높은 성능을 냈다고 보고한다.

# 읽을 때 주의할 점

소형 특화 모델은 전체 코드베이스를 추론하는 에이전트와 경쟁하기보다 짧고 빈번한 수정에서 지연과 privacy 이점을 노린다. 실제 생산성은 언어별 정확도, 잘못된 제안의 수, IDE 통합 지연과 suggestion acceptance rate로 평가해야 한다. GeekNews 토론에 따르면 소개된 JetBrains plugin은 당시 로컬 모델이 아니라 hosted model을 사용했으므로 “모델이 로컬 실행 가능하다”와 “plugin이 로컬 실행한다”를 구분해야 한다.

# 출처

- [GeekNews 정리와 토론](https://news.hada.io/topic?id=26047)

