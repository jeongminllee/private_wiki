# Wiki Index

## Categories

### Wiki
- [ML](wiki/ml/index.md) - Machine Learning notes and concept documents
  - [Big Data Analysis](wiki/ml/bigdata_analysis/index.md) - 빅데이터 분석 기획, 통계적 가설 검정, 회귀분석, 머신러닝/데이터마이닝 분류·군집·앙상블 모델 지식 대시보드
  - [MML Study](wiki/ml/mml/index.md) - Mathematics for Machine Learning book study
  - [LLM Ensemble Methods](wiki/ml/llm-ensemble.md) - LLM에 앙상블 기법을 적용하는 아이디어 분석
  - [cuML Random Forest](wiki/ml/cuml-random-forest.md) - GPU 기반 랜덤 포레스트 가속 분석 및 학습 가이드
- [CV](wiki/cv/index.md) - Szeliski 《Computer Vision》 기반 영상 형성, 3D 기하, SLAM, VLM, NeRF/3D-GS 챕터별 지식 대시보드
- [Infra](wiki/infra/index.md) - Infrastructure, networks, and DevOps notes
  - [LLM 생명주기 환경 설계](wiki/infra/llm-lifecycle-environment-design.md) - 개발·학습·서빙·평가 환경의 통합과 분리 판단 기준
  - [Symlink](wiki/infra/symlink.md) - OS별 심볼릭 링크 생성 및 해제 방법
- [Errors](wiki/errors/index.md) - Troubleshooting and error logs
  - [Mistral Small 4 B200 vLLM 0.26 서빙 트러블슈팅](wiki/errors/mistral-small4-b200-vllm-serving-troubleshooting-20260820.md) - official native FP8 base를 B200 TP2로 기동하며 해결한 format·shard·kernel·IPC 문제
- [CS](wiki/cs/index.md) - Computer Science core concepts
  - [Python Study](wiki/cs/python/index.md) - Core Python programming study notes
  - [Java Programming](wiki/cs/java/index.md) - Core Java programming study notes
  - [JSP & Web Architecture](wiki/cs/jsp/index.md) - JSP, 서블릿, 톰캣 아키텍처, MVC, JDBC 데이터베이스 및 웹 시큐리티 총 17개 챕터
  - [정보처리기사 실기](wiki/cs/engineer_info_processing/index.md) - 정보처리기사 실기 기본서, Final 모의고사 및 기출문제 모음집
- [Algorithms](wiki/algorithms/index.md) - Data Structure & Algorithm study dashboard
- [Projects](wiki/projects/index.md) - Side projects and active project notes
  - [Fine-Tuned Project](wiki/projects/Fine_Tuned/index.md) - B200 서버 기반 LLM 서빙, 보안 데이터셋, AegisLM 파인튜닝 실행 기록
    - [GPT-OSS Qwen 계약 5-step 스모크](wiki/projects/Fine_Tuned/repos/AegisLM/docs/GPT_OSS_QWEN_SMOKE_20260921.md) - Q1R10 판정·Q1R11 근거 선택의 독립 학습과 개발 평가

    - [r4 데이터 사전 검사 FAIL](wiki/projects/Fine_Tuned/repos/AegisLM/docs/DATASET_PREFLIGHT_20260921.md) - 정답 오류 4건·기존 파일럿 검토 정정·새 학습 미실행

    - [C/C++ 데이터 실패 분석](wiki/projects/Fine_Tuned/repos/AegisLM/docs/SOURCE_DATASET_FAILURE_ANALYSIS_20260919.md) - 실패 canary 재현·CWE gold 반례·평가 프로토콜 감사
    - [장문맥 C/C++ 프로젝트 연구 계획](wiki/projects/Fine_Tuned/repos/AegisLM/docs/LONG_CONTEXT_PROJECT_RESEARCH_PLAN_20260918.md) - 다중 파일 근거 연결·8K/16K/32K 비교·C/C++ 소스 분석
    - [GPT-OSS-20B 첫 파일럿](wiki/projects/Fine_Tuned/repos/AegisLM/docs/GPT_OSS_PILOT_20260918.md) - AegisLM V3.1 하네스와 단일 32-step 학습·reload, Harmony 평가 정정 및 후속 학습 테이블
    - [AegisLM Phase F](wiki/projects/Fine_Tuned/training/aegislm_phase_f_experiment_plan_20260728.md) - F0–F9 데이터 감사, Qwen 80B 신규 학습, binary/NuriLab 실험 연구 기록
    - [AegisLM Q1R10 Blind 평가 결정](wiki/projects/Fine_Tuned/training/aegislm_q1r10_blind_evaluation_decision_20260730.md) - Decision PASS, evidence FAIL과 새 blind·Q1R11 결정 기록
    - [AegisLM Q1R11 신규 Blind 500 PASS](wiki/projects/Fine_Tuned/training/aegislm_q1r11_fresh_blind_pass_decision_20260730.md) - source two-stage·F5-M1 PASS와 F6 binary 최초 판정 기록
    - [AegisLM Binary 엄격 Target Evidence 재감사](wiki/projects/Fine_Tuned/training/aegislm_binary_strict_target_evidence_decision_20260730.md) - F7 500-pair 확대, 과거 판정 정정과 보수적 공급 gate
    - [AegisLM Binary Model-Ready Target Gate](wiki/projects/Fine_Tuned/training/aegislm_binary_model_ready_target_gate_decision_20260731.md) - strict v7 공급 차단과 ARVO 200건 patch gate `FAIL EARLY` 결정
    - [AegisLM CVEfixes Patch-label 공급 Gate](wiki/projects/Fine_Tuned/training/aegislm_cvefixes_supply_gate_decision_20260731.md) - 6,248쌍 공급량 PASS 뒤 수동 `11/28 FAIL EARLY`, direct-label 학습 거부 결정
    - [AegisLM Decompile-Bench Alignment·Provenance Gate](wiki/projects/Fine_Tuned/training/aegislm_decompile_bench_alignment_decision_20260731.md) - source–assembly 96/100 PASS와 provenance 부족에 따른 reference-only 결정
    - [AegisLM Assemblage LinuxELF Metadata Gate](wiki/projects/Fine_Tuned/training/aegislm_assemblage_metadata_decision_20260731.md) - artifact·schema PASS 뒤 strict metadata 0건으로 raw ELF·학습 거부 결정
    - [AegisLM BinKit 2.0 Metadata Gate](wiki/projects/Fine_Tuned/training/aegislm_binkit_metadata_decision_20260731.md) - compiler matrix 확인 뒤 고정 artifact·license·schema 부재로 binary·pickle 보류 결정
    - [AegisLM EMBER2024 ELF Static-Feature Benchmark Gate](wiki/projects/Fine_Tuned/training/aegislm_ember2024_benchmark_decision_20260731.md) - raw 12,000행을 6,000관측치로 중복 제거한 독립 malware benchmark 결정
    - [AegisLM EMBER2024 ELF Classifier 절대평가](wiki/projects/Fine_Tuned/training/aegislm_ember2024_classifier_baseline_decision_20260731.md) - 자체 temporal LightGBM·공식 모델의 시간 분리 절대 gate 실패와 NuriLab 연결 보류
    - [AegisLM ARVO Patch Gate](wiki/projects/Fine_Tuned/training/aegislm_binary_model_ready_target_gate_decision_20260731.md) - 공개 개발자 패치 200건 수동 오류 11건과 학습 불승인
