---
type: Reference
title: "GLM-4.7 성능과 실용성: 장문 코딩 에이전트에 강하지만 검증이 필요한 비교"
description: "MoE 구조, 긴 컨텍스트, 멀티턴 추론과 코딩 벤치마크를 정리하고 가격·로컬 실행 제약을 함께 본 글"
resource: "https://litmers.com/blog/glm-4-7-%EC%84%B1%EB%8A%A5-%EC%B4%9D%EC%A0%95%EB%A6%AC-%EA%B0%80%EA%B2%A9-%ED%9B%84%EA%B8%B0-gpt-%ED%81%B4%EB%A1%9C%EB%93%9C-%EC%A0%9C%EB%AF%B8%EB%82%98%EC%9D%B4-%EB%B9%84%EA%B5%90%EA%B9%8C%EC%A7%80"
notion: "https://app.notion.com/p/3e11a73cf20b8228b4eb01935fd0ba4d"
tags: [reading, llm, coding-agents, model-evaluation]
timestamp: 2026-07-24
status: summarized
---

# 글이 강조하는 특징

GLM-4.7을 코딩, 복잡 추론과 도구 기반 멀티턴 작업에 초점을 둔 open-weight MoE 모델로 소개한다. 총 parameter는 약 355~358B, token마다 활성화되는 용량은 약 32B로 설명하며 200K 입력 context와 최대 128K 출력을 제시한다. Interleaved Thinking과 Preserved Thinking으로 tool call 전후와 여러 turn 사이의 추론 일관성을 높였다는 것이 핵심 주장이다.

글에 인용된 지표는 MMLU-Pro 84.3, GPQA-Diamond 85.7, AIME 2025 95.7, HLE with tools 42.8%, SWE-bench Verified 73.8%, SWE-bench Multilingual 66.7%, TerminalBench 2.0 41.0%다. 특히 파일 수정, test와 재시도가 이어지는 coding agent 작업에서 전작보다 상태 유지가 좋아졌다고 평가한다.

# 비용과 실행

가중치를 직접 호스팅하거나 Z.ai와 partner API를 이용할 수 있다. 글은 특정 provider 기준 입력 $0.60/M token, 출력 $2.20/M token과 월 $3 coding plan을 소개한다. 다만 가격·quota는 변동하므로 사용 시점의 공식 페이지를 다시 확인해야 한다. 큰 MoE 모델이라 4-bit 양자화도 개인 장비에는 무겁고, 저렴한 API 사용이 더 현실적일 수 있다.

# 읽을 때의 주의

이 글의 수치 상당수는 제작사 발표나 서로 다른 출처의 benchmark를 재정리한 것이다. 경쟁 모델 표에는 세대가 다른 GPT·Claude·Gemini 이름과 추정치가 섞여 있어 동일 조건의 직접 비교로 볼 수 없다. “오픈소스”라는 표현도 source code와 training data까지 모두 공개됐다는 뜻인지, open weights와 사용 license를 뜻하는지 공식 model card에서 구분해야 한다.

실제 선택은 같은 repository task, prompt, context 길이와 tool harness에서 성공률·review 품질·지연·비용을 재측정해 결정하는 편이 낫다.

# 출처

- [Litmers의 GLM-4.7 정리](https://litmers.com/blog/glm-4-7-%EC%84%B1%EB%8A%A5-%EC%B4%9D%EC%A0%95%EB%A6%AC-%EA%B0%80%EA%B2%A9-%ED%9B%84%EA%B8%B0-gpt-%ED%81%B4%EB%A1%9C%EB%93%9C-%EC%A0%9C%EB%AF%B8%EB%82%98%EC%9D%B4-%EB%B9%84%EA%B5%90%EA%B9%8C%EC%A7%80)
