---
type: Reference
title: "Google Opal: 시각적 AI workflow로 만드는 mini app"
description: "여러 prompt, model과 tool을 node로 연결해 조사·문구·이미지·영상을 자동화하는 Google Labs의 no-code builder"
resource: "https://www.youtube.com/watch?v=GzGcQzMo_Rw"
notion: "https://app.notion.com/p/0341a73cf20b83479af0816ce96f8ce1"
tags: [reading, google, opal, workflow, no-code, ai-agent]
timestamp: 2026-07-24
status: summarized
---

# 무엇인가

영상에서 “58”처럼 들리는 제품명은 `Opal(오팔)`이다. Project Astra가 아니라 Google Labs가 공개한 실험적 AI mini-app builder다. 자연어로 원하는 app을 설명하면 input, prompt·model 호출, tool과 output을 연결한 workflow를 만들고, 사용자는 visual editor에서 각 단계를 수정하거나 gallery의 예제를 remix할 수 있다.

영상은 제품명 하나를 입력하면 web research, marketing copy, video prompt와 생성 model을 차례로 실행하는 사례를 보여준다. Input image를 추가해 여러 node로 보내거나, model과 단계별 instruction을 바꾸고 image generation node를 붙이는 식으로 workflow를 확장한다. 완성된 app은 Google 계정 사용자가 바로 실행할 수 있는 형태로 공유된다.

# 어디에 쓸 수 있나

- 제품 조사 결과를 문구·poster·video 초안으로 변환
- YouTube 링크를 요약하고 이해도 문제를 만드는 학습 app
- 주제에서 blog 초안과 시각 자료를 함께 생성
- 반복되는 multi-model prompt를 재사용 가능한 업무 화면으로 제공

핵심 가치는 한 번의 거대한 prompt가 아니라 단계별 input과 output을 눈으로 확인하고 수정하는 데 있다. 실패한 node만 다시 실행하고 중간 결과를 검사할 수 있어 단순 chat보다 debugging하기 쉽다.

# 확인과 주의

영상의 미국 계정·VPN 필요 설명은 시점상 부정확하거나 이전 상태를 따른 안내다. Google은 2025년 10월 7일 이미 한국을 포함한 15개국으로 Opal을 확대했고, 12월 17일에는 Gemini web의 실험적 Gems에서도 Opal mini app을 만들 수 있다고 발표했다.

Opal은 prototype과 개인 자동화에 적합하지만 “업무 전부 자동화”는 과장된 표현이다. Web research의 hallucination, 생성 media 권리, 외부 system 쓰기 권한, 비용과 재시도 정책을 workflow가 자동으로 해결하지 않는다. 중요한 업무에서는 단계별 schema, source citation, human approval, 실패 fallback과 평가 sample을 추가해야 한다.

YouTube에는 한국어 자동 자막 track이 있으나 수집 시점에 transcript endpoint가 `429 Too Many Requests`를 반환했다. 따라서 영상의 공개 metadata와 상세한 공개 요약을 공식 Opal 문서로 대조했으며, 발화 전문을 인용하지 않았다.

# 출처

- [원본 YouTube 영상](https://www.youtube.com/watch?v=GzGcQzMo_Rw)
- [Google Developers의 Opal 소개](https://developers.googleblog.com/en/introducing-opal/)
- [Opal 공식 overview](https://developers.google.com/opal/overview)
- [Google Korea의 한국 서비스 확대 발표](https://blog.google/intl/ko-kr/products/opal-expansion-kr/)
- [Gemini web의 Opal mini app 발표](https://blog.google/innovation-and-ai/models-and-research/google-labs/mini-apps-opal-gemini-app-experiment/)
