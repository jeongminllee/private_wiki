---
type: Reference
title: "NodeNest: 질문을 지식 그래프로 펼치는 오픈소스 AI 튜터"
description: "선형 채팅을 개념 node와 질문 tree로 바꾸는 NodeNest의 학습 방식과 검증 포인트"
resource: https://discuss.pytorch.kr/t/nodenest-ai/8545
notion: https://app.notion.com/p/8dd1a73cf20b83ccbeaf810770591b27
tags: [reading, ai-tutor, knowledge-graph, education]
timestamp: 2026-07-24
status: summarized
---

# 아이디어

NodeNest는 AI tutor와의 대화를 한 줄짜리 chat history로 쌓지 않고, 질문과 개념을 canvas의 node로 펼친다. 사용자는 한 개념에서 파생된 질문을 가지처럼 따라가며 전체 학습 구조와 현재 위치를 볼 수 있다.

# 동작 방식

답을 즉시 주기보다 Socratic question으로 생각을 유도하고, 한 주제를 깊이 파기 전에 관련 개념을 폭넓게 펼치는 breadth-first tree를 지향한다. UI는 React Flow와 Dagre로 graph를 배치하며 Next.js 16, Zustand, Tailwind CSS 4와 Gemini 3 Flash Preview를 사용한다. 로컬 또는 Vercel에서 실행하고 Google API key를 연결하는 형태다.

# 기대 효과

시각적 구조는 대화 중 놓친 분기와 개념 관계를 다시 찾기 쉽게 만든다. 특히 여러 하위 개념이 얽힌 공부에서 “무엇을 알고 무엇을 아직 묻지 않았는가”를 확인하는 외부 기억 장치로 쓸 수 있다.

# 주의할 점

Graph UI가 곧 학습 효과를 보장하지는 않는다. node 수가 많아질수록 화면이 복잡해지고, AI가 만든 관계가 부정확하면 오개념도 시각적으로 강화될 수 있다. 실제 사용에서는 source citation, concept 수정·병합, 학습 목표별 pruning과 복습 기능을 확인해야 한다.

또한 local UI라고 해도 Gemini API를 쓰면 prompt가 외부로 전송된다. “추적 없음”이나 privacy 주장은 저장 위치, telemetry와 provider policy를 직접 점검한 뒤 판단해야 한다.

# 출처

- [PyTorchKR 소개](https://discuss.pytorch.kr/t/nodenest-ai/8545)

