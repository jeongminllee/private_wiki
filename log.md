# Change Log

## 2026-07-28

- **Project Note**: [AegisLM Phase F 데이터 재설계와 바이너리 분석 실험](wiki/projects/Fine_Tuned/training/aegislm_phase_f_experiment_plan_20260728.md)을 추가했다. 구현 SSOT와 별도로 Phase E 판정, F0–F4 상태, source·binary 모델 실험 사다리, 절대 gate, NuriLab 연결 순서와 다음 실행을 Wiki에서 추적하도록 구성했다.
- **Implementation**: AegisLM-B200를 `Phase E infrastructure PASS / model quality FAIL`로 종료하고 Phase F를 활성화했다. label·source·metadata를 모델 prompt에서 제외하고, source catalog/eligible manifest Parquet와 10,000 train·1,000 validation·500 blind challenge를 고정 seed로 만드는 `phase-f-source-v2` 파이프라인을 구현했다.
- **Schema**: raw executable 대신 pseudo-C, 제한된 assembly, imports·sections·strings·symbols를 받는 `aegislm.binary-analysis-record.v1`과 `present / not_observed / uncertain` 출력 계약을 추가했다. dataset·label·split·artifact path/hash는 binary prompt에서 제외하며 raw byte/payload key를 거부한다.
- **Evaluation**: source 절대 gate와 별개로 binary precision·recall·FPR·abstention·schema·evidence 및 compiler consistency를 계산하는 evaluator를 추가했다. Source와 binary adapter가 독립 gate를 통과하기 전에는 multitask, NuriLab, RAG/MCP로 진행하지 않는 중단 순서를 확정했다.
- **Docs**: [Phase F 데이터 재설계 및 바이너리 분석 실험 계획](wiki/projects/Fine_Tuned/repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md)을 SSOT로 추가하고 기존 데이터 축소 Decision Note, workbook, 데이터·평가 문서와 index를 연결했다.
- **Decision Note**: [AegisLM 데이터 축소와 통제된 무작위화 결정](wiki/projects/Fine_Tuned/training/aegislm_dataset_reduction_randomization_decision_20260728.md)을 추가했다. 33만 건·7일 학습과 빠른 loss 수렴이 실제 500건 보안 품질로 이어지지 않은 연구 흐름을 가설–관측–검증–원인–다음 가설 구조로 기록하고, 다음 train을 1–2만 건으로 축소하기로 했다.
- **Data Policy**: DiverseVul label/target 제거, BigVul before/after pair, Cybersecurity QA 분리, 중복 제거를 다음 dataset revision의 필수 조건으로 정했다. 무작위화는 고정 seed와 code hash를 사용한 표본·입력 표현 다양화로 제한하고 label, risk, JSON schema는 무작위화하지 않도록 규칙을 명시했다.
- **Experiment**: merged Qwen3-Coder-Next adapter를 vLLM `0.26.0` TP2로 서빙해 250개 취약·250개 정상 label-blind challenge를 완주했다. 누락·서버 오류·OOM은 없었지만 TP/FP/TN/FN `84/116/0/166`, precision `0.42`, recall `0.336`, FPR `0.464`, abstention `0.598`, parse `0.556`, schema `0.53`으로 모든 품질 gate를 통과하지 못했다. 222개 JSON parse 실패 중 대부분은 1,024-token 상한까지 이어진 반복 루프였고 정상 사례를 유효한 `low`로 판정한 경우는 0건이었다.
- **Audit**: 332,807개 train record를 집계해 DiverseVul 211,333개 전부의 model-visible prompt에 dataset label·target·provenance가 들어가고, assistant expected output은 전체 JSON 기준 20개 형태에 집중된 것을 확인했다. BigVul 120,897개도 입력을 취약 코드라고 먼저 알리고 전부 `high`로 학습했다. 마지막 loss `1.5e-6`은 raw-code 분석 능력보다 노출 label과 정형 target 재현에 수렴한 것으로 판정했다.
- **Decision**: 현재 adapter는 채택하지 않고 **데이터 수정 후 재학습**으로 결정했다. label/source/metadata를 제거한 raw-code prompt, 코드별 구체 근거 target, 정상 hard negative, template 중복 축소, 조기 blind gate를 다음 학습의 필수 조건으로 정했다. model-only gate를 통과하기 전에는 NuriLab·RAG·MCP 연결과 50건×3회 재현성 실험을 진행하지 않는다.
- **Update**: AegisLM 수동 파인튜닝 검증 워크북에 vLLM 0.26.0의 Qwen3-Coder-Next MoE LoRA 기동 정체를 기록했다. 세 차례의 유효한 시도, `/dev/shm`·OOM 배제 근거, 증거 로그를 남기고 adapter 품질 실패와 serving compatibility 차단을 분리했다. 같은 환경의 base-only vLLM은 startup과 실제 Chat Completions HTTP 200까지 통과해 동적 MoE LoRA 경로로 범위를 좁혔다. LLaMA-Factory/Hugging Face API는 adapter load와 추론에 성공했고, LoRA를 149GiB full checkpoint로 병합한 일반 vLLM 경로도 서빙과 5건 smoke를 완주했다. HF/merged vLLM의 schema 통과율은 각각 80%/60%, risk match는 모두 60%여서 품질 경고로 보존했다. 500건 challenge 초안은 ID에 `diversevul` provenance가 노출되는 구현 불일치를 발견해 폐기 증거로 남기고, builder를 익명 code-hash ID로 수정·검증한 v2 artifact를 생성했다.
- **Concept**: Qwen3-Coder-Next 80B 학습 이후 서빙 환경을 준비하면서 얻은 교훈을 [LLM 생명주기 환경 설계](wiki/infra/llm-lifecycle-environment-design.md)로 정리했다. 개발·학습·저장·재로드·실제 서빙·평가를 full training 전에 함께 검증하고, 동일 환경에서 통과하면 통합하며 실제 충돌이 확인된 역할만 분리한다는 원칙을 기록했다.
- **Decision**: 이번 AegisLM-B200 run의 별도 `.venv-serving`은 이미 장시간 검증된 학습 환경을 보존하기 위한 위험 완화 조치로 분류했다. 다음 모델부터는 통합 환경을 기본 후보로 100-step 생명주기 preflight를 먼저 수행하고, Docker는 검증된 version matrix를 고정하는 수단으로 사용하며 Kubernetes는 실제 다중 node·운영 요구가 생길 때 검토한다.
- **Update**: 루트·Infra·Fine-Tuned index와 Qwen3-Coder-Next 실행 기록에 새 개념 문서의 cross-link를 추가했다.

