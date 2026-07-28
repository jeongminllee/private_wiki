---
type: Reference
title: "Hugging Face Skills: AI·ML workflow를 coding agent용 실행 지침으로 패키징하기"
description: "Hub, dataset, 평가, training, job, 논문 게시와 실험 추적 절차를 SKILL.md·script·template로 제공하는 모음"
resource: https://discuss.pytorch.kr/t/hugging-face-skills-ai-ml-ai-feat-acp/9071
notion: https://app.notion.com/p/c1d1a73cf20b83a2aedb017709ef72c3
tags: [reading, agent-skills, hugging-face, mlops]
timestamp: 2026-07-24
status: summarized
---

# 무엇이 다른가

Hugging Face Skills는 API endpoint를 새로 만드는 제품이라기보다 coding agent가 AI·ML 작업을 수행할 때 읽는 절차 묶음이다. 각 독립 폴더의 `SKILL.md`에 사용 조건, 단계, 예시와 guardrail을 적고, 필요하면 dataset query, GGUF 변환과 평가 실행용 script·template를 함께 둔다. 모든 지식을 system prompt에 넣지 않고 관련 작업이 생길 때만 불러오는 구조다.

# 포함 영역

소개 글이 정리한 주요 skill은 다음과 같다.

- `hugging-face-cli`: Hub의 model·dataset·repository·job 작업
- `hugging-face-datasets`: dataset 생성, streaming update, SQL query와 변환
- `hugging-face-evaluation`: model card 평가표, lighteval·vLLM 평가
- `hugging-face-jobs`: remote compute job 실행·예약·상태 확인
- `hugging-face-model-trainer`: TRL 기반 SFT·DPO·GRPO·reward modeling, 비용 추정과 GGUF 변환
- `hugging-face-paper-publisher`: 논문 page와 model·dataset 연결
- `hugging-face-tool-builder`, `hugging-face-trackio`: 재사용 API script와 experiment tracking

Claude Code plugin, Gemini extension, Codex의 instruction 구조 등 여러 agent 환경에서 같은 domain 지식을 재사용하려는 것이 장점이다. MCP가 live tool connection을 제공한다면 skill은 “어떤 순서와 기준으로 그 도구를 쓸지”를 보강한다.

# 적용할 때

설치 후 바로 production training을 맡기기보다 skill이 제안하는 command, 비용 계산, dataset revision과 output path를 사람이 검토한다. 동봉된 helper script도 일반 code와 마찬가지로 network, credential, 삭제·업로드 동작을 확인해야 한다. API와 library가 빠르게 바뀌므로 skill revision과 공식 Hugging Face 문서가 일치하는지도 점검한다.

PyTorchKR 글은 GPT로 정리한 2차 자료라고 명시한다. 설치 명령과 지원 범위를 확정할 때는 연결된 공식 repository의 현재 `SKILL.md`와 license를 우선한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/hugging-face-skills-ai-ml-ai-feat-acp/9071)
- [Hugging Face Skills 저장소](https://github.com/huggingface/skills)

