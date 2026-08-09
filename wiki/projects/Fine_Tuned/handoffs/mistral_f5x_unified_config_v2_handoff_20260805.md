---
type: Project
title: Mistral F5-X 통합 설정 v2 새 대화 인계 보고서
description: AegisLM-B200의 현재 진행 상태, Mistral 119B 실험 계획, 모델별 계약과 인스레드 서브에이전트 작업 방식을 동결한 인계 문서
tags: [aegislm, mistral, b200, fine-tuning, handoff, multi-agent]
timestamp: 2026-08-05
status: active
---

# 목적

이 문서는 새 Codex 대화가 `Mistral 119B 통합 설정·LoRA/QLoRA B200 실험 계획 v2`를 다시 조사하지 않고 이어받기 위한 단일 인계 보고서다.

다음 네 항목을 정본으로 제공한다.

1. 프로젝트 진행 현황
2. 현재 승인된 구현 계획
3. Sol·Terra·Luna의 계약
4. 새 대화에서 사용할 작업 방식

확인된 사실, 사용자 결정, 아직 실행하지 않은 계획을 구분한다. 이 문서 자체는 B200 서버에 배포할 공통 코드가 아니라 상위 Wiki에만 존재하는 작업 인계 기록이다.

# 1. 프로젝트 진행 현황

## 1.1 저장소 기준선

| 항목 | 현재 값 |
| --- | --- |
| 대상 저장소 | `wiki/projects/Fine_Tuned/repos/AegisLM-B200` |
| 브랜치 | `codex/phase-f-source-v3` |
| 확인한 HEAD | `cb520cdd132f86f23fc45a8800cb6c20c3ab9dc3` |
| 기준 dirty diff SHA-256 | `893f38f86b0acac9ba0a8449cfc104a3744982efbc59694845930a3d5a4cd4df` |
| Git 작업 | stage·commit·push 미승인 및 미실행 |
| 외부 작업 | 설치·다운로드·GPU·SSH·실제 symlink 생성 미승인 및 미실행 |

새 대화는 위 HEAD와 작업 트리가 일치하는지 가장 먼저 다시 확인해야 한다. 값이 달라졌으면 구현을 시작하지 말고 기존 변경의 작성자와 범위를 먼저 확인한다.

## 1.2 완료된 연구 기준선

- Phase E의 학습·adapter 저장·merge·vLLM 서빙·5건 및 500건 평가 lifecycle은 완료됐다.
- Phase E 인프라는 `PASS`, 기존 80B adapter의 모델 품질은 `FAIL`로 기록됐다.
- 실패 원인은 loss 자체가 아니라 데이터 중복, label·출처 노출, 단조로운 target, negative 붕괴였다.
- Phase F에서는 대규모 중복 데이터 대신 근거가 있는 소규모 데이터와 절대평가 gate를 사용한다.
- 기존 Qwen3-Coder-Next 80B 설정, LLaMA-Factory 코드, adapter 및 평가 결과는 회귀 기준선이며 이번 작업에서 변경하지 않는다.
- Mistral Small 4 119B 실험은 Qwen 실험을 대체하거나 덮어쓰는 작업이 아니라 별도의 F5-X canary다.

## 1.3 현재 구현 상태

통합 설정 v2는 아직 구현되지 않았다. 기존 `g1_1step` 중심 초안에서 만들어진 다음 5개 untracked draft만 존재한다.

```text
configs/axolotl/b200/mistral_small_4_119b_chat_template_contract.json
configs/axolotl/b200/mistral_small_4_119b_phase_f_decision_g1_1step.yml
configs/phase_f/mistral_small_4_119b_f5x_manifest.json
scripts/preflight_phase_f_mistral_f5x.py
tests/test_phase_f_mistral_f5x_preflight.py
```

이 파일들은 완료 구현물이 아니다. v2 구현에서 검토 후 삭제하고 통합 구조로 교체한다.

2026-08-05 마지막 읽기 전용 확인에서는 위 5개 외에 새 구현 파일이나 tracked 변경이 관찰되지 않았다. 별도 Luna 대화에 잘못 전달한 Work Order는 `STOPPED`로 종료됐고, 해당 작업에서 수정한 파일이 없음을 확인했다. 새 대화는 별도 작업을 재사용하지 말고, 시작 직후 `git status --short`로 상태를 재확인한다.

## 1.4 사용자가 확정한 두 결정

### Expert LoRA와 dropout

- MoE expert LoRA를 유지한다.
- Axolotl `lora_target_parameters` 제약에 맞춰 `lora_dropout: 0.0`으로 고정한다.
- dropout 0.0은 모든 LoRA 실험의 일반 원칙이 아니라 이번 expert parameter 경로의 호환 조건이다.
- 과적합 여부는 loss만으로 판단하지 않고 1-step, 10-step, 100-step canary와 500건 절대평가로 판단한다.

