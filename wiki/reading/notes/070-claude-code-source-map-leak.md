---
type: Reference
title: "Claude Code source map 공개 사고"
description: "npm 패키지에 디버깅용 source map이 포함되어 약 51만 2천 줄의 TypeScript 원본이 노출된 2026년 사건"
resource: https://www.youtube.com/watch?v=G4VyivO2jbE
notion: https://app.notion.com/p/1361a73cf20b820688778110d00020a7
tags: [reading, claude-code, security, supply-chain]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

2026년 3월 31일 `@anthropic-ai/claude-code` npm 패키지의 한 릴리스에 약 59.8MB source map이 실수로 포함됐다. 이 파일에는 압축된 JavaScript와 원 TypeScript를 연결하는 정보가 들어 있어 약 1,900개 파일, 51만 2천여 줄의 읽을 수 있는 소스가 복원됐다. 영상 제목과 자막의 “500만 줄”은 10배가량 큰 잘못된 수치다.

# 사건의 성격

외부 침입으로 서버나 고객 데이터가 탈취된 사건이 아니라 공개 패키징 과정의 human error였다. Anthropic은 내부 소스가 포함됐지만 민감한 고객 데이터와 자격 증명은 노출되지 않았다고 밝혔다. 이미 배포된 압축 코드는 읽을 수 있었지만 source map은 파일 구조, 주석과 원본 이름을 훨씬 쉽게 드러냈다.

공개 자료에서는 기본 agent loop, tool dispatch, memory와 미출시 feature flag 등이 분석됐다. 그러나 feature flag가 존재한다고 실제 출시 계획이나 완성된 기능이라고 단정할 수 없다. 영상의 숨은 기능 설명과 매출 추정도 확인된 사건 사실과 구분해야 한다.

# 실무 교훈

- package manifest와 ignore 규칙을 CI에서 검사한다.
- 배포 tarball을 실제로 생성해 허용 파일 목록과 크기를 검증한다.
- source map은 별도 비공개 저장소에 업로드하고 production artifact에서 제외한다.
- 비밀 값은 소스와 build artifact에 처음부터 넣지 않는다.
- 유출본을 사칭한 저장소와 패키지는 악성 코드 유포 경로가 될 수 있으므로 내려받지 않는다.

# 출처

- [원본 YouTube 영상](https://www.youtube.com/watch?v=G4VyivO2jbE)
- [Axios 사건 보도](https://www.axios.com/2026/03/31/anthropic-leaked-source-code-ai)
- [Claude Code 공식 저장소](https://github.com/anthropics/claude-code)
- [Notion 원본 항목](https://app.notion.com/p/1361a73cf20b820688778110d00020a7)

