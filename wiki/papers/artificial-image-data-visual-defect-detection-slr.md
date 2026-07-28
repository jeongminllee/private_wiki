---
type: Paper Note
title: A Systematic Literature Review of the Application of Artificial Image Data for Visual Defect Detection
description: 시각적 결함 검출에서 데이터 증강·GAN·오토인코더·확산 모델 등 인공 이미지 활용 연구를 분류하고, 실무 적용 조건과 리뷰 설계의 한계를 비판적으로 정리한 논문 노트
resource: https://doi.org/10.1109/ACCESS.2025.3615795
tags: [paper, visual-defect-detection, synthetic-data, data-augmentation, systematic-literature-review]
timestamp: 2026-07-25
status: reading
---

# One-line Summary

시각적 결함 검출의 데이터 부족을 다룬 연구에서는 전통적 데이터 증강(Data Augmentation)이 가장 널리 쓰이고 GAN이 그 뒤를 잇지만, 생성 이미지의 품질과 실제 검출 성능을 비교할 공통 평가 체계가 부족하며 이 리뷰 자체에도 검색·선정 문헌 수의 내부 불일치가 있다.

# Problem

결함 이미지는 정상 이미지보다 희소하고, 새로운 결함 유형이나 다양한 촬영 조건을 충분히 수집하기 어렵다. 이 때문에 딥러닝 기반 결함 검출 모델은 데이터 수와 다양성 부족, 클래스 불균형, 실제 환경으로의 일반화 문제를 겪는다.

이 논문은 다음 질문에 답하려 한다.

- 시각적 결함 검출용 데이터셋을 인공 이미지로 확장할 때 어떤 생성·변형 방법이 사용되는가?
- 그 방법들은 어떤 산업 영역에서 주로 사용되는가?
- 현재 연구가 집중된 영역과 아직 남은 공백은 무엇인가?

# Method

## 서지 정보

