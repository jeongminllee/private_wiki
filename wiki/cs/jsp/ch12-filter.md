---
type: Concept
title: "Ch12. 서블릿 필터 (Servlet Filter)"
description: "Filter 인터페이스의 생명주기, FilterChain 동작 구조 및 공통 한글 인코딩 필터 구현을 분석합니다."
tags: [jsp, servlet, filter, filter-chain, character-encoding, doFilter]
timestamp: 2026-08-19
status: active
---

# Summary
서블릿 필터(Servlet Filter)는 클라이언트의 요청이 서블릿이나 JSP 등의 최종 리소스에 도달하기 **전(Pre-processing)**이나, 서버의 응답이 클라이언트에 전송되기 **직전(Post-processing)**에 HTTP 요청 및 응답 객체를 가로채어 공통 작업(인코딩 변환, 로깅, 인증/인가 검사, 암호화 등)을 수행하는 웹 컴포넌트이다.

---

# Why it matters
1. **횡단 관심사(Cross-Cutting Concerns)의 분리**: 모든 JSP/서블릿마다 중복 작성해야 하는 한글 인코딩(`setCharacterEncoding`), 세션 인증 검사, 요청 로깅 코드를 단일 필터 클래스로 모듈화한다.
2. **필터 체이닝(Filter Chaining)**: 여러 개의 필터를 파이프라인 형태로 연결하여 순차적으로 실행할 수 있다.

---

# Key Ideas

## 1. Filter 인터페이스의 생명주기 (Lifecycle)

```mermaid
flowchart LR
    Client["클라이언트 요청"] --> F1["Filter 1 (전처리)"]
    F1 -->|chain.doFilter()| F2["Filter 2 (전처리)"]
    F2 -->|chain.doFilter()| Target["대상 서블릿 / JSP"]
    Target --> F2_Post["Filter 2 (후처리)"]
    F2_Post --> F1_Post["Filter 1 (후처리)"]
    F1_Post --> ClientResp["클라이언트 응답"]
```

1. `init(FilterConfig filterConfig)`: 컨테이너 시작 시 필터 인스턴스 생성 및 1회 초기화.
2. `doFilter(ServletRequest request, ServletResponse response, FilterChain chain)`: 요청이 들어올 때마다 실행되는 핵심 로직.
   - `chain.doFilter(request, response)`를 호출하여 다음 필터나 최종 서블릿으로 제어권을 넘긴다.
3. `destroy()`: 컨테이너 종료 시 필터 인스턴스 소멸.

---

# Examples

### 한글 인코딩 필터 구현 (`filter/CharacterEncodingFilter.java`)
```java
package filter;

import java.io.IOException;
import javax.servlet.*;

public class CharacterEncodingFilter implements Filter {
    private String encoding;

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        // web.xml의 초기화 파라미터에서 인코딩 값 로딩 (기본값 UTF-8)
        encoding = filterConfig.getInitParameter("encoding");
        if (encoding == null) encoding = "UTF-8";
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        // 1. [전처리]: 요청 데이터 인코딩 설정
        request.setCharacterEncoding(encoding);

        // 2. 다음 필터 또는 서블릿으로 전달
        chain.doFilter(request, response);

        // 3. [후처리]: 필요 시 응답 헤더 조작 등 수행
    }

    @Override
    public void destroy() {}
}
```

### `web.xml` 필터 매핑
```xml
<filter>
    <filter-name>EncodingFilter</filter-name>
    <filter-class>filter.CharacterEncodingFilter</filter-class>
    <init-param>
        <param-name>encoding</param-name>
        <param-value>UTF-8</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>EncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

---

# Related Concepts
- [Ch06. 폼 태그](ch06-form-processing.md) - 인코딩 필터를 통한 `setCharacterEncoding` 자동화
- [Ch10. 시큐리티](ch10-security.md) - 필터 기반 사용자 로그인 검증
- [Ch18. 웹 MVC](ch18-web-mvc.md) - Front Controller 진입 전 필터 파이프라인

---

# Citations
- `raw/notes/JSP/Ch12 필터.pptx`
