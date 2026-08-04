# Training Runtime

- [LLaMA-Factory + W&B Fine-Tuning Integration](llamafactory_wandb_finetuning.md) - B200 서버에서 LLaMA-Factory, DeepSpeed, W&B로 Qwen3-Coder SFT를 실행하는 가이드
- [W&B Training Metrics Guide for MalwareAnalysisLLM](wandb_training_metrics_guide.md) - LLaMA-Factory 학습 중 W&B에 표시되는 loss, learning rate, grad norm, epoch, runtime, system metric 해석 가이드
- [Qwen3-Coder-Next 80B B200 2-GPU Real Training Run](qwen3_coder_next_80b_2gpu_run_20260720.md) - 400GiB cgroup 환경의 ZeRO-3 로딩 peak, steady-state VRAM/RAM, loss, evaluation, checkpoint 추적 기록
- [AegisLM 데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md) - 33만 건·7일 학습의 절대평가 실패를 근거로 1–2만 건 고품질 데이터와 재현 가능한 입력 다양화로 전환한 결정
- [AegisLM Phase F 실행 계획](../repos/AegisLM-B200/docs/experiments/plans/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md) - source catalog와 binary-derived 별도 adapter 실험의 SSOT
- [AegisLM Phase F 연구 계획](aegislm_phase_f_experiment_plan_20260728.md) - Phase E 실패에서 F0–F4 실행 순서, gate, 현재 상태와 다음 작업을 잇는 Project Note
- [AegisLM Q1R10 Blind 평가와 Evidence 보정 결정](aegislm_q1r10_blind_evaluation_decision_20260730.md) - Decision adapter PASS와 evidence renderer FAIL을 분리하고 새 blind·Q1R11로 진행한 결정
- [AegisLM Q1R11 신규 Blind 500 PASS와 Source 후보 동결](aegislm_q1r11_fresh_blind_pass_decision_20260730.md) - Q1R10→Q1R11 절대평가 PASS, 적용 범위와 merge·vLLM 다음 gate
- [AegisLM Binary 엄격 Target Evidence 재감사](aegislm_binary_strict_target_evidence_decision_20260730.md) - compile 성공과 target 관계 보존을 분리한 F7 공급 감사
- [AegisLM Binary Model-Ready Target Gate](aegislm_binary_model_ready_target_gate_decision_20260731.md) - target v1–v4 수동 실패와 strict v5 공급 복구 결정
