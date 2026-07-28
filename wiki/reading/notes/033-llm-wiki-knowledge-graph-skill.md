---
type: Reference
title: "llm-wiki: 흩어진 정보를 연결된 로컬 지식으로 만들기"
description: "자료 분석, 페이지 생성, 출처 신뢰도, 중복 제거, 상태 점검을 묶은 에이전트용 로컬 wiki 스킬"
resource: https://discuss.pytorch.kr/t/llm-wiki-karpathy/10843
resource_aliases: [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f]
notion: https://app.notion.com/p/3871a73cf20b8064ad2fcb8c04c44f65
notion_aliases: [https://app.notion.com/p/0351a73cf20b823faa8d8118346319f7, https://app.notion.com/p/2041a73cf20b82599ba0013bc90cdeaf]
tags: [reading, llm-wiki, knowledge-base, knowledge-graph]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`llm-wiki`는 논문, 블로그, 트윗, 메모를 한 번 요약하고 끝내지 않고 엔티티·주제·출처 페이지로 나눠 지속적으로 연결하는 에이전트 스킬이다. 결과를 로컬 Markdown으로 저장해 Obsidian과 일반 편집기에서 읽을 수 있고, 자체 완결형 HTML 지식 그래프도 생성한다.

# 지식을 쌓는 방식

자료 처리는 분석과 페이지 생성의 두 단계로 나뉜다. 긴 자료를 분석한 결과는 스크립트가 형식 검증하고, URL 종류에 맞는 추출기를 선택한다. 생성된 주장에는 다음과 같은 신뢰도 표식을 붙인다.

- `EXTRACTED`: 원문에서 직접 확인
- `INFERRED`: 원문을 바탕으로 추론
- `AMBIGUOUS`: 여러 해석이 가능
- `UNVERIFIED`: 아직 검증하지 못함

SHA-256 기반 중복 제거, write-through cache, 실패 시 복구 장치를 두어 같은 자료의 반복 처리와 반쯤 작성된 상태를 줄인다. 지식베이스가 커지면 고아 페이지, 깨진 링크, 인덱스 불일치를 검사하고 AI를 이용한 모순·교차 참조 검토도 수행한다. 대화에서 재사용할 결정을 문서로 만드는 conversation crystallization과 세션 시작 시 관련 지식을 주입하는 기능도 포함한다.

# 이 저장소와의 관계

현재 wiki의 `raw/` 원본 보존, OKF 문서, cross-link, `index.md`, `log.md`, lint 규칙은 같은 문제를 더 명시적인 저장소 운영 규칙으로 푼다. 참고할 만한 부분은 주장별 신뢰도와 내용 해시 기반 중복 제거다. 반면 이 저장소는 하나의 concept를 작은 문서로 유지하고 일반 Markdown 링크를 사용하므로, 도구의 전체 구조를 그대로 덮어쓰기보다 필요한 기능만 흡수하는 편이 안전하다.

# 적용 아이디어

- 웹 수집 문서에 `확인됨 / 추론 / 확인 필요` 상태를 문단 또는 주장 단위로 표시한다.
- URL뿐 아니라 내용 해시와 원문 날짜를 저장해 이동·재게시된 중복을 찾는다.
- 큰 ingest 뒤에는 고립 문서, 깨진 링크, 색인 누락, 상충 주장을 한 번에 검사한다.
- 대화 중 결정된 운영 규칙은 대화 기록에만 두지 않고 Decision Note로 남긴다.

# 주의할 점

자동 생성된 지식 그래프는 링크 수가 많다고 좋은 지식이 되는 것이 아니다. 링크의 관계와 근거가 불분명하면 탐색 잡음만 늘어난다. 원문과 추론을 분리하고, 자동 재작성 전 변경 이력과 사람 검토 경로를 유지해야 한다.

# 관련 문서

- [OpenWiki](08-openwiki.md)
- [obsidian-second-brain](027-obsidian-second-brain.md)
- [저장소의 LLM Wiki 참고 문서](../../../references/llm-wiki.md)

# 출처

- [PyTorchKR 소개 글](https://discuss.pytorch.kr/t/llm-wiki-karpathy/10843)
- [llm-wiki-skill 저장소](https://github.com/sdyckjq-lab/llm-wiki-skill)
- [Karpathy의 LLM Wiki 제안](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
