---
type: Concept
title: "SOAP와 REST 차이"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-03-29)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-03-29
status: active
---

# SOAP와 REST 차이

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-03-29

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
HTTP, HTTPS, SMTP 등의 웹 서비스에서 사용되는 XML 기반의 메시지 프로토콜으로서, 다양한 프로그램 언어에서 쉽게 작성 가능하고 실행할 수 있는 프로토콜이 무엇인지 쓰시오.

### 💡 답변 (Assistant)
✅ 문제 분석

제시된 설명의 핵심 포인트는 다음과 같습니다.

- HTTP, HTTPS, SMTP 등 다양한 프로토콜 위에서 동작  
- XML 기반 메시지 구조  
- 다양한 프로그래밍 언어에서 쉽게 구현 가능  
- 웹 서비스에서 사용되는 메시지 프로토콜  

→ 핵심 키워드:  
XML 기반, 웹 서비스, 다양한 프로토콜 지원, 언어 독립성

---

🎯 정답  
👉 SOAP (Simple Object Access Protocol)

---

📌 정답인 이유

SOAP는 웹 서비스에서 사용하는 대표적인 XML 기반 메시지 프로토콜입니다.

구분 | 설명
---|---
기반 | XML
전송 프로토콜 | HTTP, HTTPS, SMTP 등 다양한 프로토콜 사용 가능
특징 | 플랫폼/언어 독립적
목적 | 분산 환경에서 구조화된 정보 교환

문제에서 제시된

- "XML 기반 메시지 프로토콜"  
- "HTTP, HTTPS, SMTP 등에서 사용"  
- "다양한 언어에서 쉽게 작성 가능"  

→ 이 3가지 특징은 SOAP의 정의와 완전히 일치합니다.

---

🔎 헷갈릴 수 있는 오답

❌ REST (Representational State Transfer)

- JSON 기반이 일반적
- 메시지 프로토콜이 아니라 **아키텍처 스타일**
- HTTP에 종속적

→ XML 기반 메시지 프로토콜이 아니므로 오답

---

📚 추가로 공부해야 할 것 (만약 틀렸다면)

SOAP vs REST 차이 → **실기 단골 문제**

구분 | SOAP | REST
---|---|---
형식 | XML | JSON (주로)
성격 | 프로토콜 | 아키텍처 스타일
전송 | HTTP, SMTP 등 다양 | HTTP 기반
구조 | 엄격함 | 유연함

👉 특히 “SOAP = XML”은 무조건 암기

---

🧠 실기시험 포인트 정리

✔ XML 기반 메시지 → SOAP  
✔ JSON 기반 + HTTP → REST  
✔ 프로토콜이다 → SOAP  
✔ 아키텍처 스타일이다 → REST  

👉 “XML + 다양한 프로토콜 지원” 나오면 무조건 SOAP입니다.

---

### 💡 답변 (Assistant)
✅ 문제 분석

제시된 설명의 핵심 포인트는 다음과 같습니다.

- 소프트웨어 보안 취약점  
- 데이터베이스 관련 공격  
- SQL 문을 악의적으로 조작  
- 인증 우회, 데이터 유출 가능  

→ 핵심 키워드:  
SQL 조작, 입력값 검증 부족, DB 공격, 인증 우회

---

🎯 정답  
👉 SQL Injection

---

📌 정답인 이유

SQL Injection은 사용자 입력값을 적절히 검증하지 않을 경우,  
악의적인 SQL 구문이 삽입되어 데이터베이스가 비정상적으로 동작하는 공격 기법입니다.

구분 | 설명
---|---
정의 | 입력값에 SQL 구문을 삽입하여 DB를 조작하는 공격
원인 | 입력값 검증 부족, 동적 쿼리 사용
영향 | 인증 우회, 데이터 조회/변조/삭제
대표 사례 | 로그인 우회 (`' OR 1=1 --`)

📍 예시

```sql
SELECT * FROM users WHERE id = 'admin' AND pw = '1234';
```

→ 공격 입력:

```sql
' OR 1=1 --
```

→ 실행 결과:

```sql
SELECT * FROM users WHERE id = 'admin' AND pw = '' OR 1=1 --';
```

→ 항상 참 → 로그인 우회 성공

---

🔎 헷갈릴 수 있는 오답

❌ XSS (Cross Site Scripting)

