---
type: Concept
title: "OKF 지식 저장 형식"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-06-18)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-06-18
status: active
---

# OKF 지식 저장 형식

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-18

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
md 파일 분석하자. 지식 관리를 위해서 필요할거 같아서 가져왔어

### 💡 답변 (Assistant)
좋아요. 이 md 파일의 핵심은 **OKF(Open Knowledge Format)** 라는 “지식 저장 형식” 제안서입니다. 한 줄로 요약하면:

> **폴더 + Markdown + YAML frontmatter만으로 사람도 읽고, AI agent도 파싱할 수 있는 지식 저장소를 만들자는 규격**입니다. fileciteturn0file0

## 1. 이 문서의 핵심 구조

OKF는 지식을 복잡한 DB나 전용 앱에 넣는 대신, 다음처럼 관리하자는 방식입니다.

```text
knowledge_bundle/
├── index.md
├── log.md
├── concepts/
│   ├── machine-learning.md
│   ├── autogluon.md
│   └── gpu-troubleshooting.md
└── projects/
    ├── guam.md
    └── chatbot.md
```

각 `.md` 파일은 하나의 **Concept**, 즉 하나의 지식 단위입니다. 예를 들어:

```markdown
---
type: Concept
title: AutoGluon
description: AutoML 프레임워크이며 tabular, multimodal, time series 작업을 지원한다.
tags: [automl, machine-learning, python]
timestamp: 2026-06-18T09:00:00+09:00
---

# 핵심 요약

AutoGluon은 빠르게 baseline을 만들 때 유용하다.

# 자주 겪은 문제

- `ModuleNotFoundError`
- editable install 경로 문제
- report 저장 문제

# 관련 문서

- [GUAM 프로젝트](../projects/guam.md)
```

문서에서 필수로 요구하는 건 거의 하나뿐입니다. **일반 개념 문서에는 YAML frontmatter가 있어야 하고, 그 안에 `type` 필드가 반드시 있어야 합니다.** 그 외 `title`, `description`, `resource`, `tags`, `timestamp`는 권장 필드입니다. fileciteturn0file0

---

## 2. 개인 지식관리 관점에서 아주 괜찮은 이유

이 형식은 지금 사용자의 상황과 꽤 잘 맞습니다. 특히 사용자는 ML, AutoML, PyTorch, Kaggle, Ubuntu, GPU, 에러 해결, 알고리즘, CS 공부처럼 **여러 주제를 장기간 누적**하고 있습니다. 이럴 때 Notion처럼 화면은 예쁘지만 구조가 느슨한 도구보다, Markdown 기반 저장소가 더 강합니다.

OKF의 장점은 크게 네 가지입니다.

첫째, **사람이 그냥 읽을 수 있습니다.** 전용 앱이 없어도 VS Code, Obsidian, GitHub, 터미널에서 열 수 있습니다.

둘째, **AI가 읽기 좋습니다.** YAML frontmatter에 `type`, `tags`, `description`이 있으므로 나중에 “내 AutoGluon 관련 문제만 찾아줘”, “GPU 오류 해결 로그만 요약해줘” 같은 작업을 시키기 좋습니다.

셋째, **Git으로 버전 관리하기 좋습니다.** md 파일은 diff가 잘 보입니다. 지식이 언제 어떻게 바뀌었는지 추적할 수 있습니다.

넷째, **도구 종속성이 낮습니다.** Notion, Obsidian, Logseq, VS Code, GitHub 어디로든 옮기기 쉽습니다. 문서도 OKF가 “central authority, schema registry, required tooling이 없다”는 최소주의를 강조합니다. fileciteturn0file0

---

## 3. 이 문서에서 가장 중요한 개념

### Knowledge Bundle

하나의 지식 저장소 전체입니다.

예:

```text
my-knowledge/
```

사용자에게는 이걸 GitHub repo 하나로 두는 게 좋습니다.

```text
jeongmin-knowledge/
```

---

### Concept

하나의 md 파일입니다. “개념 하나 = 파일 하나”라고 보면 됩니다.

예:

```text
ml/autogluon.md
ml/pytorch-tensor-shape.md
infra/ubuntu-cuda-install.md
errors/module-not-found.md
```

---

### Concept ID

파일 경로에서 `.md`를 뺀 값입니다.

```text
ml/autogluon.md
```

이면 concept ID는:

```text
ml/autogluon
```

이 방식이 중요한 이유는 나중에 AI나 검색기가 문서를 식별할 때 안정적인 ID가 되기 때문입니다.

---

### Frontmatter

md 파일 맨 위의 YAML 메타데이터입니다.

```yaml
---
type: Error Note
title: ModuleNotFoundError in GUAM
description: GUAM 패키지 editable install 이후 import가 실패한 문제.
tags: [python, package, guam, error]
timestamp: 2026-06-18T09:00:00+09:00
---
```

개인 지식관리에서는 이 frontmatter가 핵심입니다. 본문은 사람이 읽는 내용이고, frontmatter는 검색·분류·AI 활용을 위한 메타데이터입니다.

---

## 4. 주의할 점: 문서 안에 약간의 규칙 충돌이 있음

작은 모순이 하나 있습니다.

문서의 `Index Files` 섹션에서는 `index.md`에 frontmatter가 없다고 설명합니다. 그런데 `Versioning` 섹션에서는 bundle-root `index.md`에 한해서 `okf_version: "0.1"` frontmatter를 넣을 수 있다고 합니다. fileciteturn0file0

즉, 실제로 적용할 때는 이렇게 정리하면 됩니다.

```text
일반 index.md:
- frontmatter 없음

루트 index.md:
- 예외적으로 okf_version frontmatter 허용
```

예:

```markdown
---
okf_version: "0.1"
---

# Jeongmin Knowledge Base

## ML
* [AutoGluon](ml/autogluon.md) - AutoML 실험과 리포트 정리
* [PyTorch](ml/pytorch.md) - 텐서, 학습 루프, 에러 정리
```

이 정도로 해석하면 실사용에 문제 없습니다.

---

## 5. 사용자에게 추천하는 실제 폴더 구조

지금까지 다룬 주제를 기준으로 하면 이렇게 시작하는 게 좋아 보입니다.

```text
knowledge/
├── index.md
├── log.md
├── ml/
│   ├── index.md
│   ├── autogluon.md
│   ├── pytorch.md
│   ├── lightautoml.md
│   ├── xgboost.md
│   └── model-evaluation.md
├── infra/
│   ├── index.md
│   ├── ubuntu.md
│   ├── cuda.md
│   ├── vllm.md
│   └── uv-python.md
├── errors/
│   ├── index.md
│   ├── module-not-found.md
│   ├── pip-editable-install.md
│   ├── cuda-install-failure.md
│   └── empty-stream-lmstudio.md
├── projects/
│   ├── index.md
│   ├── guam.md
│   ├── chatbot-kakaotalk-summary.md
│   └── automl-report-generator.md
├── cs/
│   ├── index.md
│   ├── operating-system.md
│   ├── database.md
│   ├── network.md
│   └── software-engineering.md
├── algorithms/
│   ├── index.md
│   ├── bfs-dfs.md
│   ├── dp.md
│   ├── dijkstra.md
│   └── union-find.md
└── papers/
    ├── index.md
    └── reading-template.md
```

개인적으로는 `errors/` 디렉토리를 꼭 따로 두는 걸 추천합니다. 사용자는 환경설정, 패키지 설치, GPU, import path 문제를 자주 다루기 때문에, 에러 해결 지식이 시간이 지날수록 가장 값진 자산이 됩니다.

---

## 6. 바로 쓸 수 있는 md 템플릿

### 개념 정리용

```markdown
---
type: Concept
title: 
description: 
tags: []
timestamp: 
---

# 핵심 요약

# 왜 중요한가

# 주요 개념

# 예제

# 관련 문서

# Citations
```

---

### 에러 해결용

```markdown
---
type: Error Note
title: 
description: 
tags: [error]
timestamp: 
status: solved
---

# 상황

# 에러 메시지

```text
여기에 에러 로그 붙여넣기
```

# 원인

# 해결 방법

# 재발 방지

# 관련 문서
```

---

### 프로젝트 기록용

```markdown
---
type: Project
title: 
description: 
tags: [project]
timestamp: 
status: active
---

# 목표

# 현재 상태

# 폴더 구조

# 실행 방법

# 주요 문제

# 다음 작업

# 관련 문서
```

