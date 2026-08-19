---
type: Concept
title: "Ch04. 액션 태그 및 자바빈즈 (Action Tags & JavaBeans)"
description: "런타임 시 페이지 이동, 파일 동적 포함, 파라미터 전달 및 자바빈즈(DTO/VO) 객체 연동을 처리하는 표준 액션 태그를 다룹니다."
tags: [jsp, action-tags, forward, include, javabeans, useBean]
timestamp: 2026-08-19
status: active
---

# Summary
JSP 액션 태그(Action Tag)는 클라이언트의 요청을 처리할 때 **서버 측에서 특정 동작(페이지 포워딩, 동적 포함, 자바빈 객체 바인딩 등)을 수행하도록 지시하는 XML 형식의 표준 태그**이다. `<jsp:태그명>` 형태를 가지며, 자바빈즈(JavaBeans) 액션 태그를 통해 스크립틀릿 없이도 데이터 모델(DTO)과 화면을 바인딩할 수 있다.

---

# Why it matters
1. **스크립틀릿 코드의 최소화**: 자바 인스턴스 생성 및 Getter/Setter 호출을 XML 태그 형태로 대체하여 가독성을 높인다.
2. **효율적인 웹 페이지 흐름 제어**: `forward`를 통한 서버 내부 페이지 이동과 `include`를 통한 레이아웃 조립을 구현한다.
3. **자바빈즈 규약 확립**: 웹 계층과 비즈니스 데이터 계층 간의 표준 데이터 전송 객체(DTO) 연동 방식을 정립한다.

---

# Key Ideas

## 1. 페이지 흐름 및 제어 액션 태그

```mermaid
flowchart TD
    subgraph ForwardFlow["jsp:forward 동작 원리"]
        C1["클라이언트"] -->|1. 요청| JSP_A["pageA.jsp"]
        JSP_A -->|2. 내부 제어권 위임
(URL 변경 없음)| JSP_B["pageB.jsp"]
        JSP_B -->|3. 최종 응답 전송| C1
    end
```

- `<jsp:forward page="target.jsp" />`:
  - 현재 페이지의 실행을 중단하고 지정된 대상 페이지로 **서버 내부에서 요청을 전달(Forward)**한다.
  - 클라이언트 브라우저의 URL 주소는 변경되지 않는다.
- `<jsp:include page="module.jsp" flush="false" />`:
  - 런타임에 지정된 파일의 실행 결과를 현재 출력 스트림에 삽입한다.
  - 대상 파일이 독립된 서블릿으로 실행된 후 결과만 포함된다.
- `<jsp:param name="key" value="val" />`:
  - `forward`나 `include` 태그의 자식 요소로 파라미터를 추가하여 전달한다.

## 2. 자바빈즈(JavaBeans) 규약
자바빈즈는 데이터를 표현하는 재사용 가능한 자바 클래스(DTO/VO)로 다음 규약을 반드시 만족해야 한다.
1. `java.io.Serializable` 인터페이스 구현 권장.
2. 매개변수가 없는 **기본 생성자(Default Constructor)** 필수.
3. 모든 필드는 `private` 접근 제한자 적용 (정보 은닉).
4. 각 필드에 대해 표준 명명 규칙을 따르는 `getter`/`setter` 메서드 제공.

## 3. 자바빈즈 액션 태그 3총사
- `<jsp:useBean id="빈이름" class="패키지.클래스명" scope="page|request|session|application" />`:
  - 지정된 스코프에서 객체를 조회하고, 없으면 새로 생성하여 바인딩한다.
- `<jsp:setProperty name="빈이름" property="필드명" value="값" />`:
  - `property="*"` 지정 시 요청 파라미터(Request Parameter)와 자바빈 필드명이 일치하는 항목을 **자동 일괄 매핑(Auto-binding)**한다.
- `<jsp:getProperty name="빈이름" property="필드명" />`:
  - 자바빈의 getter 메서드를 호출하여 값을 화면에 출력한다.

---

# Examples

### 자바빈즈 클래스 (`dto/MemberDTO.java`)
```java
package dto;

public class MemberDTO {
    private String id;
    private String name;

    public MemberDTO() {} // 기본 생성자 필수

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
```

### 액션 태그를 이용한 파라미터 자동 바인딩 및 출력 (`memberProcess.jsp`)
```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>

<!-- 1. 자바빈 객체 생성 (request 스코프) -->
<jsp:useBean id="member" class="dto.MemberDTO" scope="request" />

<!-- 2. 요청 파라미터를 DTO 필드에 자동 주입 -->
<jsp:setProperty name="member" property="*" />

<!DOCTYPE html>
<html>
<head><title>Member Info</title></head>
<body>
    <h3>회원 등록 정보</h3>
    <p>아이디: <jsp:getProperty name="member" property="id" /></p>
    <p>이름: <jsp:getProperty name="member" property="name" /></p>

    <!-- 다른 페이지로 포워딩하면서 추가 파라미터 전달 -->
    <jsp:forward page="welcome.jsp">
        <jsp:param name="authLevel" value="user" />
    </jsp:forward>
</body>
</html>
```

---

# Related Concepts
- [Ch03. 디렉티브 태그](ch03-directive-elements.md) - include 디렉티브 vs include 액션 태그 비교
- [Ch05. 내장 객체 및 영역](ch05-implicit-objects.md) - `useBean`의 4대 스코프 영역
- [Ch18. 웹 MVC 아키텍처](ch18-web-mvc.md) - Model 계층으로서의 자바빈즈(DTO)

---

# Citations
- `raw/notes/JSP/Ch04 액션 태그.pptx`