- 웹 페이지에 스크립트 삽입
- 클라이언트 공격

→ SQL이 아닌 **스크립트 공격**

❌ CSRF (Cross Site Request Forgery)

- 사용자의 권한을 도용한 요청

→ DB 쿼리 조작과 무관

---

📚 추가로 공부해야 할 것 (만약 틀렸다면)

SQL Injection 방어 기법은 **실기 단골**

1️⃣ 입력값 검증 (Validation)

- 특수문자 필터링
- 화이트리스트 기반 검증

2️⃣ Prepared Statement (매우 중요)

```sql
SELECT * FROM users WHERE id = ? AND pw = ?
```

→ SQL 구조와 데이터를 분리

3️⃣ ORM 사용

→ 자동으로 SQL Injection 방어

4️⃣ 최소 권한 원칙

→ DB 계정 권한 제한

---

🧠 실기시험 포인트 정리

✔ "입력값 검증 부족" → SQL Injection  
✔ "SQL 구문 삽입" → SQL Injection  
✔ "로그인 우회" → SQL Injection 대표 사례  
✔ "Prepared Statement" → 핵심 방어 방법  

👉 “SQL + 입력값 조작” 나오면 무조건 SQL Injection입니다.

---

### ❓ 질문 (User)
소프트웨어 보안의 취약점 중 하나인 SQL Injection에 대해 약술하시오

### 💡 답변 (Assistant)
✅ 문제 분석

제시된 요구는 **서술형 정의 문제**입니다.

→ 핵심은 다음 3가지를 포함해야 합니다.

- 무엇인가 (정의)
- 어떻게 발생하는가 (원인)
- 어떤 문제가 발생하는가 (영향)

→ 핵심 키워드:  
입력값 검증 부족, SQL 구문 삽입, 데이터베이스 조작

---

🎯 정답  
👉 SQL Injection

---

📌 정답 서술 (모범 답안)

**SQL Injection이란, 사용자 입력값에 SQL 구문을 삽입하여 데이터베이스의 쿼리를 변조함으로써 인증 우회, 데이터 조회·변조·삭제 등의 비정상적인 동작을 유발하는 보안 취약점이다.**

---

📌 정답인 이유

SQL Injection은 다음 구조로 이해하면 정확합니다.

구분 | 설명
---|---
발생 원인 | 입력값 검증 부족
공격 방법 | SQL 문에 악의적 구문 삽입
영향 | 인증 우회, 데이터 유출/변조/삭제

문제에서 요구하는 "서술"은  
👉 **정의 + 원인 + 영향**을 포함해야 고득점입니다.

---

🔎 헷갈릴 수 있는 오답

❌ XSS (Cross Site Scripting)

- 클라이언트 측 스크립트 공격

❌ CSRF (Cross Site Request Forgery)

- 사용자 권한을 이용한 요청 위조

→ 둘 다 **DB 쿼리 조작과 무관**

---

📚 추가로 공부해야 할 것 (만약 틀렸다면)

시험에서는 **방어 기법까지 같이 출제되는 경우 많음**

1️⃣ Prepared Statement (가장 중요)

- SQL 구조와 데이터를 분리

2️⃣ 입력값 검증

- 특수문자 제한, 화이트리스트 적용

3️⃣ ORM 사용

- SQL 자동 생성으로 취약점 감소

---

🧠 실기시험 포인트 정리

✔ "SQL 삽입" → SQL Injection  
✔ "입력값 검증 부족" → 발생 원인  
✔ "인증 우회 / 데이터 유출" → 결과  

👉 서술형은 반드시  
**“정의 + 원인 + 결과” 3요소 포함해서 작성**하세요.

---

### ❓ 질문 (User)
SQL Injection에 대해 서술하시오

### 💡 답변 (Assistant)
✅ 문제 분석

제시된 설명의 핵심 포인트는 다음과 같습니다.

- SQL 제어어(DCL 또는 TCL 문맥에서 출제 빈도 높음)  
- 트랜잭션 관련 명령어  
- 작업 취소 / 이전 상태로 복구  

→ 핵심 키워드:  
트랜잭션, 작업 취소, 이전 상태 복원

---

🎯 정답  
👉 ROLLBACK

---

📌 정답 서술 (모범 답안)