---

### 논문 읽기용

```markdown
---
type: Paper Note
title: 
description: 
resource: 
tags: [paper]
timestamp: 
---

# 한 줄 요약

# 문제의식

# 핵심 아이디어

# 방법론

# 실험 결과

# 내가 이해한 내용

# 내 프로젝트에 적용할 점

# 모르는 부분
```

---

## 7. 내 판단: 이 파일은 “개인 지식관리 + AI 활용”에 적합함

이 OKF 문서는 단순 메모법이라기보다, **AI가 읽을 수 있는 개인 위키 형식**에 가깝습니다. Obsidian처럼 자유롭게 링크를 걸 수 있고, GitHub처럼 버전 관리할 수 있으며, 나중에는 RAG나 검색 시스템에 넣기에도 좋습니다.

다만 처음부터 너무 완벽하게 하려고 하면 부담이 큽니다. 시작 규칙은 세 개만 잡으면 충분합니다.

1. md 파일마다 frontmatter를 넣는다.
2. `type`, `title`, `description`, `tags`, `timestamp`만 우선 쓴다.
3. 에러, 개념, 프로젝트, 논문을 분리해서 저장한다.

가장 먼저 만들면 좋은 것은 이 구조입니다.

```text
knowledge/
├── index.md
├── errors/
├── ml/
├── infra/
└── projects/
```

이 정도만 해도 지금까지 쌓인 GUAM, AutoGluon, LM Studio, Hermes, CUDA, PyTorch, CS 공부 내용을 꽤 체계적으로 정리할 수 있습니다.

---

### 💡 답변 (Assistant)
파일 내용은 OKF(Open Knowledge Format) 초안이네요. 개인 지식관리용으로 쓸 수 있는지, 어떤 구조로 적용하면 좋은지 중심으로 바로 분석해볼게요.

---

### ❓ 질문 (User)
이거를 어디에 저장하고 보관하는게 좋을까? 로컬에 vscode 로 관리한 다음 github에서 관리하는게 좋을까 아니면 옵시디언과 같은 도구를 이용하는게 좋을까

### 💡 답변 (Assistant)
좋은 질문이에요. 이건 단순히 “어디에 저장할까”가 아니라, 앞으로 지식을 **얼마나 오래, 안전하게, AI 친화적으로 굴릴 것인가**의 선택이라서 기준을 나눠서 판단해보겠습니다.

---

### 💡 답변 (Assistant)
제 추천은 **“로컬 폴더를 원본으로 두고, Obsidian + VS Code를 같이 쓰며, GitHub private repo로 백업/버전관리”**입니다.

즉, 둘 중 하나를 고르는 문제가 아니라 이렇게 가져가는 게 제일 좋습니다.

```text
로컬 폴더 = 진짜 원본
Obsidian = 읽고 쓰고 연결하는 도구
VS Code = 구조 정리, 검색, 일괄 수정, Git 관리
GitHub private repo = 백업 + 버전관리 + 장기 보관
```

OKF 자체가 “Markdown 파일 + YAML frontmatter + 폴더 구조”를 전제로 한 형식이라서, 전용 앱보다 **파일 시스템 기반 관리**와 잘 맞습니다. 문서에서도 OKF를 “디렉터리 안의 Markdown 파일들과 YAML frontmatter”로 설명하고, Git repo 배포를 권장 형태로 제시합니다. fileciteturn0file0

## 결론부터 말하면

사용자님에게는 이 방식이 제일 좋습니다.

```text
C:/Users/<사용자명>/Documents/knowledge/
또는
C:/dev/knowledge/
```

이 폴더를 만든 다음:

1. **Obsidian Vault로 연다**
2. **VS Code에서도 같은 폴더를 연다**
3. **GitHub private repository에 연결한다**

Obsidian은 노트를 Markdown plain text 파일로 로컬 vault 폴더에 저장합니다. 즉, Obsidian을 쓰더라도 파일은 여전히 일반 `.md` 파일이라 VS Code, Git, Python 스크립트, AI 도구에서 그대로 다룰 수 있습니다. citeturn151029search1

GitHub는 private repository를 만들 수 있고, private repo는 본인과 명시적으로 접근 권한을 준 사람만 접근할 수 있습니다. 다만 클라우드에 올라가는 것이므로 API key, 비밀번호, 주민등록번호, 회사 기밀 같은 것은 넣지 않는 게 좋습니다. citeturn151029search10

---

## 왜 Obsidian만 쓰는 것보다 이 조합이 좋은가

Obsidian만 쓰면 **연결형 사고**에는 좋습니다. 예를 들어:

```markdown
[[AutoGluon]]
[[CUDA 설치]]
[[ModuleNotFoundError]]
[[GUAM 프로젝트]]
```

이런 식으로 지식 간 연결을 만들기 좋습니다. 특히 CS 공부, ML 개념, 에러 해결, 프로젝트 로그처럼 계속 연결되는 지식에는 Obsidian이 편합니다.

하지만 Obsidian만 쓰면 다음이 약합니다.

```text
- Git commit 관리
- 대량 파일 수정
- YAML frontmatter 검사
- Python 스크립트로 md 파일 분석
- 폴더 구조 리팩토링
- 코드와 문서 동시 관리
```

이건 VS Code가 훨씬 강합니다.

반대로 VS Code만 쓰면 지식관리 앱 특유의 편의성이 약합니다.

```text
- 백링크
- 그래프 뷰
- 빠른 문서 연결
- 데일리 노트
- 태그 기반 탐색
- 읽기 좋은 미리보기
```

그래서 **Obsidian은 지식 탐색/작성용**, **VS Code는 구조 관리/정리용**, **GitHub는 백업/버전관리용**으로 나누는 게 제일 안정적입니다.

---

## 추천 구조

처음에는 이렇게 시작하세요.

```text
knowledge/
├── index.md
├── log.md
├── ml/
│   ├── index.md
│   ├── autogluon.md
│   ├── pytorch.md
│   └── guam.md
├── infra/
│   ├── index.md
│   ├── ubuntu.md
│   ├── cuda.md
│   └── uv-python.md
├── errors/
│   ├── index.md
│   ├── module-not-found.md
│   ├── pip-editable-install.md
│   └── lmstudio-empty-stream.md
├── cs/
│   ├── index.md
│   ├── database.md
│   ├── operating-system.md
│   └── network.md
├── algorithms/
│   ├── index.md
│   ├── bfs-dfs.md
│   ├── dp.md
│   └── dijkstra.md
└── projects/
    ├── index.md
    ├── guam.md
    ├── automl-report.md
    └── kakaotalk-summary-bot.md
```

사용자님은 설치 오류, ML 실험, CS 공부, 알고리즘, 프로젝트 기록이 모두 섞여 있기 때문에 `errors/`, `ml/`, `infra/`, `projects/`는 반드시 분리하는 게 좋습니다.

---

## GitHub에는 private repo로 올리세요

repo 이름은 이런 식이면 충분합니다.

```text
knowledge-base
personal-knowledge
jeongmin-knowledge
ml-knowledge-base
```

저라면 이렇게 하겠습니다.

```text
jeongmin-knowledge
```

그리고 GitHub에서는 반드시 **Private**로 생성하세요.

공개해도 되는 글만 나중에 따로 public repo나 블로그로 빼면 됩니다. 처음부터 public으로 시작하면 에러 로그, 경로, 이메일, 로컬 환경 정보 같은 것이 섞일 수 있어서 위험합니다.

---

## Obsidian Sync는 필요할까?

처음에는 없어도 됩니다.

기본 추천은:

```text
PC 한 대 중심 → GitHub private repo만으로 충분
여러 기기에서 자주 사용 → Obsidian Sync 고려
모바일에서도 자주 수정 → Obsidian Sync가 Git보다 편함
```

Obsidian Sync는 공식적으로 end-to-end encryption과 AES-256 암호화, note version history를 제공한다고 설명합니다. 그래서 여러 기기 동기화가 목적이라면 편한 선택입니다. citeturn151029search5

다만 지금 단계에서는 돈 내고 Sync부터 쓰기보다, 먼저 **로컬 + GitHub private**로 습관을 만드는 게 좋습니다.

