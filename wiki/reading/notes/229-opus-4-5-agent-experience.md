---
type: Reference
title: "Opus 4.5 자율 개발 경험에서 분리해야 할 능력과 책임"
description: "여러 application을 빠르게 만든 개인 사례와 production 품질·보안·유지보수의 간극"
resource: https://news.hada.io/topic?id=25629
notion: https://app.notion.com/p/5f21a73cf20b8300a4450194f680649b
tags: [reading, ai-coding, claude, software-engineering]
timestamp: 2026-07-24
status: summarized
---

# 경험 사례

작성자는 Opus 4.5에 Windows image converter, 화면 녹화·편집 도구, AI 게시 app과 주문 추적 app을 맡겼다. model이 CLI build, 오류 수정, Firebase 설정, GitHub Actions와 배포까지 수행해 prototype 제작 시간이 크게 줄었다고 평가한다.

# 실제로 강했던 부분

명확한 목표와 빠른 feedback이 있는 새 project에서 scaffold, integration과 반복 수정이 빠르다. 단순한 구조, 명시적 control flow, 낮은 coupling, structured logging처럼 agent가 읽고 다시 만들기 쉬운 설계를 지시했을 때 효과가 컸다.

# 과장해서는 안 되는 부분

개인 prototype 몇 개는 기존 대규모 codebase의 유지보수, 성능, 접근성, 보안과 장기 ownership을 증명하지 않는다. 작성자도 보안 완성도를 약 80%로 보았고 API key 관리는 직접 책임져야 한다고 했다. 토론에는 임의 코드 삭제, 저수준 algorithm 실패, 높은 token 비용과 “마지막 20%”의 제품화 난도가 보고됐다.

# 결론

이 사례의 핵심은 개발자 대체를 단정하는 데 있지 않다. 잘 정의된 작업에서 실행 loop를 크게 위임할 수 있게 됐지만, 요구사항·acceptance test·review·배포 책임의 가치는 오히려 커진다.

# 출처

- [GeekNews 정리와 토론](https://news.hada.io/topic?id=25629)

