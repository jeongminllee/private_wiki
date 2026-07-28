---
type: Reference
title: "obsidian-second-brain: AI가 유지보수하는 Obsidian 지식베이스"
description: "여러 코딩 에이전트에서 자료 수집, 연결, 모순 검토, 구조 정비를 수행하는 Obsidian용 스킬 모음"
resource: https://discuss.pytorch.kr/t/obsidian-second-brain-obsidian-vault-ai/10730
notion: https://app.notion.com/p/3881a73cf20b8117a527dbb4c868f01d
tags: [reading, obsidian, knowledge-base, ai-agent]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`obsidian-second-brain`은 Obsidian vault를 Claude Code, Codex, Gemini CLI, OpenCode 같은 에이전트가 읽고 갱신할 수 있도록 만든 오픈소스 스킬 모음이다. 회의 메모, 음성, 스크린샷, 영상, 웹 자료를 넣고 검색·연구·연결·구조 진단까지 수행하는 약 43개의 명령을 제공한다.

# 핵심 아이디어

이 프로젝트는 Karpathy의 LLM Wiki 아이디어를 “자료를 계속 추가하는 위키”에서 “기존 내용을 다시 쓰고 유지보수하는 지식 시스템”으로 확장한다.

- `/obsidian-save`, `/obsidian-ingest`로 대화와 외부 자료를 vault에 넣는다.
- `/research-deep`는 기존 노트와 외부 조사를 결합해 연구 결과를 작성한다.
- `/obsidian-challenge`는 노트의 주장과 반론, 빠진 근거를 점검한다.
- `/obsidian-architect`는 폴더, 태그, frontmatter, 고립 문서 등 구조 문제를 진단한다.
- `/obsidian-daily`와 예약 에이전트는 정기적으로 수집함과 오래된 노트를 정리한다.
- NotebookLM 연동 등 외부 도구를 활용하는 명령도 포함한다.

결과가 로컬 Markdown이라는 점은 특정 서비스에 종속되지 않고 Git 이력, 검색, 다른 도구와 함께 사용할 수 있다는 장점이 있다.

# 이 wiki에 적용하기

현재 저장소의 `raw -> wiki -> index/log` 흐름과 매우 가깝다. 참고할 부분은 단순 수집보다 `모순 찾기`, `오래된 내용 갱신`, `고립 문서 연결`, `정기 구조 점검`을 독립 작업으로 둔 것이다. 반면 이 저장소는 Obsidian 전용 문법보다 일반 Markdown 링크와 OKF frontmatter를 사용하므로 명령 자체를 그대로 가져오기보다 운영 패턴만 선택하는 편이 맞다.

# 주의할 점

에이전트가 기존 노트를 자동 재작성하면 출처가 사라지거나 개인의 해석을 사실처럼 굳힐 수 있다. 큰 변경 전 버전 관리, 원문 보존, 변경 검토가 필수다. 음성·회의·개인 문서를 외부 모델에 보낼 때 개인정보와 회사 기밀도 확인해야 한다. 설치한 스킬은 실행 명령과 권한 범위를 먼저 읽는 것이 좋다.

# 관련 문서

- [OpenWiki](08-openwiki.md)
- [llm-wiki](033-llm-wiki-knowledge-graph-skill.md)

# 출처

- [PyTorchKR 소개 글](https://discuss.pytorch.kr/t/obsidian-second-brain-obsidian-vault-ai/10730)
- [GitHub 저장소](https://github.com/eugeniughelbur/obsidian-second-brain)
- [Karpathy의 LLM Wiki 제안](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