**ROLLBACK은 트랜잭션 수행 중 발생한 변경 사항을 취소하고, 마지막 COMMIT 시점 또는 트랜잭션 시작 이전 상태로 되돌리는 명령어이다.**

---

📌 정답인 이유

ROLLBACK은 트랜잭션 제어어(TCL)의 대표적인 명령어로, 데이터의 일관성을 유지하기 위해 사용됩니다.

구분 | 설명
---|---
역할 | 작업 취소
적용 대상 | 트랜잭션 내 변경 내용
기준 시점 | 마지막 COMMIT 또는 BEGIN 이전
목적 | 오류 발생 시 데이터 복구

문제에서 요구하는

- "작업 취소"  
- "이전 상태로 복구"  

→ 이는 ROLLBACK의 정의와 정확히 일치합니다.

---

🔎 헷갈릴 수 있는 오답

❌ COMMIT

- 변경 사항을 **영구 저장**
- 취소가 아닌 확정

❌ SAVEPOINT

- 특정 시점 지정
- 부분 ROLLBACK을 위한 기준점

---

📚 추가로 공부해야 할 것 (만약 틀렸다면)

트랜잭션 제어어(TCL)는 세트로 출제됩니다.

1️⃣ COMMIT

- 작업 완료 후 저장

2️⃣ ROLLBACK

- 작업 취소

3️⃣ SAVEPOINT

- 중간 지점 설정

---

🧠 실기시험 포인트 정리

✔ "작업 취소" → ROLLBACK  
✔ "영구 반영" → COMMIT  
✔ "중간 복구 지점" → SAVEPOINT  

👉 시험에서는 반드시 **COMMIT vs ROLLBACK 대비**로 기억하세요.

---

### ❓ 질문 (User)
SQL 제어어(DCL) 중 ROLLBACK 명령에 대해 약술하시오

### 💡 답변 (Assistant)
✅ 문제 분석

제시된 설명의 핵심 포인트는 다음과 같습니다.

- 재해 복구(Disaster Recovery) 관련 용어  
- 복구 대상이 정상 상태로 돌아올 때까지의 시간  
- “최대로 허용하는 대기 시간”  

→ 핵심 키워드:  
복구 시간, 허용 가능한 최대 시간, 서비스 중단 시간

---

🎯 정답  
👉 RTO (Recovery Time Objective)

---

📌 정답인 이유

RTO는 재해 발생 후 시스템이나 서비스가 정상적으로 복구되기까지  
**허용되는 최대 시간**을 의미합니다.

구분 | 설명
---|---
의미 | 복구 목표 시간
기준 | 서비스 중단 후 복구 완료까지
목적 | 서비스 연속성 확보
단위 | 시간 (분, 시간 등)

문제에서 제시된

- "복구되기까지의 최대로 허용하는 대기 시간"

→ 이는 RTO의 정의와 정확히 일치합니다.

---

🔎 헷갈릴 수 있는 오답

❌ RPO (Recovery Point Objective)

- 데이터 손실 허용 범위 (시간 기준)
- “얼마나 과거 데이터까지 복구 가능한가”

→ 시간은 맞지만 **복구 시점 기준**이라 다른 개념

---

📚 추가로 공부해야 할 것 (만약 틀렸다면)

RTO vs RPO는 **세트로 반드시 암기**

구분 | RTO | RPO
---|---|---
의미 | 복구까지 걸리는 시간 | 데이터 손실 허용 범위
초점 | 서비스 복구 시간 | 데이터 복구 시점
질문 형태 | “언제까지 복구?” | “어디까지 복구?”

---

🧠 실기시험 포인트 정리

✔ "복구 시간" → RTO  
✔ "데이터 손실 범위" → RPO  
✔ "최대 허용 시간" → RTO  

👉 “시간(복구까지)” 나오면 무조건 RTO입니다.

---

### ❓ 질문 (User)
재해 복구 시스템에서 주로 사용되는 용어로, 복구 대상이 복구되기 까지의 최대로 허용하는 대기 시간을 의미하는 것이 무엇인지 약어로 쓰시오.

### ❓ 질문 (User)
신기술 동향과 관련된 설명에 가장 부합하는 용어
---
- 사용자가 정확하게 원하는 정보를 찾을 수 있도록 웹상의 모든 데이터와 데이터베이스를 무료로 공개하고 연계하는 것이다.
- 웹에 게시되는 데이터에 식별자(URI)를 부여하고 관련 정보를 구조적으로 제공하는 연계 데이터를 저작권 없이 무료로 제공하여 사용자가 정보를 다양하고 효율적으로 활용할 수 있도록 한다.
- 데이터를 재사용할 수 있고, 데이터 중복을 줄일 수 있다는 장점이 있다.

