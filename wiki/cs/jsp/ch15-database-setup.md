---
type: Concept
title: "Ch15. 데이터베이스 개발 환경 구축 (Database Setup)"
description: "MySQL/MariaDB 설치, 데이터베이스 및 사용자 계정 생성, 권한 부여와 테이블 DDL 구성을 다룹니다."
tags: [jsp, database, mysql, mariadb, ddl, sql-setup]
timestamp: 2026-08-19
status: active
---

# Summary
웹 애플리케이션의 영속적(Persistent) 데이터 저장을 위해 관계형 데이터베이스(RDBMS, MySQL/MariaDB)를 설치하고 전용 데이터베이스 인스턴스, 사용자 계정, 접근 권한 및 테이블 스키마를 구성하는 개발 환경 구축 단계이다.

---

# Key Ideas

## 1. DB 계정 및 권한 생성 SQL
```sql
-- 1. 데이터베이스 생성
CREATE DATABASE jspbookdb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 전용 사용자 생성 및 비밀번호 지정
CREATE USER 'jspuser'@'localhost' IDENTIFIED BY 'jsppass';
CREATE USER 'jspuser'@'%' IDENTIFIED BY 'jsppass';

-- 3. 모든 권한 부여 및 반영
GRANT ALL PRIVILEGES ON jspbookdb.* TO 'jspuser'@'localhost';
GRANT ALL PRIVILEGES ON jspbookdb.* TO 'jspuser'@'%';
FLUSH PRIVILEGES;
```

## 2. 회원 및 상품 테이블 스키마 (DDL)
```sql
USE jspbookdb;

-- 회원 테이블
CREATE TABLE member (
    id VARCHAR(20) NOT NULL PRIMARY KEY,
    passwd VARCHAR(100) NOT NULL,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(50),
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 상품 테이블
CREATE TABLE product (
    p_id VARCHAR(10) NOT NULL PRIMARY KEY,
    p_name VARCHAR(50) NOT NULL,
    p_unitPrice INT NOT NULL,
    p_description TEXT,
    p_category VARCHAR(20),
    p_unitsInStock BIGINT,
    p_condition VARCHAR(20),
    p_fileName VARCHAR(50)
);
```

---

# Related Concepts
- [Ch16. JDBC 데이터베이스 연동](ch16-jdbc-database.md) - 구축된 DB와 자바/JSP 연동

---

# Citations
- `raw/notes/JSP/Ch15 데이터베이스 개발 환경 구축.pptx`