## 2026-07-27

- **Refactor**: 사용자 지침에 따라 데일리 루틴 디렉터리를 [wiki/routine/](file:///D:/wiki/wiki/routine/)으로 통합 구성함. 하위에 `ai_paper`, `economy`, `Eng`, `Job_LLM_ML` 4개 과목 폴더 및 `checklist` 폴더를 생성함.
- **Workflow**: `wiki/routine/days.py` 및 `run_today.bat`을 작성하여 클릭 시 당일 4개 과목 날짜 폴더와 원문 markdown 파일, 그리고 [checklist/YYYY-MM-DD.md](file:///D:/wiki/wiki/routine/checklist/2026-07-27.md)가 자동 생성되도록 구성을 완료함.

## 2026-07-25

- **Ingest**: Schadt, Mai, Buettner의 2025년 IEEE Access 논문 *A Systematic Literature Review of the Application of Artificial Image Data for Visual Defect Detection* 원문을 `raw/papers/`에 보존하고, 검색·분류 방법, 분야별 결과, 실무 적용 순서와 후속 질문을 [논문 노트](wiki/papers/artificial-image-data-visual-defect-detection-slr.md)로 정리했다.
- **Review**: PRISMA 흐름도의 52편과 본문의 51편이 일치하지 않는 점, 의료 분야 Web of Science 보강 검색이 Method와 최종 문헌 집합에 명확히 통합되지 않은 점, 좁은 검색식·conference 제외·이질적 지표 비교 한계를 확인해 저자 주장과 비판적 해석을 분리했다.
- **Update**: 누락되어 있던 `wiki/papers/index.md`를 생성하고 루트 `index.md`에 새 논문 노트를 연결했다.

## 2026-07-24

- **Ingest**: 읽기 자료 전체 작업의 마지막 배치 5개를 `wiki/reading/notes/401-405`로 재작성했다. LinkedIn의 SIMA 2 소개 글은 Google DeepMind blog와 technical report로 검증했고, 외부 URL이 없던 연구 탐색 prompt는 1차 출처·version·공정한 benchmark 비교·재현성 검사를 포함한 command note로 다듬었다. Mamba-3 기사는 논문의 state size·MIMO 결과와 기사 표현을 구분했으며, GPT-5.2의 12월 9일 출시설은 실제 12월 11일 공식 발표와 대조했다. 영상에서 “58”로 잘못 인식된 제품은 Google Labs의 `Opal`로 바로잡고 공식 문서 및 한국 서비스 확대 시점을 확인했다. 이로써 고유 자료 405개 전부에 로컬 note를 연결했으며, 원문 확인 요약 375개, 접근 제한 또는 원문 소실 사유 기록 30개, 대기 0개, 원본 목록과 연결되지 않은 note 0개다.
- **Update**: `scripts/build_reading_progress.py`가 대기 자료가 없을 때 완료 상태와 접근 제한 자료의 재처리 조건을 표시하도록 수정했다.
- **Ingest**: 읽기 자료 전체 작업의 스무 번째 배치 20개를 `wiki/reading/notes/381-400`으로 재작성했다. AI agent 숙련 가이드, on-policy distillation survey, Claude 9-agent 개발 시스템, OmniCoder-9B, 무료 AI 교육·인증 과정, Claude Code community 도구, OpenCode 입문, solo AI SaaS 아이디어, agent engineering 함정, Addy Osmani의 LLM workflow 2편, 2026 IT 리더 과제, Python library, 업무 최적화, CMU 11-785와 DeepSeek V4를 원문·공식 문서·논문·공개 mirror와 대조했다. 회원 전용 글 3개와 본문·도서 목록을 복구할 수 없는 영상 2개는 공개 범위를 넘겨 추정하지 않고 필요한 전문·transcript 조건을 기록했으며, OpenCode 설정과 DeepSeek V4 출시 루머는 현재 공식 문서 및 실제 2026-04-24 공개 내용과 분리했다. 현재 고유 자료 405개 중 원문 확인 요약 370개, 접근 제한 또는 원문 소실 30개, 대기 5개다.
- **Ingest**: 읽기 자료 전체 작업의 열아홉 번째 배치 20개를 `wiki/reading/notes/361-380`으로 재작성했다. 에이전틱 코딩의 실제 효용 토론, ISL과 Shalizi 통계 교재, RAG 아키텍처 8종, agent pattern 카드 뷰어, AI coding workflow와 창의성 논쟁, 독립 개발 사례, AI 하이브리드 독서법, 기업 AI ROI, AI engineering stack, agent 명세와 공개 비방 책임, Rules·Skills·Commands·Subagents, 개발자의 문제 정의 역량, AI 시대 code review 2편, AI 대학원 면접 학습 앱, CCPS 신뢰도 보정과 AI Co-Mathematician을 원문·공식 page·논문·공개 영상 설명과 대조했다. 같은 code review 주제의 GeekNews URL과 저자 원문은 각각 보존하고 상호 연결했으며, 영상 1개는 제목·설명·chapter와 자동 자막 track 존재까지 확인하되 `429`로 전체 transcript를 받지 못한 범위를 명시했다. 현재 고유 자료 405개 중 원문 확인 요약 355개, 접근 제한 또는 원문 소실 25개, 대기 25개다.
- **Ingest**: 읽기 자료 전체 작업의 열여덟 번째 배치 20개를 `wiki/reading/notes/341-360`으로 재작성했다. claude-recall, Claude Code 노출 소스 분석서, Claude Agent SDK workshop, CMU 11-785 영상 자료실, Google Career Dreamer, CandleView, CUDA 가속과 에너지 효율, CS146S 한국어 site, CMDS 공식 page 3개, production agent system 7계층, 확장형 Agentic RAG, EPL 예측 MLOps 연재 3편, LangChain·LangGraph·RAGAS 복합 RAG, directed SSSP와 Kakao Tech Blog portal을 원문·공개 transcript·source repository와 대조했다. 회원 전용 EPL·RAG article은 저자가 연결한 공개 repository와 phase code로 보완했고, 같은 주제를 가리키는 CMDS·CS146S·RAG URL은 문서별 고유 범위와 version을 분리해 기존 note에 연결했다. 본문과 transcript를 찾지 못한 Claude Code background subagent 영상 1개에는 필요한 subtitle·mirror 조건을 기록했다. 현재 고유 자료 405개 중 원문 확인 요약 335개, 접근 제한 또는 원문 소실 25개, 대기 45개다.
- **Ingest**: 읽기 자료 전체 작업의 열일곱 번째 배치 20개를 `wiki/reading/notes/321-340`으로 재작성했다. 추론 토큰 기능적 중요도, AI agent protocol 6종, Deep Delta Learning, 무료 데이터 과학 학습, ECL 데이터 엔지니어링, Claude Code의 skill 기반 지속 학습, CodeSpeak, Cloud CLI, ClawTeam, Claude 구독 정책 해석, Anthropic 내부 skill 설계, agent 대기 시간 활용, 다중 agent code review, Boris Cherny workflow 2편, Claude Code 팁 70선과 Agent Teams를 논문·원문·공식 자료와 대조했다. YouTube caption endpoint가 차단된 Django·FastAPI 영상과 회원 전용인 Python agent 구현 글 2편은 공개 범위만 기록하고 필요한 transcript·전문·source code 조건을 남겼다. 정책·가격·vendor benchmark와 개인 생산성 수치는 시점 의존 정보 및 저자 주장과 확인된 사실을 분리했다. 현재 고유 자료 405개 중 원문 확인 요약 316개, 접근 제한 또는 원문 소실 24개, 대기 65개다.
- **Ingest**: 읽기 자료 전체 작업의 열여섯 번째 배치 20개를 `wiki/reading/notes/301-320`으로 재작성했다. CMDS System Files, OpenClaw MLX setup, Claw Code, Claw3D, DeepSeek Engram, 비공식 전자책 저장소, Act Operator, Agentic Data Scientist, LangGraph 1.0 tutorial, Nano-vLLM, 복합 RAG, MiroFish, Codex 추론 강도 비교, GPT-5.2 이론물리학 협업, GLM-4.7, Ollama 비판, 공개 통계 교재, Netflix 추천 foundation model, Everything Claude Code와 EgoX를 원문·공식 저장소·논문 페이지와 대조했다. 리디렉션된 GitHub·GeekNews·Netflix·PyTorchKR 자료는 저장 당시 단축·이전 URL을 별칭으로 남겼고, 상업 서적 PDF 저장소는 내용을 복제하지 않고 저작권과 보존 위험을 기록했다. 벤치마크, 과학 발견과 도구 비판은 저자 주장·실험 한계·재검증 조건을 분리했다. 현재 고유 자료 405개 중 원문 확인 요약 299개, 접근 제한 또는 원문 소실 21개, 대기 85개다.
- **Ingest**: 읽기 자료 전체 작업의 열다섯 번째 배치 20개를 `wiki/reading/notes/281-300`으로 재작성했다. Caveman, InkOS, Inheritune, AI 리터러시 도서 6권, 바이브 코딩 학습법, Hugging Face Skills, 로컬 end-to-end ML platform, Claude Code context 관리 강의, Hermes Agent, Global AI Frontiers Symposium, GlobalBuildingAtlas, Stanford CS146S 한국어판, Solar-GLM weight 분석, Parcae, reasoning model 학습 code, Mistral Vibe, macOS Agent!, OpenMythos와 autoresearch를 원문·자동 자막·논문·공식 저장소와 대조했다. YouTube caption endpoint 제한은 공개 transcript로 보완했고, 같은 Hermes·Parcae 주제의 기존 문서는 URL별로 보존해 상호 연결했다. Medium 회원 전용 Claude Code·Ollama 글은 공개 도입부와 현재 공식 연동 방식까지만 확인해 전문을 추정하지 않고 필요한 대체 자료를 기록했다. 현재 고유 자료 405개 중 원문 확인 요약 279개, 접근 제한 또는 원문 소실 21개, 대기 105개다.
- **Ingest**: 읽기 자료 전체 작업의 열네 번째 배치 20개를 `wiki/reading/notes/261-280`으로 재작성했다. MiMo-V2-Flash, Hyperagents, Mantic, ML Intern, MCP와 CLI의 역할, LangChain Skills 평가, LLM 생성 code 검증, QLoRA 편향 보정, LLM 협업 피로, LLM 도서 7권, Architecture Gallery 관련 URL 3개, 한 시간 LLM 학습 workshop, LINE 서버 개발자 회고, K-EXAONE, knowledge-graph API discovery, Kimi Claw와 KanVibe를 원문·논문·공식 저장소와 대조했다. 폐쇄된 LINE 회고 원문은 Wayback snapshot으로 복구했고, 저장 당시 “embedding 없음”이던 Mantic과 K2.5 기반 Kimi Claw가 현재 각각 optional semantic reranking과 K2.6으로 바뀐 점을 구분했다. 공개 영상의 chapter는 확인됐지만 자동 자막 endpoint가 반복 차단된 권영수 인터뷰에는 필요한 transcript 조건을 남겼다. 현재 고유 자료 405개 중 원문 확인 요약 260개, 접근 제한 또는 원문 소실 20개, 대기 125개다.
- **Ingest**: 읽기 자료 전체 작업의 열세 번째 배치 20개를 `wiki/reading/notes/241-260`으로 재작성했다. 오픈 AI·ML 교재 11권, OneRAG, Omni, Olmo 3, Ollama·MLX, Obsidian Skills, Hermes Agent, NodeNest, Pichia-CLM, Nested Learning, NVTX, NemoClaw, RAPIDS LAB, NIA 2026 트렌드, Moltresearch, Moltbook과 MiniMind를 원문·공식 저장소·논문 정보와 대조했다. 같은 주제지만 URL이 다른 Ollama·MLX 문서 2개는 각각 보존하고 상호 연결했으며, 공개 공유가 끊긴 Clawdbot Notion 문서와 설명·자막이 없는 MiniMax M2.1 영상에는 확인된 metadata, 막힌 이유와 필요한 대체 자료를 기록했다. 현재 고유 자료 405개 중 원문 확인 요약 241개, 접근 제한 또는 원문 소실 19개, 대기 145개다.
- **Ingest**: 읽기 자료 전체 작업의 열두 번째 배치 20개를 `wiki/reading/notes/221-240`으로 재작성했다. Practical ML 최적화 글 모음, Pi 에이전트의 미니멀 설계, ML 과학철학 open-access 편저, Parcae 모델 배포, PaperOrchestra, PageIndex, Opus 4.5 개발 경험, Opentology, OpenSwarm, OpenKB, 생성형 UI, OpenClaw, agent 구축 가이드, Claude Code용 Codex plugin, Open SWE, Open Responses와 OpenCode의 local·저가 모델 활용을 원문·공식 프로젝트·토론과 대조했다. 같은 주제를 가리키지만 저장 URL이 다른 PaperOrchestra와 Open SWE 문서는 URL 기준에 따라 각각 보존하고 상호 연결했으며, model 가격과 무료 quota는 변동 정보임을 분리했다. 현재 고유 자료 405개 중 원문 확인 요약 223개, 접근 제한 또는 원문 소실 17개, 대기 165개다.
- **Ingest**: 읽기 자료 전체 작업의 열한 번째 배치 20개를 `wiki/reading/notes/201-220`으로 재작성했다. WeKnora, Stanford CME 295, Sweep Next-Edit, StreamingVLM, Step 3.5 Flash, Hugging Face 오픈소스 생태계 보고서, OpenClaw 관련 공유 글 3개, 로컬 RAG, SmolVLM2, ShareGPT4Video, SKM, ZeroClaw 토론, ROMA, Qwen3·3.5, Claude Code Channels 비교와 Q-learning의 확장 한계를 원문·논문·저장소와 대조했다. Google 공유 링크 3개는 실제 도착 URL을 별칭으로 기록했고, 자동 생성된 Moltbot 설치 글은 확인되지 않은 저장소·비용·보안 주장을 실행 지침과 분리했다. 본문이 열리지 않고 제목·부제만 확인된 독학 개발 자료 1개에는 필요한 전문·PDF 조건을 남겼다. 현재 고유 자료 405개 중 원문 확인 요약 203개, 접근 제한 또는 원문 소실 17개, 대기 185개다.
- **Ingest**: 읽기 자료 전체 작업의 열 번째 배치 20개를 `wiki/reading/notes/181-200`으로 재작성했다. 2025년 11~12월과 2026년 1월 AI/ML 논문 흐름, Claude Code 제작자의 workflow, 퀀트 투자·능동적 독서 인터뷰, ZeroClaw, Ubuntu·Fedora 입문, llama.cpp OCR, Unsloth Studio, 트리 기반 ML, 소형 언어 모델 학습, Trails 지식 연결, 현대 LLM 아키텍처, 연구 자료 Notion 허브, agentic Text-to-SQL을 원문·영상 정보·저장소와 대조했다. Medium 회원 제한으로 첫 절만 공개된 Java 과잉 설계 글, 소유자가 다운로드를 금지한 Google Drive 시계열 PDF, 삭제·비공개 상태의 `How to find the idea` Notion 페이지에는 각각 확인 범위와 필요한 대체 자료를 기록했다. 현재 고유 자료 405개 중 원문 확인 요약 184개, 접근 제한 또는 원문 소실 16개, 대기 205개다.
- **Ingest**: 읽기 자료 전체 작업의 아홉 번째 배치 20개를 `wiki/reading/notes/161-180`으로 재작성했다. a16z의 2026년 전망, Claude Code 하네스 생성기, Google Workspace CLI, 100권 독서 커리큘럼, EgoX·Parcae·FiCT·Sleeper Agents·LightRAG 등 논문 6편, 르베그 측도의 연속성, LLM 실무 강의와 학습 가이드, GeekNews·PyTorchKR 주간 큐레이션을 원문·논문·공개 목차와 대조했다. 투자 전망과 논문 저자의 실험 결과는 확인된 사실과 분리했고, 영상은 전체 자막이 아닌 공개 목차를 확인한 범위를 명시했다. 단축 URL 2개는 최종 arXiv 주소를 별칭으로 기록해 이후 중복 생성을 방지했다. 현재 고유 자료 405개 중 원문 확인 요약 167개, 접근 제한 또는 원문 소실 13개, 대기 225개다.
- **Ingest**: 읽기 자료 전체 작업의 여덟 번째 배치 20개를 `wiki/reading/notes/141-160`으로 재작성했다. 한국폴리텍대학 하이테크과정, AI 코딩 도구 가격 논쟁, LLM 엔지니어링 도구 지도, 생성형 AI와 학습 성과 연구, GLM-4.7-Flash GGUF, Solar Open 100B, 에이전트 하네스 3종, Kimi K2.6, 당근의 택소노미·시맨틱 캐싱 운영기, mHC, Agent Lattice, Iceberg Index를 원문·공식 모델 카드·논문과 대조했다. 삭제 또는 비공개 상태인 YouTube 영상 2개와 로그인이 필요한 NotebookLM 1개는 접근 실패 이유와 재처리 조건을 남겼다. Karpathy의 `llm-wiki` gist 중복은 새 문서를 만들지 않고 기존 033번 문서의 URL 별칭으로 병합했으며, 진행표 생성기가 `resource_aliases`와 `notion_aliases`를 인식하도록 보강했다. 현재 고유 자료 405개 중 원문 확인 요약 147개, 접근 제한 또는 원문 소실 13개, 대기 245개다.
- **Ingest**: 읽기 자료 전체 작업의 일곱 번째 배치 20개를 `wiki/reading/notes/121-140`으로 재작성했다. Kanana pre-training, 무신사 AI 코드 리뷰, 로컬 RAG, Rocky Linux, Docker·Kubernetes, Titans·MIRAS, 다중 모델 개발 workflow와 비개발 직군의 지식 수집 자동화를 원문·공식 자료와 대조했다. 네이버 카페 글과 Arca Live 로컬 LLM 목록은 본문 접근 제한을, 감기약 조합 글은 원문 부재와 의약품 중복 복용 위험 때문에 추정하지 않은 이유를 기록했다. 현재 고유 자료 405개 중 원문 확인 요약 129개, 접근 제한 또는 원문 소실 10개, 대기 266개다.
- **Ingest**: 읽기 자료 전체 작업의 여섯 번째 배치 20개를 `wiki/reading/notes/101-120`으로 재작성했다. 에이전틱 엔지니어링 패턴, 문학적 프로그래밍, Gumini, OpenJarvis, DeepScholar, Codex, 상태머신 에이전트와 바이브 코딩 비판·경험담을 원문·논문·공식 저장소로 보강했다. 출처가 없던 “스탠퍼드 무료 AI 학위” 주장은 공식 자료로 바로잡았고, Arca Live 목록과 문서 정보를 식별할 수 없는 삼성증권 동적 뷰어에는 접근 제한 사유와 필요한 대체 자료를 기록했다. 현재 고유 자료 405개 중 원문 확인 요약 112개, 접근 제한 또는 원문 소실 7개, 대기 286개다.
- **Ingest**: 읽기 자료 전체 작업의 다섯 번째 배치 20개를 `wiki/reading/notes/081-100`으로 재작성했다. Kanana-2 Thinking, 바이브 코딩 로드맵, 정보처리기사 학습, NIA 채용, ClickStack 로그 플랫폼, FastAPI, Hotwire Native, 무신사 하이브리드 AI 인프라, RLHF·DPO와 ML 목표 지표 설계 등을 원문·공식 문서와 대조했다. 제목·URL·메모가 모두 빈 Notion 항목과 전체 식당 정보를 복구하지 못한 국수집 영상은 접근 제한 사유와 필요한 보충 자료를 기록했다. 현재 고유 자료 405개 중 원문 확인 요약 94개, 접근 제한 또는 원문 소실 5개, 대기 306개다.
- **Ingest**: 읽기 자료 전체 작업의 네 번째 배치 20개를 `wiki/reading/notes/061-080`으로 재작성했다. Claude Code 학습 로드맵과 source map 공개 사고, vLLM·Triton 서빙, TOPCIT 자료, Knuth의 `Claude's Cycles`, SendFeeCompare, Gemini Gems, AI 시대 코드 병목과 review 재설계 등을 다뤘다. 영상 자막의 “500만 줄 유출”은 보도와 공개 자료를 대조해 약 51만 2천 줄로 바로잡고, 공부법 영상의 제품 홍보와 근거 없는 배수 주장도 검증된 학습 원칙과 분리했다. 현재 고유 자료 405개 중 원문 확인 요약 76개, 접근 제한 또는 원문 소실 3개, 대기 326개다.
- **Ingest**: 읽기 자료 전체 작업의 세 번째 배치 20개를 `wiki/reading/notes/041-060`으로 재작성했다. Headroom, AI 네이티브 엔지니어링 팀, Ouroboros, 재귀적 자기 개선, 한국은행 AI 생산성 분석, Adaptive Chunking, tiny-vLLM, CodeGraph, Codex Goals 등을 원문과 공식 자료에 대조했으며, 본문 수집이 차단된 OKKY 글 1개는 추측하지 않고 접근 실패 원인과 복구 조건을 기록했다. 현재 고유 자료 405개 중 원문 확인 요약 56개, 접근 제한 또는 원문 소실 3개, 대기 346개다.
- **Ingest**: 읽기 자료 전체 작업의 두 번째 배치 20개를 `wiki/reading/notes/021-040`으로 재작성했다. Loop Library, 생성형 AI 개인정보 보호, OPID, agentdir, LiteParse, llm-wiki, HarnessX, VibeThinker-3B, Anthropic의 코딩 전문성 보고서, North Mini Code 등을 원문과 공식 후속 출처에 대조해 핵심 내용·활용 방법·한계를 분리했다.
- **Update**: `wiki/reading/progress.md`와 `scripts/build_reading_progress.py`를 추가해 고유 자료의 요약 완료, 접근 제한, 대기 상태를 Notion 항목 ID와 최종 URL로 추적하도록 했다. `shem` 추적 파라미터로 갈라진 중복 1개를 추가로 제거해 현재 전체 405개, 원문 확인 요약 37개, 접근 제한 또는 원문 소실 2개, 대기 366개이며 접근 제한 항목에는 사용자가 대체 링크를 제공할 수 있도록 실패 사유를 기록했다.

- **Update**: 저장 URL 412개의 리디렉션과 페이지 제목을 조회해 `raw/notion/resource-library-url-metadata-2026-07-24.json`에 보존했다. 243개 리디렉션과 201개 원문 제목을 확인했으며, 최종 URL 기준으로 최신 항목만 남겨 420개 중 중복 14개를 제외한 406개 자료로 재생성했다. 접근 차단·삭제·비공개·비HTML 자료로 제목을 확정하지 못한 18개는 `wiki/reading/title-review.md`에 분리했다.
- **Ingest**: Notion 읽기 자료실의 최근 20개를 원문, GitHub 저장소, 논문, 영상 자막과 대조해 `wiki/reading/notes/`에 한국어 재작성 요약 17개와 원문 접근 제한·유실 기록 2개를 추가했다. 최종 URL이 같은 중복 1개는 별도 문서를 삭제하고 최신 항목에 병합했다.
- **Ingest**: Notion의 `Second Brain (Resource Library)` 데이터베이스 420개 항목을 `raw/notion/resource-library-2026-07-24.json`으로 보존하고, 최종 URL 기준 고유 자료를 `wiki/reading/`에 가져왔다. 전체 읽기 체크리스트와 AI 에이전트, AI/ML 연구, 데이터·인프라, 소프트웨어 엔지니어링, 학습·커리어, 수학·통계, 비즈니스·생산성, 개인·미분류의 8개 분류 문서를 생성했으며, `scripts/import_notion_resource_library.py`로 반복 생성할 수 있게 했다.

## 2026-07-21

- **Update**: Qwen3-Coder-Next 80B 2-GPU 실행에서 step 500/1,000 full validation이 각각 약 3시간 30분 소요되고, evaluation 중 VRAM이 GPU당 약 106~108GiB에서 평탄하게 유지됨을 실행 추적 문서에 추가했다. checkpoint-1000 persistent mirror와 약 201MiB 크기를 확인했으며, 다음 run에서는 validation frequency를 별도 최적화 대상으로 둔다.

## 2026-07-20

- **Experiment**: B200 2장과 400GiB cgroup에서 시작한 Qwen3-Coder-Next 80B ZeRO-3 LoRA 실제 학습의 [실행 추적 문서](wiki/projects/Fine_Tuned/training/qwen3_coder_next_80b_2gpu_run_20260720.md)를 추가했다. 로딩 peak 400GiB, 학습 중 GPU당 약 90.7GiB, step당 약 32~33초, 초반 loss 변화와 step 500 evaluation/checkpoint 관측 계획을 분리해 기록했다.
- **Project**: 최신 AegisLM `main`과 선별한 B200 코드를 통합한 private 저장소 `Malicious-code-detection-project/AegisLM-B200`을 만들고 draft PR #1을 생성했다. B200 2장, 400GiB cgroup, LlamaFactory v0.9.5, DeepSpeed ZeRO-3 LoRA 환경을 `/home/daegu/workspace/AegisLM-B200`에 배포했다.
- **Data/Model**: `hf-full-v1` 416,009건을 train 332,807 / validation 41,600 / test 41,602로 생성하고 source revision과 SHA256 manifest를 남겼다. Qwen3-Coder-Next revision `a7fbcb5…`의 148.41GiB safetensors 40개를 받아 누락이 없음을 확인했다.
- **Checkpoint**: local 최신 1개와 persistent 최신 1개의 atomic mirror, step 불일치 시 자동 중단하는 resume 정책을 구현하고 dummy checkpoint로 검증했다.
- **Performance**: dataset record의 중복 schema 검증과 split 후 재검증을 제거해 full 전처리 시간을 1시간 이상에서 약 7분으로 단축했다.
- **Documentation**: [AegisLM-B200 2-GPU 재구축](wiki/projects/Fine_Tuned/b200/aegislm_b200_2gpu_rebuild.md)에 서버 상태, 실행 명령, 저장 경로, checkpoint 정책, 남은 Git 인증 항목을 기록했다. 실제 80B model load와 training은 시작하지 않았다.

## 2026-07-18

- **Study Note**: 정보처리기사 실기 200문제 진단에서 드러난 오답·혼동 개념을 정식 답안, 비교표, 코드·SQL 실수 방지 규칙, 10분 자가시험 형태로 재구성한 [200문제 기반 최종 강화 노트](wiki/cs/engineer_info_processing/final_200_question_reinforcement.md)를 추가하고 학습 대시보드에 연계했다.

## 2026-07-16

- **Ingest**: 2026-07-16일 자 신규 학습 일지인 [my_study_log_260716.md](wiki/cs/engineer_info_processing/my_study_log_260716.md)를 생성하고 82번 보안 공격 용어(사회공학, 피싱) 퀴즈 풀이와 5대 인적 보안 위협 심화 개념을 정리하여 대시보드 index.md 및 README.md 대문 링크를 최신화했다.

## 2026-07-15

- **Ingest**: 시험 3일 전 벼락치기 최종 핵심 요약집인 [final_cheat_sheet.md](wiki/cs/engineer_info_processing/final_cheat_sheet.md)를 신규 작성하여 대시보드 index.md의 추천 요점 가이드 항목으로 연계했다.

## 2026-07-13

- **Ingest**: 2026-07-13일 자 신규 학습 일지인 [my_study_log_260713.md](wiki/cs/engineer_info_processing/my_study_log_260713.md)를 생성하고 66번 C언어 포인터 매개변수 전송(Call by Value) 및 문자열 출력(%s 널 문자 검색 규칙) 퀴즈 풀이를 수록했으며, 대시보드 index.md 및 README.md 대문 링크를 최신화했다.

## 2026-07-12

- **Ingest**: 2026-07-12일 자 신규 학습 일지인 [my_study_log_260712.md](wiki/cs/engineer_info_processing/my_study_log_260712.md)를 생성하고 50번 네트워크 라우팅 프로토콜 알고리즘(거리 벡터 알고리즘) 퀴즈 풀이를 수록했으며, 대시보드 index.md 및 README.md 대문 링크를 최신화했다.
- **Ingest**: 프로세스 스케줄링의 선점형/비선점형 알고리즘 메커니즘, 평가 지표(대기, 반환, 반응 시간) 계산 공식을 총망라한 [프로세스 스케줄링 알고리즘 종합 가이드](wiki/cs/engineer_info_processing/process_scheduling_bible.md)를 신규 작성하여 대시보드 index.md에 연계했다.
- **Ingest**: 패스워드 크래킹, 스푸핑/스니핑 기법, DoS/DDoS 5대 해킹 기법의 세부 패킷 조작 메커니즘을 총정리한 [보안 공격 기법 종합 가이드](wiki/cs/engineer_info_processing/security_attacks_bible.md)를 신규 생성하여 대시보드 index.md에 연계했다.

## 2026-07-11

- **Ingest**: 2026-07-11일 자 신규 학습 일지인 [my_study_log_260711.md](wiki/cs/engineer_info_processing/my_study_log_260711.md)를 생성하고 48번 C언어 후위 표기법(Postfix) 스택 수식 연산 및 아스키 출력(65 -> 'A') 퀴즈 풀이를 수록했으며, 대시보드 index.md 및 README.md 대문 링크를 최신화했다.

## 2026-07-10

- **Ingest**: 2026-07-10일 자 신규 학습 일지인 [my_study_log_260710.md](wiki/cs/engineer_info_processing/my_study_log_260710.md)를 생성하고 47번 C언어 포인터 매개변수 전송 방식(Call by Value/Reference) 복합 연산 퀴즈 풀이를 수록했으며, 대시보드 index.md 및 README.md 대문 링크를 최신화했다.

## 2026-07-09

- **Ingest**: 2026-07-09일 자 신규 학습 일지인 [my_study_log_260709.md](wiki/cs/engineer_info_processing/my_study_log_260709.md)를 생성하고 45번 IoT 프로토콜 퀴즈 풀이(MQTT, CoAP)를 수록했으며, 대시보드 index.md 및 README.md 대문 링크를 최신화했다.
- **Ingest**: IoT 2대 통신 규격(MQTT, CoAP)의 심화 구조, QoS 레벨 및 관련 기출 무선 기술을 정리한 [사물인터넷(IoT) 프로토콜 종합 가이드](wiki/cs/engineer_info_processing/iot_protocols_bible.md)를 신규 작성하여 업로드하고 대시보드 index.md에 연계했다.
- **Ingest**: 다중 접근 제어(MAC) 기법의 핵심 규격인 CSMA/CD, CSMA/CA의 매커니즘, IFS 및 RTS/CTS 프레임 상호작용을 정리한 [다중 접근 제어(MAC) 프로토콜 종합 가이드](wiki/cs/engineer_info_processing/mac_protocols_bible.md)를 신규 생성하고 대시보드 index.md에 요점 정리 링크로 추가했다.

## 2026-07-08

- **Error Note**: Qwen3-Coder-Next 80B full training이 `train/global_step=4500`, `epoch~=0.4327`까지 진행된 뒤 checkpoint 저장 단계에서 `FileNotFoundError: model/adapters`로 중단된 사건을 [LLaMA-Factory Checkpoint Save Failed Because Model Symlink Target Disappeared](wiki/errors/llamafactory-checkpoint-save-broken-model-symlink.md)에 기록했다. 원인은 `model -> /NHNHOME/WORKSPACE/26moel002_A/DAEGU/Model/MalwareAnalysis/` symlink target이 현재 존재하지 않는 상태로 확인되어 checkpoint output root를 만들 수 없었던 것이다.
- **Study Note**: Qwen3-Coder-Next 80B full training 중 W&B dashboard에 표시되는 `loss`, `eval_loss`, `learning_rate`, `epoch`, `grad_norm`, runtime, system metric을 해석하기 위한 [W&B Training Metrics Guide for MalwareAnalysisLLM](wiki/projects/Fine_Tuned/training/wandb_training_metrics_guide.md)를 추가했다. `logging_steps: 5`, `eval_steps: 250`, global batch size 32 기준으로 train/eval metric을 읽는 방법과 cgroup telemetry를 함께 봐야 하는 경우를 정리했다.
- **Ingest**: 2026-07-08일 자 신규 학습 일지인 [my_study_log_260708.md](wiki/cs/engineer_info_processing/my_study_log_260708.md)를 생성하고 43번 자바 비트 연산 퀴즈 풀이를 수록했으며, 대시보드 index.md 및 README.md 대문 링크를 최신화했다.

## 2026-07-07

- **Update**: `wiki/cs/engineer_info_processing/`의 정보처리기사 실기 OCR 추출 Markdown 69개를 대상으로 한글 조각 공백, 반복 OCR 오독, 문장부호를 1차 교정했다. 원문 확인이 필요한 줄에는 `[확인 필요]`를 표시했으며, 작업 전 백업은 `backups/engineer_info_processing-before-ocr-cleanup-20260707-113046.zip`에 보존했다.
- **Ingest**: 정보처리기사 실기 학습 대시보드 구조를 활용하여 실시간 퀴즈 풀이 및 오답 노트를 누적 기록하는 [정보처리기사 실기 개인 학습 기록 (260707)](wiki/cs/engineer_info_processing/my_study_log_260707.md)을 신규 생성했다.
- **Update**: [정보처리기사 실기 학습 대시보드](wiki/cs/engineer_info_processing/index.md)에 개인 학습 기록 섹션 및 링크를 업데이트했다.
- **Decision**: GitHub 지식베이스 백업 시 개인정보 및 로컬 절대 경로 유출 방지를 위해 `raw/` 폴더 등을 제외하는 `.gitignore` 파일을 루트 디렉토리에 신규 생성했다.
- **Ingest**: 정보처리기사 15년 차 강사 페르소나 및 풀이 출력 템플릿 명세를 레퍼런스 문서 [정보처리기사 실기 강사 페르소나 프롬프트](references/instructor-prompt.md)로 보관하였으며, [대시보드 index.md](index.md)의 References 영역에 링크를 추가했다.
- **Ingest**: 머신러닝 리서처 및 엔지니어 2대 축으로 성장하려는 수험생의 학습 환경 구축을 위해 [ML 엔지니어 프롬프트](references/ml-engineer-prompt.md) 및 [ML 리서처 프롬프트](references/ml-researcher-prompt.md) 레퍼런스 문서를 각각 신규 보관하고 [대시보드 index.md](index.md)에 연계했다.
- **Ingest**: 요구사항 엔지니어링의 전체 프로세스와 핵심 기법을 일괄 요약 정리한 [요구사항 엔지니어링 종합 가이드](wiki/cs/engineer_info_processing/requirements_engineering_bible.md)를 신규 작성하여 업로드하고 대시보드 index.md에 요점 정리 섹션으로 노출했다.
- **Ingest**: GitHub 업로드 시 대문 화면 노출을 극대화하기 위해 저장소 구조, 대시보드 바로가기 및 에이전트 소개를 상세히 수록한 [README.md](README.md) 파일을 신규 생성했다.

## 2026-07-06

- **Error Note**: `MalwareAnalysisLLM`에서 `.venv/bin/llamafactory-cli`가 누락되어 training runner가 시작 즉시 실패한 사건을 [LLaMA-Factory CLI Missing After Dependency Drift](wiki/errors/llamafactory-cli-missing-after-uv-sync.md)에 기록했다. 해결책은 root `pyproject.toml`의 `training` dependency group과 local editable `LLaMA-Factory` source를 기준으로 `uv sync --group training`을 수행하는 것이다.
- **Fix**: `MalwareAnalysisLLM` root `pyproject.toml`을 B200 학습/다운로드 흐름에 맞게 재조정했다. `datasets`는 LLaMA-Factory guard에 맞춰 `<=4.0.0`로 유지하고, `transformers!=4.57.0`, `hf-transfer`, local editable `LLaMA-Factory` training group(`accelerate`, `deepspeed`, `peft`, `trl`)을 추가했으며 `uv.lock`을 갱신했다.
- **Update**: B200 GPU 서버를 더 이상 smoke 중심으로 비워두지 않기 위해 [B200 Full-Size Training Queue](wiki/projects/Fine_Tuned/b200/b200_full_size_training_queue.md)를 추가했다. 원격 `MalwareAnalysisLLM`에는 `Qwen/Qwen3-Coder-Next` 80B full dataset LLaMA-Factory config와 runner를 추가하고, `scripts/download_hf_model.py`에 DeepSeek/GLM/Qwen3-Coder-Next variant alias를 등록했으며 Qwen2/72B는 active training queue에서 제외했다.
- **Recovery**: `log.md`가 PowerShell 인코딩 경로에서 mojibake 상태가 되어, 최근 Fine_Tuned/B200 프로젝트 중심의 changelog를 읽을 수 있는 한국어 요약 형태로 복원했다.

## 2026-07-03

- **Update**: `wiki/projects/Fine_Tuned` 루트에 흩어져 있던 문서를 `b200/`, `data/`, `training/`, `libraries/`, `fundamentals/` 폴더로 재정리했다. 루트 `index.md`는 폴더형 진입점으로 단순화하고, 각 하위 폴더에 `index.md`를 추가했으며 이동된 문서들의 상대 링크를 갱신했다.
- **Experiment**: B200 서버의 800GiB container profile에서 모델 로딩 한계를 측정하기 위해 [B200 Model Limit Load-Only Probes](wiki/projects/Fine_Tuned/b200/b200_model_limit_load_only_probes.md)를 추가했다. 원격 `MalwareAnalysisLLM`에는 후보 manifest, `scripts/run_model_limit_probe.py`, observe-only telemetry 연동, unit test와 실행 문서를 구현했다.
- **Decision**: 기존 B200 LLM 후보군을 현재 실험 결과 기준으로 재정리해 [MalwareAnalysisLLM LLM Candidate Matrix](wiki/projects/Fine_Tuned/b200/llm_candidate_matrix_20260703.md)를 추가했다. 이후 2026-07-06 결정에 따라 Qwen2/72B는 active queue에서 제외하고 Qwen3-Coder-Next 80B를 우선 후보로 승격했다.
- **Report**: `MalwareAnalysisLLM` B200 fine-tuning 준비 중 발생한 데이터셋 build, Hugging Face 로딩, secret-like row validation, memory soft-stop 혼선, DeepSpeed ZeRO-3 dtype mismatch, LLaMA-Factory dependency guard, 480B FP8 checkpoint loading `SIGKILL` 문제를 [B200 Fine-Tuning Troubleshooting Report](wiki/projects/Fine_Tuned/b200/b200_finetuning_troubleshooting_report_20260703.md)로 종합 정리했다.
- **Study Notes**: `MalwareAnalysisLLM` 프로젝트가 실제로 사용하는 라이브러리 스택을 기준으로 [MalwareAnalysisLLM Library Stack Map](wiki/projects/Fine_Tuned/libraries/malwareanalysisllm_library_stack_map.md), [AegisLM Training Libraries](wiki/projects/Fine_Tuned/libraries/aegislm_training_libraries.md), [Training Runtime Libraries](wiki/projects/Fine_Tuned/libraries/training_runtime_libraries.md), [project_Nurilab Library Notes](wiki/projects/Fine_Tuned/libraries/project_nurilab_library_notes.md)를 추가했다.
- **Study Notes**: PyTorch, Transformers/SFT, dataset format, LoRA/PEFT, distributed training, DeepSpeed ZeRO, LLaMA-Factory, W&B/telemetry, framework comparison 기본기 노트를 [Fine-Tuned Project](wiki/projects/Fine_Tuned/index.md)에 연결했다.
- **Setup Guide**: B200 `Qwen3-Coder-480B-A35B-Instruct-FP8` full training 전 사용자가 직접 실행/모니터링할 gate를 [B200 Qwen3-Coder 480B Training Gate Guide](wiki/projects/Fine_Tuned/b200/b200_480b_training_gate_guide.md)에 정리했다.
- **Error Note**: B200 서버의 30B/72B LLaMA-Factory LoRA run이 첫 optimizer step에서 `TypeError: output tensor must have the same type as input tensor`로 실패한 사건을 [LLaMA-Factory DeepSpeed ZeRO-3 LoRA BF16 Dtype Mismatch](wiki/errors/llamafactory-deepspeed-zero3-dtype-mismatch.md)에 기록했다.
- **Experiment**: B200 서버에서 Qwen3-Coder-30B-A3B와 Qwen2-72B의 ZeRO-2 1-step diagnostic run이 통과했음을 기록했다. 이 결과는 이후 Qwen2/72B를 active queue에서 제외하기 전의 pipeline sanity 기준선으로 남긴다.
- **Update**: B200 Qwen3-Coder 480B FP8 재분석을 위해 프로젝트 자체 memory soft-limit/controlled stop 경로를 제거하고 observe-only telemetry 정책으로 전환했다.

## 2026-07-02

- **Update**: B200 480B FP8 multi-framework 비교 실험 골격을 원격 `MalwareAnalysisLLM` 프로젝트에 추가하고, wiki mirror 문서 [B200 480B FP8 Framework Matrix Experiments](wiki/projects/Fine_Tuned/repos/AegisLM/docs/FRAMEWORK_MATRIX_EXPERIMENTS.md)를 생성했다.
- **Update**: B200 480B FP8 실패 분석 문서에서 원인을 OOM으로 확정하지 않도록 표현을 정정했다. `SIGKILL(-9)`은 외부 kill 신호이며, 현재는 cgroup memory limit kill이 강한 가설이지만 CPU pressure, pids limit, loader 경로를 추가 실험으로 분리해야 한다고 기록했다.
- **Update**: B200 `Qwen3-Coder-480B-A35B-Instruct-FP8` smoke run의 2026-07-02 15:44 KST 추가 실패를 기록했다. torchrun 로그와 memory watcher JSONL을 결합해 container cgroup memory limit kill 가능성이 높다고 분석했다.
- **Update**: B200 memory watch 로그에 process-level snapshot을 추가하고, `scripts/check_memory_budget.py --watch`가 JSONL/CSV에 cgroup, GPU, process metrics를 기록하도록 확장했다.
- **Error Note**: B200 4-GPU 환경의 `Qwen3-Coder-480B-A35B-Instruct-FP8` LLaMA-Factory/DeepSpeed ZeRO-3 run이 checkpoint loading 약 40% 지점에서 `SIGKILL(exitcode -9)`로 종료된 원인을 [LLaMA-Factory Qwen3-Coder 480B FP8 SIGKILL Investigation](wiki/errors/llamafactory-qwen3-coder-480b-fp8-oom-kill.md)에 기록했다.
- **Fix**: AegisLM 데이터셋 빌더에서 `rezaduty/cybersecurity-qa-v2` parquet 로딩 실패를 HF Hub JSONL 직접 로더로 우회하고, `--max-per-source -1`을 source별 전체 수집 옵션으로 확장했다.
- **Update**: [Symlink](wiki/infra/symlink.md) 및 [Infra Index](wiki/infra/index.md)를 생성하여 OS별 심볼릭 링크 생성/해제 방법을 지식베이스에 추가했다.

## 2026-07-01

- **Fix**: 사용자가 원하는 하드코딩 credential류 보안 패턴을 데이터셋에서 버리지 않도록 AegisLM 변환 정책을 변경했다. `password=`, `api_key=`, `client_secret=` assignment는 실제 값을 `[REDACTED_SECRET]`으로 마스킹하고 학습에는 포함하되 secret 값은 보존하지 않도록 수정했다.
- **Update**: AegisLM 데이터셋 빌더를 원래 5갈래 흐름(Cybersecurity QA, DiverseVul, BigVul, CTF write-up, ZIP/source corpus)으로 확장하고, CTF/BigVul target redaction, ZIP path traversal 방어, `.env.example`, `scripts/check_environment.py` 기반 B200 환경 preflight 계획을 문서화했다.
- **Update**: B200 서버의 `/home/wyhwang/workspace/MalwareAnalysisLLM`에 AegisLM 스타일 파인튜닝 파이프라인을 구현했다. Hugging Face 직접 추출, AegisLM canonical JSONL 전처리, train/validation/test split, LLaMA-Factory dataset export/registration, Qwen3-Coder-480B 및 FP8 LoRA SFT 설정, W&B online logging run script를 추가했다.
- **Update**: [Security Datasets](wiki/projects/Fine_Tuned/data/security_datasets.md)를 현재 AegisLM 구조에 맞춰 정리하고, 데이터셋 추출, canonical preprocessing, train/validation/test split, LLaMA-Factory export 절차를 문서화했다.
- **Update**: [LLaMA-Factory + W&B Fine-Tuning Integration](wiki/projects/Fine_Tuned/training/llamafactory_wandb_finetuning.md)을 작성하고, LLaMA-Factory exporter, B200 DeepSpeed ZeRO-3 설정, W&B logging YAML, 실행 스크립트, Project NuriLab 연동 문서를 반영했다.