### Persistent storage 경계

- `data`와 `model`은 persistent root 전체 디렉터리에 연결한다.
- `training_artifacts` 자체는 기존 Qwen의 로컬 checkpoint·별도 mirror 정책을 보존하는 로컬 ignored directory로 유지한다.
- Mistral 결과만 `training_artifacts/mistral-small-4-119b`에서 persistent `TrainingArtifacts/mistral-small-4-119b`로 연결한다.
- 전체 `training_artifacts`를 persistent storage로 바꿔 Qwen 저장 의미를 조용히 변경하면 안 된다.

# 2. 현재 계획 — Mistral F5-X 통합 설정 v2

## 2.1 목표 구조

사람이 수정하는 설정은 다음 한 파일로 통합한다.

```text
configs/experiment.yaml
```

Python은 설정값을 여러 파일에 재정의하지 않는다. 다음 책임만 가진다.

- YAML을 부작용 없이 읽고 exact schema와 immutable pin을 검증한다.
- 선택된 실행 profile을 Axolotl 설정으로 렌더링한다.
- 승인된 YAML raw-byte SHA-256과 현재 파일을 대조한다.
- 실행별 승인 설정, 생성 설정, inventory와 log를 Git 밖에 보존한다.

단일 CLI만 제공한다.

```text
python scripts/run_experiment.py --config configs/experiment.yaml --action validate|render|run
```

모델, revision, profile, step, output 경로를 CLI로 덮어쓰는 옵션은 만들지 않는다.

## 2.2 G1 실행 profile

동일한 모델·데이터·LoRA target을 사용해 다음 순서로 1-step canary를 실행한다.

1. `QLoRA + DDP`
2. `BF16 LoRA + FSDP2`

공통값은 다음과 같다.

```yaml
sequence_len: 2048
lora_rank: 8
lora_alpha: 16
lora_dropout: 0.0
expert_lora: true
max_steps: 1
```

QLoRA profile은 4-bit base와 MoE expert quantization을 사용하며 FSDP·DeepSpeed key를 생성하지 않는다. LoRA profile은 BF16 base, FSDP2와 modern FSDP2 key를 사용하며 양자화하지 않는다.

## 2.3 Immutable inputs

| 항목 | 고정값 |
| --- | --- |
| source model | `mistralai/Mistral-Small-4-119B-2603` |
| source revision | `a11f36bebf709121056b1dbcc943d1c6afbe494d` |
| training model | `axolotl-ai-co/Mistral-Small-4-119B-2603-BF16` |
| training revision | `7918b06c0799750ce522f949bcc97dff2dca632a` |
| Axolotl revision | `3c8334b6f9ae6bf5596f99a1845525c8ffc0a97a` |
| Transformers revision | `d24d79da55f7ee6e538a460d3025e41dcc41ab21` |
| CutCrossEntropy revision | `5f0c7a7778b5b17d37738fae10065ed3034373af` |
| dataset profile | `phase-f-source-decision-v1` |
| train | 10,000건, `2d46c7d8161cbf97cc4efeb1a8c223311f4260ccf7a333dbe3cd71b73715f322` |
| validation | 1,000건, `ab576d0332282244b68711f5fb7129c171cd0b95784f914cf5a7255e880d5481` |
| manifest SHA-256 | `b987d174657061b0d0cdf263f738025514abbd9e3bb054251ca7d9d1777daa4e` |
| system prompt SHA-256 | `9a72abf082ce57817ed0186719aeede75e51579c8131c95afd62b736485352ef` |
| seed | `20260728` |
| prompt | OpenAI messages, tokenizer default template, assistant-only, `reasoning_effort=none` |

G2, G3, merge, evidence adapter, full epoch는 초기 설정에서 모두 `false`다.

## 2.4 G0–G3 gate

### G0 — CPU/static

- exact schema, pin, revision, dataset count와 hash를 검사한다.
- placeholder, secret-like field, Linux·Windows 절대경로, `../` 경로 탈출을 거부한다.
- future gate 활성화와 unsafe run ID를 거부한다.
- `validate` action은 파일을 생성하지 않는다.

### G1 — runtime preflight

- pinned tokenizer와 chat template로 train 10,000건과 validation 1,000건을 전수 렌더링한다.
- 2,048-token 초과, `[THINK]` 또는 `[/THINK]`, role·target·system prompt 오류가 한 건이라도 있으면 중단한다.
- `QLoRA-DDP` 1-step 뒤 `BF16-LoRA-FSDP2` 1-step을 실행한다.
- 양 GPU 참여, GPU당 peak VRAM 165GiB 이하, finite loss, adapter 저장 및 hash가 필요하다.

### 방식 선택

