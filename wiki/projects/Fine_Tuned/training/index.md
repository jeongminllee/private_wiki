# Training Runtime

- [LLaMA-Factory + W&B Fine-Tuning Integration](llamafactory_wandb_finetuning.md) - B200 서버에서 LLaMA-Factory, DeepSpeed, W&B로 Qwen3-Coder SFT를 실행하는 가이드
- [W&B Training Metrics Guide for MalwareAnalysisLLM](wandb_training_metrics_guide.md) - LLaMA-Factory 학습 중 W&B에 표시되는 loss, learning rate, grad norm, epoch, runtime, system metric 해석 가이드
- [Qwen3-Coder-Next 80B B200 2-GPU Real Training Run](qwen3_coder_next_80b_2gpu_run_20260720.md) - 400GiB cgroup 환경의 ZeRO-3 로딩 peak, steady-state VRAM/RAM, loss, evaluation, checkpoint 추적 기록
- [AegisLM 데이터 축소와 통제된 무작위화 결정](aegislm_dataset_reduction_randomization_decision_20260728.md) - 33만 건·7일 학습의 절대평가 실패를 근거로 1–2만 건 고품질 데이터와 재현 가능한 입력 다양화로 전환한 결정
- [AegisLM Phase F 실행 계획](../repos/AegisLM-B200/docs/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md) - source catalog와 binary-derived 별도 adapter 실험의 SSOT
- [AegisLM Phase F 연구 계획](aegislm_phase_f_experiment_plan_20260728.md) - Phase E 실패에서 F0–F4 실행 순서, gate, 현재 상태와 다음 작업을 잇는 Project Note
