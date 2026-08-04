---
type: Concept
title: "SQL 쿼리 선택 문제"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-08-17)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-08-17
status: active
---

# SQL 쿼리 선택 문제

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-08-17

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
정답: **B) COUNT, ON, GROUP**

### 왜 B가 맞나요?
- **COUNT**: 주문 개수를 세야 하므로 `COUNT(OrderID)`가 맞습니다. `SUM`은 합계를 낼 때 사용합니다.
- **ON**: 조인 조건을 명시할 때 `JOIN ... ON ...`을 사용합니다. (`USING`은 두 테이블의 조인 키 이름이 완전히 같을 때만 가능하고, 보기 D는 마지막이 `ORDER`라 집계가 안 됩니다.)
- **GROUP BY**: 고객별로 묶어서(그룹화) 주문 수를 집계해야 하므로 `GROUP BY Customer.Name` (또는 더 안전하게 `GROUP BY Customer.CustomerID`)가 필요합니다. `HAVING`은 그룹화된 결과에 **조건을 거를 때** 쓰는 절입니다(집계 자체를 만드는 건 아님).

---

## 예시 데이터 만들기

> 아래 예시에서는 질문의 결과 표에 **Rose**가 있으므로, Customer에 Rose(104)를 추가합니다.

```sql
-- 테이블 생성
CREATE TABLE Customer (
  CustomerID INT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL
);

CREATE TABLE Order_Test (
  OrderID INT PRIMARY KEY,
  CustomerID INT NOT NULL,
  OrderDate DATE,
  FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- 고객 데이터
INSERT INTO Customer (CustomerID, Name) VALUES
(101, 'James'),
(102, 'Alex'),
(103, 'Kate'),
(104, 'Rose');

-- 주문 데이터 (James 6건, Alex 3건, Kate 3건, Rose 3건)
INSERT INTO Order_Test (OrderID, CustomerID, OrderDate) VALUES
(1, 101, '2025-01-01'),
(2, 101, '2025-01-05'),
(3, 101, '2025-02-11'),
(4, 101, '2025-03-20'),
(5, 101, '2025-04-02'),
(6, 101, '2025-04-18'),

(7, 102, '2025-01-03'),
(8, 102, '2025-02-14'),
(9, 102, '2025-03-01'),

(10, 103, '2025-02-02'),
(11, 103, '2025-02-10'),
(12, 103, '2025-03-07'),

(13, 104, '2025-01-09'),
(14, 104, '2025-03-15'),
(15, 104, '2025-04-01');
```

---

## 정답 쿼리

```sql
SELECT c.Name, COUNT(ot.OrderID) AS OrderCount
FROM Customer AS c
JOIN Order_Test AS ot ON c.CustomerID = ot.CustomerID
GROUP BY c.Name;
```

### 결과
```
Name  | OrderCount
------+-----------
James | 6
Alex  | 3
Kate  | 3
Rose  | 3
```

---

## 실무 팁 (중요)
- **그룹 키는 PK로!** 이름은 중복될 수 있어요. 더 안전하게는 아래처럼:
  ```sql
  SELECT c.Name, COUNT(*) AS OrderCount
  FROM Customer c
  JOIN Order_Test ot ON c.CustomerID = ot.CustomerID
  GROUP BY c.CustomerID, c.Name;
  ```
- **주문이 0건인 고객도 보고 싶다면** `JOIN` → `LEFT JOIN`:
  ```sql
  SELECT c.Name, COUNT(ot.OrderID) AS OrderCount
  FROM Customer c
  LEFT JOIN Order_Test ot ON c.CustomerID = ot.CustomerID
  GROUP BY c.CustomerID, c.Name;
  ```
- **집계 조건**은 `HAVING`:
  ```sql
  -- 주문이 3건 이상인 고객만
  SELECT c.Name, COUNT(*) AS OrderCount
  FROM Customer c
  JOIN Order_Test ot ON c.CustomerID = ot.CustomerID
  GROUP BY c.CustomerID, c.Name
  HAVING COUNT(*) >= 3;
  ```

다음 질문 주세요—윈도우 함수, 롤업/큐브, 서브쿼리/CTE, 성능튜닝(인덱스/실행계획)까지 차근차근 가봅시다.

---

### ❓ 질문 (User)
너는 15년차 데이터 엔지니어야. 나에게 SQL 강의를 해주고 있어. 내가 앞으로 하는 질문에 대해서 상세하게 설명해주고 예시 데이터를 입력해줘.
[Data]
CustomerID | Name |
101 | James |
102 | Alex |
103 | Kate | 

---
SELECT `Customer`.Name, ??? (`Order_Test`.OrderID) as 'OrderCount'
FROM Customer
JOIN Order_Test ??? Customer.CustomerID = Order_Test.CustomerID
??? BY Customer.Name;
---
Name | OrderCount |
James | 6 |
Alex | 3 |
Kate | 3 | 
Rose | 3 |
---

A) SUM, ON, GROUP
B) COUNT, ON, GROUP
C) COUNT, ON, HAVING
D) COUNT, USING, ORDER

### 💡 답변 (Assistant)
정답: **D) WHERE, ORDER, DESC** ✅

---

## 이유 설명
1. **조건 필터링 → WHERE**  
   - `OrderDate >= '2024-01-01'` 같이 **행을 필터링**할 때는 `WHERE`를 사용합니다.  
   - `HAVING`은 집계 결과(예: COUNT, SUM 등)에 조건을 걸 때 사용합니다.

2. **정렬 → ORDER BY**  
   - 결과를 정렬할 때는 항상 `ORDER BY`를 씁니다.  
   - `GROUP BY`는 그룹화할 때만 쓰는 절이라 여기서는 틀립니다.

3. **내림차순 정렬 → DESC**  
   - 최근 날짜부터 정렬하려면 `DESC`(내림차순).  
   - `ASC`는 오름차순(가장 오래된 것부터).

---

## 올바른 쿼리