- LoRA가 VRAM·저장·시간 gate를 통과하면 LoRA를 우선한다.
- LoRA가 OOM, 165GiB 초과 또는 save 실패이고 QLoRA가 통과하면 QLoRA를 선택한다.
- 둘 다 실패하면 G2로 진행하지 않는다.

### G2/G3

- 선택된 방식만 10-step save → 새 process reload → 단일 inference를 수행한다.
- 통과 후 100-step과 기존 500건 regression 절대평가를 수행한다.
- 최종 품질은 loss가 아니라 precision, recall, FPR, abstention, schema, safety, evidence gate로 판단한다.
- 100-step PASS 전 merge, evidence adapter와 full epoch를 금지한다.

## 2.5 실행 artifact

```text
training_artifacts/mistral-small-4-119b/<run-id>/
├── approved-config.yaml
├── approved-config.sha256
├── axolotl.generated.yaml
├── inventory.json
└── logs/
```

`render`와 `run`은 `AEGISLM_APPROVED_CONFIG_SHA256`이 현재 `configs/experiment.yaml` raw bytes hash와 정확히 일치해야 한다. 이미 존재하는 run directory는 덮어쓰지 않는다.

## 2.6 구현 allowlist

### 삭제

앞서 열거한 기존 untracked draft 5개.

### 추가

```text
configs/experiment.yaml
aegislm/experiments/__init__.py
aegislm/experiments/config.py
aegislm/experiments/axolotl.py
scripts/run_experiment.py
tests/test_experiment_config.py
tests/test_axolotl_renderer.py
```

### 수정

```text
scripts/setup_b200_workspace.py
tests/test_setup_b200_workspace.py
.env.example
docs/experiments/plans/PHASE_F_DATASET_AND_BINARY_EXPERIMENT_PLAN.md
docs/operations/b200/FINETUNING_TEST_WORKBOOK.md
docs/operations/b200/B200_2GPU_SETUP.md
```

이 allowlist 밖 파일이 필요해지면 worker가 임의로 넓히지 않고 `BLOCK`한다.

# 3. 각 서브에이전트 계약

## 3.1 공통 계약

- 여기서 `subagent`는 현재 새 대화 내부에서 `spawn_agent`로 만든 자식 작업자만 뜻한다.
- Codex 사이드바에 있는 별도 Terra/Luna 대화에 메시지를 보내는 방식은 사용하지 않는다.
- worker는 재위임, 다른 worker 호출, 자동 handoff를 하지 않는다.
- maximum delegation depth는 1이다.
- 같은 파일을 둘 이상의 worker가 동시에 수정하지 않는다.
- 설치, dependency 변경, 모델·데이터 다운로드, 실제 symlink 생성, GPU·SSH, Git stage·commit·push는 각각 사용자 승인이 필요하다.
- 기존 dirty worktree는 baseline으로 기록하고 보존한다.
- worker는 명령, exit code, 핵심 출력, 변경 파일, 미실행 항목을 증거로 남긴다.

## 3.2 Sol main 계약

책임:

- 사용자 요구사항과 불변 조건을 해석한다.
- Work Order, allowlist, PASS/BLOCK gate와 외부 권한 경계를 동결한다.
- 현재 대화 내부의 Terra 또는 Luna만 depth 1로 호출한다.
- worker evidence와 diff를 종합해 최종 `PASS` 또는 `BLOCK`을 판정한다.
- 동일 HEAD와 완전한 evidence가 있으면 동일 gate를 이유 없이 반복하지 않는다.

금지:

- 구현 worker에게 설계 권한을 넘기지 않는다.
- Luna가 없는데 Terra를 Luna라고 부르거나 Sol이 몰래 대신 구현하지 않는다.
- 별도 사용자 소유 대화를 subagent처럼 운용하지 않는다.

## 3.3 Terra planner/reviewer 계약

계획 단계 책임:

- 저장소를 읽고 기존 구조, 충돌, allowlist 누락, 테스트 가능성을 조사한다.
- 수정하지 않는 감사형 read-only 방식으로 파일 단위 계획을 제출한다.
- 요구사항이나 gate를 재설계하지 않고 동결된 기준과의 충돌만 보고한다.

검토 단계 책임:

- Luna 구현이 끝난 뒤 diff, allowlist, 테스트 증거, Qwen 회귀 여부를 읽기 전용으로 검토한다.
- 판정은 `PASS / REQUEST_CHANGES / BLOCK` 중 하나만 사용한다.

필수 무변경 증거:

```yaml
changed_files: []
delegation_used: false
delegated_to: []
```

## 3.4 Luna implementation 계약

책임:

- 동결된 allowlist 안에서 통합 config, validator, renderer, bootstrap과 CPU 테스트를 직접 구현한다.
- allowlist 내부 결함은 직접 고치고 재시험한다.
- 결과는 `FIXED` 또는 `BLOCK`만 사용한다.

금지:

