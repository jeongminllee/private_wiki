---
type: Error Note
title: "SQL 데이터 추출 및 조인"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2025-08-24)"
tags: [errors, chatgpt-export]
timestamp: 2025-08-24
status: active
---

# SQL 데이터 추출 및 조인

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-08-24

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
```
# Q4. SQL – Data Extraction and Join

# All data preprocessing must be done strictly using SQL.

# [Goal]
# Create 3 DataFrames through SQL queries.

# [Database]
# Use the classicmodels database
# Follow below steps to set up 'classicmodels' database
# 1. Insert "mysqlsampledatabase.sql" query into your MySQLWorkbench (File Provided)

# [Tables]
# orders, orderdetails

# [Steps]
# connect the classicmodels database using mysql.connector

# (1) Display the orders DataFrame
# Load all columns from the orders table into a DataFrame.
# Display data information (as shown in the cell output).
# Show the top 5 rows of the DataFrame.


# (2) Display the orderdetails DataFrame
# Load all columns from the orderdetails table into a DataFrame.
# Display data information (as shown in the cell output).
# Show the top 5 rows of the DataFrame.

# (3) Create a joined DataFrame of orders and orderdetails
# Join all columns from orders and orderdetails into a new DataFrame.
# Join condition: orderNumber
# Perform the data extraction and join only using SQL queries (not Pandas merging).
# Display data information (as shown in the cell output).
# Show the top 5 rows of the DataFrame.

import warnings
warnings.filterwarnings('ignore')

%pip install mysql-connector-python
```

이 SQL 데이터베이스를 파이썬 주피터 노트북으로 접근하려고 해. 다음 코드셀의 코드를 보고 코드에서 원하는 코드를 만들어줘.

### 💡 답변 (Assistant)
좋아요! 아래 셀을 그대로 주피터 노트북에 붙여 넣으면 `mysql.connector`로 MySQL에 접속해서 **(1) orders**, **(2) orderdetails**, **(3) SQL만으로 조인한 테이블**을 각각 DataFrame으로 가져오고, 정보/상위 5행/shape 를 출력합니다.  
(먼저 MySQL Workbench에서 `mysqlsampledatabase.sql`을 실행해 `classicmodels` 스키마와 데이터를 만들어 두세요. fileciteturn0file0)

```python
# ------------------------------------------------------------
# Classicmodels: orders / orderdetails 추출 + SQL-Join DataFrame
# 요구사항: pandas 병합 금지, SQL로만 조인
# ------------------------------------------------------------
import pandas as pd
import mysql.connector
from IPython.display import display

# 보기 옵션(원한다면 수정)
pd.set_option("display.max_rows", 20)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)

# ✅ 본인 환경에 맞게 접속 정보 수정
config = {
    "host": "localhost",      # 또는 127.0.0.1, RDS/Cloud면 해당 엔드포인트
    "port": 3306,
    "user": "root",           # 사용자명
    "password": "YOUR_PASSWORD",  # 비밀번호
    "database": "classicmodels",  # mysqlsampledatabase.sql로 생성됨
    "autocommit": True,
}

def show_df(df, title):
    print("=" * 70)
    print(f"( {title} )")
    print("=" * 70)
    # 데이터 정보
    print("\n[Data info]")
    buf = []
    df.info(buf=buf)
    print("\n".join(str(x) for x in buf))
    # 상위 5행
    print("\n[Head]")
    display(df.head(5))
    # shape
    print(f"\n{df.shape}\n")

# --- SQL들(모든 전처리는 SQL로만 수행) ---
SQL_ORDERS = """
SELECT
    *
FROM classicmodels.orders
ORDER BY orderNumber;
"""

SQL_ORDERDETAILS = """
SELECT
    *
FROM classicmodels.orderdetails
ORDER BY orderNumber, orderLineNumber;
"""

# 조인: 판다스 merge 금지, SQL에서 처리
# (orders + orderdetails 전 컬럼을 조인. orderNumber 기준)
SQL_JOIN = """
SELECT
    od.*,
    o.*
FROM classicmodels.orderdetails AS od
JOIN classicmodels.orders      AS o
  ON od.orderNumber = o.orderNumber
ORDER BY od.orderNumber, od.orderLineNumber;
"""

# --- 실행 ---
conn = None
try:
    conn = mysql.connector.connect(**config)

    # (1) orders DataFrame
    df_orders = pd.read_sql(SQL_ORDERS, conn)
    show_df(df_orders, "1) orders DataFrame")

    # (2) orderdetails DataFrame
    df_orderdetails = pd.read_sql(SQL_ORDERDETAILS, conn)
    show_df(df_orderdetails, "2) orderdetails DataFrame")

    # (3) SQL로만 조인한 DataFrame
    df_join = pd.read_sql(SQL_JOIN, conn)
    show_df(df_join, "3) Join table of orders and orderdetails DataFrame")

except mysql.connector.Error as e:
    print("MySQL 연결/쿼리 중 오류:", e)
finally:
    if conn is not None and conn.is_connected():
        conn.close()
```

