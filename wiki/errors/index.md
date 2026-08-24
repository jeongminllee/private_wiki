# Errors

- [Mistral Small 4 B200 vLLM 0.26 서빙 트러블슈팅](mistral-small4-b200-vllm-serving-troubleshooting-20260820.md) - native/HF checkpoint format, 누락 consolidated shard, B200 attention backend, Triton cache, IPC path와 CuTeDSL warmup 실패를 거쳐 base API server를 기동한 기록
- [Mistral Fused Expert가 bitsandbytes INT_MAX를 초과해 QLoRA 실패](mistral-fused-expert-bitsandbytes-intmax-qlora.md) - gate_up_proj가 정확히 2^31개 원소라 4-bit CUDA kernel 크기 한계를 넘은 QLoRA G1 BLOCK 기록
- [Mistral 전수 Preflight의 잘못된 Empty Target 판정](mistral-preflight-empty-target-batchencoding.md) - Transformers 5.x chat-template 반환 객체의 input_ids를 꺼내지 않아 정상 target을 빈 값으로 오판한 문제
- [B200 Persistent Root 하위 Symlink 일괄 Broken 진단](b200-persistent-root-symlinks-broken-20260812.md) - model·data·artifact·tools link는 존재하지만 공통 persistent root를 resolve하지 못하는 mount·권한 사건 조사
- [Mistral PixtralProcessor TorchVision 누락](mistral-pixtralprocessor-torchvision-missing.md) - text-only 검사에서도 multimodal processor가 요구한 TorchVision을 PyTorch 2.12.1/CUDA 13.0 호환 버전으로 복구
- [Mistral FP8 to BF16 변환 스크립트 오타와 사후 실패 위험](mistral-fp8-bf16-converter-script-typos.md) - 대형 checkpoint descale script의 scale 집합·params 저장·config 검증 오타 수정 기록
- [LLaMA-Factory Checkpoint Save Failed Because Model Symlink Target Disappeared](llamafactory-checkpoint-save-broken-model-symlink.md) - Qwen3-Coder-Next 80B full training이 checkpoint 저장 단계에서 깨진 `model` symlink 때문에 중단된 사건
- [LLaMA-Factory CLI Missing After Dependency Drift](llamafactory-cli-missing-after-uv-sync.md) - `.venv/bin/llamafactory-cli` 누락과 `pyproject.toml` training group 복구 기록
- [LLaMA-Factory Qwen3-Coder 480B FP8 SIGKILL Investigation](llamafactory-qwen3-coder-480b-fp8-oom-kill.md) - B200 4-GPU 환경에서 480B FP8 checkpoint loading 중 발생한 `SIGKILL` 분석
- [LLaMA-Factory DeepSpeed ZeRO-3 LoRA BF16 Dtype Mismatch](llamafactory-deepspeed-zero3-dtype-mismatch.md) - 30B/72B LoRA training의 첫 optimizer step dtype mismatch 분석