Obsidian Git 플러그인도 있긴 합니다. 자동 commit, pull, push를 Obsidian 안에서 할 수 있게 해주는 커뮤니티 플러그인입니다. 다만 모바일 쪽은 불안정하다는 안내가 있으므로, 초반에는 VS Code나 터미널에서 직접 Git을 쓰는 쪽이 더 안전합니다. citeturn151029search8

---

## 실제 운영 방식

매일 쓰는 흐름은 이렇게 잡으면 됩니다.

```text
1. Obsidian에서 새 노트 작성
2. 관련 노트 링크 연결
3. VS Code에서 폴더 구조나 frontmatter 정리
4. 하루 끝에 Git commit
5. GitHub private repo로 push
```

예를 들어 오늘 GUAM 문제를 정리한다면:

```text
errors/module-not-found-guam.md
projects/guam.md
ml/autogluon.md
infra/python-package-path.md
```

이렇게 나누고 서로 링크합니다.

```markdown
관련 문서:
- [GUAM 프로젝트](../projects/guam.md)
- [Python package path](../infra/python-package-path.md)
- [AutoGluon](../ml/autogluon.md)
```

---

## `.gitignore`는 이렇게 시작하면 좋습니다

Obsidian 설정을 어디까지 Git에 넣을지는 취향이지만, 처음에는 불필요한 workspace 파일은 제외하는 게 좋습니다.

```gitignore
# OS
.DS_Store
Thumbs.db

# Obsidian local workspace
.obsidian/workspace.json
.obsidian/workspace-mobile.json

# Trash
.trash/

# Temporary files
*.tmp
*.bak

# Large local assets if needed
assets/raw/
assets/large/
```

`.obsidian/` 전체를 무조건 ignore할 수도 있지만, 테마나 플러그인 설정까지 동기화하고 싶으면 일부는 commit해도 됩니다. 처음에는 위 정도만 제외하는 걸 추천합니다.

---

## 최종 추천

사용자님에게 가장 맞는 방식은 이것입니다.

```text
저장 위치:
로컬 PC의 일반 폴더

작성/탐색:
Obsidian

구조 정리/코드/일괄 수정:
VS Code

백업/버전관리:
GitHub private repository

동기화:
초기에는 GitHub만
나중에 모바일 사용량이 늘면 Obsidian Sync 고려
```

이 방식이면 OKF의 장점인 **Markdown 기반, Git 친화성, AI 친화성, 장기 보존성**을 모두 살릴 수 있습니다. Obsidian을 쓰더라도 파일은 일반 Markdown으로 남기 때문에, 나중에 Notion, 블로그, RAG 시스템, 개인 AI 에이전트로 옮기기도 쉽습니다.

---

### ❓ 질문 (User)
이거랑 차이는 뭐야??

### 💡 답변 (Assistant)
차이를 아주 간단히 말하면 이겁니다.

> **OKF는 “지식을 어떤 파일 형식으로 저장할 것인가”에 대한 규격이고, LLM Wiki는 “LLM에게 지식 베이스를 어떻게 유지보수하게 할 것인가”에 대한 운영 방식입니다.**

둘은 경쟁 관계가 아니라 **상하위 관계**에 가깝습니다.

```text
LLM Wiki = 운영 철학 / 워크플로우 / 사용 패턴
OKF      = 그 워크플로우에 쓸 수 있는 저장 포맷 / 문서 규칙
```

---

## 핵심 차이

| 구분 | OKF | LLM Wiki |
|---|---|---|
| 성격 | 포맷 명세서 | 지식관리 운영 패턴 |
| 핵심 질문 | “Markdown 지식 파일은 어떤 구조여야 하나?” | “LLM이 내 지식 베이스를 어떻게 계속 관리하게 만들까?” |
| 중심 개념 | Knowledge Bundle, Concept, YAML frontmatter, index.md, log.md | Raw sources, Wiki, Schema, Ingest, Query, Lint |
| 누가 쓰기 좋나 | 사람 + agent + 조직 간 교환 | 개인/팀이 LLM agent로 지식베이스를 키울 때 |
| 엄격함 | 비교적 명세적 | 비교적 추상적/실천적 |
| 산출물 | 규칙에 맞는 md 파일 묶음 | LLM이 계속 업데이트하는 개인 위키 |
| 비유 | 문서 저장 규격 | 위키 운영 방법론 |

OKF 문서는 “Markdown 파일 + YAML frontmatter”를 기본으로 하고, 각 지식 단위를 `Concept`로 정의하며, 일반 `.md` 파일에는 `type` 필드가 필요하다는 식으로 규칙을 정합니다. 즉 **문서가 어떤 모양이어야 하는지**를 말합니다. fileciteturn0file0

반면 LLM Wiki 문서는 “LLM이 raw source를 읽고, 요약하고, 기존 위키 페이지를 업데이트하고, 모순을 표시하고, 링크를 유지보수하게 하자”는 아이디어입니다. 즉 **LLM을 지식관리 담당자처럼 쓰는 방식**을 말합니다. fileciteturn1file0

---

## 가장 중요한 차이: OKF는 “형식”, LLM Wiki는 “행동”

예를 들어 사용자가 AutoGluon 문제를 정리한다고 해보겠습니다.

### OKF 관점

OKF는 이런 걸 정합니다.

```markdown
---
type: Error Note
title: AutoGluon ModuleNotFoundError
description: GUAM 환경에서 AutoGluon import가 실패한 문제
tags: [autogluon, guam, python, error]
timestamp: 2026-06-18T09:00:00+09:00
---

# 상황

# 에러 메시지

# 원인

# 해결 방법

# 관련 문서
```

즉, **파일 구조와 메타데이터 규칙**을 줍니다.

---

### LLM Wiki 관점

LLM Wiki는 이런 일을 하게 만들자는 겁니다.

```text
1. 에러 로그 원본을 raw sources에 저장한다.
2. LLM이 로그를 읽는다.
3. errors/autogluon-module-not-found.md를 만든다.
4. projects/guam.md에도 이 이슈를 연결한다.
5. infra/python-package-path.md도 업데이트한다.
6. index.md에 새 문서를 추가한다.
7. log.md에 오늘 처리한 내용을 기록한다.
8. 나중에 비슷한 에러가 나오면 기존 문서와 비교해서 답한다.
```

즉, **LLM이 위키를 어떻게 키우고 관리할지**를 설명합니다.

---

## 계층으로 보면 이렇게 됩니다

```text
[1] Raw Sources
    원본 자료, 에러 로그, 논문, 웹 클리핑, 강의노트

[2] LLM Wiki Workflow
    LLM이 원본을 읽고 요약, 통합, 링크, 수정, 점검

[3] OKF Format
    위키 파일을 Markdown + YAML frontmatter 규칙으로 저장

[4] Tools
    Obsidian, VS Code, GitHub, Codex, Claude Code 등
```

LLM Wiki 문서에는 세 계층이 나옵니다.

```text
Raw sources
The wiki
The schema
```

원본 자료는 수정하지 않고, LLM이 생성한 wiki layer를 따로 유지하며, `CLAUDE.md`나 `AGENTS.md` 같은 schema 문서로 LLM에게 규칙을 알려주는 방식입니다. fileciteturn1file0

OKF는 이 중에서 특히 **The wiki layer를 어떤 파일 형식으로 만들 것인가**에 대한 답으로 쓰기 좋습니다.

---

## 내 판단: 둘 중 하나를 고르는 게 아니라 같이 쓰는 게 맞음

사용자님에게는 이 조합이 제일 좋습니다.

```text
LLM Wiki = 전체 운영 방식
OKF = 실제 md 파일 포맷
Obsidian = 읽고 탐색하는 UI
VS Code = 수정, 검색, Git 관리
GitHub private repo = 백업과 버전관리
```

즉, 이렇게 정리하면 됩니다.

```text
나는 LLM Wiki 방식으로 지식베이스를 운영한다.
다만 파일 포맷은 OKF 스타일을 따른다.
```

이게 가장 안정적입니다.

---

## 실제 폴더 구조는 이렇게 가면 좋습니다

```text
knowledge/
├── AGENTS.md
├── index.md
├── log.md
├── raw/
│   ├── articles/
│   ├── papers/
│   ├── error-logs/
│   └── transcripts/
├── wiki/
│   ├── ml/
│   ├── infra/
│   ├── errors/
│   ├── cs/
│   ├── algorithms/
│   └── projects/
└── assets/
```

