# B200 Experiments

- [AegisLM-B200 2-GPU 재구축](aegislm_b200_2gpu_rebuild.md) - Qwen3-Coder-Next 80B용 B200 2장 환경, full dataset, model, checkpoint, handoff 준비 기록
- [B200 Server Fine-Tuning](B200_server.md) - B200 GPU 서버 기반 LLM fine-tuning 실행 환경 기록
- [B200 Full-Size Training Queue](b200_full_size_training_queue.md) - Qwen2/72B를 제외하고 Qwen3-Coder-Next 80B부터 full dataset real training으로 전환하는 실행 큐
- [B200 Model Limit Load-Only Probes](b200_model_limit_load_only_probes.md) - B200 800GiB container profile에서 후보 모델 load-only 한계를 측정하는 실험 문서
- [MalwareAnalysisLLM LLM Candidate Matrix](llm_candidate_matrix_20260703.md) - 30B/72B/480B, GLM, DeepSeek, gpt-oss 후보를 serving/fine-tuning 관점으로 정리
- [B200 Fine-Tuning Troubleshooting Report](b200_finetuning_troubleshooting_report_20260703.md) - 데이터셋, dependency, DeepSpeed, memory/cgroup 문제와 해결 내역 종합 보고서
- [B200 Qwen3-Coder 480B Training Gate Guide](b200_480b_training_gate_guide.md) - 480B FP8 full training 이전 gate, command, monitoring, recording rules