- schema, immutable pin, gate, profile 순서나 allowlist를 변경하지 않는다.
- 다른 agent/thread에 넘기지 않는다.
- 설치·다운로드·실제 symlink·GPU·Git을 실행하지 않는다.

Luna를 현재 대화 내부 subagent로 실제 생성할 수 없으면 Sol은 임의 대체하지 않고 사용자에게 `BLOCK`을 보고한다.

## 3.5 필수 Evidence 계약

각 worker는 최소한 다음 필드를 반환한다.

```yaml
work_order_id:
actor_role:
parent_work_order_id:
head_sha:
worktree_diff_sha256:
result:
delegation_used: false
delegated_to: []
effective_sandbox_mode:
effective_approval_policy:
commands:
  - command:
    exit_code:
    key_output:
changed_files: []
out_of_allowlist_changes: []
preexisting_changes_preserved:
failed_skipped_not_executed:
  failed: []
  skipped: []
  not_executed: []
evidence_complete:
revalidation_basis:
revalidation_reason:
known_limitations: []
approval_required_next: []
```

# 4. 새 대화의 작업 방식

## 4.1 시작 순서

1. 이 인계 문서를 처음부터 끝까지 읽는다.
2. AegisLM-B200의 `AGENTS.md`와 `docs/governance/AGENT_WORKFLOW.md`를 전부 읽는다.
3. `git rev-parse HEAD`, `git status --short`와 기존 draft 5개를 확인한다.
4. 별도 Terra/Luna 대화를 호출하거나 메시지를 보내지 않겠다고 사용자에게 명시한다.
5. Work Order `mistral-f5x-unified-config-v2`를 현재 HEAD 기준으로 다시 동결한다.
6. 필요하면 현재 대화 내부 Terra를 read-only planner로 한 번 호출한다.
7. 사용자에게 파일 범위 재승인이 필요한 변화가 없으면 현재 대화 내부 Luna implementation subagent를 호출한다.
8. Luna가 끝난 뒤 Terra reviewer를 순차 호출한다. 같은 파일의 병렬 수정은 금지한다.
9. Sol main이 diff와 evidence를 직접 확인해 CPU 구현 결과를 판정한다.
10. 설치 → 모델 다운로드 → 실제 symlink → G1 GPU 실행 → Git은 각각 별도 사용자 승인으로 진행한다.

## 4.2 새 대화 첫 지시문

다음 문장을 새 대화에 전달하면 된다.

```text
D:\wiki\wiki\projects\Fine_Tuned\handoffs\mistral_f5x_unified_config_v2_handoff_20260805.md를 처음부터 끝까지 읽고, AegisLM-B200의 AGENTS.md와 docs/governance/AGENT_WORKFLOW.md를 확인해. 별도 Codex 대화에 작업을 넘기지 말고 현재 대화 내부 subagent만 사용해. 먼저 HEAD와 dirty baseline을 검증한 뒤 Work Order를 다시 동결하고, Mistral F5-X 통합 설정 v2 구현을 재개해. Luna를 인스레드 subagent로 호출할 수 없으면 임의 대체하지 말고 BLOCK해.
```

## 4.3 CPU 구현 완료와 실제 실험의 구분

CPU 테스트와 static validation이 통과해도 Mistral 학습이 성공한 것은 아니다.

```text
통합 config 구현·CPU 검증
→ 사용자 설치 승인
→ 사용자 모델 다운로드 승인
→ 사용자 symlink 생성 승인
→ G1 QLoRA 1-step
→ G1 LoRA FSDP2 1-step
→ 방식 선택
→ G2 10-step save/reload/inference
→ G3 100-step + 500건 절대평가
→ merge/evidence/full epoch 별도 결정
```

# 5. 다음 대화가 즉시 확인할 위험

- 별도 Luna 작업은 `STOPPED`와 변경 파일 0건으로 확인됐지만, 새 대화도 독립적으로 현재 상태를 확인한다.
- 기존 5개 draft 외 변경이 있으면 작성 주체와 시간을 확인하기 전 삭제하거나 덮어쓰지 않는다.
- `lora_dropout: 0.05`와 expert `lora_target_parameters`를 동시에 되살리지 않는다.
- 전체 `training_artifacts` symlink로 Qwen 정책을 변경하지 않는다.
- 실제 tokenizer가 없을 때 문자 수 추정으로 token gate를 통과시키지 않는다.
- QLoRA의 양자화 오류와 공통 model/data/NCCL 오류를 구분한다.
- CPU 구현 완료를 G1·G2·G3 PASS라고 기록하지 않는다.

# Related Concepts

- [Fine-Tuned Project Index](../index.md)
- [AegisLM Phase F 실행 계획](../training/aegislm_phase_f_experiment_plan_20260728.md)
- [LLM 생명주기 환경 설계](../../../infra/llm-lifecycle-environment-design.md)