### 💡 답변 (Assistant)
✅ 문제 분석

제시된 설명의 핵심 포인트는 다음과 같습니다.

- 웹상의 데이터 및 DB를 무료 공개  
- 데이터에 식별자(URI) 부여  
- 구조화된 데이터 제공  
- 데이터 간 연계 (Linked)  
- 저작권 없이 자유롭게 활용 가능  
- 재사용 가능, 중복 감소  

→ 핵심 키워드:  
URI, 데이터 공개, 연계 데이터, 재사용, 무료 제공

---

🎯 정답  
👉 LOD (Linked Open Data)

---

📌 정답인 이유

LOD는 웹 상의 데이터를 **URI로 식별하고**,  
서로 연결하여 **개방(Open)** 형태로 제공하는 데이터 구조입니다.

구분 | 설명
---|---
Linked | 데이터 간 연결
Open | 누구나 자유롭게 사용 가능
Data | 구조화된 데이터 제공
핵심 기술 | URI, RDF 등

문제에서 제시된

- "URI를 부여"  
- "데이터를 구조적으로 제공"  
- "무료 공개 및 재사용 가능"  

→ 이는 LOD의 정의와 완전히 일치합니다.

---

🔎 헷갈릴 수 있는 오답

❌ 빅데이터 (Big Data)

- 대용량 데이터 처리 기술
- 데이터 공개/연계 개념 아님

❌ 시맨틱 웹 (Semantic Web)

- 의미 기반 웹 기술
- LOD의 상위 개념

→ 문제는 **데이터 공개 + 연계 + URI** → LOD

---

📚 추가로 공부해야 할 것 (만약 틀렸다면)

LOD 관련 핵심 기술

1️⃣ URI

- 데이터 식별자

2️⃣ RDF (Resource Description Framework)

- 데이터 구조 표현

3️⃣ SPARQL

- 데이터 질의 언어

---

🧠 실기시험 포인트 정리

✔ "URI로 식별" → LOD  
✔ "데이터 연결" → Linked  
✔ "무료 공개" → Open  
✔ "재사용 가능" → LOD 특징  

👉 “URI + 데이터 공개 + 연계” 나오면 무조건 LOD입니다.

---

### 💡 답변 (Assistant)
✅ 문제 분석

제시된 설명의 핵심 포인트는 다음과 같습니다.

- EAI(Enterprise Application Integration) 유형  
- 총 4가지 유형  
- 이미 제시된 것:  
  - Message Bus  
  - Hybrid  
- 나머지 2가지 유형을 묻는 문제  

→ 핵심 키워드:  
EAI 유형, 4가지 구조

---

🎯 정답  
👉 (1) Point-to-Point  
👉 (2) Hub & Spoke

---

📌 정답인 이유

EAI의 대표적인 4가지 유형은 다음과 같습니다.

구분 | 설명
---|---
Point-to-Point | 시스템 간 1:1 직접 연결
Hub & Spoke | 중앙 허브를 통해 통합
Message Bus | 버스를 통한 메시지 기반 통합
Hybrid | 여러 방식 혼합

문제에서 이미

- Message Bus  
- Hybrid  

가 주어졌으므로 나머지는

👉 Point-to-Point  
👉 Hub & Spoke  

가 됩니다.

---

🔎 헷갈릴 수 있는 오답

❌ ESB (Enterprise Service Bus)

- Message Bus의 확장 개념
- EAI 유형 이름으로 직접 출제되진 않음

❌ SOA

- 아키텍처 스타일
- EAI 유형이 아님

---

📚 추가로 공부해야 할 것 (만약 틀렸다면)

EAI 유형 특징 비교 (시험 자주 출제)

유형 | 특징 | 단점
---|---|---
Point-to-Point | 단순, 빠른 구축 | 연결 증가 시 복잡도 급증
Hub & Spoke | 중앙 집중 관리 | 허브 장애 시 전체 영향
Message Bus | 확장성 우수 | 설계 복잡
Hybrid | 장점 혼합 | 관리 복잡