```sql
SELECT Order_Test.OrderID, Order_Test.CustomerID, Order_Test.OrderDate
FROM Order_Test
WHERE Order_Test.OrderDate >= '2024-01-01'
ORDER BY Order_Test.OrderDate DESC;
```

---

## 실행 결과 예시 (앞서 넣었던 데이터 기반)

```
OrderID | CustomerID | OrderDate
--------+------------+------------
15      | 104        | 2025-04-01
6       | 101        | 2025-04-18
5       | 101        | 2025-04-02
14      | 104        | 2025-03-15
12      | 103        | 2025-03-07
...
```

즉, **2024-01-01 이후 주문만 나오고, 최근 날짜가 위에 표시됩니다.**

---

👉 다음 단계로 제가 `HAVING` 절과 `WHERE` 절의 차이를 실제 예제로 비교해 드릴까요?

---

### ❓ 질문 (User)
Q2. Choose the correct option that fills in the blanks ??? in order.
(Purpose:
1. Select only the data where the order date is on or after ‘2024-01-01’.
2. Sort the data by order date in descending (most recent first) order.)
[Query]
SELECT Order_Test.OrderID, Order_Test.CustomerID, Order_Test.OrderDate
FROM Order_Test
??? Order_Test.OrderDate >= '2024-01-01'
??? BY Order_Test.OrderDate ???;

A) WHERE, GROUP, ASC
B) HAVING, GROUP, DESC
C) WHERE, ORDER, ASC
D) WHERE, ORDER, DESC

### 💡 답변 (Assistant)
좋습니다 👍  
이제 사용자가 올려준 **실제 Customer / Order_Test 데이터**를 기반으로 Q1 문제를 다시 풀어볼게요.  

---

## 📌 문제 Q1 (다시)

**목표:**  
- 고객별 주문 개수를 구하라.  
- 결과 예시:  
  ```
  Name  | OrderCount
  -------------------
  James | 6
  Alex  | 3
  Kate  | 3
  Rose  | 3
  ```

---

## 📊 입력 데이터

### Customer
| CustomerID | Name  |
|------------|-------|
| 101        | James |
| 102        | Alex  |
| 103        | Kate  |
| 104        | Rose  |

### Order_Test
| OrderID | CustomerID | OrderDate   |
|---------|------------|-------------|
| a-001   | 101        | 2023-01-24  |
| a-002   | 101        | 2023-01-24  |
| a-003   | 101        | 2024-01-10  |
| a-004   | 101        | 2024-01-12  |
| a-005   | 101        | 2024-01-13  |
| a-006   | 101        | 2024-04-01  |
| b-001   | 102        | 2024-01-15  |
| b-002   | 102        | 2024-01-17  |
| b-003   | 102        | 2024-04-05  |
| c-001   | 103        | 2024-02-15  |
| c-002   | 103        | 2024-02-20  |
| c-003   | 103        | 2024-04-10  |
| d-001   | 104        | 2023-01-12  |
| d-002   | 104        | 2023-03-12  |
| d-003   | 104        | 2023-04-13  |

---

## ✅ 정답 SQL

```sql
SELECT c.Name, COUNT(o.OrderID) AS OrderCount
FROM Customer c
JOIN Order_Test o ON c.CustomerID = o.CustomerID
GROUP BY c.Name;
```

---

## 📝 결과 해석

실제 데이터로 COUNT를 세면:

- **James (101)** → a-001 ~ a-006 → **6건**  
- **Alex (102)** → b-001 ~ b-003 → **3건**  
- **Kate (103)** → c-001 ~ c-003 → **3건**  
- **Rose (104)** → d-001 ~ d-003 → **3건**

### 결과 테이블
```
Name  | OrderCount
------+-----------
James | 6
Alex  | 3
Kate  | 3
Rose  | 3
```

---

## 🔎 따라서 1번 문제 정답은?
👉 **B) COUNT, ON, GROUP**

---

원한다면 지금 데이터 기준으로 Q2 (`WHERE`, `ORDER BY`, `DESC`) 도 같이 실행해 드릴까요?

---

### ❓ 질문 (User)
입력 데이터는 다음과 같아. 이 데이터를 기반으로 1번부터 다시 응답해줘.

### 💡 답변 (Assistant)
좋습니다 👍 Q2도 지금 사용자가 제공한 **실제 데이터(Customer + Order_Test)**를 기반으로 다시 풀어드릴게요.  

---

## 📌 문제 Q2
**조건**  
1. `OrderDate >= '2024-01-01'` 인 데이터만 선택한다. (**2024년 이후 주문**)  
2. `OrderDate` 기준으로 **내림차순(DESC, 최신순)** 정렬한다.  

---

## ✅ 정답 SQL
```sql
SELECT o.OrderID, o.CustomerID, o.OrderDate
FROM Order_Test o
WHERE o.OrderDate >= '2024-01-01'
ORDER BY o.OrderDate DESC;
```

👉 따라서 정답은 **D) WHERE, ORDER, DESC**

---

## 📊 데이터 필터링 과정

### 원본 Order_Test
| OrderID | CustomerID | OrderDate   |
|---------|------------|-------------|
| a-001   | 101        | 2023-01-24  |
| a-002   | 101        | 2023-01-24  |
| a-003   | 101        | 2024-01-10  |
| a-004   | 101        | 2024-01-12  |
| a-005   | 101        | 2024-01-13  |
| a-006   | 101        | 2024-04-01  |
| b-001   | 102        | 2024-01-15  |
| b-002   | 102        | 2024-01-17  |
| b-003   | 102        | 2024-04-05  |
| c-001   | 103        | 2024-02-15  |
| c-002   | 103        | 2024-02-20  |
| c-003   | 103        | 2024-04-10  |
| d-001   | 104        | 2023-01-12  |
| d-002   | 104        | 2023-03-12  |
| d-003   | 104        | 2023-04-13  |