여기서 역할은 이렇습니다.

```text
raw/       = 원본. 가능한 수정하지 않음.
wiki/      = LLM이 정리한 지식 문서.
AGENTS.md  = LLM에게 주는 운영 규칙.
index.md   = 전체 목차.
log.md     = 변경 기록.
assets/    = 이미지, 첨부 파일.
```

OKF만 보면 `raw/`와 `AGENTS.md`는 필수 개념이 아닙니다. 그런데 LLM Wiki 방식에서는 이 둘이 매우 중요합니다. 특히 `AGENTS.md`는 “LLM이 앞으로 이 지식베이스를 어떻게 다뤄야 하는지”를 적는 운영 매뉴얼입니다.

---

## 사용자님에게 맞춘 최종 추천

사용자님은 지금 단순 노트 앱보다 **장기적인 ML/CS/프로젝트/에러 해결 지식 축적 시스템**이 필요합니다. 그래서 이렇게 가는 게 좋습니다.

```text
1. Obsidian Vault 하나를 만든다.
2. 그 Vault 자체를 GitHub private repo로 관리한다.
3. raw/에는 원본 자료를 넣는다.
4. wiki/에는 OKF 스타일의 정리 문서를 둔다.
5. AGENTS.md에 LLM Wiki 운영 규칙을 쓴다.
6. ChatGPT/Codex/Claude Code에게 raw를 읽고 wiki를 업데이트하게 한다.
```

정리하면:

> **LLM Wiki는 “LLM이 지식관리 비서가 되는 방식”이고, OKF는 “그 결과물을 저장하는 Markdown 규격”입니다.**

따라서 사용자님은 **LLM Wiki를 운영 모델로 채택하고, OKF를 문서 포맷으로 쓰는 방식**이 가장 좋습니다.

---

### ❓ 질문 (User)
아 그러면 하나의 파일로 운영하기 보다는 지식 정리는 LLM wiki 로 하고, 여기서 나온 정보들은 OKF 로 관리를 하면 된다. 이말이지?

### 💡 답변 (Assistant)
맞아요. 정확히 이해하셨어요.

다만 표현을 조금 더 정확히 하면:

> **지식관리 “운영 방식”은 LLM Wiki로 하고, 실제 저장되는 문서 “형식”은 OKF 스타일로 맞추면 된다**는 뜻입니다.

즉, 하나의 큰 파일에 전부 때려 넣는 방식이 아니라, **여러 개의 Markdown 파일로 쪼개서 관리**하는 게 핵심입니다.

```text
원본 자료(raw) 
    ↓ LLM이 읽고 정리
LLM Wiki 방식으로 구조화
    ↓
OKF 스타일의 Markdown 문서들로 저장
```

## 역할을 나누면 이렇게 됩니다

```text
LLM Wiki
= 어떻게 운영할 것인가?
= LLM이 원본을 읽고, 요약하고, 링크 걸고, 기존 문서를 업데이트하는 방식

OKF
= 어떤 형식으로 저장할 것인가?
= Markdown + YAML frontmatter + index.md + log.md 구조
```

LLM Wiki 문서는 원본 자료를 `raw sources`, LLM이 관리하는 `wiki`, 그리고 LLM에게 규칙을 알려주는 `schema` 세 계층으로 나눕니다. 핵심은 LLM이 단순히 검색만 하는 게 아니라, 새 자료를 읽고 기존 위키에 통합하면서 지식이 누적되게 하는 것입니다. fileciteturn1file0

OKF는 그 결과물을 저장할 때 쓸 수 있는 규칙입니다. 예를 들어 각 지식 문서를 하나의 `Concept`로 보고, Markdown 파일 맨 위에 YAML frontmatter를 두고, 최소한 `type` 필드를 포함하도록 합니다. fileciteturn0file0

## 그래서 실제 운영은 이렇게 하면 됩니다

```text
knowledge/
├── AGENTS.md
├── index.md
├── log.md
├── raw/
│   ├── articles/
│   ├── papers/
│   ├── error-logs/
│   └── transcripts/
└── wiki/
    ├── ml/
    ├── infra/
    ├── errors/
    ├── cs/
    ├── algorithms/
    └── projects/
```

여기서:

```text
raw/
= 원본 자료 보관소
= 수정하지 않는 자료
= 에러 로그, 논문 PDF, 웹 클리핑, 강의 노트 원본

wiki/
= LLM이 정리한 지식 문서
= OKF 스타일 Markdown 파일들

AGENTS.md
= LLM에게 주는 운영 규칙
= “새 자료가 들어오면 어떻게 처리하라”는 지침

index.md
= 전체 목차

log.md
= 변경 이력
```

## 예를 들어 GUAM 에러를 정리한다면

원본은 여기에 둡니다.

```text
raw/error-logs/2026-06-18-guam-module-not-found.md
```

LLM이 그걸 읽고 정리한 문서는 여기에 만듭니다.

```text
wiki/errors/guam-module-not-found.md
wiki/projects/guam.md
wiki/infra/python-package-path.md
```

각 문서는 OKF 스타일로 작성합니다.

```markdown
---
type: Error Note
title: GUAM ModuleNotFoundError
description: GUAM 패키지 설치 후 import가 실패한 문제와 해결 과정
tags: [guam, python, package, error]
timestamp: 2026-06-18T09:00:00+09:00
---

# 상황

# 에러 메시지

# 원인

# 해결 방법

# 관련 문서
```

## 결론

네, 방향은 이겁니다.

```text
하나의 파일로 모든 지식을 관리하지 않는다.

대신:
1. 원본은 raw/에 보관한다.
2. LLM이 LLM Wiki 방식으로 정리한다.
3. 정리된 결과는 wiki/ 안에 OKF 스타일 md 파일로 저장한다.
4. Obsidian으로 읽고 탐색한다.
5. VS Code와 GitHub로 구조 관리와 백업을 한다.
```

쉽게 말하면:

> **LLM Wiki는 일하는 방식이고, OKF는 파일 저장 규칙입니다.**

이 조합이 지금 사용자님 상황에는 가장 잘 맞습니다.

---

### ❓ 질문 (User)
아 내말은 굳이 llm wiki 와 okf 를 하나의 문서로 합쳐서 관리하는거 보다는 따로 들고 있는게 낫지 않겠냐? 라는 질문이었어

### 💡 답변 (Assistant)
아, 네. 그 질문이면 **“따로 들고 있는 게 낫다”**가 제 답입니다.

즉, **LLM Wiki 문서와 OKF 문서를 하나로 합쳐서 하나의 통합 문서처럼 관리하는 건 비추천**입니다. 둘은 성격이 다르기 때문입니다.

```text
LLM Wiki = 운영 철학 / 워크플로우 문서
OKF      = 저장 포맷 / 문서 구조 규격
```

LLM Wiki 문서는 “LLM이 어떻게 원본 자료를 읽고, 위키를 업데이트하고, index/log를 관리하고, lint까지 할 것인가”를 설명하는 **운영 패턴 문서**입니다. 특히 raw sources, wiki, schema 세 계층을 나누고, ingest/query/lint 같은 작업 흐름을 설명합니다. fileciteturn1file0

반면 OKF는 “Markdown 파일 하나를 어떤 구조로 작성할 것인가”, “frontmatter에 어떤 필드를 둘 것인가”, “index.md와 log.md는 어떤 의미인가”를 정의하는 **파일 포맷 명세**에 가깝습니다. fileciteturn0file0

그래서 둘을 합치면 오히려 애매해집니다.

---

## 추천 관리 방식

이렇게 분리해두는 게 좋습니다.

```text
knowledge/
├── AGENTS.md
├── references/
│   ├── llm-wiki.md
│   └── okf-v0.1.md
├── raw/
├── wiki/
├── index.md
└── log.md
```

역할은 이렇게 보면 됩니다.

```text
references/llm-wiki.md
= 이 지식베이스를 어떤 방식으로 운영할지 참고하는 철학/패턴 문서

references/okf-v0.1.md
= wiki/ 안의 md 파일들을 어떤 형식으로 쓸지 참고하는 포맷 문서

AGENTS.md
= 실제로 내 지식베이스에서 LLM이 따라야 할 구체 규칙

wiki/
= 실제 지식 문서들

raw/
= 원본 자료
```

핵심은 **원본 문서 두 개는 reference로 보관**하고, 실제 적용 규칙은 `AGENTS.md`에 따로 요약해서 쓰는 겁니다.

