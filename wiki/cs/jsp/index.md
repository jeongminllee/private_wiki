---
type: Reference
title: "JSP (JavaServer Pages) 및 웹 프로그래밍 대시보드"
description: "JSP 핵심 문법, 내장 객체, 서블릿, MVC 아키텍처, 데이터베이스 연동 및 웹 보안을 포괄하는 지식베이스 인덱스입니다."
tags: [jsp, java, servlet, web, backend, mvc, index]
timestamp: 2026-08-19
status: active
---

# JSP & Web Architecture Study Dashboard

JSP(JavaServer Pages) 및 서블릿 기반 웹 프로그래밍의 기초부터 MVC 패턴, JDBC 데이터베이스 연동, 웹 보안 및 세션 관리에 이르는 전체 개념 학습 대시보드입니다.

---

## 📚 챕터별 지식 문서 목록

### Part 1. JSP 기본 구조와 스크립트 요소
- **[Ch01. JSP 개요 및 웹 아키텍처](ch01-overview.md)** - 웹의 동작 원리, 클라이언트/서버 모델, JSP/서블릿 컨테이너(Tomcat) 라이프사이클 및 변환 과정
- **[Ch02. 스크립트 태그 (Scripting Elements)](ch02-script-elements.md)** - 선언문(`<%! %>`), 스크립틀릿(`<% %>`), 표현식(`<%= %>`)의 자바 서블릿 변환 규칙 및 활용
- **[Ch03. 디렉티브 태그 (Directive Elements)](ch03-directive-elements.md)** - `page`, `include`, `taglib` 디렉티브의 속성과 역할
- **[Ch04. 액션 태그 및 자바빈즈 (Action Tags & JavaBeans)](ch04-action-tags.md)** - `jsp:forward`, `jsp:include`, `jsp:param`, 자바빈즈(`jsp:useBean`, `jsp:setProperty`, `jsp:getProperty`)

### Part 2. HTTP 요청/응답과 상태 관리
- **[Ch05. 내장 객체 및 영역 (Implicit Objects & Scope)](ch05-implicit-objects.md)** - `request`, `response`, `out`, `session`, `application` 등 9대 내장 객체 및 4대 영역(Scope)
- **[Ch06. 폼 태그 및 파라미터 처리 (Form Processing)](ch06-form-processing.md)** - HTML Form 요소, GET/POST 전송 방식 비교 및 요청 파라미터 한글 인코딩 처리
- **[Ch07. 파일 업로드 (File Upload)](ch07-file-upload.md)** - `multipart/form-data`, `MultipartRequest`(cos.jar) 및 Apache Commons-FileUpload를 활용한 멀티파트 파일 업로드
- **[Ch08. 유효성 검사 (Form Validation)](ch08-validation.md)** - 자바스크립트 기반 기본 검증, 정규 표현식(RegExp)을 이용한 데이터 유효성 검사

### Part 3. 보안, 예외 처리 및 컴포넌트 확장
- **[Ch10. 웹 시큐리티 (Web Security)](ch10-security.md)** - 선언적 보안(`web.xml`, 시큐리티 롤/제약조건, FORM 인증) 및 프로그래밍적 보안 API
- **[Ch11. 예외 처리 (Exception Handling)](ch11-exception-handling.md)** - `page` 디렉티브(`errorPage`/`isErrorPage`), `web.xml` 에러 코드 및 예외 타입 매핑
- **[Ch12. 서블릿 필터 (Servlet Filter)](ch12-filter.md)** - `Filter` 인터페이스, 라이프사이클(`init`, `doFilter`, `destroy`), `FilterChain`, 한글 인코딩 필터 구현
- **[Ch13. 세션 기반 상태 관리 (Session Management)](ch13-session.md)** - `HttpSession` 인터페이스, 세션 생성·유지·만료, 장바구니 및 로그인 인증 구현
- **[Ch14. 쿠키 기반 상태 관리 (Cookie Management)](ch14-cookie.md)** - `Cookie` 클래스, 클라이언트 사이드 데이터 저장, 자동 로그인 및 유효기간 설정 (세션과의 비교)

### Part 4. 데이터베이스 연동 및 MVC 아키텍처
- **[Ch15. 데이터베이스 개발 환경 구축 (Database Setup)](ch15-database-setup.md)** - MySQL/MariaDB 설치, 데이터베이스 계정/권한 부여, 테이블 생성 및 환경 설정
- **[Ch16. JDBC 데이터베이스 연동 & 커넥션 풀 (JDBC & DBCP)](ch16-jdbc-database.md)** - `Connection`, `Statement`, `PreparedStatement`, `ResultSet`, DBCP(커넥션 풀)를 활용한 CRUD 구현
- **[Ch17. JSTL & EL (표준 태그 라이브러리 및 표현 언어)](ch17-jstl-el.md)** - 표현 언어(EL) 문법, JSTL Core(`c:if`, `c:forEach`), Formatting(`fmt:`), Functions(`fn:`) 라이브러리
- **[Ch18. 웹 MVC 아키텍처 (Web MVC Architecture)](ch18-web-mvc.md)** - Model 1 vs Model 2 비교, Front Controller 패턴, 서블릿 컨트롤러, Service, DAO, JSP 뷰 레이어 설계

---

## 🔗 관련 문서 및 상위 인덱스
- [CS Study Index](../index.md) - 컴퓨터 과학 핵심 개념 인덱스
- [Java Programming](../java/index.md) - 자바 프로그래밍 핵심 개념
- [Root Wiki Index](../../../index.md) - 전체 지식베이스 루트 인덱스
