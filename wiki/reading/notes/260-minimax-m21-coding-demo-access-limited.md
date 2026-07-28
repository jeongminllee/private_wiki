---
type: Reference
title: "MiniMax M2.1 Coding Agent 장기 지시 실험: 자막 확인 필요"
description: "영상 제목과 제작자는 확인됐지만 설명·자막을 가져오지 못한 coding agent demo 기록"
resource: https://www.youtube.com/watch?v=f6kxojY2Cxw
resource_aliases: [https://youtu.be/f6kxojY2Cxw]
notion: https://app.notion.com/p/8a11a73cf20b8276a33601a51d4d3351
tags: [reading, access-limited, coding-agent, video]
timestamp: 2026-07-24
status: access-limited
---

# 확인된 내용

YouTube oEmbed metadata에서 영상 제목은 “MiniMax M2.1 Coding Agent Demo (MiniMax M2.1 ‘장기지시 수행 모델’ 실험 영상)”, 제작자는 `AmesianX`로 확인된다. 영상은 embed 가능한 공개 상태다.

# 막힌 이유

2026-07-24 확인 당시 공개 metadata에는 설명이 없었고 caption track도 반환되지 않았다. 영상 화면과 음성을 안정적으로 추출할 수 없어 어떤 task, repository, prompt와 평가 기준을 사용했는지 확인하지 못했다.

제목만으로 MiniMax M2.1이 장기 지시를 성공적으로 수행했다고 결론 내리면 demo의 성공·실패 과정과 사람의 개입을 누락하게 된다. 따라서 model 사양이나 다른 review의 내용을 영상 내용처럼 대신 채우지 않았다.

# 다시 처리하려면

- YouTube에서 내보낸 자막 또는 transcript
- 주요 장면과 prompt가 포함된 영상 요약
- 영상 file이나 audio transcript

# 출처

- [YouTube 영상](https://www.youtube.com/watch?v=f6kxojY2Cxw)
