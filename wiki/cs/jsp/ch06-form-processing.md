---
type: Concept
title: "Ch06. 폼 태그 및 HTTP 요청 파라미터 처리"
description: "HTML Form 요소의 구성, GET과 POST 전송 방식의 특징, JSP에서의 다중 파라미터 수신 및 한글 인코딩 처리를 다룹니다."
tags: [jsp, form, http-method, get, post, request-parameters, encoding]
timestamp: 2026-08-19
status: active
---

# Summary
폼(Form) 태그는 사용자가 웹 브라우저에서 입력한 데이터를 웹 서버로 전송하기 위한 표준 HTML 인터페이스이다. JSP는 `request` 내장 객체의 `getParameter()`, `getParameterValues()` 등의 메서드를 통해 전송된 폼 파라미터를 추출하고 처리한다.

---

# Why it matters
- **사용자 상호작용의 핵심**: 회원가입, 로그인, 게시글 작성, 검색 등 모든 사용자 입력 데이터의 진입점이다.
- **GET vs POST 보안 및 캐싱 특성**: 데이터의 노출 여부, 전송 크기 제한, 멱등성(Idempotency)에 따른 전송 방식 선택 기준을 제공한다.

---

# Key Ideas

## 1. GET 방식 vs POST 방식 비교

| 비교 항목 | GET 방식 | POST 방식 |
| :--- | :--- | :--- |
| **데이터 전달 위치** | URL의 쿼리 스트링(Query String) 뒤에 결합 (`?key=val&...`) | HTTP 요청 바디(Request Body)에 포함되어 전송 |
| **보안성** | URL에 데이터가 노출되므로 패스워드 등 민감 정보 전송 불가 | URL에 노출되지 않아 상대적으로 안전 (HTTPS 결합 필요) |
| **전송 데이터 용량** | 브라우저/서버 URL 길이 제한에 따라 제한적 | 용량 제한이 사실상 없음 (대용량 데이터 및 파일 전송 가능) |
| **캐싱 및 북마크** | 브라우저 히스토리 저장 및 북마크 가능 (조회 연산에 적합) | 캐싱 및 북마크 불가 (서버 상태 변경 연산에 적합) |

## 2. 주요 HTML 폼 컨트롤 태그
- `<input type="text|password|hidden|radio|checkbox|file|submit|reset|button">`
- `<select>` 와 `<option>`: 드롭다운 선택 메뉴
- `<textarea>`: 여러 줄 텍스트 입력

## 3. JSP의 요청 파라미터 수신 메서드 (`HttpServletRequest`)
- `request.getParameter(String name)`: 단일 파라미터 값 추출 (문자열 반환)
- `request.getParameterValues(String name)`: 체크박스 등 동일한 이름으로 전송된 **다중 파라미터 값 추출 (String[] 배열 반환)**
- `request.getParameterNames()`: 전송된 모든 파라미터의 이름 열거 (`Enumeration<String>`)
- `request.getParameterMap()`: 모든 파라미터를 Map 구조로 반환 (`Map<String, String[]>`)

## 4. 한글 인코딩 처리 (한글 깨짐 해결)
- **POST 방식**: 파라미터 추출 **이전에** 반드시 `request.setCharacterEncoding("UTF-8");` 호출 필수.
- **GET 방식**: 톰캣 `server.xml`의 `<Connector URIEncoding="UTF-8" ...>` 설정으로 처리.

---

# Examples

### 1. 입력 폼 (`formInput.jsp`)
```html
<form action="formProcess.jsp" method="POST">
    아이디: <input type="text" name="userId"><br>
    취미:
    <input type="checkbox" name="hobby" value="Sports"> 운동
    <input type="checkbox" name="hobby" value="Music"> 음악
    <input type="checkbox" name="hobby" value="Movie"> 영화<br>
    <input type="submit" value="전송">
</form>
```

### 2. 파라미터 수신 처리 (`formProcess.jsp`)
```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    // POST 한글 인코딩 설정 (반드시 getParameter 전에 실행)
    request.setCharacterEncoding("UTF-8");

    String userId = request.getParameter("userId");
    String[] hobbies = request.getParameterValues("hobby");
%>
<!DOCTYPE html>
<html>
<head><title>Form Result</title></head>
<body>
    <h3>수신된 데이터</h3>
    <p>아이디: <%= userId %></p>
    <p>선택된 취미:</p>
    <ul>
    <%
        if (hobbies != null) {
            for (String h : hobbies) {
                out.println("<li>" + h + "</li>");
            }
        } else {
            out.println("<li>선택된 취미가 없습니다.</li>");
        }
    %>
    </ul>
</body>
</html>
```

---

# Related Concepts
- [Ch05. 내장 객체](ch05-implicit-objects.md) - `request` 내장 객체의 기능
- [Ch07. 파일 업로드](ch07-file-upload.md) - `enctype="multipart/form-data"` 폼 처리
- [Ch08. 유효성 검사](ch08-validation.md) - 폼 전송 전 자바스크립트 데이터 검증

---

# Citations
- `raw/notes/JSP/Ch06 폼 태그.pptx`