### ① WHERE 조건 적용 (2024-01-01 이후만)
```
a-003 (2024-01-10)
a-004 (2024-01-12)
a-005 (2024-01-13)
a-006 (2024-04-01)
b-001 (2024-01-15)
b-002 (2024-01-17)
b-003 (2024-04-05)
c-001 (2024-02-15)
c-002 (2024-02-20)
c-003 (2024-04-10)
```

### ② ORDER BY OrderDate DESC (최신순 정렬)
| OrderID | CustomerID | OrderDate   |
|---------|------------|-------------|
| c-003   | 103        | 2024-04-10  |
| b-003   | 102        | 2024-04-05  |
| a-006   | 101        | 2024-04-01  |
| c-002   | 103        | 2024-02-20  |
| c-001   | 103        | 2024-02-15  |
| b-002   | 102        | 2024-01-17  |
| b-001   | 102        | 2024-01-15  |
| a-005   | 101        | 2024-01-13  |
| a-004   | 101        | 2024-01-12  |
| a-003   | 101        | 2024-01-10  |

---

## ✅ 최종 정리
- 조건문: **WHERE**  
- 정렬문: **ORDER BY**  
- 정렬방향: **DESC**  
👉 정답: **D) WHERE, ORDER, DESC**

---

혹시 Q3로 넘어가면서 `HAVING` 절과 `WHERE` 절 차이를 **이 데이터에 직접 적용해서** 비교해드릴까요?

---

### ❓ 질문 (User)
Q2 도 알려줘.

### ❓ 질문 (User)
Q3. Choose the correct option that fills in the blanks ??? in order.
(Purpose:
1. Keep only the data where the order ID starts with 'a' or 'b'.
2. Sort the data by the most recent date and extract the top 5 records.)
[Query]
SELECT *
FROM Order_Test
WHERE Order_Test.OrderID ??? 'a%' or Order_Test.OrderID ??? 'b%'
??? BY Order_Test.OrderDate ???
??? 5;

A) LIKE, LIKE, ORDER, DESC, LIMIT
B) LIKE, IN, GROUP, ASC, OFFSET
C) IN, IN, ORDER, ASC, LIMIT
D) LIKE, LIKE, GROUP, DESC, LIMIT

다음 그림과 같이 나오는 선택지를 골라줘.

### 💡 답변 (Assistant)
좋습니다 👍 지금 주신 **결과 화면 (Result Grid)** 와 조건을 맞춰서 보겠습니다.  

---

## 📌 문제 Q3 조건
1. `OrderID` 가 `'a'` 또는 `'b'`로 시작하는 행만 가져온다.  
   → `LIKE 'a%'` 또는 `LIKE 'b%'`  
2. `OrderDate` 기준으로 최신순 정렬 (**DESC**)  
3. 상위 5개만 추출 (**LIMIT 5**)  

---

## ✅ 정답 SQL
```sql
SELECT *
FROM Order_Test
WHERE Order_Test.OrderID LIKE 'a%' OR Order_Test.OrderID LIKE 'b%'
ORDER BY Order_Test.OrderDate DESC
LIMIT 5;
```

---

## 📝 실행 결과 (사용자 제공 캡처와 동일)
| OrderID | CustomerID | OrderDate   |
|---------|------------|-------------|
| b-003   | 102        | 2024-04-05  |
| a-006   | 101        | 2024-04-01  |
| b-002   | 102        | 2024-01-17  |
| b-001   | 102        | 2024-01-15  |
| a-005   | 101        | 2024-01-13  |

---

## ✅ 정답 선택지
👉 **A) LIKE, LIKE, ORDER, DESC, LIMIT**

---

혹시 이어서 Q4로 `HAVING` vs `WHERE` 차이를 이 데이터로 직접 비교해드릴까요?

---

### ❓ 질문 (User)
Q4. What is the role of the WHERE clause in a database?
A) Insert data
B) Change the order of data
C) Group data
D) Filter data based on specific conditions

### 💡 답변 (Assistant)
좋은 질문이에요 👍  

---

## 📌 Q4. What is the role of the **WHERE** clause in a database?

- **A) Insert data** → ❌ `INSERT`문으로 하는 작업.  
- **B) Change the order of data** → ❌ `ORDER BY`로 하는 작업.  
- **C) Group data** → ❌ `GROUP BY`로 하는 작업.  
- **D) Filter data based on specific conditions** → ✅ 정답!  

---

## ✅ 정답
👉 **D) Filter data based on specific conditions**

---

## 🔎 예시 (실제 데이터 기반)

```sql
-- 2024년 이후 주문만 필터링
SELECT *
FROM Order_Test
WHERE OrderDate >= '2024-01-01';
```

**결과:**  
2024년 1월 1일 이후의 주문만 남기고, 2023년도 주문은 제외됨.  

즉, `WHERE` 절은 **데이터를 추출할 때 조건을 걸러내는 역할**을 합니다.  

---

👉 다음 Q5는 아마 `HAVING` 절과 비교하는 문제일 가능성이 높을 것 같은데, 지금 이 데이터로 `WHERE` vs `HAVING` 차이를 보여드릴까요?

---

### ❓ 질문 (User)
Q5. What is the difference between the VARCHAR and CHAR data types?
A) VARCHAR is fixed length, CHAR is variable length
B) VARCHAR is variable length, CHAR is fixed length
C) VARCHAR stores numbers, CHAR stores characters
D) VARCHAR stores large data, CHAR stores small data

### 💡 답변 (Assistant)
좋습니다 👍 Q5 문제는 **VARCHAR vs CHAR 차이**에 대한 것이네요.  

---

## 📌 Q5. What is the difference between the VARCHAR and CHAR data types?

- **A) VARCHAR is fixed length, CHAR is variable length** → ❌ (반대)  
- **B) VARCHAR is variable length, CHAR is fixed length** → ✅ 정답  
- **C) VARCHAR stores numbers, CHAR stores characters** → ❌ (둘 다 문자형 저장 가능)  
- **D) VARCHAR stores large data, CHAR stores small data** → ❌ (데이터 크기 구분 아님)  

---

## ✅ 정답  
👉 **B) VARCHAR is variable length, CHAR is fixed length**

