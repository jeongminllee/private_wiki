---
type: Study Note
title: Mistral Source Decision 데이터셋 언어 분포
description: G3 학습·검증·blind 데이터의 C/C++ 분포를 eligible manifest와 deterministic join으로 감사한 결과
tags: [mistral, dataset, c, cpp, provenance]
timestamp: 2026-08-25
status: active
---

# Summary

Mistral Small 4 119B G3 source-decision 데이터는 C와 C++만 포함한다. train과
validation을 합치면 C 78.24%, C++ 21.76%이며 unknown·conflict·join 누락은 0이다.
JSONL 내용에 대한 문법 추정이 아니라 eligible manifest의 `archive_path` 확장자를 record
ID로 deterministic join해 산출했다.

# Distribution

| Split | 전체 row | C (`.c`) | C++ (`.cpp`) | unknown/conflict |
| --- | ---: | ---: | ---: | ---: |
| train | 10,000 | 7,814 (78.14%) | 2,186 (21.86%) | 0 |
| validation | 1,000 | 792 (79.20%) | 208 (20.80%) | 0 |
| train + validation | 11,000 | 8,606 (78.24%) | 2,394 (21.76%) | 0 |
| fresh blind challenge | 500 | 402 (80.40%) | 98 (19.60%) | 0 |

# Label Balance

각 언어 내부에서도 `present`와 `not_observed`가 정확히 균형이다.

- train C: 3,907 / 3,907, C++: 1,093 / 1,093
- validation C: 396 / 396, C++: 104 / 104
- blind C: 201 / 201, C++: 49 / 49

고유 source group 수도 각 언어의 label 한쪽 수와 같다. 하나의 source group에서 양 label
pair가 생성된 구조다.

# Provenance Method

- train/validation JSONL schema: `id`, `messages`
- blind challenge schema: `id`, `messages`
- blind gold schema: `id`, `expected_output`
- JSONL과 `dataset_manifest.json`에는 명시적 `language` 필드가 없다.
- train/validation ID는 `phase-f-source-v5-r1/eligible_manifest.parquet`에 100% join된다.
- blind ID는 `phase-f-source-fresh-blind-500-v1/eligible_manifest.parquet`에 100% join된다.
- join된 `archive_path`는 `C/testcases/.../*.c` 또는 `*.cpp`로 끝난다.
- blind gold는 label 균형 확인에만 사용했고 언어 판정은 challenge ID와 eligible manifest로
  수행했다.

# Interpretation

현재 adapter의 검증 범위는 C/C++ source security decision이다. C가 약 78%로 우세하므로
두 언어가 균등하다고 표현하면 안 된다. Java, Python, Rust, Go, binary, assembly와
pseudo-code 성능은 이 데이터로 증명되지 않았다.

# Reproduction

```bash
uv run --no-sync python -c '
import os
from collections import Counter
import pyarrow.parquet as pq

for path in [
    "data/processed/phase-f-source-v5-r1/eligible_manifest.parquet",
    "data/processed/phase-f-source-fresh-blind-500-v1/eligible_manifest.parquet",
]:
    rows = pq.read_table(path).to_pylist()
    print(path)
    print(Counter(
        (row["split"], os.path.splitext(row["archive_path"])[1].lower())
        for row in rows
    ))
'
```

# Related Concepts

- [Mistral G3 Blind 500 Source Decision PASS](../training/mistral_small_4_119b_g3_blind500_decision_20260820.md)
- [Security Datasets](security_datasets.md)
- [Mistral F5-X 첫 파인튜닝 워크북](../training/mistral_f5x_first_finetuning_workbook_20260809.md)
