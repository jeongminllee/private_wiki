# Fine-Tuning Fundamentals

- [PyTorch Training Basics](pytorch_training_basics.md) - tensor, dtype, device, autograd, forward/backward/optimizer step 기본기
- [Transformers SFT Basics](transformers_sft_basics.md) - tokenizer, causal LM, `from_pretrained`, chat template, SFT 구조
- [Datasets and SFT Format Basics](datasets_sft_format_basics.md) - raw dataset, preprocessing, split, Alpaca-style export, dataset registration
- [LoRA and PEFT Basics](lora_peft_basics.md) - full fine-tuning과 LoRA/PEFT adapter fine-tuning의 차이
- [Distributed Training Basics](distributed_training_basics.md) - process, rank, local rank, world size, `torchrun`, DDP 기본기
- [DeepSpeed ZeRO Basics](deepspeed_zero_basics.md) - ZeRO-1/2/3, offload, parameter partitioning, dtype mismatch 맥락
- [LLaMA-Factory Basics](llamafactory_basics.md) - YAML config, dataset registration, AegisLM과 LLaMA-Factory의 책임 경계
- [W&B and Telemetry Basics](wandb_telemetry_basics.md) - W&B loss logging, model/watch 설정, cgroup/GPU/process telemetry
- [Fine-Tuning Framework Comparison Basics](finetuning_framework_comparison.md) - LLaMA-Factory, TRL, Axolotl, torchtune, ms-swift, NeMo, Unsloth 비교
- [Mistral 공식 FP8 체크포인트의 로컬 BF16 변환 이해](mistral_fp8_to_bf16_checkpoint_conversion.md) - FP8 weight와 inverse scale을 BF16 tensor로 펼치는 수학적 의미, safetensors 구조, 변환 한계와 학습 전 검증 gate
