---
type: Paper Note
title: "CCPS: 내부 표현 교란으로 LLM 답변 신뢰도 추정하기"
description: "최종 hidden state를 미세하게 교란했을 때의 안정성으로 답변 정답 확률을 학습하는 confidence calibration 방법"
resource: "https://www.aitimes.com/news/articleView.html?idxno=204039"
notion: "https://app.notion.com/p/0271a73cf20b8323958d81f3184b4c5f"
tags: [reading, paper, llm, calibration, uncertainty]
timestamp: 2026-07-24
status: summarized
---

# 문제와 방법

LLM이 말로 표현하는 자신감이나 한 번의 token probability는 실제 정답률과 잘 맞지 않을 수 있다. `CCPS(Calibrating LLM Confidence by Probing Perturbed Representation Stability)`는 답변 token을 만든 마지막 hidden state를 adversarial direction으로 조금씩 움직여, 원래 선택이 얼마나 쉽게 흔들리는지 측정한다.

각 token에서 원래 probability·entropy·margin, top token이 바뀌는 데 필요한 perturbation, perturbed distribution과 원본의 divergence 같은 feature를 만든다. Multiple-choice에는 MLP, open-ended 답변에는 1D convolution과 pooling을 사용해 전체 답변이 맞을 확률을 예측한다. Base LLM은 frozen 상태지만, feature projection과 classifier는 정답 label로 학습한다.

# 보고된 결과

Llama 3.1 8B, Qwen 2.5 14B·32B, Mistral 24B를 MMLU와 MMLU-Pro의 객관식·주관식 형태로 평가했다. 논문은 가장 강한 비교 방법 대비 평균 ECE를 약 55%, Brier score를 21% 줄이고 accuracy 5%p, AUPRC 4%p, AUROC 6%p를 높였다고 보고한다.

# 해석과 한계

“조금 흔들어 답이 바뀌면 틀렸다”는 사용자 prompt 요령이 아니라 model 내부 activation과 gradient에 접근해야 하는 방법이다. Closed API에는 그대로 적용하기 어렵고, 별도 labeled calibration data와 model별 feature extraction 비용이 든다. MMLU 계열 성능이 긴 reasoning, 사실 확인, 의료·금융의 distribution shift까지 보장하지도 않는다.

Confidence score는 답변의 근거나 진실을 증명하지 않는다. Human review 우선순위를 정하는 risk signal로 사용하고, retrieval evidence, external verifier와 domain validation을 함께 둬야 한다.

# 출처

- [AI타임스 소개 기사](https://www.aitimes.com/news/articleView.html?idxno=204039)
- [CCPS 논문](https://arxiv.org/abs/2505.21772)
- [공개 코드](https://github.com/ledengary/CCPS)
