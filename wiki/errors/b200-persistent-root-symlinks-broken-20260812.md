---
type: Error Note
title: B200 Persistent Root 하위 Symlink 일괄 Broken 진단
description: B200 Mistral 프로젝트의 model·data·artifact·tools symlink는 존재하지만 공통 persistent root를 resolve하지 못하는 사건의 진단 기록
tags: [error, b200, symlink, storage, permissions, mount, mistral]
timestamp: 2026-08-12
status: solved
---

# Situation

B200의 별도 Mistral 프로젝트에서 model, data, artifact와 tools 저장 경로가 모두
사라진 것처럼 보였다. 수정 전에 symlink directory entry와 target resolution을
분리해 검사했다.

# Error Message

확인 결과 링크는 삭제되지 않았다.

```text
model    -> ${PERSISTENT_LLM_ROOT}/Model
data     -> ${PERSISTENT_LLM_ROOT}/Data/
artifact -> ${PERSISTENT_LLM_ROOT}/TrainingArtifacts/
tools    -> ${PERSISTENT_LLM_ROOT}/Tools/
```

네 링크 모두 project owner가 소유한 정상 `lrwxrwxrwx` symlink였지만
`readlink -f`는 target을 resolve하지 못했다.

초기 진단에서 `artifacts`, `training_artifacts`만 검사해 실제 단수형 `artifact`를
누락했다. project root 전체 `find` 결과로 실제 이름을 바로잡았다.

# Confirmed Facts

- project root의 symlink 4개는 존재한다.
- 네 link inode도 서로 다른 정상 directory entry다.
- link text는 모두 같은 `${PERSISTENT_LLM_ROOT}` 아래를 가리킨다.
- 네 target 모두 `readlink -f`에서 실패한다.
- 따라서 “링크 삭제”가 아니라 “공통 target path 해석 실패”다.
- 아직 mount 해제, 상위 directory execute permission/ACL, target rename·삭제 중 어느
  원인인지는 확정하지 않았다.

# Cause

서버 관리 측 오류가 해소된 뒤 project symlink를 삭제·재생성하거나 permission을
수정하지 않았는데 네 target이 동시에 다시 resolve됐다. 따라서 project 내부 link
손상이나 local owner/mode 변경은 원인이 아니었다.

가장 강한 원인은 서버 측 shared filesystem, bind mount 또는 mount namespace의
일시적 장애다. 정확한 운영 측 장애 유형과 root cause report는 확보하지 못했으므로
filesystem 종류나 실패 component는 추정으로 남긴다.

네 target이 동시에 실패하고 공통 prefix를 사용했으므로 진단 당시에도 개별 link
문제보다 다음 원인을 우선 조사했다.

1. shared filesystem 또는 container bind mount가 현재 namespace에서 빠짐
2. `${PERSISTENT_LLM_ROOT}` 또는 그 상위 component가 rename·삭제됨
3. 상위 directory의 execute (`x`) permission 또는 ACL이 project user/group에서 제거됨
4. container 또는 job이 다른 mount namespace로 재생성됨

단순 symlink mode `lrwxrwxrwx`는 원인이 아니다. Linux에서 target 접근 가능성은 link
자체 mode가 아니라 target까지의 모든 parent directory 탐색 권한과 mount 상태에
좌우된다.

# Diagnostic Procedure

수정 전에 다음 read-only evidence를 확보한다.

```bash
id
namei -l "${PERSISTENT_LLM_ROOT}/Model"
namei -l "${PERSISTENT_LLM_ROOT}/Data"
findmnt -T "${PERSISTENT_LLM_ROOT}" 2>&1
findmnt -R /NHNHOME 2>&1
```

parent component별 `ls -ld`와 ACL을 확인한다. 실제 private path는 Wiki와 공개 log에
복사하지 않는다.

```bash
namei -l "${PERSISTENT_LLM_ROOT}"
getfacl -p "${PERSISTENT_LLM_ROOT}" 2>&1
```

해석 기준:

- `No such file or directory`: mount 또는 path component 유실 가능성
- `Permission denied`: 해당 component의 execute permission/ACL 문제
- `findmnt`에 예상 shared filesystem 없음: mount namespace 또는 storage mount 문제
- root는 보이지만 하위 `LLM`만 없음: target rename·삭제 가능성

# Solution

서버 관리 측에서 외부 장애를 복구했고 기존 symlink가 별도 수정 없이 회복됐다.
project에서는 link 삭제, 재생성, `chmod -R` 또는 `chown -R`을 수행하지 않았다.

복구 후 다음 read-only 검사를 수행해 네 target이 모두 정상 resolve되는지 확인한다.

```bash
for item in model data artifact tools; do
    test -L "$item" || { echo "NOT_SYMLINK $item"; exit 1; }
    resolved="$(readlink -f -- "$item")"
    test -d "$resolved" || { echo "BROKEN $item"; exit 1; }
    printf 'PASS %s -> %s\n' "$item" "$resolved"
done
```

모델·데이터 inventory와 artifact write canary가 통과하기 전에는 중단됐던 학습을
즉시 재개하지 않는다. read 정상화와 write 안정성은 별도 조건이다.

원인별 일반 복구 원칙은 다음과 같다.

- mount 문제: 운영자가 원래 shared/bind mount를 복원한다.
- permission/ACL 문제: 기존 승인 owner/group/ACL과 비교해 최소 권한만 복원한다.
- target 이동: 새 위치와 데이터 inventory를 검증한 뒤 link contract를 새로 승인한다.
- container namespace 변경: 올바른 storage mount가 포함된 container/job으로 복구한다.

진단 전 symlink를 삭제하거나 새 target으로 덮어쓰면 기존 target 증거를 잃으므로
금지한다. 이번 사건처럼 root 원인이 해결되면 네 symlink는 별도 재생성 없이 동시에
회복될 수 있다.

# Prevention

- 학습 전 `readlink`, `readlink -f`, `test -d`를 각각 검사한다.
- model·data·artifact·tools의 resolved target과 filesystem ID를 inventory에 기록한다.
- 장시간 학습 중 mount와 artifact output root를 주기적으로 observe-only 검사한다.
- artifact save 전에 별도의 write canary를 실행하되 진단 단계에서는 쓰지 않는다.
- project 경로 이름을 단수 `artifact`로 계약에 고정해 검사 누락을 방지한다.
- container 재생성 시 persistent mount contract를 preflight gate로 둔다.

# Related Concepts

- [LLaMA-Factory Checkpoint Save Failed Because Model Symlink Target Disappeared](llamafactory-checkpoint-save-broken-model-symlink.md)
- [Symlink](../infra/symlink.md)
- [Mistral F5-X 첫 파인튜닝 실습 워크북](../projects/Fine_Tuned/training/mistral_f5x_first_finetuning_workbook_20260809.md)
