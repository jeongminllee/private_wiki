---
type: Reference
title: "Hotwire Native로 서버 렌더링 웹을 모바일 앱으로 확장하기"
description: "HTML을 native shell에 표시하고 bridge component와 native screen으로 점진 강화하는 web-first 접근"
resource: https://www.youtube.com/watch?v=yIdzxdLX9Dk
notion: https://app.notion.com/p/d081a73cf20b8282925281f58c75d562
tags: [reading, hotwire-native, mobile, server-rendering]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Hotwire Native는 서버가 render한 HTML을 iOS·Android의 native shell 안에 표시하고, link navigation은 platform의 native stack과 animation으로 처리한다. 하나의 web application을 중심으로 mobile app을 빠르게 만들고 필요한 부분만 Swift·Kotlin으로 강화하는 방식이다.

# 동작 방식

- web view가 HTML과 CSS를 표시하지만 화면 push, back gesture와 transition은 native navigation이 맡는다.
- 서버가 새 web screen을 배포하면 client는 별도 app update 없이 그 HTML을 표시할 수 있다.
- Bridge Component는 Stimulus controller와 Swift/Kotlin counterpart를 연결해 native button, menu와 platform API를 호출한다.
- camera·biometric처럼 반응성과 platform 통합이 중요한 기능은 component 또는 전체 native screen으로 구현할 수 있다.

# 잘 맞는 경우

responsive server-rendered web app이 이미 있고 iOS·Android의 기능 대부분이 form, content와 account workflow인 작은 팀에 유리하다. Rails와 궁합이 좋지만 핵심 조건은 특정 framework가 아니라 link 중심의 server-rendered HTML이다.

# 경계

영상의 “한 명으로 가능”, “비용 80% 절감” 같은 수치는 발표자의 경험이며 보장값이 아니다. web screen 변경은 빠르지만 native shell, bridge code와 권한을 바꾸면 app store 배포가 필요하다. 결제·개인정보·review 정책 역시 web view라고 사라지지 않는다. offline-first, 무거운 animation, background processing과 고성능 native interaction이 핵심이면 다른 architecture가 나을 수 있다.

# 출처

- [YouTube 원본 영상](https://www.youtube.com/watch?v=yIdzxdLX9Dk)
- [Hotwire Native 공식 동작 설명](https://native.hotwired.dev/overview/how-it-works)
- [Bridge Components](https://native.hotwired.dev/overview/bridge-components)
- [Notion 원본 항목](https://app.notion.com/p/d081a73cf20b8282925281f58c75d562)
