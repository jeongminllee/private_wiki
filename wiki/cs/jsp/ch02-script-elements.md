---
type: Concept
title: "Ch02. 스크립트 태그 (Scripting Elements)"
description: "선언문, 스크립틀릿, 표현식 등 JSP 내에서 자바 코드를 기술하는 핵심 스크립트 요소의 문법과 서블릿 변환 규칙을 다룹니다."
tags: [jsp, scripting-tags, scriptlet, declaration, expression]
timestamp: 2026-08-19
status: active
---

# Summary
JSP 스크립트 태그는 HTML 문서 내에 자바 코드를 직접 기술하기 위해 사용되는 문법 요소이다. **선언문(`<%! %>`)**, **스크립틀릿(`<% %>`)**, **표현식(`<%= %>`)**의 세 가지로 분류되며, 각 태그는 톰캣이 생성하는 서블릿 클래스의 서로 다른 영역(멤버 영역 vs 서비스 메서드 내부)으로 변환된다.

---

# Why it matters
- **자바 문법의 직접 활용**: 반복문, 조건문, 연산, 메서드 호출 등 자바 언어의 모든 제어 구조를 웹 페이지 렌더링에 사용할 수 있다.
- **서블릿 변환 메커니즘의 이해**: 선언문과 스크립틀릿 변수의 스코프(Scope) 및 스레드 안전성(Thread Safety) 차이를 명확히 파악할 수 있다.

---

# Key Ideas

## 1. 스크립트 태그 3요소 비교

| 구분 | 문법 | 변환되는 자바 서블릿 위치 | 주요 용도 | 스레드 안전성 주의 |
| :--- | :--- | :--- | :--- | :--- |
| **선언문 (Declaration)** | `<%! ... %>` | 서블릿 클래스의 **멤버 변수 및 메서드** | 전역 변수, 유틸리티 메서드 선언 | ⚠️ 모든 요청 스레드가 공유하므로 동기화 이슈 주의 |
| **스크립틀릿 (Scriptlet)** | `<% ... %>` | `_jspService()` **메서드 내부의 지역 코드** | 비즈니스 로직, 반복/조건문, 지역 변수 | 요청마다 별도 스택 프레임 생성 (안전) |
| **표현식 (Expression)** | `<%= ... %>` | `out.print(...)` **출력문** | 연산 결과나 변수 값을 화면에 출력 | 세미콜론(`;`)을 붙이지 않음 |

## 2. 주석 (Comments)의 종류와 차이
- **JSP 주석**: `<%-- 주석 내용 --%>` → 서블릿 변환 시 완전히 제거되어 브라우저 소스 보기에서도 노출되지 않음 (보안상 권장).
- **HTML 주석**: `<!-- 주석 내용 -->` → 브라우저로 그대로 전송되어 '페이지 소스 보기' 시 노출됨.
- **자바 주석**: `// 한 줄 주석`, `/* 여러 줄 주석 */` → 스크립틀릿 내부에서 사용되며 `.java`에는 남지만 HTML에는 미전송.

---

# Examples

### 선언문, 스크립틀릿, 표현식의 종합 예제
```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head><title>Scripting Elements</title></head>
<body>
    <%!
        // 1. 선언문: 멤버 변수 및 메서드
        private int visitCount = 0;
        public int multiply(int a, int b) {
            return a * b;
        }
    %>

    <%
        // 2. 스크립틀릿: _jspService 내부 지역 로직
        visitCount++;
        int valA = 5;
        int valB = 8;
        int result = multiply(valA, valB);
    %>

    <!-- 3. 표현식: 화면 출력 -->
    <h2>스크립팅 태그 결과</h2>
    <p>누적 방문 수: <%= visitCount %></p>
    <p><%= valA %> x <%= valB %> = <%= result %></p>

    <!-- 구구단 출력 루프 예제 -->
    <table border="1">
    <% for (int i = 1; i <= 3; i++) { %>
        <tr>
            <td>2 x <%= i %></td>
            <td><%= 2 * i %></td>
        </tr>
    <% } %>
    </table>
</body>
</html>
```

---

# Related Concepts
- [Ch01. JSP 개요](ch01-overview.md) - JSP의 서블릿 변환 및 생명주기
- [Ch03. 디렉티브 태그](ch03-directive-elements.md) - 페이지 설정 및 import 디렉티브
- [Ch17. JSTL & EL](ch17-jstl-el.md) - 스크립틀릿을 대체하는 최신 표준 태그

---

# Citations
- `raw/notes/JSP/Ch02 스크립트 태그.pptx`