### 메모
- 위 코드는 **판다스 병합을 사용하지 않고** `SELECT ... JOIN ...`으로만 조인을 수행합니다.
- 출력 형식은 스크린샷처럼 **섹션 헤더 → info → head(5) → (rows, cols)** 순서로 보이도록 구성했습니다.
- 포트/유저/비밀번호가 다르면 `config`를 수정하세요.  
- `mysqlsampledatabase.sql`을 먼저 실행하여 `classicmodels` 스키마와 `orders`, `orderdetails` 테이블을 생성/적재해야 합니다. fileciteturn0file0

원하는 형태에서 더 바꿀 부분 있으면 말씀만 주세요!

---

### 💡 답변 (Assistant)
이 에러는 거의 확실히 `df.info(buf=buf)` 때문에 났어요. `buf`에 **리스트**를 넣으면 `info()`가 `write()` 메서드를 호출하려다 실패합니다(버퍼는 `write()`가 있는 파일-like 객체여야 해요). 아래처럼 `io.StringIO()`를 쓰도록 바꾸면 해결됩니다. 또 혹시 노트북 파일명이 `mysql.py`, `pandas.py`처럼 모듈명과 같으면 임포트 충돌로 비슷한 에러가 날 수 있으니 파일명도 확인해 주세요.

아래 셀을 그대로 교체해서 실행하세요.

```python
# ------------------------------------------------------------
# Classicmodels: orders / orderdetails 추출 + SQL-Join (SQL만 사용)
# ------------------------------------------------------------
import io
import pandas as pd
import mysql.connector
from IPython.display import display

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)

# 본인 환경에 맞게 수정
config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "YOUR_PASSWORD",
    "database": "classicmodels",
    "autocommit": True,
}

def show_df(df, title):
    print("=" * 70)
    print(f"({title})")
    print("=" * 70)

    # ✅ info 캡처: StringIO를 버퍼로 사용 (리스트 X)
    print("\n[Data info]")
    s = io.StringIO()
    df.info(buf=s)
    print(s.getvalue())

    print("[Head]")
    display(df.head(5))
    print(f"\n{df.shape}\n")

SQL_ORDERS = """
SELECT *
FROM classicmodels.orders
ORDER BY orderNumber;
"""

SQL_ORDERDETAILS = """
SELECT *
FROM classicmodels.orderdetails
ORDER BY orderNumber, orderLineNumber;
"""

SQL_JOIN = """
SELECT
    od.*,
    o.*
FROM classicmodels.orderdetails AS od
JOIN classicmodels.orders      AS o
  ON od.orderNumber = o.orderNumber
ORDER BY od.orderNumber, od.orderLineNumber;
"""

conn = None
try:
    conn = mysql.connector.connect(**config)

    # (1) orders
    df_orders = pd.read_sql(SQL_ORDERS, conn)
    show_df(df_orders, "1) orders DataFrame")

    # (2) orderdetails
    df_orderdetails = pd.read_sql(SQL_ORDERDETAILS, conn)
    show_df(df_orderdetails, "2) orderdetails DataFrame")

    # (3) SQL로만 조인
    df_join = pd.read_sql(SQL_JOIN, conn)
    show_df(df_join, "3) Join table of orders and orderdetails DataFrame")

except mysql.connector.Error as e:
    print("MySQL 연결/쿼리 오류:", e)
finally:
    if conn is not None and conn.is_connected():
        conn.close()
```

추가 체크리스트
- 노트북/스크립트 파일명이 `mysql.py`, `pandas.py`, `io.py` 같은 모듈명과 겹치지 않는지 확인.
- `mysql-connector-python` 설치 후 커널 재시작.
- `classicmodels` 스키마가 `mysqlsampledatabase.sql`로 미리 생성되어 있는지 확인.

계속 오류가 뜨면 **전체 traceback**의 마지막 몇 줄을 붙여 주세요. 어디서 ‘module is not callable’가 발생하는지 정확히 짚어서 바로 고쳐 드릴게요.

---

### ❓ 질문 (User)
TypeError: 'module' object is not callable