---

## 🔎 상세 설명
- **CHAR(n)**  
  - **고정 길이 문자형**  
  - 항상 n 바이트를 차지합니다.  
  - 예: `CHAR(10)`이면 `'SQL'`을 저장해도 `'SQL       '`(뒤에 공백)처럼 10자리를 채움.  
  - 장점: 데이터 길이가 일정 → 검색 속도가 빠름.  
  - 단점: 공간 낭비가 발생할 수 있음.  

- **VARCHAR(n)**  
  - **가변 길이 문자형**  
  - 실제 입력된 문자열 길이에 따라 저장 공간이 달라짐.  
  - 예: `VARCHAR(10)`에 `'SQL'` 저장 → 3바이트만 차지.  
  - 장점: 저장공간 절약.  
  - 단점: 데이터 길이가 달라서 성능상 약간의 부하 발생 가능.  

---

## 예시

```sql
CREATE TABLE Example (
    col1 CHAR(5),
    col2 VARCHAR(5)
);

INSERT INTO Example VALUES ('Hi', 'Hi');
```

- `col1` → `'Hi   '` (길이 5로 맞춰짐)  
- `col2` → `'Hi'` (길이 2만 저장됨)  

---

👉 Q6로 넘어가면 `PRIMARY KEY vs FOREIGN KEY` 같은 제약조건 문제일 확률이 높은데, 그 부분도 예시 데이터와 함께 설명해드릴까요?

---

### ❓ 질문 (User)
Q6. Choose the incorrect explanation about JOIN.
A) RIGHT JOIN returns all data from the right table, with unmatched data from the left
table displayed as NULL.
B) FULL OUTER JOIN returns all data from both tables, with unmatched data displayed
as NULL.
C) RIGHT JOIN returns all data from the right table, yielding the same results as LEFT
JOIN.
D) LEFT JOIN returns all data from one table and matching data, while FULL OUTER
JOIN returns all data from both tables.

### 💡 답변 (Assistant)
좋습니다 👍 Q6 문제는 **JOIN 설명 중 틀린 것**을 찾는 문제네요.  

---

## 📌 각 선택지 검토

**A) RIGHT JOIN**  
> "오른쪽 테이블의 모든 데이터를 반환하고, 매칭되지 않는 왼쪽 테이블 데이터는 NULL로 표시한다."  
→ ✅ 올바른 설명입니다.  

**B) FULL OUTER JOIN**  
> "양쪽 테이블의 모든 데이터를 반환하고, 매칭되지 않는 데이터는 NULL로 표시한다."  
→ ✅ 올바른 설명입니다.  

**C) RIGHT JOIN returns all data from the right table, yielding the same results as LEFT JOIN.**  
→ ❌ 틀린 설명입니다.  
- RIGHT JOIN과 LEFT JOIN은 대칭적인 개념이지만, 같은 결과가 나오지는 않습니다.  
- 어느 테이블을 기준으로 "모든 행을 보존"할지 달라지므로, 결과가 달라질 수 있습니다.  

**D) LEFT JOIN**  
> "LEFT JOIN은 한쪽 테이블의 모든 데이터와 매칭되는 데이터를 반환하고, FULL OUTER JOIN은 양쪽 모든 데이터를 반환한다."  
→ ✅ 올바른 설명입니다.  

---

## ✅ 정답
👉 **C) RIGHT JOIN returns all data from the right table, yielding the same results as LEFT JOIN.**

---

## 🔎 간단 예시 (실제 Customer & Order_Test 데이터 기반)

```sql
-- LEFT JOIN
SELECT c.Name, o.OrderID
FROM Customer c
LEFT JOIN Order_Test o ON c.CustomerID = o.CustomerID;

-- RIGHT JOIN
SELECT c.Name, o.OrderID
FROM Customer c
RIGHT JOIN Order_Test o ON c.CustomerID = o.CustomerID;
```

- **LEFT JOIN**: 고객(Customer)을 기준으로 → 모든 고객이 나오고, 주문 없는 고객은 `NULL`  
- **RIGHT JOIN**: 주문(Order_Test)을 기준으로 → 모든 주문이 나오고, 고객이 없으면 `NULL`  

👉 따라서 LEFT JOIN과 RIGHT JOIN은 **결과가 다를 수 있다**는 게 핵심입니다.  

---

원하시면 Q7에서 `INNER JOIN`과 `OUTER JOIN` 차이를 도식으로 정리해 드릴까요?

---

### ❓ 질문 (User)
Q7. Explain the roles of PRIMARY KEY and FOREIGN KEY in SQL.
A) PRIMARY KEY allows duplicates, FOREIGN KEY does not allow duplicates.
B) PRIMARY KEY uniquely identifies a table, FOREIGN KEY references another table.
C) PRIMARY KEY specifies the table name, FOREIGN KEY specifies the data type.
D) PRIMARY KEY and FOREIGN KEY cannot be used in the same table.

### 💡 답변 (Assistant)
좋습니다 👍 Q7은 **PRIMARY KEY와 FOREIGN KEY의 역할**에 관한 문제네요.  

---

## 📌 각 선택지 검토  

**A) PRIMARY KEY allows duplicates, FOREIGN KEY does not allow duplicates.**  
- ❌ 잘못된 설명.  
- PRIMARY KEY는 **중복 불가, NULL 불가**가 원칙입니다.  
- FOREIGN KEY는 참조 제약 조건일 뿐, 값 중복을 허용할 수 있습니다(예: 여러 주문이 같은 고객을 참조).  

**B) PRIMARY KEY uniquely identifies a table, FOREIGN KEY references another table.**  
- ✅ 맞는 설명.  
- PRIMARY KEY → 해당 테이블의 각 행을 고유하게 식별.  
- FOREIGN KEY → 다른 테이블의 PRIMARY KEY를 참조하여 **관계(relationship)**를 정의.  

