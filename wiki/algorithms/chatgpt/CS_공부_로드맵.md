---
type: Concept
title: "CS 공부 로드맵"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-06-02)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-06-02
status: active
---

# CS 공부 로드맵

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-02

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
너는 베테랑 머신러닝 엔지니어잖아. 요즘 이쪽 취업하려니까 알고리즘 코딩 테스트를 거의 안본대. Cs를 더 깐깐하게 보나봐. Cs 카테고리를 크게 카테고리로 한 다음에 세부적으로 나누면서 공부하려고. 도와줘

### 💡 답변 (Assistant)
좋은 방향이야.

실제로 2025~2026년 기준으로 머신러닝 엔지니어(MLE), LLM Engineer, AI Engineer 채용을 보면 예전처럼 "백준 골드~플래티넘 수준 알고리즘"을 강하게 요구하는 곳은 줄어들고, 대신 **CS + 시스템 + ML 실무 이해**를 훨씬 깊게 보는 추세야.

특히 너처럼 **비전공 → 머신러닝 엔지니어 전환**을 목표로 한다면 알고리즘보다 CS가 투자 대비 효율이 훨씬 좋다.

---

# 전체 로드맵

```text
CS
├── 1. 운영체제 (OS)
├── 2. 컴퓨터 네트워크
├── 3. 데이터베이스
├── 4. 자료구조 & 알고리즘
├── 5. 컴퓨터 구조
├── 6. Linux & System
├── 7. Software Engineering
├── 8. Distributed System
├── 9. MLOps & Serving
└── 10. AI System Design
```

---

# 1. 운영체제 (최우선)

MLE 면접에서 제일 많이 나옴.

---

## Process

```text
프로세스
├── 프로그램과 차이
├── PCB
├── Context Switching
├── Process State
└── Parent Child Process
```

질문 예시

- 프로세스와 프로그램 차이
- Context Switch 비용
- fork() 동작

---

## Thread

```text
스레드
├── User Thread
├── Kernel Thread
├── Multi Thread
├── Thread Pool
└── GIL
```

특히 Python

- GIL
- multiprocessing
- multithreading

엄청 나옴.

---

## Memory

```text
메모리
├── Stack
├── Heap
├── Data
├── Code
├── Virtual Memory
├── Paging
├── Segmentation
├── TLB
└── Page Fault
```

질문

- Stack vs Heap
- Python 객체는 어디 저장?
- Page Fault란?

---

## Synchronization

```text
동기화
├── Race Condition
├── Mutex
├── Semaphore
├── Deadlock
├── Starvation
└── Livelock
```

---

## CPU Scheduling

```text
FCFS
SJF
SRT
RR
Priority
MLQ
MLFQ
```

---

# 2. 네트워크 (최우선)

LLM 서비스 운영에서는 필수.

---

## OSI 7 Layer

```text
Application
Transport
Network
Data Link
Physical
```

---

## TCP/IP

```text
TCP
├── 3 Way Handshake
├── 4 Way Handshake
├── Flow Control
├── Congestion Control
└── Retransmission

UDP
```

질문

- TCP와 UDP 차이
- 왜 TCP가 느린가

---

## HTTP

```text
HTTP
├── GET
├── POST
├── PUT
├── PATCH
├── DELETE
├── Status Code
└── Header
```

---

## HTTPS

```text
HTTPS
├── TLS
├── 공개키
├── 대칭키
└── 인증서
```

---

## DNS

```text
브라우저 주소 입력
↓
DNS
↓
IP 획득
↓
TCP 연결
↓
HTTP 요청
```

엄청 자주 나옴.

---

# 3. 데이터베이스

---

## RDBMS

```text
DB
├── Primary Key
├── Foreign Key
├── Index
├── Join
├── Normalization
└── Transaction
```

---

## Index

중요

```text
B Tree
B+ Tree
Clustered
Non Clustered
```

질문

