# Fine-Tuned Project

B200 서버 기반 LLM fine-tuning, 보안 데이터셋, AegisLM/LLaMA-Factory 실험 기록을 관리한다.

## Sections

- [B200 Experiments](b200/index.md) - B200 서버, 480B/80B 모델 한계, troubleshooting, 후보군 정리
- [Data Pipeline](data/index.md) - 보안 데이터셋 추출, 전처리, SFT 포맷, split/export 흐름
- [Training Runtime](training/index.md) - LLaMA-Factory, W&B, DeepSpeed 기반 실행 가이드
- [Project Library Stack](libraries/index.md) - MalwareAnalysisLLM과 project_Nurilab에서 실제로 쓰는 라이브러리 지도
- [Fine-Tuning Fundamentals](fundamentals/index.md) - PyTorch, Transformers, LoRA, 분산 학습, telemetry 기본기
- [Repository Mirrors](repos/) - AegisLM, project_Nurilab 관련 mirror 문서와 원격 프로젝트 docs

## High-Signal Docs

- [LLM 생명주기 환경 설계](../../infra/llm-lifecycle-environment-design.md) - 개발·학습·서빙·평가의 end-to-end preflight와 환경 통합·분리 기준
- [AegisLM-B200 2-GPU 재구축](b200/aegislm_b200_2gpu_rebuild.md) - 새 private 저장소와 B200 2장·400GiB 환경의 80B full-training 준비 및 검증 기록
- [B200 Full-Size Training Queue](b200/b200_full_size_training_queue.md) - Qwen3-Coder-Next 80B부터 full dataset real training으로 전환하는 실행 큐
- [B200 Model Limit Load-Only Probes](b200/b200_model_limit_load_only_probes.md) - B200 800GiB container profile에서 GLM, Qwen3-Coder Next, DeepSeek V4 Flash 후보의 load-only 한계 측정
- [B200 Fine-Tuning Troubleshooting Report](b200/b200_finetuning_troubleshooting_report_20260703.md) - 데이터셋, dependency, DeepSpeed, memory/cgroup 문제와 해결 내역 종합 보고서
- [MalwareAnalysisLLM LLM Candidate Matrix](b200/llm_candidate_matrix_20260703.md) - Qwen3-Coder, GLM, DeepSeek, gpt-oss 후보를 serving/fine-tuning 관점으로 정리
- [Security Datasets](data/security_datasets.md) - AegisLM 보안 fine-tuning 데이터셋 추출, 전처리, split, LLaMA-Factory export 가이드
- [LLaMA-Factory + W&B Fine-Tuning Integration](training/llamafactory_wandb_finetuning.md) - B200 서버에서 LLaMA-Factory, DeepSpeed, W&B로 Qwen3-Coder SFT를 실행하는 가이드
- [AegisLM 데이터 축소와 통제된 무작위화 결정](training/aegislm_dataset_reduction_randomization_decision_20260728.md) - 33만 건·7일 학습 실패에서 1–2만 건 고품질 데이터 전략으로 전환한 연구 결정
- [AegisLM Binary 엄격 Target Evidence 재감사 결정](training/aegislm_binary_strict_target_evidence_decision_20260730.md) - F7 500-pair 확대와 과거 B0·pilot 재감사, Wilson 공급 gate 결정
- [AegisLM Binary Model-Ready Target Gate 결정](training/aegislm_binary_model_ready_target_gate_decision_20260731.md) - target v1–v4 수동 실패와 strict v5 공급 복구 결정
- [AegisLM Decompile-Bench Alignment·Provenance Gate 결정](training/aegislm_decompile_bench_alignment_decision_20260731.md) - source–assembly 정렬 PASS와 provenance·build metadata 부족에 따른 reference-only 판정
- [AegisLM Assemblage LinuxELF Metadata Gate 결정](training/aegislm_assemblage_metadata_decision_20260731.md) - artifact·schema PASS 뒤 strict complete metadata 0건으로 raw ELF·학습 불승인
- [AegisLM BinKit 2.0 Metadata Gate 결정](training/aegislm_binkit_metadata_decision_20260731.md) - matrix 확인 뒤 versioned dataset artifact·license·schema 부재로 binary·pickle 보류
- [AegisLM EMBER2024 ELF Static-Feature Benchmark Gate 결정](training/aegislm_ember2024_benchmark_decision_20260731.md) - raw 12,000행을 6,000 temporal observation으로 중복 제거한 독립 malware benchmark 승인
- [AegisLM EMBER2024 ELF Classifier 절대평가 결정](training/aegislm_ember2024_classifier_baseline_decision_20260731.md) - train 26,000·test 6,000건의 자체·공식 모델 temporal FPR gate 실패와 NuriLab 연결 보류
- [AegisLM Phase F 실행 계획](repos/AegisLM-B200/docs/experiments/plans/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md) - F0–F9 데이터 감사, Qwen 80B 신규 학습, source/binary 절대평가 계획
- [AegisLM Phase F 연구 계획](training/aegislm_phase_f_experiment_plan_20260728.md) - F0–F9 상태, 모델 실험 사다리, 중단 기준과 다음 실행을 추적하는 Wiki Project Note
- [MalwareAnalysisLLM Library Stack Map](libraries/malwareanalysisllm_library_stack_map.md) - data, schema, model loading, training runtime, logging, security analysis 계층별 라이브러리 지도
