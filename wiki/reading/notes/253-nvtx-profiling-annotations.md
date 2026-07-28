---
type: Reference
title: "NVTX로 CPU·CUDA 실행 구간에 의미 있는 이름 붙이기"
description: "Python과 C/C++ code를 NVTX range로 표시하고 Nsight Systems에서 병목을 찾는 방법"
resource: https://developer.nvidia.com/ko-kr/blog/nvidia-tools-extension-api-python-%EB%B0%8F-c-c%EC%97%90%EC%84%9C-%EC%BD%94%EB%93%9C%EB%A5%BC-%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%EB%A7%81%ED%95%98%EA%B8%B0-%EC%9C%84%ED%95%9C-%EC%A3%BC%EC%84%9D/
notion: https://app.notion.com/p/dee1a73cf20b8351afb881423d9af787
tags: [reading, nvidia, profiling, cuda]
timestamp: 2026-07-24
status: summarized
---

# 역할

NVTX(NVIDIA Tools Extension)는 application의 함수, loop와 작업 단계에 이름·색·범위를 붙이는 annotation API다. CUDA kernel 이름만 가득한 profiler timeline을 “data loading”, “allocation”, “inference” 같은 domain 작업으로 연결해 병목을 찾기 쉽게 만든다.

# 사용 흐름

Python에서는 `nvtx.annotate` decorator나 context manager로 구간을 감싸고, C/C++에서는 NVTX range API를 사용한다. 그 뒤 다음처럼 Nsight Systems에서 NVTX, OS runtime과 CUDA trace를 함께 수집한다.

```bash
nsys profile -t nvtx,osrt,cuda python app.py
```

Timeline에서는 CPU function, process·thread, NVTX range와 그 아래 실행된 CUDA allocation·copy·kernel의 관계를 확인할 수 있다. Multiprocessing에서도 process별 작업을 구분해 pipeline overlap과 idle time을 찾는 데 도움이 된다.

# 최적화 사례를 읽는 법

반복되는 `cudaMalloc`이 큰 비중을 차지하면 RMM pool allocator처럼 allocation을 재사용하는 방법을 검토할 수 있다. 작은 elementwise kernel이 연속으로 실행되면 `cupy.fuse` 같은 kernel fusion이 launch overhead를 줄일 수 있다.

NVTX 자체는 code를 빠르게 만들지 않는다. 어디서 시간이 쓰이는지 설명 가능한 trace를 만드는 도구다. Annotation overhead를 감안해 대표 workload를 profile하고, 변경 전후 wall time과 correctness를 함께 비교해야 한다.

# 출처

- [NVIDIA Developer Blog](https://developer.nvidia.com/ko-kr/blog/nvidia-tools-extension-api-python-%EB%B0%8F-c-c%EC%97%90%EC%84%9C-%EC%BD%94%EB%93%9C%EB%A5%BC-%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%EB%A7%81%ED%95%98%EA%B8%B0-%EC%9C%84%ED%95%9C-%EC%A3%BC%EC%84%9D/)