- 저자: Merlin Schadt, Christopher Mai, Ricardo Buettner
- 저널: IEEE Access, Volume 13, 2025, pp. 172674-172691
- DOI: [10.1109/ACCESS.2025.3615795](https://doi.org/10.1109/ACCESS.2025.3615795)
- 검색 기준일: 2025-01-19
- 원문: [로컬 PDF](../../raw/papers/A_Systematic_Literature_Review_of_the_Application_of_Artificial_Image_Data_for_Visual_Defect_Detection.pdf)
- SHA-256: `3E76C52096A7C4708A1DC82AD1212D5826CD4598A6CC17F85B7E0B4021E8B5B4`

## 검색 및 선정

- PRISMA 지침을 따른 Systematic Literature Review(SLR)를 표방한다.
- 데이터베이스는 IEEE Xplore와 ACM Digital Library 두 곳이다.
- 검색어는 다음 세 블록을 `AND`로 연결한다.
  - `deep learning`
  - `artificial images OR synthetic images`
  - `defect detection OR defect recognition`
- 2018년 이전, 영어 이외의 언어, 주제 외 문헌을 제외한다.
- 학술지와 early access 논문만 포함하고 conference paper는 제외한다.
- 제목·초록 선별을 모든 저자가 수행했으며, 논문은 84편에 대해 100% 합의했다고 보고한다. 별도의 inter-rater reliability 지표는 사용하지 않았다.

## 분류 프레임

연구를 두 축으로 분류한다.

1. 응용 영역: GICS(Global Industry Classification Standard)의 11개 섹터 중 실제 문헌이 모인 산업(Industry), 인프라(Infrastructure), 의료(Health Care)
2. 이미지 생성·변형 방법: 데이터 증강, Autoencoder/Decoder, GAN, 기타 방법

`기타 방법`에는 diffusion model, 시뮬레이션, 3D modelling, 결함 마스크·이미지 융합처럼 하나의 생성 계열로 묶기 어려운 접근이 포함된다.

# Experiments

이 논문은 새로운 결함 검출 모델을 학습하는 실험 논문이 아니라, 기존 연구를 수집·분류하고 보고된 결과를 비교하는 SLR이다.

## 리뷰 데이터

- 최초 검색 결과: IEEE Xplore 178건, ACM 65건
- 저자 본문의 최종 설명: IEEE 49편과 ACM 2편, 총 51편
- 논문이 보고한 방법별 핵심 결과: 데이터 증강 27편, 그다음 GAN, Autoencoder/Decoder와 기타 방법은 상대적으로 적음
- 연도별로는 데이터 증강이 전 기간에 지속적으로 사용되고, GAN은 2020년 이후 증가하는 경향을 보임

## 비교 대상

- 검출·분류 성능: accuracy, F1, AP, mAP, AUROC 등
- 합성 이미지 품질: FID, KID, SSIM 등
- 대표 검출기: 여러 연구에서 YOLO 계열, 특히 YOLOv5가 반복적으로 사용됨
- 대표 생성기: 생성 모델 가운데 DCGAN이 가장 자주 관찰됨

# Key Findings

## 확인된 결과

1. **데이터 증강이 기본 선택지다.** 구현이 쉽고 CPU에서도 비교적 빠르게 수행할 수 있으며, 적은 자원으로 기존 파이프라인에 넣기 쉽다.
2. **GAN은 새로운 결함 형태를 생성할 가능성이 있다.** 단순 회전·자르기·노이즈 추가와 달리 기존 데이터에 없던 결함 정보를 만들 수 있지만, 현실적인 이미지를 학습하려면 다시 충분한 원본 데이터와 GPU 자원이 필요할 수 있다.
3. **실제 이미지와 합성 이미지를 섞는 구성이 자주 유리했다.** 여러 연구에서 실제 데이터만 사용한 경우보다 혼합 데이터로 학습했을 때 검출·분류 지표가 개선되었다.
4. **최고 개선 폭은 영역과 지표마다 다르다.** 논문은 산업 분야에서 최대 약 15.18%p F1 향상, 인프라 분야에서 최대 20%p mAP 향상, 의료 분야에서 stable diffusion을 사용한 13%p 이상의 향상을 소개한다.
5. **숫자를 직접 서열화하면 안 된다.** 연구마다 데이터셋, 분할, 결함 유형, 모델, 지표가 다르므로 위 개선 폭은 방법 간 우열을 증명하는 메타분석 결과가 아니다.
6. **합성 이미지 품질 평가가 표준화되지 않았다.** FID·KID·SSIM은 서로 변환할 수 없고, 같은 FID라도 데이터 복잡도와 해상도가 다르면 직접 비교하기 어렵다.
7. **확산 모델은 잠재력과 비용을 함께 가진다.** 더 사실적인 이미지 생성 가능성이 있지만 느린 sampling, 어려운 학습, 높은 연산 자원이 장애물이다.
8. **의료 분야는 별도 검증이 필요하다.** 생물학적으로 불가능한 특징, 잘못된 병변, 규제·프라이버시, 설명 가능성, 임상 수용성 때문에 단순 성능 향상만으로 적용을 정당화할 수 없다.

## 논문이 제시한 연구 공백

- 소량의 원본으로도 안정적으로 학습되는 경량 생성 모델
- diffusion model의 속도와 자원 효율 개선
- 생성 방법 간 공정한 비교
- 합성 이미지 품질과 downstream 검출 성능을 함께 평가하는 표준
- 의료 영상에서의 별도 SLR과 전문가 검증
- GICS의 나머지 섹터와 video/frame 기반 실시간 결함 검출

# My Understanding

## 실무적으로 읽으면

이 논문의 가장 유용한 메시지는 “생성 모델이 전통적 증강보다 항상 낫다”가 아니다. 오히려 다음 순서로 접근해야 한다는 근거에 가깝다.

1. 실제 데이터 분할과 누수 방지 기준을 먼저 고정한다.
2. 회전·crop·색상·noise 등 물리적으로 타당한 데이터 증강을 baseline으로 둔다.
3. 기존 샘플의 변형만으로 만들 수 없는 희귀 결함 형태가 필요한지 판단한다.
4. 그때 GAN·diffusion·결함 합성·물리 시뮬레이션을 후보로 추가한다.
5. 생성 이미지의 외형뿐 아니라 실제 데이터만으로 구성한 holdout에서 검출 성능·calibration·오탐을 평가한다.

핵심은 합성 이미지의 “그럴듯함”이 아니라 **실제 환경에서의 task utility와 위험**이다. FID가 낮더라도 결함의 위치·크기·경계·물리적 발생 조건이 틀리면 검출기에 잘못된 shortcut을 학습시킬 수 있다.

## 비판적 검토

### 1. PRISMA 수치가 내부적으로 일치하지 않는다

- Figure 2는 최초 243건에서 제외 기준으로 160건을 제거했다고 적는다. 산술적으로는 83건이지만 다음 단계에는 84건이 표시된다.
- 같은 도식은 off-topic 32건을 제외해 최종 52편이라고 표시한다.
- 본문은 84편 중 33편을 제외하고 IEEE 49편과 ACM 2편, 총 51편이라고 설명한다.

따라서 최종 분석 집합이 51편인지 52편인지, 어느 단계에서 한 편의 차이가 생겼는지 원문만으로 재현할 수 없다.

### 2. 의료 분야의 보강 검색 경계가 불명확하다

결과 절은 의료 분야에서 데이터 증강뿐 아니라 Autoencoder, GAN, diffusion 연구를 소개한다. 그러나 Discussion은 최초 검색에서 해당 생성 방법의 의료 연구를 찾지 못했고, 이후 Web of Science를 수동 검색했다고 말한다. Web of Science 검색식·검색일·선정 절차와 보강 문헌이 최초 51편에 포함되는지는 Method에 명확히 통합되어 있지 않다.

### 3. 검색 범위가 좁다

- `visual anomaly detection`, `surface inspection`, `fault detection`, `quality inspection`처럼 결함 검출 연구에서 흔한 표현이 검색식에 없다.
- `data augmentation`, `GAN`, `diffusion`도 검색식에 직접 포함되지 않는다.
- 컴퓨터 비전 연구가 많이 발표되는 conference paper를 모두 제외했다.
- IEEE·ACM만 사용해 Scopus, Web of Science, PubMed, arXiv 등의 연구가 체계적으로 포함되지 않았다.

따라서 이 논문은 분야 전체의 완전한 지도보다, 좁은 검색식으로 얻은 peer-reviewed journal 표본의 분류로 보는 편이 안전하다.

### 4. 연구 품질 평가와 정량 합성이 약하다

- 개별 연구의 bias risk나 품질 점수를 체계적으로 평가하지 않는다.
- 저자 전원 합의 100%를 보고하지만 독립 평가 과정과 Cohen's kappa 같은 신뢰도 지표는 없다.
- 서로 다른 데이터셋과 지표의 최고 개선 폭을 나열하므로 방법의 평균 효과나 통계적 우월성을 말할 수 없다.
- FID·SSIM 같은 일반 이미지 유사도만으로 결함의 물리적 타당성과 검출 유용성을 보장할 수 없다.

### 5. 분류 체계가 기술적 의사결정에는 거칠다

GICS는 응용 산업을 정리하기에는 유용하지만, 실제 모델 선택에는 다음 축이 더 직접적이다.

- image-level classification / localization / object detection / segmentation
- supervised / semi-supervised / unsupervised anomaly detection
- image-to-image translation / mask-conditioned generation / physics simulation / 3D rendering
- 데이터 희소성 / 클래스 불균형 / domain shift / privacy 목적
- real-to-synthetic 비율과 실제 holdout 성능

# How I Can Use This

## 결함 검출 프로젝트의 실험 순서

1. **Real-only baseline**: 실제 데이터만으로 모델과 분할 기준을 고정한다.
2. **Classical DA baseline**: 결함의 물리적 의미를 보존하는 증강만 적용한다.
3. **Synthetic 후보 분리**: GAN, diffusion, copy-paste/mask 합성, 물리 시뮬레이션을 각각 독립 실험으로 둔다.
4. **혼합 비율 ablation**: real:synthetic 비율을 바꾸고 실제 holdout에서 비교한다.
5. **두 종류의 평가**:
   - 이미지 품질: FID/KID/SSIM, 다양성, 중복·memorization
   - 과업 품질: 실제 데이터의 AP/mAP/F1, class별 recall, calibration, false positive
6. **도메인 검토**: 제조·인프라는 공정 전문가, 의료는 임상 전문가가 결함의 타당성을 확인한다.
7. **외부 검증**: 다른 설비·카메라·현장·기관 데이터에서 일반화를 확인한다.

## 이 논문을 인용할 때

- “2025년 SLR에서 데이터 증강이 가장 흔한 방법으로 보고되었다”는 배경 근거로 사용할 수 있다.
- 특정 생성 방법이 더 우수하다는 근거로 사용하면 안 된다.
- “51편을 분석했다”고 쓸 때는 Figure 2의 52편 표기와 수치 불일치를 함께 확인해야 한다.

# Open Questions

- 합성 이미지의 실제성보다 downstream 성능을 더 잘 예측하는 defect-aware 품질 지표는 무엇인가?
- 실제 결함이 극히 적을 때 생성 모델이 결함을 학습한 것인지 배경·촬영 조건을 복제한 것인지 어떻게 검증할 수 있는가?
- real:synthetic 비율의 최적점은 결함 희소도와 domain shift에 따라 어떻게 변하는가?
- 합성 데이터가 class imbalance를 완화하면서 새로운 편향이나 shortcut을 만들지는 않는가?
- 생성 모델이 training image를 암기하지 않았음을 어떤 privacy·similarity 검사로 확인할 것인가?
- 물리 시뮬레이션, copy-paste, GAN, diffusion을 동일 데이터와 검출기로 비교하면 비용 대비 효율은 어떻게 달라지는가?
- 의료 부문 보강 문헌과 최초 SLR 집합을 분리해 재현하면 논문의 결론이 유지되는가?

# Related Concepts

- [Papers Index](index.md)

현재 위키에는 visual defect detection 또는 synthetic defect data를 직접 다룬 기존 concept 문서가 없다. 후속 분석에서 `합성 결함 데이터 평가`와 `결함 검출 데이터 증강 전략`을 독립 concept로 분리할 가치가 있다.

# Citations

- Schadt, M., Mai, C., & Buettner, R. (2025). *A Systematic Literature Review of the Application of Artificial Image Data for Visual Defect Detection*. IEEE Access, 13, 172674-172691. [DOI](https://doi.org/10.1109/ACCESS.2025.3615795)
- Method와 PRISMA 흐름: 원문 pp. 3-6.
- 분야·방법별 결과: 원문 pp. 7-12.
- Discussion, 한계, 향후 연구: 원문 pp. 12-16.