**C) PRIMARY KEY specifies the table name, FOREIGN KEY specifies the data type.**  
- ❌ 잘못된 설명.  
- 테이블명/데이터 타입과는 전혀 관계 없음.  

**D) PRIMARY KEY and FOREIGN KEY cannot be used in the same table.**  
- ❌ 잘못된 설명.  
- 동일한 테이블 안에서도 사용할 수 있습니다. (예: `Employee` 테이블에서 `EmployeeID`는 PRIMARY KEY이고, `ManagerID`는 같은 테이블의 `EmployeeID`를 참조하는 FOREIGN KEY).  

---

## ✅ 정답  
👉 **B) PRIMARY KEY uniquely identifies a table, FOREIGN KEY references another table.**

---

## 🔎 예시 (Customer & Order_Test 테이블)

```sql
CREATE TABLE Customer (
  CustomerID INT PRIMARY KEY,  -- PRIMARY KEY (고유 식별자)
  Name VARCHAR(50)
);

CREATE TABLE Order_Test (
  OrderID VARCHAR(10) PRIMARY KEY,
  CustomerID INT,
  OrderDate DATE,
  FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)  -- FOREIGN KEY (다른 테이블 참조)
);
```

- **Customer.CustomerID** → PRIMARY KEY (고객을 고유하게 식별)  
- **Order_Test.CustomerID** → FOREIGN KEY (주문이 어느 고객 것인지 연결)  

---

👉 다음 Q8은 보통 **INDEX**나 **UNIQUE KEY** 관련 개념 문제일 가능성이 높습니다. 제가 이어서 준비해드릴까요?

---

### ❓ 질문 (User)
Q8. What is the role of the DISTINCT keyword in SQL?
A) Sort data in descending order
B) Insert new data
C) Merge tables
D) Remove duplicate data

### 💡 답변 (Assistant)
좋습니다 👍 Q8은 **DISTINCT 키워드**의 역할에 대한 문제네요.  

---

## 📌 각 선택지 검토  

**A) Sort data in descending order**  
- ❌ 정렬은 `ORDER BY ... DESC` 로 합니다.  

**B) Insert new data**  
- ❌ 새로운 데이터 입력은 `INSERT` 문으로 합니다.  

**C) Merge tables**  
- ❌ 테이블 병합은 `JOIN`이나 `UNION`으로 합니다.  

**D) Remove duplicate data**  
- ✅ 맞습니다!  
- `DISTINCT`는 SELECT 결과에서 **중복된 행을 제거**합니다.  

---

## ✅ 정답  
👉 **D) Remove duplicate data**

---

## 🔎 예시 (실제 데이터 기반)

```sql
-- 중복된 CustomerID가 있을 경우
SELECT CustomerID
FROM Order_Test;

-- 결과 예시 (중복 있음)
CustomerID
----------
101
101
101
102
102
103
103
104
...

-- DISTINCT 적용
SELECT DISTINCT CustomerID
FROM Order_Test;

-- 결과 (중복 제거)
CustomerID
----------
101
102
103
104
```

---

즉, `DISTINCT`는 **중복된 값을 제거해서 유일한 값만 남긴다**는 게 핵심입니다.  

👉 다음 Q9는 아마 **INDEX**나 `UNION vs UNION ALL` 같은 최적화/집합 연산 문제일 가능성이 있는데, 그 부분도 같이 정리해드릴까요?

---

### ❓ 질문 (User)
Q9. What does a NULL value mean in SQL, and which keyword is used to compare
NULL values?
A) Indicates that data exists, NOT NULL
B) Represents absence of data, IS NULL
C) Indicates that data has been modified, UPDATE NULL
D) Signifies data duplication, CHECK NULL

### 💡 답변 (Assistant)
좋습니다 👍 Q9는 **SQL에서 NULL의 의미와 비교 키워드**에 대한 문제네요.  

---

## 📌 각 선택지 검토  

**A) Indicates that data exists, NOT NULL**  
- ❌ `NOT NULL`은 제약 조건으로, 해당 컬럼이 절대 NULL을 가질 수 없음을 의미.  
- NULL의 의미 설명으로는 틀림.  

**B) Represents absence of data, IS NULL**  
- ✅ 정답!  
- `NULL`은 **데이터가 없음을 의미(unknown, missing, not applicable)**.  
- 비교할 때는 `=` 나 `!=` 이 아닌 `IS NULL`, `IS NOT NULL`을 사용해야 함.  

**C) Indicates that data has been modified, UPDATE NULL**  
- ❌ `UPDATE`문은 데이터 변경용. `UPDATE NULL` 같은 구문은 없음.  

**D) Signifies data duplication, CHECK NULL**  
- ❌ `NULL`은 중복과 관계없음. `CHECK` 제약 조건은 조건 검증용.  

---

## ✅ 정답  
👉 **B) Represents absence of data, IS NULL**

---

## 🔎 예시 (실제 데이터 활용)

```sql
-- 주문 중 CustomerID가 없는 경우 찾기
SELECT OrderID
FROM Order_Test
WHERE CustomerID IS NULL;

-- 주문 중 CustomerID가 존재하는 경우만
SELECT OrderID
FROM Order_Test
WHERE CustomerID IS NOT NULL;
```

---

💡 **중요 포인트**  
- `NULL`은 0, 공백(`''`), `'NULL'` 문자열과 다릅니다.  
- 연산 불가: `=`, `<`, `>` 비교 불가. 반드시 `IS NULL` / `IS NOT NULL`을 써야 합니다.  

---

👉 Q10은 보통 **INDEX 역할**이나 **UNION vs UNION ALL 차이** 같은 최적화 관련 문제가 나올 가능성이 높은데, 이어서 정리해드릴까요?

---

### ❓ 질문 (User)
Q10. When is the HAVING clause used?
A) To delete data that meets a condition
B) To group data based on a specific column
C) To apply conditions to grouped data
D) To insert data into a table

### 💡 답변 (Assistant)
좋습니다 👍 Q10은 **HAVING 절의 사용 목적**에 관한 문제네요.  

---

## 📌 각 선택지 검토  