---

## 왜 합치면 별로인가

하나로 합치면 이런 문제가 생깁니다.

```text
1. LLM Wiki의 추상적 운영 아이디어와 OKF의 구체 포맷 규칙이 섞임
2. 나중에 OKF 버전이 바뀌면 문서 전체를 다시 손봐야 함
3. 내 개인 규칙과 원문 규격이 뒤섞여서 출처가 불명확해짐
4. LLM에게 줄 지시문이 길어지고 모호해짐
5. “원문 reference”와 “내가 실제로 채택한 규칙”을 구분하기 어려워짐
```

특히 5번이 중요합니다. 사용자가 실제로 필요한 건 원문 전체가 아니라, 그중에서 **내 지식관리 시스템에 채택할 규칙**입니다.

---

## 가장 좋은 방식

저라면 이렇게 합니다.

```text
1. LLM Wiki 원문은 references/llm-wiki.md에 그대로 보관
2. OKF 원문은 references/okf-v0.1.md에 그대로 보관
3. 둘을 읽고 내가 채택한 운영 규칙만 AGENTS.md에 작성
4. 실제 지식 문서는 wiki/ 안에 OKF 스타일로 작성
```

즉, 구조는 이렇게 됩니다.

```text
원문 문서들
  └── references/

내 운영 규칙
  └── AGENTS.md

실제 지식 산출물
  └── wiki/
```

---

## 한 문장 결론

맞습니다. **LLM Wiki와 OKF는 하나로 합치지 말고, 각각 reference 문서로 따로 보관한 뒤, 실제 운영 규칙만 `AGENTS.md`에 추려서 쓰는 게 가장 좋습니다.**

이렇게 하면 원문은 보존되고, 실제 시스템은 깔끔하게 운영됩니다.

---

### ❓ 질문 (User)
# Enrichment Agent — an OKF proof of concept

### 📖 [Read the Open Knowledge Format v0.1 specification → SPEC.md](SPEC.md)

> **This repository is primarily about the [Open Knowledge Format
> (OKF)](SPEC.md).**
>
> OKF is a **universal, vendor-neutral format** for representing knowledge
> as plain markdown files with YAML frontmatter. It is **not tied to any
> particular agent, framework, model provider, or serving system**. The
> goal is simple:
>
> - **Anyone can produce** OKF — humans authoring by hand, agents built on
>   any framework (Google ADK, LangChain, custom), export pipelines from
>   existing catalogs (Dataplex, Unity Catalog, Collibra, …), or scripts
>   walking a database.
> - **Anyone can serve and consume** OKF — a static file server, a
>   knowledge-management UI (Obsidian, Notion, MkDocs), an LLM loading
>   files into context, a search index, or a graph viewer like the one
>   bundled in this repo.
>
> The agent below is a **proof of concept** demonstrating *one* way to
> produce OKF bundles automatically. The format itself is the
> contribution; this agent and the visualizer exist to make the format
> tangible at both ends — production and consumption.
>
> **See OKF in practice** — three ready-to-browse bundles produced by this
> agent, checked into [`bundles/`](bundles/):
>
> - [`bundles/ga4/`](bundles/ga4/) — GA4 e-commerce dataset
>   ([viz.html](bundles/ga4/viz.html))
> - [`bundles/stackoverflow/`](bundles/stackoverflow/) — Stack Overflow
>   public dataset ([viz.html](bundles/stackoverflow/viz.html))
> - [`bundles/crypto_bitcoin/`](bundles/crypto_bitcoin/) — Bitcoin
>   blocks/transactions ([viz.html](bundles/crypto_bitcoin/viz.html))

A reference agent that ingests metadata from a pluggable source and emits an
**[OKF](SPEC.md) bundle**: a directory of markdown documents with YAML
frontmatter that catalog tools, downstream agents, and humans can all read.

