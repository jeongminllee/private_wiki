---
type: Concept
title: "Ch14. 쿠키 기반 클라이언트 상태 저장 (Cookie Management)"
description: "Cookie 객체의 생성, 속성 설정, 클라이언트 전송 및 조회와 세션과의 아키텍처 비교를 설명합니다."
tags: [jsp, cookie, client-storage, session-vs-cookie, max-age]
timestamp: 2026-08-19
status: active
---

# Summary
쿠키(Cookie)는 웹 서버가 클라이언트 브라우저에 전송하여 **클라이언트 로컬 디스크/메모리에 텍스트 파일 형태로 저장되는 작은 데이터 조각(최대 4KB)**이다. 이후 클라이언트가 동일한 서버에 요청을 보낼 때마다 HTTP 요청 헤더(`Cookie`)에 쿠키를 자동으로 동봉하여 전송한다.

---

# Why it matters
- **서버 메모리 부하 절감**: 세션과 달리 상태 데이터를 클라이언트에 분산 저장하므로 서버 자원을 점유하지 않는다.
- **영속적 상태 유지 (Persistent)**: 브라우저가 종료되어도 `setMaxAge()` 유효기간 동안 디스크에 유지되므로 '아이디 기억하기', '팝업 오늘 하루 열지 않기' 등에 적합하다.

---

# Key Ideas

## 1. 쿠키 vs 세션 비교

| 비교 항목 | 쿠키 (Cookie) | 세션 (Session) |
| :--- | :--- | :--- |
| **저장 위치** | 클라이언트 브라우저 (로컬 디스크/메모리) | 웹 서버 메모리 |
| **보안성** | 클라이언트에서 위/변조 가능하므로 취약 | 서버에 저장되므로 상대적으로 안전 |
| **저장 용량** | 도메인당 20개, 쿠키당 4KB로 제한적 | 서버 메모리가 허용하는 한 제한 없음 |
| **수명** | 만료 날짜(`setMaxAge`)까지 브라우저 종료 후도 유지 가능 | 브라우저 종료 또는 세션 타임아웃 시 소멸 |
| **주요 용도** | 아이디 저장, 자동 로그인, 팝업 제어, 방문 통계 | 사용자 인증 로그인 상태, 장바구니, 결제 정보 |

## 2. `Cookie` 클래스 주요 API
- `Cookie cookie = new Cookie(String name, String value)`: 쿠키 객체 생성
- `cookie.setMaxAge(int expiry)`: 쿠키 유효기간 설정 (초 단위, `0` 설정 시 즉시 삭제)
- `cookie.setPath(String uri)`: 쿠키가 전송될 유효 디렉터리 경로 지정
- `response.addCookie(Cookie cookie)`: 응답 헤더에 `Set-Cookie`로 클라이언트에 전송
- `request.getCookies()`: 클라이언트가 전송한 모든 쿠키 배열(`Cookie[]`) 조회

---

# Examples

### 1. 쿠키 생성 및 전송 (`setCookie.jsp`)
```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    // 아이디 저장 쿠키 생성 (7일간 유지)
    Cookie idCookie = new Cookie("savedId", "user123");
    idCookie.setMaxAge(7 * 24 * 60 * 60); // 7일 (초 단위)
    idCookie.setPath("/");
    response.addCookie(idCookie);
%>
<p>쿠키가 설정되었습니다.</p>
```

### 2. 쿠키 읽기 (`getCookie.jsp`)
```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    String savedId = "";
    Cookie[] cookies = request.getCookies();
    if (cookies != null) {
        for (Cookie c : cookies) {
            if ("savedId".equals(c.getName())) {
                savedId = c.getValue();
                break;
            }
        }
    }
%>
<p>저장된 아이디: <%= savedId %></p>
```

---

# Related Concepts
- [Ch05. 내장 객체](ch05-implicit-objects.md) - `request`와 `response`를 통한 쿠키 제어
- [Ch13. 세션](ch13-session.md) - 세션 ID 전송 매개체로서의 쿠키

---

# Citations
- `raw/notes/JSP/Ch14 쿠키.pptx`
