---
type: Reference
title: AI Coding Usage Card
description: 로컬 AI 코딩 사용량을 GitHub 프로필 카드로 만드는 셀프 호스팅 도구의 구조와 활용 포인트
resource: https://github.com/Baek-Seunghyun/ai-coding-usage-card
notion: https://app.notion.com/p/3a61a73cf20b81bf8ccdc507fd90b537
tags: [reading, repository, ai-coding, observability]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Claude Code, Codex, Gemini 같은 AI 코딩 도구의 로컬 사용 로그를 집계해 GitHub 프로필용 SVG 카드로 만드는 프로젝트다. 외부 분석 서비스에 로그를 보내기보다 내 컴퓨터에서 통계를 계산하고 생성 결과만 저장소에 반영한다.

# 핵심 내용

- `ccusage` 계열 파서를 이용해 토큰 사용량과 추정 비용을 계산한다.
- Windows 작업 스케줄러, cron, launchd로 매일 집계와 SVG 생성을 자동화할 수 있다.
- 여러 장치가 각자의 JSON을 `cards/devices/`에 남기면 병합된 카드로 표시한다.
- 전체형, 절반형, 잔디형, 조합형 등 README 배치에 맞춘 카드 변형을 제공한다.

# 왜 읽을 만한가

AI 코딩을 감으로만 사용하지 않고 비용과 사용 패턴을 관찰하는 작은 출발점이다. 셀프 호스팅 구조라 개인 로그를 외부 대시보드에 넘기지 않는다는 점도 실용적이다.

# 적용 아이디어

- 공개 프로필 카드보다 먼저 비공개 저장소에서 주간 토큰·비용 추세를 검증한다.
- 단순 사용량과 함께 작업 완료율, 테스트 통과율, 되돌린 변경 수를 기록해 결과 지표와 연결한다.
- 여러 PC를 쓴다면 장치별 데이터를 분리하고 병합 시점과 중복 계산 규칙을 확인한다.

# 주의할 점

토큰과 추정 비용은 생산성 그 자체가 아니다. 자동 커밋을 켜기 전에 생성 파일 범위, Git 인증 정보, 로그에 민감한 내용이 포함되는지 확인해야 한다.

# 출처

- [GitHub 저장소](https://github.com/Baek-Seunghyun/ai-coding-usage-card)
- [Notion 원본 항목](https://app.notion.com/p/3a61a73cf20b81bf8ccdc507fd90b537)
