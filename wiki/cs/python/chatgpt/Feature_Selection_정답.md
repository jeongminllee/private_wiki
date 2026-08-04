---
type: Concept
title: "Feature Selection 정답"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2026-05-14)"
tags: [cs, chatgpt-export]
timestamp: 2026-05-14
status: active
---

# Feature Selection 정답

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-14

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
Which of the following is true about feature selection?



Reduce noise by only keeping useful features

Reduce data processing time

Reduce collinearity from highly correlated features

Increase cost related to deployment

Mitigate overfitting

이거 정답은 뭘까

### 💡 답변 (Assistant)
정답은 **대부분 참이고, “Increase cost related to deployment”만 거짓**입니다.

Feature selection의 효과는 다음과 같습니다.

| 보기 | 정답 여부 | 이유 |
|---|---:|---|
| **Reduce noise by only keeping useful features** | 참 | 불필요하거나 의미 없는 feature를 제거해서 노이즈를 줄일 수 있음 |
| **Reduce data processing time** | 참 | feature 수가 줄어들면 학습/추론/전처리 시간이 줄어듦 |
| **Reduce collinearity from highly correlated features** | 참 | 서로 강하게 상관된 feature 중 일부를 제거해 다중공선성을 줄일 수 있음 |
| **Increase cost related to deployment** | 거짓 | 보통 feature 수가 줄어들어 배포 비용과 복잡도가 감소함 |
| **Mitigate overfitting** | 참 | 불필요한 feature를 줄이면 모델이 잡음에 과적합되는 위험이 줄어듦 |

따라서 체크해야 할 것은:

**Reduce noise by only keeping useful features**  
**Reduce data processing time**  
**Reduce collinearity from highly correlated features**  
**Mitigate overfitting**

체크하지 말아야 할 것은:

**Increase cost related to deployment**

---

### ❓ 질문 (User)
15년차 베테랑 머신러닝 리서처 처럼 자세하게 설명해줘.

### 💡 답변 (Assistant)
좋습니다. 이 문제는 단순히 “feature selection의 장점 고르기”처럼 보이지만, 실제 머신러닝 관점에서는 **모델 일반화 성능, 계산 비용, 데이터 품질, 배포 안정성**까지 연결되는 꽤 중요한 개념입니다.

결론부터 말하면 정답은 다음 4개입니다.

> **Reduce noise by only keeping useful features**  
> **Reduce data processing time**  
> **Reduce collinearity from highly correlated features**  
> **Mitigate overfitting**

그리고 틀린 선택지는 이것입니다.

> **Increase cost related to deployment**

---

# 1. Feature Selection이란?

**Feature selection**은 모델 학습에 사용할 입력 변수, 즉 feature들 중에서 **유용한 feature만 선택하고 불필요한 feature는 제거하는 과정**입니다.

예를 들어 타이타닉 생존 예측 모델을 만든다고 해보겠습니다.

```text
입력 feature:
- age
- sex
- pclass
- fare
- cabin
- passenger_id
- ticket_number
- name
- embarked
```

이 중에서 `passenger_id`는 승객을 구분하기 위한 ID일 뿐이고, 일반적으로 생존 여부를 설명하는 데 직접적인 의미가 없습니다. `ticket_number`도 특정 상황에서는 의미가 있을 수 있지만, 대부분은 노이즈가 될 가능성이 큽니다.

Feature selection은 이런 식으로 질문합니다.

> “이 feature가 정말 예측에 도움이 되는가?”  
> “이 feature가 모델을 더 복잡하게만 만들고 있지는 않은가?”  
> “이 feature 때문에 모델이 훈련 데이터에만 과하게 맞춰지는 것은 아닌가?”

---

# 2. 선택지별로 자세히 보기

---

## ① Reduce noise by only keeping useful features

> **유용한 feature만 남겨서 노이즈를 줄인다.**

이건 **맞는 설명**입니다.

머신러닝에서 모든 feature가 좋은 것은 아닙니다. 어떤 feature는 실제 패턴을 담고 있지만, 어떤 feature는 거의 랜덤한 정보에 가깝습니다.

예를 들어 신용 위험 예측 모델을 만든다고 해보겠습니다.

```text
유용할 가능성이 높은 feature:
- income
- credit history
- debt ratio
- payment delay history
- employment status

노이즈일 가능성이 높은 feature:
- customer_id
- random serial number
- registration form color
- meaningless code
```

모델은 생각보다 “쓸모없는 feature”에서도 패턴을 찾으려고 합니다. 특히 decision tree, random forest, gradient boosting, neural network 같은 모델은 복잡한 관계를 잘 찾는 대신, **우연히 생긴 패턴까지 학습할 위험**이 있습니다.

예를 들어 훈련 데이터에서 우연히 이런 일이 있었다고 해보겠습니다.

```text
customer_id가 7000 이상인 사람들 중 bad credit이 많았다
```

