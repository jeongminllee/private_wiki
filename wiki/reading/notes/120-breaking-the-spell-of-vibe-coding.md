---
type: Reference
title: "바이브 코딩의 마법을 깨기"
description: "생성량이 성과처럼 느껴지는 dark flow를 경계하고 실제 속도·품질·학습을 측정하자는 비판"
resource: https://news.hada.io/topic?id=26708
notion: https://app.notion.com/p/5961a73cf20b8311a7b881fc95852ccc
tags: [reading, vibe-coding, productivity, software-engineering]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

fast.ai의 Rachel Thomas는 대량의 AI code를 사람이 읽지 않은 채 쌓는 바이브 코딩이 진짜 flow보다 도박의 `dark flow`와 닮을 수 있다고 비판한다. code line과 agent의 긴 작업 표시가 즉각적인 성취감을 주지만, 쓸모·유지보수성과 bug는 훨씬 늦게 드러날 수 있다는 문제다.

# 잘못된 생산성 신호

- 생성된 코드량과 동시에 실행되는 작업 수를 성과로 착각한다.
- 부분 성공을 전체 성공처럼 받아들이고 숨은 손실을 늦게 발견한다.
- architecture 선택을 직접 통제한다고 느끼지만 LLM이 제시한 좁은 선택지 안에서 움직인다.
- 빠른 feedback의 즐거움 때문에 실제 사용자 가치와 학습을 점검하지 않는다.

# 근거를 읽는 법

글은 METR 연구에서 익숙한 open-source repository를 다룬 숙련 개발자가 AI 사용 시 실제로 19% 느려졌지만 더 빨라졌다고 예상한 결과를 인용한다. 중요한 경고지만 특정 시점의 tool, 참여자와 task에 대한 연구이므로 모든 AI 코딩이 느리다는 결론은 아니다.

# 적용 원칙

작업 전 성공 기준과 예상 시간을 적고, AI 사용 여부별 cycle time, defect, review와 재작업 비용을 기록한다. 작은 diff, automated test와 실제 사용자 검증으로 feedback을 빠르게 만든다. AI 사용 quota나 미래 예측 때문에 기본기 학습을 포기하지 않고, 이해하지 못한 코드는 production에 넣지 않는다.

# 비판적으로 볼 점

“AI는 유용한 추상화나 모듈화를 만들지 못한다” 같은 단정은 모델과 task에 따라 반례가 가능한 저자의 주장이다. 글의 가장 재사용 가능한 부분은 AI를 배척하라는 결론보다 자기 생산성을 느낌이 아닌 결과로 측정하라는 요구다.

# 출처

- [fast.ai 원문](https://www.fast.ai/posts/2026-01-28-dark-flow/)
- [GeekNews 한국어 정리와 토론](https://news.hada.io/topic?id=26708)
- [METR 연구](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [Notion 원본 항목](https://app.notion.com/p/5961a73cf20b8311a7b881fc95852ccc)
