---
type: Reference
title: "LLM 생성 code는 compile 성공보다 invariant와 성능 기준으로 검증해야 한다"
description: "Rust로 재작성한 SQLite 사례가 보여주는 그럴듯한 구현과 실제 correctness·performance의 간극"
resource: https://news.hada.io/topic?id=27296
notion: https://app.notion.com/p/1771a73cf20b8373a69781be06dbcfc5
tags: [reading, ai-coding, software-quality, testing]
timestamp: 2026-07-24
status: summarized
---

# 사례

글은 LLM이 생성한 Rust SQLite 재구현이 compile되고 file format test도 통과했지만, 100-row primary-key lookup에서 원본 SQLite의 0.09ms보다 약 20,000배 느린 1,815.43ms를 기록한 사례를 든다.

원인은 언어 선택이 아니라 database invariant를 구현하지 못한 데 있었다. PRIMARY KEY를 index lookup으로 처리하지 않았고 query마다 `fsync`를 호출해, 겉보기 API와 test는 맞아도 핵심 algorithm과 durability path가 비정상이었다.

# 무엇을 배워야 하나

“SQLite를 Rust로 다시 써라”는 기능 범위만 있고 성공 기준은 없다. Agent는 compile과 제공된 test 통과처럼 쉽게 관찰되는 목표를 최적화한다. Baseline의 algorithmic property, latency·throughput, crash consistency와 compatibility를 명시하지 않으면 느리지만 그럴듯한 결과가 나올 수 있다.

# 실전 검증 순서

1. 기존 system의 observable contract와 반드시 지켜야 할 invariant를 적는다.
2. Functional test 외에 representative benchmark와 failure injection을 만든다.
3. Agent가 구현하기 전에 acceptance threshold를 고정한다.
4. Profile로 병목을 찾아 algorithmic complexity와 I/O path를 검토한다.
5. 성능이 좋아도 data corruption, concurrency와 recovery를 따로 시험한다.

# 균형 잡힌 해석

한 번의 SQLite clone 사례가 모든 LLM code가 틀렸다는 증거는 아니다. 요구사항이 지나치게 넓었고 baseline은 수십 년간 최적화된 system이다. 그래도 “compile + unit test = correct”가 아니라는 점과, 명시적 evaluator 없이는 agent가 숨은 품질을 최적화하지 않는다는 교훈은 유효하다.

# 출처

- [GeekNews 요약과 토론](https://news.hada.io/topic?id=27296)