실제로는 customer_id가 신용 위험과 아무 관련이 없는데, 모델이 이걸 중요한 패턴으로 착각할 수 있습니다.

이런 feature는 모델 입장에서 **노이즈**입니다.

Feature selection을 하면 이런 노이즈 feature를 제거해서 모델이 더 핵심적인 정보에 집중할 수 있습니다.

그래서 이 선택지는 맞습니다.

---

## ② Reduce data processing time

> **데이터 처리 시간을 줄인다.**

이것도 **맞는 설명**입니다.

Feature 수가 많으면 다음 과정들이 모두 느려집니다.

```text
데이터 로딩
결측치 처리
인코딩
스케일링
학습
검증
추론
모델 저장
배포 후 실시간 예측
```

예를 들어 feature가 10개인 데이터와 10,000개인 데이터를 비교하면, 같은 샘플 수라도 처리량이 완전히 달라집니다.

특히 다음과 같은 모델에서는 feature 수가 계산량에 직접적으로 영향을 줍니다.

```text
Linear Regression
Logistic Regression
SVM
KNN
Random Forest
XGBoost
LightGBM
Neural Network
```

예를 들어 선형 모델에서는 대략적으로 입력 차원이 커질수록 계산해야 할 weight 수가 증가합니다.

```text
feature 10개  → weight 10개
feature 1,000개 → weight 1,000개
feature 100,000개 → weight 100,000개
```

딥러닝에서도 입력 feature 수가 많아지면 첫 번째 layer의 parameter 수가 늘어납니다.

예를 들어:

```python
input_dim = 10000
hidden_dim = 512
```

이면 첫 layer parameter 수는 대략:

```text
10000 × 512 = 5,120,000개
```

반면 feature selection으로 input_dim을 1,000개로 줄이면:

```text
1000 × 512 = 512,000개
```

10분의 1 수준으로 줄어듭니다.

즉 feature selection은 단순히 성능 개선만이 아니라, **학습 비용과 추론 비용을 줄이는 최적화 작업**이기도 합니다.

그래서 이 선택지도 맞습니다.

---

## ③ Reduce collinearity from highly correlated features

> **강하게 상관된 feature들로 인한 collinearity를 줄인다.**

이것도 **맞는 설명**입니다.

여기서 중요한 단어가 **collinearity**, 또는 **multicollinearity**입니다.

쉽게 말하면 feature들끼리 너무 비슷한 정보를 담고 있는 상황입니다.

예를 들어 집값 예측 모델을 만든다고 해보겠습니다.

```text
feature A: 집 면적, square meter
feature B: 집 면적, 평
feature C: 방 개수
feature D: 건물 총면적
```

`집 면적(square meter)`와 `집 면적(평)`은 사실상 같은 정보입니다. 단위만 다릅니다.

또 다른 예:

```text
height_cm
height_m
weight_kg
BMI
```

`BMI`는 height와 weight로 계산됩니다. 즉 feature들 사이에 정보가 강하게 겹칩니다.

이런 상관성이 높은 feature들이 많으면, 특히 선형 모델에서 문제가 됩니다.

대표적으로:

```text
Linear Regression
Logistic Regression
Ridge/Lasso Regression
Generalized Linear Model
```

이런 모델들은 feature 간 독립성 또는 낮은 상관성을 어느 정도 기대합니다. 그런데 feature들이 서로 강하게 상관되어 있으면 모델이 이렇게 헷갈릴 수 있습니다.

> “도대체 age가 중요한 거야, birth_year가 중요한 거야?”  
> “income이 중요한 거야, tax_paid가 중요한 거야?”  
> “height가 중요한 거야, BMI가 중요한 거야?”

결과적으로 coefficient, 즉 회귀계수가 불안정해질 수 있습니다.

예를 들어:

```text
모델 1:
income coefficient = 2.3
tax_paid coefficient = 0.1

모델 2:
income coefficient = 0.4
tax_paid coefficient = 1.9
```

데이터를 조금만 바꿨는데 coefficient가 크게 바뀐다면 해석 가능성이 떨어집니다.

Feature selection을 통해 서로 강하게 상관된 feature 중 하나만 남기면 이런 문제를 줄일 수 있습니다.

예를 들어:

```text
height_cm, height_m 둘 중 하나만 남기기
income, tax_paid 중 예측력이 더 좋은 하나만 남기기
square_meter, pyeong 중 하나만 남기기
```

그래서 이 선택지도 맞습니다.

---

## ④ Increase cost related to deployment

> **배포 관련 비용을 증가시킨다.**

이건 일반적으로 **틀린 설명**입니다.

Feature selection은 보통 배포 비용을 **증가시키는 것이 아니라 감소시킵니다**.

왜냐하면 배포 환경에서는 feature 수가 적을수록 관리가 쉽기 때문입니다.

머신러닝 모델을 실제 서비스에 배포할 때는 단순히 모델 파일만 올리면 끝나는 게 아닙니다. 다음 요소들이 필요합니다.

