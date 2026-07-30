# 🧠 Nuri's Personal Knowledge Base (Private Wiki)

> **시간이 지날수록 지속적으로 복리처럼 축적되고 갱신되는 개인 지식베이스 아카이브**
>
> 본 저장소는 **LLM Wiki** 방식을 기반으로 운영되며, 모든 지식 문서는 **OKF(Open Knowledge Format) 스펙**을 준수하여 작성 및 관리됩니다.

---

## 📅 실시간 대시보드 & 데일리 루틴

* 📑 **[전체 지식베이스 인덱스 (index.md)](index.md)**: 지식베이스 전체 카테고리 진입점
* 🔄 **[데일리 루틴 대시보드 (wiki/routine)](wiki/routine/)**: 매일 수행하는 AI Paper, 경제, 영어, 공채 트래킹 및 체크리스트
* 📑 **[정보처리기사 실기 대시보드](wiki/cs/engineer_info_processing/index.md)**: 기사 실기 전 과목 핵심 요약 및 기출 분석 대시보드
* 📚 **[Reading Library 대시보드](wiki/reading/index.md)**: Notion 스크랩 글, 논문, 영상 로컬 분류 아카이브

---

## 🔄 데일리 루틴 시스템 (`wiki/routine/`)

매일 수행하는 학습 및 수집 루틴을 체계적으로 관리합니다.

* **4대 루틴 영역**:
  1. 🤖 **AI Paper & Tech**: 최신 AI 논문, 릴리스 소식, 하드웨어/추론 가속 동향 브리핑
  2. 📈 **Economy**: 미국/한국 경제 아침 브리핑 및 금리/중동/시장 동향
  3. 🔤 **English**: 재사용 가능한 실무/회화 영어 말하기 템플릿 학습
  4. 💼 **Job Info**: LLM / ML / AI 엔지니어 고적합 채용 공고 분석
* **자동 생성 스크립트**:
  * [wiki/routine/days.py](wiki/routine/days.py) 또는 `run_today.bat` 클릭 한 번으로 당일 과목별 노트 및 통합 [checklist](wiki/routine/checklist/) 자동 작성.

---

## 🛠️ AI 에이전트 프롬프트 명세 (`references/`)

본 지식베이스의 정제, 분석, 멘토링을 전담하는 핵심 AI 에이전트 명세서입니다.

1. 🎓 **[정보처리기사 실기 15년 차 강사](references/instructor-prompt.md)**: 수험 개념 및 기출 디버깅 멘토
2. 💻 **[ML 엔지니어 (Nuri-Engine)](references/ml-engineer-prompt.md)**: PyTorch 가속, CUDA 튜닝, 분산 학습 전담 전문가
3. 🔬 **[ML 리서처 (Nuri-Research)](references/ml-researcher-prompt.md)**: 논문 수식 유도, 수학적 이론 해석 전담 전문가
4. 📖 **[LLM Wiki 운영 가이드](references/llm-wiki.md)**: 개인 지식베이스 아키텍처 및 Ingest/Lint 가이드

---

## 📂 저장소 디렉토리 구조 (Directory Structure)

```text
private_wiki/
├── AGENTS.md                   # 개인 지식베이스 운영 규칙 및 Git Rules
├── README.md                   # GitHub 대문 문서 (현재 파일)
├── index.md                    # 전체 지식베이스 대시보드 진입점
├── log.md                      # 전체 지식베이스 변경/Ingest 히스토리
├── references/                 # 시스템 운영 규칙 및 AI 프롬프트 명세
├── raw/                        # 원본 수집 자료 (보안 관리를 위해 .gitignore 적용)
└── wiki/                       # 카테고리별 정제 마크다운 지식 문서
    ├── routine/                # 데일리 루틴 (AI Paper, Economy, Eng, Job_LLM_ML, Checklist)
    ├── cs/                     # 컴퓨터 과학 (Java, Python, 정보처리기사 등)
    ├── ml/                     # 머신러닝 이론, 수학 기초, 앙상블 기법
    ├── papers/                 # 학술 논문 요약 및 체계적 문헌고찰(SLR)
    ├── projects/               # side project & Fine-Tuned (B200 / AegisLM 등)
    ├── reading/                # 외부 자료 로컬 읽기 라이브러리
    ├── infra/                  # 시스템 인프라, 셋업 가이드, 심볼릭 링크
    ├── errors/                 # 실무 에러 트러블슈팅 노트
    └── algorithms/             # 알고리즘 & 자료구조 문제 풀이 대시보드
```

---

## 📜 지식베이스 운영 원칙 (Core Principles)

1. **지식 복리 축적 (Compounding Knowledge)**: 수집(Raw) 및 일일 일지(Routine)에서 검증된 핵심 지식을 영구 지식(Wiki)으로 지속 승격합니다.
2. **유기적 상호 연결 (Cross-Linking)**: 모든 문서는 개념 ↔ 예제 ↔ 에러 ↔ 프로젝트 간 마크다운 링크로 연결됩니다.
3. **엄격한 보안성 (Privacy & Safety)**: API Key, 비밀번호, 기밀 경로 등은 Git 트래킹에서 전면 차단됩니다.
4. **사용자 주도 Git 통제권**: 모든 Commit 및 Push는 오직 사용자의 명시적 지시하에만 수행됩니다.