---

🧠 실기시험 포인트 정리

✔ EAI 4가지 유형 → **Point-to-Point / Hub & Spoke / Message Bus / Hybrid**  
✔ “중앙 허브” → Hub & Spoke  
✔ “1:1 연결” → Point-to-Point  
✔ “버스 기반” → Message Bus  

👉 EAI 유형은 **4개 세트 암기 필수**입니다.

---

### ❓ 질문 (User)
EAI 유형에는 메세지 버스(Message bus), 하이브리드(Hybrid), (   1.  ), (   2.   ) 4가지가 있다.

### 💡 답변 (Assistant)
✅ 문제 분석

제시된 코드의 핵심 포인트는 다음과 같습니다.

- 추상 클래스 `Vehicle`  
- 메서드 **오버로딩 vs 오버라이딩**  
- 참조 변수 타입 vs 실제 객체 타입 (**다형성**)  
- `getName()` 호출 시 어떤 메서드가 실행되는가  

→ 핵심 키워드:  
오버라이딩, 오버로딩, 다형성, 메서드 바인딩

---

🎯 정답  
👉 **vehicle name:Spark**

---

📌 정답인 이유

### 1️⃣ 객체 생성 구조

```java
Vehicle obj = new Car("Spark");
```

- 참조 타입: `Vehicle`
- 실제 객체: `Car`

👉 **다형성 적용**

---

### 2️⃣ 생성자 실행

```java
public Car(String val){
    setName(val);
}
```

→ `Vehicle`의 `setName()` 실행  
→ `name = "Spark"` 저장

---

### 3️⃣ 호출 메서드 분석

```java
System.out.print(obj.getName());
```

👉 호출된 메서드:

```java
public String getName(){
    return "vehicle name:" + name;
}
```

---

### 4️⃣ 핵심 포인트 (시험 핵심🔥)

Car 클래스에는

```java
public String getName(String val)   // 오버라이딩
public String getName(byte val[])   // 오버로딩
```

👉 하지만 중요한 점

- `getName()` (매개변수 없음) 은 **Car에서 재정의되지 않음**
- 따라서 **Vehicle의 메서드 사용**

---

### 5️⃣ 최종 실행 흐름

- name = "Spark"
- Vehicle.getName() 호출

👉 결과:

```
vehicle name:Spark
```

---

🔎 헷갈릴 수 있는 포인트

❌ "Car 객체니까 Car 메서드 실행 아닌가?"

→ ❗ 틀림

- **오버라이딩된 메서드만 동적 바인딩**
- 없는 메서드는 부모 메서드 사용

---

❌ getName(String val) 호출된다고 착각

→ ❗ 매개변수가 없음 → 전혀 다른 메서드

---

📚 추가로 공부해야 할 것 (매우 중요🔥)

### 1️⃣ 오버라이딩 vs 오버로딩

구분 | 오버라이딩 | 오버로딩
---|---|---
조건 | 상속 관계 | 같은 클래스
메서드명 | 동일 | 동일
매개변수 | 동일 | 다름
실행 시점 | 런타임 (동적 바인딩) | 컴파일 타임

---

### 2️⃣ 다형성 핵심

```java
부모타입 변수 = 자식객체
```

- 호출 가능 메서드 → **부모 기준**
- 실행 메서드 → **자식(오버라이딩 시)**

---

🧠 실기시험 포인트 정리

✔ "매개변수 다르면" → 오버로딩  
✔ "같은 시그니처" → 오버라이딩  
✔ "오버라이딩 안 했으면" → 부모 메서드 실행  
✔ "참조 타입 기준으로 호출 가능 여부 결정"  

👉 이 문제는 **오버라이딩 + 다형성 함정 문제**입니다.

---

### ❓ 질문 (User)
```java
abstract class vehicle{
	private String name;
    abstract public String getName(String val);
    public String getName(){
    	return "vehicle name:" + name;
    }
	public void setName(String val){
    	name = val;
    }
}

class Car extends Vehicle{
	public Car(String val){
    	setName(val);
   }
public String getName(String val){
	return "Car name : " + val;
   }
public String getName(byte val[]){
	return "Car name : " + val;
   }
}

public class good {
	public Static void main(String[] args){
    Vehicle obj = new Car("Spark");
    System.out.print(obj.getName());
    }
}
```
출력결과는?