```text
feature 수집
feature validation
feature preprocessing
feature transformation
feature store 관리
실시간 feature 생성
결측치 처리
schema drift 감지
데이터 파이프라인 유지보수
모델 입력 형식 관리
```

feature가 많을수록 이 모든 과정이 복잡해집니다.

예를 들어 실시간 대출 승인 모델이 있다고 해보겠습니다.

모델이 200개의 feature를 요구한다면, 서비스 시점에 그 200개 feature를 모두 가져와야 합니다.

```text
고객 기본정보 DB
거래 이력 DB
신용평가 API
외부 금융 API
로그 데이터
앱 행동 데이터
```

이렇게 여러 시스템에서 feature를 가져와야 하면 배포 시스템이 복잡해집니다.

반면 feature selection을 해서 feature를 200개에서 30개로 줄였다면:

```text
- 데이터 수집 비용 감소
- API 호출 비용 감소
- feature pipeline 단순화
- latency 감소
- 장애 가능성 감소
- monitoring 대상 감소
- 유지보수 비용 감소
```

즉 실제 프로덕션에서는 feature가 적은 모델이 훨씬 다루기 쉽습니다.

물론 예외는 있습니다. Feature selection 자체를 위한 추가 실험이나 분석 비용은 발생할 수 있습니다. 하지만 이 선택지는 보통 feature selection의 결과가 **deployment cost를 증가시킨다**고 말하고 있기 때문에 일반적인 설명으로는 틀립니다.

정리하면:

```text
Feature selection 과정에는 분석 비용이 들 수 있다.
하지만 feature selection 결과는 보통 배포 비용을 줄인다.
```

그래서 이 선택지는 정답으로 고르면 안 됩니다.

---

## ⑤ Mitigate overfitting

> **과적합을 완화한다.**

이것도 **맞는 설명**입니다.

Overfitting은 모델이 훈련 데이터의 일반적인 패턴이 아니라, 훈련 데이터에만 존재하는 잡음까지 외워버리는 현상입니다.

예를 들어 feature가 너무 많으면 모델은 다음과 같은 이상한 규칙을 학습할 수 있습니다.

```text
이름에 'A'가 들어가면 생존 확률이 높다
고객 ID 끝자리가 7이면 연체 가능성이 낮다
특정 zip code와 특정 가입일 조합이면 구매 가능성이 높다
```

훈련 데이터에서는 우연히 맞을 수 있습니다. 하지만 새로운 데이터에서는 성능이 떨어집니다.

Feature 수가 많을수록 모델이 선택할 수 있는 “가짜 패턴”의 경우의 수가 늘어납니다.

특히 샘플 수에 비해 feature 수가 많을 때 위험합니다.

```text
샘플 500개, feature 10개   → 상대적으로 안정적
샘플 500개, feature 10,000개 → 과적합 위험 큼
```

이 문제는 텍스트 분류, 유전체 데이터, 이미지 feature, 로그 데이터, one-hot encoding이 많은 tabular 데이터에서 자주 나타납니다.

Feature selection은 불필요한 feature를 줄여서 모델의 자유도를 낮춥니다. 모델이 훈련 데이터를 외울 수 있는 여지를 줄이는 것입니다.

이건 regularization과도 연결됩니다.

```text
Feature selection: feature 자체를 제거
Regularization: feature는 남기되 weight를 작게 제한
```

둘 다 과적합을 줄이는 방향으로 작용합니다.

그래서 이 선택지도 맞습니다.

---

# 최종 정답

따라서 정답은 다음과 같습니다.

```text
✅ Reduce noise by only keeping useful features
✅ Reduce data processing time
✅ Reduce collinearity from highly correlated features
❌ Increase cost related to deployment
✅ Mitigate overfitting
```

즉 **4개가 맞고, 1개가 틀립니다.**

---

# 시험식으로 기억하는 방법

Feature selection의 핵심 효과는 이렇게 외우면 좋습니다.

```text
좋은 feature만 남긴다
→ 노이즈 감소
→ 계산량 감소
→ 상관성 높은 중복 feature 감소
→ 과적합 감소
→ 배포/운영 복잡도 감소
```

반대로 이런 표현이 나오면 조심해야 합니다.

```text
Increase cost
Increase complexity
Increase noise
Increase overfitting
Increase processing time
```

Feature selection은 보통 이런 것들을 **증가시키는 것이 아니라 감소시키는 방향**입니다.

---

# 실무자 관점에서 한 줄 요약

15년차 리서처 관점에서 보면 feature selection은 단순한 전처리 기법이 아니라, **모델의 일반화 성능, 해석 가능성, 학습 효율, 추론 latency, 운영 안정성을 동시에 개선할 수 있는 모델링 전략**입니다.

그래서 이 문제에서 “Increase cost related to deployment”만 빼고 나머지는 모두 feature selection의 장점으로 보는 게 맞습니다.

---
