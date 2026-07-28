---
type: Reference
title: "Claude Code로 만든 해외 송금 비교 서비스"
description: "Next.js, Supabase와 정기 scraper로 SendFeeCompare를 만든 개발자가 AI 코딩의 강점과 설계 한계를 정리한 사례"
resource: https://yozm.wishket.com/magazine/detail/3660/
notion: https://app.notion.com/p/fa71a73cf20b83939a498167ec9dc15e
tags: [reading, claude-code, product, web-development]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

SendFeeCompare는 미국과 한국 사이의 여러 송금 서비스에서 환율, 명시 수수료와 예상 수령액을 비교하는 서비스다. 개발자는 출시 속도와 낮은 운영비를 우선해 Next.js, Supabase, Vercel과 GitHub Actions 기반 정기 수집을 선택하고, 반복 구현에 Claude Code를 사용했다.

# AI가 잘한 부분

- 비교 결과 카드처럼 요구가 구체적인 UI component 생성
- 비슷한 구조를 가진 여러 업체 scraper와 서비스 module 반복 구현
- 자동화 workflow, 문서와 테스트의 초안 작성
- 기존 pattern을 다른 통화·업체에 확장하는 기계적 변경

짧은 기간에 많은 module을 만들 수 있었던 이유는 AI의 코드 생성뿐 아니라 실제 사용자가 겪는 문제, 단순한 배포 구조와 반복 가능한 module 경계가 이미 있었기 때문이다.

# 사람이 맡은 부분

업체마다 정액·정률 수수료, 환율 margin과 promotion 방식이 달라 공통 데이터 모델로 정규화하는 판단은 도메인 이해가 필요했다. 실시간 scraping은 비용과 차단 위험이 있으므로 금액 구간과 갱신 주기를 정하는 운영 절충도 사람이 결정했다. AI 제안을 연속해서 무비판적으로 수락하면 중복 코드와 구조 불일치가 쌓였다는 회고도 중요하다.

# 적용 교훈

AI에는 이미 정한 pattern의 확장을 맡기고, schema·돈 계산·외부 데이터 신뢰성은 명시적 테스트와 사람이 소유한다. scraper 실패, 오래된 환율, promotion 누락을 관찰하고 사용자에게 갱신 시각과 계산 근거를 보여줘야 한다.

# 주의할 점

개인 프로젝트 회고이며 생산성 배수와 “운영비 0원”은 개발자의 조건과 무료 tier 시점에 의존한다. 금융 비교 결과는 실제 거래 전 각 업체에서 다시 확인해야 하며 affiliate 관계, 규제, 개인정보와 서비스 약관도 검토해야 한다.

# 출처

- [요즘IT 원문](https://yozm.wishket.com/magazine/detail/3660/)
- [SendFeeCompare](https://sendfeecompare.com/)
- [Notion 원본 항목](https://app.notion.com/p/fa71a73cf20b83939a498167ec9dc15e)