**A) To delete data that meets a condition**  
- ❌ 데이터 삭제는 `DELETE ... WHERE` 로 합니다.  

**B) To group data based on a specific column**  
- ❌ 그룹화는 `GROUP BY` 절의 역할입니다.  

**C) To apply conditions to grouped data**  
- ✅ 정답!  
- `HAVING` 은 **집계 결과(그룹화된 데이터)에 조건을 적용**할 때 사용합니다.  
- 반면 `WHERE` 은 **행 단위 조건 필터링**입니다.  

**D) To insert data into a table**  
- ❌ 데이터 삽입은 `INSERT INTO ... VALUES(...)` 구문으로 합니다.  

---

## ✅ 정답  
👉 **C) To apply conditions to grouped data**

---

## 🔎 예시 (Customer & Order_Test 데이터 기반)

### 1. 고객별 주문 개수 구하기
```sql
SELECT CustomerID, COUNT(*) AS OrderCount
FROM Order_Test
GROUP BY CustomerID;
```

### 2. 주문이 3건 이상인 고객만 필터링 (`HAVING`)
```sql
SELECT CustomerID, COUNT(*) AS OrderCount
FROM Order_Test
GROUP BY CustomerID
HAVING COUNT(*) >= 3;
```

---

## 📊 결과 (실제 데이터)
| CustomerID | OrderCount |
|------------|------------|
| 101        | 6 |
| 102        | 3 |
| 103        | 3 |
| 104        | 3 |

👉 `HAVING COUNT(*) >= 3` 조건에 따라 모든 고객이 남지만, 만약 `>= 4`라면 James(101)만 남습니다.  

---

💡 정리:  
- **WHERE**: 그룹화 이전, 행 단위 조건 필터링  
- **HAVING**: 그룹화 이후, 집계 결과 필터링  

---

혹시 원하시면 Q1~Q10 전체를 **하나의 요약집(문제+정답+핵심 설명)** 형태로 정리해드릴까요?

---

### ❓ 질문 (User)
지금부터 1~10번을 실습할 수 있게 데이터를 만들어주고 쿼리를 짜줘. 
MySQL 실습환경도 좋지만 BIgQuery 에서 실습해보고 싶어.

### 💡 답변 (Assistant)
좋아요! BigQuery에서 1~10번을 그대로 실습할 수 있게 **데이터셋/테이블 생성 → 데이터 입력 → 각 문항별 쿼리**를 한 번에 드릴게요.  
(아래 스크립트는 **BigQuery Standard SQL** 기준입니다. 필요하면 `project-id`만 본인 프로젝트로 바꿔주세요.)

---

# 0) 실습 환경 만들기 (데이터셋/테이블/데이터)

```sql
-- (선택) 본인 프로젝트/리전에 데이터셋 생성
-- 프로젝트 ID를 바꾸고 싶다면 `your-project-id`로 교체
CREATE SCHEMA IF NOT EXISTS `your-project-id.sql_lab`;

-- 고객 테이블
CREATE OR REPLACE TABLE `your-project-id.sql_lab.Customer` (
  CustomerID INT64,
  Name STRING
);

-- 주문 테이블
CREATE OR REPLACE TABLE `your-project-id.sql_lab.Order_Test` (
  OrderID STRING,
  CustomerID INT64,
  OrderDate DATE
);

-- 고객 데이터
INSERT INTO `your-project-id.sql_lab.Customer` (CustomerID, Name) VALUES
  (101, 'James'),
  (102, 'Alex'),
  (103, 'Kate'),
  (104, 'Rose');

-- 주문 데이터 (Q1~Q3 결과가 일치하도록 구성)
INSERT INTO `your-project-id.sql_lab.Order_Test` (OrderID, CustomerID, OrderDate) VALUES
  ('a-001', 101, DATE '2023-01-24'),
  ('a-002', 101, DATE '2023-01-24'),
  ('a-003', 101, DATE '2024-01-10'),
  ('a-004', 101, DATE '2024-01-12'),
  ('a-005', 101, DATE '2024-01-13'),
  ('a-006', 101, DATE '2024-04-01'),

  ('b-001', 102, DATE '2024-01-15'),
  ('b-002', 102, DATE '2024-01-17'),
  ('b-003', 102, DATE '2024-04-05'),

  ('c-001', 103, DATE '2024-02-15'),
  ('c-002', 103, DATE '2024-02-20'),
  ('c-003', 103, DATE '2024-04-10'),

  ('d-001', 104, DATE '2023-01-12'),
  ('d-002', 104, DATE '2023-03-12'),
  ('d-003', 104, DATE '2023-04-13');

-- (Q9 실습용) NULL 비교 테스트를 위해 CustomerID가 NULL인 주문 1건 추가
-- Q1~Q3에는 영향 없도록 OrderID 접두사를 'x'로 설정
INSERT INTO `your-project-id.sql_lab.Order_Test` (OrderID, CustomerID, OrderDate) VALUES
  ('x-001', NULL, DATE '2024-04-11');
```

> ⚠️ BigQuery에는 MySQL의 `VARCHAR/CHAR` 개념이 없습니다(모두 `STRING`). Q5는 개념 문제이므로 쿼리는 참고 예시로 드립니다.

---

# 1) Q1 – 고객별 주문 수 (COUNT / JOIN / GROUP BY)

```sql
SELECT c.Name, COUNT(o.OrderID) AS OrderCount
FROM `your-project-id.sql_lab.Customer` AS c
JOIN `your-project-id.sql_lab.Order_Test` AS o
  ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.Name
ORDER BY c.Name;
```

---

# 2) Q2 – 2024-01-01 이후 주문만, 최신순 정렬

```sql
SELECT OrderID, CustomerID, OrderDate
FROM `your-project-id.sql_lab.Order_Test`
WHERE OrderDate >= DATE '2024-01-01'
ORDER BY OrderDate DESC;
```

---

# 3) Q3 – OrderID가 a/b로 시작 & 최신순 Top 5

