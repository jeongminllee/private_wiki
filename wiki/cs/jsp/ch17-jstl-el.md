---
type: Concept
title: "Ch17. JSP 표준 태그 라이브러리(JSTL) 및 표현 언어(EL)"
description: "스크립틀릿을 대체하는 표현 언어(EL)의 문법과 JSTL Core, Formatting, Functions 라이브러리 활용법을 다룹니다."
tags: [jsp, jstl, el, expression-language, jstl-core, fmt]
timestamp: 2026-08-19
status: active
---

# Summary
표현 언어(EL, Expression Language)와 JSP 표준 태그 라이브러리(JSTL, JavaServer Pages Standard Tag Library)는 **JSP 페이지에서 복잡한 스크립틀릿(`<% %>`) 자바 코드를 완전히 제거**하고, HTML과 유사한 XML 태그 및 `${표현식}` 형태로 화면 데이터를 깔끔하게 바인딩할 수 있도록 지원하는 표준 뷰 템플릿 기술이다.

---

# Why it matters
1. **View 계층의 순수성 보장**: 비즈니스 로직이 JSP 뷰 화면에 난립하는 스파게티 코드를 방지하고 가독성을 극대화한다.
2. **NullPointerException 자동 방어**: EL은 null 객체의 프로퍼티를 조회해도 예외를 발생시키지 않고 빈 문자열(`""`)로 안전하게 처리한다.

---

# Key Ideas

## 1. 표현 언어 (EL, `${expr}`)
- 4대 스코프(`pageScope` -> `requestScope` -> `sessionScope` -> `applicationScope`)에 저장된 자바빈즈 프로퍼티를 자동으로 탐색하여 출력한다.
- 자바빈 Getter 자동 호출: `${member.name}` 은 `member.getName()`을 호출한 것과 동일하다.
- 연산자 지원: 산술(`+`, `-`), 비교(`==` 또는 `eq`, `!=` 또는 `ne`), 논리(`&&` 또는 `and`), `empty` 연산자(null 또는 빈 컬렉션 검사).

## 2. JSTL 라이브러리 구성

| 라이브러리 | 접두사 (Prefix) | 디렉티브 선언 URI | 주요 기능 태그 |
| :--- | :---: | :--- | :--- |
| **Core** | `c` | `http://java.sun.com/jsp/jstl/core` | 변수 설정(`c:set`), 조건문(`c:if`, `c:choose/c:when`), 반복문(`c:forEach`), URL 처리(`c:url`) |
| **Formatting** | `fmt` | `http://java.sun.com/jsp/jstl/fmt` | 날짜 포맷팅(`fmt:formatDate`), 숫자/통화 포맷팅(`fmt:formatNumber`), 다국어 지원 |
| **Functions** | `fn` | `http://java.sun.com/jsp/jstl/functions` | 문자열 처리 함수 (`fn:length`, `fn:substring`, `fn:contains`) |

---

# Examples

### JSTL과 EL을 활용한 게시글 목록 렌더링
```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>

<!DOCTYPE html>
<html>
<head><title>Board List with JSTL</title></head>
<body>
    <h3>게시판 목록</h3>

    <!-- 목록이 비어있는 경우 -->
    <c:if test="${empty boardList}">
        <p>등록된 게시글이 없습니다.</p>
    </c:if>

    <!-- 목록 순회 출력 -->
    <table border="1">
        <tr>
            <th>번호</th><th>제목</th><th>작성자</th><th>작성일</th><th>조회수</th>
        </tr>
        <c:forEach var="board" items="${boardList}" varStatus="status">
            <tr>
                <td>${status.count}</td>
                <td><a href="detail.do?id=${board.id}">${board.title}</a></td>
                <td>${board.writer}</td>
                <td><fmt:formatDate value="${board.regDate}" pattern="yyyy-MM-dd" /></td>
                <td><fmt:formatNumber value="${board.readCount}" type="number" /></td>
            </tr>
        </c:forEach>
    </table>
</body>
</html>
```

---

# Related Concepts
- [Ch02. 스크립트 태그](ch02-script-elements.md) - 스크립틀릿 문법과의 비교
- [Ch03. 디렉티브 태그](ch03-directive-elements.md) - `taglib` 선언
- [Ch18. 웹 MVC](ch18-web-mvc.md) - MVC 패턴에서 JSP View를 렌더링하는 표준 기법

---

# Citations
- `raw/notes/JSP/Ch17 JSP 표준 태그 라이브러리.pptx`