- [Papers](wiki/papers/index.md) - Academic papers summary
  - [Artificial Image Data for Visual Defect Detection SLR](wiki/papers/artificial-image-data-visual-defect-detection-slr.md) - 결함 검출용 합성·증강 이미지 연구의 방법, 성과와 한계를 분석한 2025년 체계적 문헌고찰
  - [AI 에이전트 & 하니스 링크 요약](wiki/papers/aifrenz-links-summary.md) - aifrenz 채널에서 수집된 AI 에이전트, 하니스 엔지니어링, 벤치마크 관련 링크 요약본
- [Reading Library](wiki/reading/index.md) - Notion에 저장한 글, 논문, 영상과 도구 링크를 로컬에서 읽고 분류하는 자료실
- [Routine](wiki/routine/index.md) - 데일리 루틴 79일의 월별 탐색, 과목별 기록과 체크리스트 현황
  - [루틴 점검 (2026-10-13)](wiki/_maintenance/routine-audit-2026-10-13.md) - 형식 복구 내역, 중복·출처·체크 상태 검토 후보



### ChatGPT Archive (세분화 지식 아카이브)
- [Algorithms (알고리즘 & 자료구조)](wiki/algorithms/chatgpt/) - 356개 지식 노트
- [CS - Software Architecture](wiki/cs/architecture/chatgpt/) - 17개 지식 노트
- [CS - 정보처리기사](wiki/cs/engineer_info_processing/chatgpt/) - 5개 지식 노트
- [CS - Java 프로그래밍](wiki/cs/java/chatgpt/) - 23개 지식 노트
- [CS - Python 프로그래밍](wiki/cs/python/chatgpt/) - 75개 지식 노트
- [Errors - CUDA & GPU](wiki/errors/cuda_gpu/chatgpt/) - 4개 지식 노트
- [Errors - General Troubleshooting](wiki/errors/general/chatgpt/) - 11개 지식 노트
- [Errors - Linux & System](wiki/errors/linux_sys/chatgpt/) - 2개 지식 노트
- [Errors - Python & Conda](wiki/errors/python_conda/chatgpt/) - 50개 지식 노트
- [Infra - Cloud & DevOps](wiki/infra/cloud_devops/chatgpt/) - 3개 지식 노트
- [Infra - Linux & Remote](wiki/infra/linux_ssh/chatgpt/) - 3개 지식 노트
- [ML - GPU & CUDA 가속](wiki/ml/gpu_cuda/chatgpt/) - 11개 지식 노트
- [ML - LLM Serving & Inference](wiki/ml/llm_serving/chatgpt/) - 5개 지식 노트
- [ML - Models & Theory](wiki/ml/models_theory/chatgpt/) - 20개 지식 노트
- [Projects - Career & Job](wiki/projects/career_job/chatgpt/) - 15개 지식 노트
- [Reading - Personal & Misc](wiki/reading/personal_misc/chatgpt/) - 61개 지식 노트
- [Reading - Tech Articles & Guides](wiki/reading/tech_articles/chatgpt/) - 2개 지식 노트

### References
