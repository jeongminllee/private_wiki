---
type: Reference
title: "tui.builders와 SuperLightTUI"
description: "브라우저에서 터미널 UI를 설계하고 대응하는 Rust 코드를 생성하는 도구와 라이브러리"
resource: https://news.hada.io/topic?id=27581
notion: https://app.notion.com/p/c511a73cf20b82e48cf28186e13799fe
tags: [reading, rust, tui, developer-tools]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

`tui.builders`는 위젯을 시각적으로 배치해 Rust 코드를 내보내는 브라우저 기반 TUI 편집기다. `SuperLightTUI`는 편집기 속성과 코드가 1:1로 대응하도록 만든 Rust 즉시 모드(immediate-mode) 라이브러리다.

# 핵심 아이디어

- 인스펙터의 너비, 패딩, 테두리 설정이 메서드 호출로 바로 변환된다.
- CSS Flexbox와 Tailwind 유틸리티에 가까운 레이아웃 감각을 사용한다.
- 앱 구조체와 복잡한 이벤트 루프 구현 없이 클로저 중심으로 시작할 수 있다.
- 기반 의존성은 `crossterm`과 `unicode-width`이며 `unsafe` 코드를 쓰지 않는다고 소개한다.
- 차트, 테이블, 이미지 등을 포함한 50개 이상의 위젯을 제공한다.

# 언제 유용한가

내부 관리 CLI, 서버 모니터링 화면, 설치 마법사처럼 배포가 간단한 단일 바이너리 UI가 필요할 때 후보가 된다. 다만 프로젝트의 성숙도, 접근성, 키보드 동작, 대형 데이터 렌더링 성능은 실제 프로토타입으로 검증해야 한다.

# 출처

- [GeekNews 소개](https://news.hada.io/topic?id=27581)
- [tui.builders](https://tui.builders)
- [SuperLightTUI GitHub](https://github.com/subinium/SuperLightTUI)

