---
type: Project
title: Mistral Small 4 119B B200 소스 보존 및 GitHub 동기화
description: B200 standalone 프로젝트와 로컬 저장본의 차이를 SHA-256으로 감사하고, 안전한 로컬 Git 기준선을 만든 기록
tags: [project, mistral, b200, git, source-sync]
timestamp: 2026-08-25
status: active
---

# Goal

B200에서 수동으로 구성하고 검증한 Mistral Small 4 119B 학습·평가·서빙 소스를
잃지 않도록 로컬과 GitHub에 보존한다. 모델, 데이터, adapter, 비밀정보와 runtime cache는
소스 저장소에 포함하지 않는다.

# Current Status

- B200 source allowlist 40개 파일을 로컬에 복제했다.
- 복제 직후 양쪽 파일은 missing 0, extra 0, SHA-256 mismatch 0으로 일치했다.
- B200의 `.git`은 존재했지만 유효한 commit과 remote가 없는 빈 저장소였다.
- 로컬에는 standalone source 저장본이 없었으므로 새 nested Git repository를 만들었다.
- 로컬 최초 commit은 `21f02558269af6f5b8b7634d69a9c3b37e54eef4`이다.
- GitHub private repository를 만들고 로컬 `main`을 push했다.
- 초기 push에서 local/remote commit `21f02558269af6f5b8b7634d69a9c3b37e54eef4`가 일치했다.
- 보존 완료 문서를 추가한 현재 remote HEAD는 `ea1891578dfd56fa679dcfd3acdecdb063c41c37`이다.
- GitHub: [AegisLM-Mistral-Small-4-119B](https://github.com/Malicious-code-detection-project/AegisLM-Mistral-Small-4-119B)
- 최초 B200 감사와 로컬 기준선 생성은 읽기 전용으로 수행했다.
- 후속 base-serving 재현에서 구버전 script drift가 확인돼 `scripts/check_serving.sh`만
  기존 파일을 artifact에 백업한 뒤 GitHub 보존본으로 역동기화했다.

# Structure

로컬 저장본에는 다음만 포함한다.

- root metadata와 training dependency lock
- `configs/`의 G1·G2·G3 Axolotl 설정
- `scripts/`의 conversion, preflight, training, evaluation, serving helper
- `serving/vllm/`의 격리된 vLLM dependency lock
- B200 원본 checksum과 sync report

다음은 제외한다.

- `.env`, token과 credential
- `.venv*`, compiler/test cache
- `model`, `data`, `artifact`, `training_artifacts`, `tools`
- 학습·평가·GPU monitoring log
- vLLM runtime cache

# How to Run

GitHub 인증이 복구된 뒤 private repository를 빈 상태로 만든 다음 로컬 `main` branch를
push한다. repository 생성 시 README, `.gitignore`, license를 GitHub에서 자동 생성하지
않아 현재 root commit과의 불필요한 merge를 피한다.

# Key Decisions

## B200와 로컬의 기준 관계

초기 40개 파일의 byte-for-byte snapshot은 B200가 기준이다. GitHub에 올릴 로컬본에는
portable·privacy·format 보완만 제한적으로 적용했다.

- `.gitignore`에 artifact와 cache 경계를 추가했다.
- 빈 README에 목적, 환경 분리와 저장 경계를 작성했다.
- serving helper의 서버 절대경로를 repository-relative/environment-variable 방식으로
  바꾸고 B200에서 실제로 통과한 short IPC temp와 CuTeDSL workaround를 반영했다.
- `.gitattributes`로 text file LF를 고정했다.
- 원본 세 파일의 trailing whitespace와 EOF만 정리했다.

따라서 로컬 Git 기준선은 B200의 단순 복사본이 아니라, 동일한 source snapshot에
이식성 보완을 얹은 보존본이다. 세부 checksum과 변경 목록은 nested repository의
`docs/B200_SOURCE_SNAPSHOT_20260825.sha256`과 `docs/B200_SYNC_REPORT_20260825.md`가
정본이다.

# Issues

- 최초 점검에서 GitHub CLI token이 만료돼 일시 중단했으나 사용자가 재인증해 해결했다.
- Windows 계정과 sandbox 파일 소유자가 달라 첫 push에서 Git의 `dubious ownership`
  보호가 동작했다. 전역 설정을 변경하지 않고 push 명령에만 `safe.directory`를 지정해
  해결했다.
- Windows 로컬에는 `uv`와 실행 가능한 Python runtime이 없어 lock·Python 실행 검사는
  수행하지 못했다. shell helper는 B200의 Bash parser로 syntax PASS를 확인했다.

# Next Actions

1. 필요한 경우 남은 portable 변경 5개만 별도 Work Order로 B200에 역동기화한다.

# Related Concepts

- [Mistral Small 4 B200 vLLM 서빙 트러블슈팅](../../../errors/mistral-small4-b200-vllm-serving-troubleshooting-20260820.md)
- [Mistral Small 4 119B G3 Blind 500 결정](../training/mistral_small_4_119b_g3_blind500_decision_20260820.md)
- [Mistral F5-X 첫 파인튜닝 실습 워크북](../training/mistral_f5x_first_finetuning_workbook_20260809.md)
