---
type: Reference
title: "Gemini Gems from Google Labs"
description: "Opal 기반 workflow를 자연어로 구성해 입력 UI와 여러 생성 모델을 묶은 AI mini-app을 만드는 실험 기능"
resource: https://tilnote.io/en/pages/696ece9ec47e87b8bec472ef
notion: https://app.notion.com/p/ede1a73cf20b82d29d8b81a1895cb007
tags: [reading, gemini, no-code, ai-workflow]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

Classic Gem이 반복 대화를 위한 맞춤형 chatbot이라면 Gems from Google Labs는 입력, 처리 단계와 출력을 가진 interactive mini-app이다. Google Labs의 Opal을 기반으로 text, image, video, music model을 workflow 안에 연결하고 자연어로 단계를 만들거나 수정할 수 있다.

# 만들고 사용하는 흐름

Gemini web의 Gems manager에서 만들 앱을 설명하면 workflow 단계와 preview가 생성된다. 사용자는 단계를 검토하고 실행한 뒤 자연어로 수정하거나 advanced editor를 열 수 있다. Google이 제공하는 template을 그대로 실행하거나 remix할 수도 있으며, 완성된 mini-app은 특정 사용자, link 공개 또는 public 범위로 공유할 수 있다.

강의 노트를 받아 image와 audio가 포함된 학습 가이드를 만드는 흐름처럼 한 번의 대화보다 반복 가능한 입력·출력 형식이 있는 작업에 적합하다. 먼저 성공 조건이 단순한 개인 workflow로 시험하고 각 단계의 중간 결과를 검토한다.

# 현재 조건

공식 도움말 기준으로 18세 이상 개인 Google 계정, desktop의 Gemini web과 영어 환경이 필요하며 업무·학교 계정과 mobile app에서는 아직 지원되지 않는다. 실험 기능이므로 제공 범위와 UI는 바뀔 수 있다.

# 개인정보와 공유 주의

Opal은 Gemini Apps 자체가 아니어서 Gemini Apps Activity와 Workspace connected-app 설정의 통제를 받지 않는다. 생성한 app, interaction과 업로드 media는 Google Drive의 `Opal` 폴더에 저장된다. public 또는 link 공유를 선택하면 민감한 instruction과 file이 노출되지 않는지 확인하고, 외부 입력의 prompt injection과 잘못된 생성 결과를 검증한다.

# 출처

- [Google 공식 도움말](https://support.google.com/gemini/answer/16802014?hl=en-GB)
- [Google Gemini privacy 안내](https://support.google.com/gemini/answer/13594961?hl=en-MP)
- [저장된 TILNOTE 가이드](https://tilnote.io/en/pages/696ece9ec47e87b8bec472ef)
- [Notion 원본 항목](https://app.notion.com/p/ede1a73cf20b82d29d8b81a1895cb007)

