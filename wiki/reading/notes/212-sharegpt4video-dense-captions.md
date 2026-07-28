---
type: Paper Note
title: "ShareGPT4Video: 정밀한 영상 caption이 이해와 생성을 함께 개선한다"
description: "시간 변화와 frame 세부를 촘촘히 기술하는 caption dataset, captioner와 8B video-language model"
resource: https://sharegpt4video.github.io/
notion: https://app.notion.com/p/f291a73cf20b831c8bcf81f085b79cf6
tags: [reading, paper, video, multimodal, dataset]
timestamp: 2026-07-24
status: summarized
---

# 문제

영상에 여러 frame을 단순 연결해 image model로 caption을 만들면 시간 순서를 혼동하거나 변화 과정을 놓치기 쉽다. ShareGPT4Video는 frame 내부의 세부와 frame 사이의 변화를 함께 설명하는 고밀도 caption이 video understanding과 text-to-video generation 양쪽의 학습 품질을 높인다고 본다.

# 구성

- **ShareGPT4Video dataset**: GPT-4V로 주석한 4만 개 video-caption pair
- **ShareCaptioner-Video**: 임의 길이·해상도·aspect ratio 영상을 설명하는 caption model
- **확장 dataset**: captioner로 주석한 480만 개 미적 영상
- **ShareGPT4Video-8B**: 이 자료로 학습한 large video-language model

caption에는 object attribute, world knowledge, camera movement와 사건의 시간적 변화가 포함된다. 연구진은 differential caption을 재사용해 sub-clip을 다시 설명하는 전략으로 길이에 대한 확장성을 확보한다.

# 결과와 주의점

프로젝트는 8B 모델이 세 video benchmark에서 당시 최고 성능을 냈고, 더 좋은 caption이 10초 text-to-video 생성에도 도움이 됐다고 보고한다. 다만 원본 video 저작권을 보유하지 않아 연구용 link-annotation pair 형태로 제공하므로 상업적 재배포와 원본 접근 안정성을 별도 확인해야 한다.

# 출처

- [ShareGPT4Video project](https://sharegpt4video.github.io/)