```sql
SELECT *
FROM `your-project-id.sql_lab.Order_Test`
WHERE OrderID LIKE 'a%' OR OrderID LIKE 'b%'
ORDER BY OrderDate DESC
LIMIT 5;
```

---

# 4) Q4 – WHERE의 역할(행 필터링) 예시

```sql
-- James(101)의 주문만 조회 (행 단위 필터)
SELECT *
FROM `your-project-id.sql_lab.Order_Test`
WHERE CustomerID = 101
ORDER BY OrderDate;
```

---

# 5) Q5 – VARCHAR vs CHAR (BigQuery 참고)

> BigQuery는 `STRING` 타입만 사용(고정/가변 길이 구분 없음).  
> 고정 길이처럼 보이게 하려면 `LPAD/RPAD`로 패딩하여 **표현만** 흉내낼 수 있습니다.

```sql
-- 고정 길이 5처럼 보이게 오른쪽 패딩
SELECT
  Name,
  RPAD(Name, 5, ' ') AS AsFixedLike
FROM `your-project-id.sql_lab.Customer`;
```

---

# 6) Q6 – JOIN 차이 (LEFT / RIGHT / FULL OUTER)

```sql
-- LEFT JOIN: 왼쪽(고객) 전체 + 매칭된 주문
SELECT c.Name, o.OrderID, o.OrderDate
FROM `your-project-id.sql_lab.Customer` c
LEFT JOIN `your-project-id.sql_lab.Order_Test` o
  ON c.CustomerID = o.CustomerID
ORDER BY c.Name, o.OrderDate;

-- RIGHT JOIN: 오른쪽(주문) 전체 + 매칭된 고객
SELECT c.Name, o.OrderID, o.OrderDate
FROM `your-project-id.sql_lab.Customer` c
RIGHT JOIN `your-project-id.sql_lab.Order_Test` o
  ON c.CustomerID = o.CustomerID
ORDER BY o.OrderDate;

-- FULL OUTER JOIN: 양쪽 전체 + 매칭 (BigQuery 지원)
SELECT c.Name, o.OrderID, o.OrderDate
FROM `your-project-id.sql_lab.Customer` c
FULL OUTER JOIN `your-project-id.sql_lab.Order_Test` o
  ON c.CustomerID = o.CustomerID
ORDER BY o.OrderDate, c.Name;
```

---

# 7) Q7 – PRIMARY KEY & FOREIGN KEY (개념, BigQuery 주의)

> BigQuery는 전통적인 **PK/FK 제약을 강제하지 않습니다**(논리적으로 관리).  
> 스키마 문서화 차원에서 설명용 주석만 두고, 쿼리는 일반 조인으로 관계를 사용합니다.

```sql
-- 관계 사용 예시(논리적 PK: Customer.CustomerID, FK: Order_Test.CustomerID)
SELECT c.CustomerID, c.Name, COUNT(o.OrderID) AS Orders
FROM `your-project-id.sql_lab.Customer` c
LEFT JOIN `your-project-id.sql_lab.Order_Test` o
  ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.Name
ORDER BY Orders DESC;
```

---

# 8) Q8 – DISTINCT (중복 제거)

```sql
-- 주문에 등장한 고객ID(중복 제거)
SELECT DISTINCT CustomerID
FROM `your-project-id.sql_lab.Order_Test`
ORDER BY CustomerID;
```

---

# 9) Q9 – NULL의 의미 & 비교 (IS NULL / IS NOT NULL)

```sql
-- CustomerID가 NULL인 주문
SELECT OrderID, CustomerID, OrderDate
FROM `your-project-id.sql_lab.Order_Test`
WHERE CustomerID IS NULL;

-- CustomerID가 존재하는 주문
SELECT OrderID, CustomerID, OrderDate
FROM `your-project-id.sql_lab.Order_Test`
WHERE CustomerID IS NOT NULL
ORDER BY OrderDate DESC;
```

---

# 10) Q10 – HAVING (그룹 결과에 조건)

```sql
-- 고객별 주문 수
SELECT CustomerID, COUNT(*) AS OrderCount
FROM `your-project-id.sql_lab.Order_Test`
GROUP BY CustomerID
HAVING COUNT(*) >= 3   -- 집계 결과(그룹)에 대한 조건
ORDER BY OrderCount DESC;
```

---

원하시면 위 스크립트를 **MySQL 호환 버전**으로도 정리해 드리거나, BigQuery용 **Notebook(Colab + bq CLI) 실행 가이드**도 만들어 드릴게요.

---

### ❓ 질문 (User)
MySQL 환경 기준으로도 작성해줘.

### 💡 답변 (Assistant)
좋습니다! 같은 실습을 **MySQL** 기준으로 바로 돌릴 수 있게
1) 스키마/테이블 생성 + 데이터 적재  
2) 1~10번 문제별 쿼리  
를 한 번에 정리해 드릴게요.

---

# 0) 실습 환경 만들기 (MySQL)

```sql
-- (선택) 새 DB
CREATE DATABASE IF NOT EXISTS sql_lab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sql_lab;

-- 기존 테이블이 있다면 정리
DROP TABLE IF EXISTS Order_Test;
DROP TABLE IF EXISTS Customer;

-- 고객 테이블 (PK)
CREATE TABLE Customer (
  CustomerID INT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 주문 테이블 (PK, FK)
CREATE TABLE Order_Test (
  OrderID VARCHAR(20) PRIMARY KEY,
  CustomerID INT NULL,
  OrderDate DATE NOT NULL,
  CONSTRAINT fk_order_customer
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

-- 고객 데이터
INSERT INTO Customer (CustomerID, Name) VALUES
(101, 'James'),
(102, 'Alex'),
(103, 'Kate'),
(104, 'Rose');

-- 주문 데이터
INSERT INTO Order_Test (OrderID, CustomerID, OrderDate) VALUES
('a-001', 101, '2023-01-24'),
('a-002', 101, '2023-01-24'),
('a-003', 101, '2024-01-10'),
('a-004', 101, '2024-01-12'),
('a-005', 101, '2024-01-13'),
('a-006', 101, '2024-04-01'),

('b-001', 102, '2024-01-15'),
('b-002', 102, '2024-01-17'),
('b-003', 102, '2024-04-05'),

('c-001', 103, '2024-02-15'),
('c-002', 103, '2024-02-20'),
('c-003', 103, '2024-04-10'),

('d-001', 104, '2023-01-12'),
('d-002', 104, '2023-03-12'),
('d-003', 104, '2023-04-13');

-- Q9 실습용: CustomerID 가 NULL 인 주문 1건
INSERT INTO Order_Test (OrderID, CustomerID, OrderDate) VALUES
('x-001', NULL, '2024-04-11');
```

