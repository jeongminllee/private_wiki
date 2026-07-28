---
type: Reference
title: "Claude Code 7단계 학습 로드맵"
description: "첫 실행부터 명세, 스킬, 메모리, 훅, 다중 에이전트와 하네스 설계까지 난이도를 점진적으로 높이는 영상"
resource: https://www.youtube.com/watch?v=IU8GvSvldWw
notion: https://app.notion.com/p/3641a73cf20b810ab0daeb513f564e37
tags: [reading, claude-code, learning, coding-agent]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

영상은 Claude Code를 설치하자마자 멀티 에이전트와 복잡한 자동화부터 배우지 말고, 현재 겪는 병목에 맞춰 한 단계씩 기능을 추가하라고 제안한다. 전체 순서는 “도구 사용”에서 “AI가 일하기 좋은 시스템 설계”로 이동한다.

# 7단계

1. **끝까지 만들어 보기**: 계산기나 할 일 앱처럼 작은 결과물을 만들며 요청, 수정, 실행과 권한 흐름을 익힌다.
2. **기준을 먼저 쓰기**: 목적, 입력, 성공 조건, 실패 사례와 테스트를 정해 단순 생성에서 명세 기반 작업으로 넘어간다.
3. **스킬 만들기**: 반복하는 리뷰 기준과 플레이북을 재사용 가능한 skill로 묶는다.
4. **메모리와 컨텍스트 관리**: `CLAUDE.md`, 세션 기록과 자동 메모리의 역할을 구분한다.
5. **작업 흐름 자동화**: hook으로 포맷, 검사, 알림과 규칙을 자동 실행하고 MCP·브라우저·CI 같은 외부 경로를 연결한다.
6. **역할 분리**: 짧고 독립적인 조사는 subagent로, 서로 소통해야 하는 큰 역할 분담은 agent team으로 처리한다.
7. **하네스 설계**: 어떤 지식을 기억·스킬·훅·에이전트·SDK에 둘지 정해 전체 실행 환경을 설계한다.

# 적용 방법

각 단계를 기능 체크리스트가 아니라 문제 해결 순서로 쓴다. 세션 맥락이 자주 끊길 때만 메모리를 보강하고, 같은 수동 검사가 반복될 때 hook을 추가한다. 단순 작업에 다중 에이전트를 먼저 넣으면 조율 비용만 커질 수 있다.

# 주의할 점

자막의 일부 제품 용어와 명령은 자동 인식 오류가 있으며 기능도 빠르게 바뀐다. 실제 설정과 권한 범위는 현재 공식 문서를 확인한다.

# 출처

- [원본 YouTube 영상](https://www.youtube.com/watch?v=IU8GvSvldWw)
- [Claude Code 공식 문서](https://code.claude.com/docs/en/overview)
- [Notion 원본 항목](https://app.notion.com/p/3641a73cf20b810ab0daeb513f564e37)

