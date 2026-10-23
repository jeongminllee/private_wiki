# 🧠 Nuri's Personal Knowledge Base (Private Wiki)

> **시간이 지날수록 지속적으로 복리처럼 축적되고 갱신되는 개인 지식베이스 아카이브**
>
> 본 저장소는 **LLM Wiki** 방식을 기반으로 운영되며, 모든 지식 문서는 **OKF(Open Knowledge Format) 스펙**을 준수하여 작성 및 관리됩니다.

---

## 📅 실시간 대시보드 & 데일리 루틴

* 📑 **[전체 지식베이스 인덱스 (index.md)](index.md)**: 지식베이스 전체 카테고리 진입점
* 🔄 **[데일리 루틴 대시보드](wiki/routine/index.md)**: 월별 AI Paper, 경제, 영어, 채용 기록 및 체크리스트 현황
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
  * [wiki/routine/days.py](wiki/routine/days.py) 또는 [run_today.bat](wiki/routine/run_today.bat) 실행으로 실행 환경의 당일 과목별 노트 및 통합 체크리스트를 생성합니다. 기존 파일은 덮어쓰지 않습니다.
  * 현재 과목 노트는 제목만 있는 빈 틀로 생성되고, 체크리스트에만 frontmatter가 들어갑니다. 과목 노트의 OKF 메타데이터 보완은 후속 정리 항목입니다.
  * 본문 입력과 실제 완료를 구분합니다. 주말 영어·신규 공고 없음 안내는 본문이 있어도 완료 체크를 자동으로 변경하지 않습니다.

저장소 루트에서 실행합니다.

```powershell
# 실행 환경의 당일 (생성 후 Enter 대기)
python wiki/routine/days.py
# 파일·형식·로컬 링크 점검 (읽기 전용)
python scripts/audit_routine.py
# 날짜별 문서는 보존하고 루틴 index만 갱신
python scripts/audit_routine.py --write-index
```

[최근 루틴 점검 기록](wiki/_maintenance/routine-audit-2026-10-13.md)에는 기존 문서의 형식·중복·출처·완료 표시 검토 후보를 정리했습니다.

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
├── CLAUDE.md                   # Claude Code 진입점 (AGENTS.md import)
├── README.md                   # GitHub 대문 문서 (현재 파일)
├── index.md                    # 전체 지식베이스 대시보드 진입점
├── log.md                      # 전체 지식베이스 변경/Ingest 히스토리
├── references/                 # 시스템 운영 규칙 및 AI 프롬프트 명세
├── raw/                        # 원본 수집 자료 (보안 관리를 위해 .gitignore 적용)
├── scripts/                    # 루틴 점검, ChatGPT·Notion import 등 유지보수 스크립트
├── assets/                     # 이미지, 포트폴리오 등 첨부 산출물
└── wiki/                       # 카테고리별 정제 마크다운 지식 문서
    ├── routine/                # 데일리 루틴 (AI Paper, Economy, Eng, Job_LLM_ML, Checklist)
    ├── cs/                     # 컴퓨터 과학 (Java, Python, 정보처리기사 등)
    ├── ml/                     # 머신러닝 이론, 수학 기초, 앙상블 기법
    ├── cv/                     # 컴퓨터 비전 (Szeliski 교재 챕터별 정리)
    ├── papers/                 # 학술 논문 요약 및 체계적 문헌고찰(SLR)
    ├── projects/               # side project & Fine-Tuned (B200 / AegisLM 등)
    ├── reading/                # 외부 자료 로컬 읽기 라이브러리
    ├── infra/                  # 시스템 인프라, 셋업 가이드, 심볼릭 링크
    ├── errors/                 # 실무 에러 트러블슈팅 노트
    ├── algorithms/             # 알고리즘 & 자료구조 문제 풀이 대시보드
    └── _maintenance/           # Lint·점검 결과 기록
```

---

## 📜 지식베이스 운영 원칙 (Core Principles)

1. **지식 복리 축적 (Compounding Knowledge)**: 수집(Raw) 및 일일 일지(Routine)에서 검증된 핵심 지식을 영구 지식(Wiki)으로 지속 승격합니다.
2. **유기적 상호 연결 (Cross-Linking)**: 모든 문서는 개념 ↔ 예제 ↔ 에러 ↔ 프로젝트 간 마크다운 링크로 연결됩니다.
3. **엄격한 보안성 (Privacy & Safety)**: API Key, 비밀번호, 기밀 경로 등은 Git 트래킹에서 전면 차단됩니다.
4. **사용자 주도 Git 통제권**: 모든 Commit 및 Push는 오직 사용자의 명시적 지시하에만 수행됩니다.