- 인덱스가 왜 빠른가
- 인덱스를 많이 만들면 왜 안 좋은가

---

## Transaction

```text
ACID
```

```text
Atomicity
Consistency
Isolation
Durability
```

---

## Isolation Level

```text
Read Uncommitted
Read Committed
Repeatable Read
Serializable
```

---

# 4. 자료구조 & 알고리즘

예전보다 비중 감소.

하지만 버릴 수 없음.

---

## 필수

```text
Array
Linked List
Stack
Queue
Heap
Hash Table
Tree
Graph
```

---

## 알고리즘

```text
BFS
DFS
Binary Search
Union Find
Dijkstra
DP
Greedy
```

너는 이미 상당 부분 공부함.

---

# 5. 컴퓨터 구조

요즘 AI 엔지니어는 중요도가 올라감.

---

## CPU

```text
ALU
CU
Register
Cache
```

---

## Cache

```text
L1
L2
L3
```

질문

- 캐시가 왜 빠른가
- Locality란?

---

## Memory Hierarchy

```text
Register
Cache
RAM
SSD
Disk
```

---

## GPU

MLE라면 추가

```text
CUDA Core
SM
Warp
HBM
VRAM
```

질문

- GPU가 왜 행렬연산에 유리한가

---

# 6. Linux & System

실무에서 매우 중요

---

## 명령어

```text
ls
cd
pwd
find
grep
awk
sed
tail
head
```

---

## Process

```text
ps
top
htop
kill
nohup
screen
tmux
```

---

## 권한

```text
chmod
chown
sudo
```

---

## 로그

```text
journalctl
systemctl
```

---

# 7. Software Engineering

생각보다 많이 물어봄.

---

## OOP

```text
Encapsulation
Inheritance
Polymorphism
Abstraction
```

---

## Design Pattern

```text
Singleton
Factory
Strategy
Observer
```

---

## SOLID

```text
SRP
OCP
LSP
ISP
DIP
```

---

# 8. Distributed System

최근 MLE 필수 영역

---

## 기본

```text
Scale Up
Scale Out
```

---

## Consistency

```text
CAP Theorem
```

---

## Message Queue

```text
Kafka
RabbitMQ
```

---

## Cache

```text
Redis
```

---

# 9. MLOps & Serving

MLE 핵심

---

## Docker

```text
Image
Container
Volume
Network
```

---

## Kubernetes

```text
Pod
Deployment
Service
Ingress
```

---

## Serving

```text
FastAPI
Triton
vLLM
TorchServe
```

너는 이미 vLLM을 만지고 있어서 강점이 있음.

---

# 10. AI System Design

2026년 이후 가장 중요

---

## RAG

```text
Chunking
Embedding
Vector DB
Retrieval
Re-ranking
```

---

## LLM Serving

```text
KV Cache
Batching
Prefill
Decode
Speculative Decoding
```

---

# 너에게 추천하는 학습 순서

현재 수준을 고려하면:

```text
1개월
운영체제
네트워크

2개월
데이터베이스
컴퓨터구조

3개월
Linux
Software Engineering

4개월
Distributed System

5개월
Docker
Kubernetes
MLOps

6개월
LLM System Design
```

특히 너는 이미 PyTorch, CUDA 사용 경험, vLLM 로그 분석, Ubuntu 환경 구축 경험이 있으므로 일반 신입보다 **MLOps/서빙 쪽 이해도가 빠르게 올라갈 가능성이 높아**.

면접 대비 효율만 따지면 현재 시점에서 우선순위는:

```text
운영체제
>
네트워크
>
데이터베이스
>
컴퓨터구조
>
Linux
>
Distributed System
>
MLOps
>
알고리즘
```

이 순서로 "면접 질문 500개를 커버하는 CS 트리" 형태로 더 세분화해서 로드맵을 만들어줄 수도 있어. 그러면 각 항목별로 "면접관이 실제로 물어보는 질문"까지 연결해서 정리해줄게.

---