Built on the Google [Agent Development Kit](https://adk.dev/) with Gemini as the
model backend. BigQuery is the first source implementation; the
`Source` interface is designed to grow.

## Why OKF?

OKF represents catalog knowledge as plain markdown files with YAML
frontmatter, organized in a directory hierarchy. That choice unlocks a few
properties that are hard to get from a service-owned metadata store:

- **Human- and agent-readable.** No SDK or query language stands between a
  reader and the content. An engineer can `cat` a concept; an LLM can ingest
  it verbatim into context.
- **Version-controllable out of the box.** Bundles live in git. Pull
  requests, line-by-line diffs, blame, and review workflows just work —
  knowledge curation becomes a normal software-engineering activity.
- **Portable and lock-in free.** A bundle is a directory. Ship it as a
  tarball, host it in any repo, mount it from any filesystem, or sync it to
  any system that speaks files. No proprietary API stands between you and
  your metadata.
- **Mixes structured and unstructured data deliberately.** Use frontmatter
  for the few fields you want to query, filter, or index on (`type`,
  `resource`, `tags`, `timestamp`); use the markdown body for the prose,
  schemas, and example queries that LLMs and humans actually read.
- **Minimally opinionated, freely extensible.** A small set of required
  keys ensures interoperability, but bundles can carry arbitrary extra
  frontmatter keys and arbitrary body sections without breaking
  consumers.
- **Composes with existing tooling.** Many knowledge tools — Notion,
  Obsidian, MkDocs, Hugo, Jekyll — already speak markdown plus YAML
  frontmatter, so bundles can be browsed, edited, or rendered without
  custom UI.
- **Progressive disclosure built in.** Auto-generated `index.md` files
  let an agent or human navigate the hierarchy one level at a time
  instead of loading the entire bundle into context.
- **Graph-shaped, not just tree-shaped.** Concepts link to each other via
  normal markdown links, expressing relationships richer than the
  parent/child implied by the directory layout.

The net effect is that enrichment agents, consumption agents, and humans
collaborate on the same artifacts in the same way they already collaborate
on source code.

## Install

```
python3.13 -m venv .venv
.venv/bin/pip install --index-url https://pypi.org/simple/ -e .[dev]
```

## Credentials

- BigQuery: `gcloud auth application-default login` plus a project for billing
  (`gcloud config set project <id>`). Public datasets are readable, but the
  caller's project is billed for query bytes.
- Gemini: set `GEMINI_API_KEY` (AI Studio) **or** use Vertex AI by setting
  `GOOGLE_GENAI_USE_VERTEXAI=true`, `GOOGLE_CLOUD_PROJECT=<id>`, and
  `GOOGLE_CLOUD_LOCATION=<region>`.

## How enrichment works

Enrichment runs in two passes. The **BQ pass** writes one OKF doc per
concept the source advertises, using BigQuery metadata alone. The **web
pass** then runs the LLM as its own crawler: it receives a list of seed
URLs (provided via `--web-seed` or `--web-seed-file`), fetches the seeds
via the `fetch_url` tool, and decides which outbound links are worth
following based on whether they look like authoritative documentation for
the existing concepts. For each page it fetches, the agent chooses to
(a) enrich one or more existing concept docs, (b) mint a standalone
`references/<slug>` doc, or (c) skip. A hard `--web-max-pages` cap and a
same-domain allowed-hosts filter (configurable via `--web-allowed-host`)
are enforced inside the tool, so the agent cannot overrun. Use `--no-web`
to skip the web pass.

## Run

Minimum invocation — point at a BigQuery dataset and a bundle output
directory. Seeds for the web pass are explicit; omit them (or pass
`--no-web`) to run BQ-only:

```
.venv/bin/python -m enrichment_agent enrich \
    --source bq \
    --dataset <project>.<dataset> \
    --web-seed-file <path/to/seeds.txt> \
    --out ./bundles/<name>
```

Iterate on a single concept by adding `--concept <type>/<name>` (e.g.
`--concept tables/events_`); repeatable.

## Samples

Each sample pairs a **recipe** (`samples/<name>/`, with the seed URLs and
exact `enrich` command) with the **produced bundle** (`bundles/<name>/`)
that the recipe generated. Open the recipe to reproduce; open the bundle
to browse the result directly.

- **GA4 Google Merchandise Store** — public e-commerce dataset, seeded
  with canonical GA4 BigQuery Export documentation URLs.
  · [recipe](samples/ga4_merch_store/README.md)
  · [bundle](bundles/ga4/)
  · [viz.html](bundles/ga4/viz.html)
- **Stack Overflow** — public dataset (mirror of the Stack Exchange Data
  Dump), seeded with the community's canonical schema references.
  Exercises multi-concept enrichment from cross-cutting docs pages.
  · [recipe](samples/stackoverflow/README.md)
  · [bundle](bundles/stackoverflow/)
  · [viz.html](bundles/stackoverflow/viz.html)
- **Bitcoin (crypto)** — public dataset (blocks, transactions, inputs,
  outputs) from the `bitcoin-etl` pipeline. Exercises cross-table
  foreign-key relationships in prose.
  · [recipe](samples/crypto_bitcoin/README.md)
  · [bundle](bundles/crypto_bitcoin/)
  · [viz.html](bundles/crypto_bitcoin/viz.html)

## Visualize

The `visualize` subcommand renders any OKF bundle as a **self-contained
interactive HTML file** — one file, no backend, no install on the
viewing side. Open it in any modern browser, share it as an artifact,
host it on a static file server, or commit it next to the bundle (as
this repo does).

The viewer is itself a proof-of-concept *consumer* of OKF, mirroring
the way the enrichment agent is a proof-of-concept *producer*. OKF
bundles can be consumed by anything that reads markdown; this is just
one shape.

### What it shows

- A **force-directed graph** of every concept in the bundle, with
  colored nodes by type (datasets, tables, references, …) and directed
  edges drawn from each cross-link in the markdown bodies.
- A **detail panel** for the selected concept showing its frontmatter
  (description, resource link, tags) and its rendered markdown body —
  with internal `[…](/path/to/concept.md)` links rewired to navigate
  within the viewer instead of following the path.
- A **"Cited by" backlinks** list under each concept (computed from the
  reverse of the link graph).
- A **search box** (matches title, concept id, and tags), a **type
  filter**, and switchable graph layouts (cose / concentric /
  breadth-first / circle / grid).

### Generate

```
.venv/bin/python -m enrichment_agent visualize --bundle ./bundles/<name>
```

That writes `bundles/<name>/viz.html`. Flags:

| Flag           | Default                | Description                                 |
|----------------|------------------------|---------------------------------------------|
| `--bundle`     | *(required)*           | Bundle root directory.                      |
| `--out`        | `<bundle>/viz.html`    | Output HTML path.                           |
| `--name`       | bundle directory name  | Display name shown in the viewer header.    |

Example, writing the output somewhere else and overriding the header:

```
.venv/bin/python -m enrichment_agent visualize \
    --bundle ./bundles/crypto_bitcoin \
    --out /tmp/btc.html \
    --name "Bitcoin OKF"
```

### How it's built

The HTML embeds the bundle as a JSON blob and uses
[Cytoscape.js](https://js.cytoscape.org/) for the graph and
[marked](https://marked.js.org/) for in-browser markdown rendering,
both loaded from a CDN. No data leaves the page; the bundle is parsed
once at generation time and serialized into the file.

## Tests

```
.venv/bin/pytest
```

okf - readme.md 인데 분석해줘.

### 💡 답변 (Assistant)
이번 README는 앞의 `SPEC.md`와 성격이 또 다릅니다. 핵심은 “OKF가 뭔가”가 아니라, **OKF 번들을 자동으로 생성하고 시각화하는 예제 구현체**를 설명하는 문서예요.

---

### 💡 답변 (Assistant)
이 README는 **OKF 자체 설명서라기보다는, OKF를 실제로 자동 생성해보는 “샘플 프로젝트/구현체” 설명서**입니다.

앞에서 본 문서들을 세 층으로 나누면 이렇게 됩니다.

```text
LLM Wiki 문서
= 지식관리 운영 패턴

OKF SPEC.md
= 지식을 저장하는 파일 포맷 규격

OKF README.md
= OKF 포맷을 실제로 생성·시각화하는 예제 프로젝트 설명
```

즉, 이번 README는 **“OKF를 이런 식으로 agent가 만들 수 있다”**를 보여주는 proof of concept입니다.

---

## 1. 이 README의 정체

문서 제목이 이미 핵심을 말합니다.

```text
Enrichment Agent — an OKF proof of concept
```

여기서 중요한 단어는 두 개입니다.

```text
Enrichment Agent
= 원본 메타데이터를 읽고 지식 문서를 풍부하게 만드는 agent

OKF proof of concept
= OKF가 실제로 동작할 수 있음을 보여주는 예제 구현
```

즉 이 repo는 **OKF 표준 자체**가 아니라, OKF 표준을 써서 다음을 하는 예제입니다.

```text
BigQuery 데이터셋 읽기
→ 테이블, 데이터셋, reference 문서 생성
→ Markdown + YAML frontmatter 형태의 OKF bundle 출력
→ HTML graph viewer로 시각화
```

OKF 자체는 Markdown 파일과 YAML frontmatter로 지식을 표현하는 포맷이고, 특정 agent나 framework에 종속되지 않는다고 설명합니다. fileciteturn0file0  
이 README는 그중 **Google ADK + Gemini + BigQuery**를 이용한 하나의 구현 예시입니다.

---

## 2. README가 설명하는 시스템 구조

이 repo의 구조는 대략 이렇습니다.

```text
Source
  ↓
Enrichment Agent
  ↓
OKF Bundle
  ↓
Visualizer / Consumer
```

조금 더 구체적으로는:

```text
BigQuery dataset
  ↓
BQ metadata pass
  ↓
기본 OKF 문서 생성
  ↓
Web enrichment pass
  ↓
공식 문서나 seed URL을 읽고 내용 보강
  ↓
bundles/<name>/ 에 Markdown 문서 저장
  ↓
viz.html 로 graph viewer 생성
```

이 README에서 말하는 enrichment는 **단순 요약**이 아니라, 기존 concept 문서를 보강하는 작업입니다. 예를 들어 BigQuery 테이블 메타데이터만으로 만든 문서에, 공식 문서에서 가져온 설명·관계·주의사항을 추가하는 식입니다.

---

## 3. SPEC.md와 README.md의 차이

가장 중요합니다.

| 구분 | SPEC.md | README.md |
|---|---|---|
| 성격 | 포맷 명세 | 구현체 설명 |
| 질문 | “OKF 문서는 어떤 구조여야 하나?” | “OKF 문서를 자동으로 어떻게 만들 수 있나?” |
| 중심 내용 | Concept, frontmatter, index.md, log.md, link, citation | enrichment agent, BigQuery, web pass, samples, visualizer |
| 범용성 | 높음 | 특정 구현에 가까움 |
| 사용자에게 필요한 정도 | 매우 중요 | 참고용 |
| 바로 적용 여부 | 적용 추천 | 지금은 보류 추천 |

SPEC.md는 **규칙**입니다.

```markdown
---
type: Concept
title: ...
description: ...
tags: [...]
---
```

이런 식으로 문서를 어떻게 써야 하는지 알려줍니다. OKF에서는 일반 concept 문서에 YAML frontmatter가 필요하고, 최소한 `type` 필드가 필요합니다. fileciteturn0file0

반면 README.md는 **그 규칙을 이용해서 자동화 도구를 만든 예제**입니다.

```bash
python -m enrichment_agent enrich ...
python -m enrichment_agent visualize ...
```

이런 실행 방법이 나옵니다.

---

## 4. LLM Wiki와 README.md의 차이

이것도 구분해야 합니다.

| 구분 | LLM Wiki | OKF README |
|---|---|---|
| 목적 | 개인/팀 지식베이스를 LLM이 유지보수 | OKF bundle을 자동 생성하는 reference agent |
| 대상 | 넓음: 공부, 프로젝트, 논문, 회의, 책, 여행 등 | 주로 데이터 카탈로그, BigQuery metadata |
| 운영 방식 | raw → wiki → schema | source → enrichment agent → bundle |
| 핵심 파일 | AGENTS.md, raw/, wiki/, index.md, log.md | SPEC.md, enrichment_agent, bundles/, samples/, viz.html |
| 사용자가 따라 할 부분 | 매우 많음 | 일부만 참고 |

LLM Wiki는 “LLM이 지식을 계속 축적·갱신하는 방식”에 가깝습니다. 원본 자료를 raw sources로 두고, LLM이 wiki 문서를 만들고, schema 문서로 운영 규칙을 관리하는 구조입니다. fileciteturn1file0

OKF README는 더 좁습니다. 특히 **BigQuery 데이터셋을 읽어 OKF 문서를 자동 생성하는 agent**에 초점이 있습니다.

---

## 5. 이 README에서 건질 만한 핵심 아이디어

사용자님 개인 지식관리 시스템에 그대로 가져올 만한 건 다음입니다.

### 1. Producer와 Consumer를 분리하는 사고

README에서는 enrichment agent를 **producer**, visualizer를 **consumer**라고 봅니다.

이건 아주 좋은 관점입니다.

```text
Producer
= 지식 문서를 만드는 쪽
= LLM, script, 사람이 직접 작성

Consumer
= 지식 문서를 읽는 쪽
= Obsidian, VS Code, 검색기, graph viewer, LLM
```

사용자님 시스템에도 그대로 적용할 수 있습니다.

```text
Producer:
ChatGPT / Claude Code / Codex / 직접 작성

Consumer:
Obsidian / VS Code / GitHub / 나중의 RAG / 개인 agent
```

---

### 2. Bundle 단위 관리

README는 `bundles/ga4`, `bundles/stackoverflow`, `bundles/crypto_bitcoin`처럼 지식 묶음을 bundle 단위로 보여줍니다.

사용자님도 나중에 이렇게 나눌 수 있습니다.

```text
knowledge/
├── bundles/
│   ├── ml-study/
│   ├── cs-study/
│   ├── guam-project/
│   └── automl-experiments/
```

다만 처음부터 이렇게 복잡하게 나누지는 말고, 처음에는 하나의 vault 안에 `wiki/`로 시작하는 게 좋습니다.

---

### 3. index.md 기반 progressive disclosure

README에서 좋은 점은 `index.md`를 단순 목차가 아니라, LLM과 사람이 한 단계씩 탐색할 수 있는 구조로 본다는 점입니다.

이건 OKF SPEC과도 연결됩니다. OKF에서도 `index.md`는 디렉터리 내용을 점진적으로 보여주는 파일로 설명됩니다. fileciteturn0file0

개인 지식관리에서도 매우 중요합니다.

```text
wiki/ml/index.md
wiki/infra/index.md
wiki/errors/index.md
wiki/projects/index.md
```

이렇게 두면 LLM이 전체 파일을 다 읽지 않고도 “어디를 봐야 하는지” 찾기 쉬워집니다.

---

### 4. graph viewer 아이디어

README의 `visualize` 기능은 OKF bundle을 HTML 그래프로 보여줍니다.

이건 Obsidian graph view와 비슷한 역할입니다.

사용자님 입장에서는 당장 이 visualizer를 설치할 필요는 없습니다. Obsidian이 이미 graph view를 제공합니다. 하지만 나중에 GitHub Pages나 static HTML로 지식 그래프를 공유하고 싶다면 참고할 만합니다.

---

## 6. 지금 사용자님에게 필요한 정도

냉정하게 말하면, **이 README의 agent 구현은 지금 당장 필요하지 않습니다.**

이유는 이 README의 구현 대상이 주로 이런 쪽이기 때문입니다.

```text
BigQuery dataset
GA4 public dataset
Stack Overflow public dataset
Bitcoin transaction table
데이터 카탈로그
테이블 메타데이터
공식 문서 기반 enrichment
```

사용자님이 지금 하려는 것은 이쪽입니다.

```text
ML 공부
CS 공부
AutoGluon/GUAM 프로젝트
Ubuntu/CUDA/GPU 에러 해결
논문 읽기
알고리즘 정리
개인 지식관리
```

따라서 README의 코드를 바로 설치하고 실행하는 것보다, **README의 구조적 아이디어만 가져오는 게 좋습니다.**

---

## 7. 추천 보관 방식

이 README는 원문 그대로 reference로 보관하세요.

```text
knowledge/
├── references/
│   ├── okf/
│   │   ├── SPEC.md
│   │   └── README.md
│   └── llm-wiki.md
├── AGENTS.md
├── raw/
├── wiki/
├── index.md
└── log.md
```

그리고 실제 운영 규칙은 `AGENTS.md`에 따로 추려서 쓰는 게 좋습니다.

```text
references/okf/README.md
= OKF 자동 생성 예제 프로젝트 원문

references/okf/SPEC.md
= OKF 포맷 규격 원문

references/llm-wiki.md
= LLM Wiki 운영 패턴 원문

AGENTS.md
= 내 지식관리 시스템에서 실제로 따를 규칙
```

---

## 8. 내 판단

이 README를 한 문장으로 정리하면:

> **OKF가 단순한 문서 규칙에 그치지 않고, agent가 자동으로 생산하고 graph viewer가 소비할 수 있는 실전 포맷이라는 것을 보여주는 예제 repo 설명서**입니다.

사용자님에게 중요한 순서는 이렇습니다.

```text
1순위: LLM Wiki 운영 방식 이해
2순위: OKF SPEC으로 문서 형식 정하기
3순위: README의 producer/consumer, visualizer, bundle 개념만 참고
4순위: enrichment_agent 코드는 나중에 필요해지면 보기
```

지금 당장 실행할 전략은 이것입니다.

```text
LLM Wiki 방식으로 운영한다.
OKF SPEC 스타일로 wiki 문서를 작성한다.
OKF README는 자동화/시각화 예제로 reference에 보관한다.
enrichment_agent는 지금은 쓰지 않는다.
```

결론적으로, 이 README는 **사용자님의 지식관리 시스템의 중심 문서가 아니라 참고 구현 문서**입니다.  
중심은 `AGENTS.md`, `wiki/`, `raw/`, `index.md`, `log.md`가 되어야 합니다.

---

### ❓ 질문 (User)
그러면 llm wiki, okf/spec.md 만 가지고 운영하는게 낫다는거네. 템플릿 하나 작성해줘.

### 💡 답변 (Assistant)
네. 지금 단계에서는 **LLM Wiki 원문 + OKF `SPEC.md` 원문만 reference로 들고 있고**, 실제 운영 규칙은 아래처럼 **`AGENTS.md` 하나로 추려서 관리**하는 게 가장 깔끔합니다.

LLM Wiki는 `raw sources → wiki → schema` 구조와 `ingest/query/lint` 운영 방식을 제공하고, OKF는 Markdown 파일·YAML frontmatter·`index.md`·`log.md` 같은 저장 규칙을 제공합니다. fileciteturn1file0 fileciteturn0file0

아래 템플릿을 `AGENTS.md`로 저장하면 됩니다.

:::writing{variant="document" id="48137"}
# AGENTS.md — Personal Knowledge Base Operating Rules

이 문서는 이 지식베이스를 관리하는 LLM agent가 따라야 할 운영 규칙이다.

이 지식베이스는 **LLM Wiki 방식으로 운영**하고, 실제 지식 문서는 **OKF 스타일의 Markdown 문서**로 저장한다.

---

# 1. Core Principle

이 저장소의 목적은 단순한 메모 보관이 아니라, 시간이 지날수록 누적되고 갱신되는 개인 지식베이스를 만드는 것이다.

LLM agent는 단순히 원본 자료를 요약하는 것이 아니라 다음 작업을 수행해야 한다.

- 원본 자료에서 핵심 지식을 추출한다.
- 기존 wiki 문서와 연결한다.
- 기존 내용과 충돌하는 부분을 표시한다.
- 필요한 경우 기존 문서를 업데이트한다.
- 관련 문서 간 cross-link를 추가한다.
- `index.md`와 `log.md`를 갱신한다.

---

# 2. Repository Structure

기본 구조는 다음을 따른다.

knowledge/
├── AGENTS.md
├── index.md
├── log.md
├── references/
│   ├── llm-wiki.md
│   └── okf-spec.md
├── raw/
│   ├── articles/
│   ├── papers/
│   ├── error-logs/
│   ├── transcripts/
│   └── notes/
├── wiki/
│   ├── ml/
│   ├── infra/
│   ├── errors/
│   ├── cs/
│   ├── algorithms/
│   ├── projects/
│   └── papers/
└── assets/

---

# 3. Directory Roles

## references/

참고 원문을 보관한다.

예:

- `references/llm-wiki.md`
- `references/okf-spec.md`

이 파일들은 운영 철학과 문서 포맷을 이해하기 위한 reference이다.  
일반적인 지식 정리 과정에서 원문을 직접 수정하지 않는다.

## raw/

원본 자료를 보관한다.

예:

- 에러 로그
- 논문 PDF에서 추출한 텍스트
- 웹 클리핑
- 강의 노트 원본
- ChatGPT 대화 복사본
- 실험 로그

`raw/` 안의 자료는 source of truth로 간주한다.  
LLM agent는 이 파일을 읽을 수 있지만, 사용자가 명시적으로 요청하지 않는 한 수정하지 않는다.

## wiki/

LLM agent가 정리하고 유지보수하는 지식 문서를 보관한다.

`wiki/` 안의 모든 일반 Markdown 문서는 OKF 스타일을 따른다.

## assets/

이미지, 첨부파일, 다이어그램, 캡처 등을 보관한다.

---

# 4. OKF Document Rules

`wiki/` 안의 일반 지식 문서는 Markdown 파일 하나가 하나의 concept이다.

모든 concept 문서는 YAML frontmatter로 시작해야 한다.

필수 필드:

```yaml
---
type: <문서 유형>
---
```

권장 필드:

```yaml
---
type: Concept
title: 
description: 
tags: []
timestamp: 
status: active
---
```

## Recommended Types

다음 type을 우선 사용한다.

- `Concept`
- `Error Note`
- `Project`
- `Paper Note`
- `Command Note`
- `Setup Guide`
- `Study Note`
- `Decision Note`
- `Reference`

새로운 type이 필요하면 만들 수 있지만, 기존 type으로 표현 가능한 경우 기존 type을 우선 사용한다.

---

# 5. Standard Wiki Templates

## 5.1 Concept

```markdown
---
type: Concept
title:
description:
tags: []
timestamp:
status: active
---

# Summary

# Why it matters

# Key Ideas

# Examples

# Related Concepts

# Citations
```

## 5.2 Error Note

```markdown
---
type: Error Note
title:
description:
tags: [error]
timestamp:
status: solved
---

# Situation

# Error Message

# Cause

# Solution

# Prevention

# Related Concepts

# Citations
```

## 5.3 Project

```markdown
---
type: Project
title:
description:
tags: [project]
timestamp:
status: active
---

# Goal

# Current Status

# Structure

# How to Run

# Key Decisions

# Issues

# Next Actions

# Related Concepts
```

## 5.4 Paper Note

```markdown
---
type: Paper Note
title:
description:
resource:
tags: [paper]
timestamp:
status: reading
---

# One-line Summary

# Problem

# Method

# Experiments

# Key Findings

# My Understanding

# How I Can Use This

# Open Questions

# Citations
```

---

# 6. Linking Rules

문서 간 연결은 일반 Markdown link를 사용한다.

가능하면 bundle-relative 또는 repository-relative link를 사용한다.

예:

```markdown
See [AutoGluon](../ml/autogluon.md).
See [GUAM Project](../projects/guam.md).
```

LLM agent는 새 문서를 만들 때 관련 기존 문서를 찾아 cross-link를 추가해야 한다.

특히 다음 관계는 적극적으로 연결한다.

- 에러 ↔ 프로젝트
- 에러 ↔ 환경 설정
- 개념 ↔ 예제 코드
- 논문 ↔ 적용 가능한 프로젝트
- CS 개념 ↔ 알고리즘 문제
- 설치 가이드 ↔ 실제 발생한 오류

---

# 7. Ingest Workflow

새로운 원본 자료가 추가되면 LLM agent는 다음 절차를 따른다.

1. `raw/` 안의 원본 자료를 읽는다.
2. 핵심 내용을 요약한다.
3. 새 wiki 문서가 필요한지 판단한다.
4. 기존 wiki 문서에 통합할 내용이 있는지 확인한다.
5. 필요한 경우 새 concept 문서를 만든다.
6. 관련 기존 문서를 업데이트한다.
7. 문서 간 cross-link를 추가한다.
8. `index.md`를 업데이트한다.
9. `log.md`에 작업 내역을 기록한다.

원본 자료 하나가 여러 wiki 문서를 업데이트할 수 있다.

---

# 8. Query Workflow

사용자가 질문하면 LLM agent는 다음 순서로 답한다.

1. 먼저 `index.md`를 확인한다.
2. 관련성이 높은 wiki 문서를 찾는다.
3. 필요한 경우 raw source를 확인한다.
4. 답변을 작성한다.
5. 답변에서 새롭게 정리할 가치가 있는 내용은 wiki 문서로 저장하거나 기존 문서에 반영할 것을 제안한다.

질문에 대한 답이 기존 wiki에 없으면, 모른다고 말하고 필요한 source나 조사 방향을 제안한다.

---

# 9. Lint Workflow

정기적으로 LLM agent는 wiki 상태를 점검한다.

점검 항목:

- frontmatter가 없는 문서
- `type` 필드가 없는 문서
- description이 비어 있는 문서
- 고립된 문서
- 깨진 링크
- 중복 문서
- 오래된 내용
- 서로 충돌하는 주장
- tag가 과도하게 많거나 일관성이 없는 문서
- index.md에 누락된 문서
- log.md에 기록되지 않은 큰 변경 사항

Lint 결과는 필요하면 `wiki/_maintenance/` 아래에 기록한다.

---

# 10. Index Rules

`index.md`는 전체 지식베이스의 진입점이다.

각 디렉터리에도 필요하면 `index.md`를 둘 수 있다.

index 문서는 다음 형태를 따른다.

```markdown
# Section Name

- [Title](path/to/file.md) - one-line description
```

LLM agent는 새 문서를 만들거나 문서 제목·위치를 바꾸면 관련 `index.md`를 갱신해야 한다.

---

# 11. Log Rules

`log.md`는 시간순 변경 기록이다.

새로운 ingest, 큰 업데이트, lint, 구조 변경이 있으면 기록한다.

형식:

```markdown
## YYYY-MM-DD

- **Ingest**: raw 자료를 읽고 관련 wiki 문서를 생성 또는 갱신함.
- **Update**: 기존 문서를 수정함.
- **Lint**: 깨진 링크와 누락된 frontmatter를 점검함.
- **Decision**: 운영 규칙 또는 구조 변경을 결정함.
```

최신 기록이 위에 오도록 한다.

---

# 12. Writing Style

wiki 문서는 다음 스타일을 따른다.

- 한국어를 기본으로 작성한다.
- 기술 용어는 필요한 경우 영어 원어를 병기한다.
- 장황한 설명보다 재사용 가능한 구조를 우선한다.
- 에러 문서는 원인과 해결 방법을 명확히 분리한다.
- 프로젝트 문서는 현재 상태와 다음 작업을 분명히 적는다.
- 논문 문서는 “내가 어떻게 써먹을 수 있는가”를 반드시 포함한다.
- 추측은 추측이라고 표시한다.
- 확인된 사실과 개인 해석을 구분한다.

---

# 13. Safety and Privacy Rules

다음 정보는 GitHub에 올리기 전에 반드시 제거하거나 마스킹한다.

- API key
- password
- token
- private key
- 주민등록번호
- 전화번호
- 상세 주소
- 계정 인증 정보
- 회사 내부 기밀
- 공개하면 안 되는 개인 정보

에러 로그에 로컬 경로, 사용자명, 이메일, 토큰이 포함될 수 있으므로 주의한다.

---

# 14. Git Rules

이 지식베이스는 Git으로 관리한다.

권장 commit message:

```text
docs: add autogluon error note
docs: update guam project note
chore: update index and log
lint: fix broken wiki links
```

큰 변경 전에는 commit을 먼저 만든다.

---

# 15. Default Agent Behavior

LLM agent는 지식베이스를 수정할 때 다음 원칙을 따른다.

- 원본 자료는 보존한다.
- wiki 문서는 작고 명확한 단위로 나눈다.
- 하나의 큰 문서에 모든 내용을 합치지 않는다.
- 관련 문서는 반드시 링크한다.
- 새 문서를 만들면 index와 log를 갱신한다.
- 기존 문서와 충돌하는 내용이 있으면 덮어쓰기 전에 충돌을 표시한다.
- 모르는 내용은 추측해서 채우지 않는다.
- 사용자가 요청한 목적에 맞는 최소한의 구조부터 만든다.
:::

처음에는 이 정도면 충분합니다. 핵심은 **원문 reference는 보존하고, 실제 agent 운영 규칙은 `AGENTS.md`에만 모으는 것**입니다.

---