---

# 1) Q1 – 고객별 주문 수 (COUNT / JOIN / GROUP BY)

```sql
SELECT c.Name, COUNT(o.OrderID) AS OrderCount
FROM Customer AS c
JOIN Order_Test AS o
  ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.Name
ORDER BY c.Name;
```

---

# 2) Q2 – 2024-01-01 이후 주문만, 최신순 정렬

```sql
SELECT OrderID, CustomerID, OrderDate
FROM Order_Test
WHERE OrderDate >= '2024-01-01'
ORDER BY OrderDate DESC;
```

---

# 3) Q3 – OrderID 가 a/b 시작 & 최신순 Top 5

```sql
SELECT *
FROM Order_Test
WHERE OrderID LIKE 'a%' OR OrderID LIKE 'b%'
ORDER BY OrderDate DESC
LIMIT 5;
```

---

# 4) Q4 – WHERE 의 역할(행 필터링) 예시

```sql
-- James(101)의 주문만
SELECT *
FROM Order_Test
WHERE CustomerID = 101
ORDER BY OrderDate;
```

---

# 5) Q5 – VARCHAR vs CHAR (MySQL에서의 차이 확인)

```sql
-- 예시 전용 테이블
DROP TABLE IF EXISTS TypeDemo;
CREATE TABLE TypeDemo (
  col_char  CHAR(5),
  col_varch VARCHAR(5)
);

INSERT INTO TypeDemo VALUES ('Hi', 'Hi');

-- 길이/표현 차이 확인
SELECT
  CONCAT('|', col_char,  '|') AS show_char,
  CONCAT('|', col_varch, '|') AS show_varchar,
  LENGTH(col_char)   AS len_char_bytes,
  LENGTH(col_varch)  AS len_varch_bytes,
  CHAR_LENGTH(col_char)  AS charlen_char,
  CHAR_LENGTH(col_varch) AS charlen_varch
FROM TypeDemo;

-- 가독성용 패딩(표현): CHAR 처럼 보이게
SELECT
  RPAD(col_varch, 5, ' ') AS varchar_padded_like_char
FROM TypeDemo;
```

> 요점  
> - `CHAR(n)`은 **고정 길이**(공간 패딩), `VARCHAR(n)`는 **가변 길이**.  
> - 비교 시 CHAR의 **후행 공백은 무시**되는 동작이 있음(저장/비교 규칙 차이).  
> - 실제 길이는 `LENGTH/CHAR_LENGTH`로 비교해 보세요.

---

# 6) Q6 – JOIN 차이 (LEFT / RIGHT / FULL OUTER)

```sql
-- LEFT JOIN: 왼쪽(Customer) 전체 + 매칭된 주문
SELECT c.Name, o.OrderID, o.OrderDate
FROM Customer c
LEFT JOIN Order_Test o
  ON c.CustomerID = o.CustomerID
ORDER BY c.Name, o.OrderDate;

-- RIGHT JOIN: 오른쪽(Order_Test) 전체 + 매칭된 고객
SELECT c.Name, o.OrderID, o.OrderDate
FROM Customer c
RIGHT JOIN Order_Test o
  ON c.CustomerID = o.CustomerID
ORDER BY o.OrderDate;

-- MySQL 은 FULL OUTER JOIN 미지원 → UNION 으로 에뮬레이션
SELECT c.Name, o.OrderID, o.OrderDate
FROM Customer c
LEFT JOIN Order_Test o
  ON c.CustomerID = o.CustomerID
UNION
SELECT c.Name, o.OrderID, o.OrderDate
FROM Customer c
RIGHT JOIN Order_Test o
  ON c.CustomerID = o.CustomerID
ORDER BY OrderDate, Name;
```

---

# 7) Q7 – PRIMARY KEY & FOREIGN KEY (제약 포함 예시)

```sql
-- 이미 PK/FK 로 생성했지만, 관계 사용 예시
SELECT c.CustomerID, c.Name, COUNT(o.OrderID) AS Orders
FROM Customer c
LEFT JOIN Order_Test o
  ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.Name
ORDER BY Orders DESC;
```

---

# 8) Q8 – DISTINCT (중복 제거)

```sql
SELECT DISTINCT CustomerID
FROM Order_Test
ORDER BY CustomerID;
```

---

# 9) Q9 – NULL 의미 & 비교 (IS NULL / IS NOT NULL)

```sql
-- CustomerID 가 NULL 인 주문
SELECT OrderID, CustomerID, OrderDate
FROM Order_Test
WHERE CustomerID IS NULL;

-- CustomerID 가 존재하는 주문
SELECT OrderID, CustomerID, OrderDate
FROM Order_Test
WHERE CustomerID IS NOT NULL
ORDER BY OrderDate DESC;
```

---

# 10) Q10 – HAVING (그룹 결과에 조건)

```sql
-- 고객별 주문 수 중 3건 이상
SELECT CustomerID, COUNT(*) AS OrderCount
FROM Order_Test
GROUP BY CustomerID
HAVING COUNT(*) >= 3
ORDER BY OrderCount DESC;
```

---

필요하시면 위 스크립트를 **.sql 파일**로 패키징하거나, Docker(MySQL)용 `docker run` 명령과 함께 초기화 스크립트까지 만들어드릴게요.

---
