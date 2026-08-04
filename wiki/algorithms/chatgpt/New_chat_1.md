---
type: Concept
title: "New chat"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-09-08)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-09-08
status: active
---

# New chat

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-09-08

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
너는 15년차 데이터 사이언티스트야. 주니어인 나에게 데이터 사이언티스트가 되기 위해 교육하려고 해. 구체적인 커리큘럼과 스케줄링을 작성해줘.

### 💡 답변 (Assistant)
좋아, 주니어에서 “프로 일 잘하는 데이터 사이언티스트”로 성장하는 걸 목표로 18주(≈4.5개월) 커리큘럼과 주간 스케줄을 짜줄게.  
두 가지 모드(파트타임 10–12h/주, 풀타임 25–30h/주) 중 상황에 맞게 고르면 돼. 내용은 같고, 투입 시간만 달라져.

# 로드맵 한눈에 보기
- **Phase 0 (1주)**: 환경 세팅 & 기초 체력 측정  
- **Phase 1 (3주)**: 필수 기초 — Python/SQL, 통계·확률, 데이터핸들링·시각화  
- **Phase 2 (4주)**: 머신러닝 핵심 — 지도/비지도, 특성공학, 모델링·평가·성능개선  
- **Phase 3 (3주)**: MLOps 실무화 — 실험관리, 데이터/모델 버저닝, API/배포, 리포팅  
- **Phase 4 (4주)**: 딥러닝·NLP·LLM — PyTorch, 임베딩·트랜스포머, RAG, 작은 파인튜닝  
- **Phase 5 (3주)**: 캡스톤 & 취업준비 — 3개 포트폴리오, 면접준비, 도메인 특화

---

## 주간 스케줄 템플릿
- **파트타임(10–12h/주)**: 월·수·금 각 2h (학습/실습), 주말 4–6h(프로젝트)  
- **풀타임(25–30h/주)**: 월~금 하루 4–5h (이론·실습), 주말 5–8h(프로젝트 정리)

> 매주 산출물: **짧은 리포트(1p) + 깃허브 커밋 + 미니 실험결과(W&B/MLflow)**

---

# 18주 상세 커리큘럼

## Phase 0 — 스타트(1주)
**목표:** 도구 세팅과 현재 레벨 점검  
- 환경: `conda`/`uv` 중 택1, VS Code, Git, pre-commit(black/ruff), Docker 기본  
- 데이터 스택: Python 3.11+, pandas/polars, numpy, matplotlib/plotly, scikit-learn  
- 계정: Kaggle, W&B(또는 MLflow 로컬), HuggingFace  
- **진단 과제:**  
  1) Pandas 100제 중 20문항 풀이  
  2) SQL 10문항(SELECT/JOIN/GROUP BY/HAVING/윈도우)  
  3) 통계 미니퀴즈(평균·분산·신뢰구간·가설검정 개념)

---

## Phase 1 — 필수 기초(3주)

**Week 1: Python & SQL 집중**
- Python: 자료구조, 함수형(람다/컴프리헨션), OOP, 예외, 파일/환경변수  
- SQL: INNER/LEFT JOIN, 윈도우 함수(ROW_NUMBER, SUM OVER), 서브쿼리  
- 미니프로젝트: **판매데이터 EDA & SQL 리포트** (질문→SQL→시각화→인사이트 5개)

**Week 2: 통계·확률 for DS**
- 분포(정규/베르누이/포아송), 표본추출, 점추정·구간추정, A/B 테스트(검정력·효과크기)  
- 평가지표의 통계적 해석(정밀도/재현율/ROC-AUC의 분산 감각)  
- 실습: **가설검정 시뮬레이션**(부트스트랩, 퍼뮤테이션 테스트)

**Week 3: 데이터핸들링 & 시각화**
- pandas/polars 비교, 결측·이상치·타입정리 파이프라인, 피처 스토어 개념 맛보기  
- 시각화: 스토리텔링 그래프(라인/바/히트맵/상자), 대시보드 초입(streamlit/plotly)  
- 미니프로젝트: **제품/고객 코호트 분석 대시보드(최소 기능)**

---

## Phase 2 — 머신러닝 핵심(4주)

**Week 4: 지도학습 I**
- 전처리 파이프라인, 데이터 누수 방지, KFold/StratifiedKFold  
- 선형/로지스틱, 정규화(L1/L2), 트리·랜덤포레스트·XGBoost 기초  
- 실습: **분류 태스크 베이스라인→튜닝→SHAP 해석**

**Week 5: 지도학습 II**
- 불균형 데이터(SMOTE, 조정된 손실), 임계값 조정, 비용민감학습  
- 회귀 성능향상: 타깃 인코딩, 카테고리 처리, 교차검증 구조화  
- 과제: **리그레이션 리더보드 챌린지(로컬 점수표)**

**Week 6: 비지도 & 특성공학**
- KMeans/DBSCAN, 차원축소(PCA/UMAP), 이상치 탐지(Isolation Forest)  
- 피처 상호작용/빈 카운트/타깃 스태킹 실험 설계  
- 미니프로젝트: **이상거래 탐지 PoC** (PR-AUC 기준)

**Week 7: 모델 해석 & 성능개선**
- 전역/국부 해석(SHAP/Permutation), 파셜디펜던스, 카운터팩추얼  
- 에러분해(바이어스·분산·노이즈), 언더/오버피팅 트레이드오프  
- 리포트: **모델카드+데이터카드** 작성

---

## Phase 3 — MLOps 실무화(3주)

**Week 8: 실험·버저닝·데이터 라인리지**
- W&B/MLflow 실험트래킹, DVC/ Git-LFS로 데이터/모델 버저닝  
- 재현가능 파이프라인(폴더 구조, config 관리, 시드 고정)  
- 실습: **동일 실험 재현 가이드** 만들어 팀원도 재현 가능하게

**Week 9: 서비스화**
- FastAPI로 예측 API, 입력 검증(pydantic), 로깅/모니터링(간단)  
- Docker 컨테이너화, 유닛테스트(pytest), 간단한 CI(GitHub Actions)  
- 배포: Render/Fly.io/EC2 중 택1로 스테이징

**Week 10: 비즈 리포팅 & 실험설계**
- 메트릭 스펙(“정의서”) 작성, A/B 테스트 설계(샘플사이즈, 기간, 위험관리)  
- 주간 리포트 템플릿(문제정의→가설→분석→인사이트→액션)  
- 과제: **가상의 기능 롤아웃 A/B 계획서 2p**

---

## Phase 4 — 딥러닝·NLP·LLM(4주)

**Week 11: PyTorch 기본기**
- 텐서/오토그라드, Dataset/DataLoader, 학습루프, 스케줄러·정규화  
- 실습: **탭/이미지 중 택1 베이스라인 네트워크 학습**

**Week 12: NLP 기초**
- 토크나이징, 전처리, 임베딩(word2vec/fastText 개념), RNN vs CNN vs Transformer  
- 실습: **감성분석/주제분류 베이스라인(sklearn→PyTorch)**

**Week 13: 트랜스포머·LLM 실무**
- 토크나이저/어텐션 마스크, 지식형 임베딩, LoRA/PEFT 미세튜닝 개요  
- **RAG 파이프라인:** 문서로더→청크→임베딩→벡터DB→리트리버→생성→평가  
- 실습: **경량 LLM + RAG 미니앱(Streamlit)**

**Week 14: LLM 평가·안전·운영**
- 답변평가(metric·rubric·pairwise), 프롬프트 안정화, 금칙어/PII 필터  
- 관측가능성(쿼리/지식드리프트), 비용·지연 최적화  
- 리포트: **RAG 시스템 설계 문서(2–3p)**

---

## Phase 5 — 캡스톤 & 취업준비(3주)

**Week 15–17: 3개 캡스톤(포트폴리오 완성)**
1) **비즈니스 대시보드 프로젝트**  
   - 예: 리테일/마케팅 코호트·LTV·전환 퍼널 대시보드  
   - 산출물: Streamlit 대시보드, 쿼리/ETL 스크립트, 인사이트 문서(2p)

2) **ML 서비스 프로젝트**  
   - 예: 이탈예측/대출리스크/수요예측 중 택1  
   - 산출물: 학습 파이프라인, 모델카드, FastAPI+Docker, 재현 가이드

3) **NLP/LLM 프로젝트 (RAG 또는 소형 튜닝)**  
   - 예: 링크 요약·검색 비서, 고객문의 요약·카테고리 분류  
   - 산출물: RAG 파이프라인, 오프라인 평가셋, 에러 카탈로그

**취업준비 패키지**
- **이력서/링크드인/깃허브 정비**: 각 프로젝트 1단락 요약(문제·접근·영향)  
- **인터뷰 대비**:  
  - **DS**: 통계/실험/제품 케이스, SQL 라이브코딩  
  - **ML**: 모델링/피처링/리스크·데이터누수, 코드리뷰  
  - **MLOps**: 파이프라인, 배포, 모니터링 시나리오  
- **모의 인터뷰 2회**: 분석 케이스 → 화이트보드 → 5분 발표

---

# 주간 체크리스트(공통)
- [ ] 최소 1개 PR + 코드리뷰 노트  
- [ ] W&B/MLflow에 이번주 실험 2개 이상 기록  
- [ ] 미니 리포트(핵심 인사이트 3개 + 다음주 액션) 1p  
- [ ] 노트 정리·개념 카드(Anki) 10장

---

## 데이터셋·과제 가이드(안전한 공개 데이터)
- 분류: UCI Adult, Telco Churn, Credit default  
- 회귀: Kaggle House Prices(Ames), NYC Taxi fare  
- 비지도/이상치: 신용카드 이상거래, KDD Cup 99(전처리 주의)  
- NLP: IMDB/AG News, 허깅페이스 SQuAD-like(요약/질의응답)  
- RAG: 본인이 관심 있는 도메인의 문서(논문/매뉴얼/FAQ)를 자체 코퍼스로

---

## 코드·품질 기준
- 폴더 구조: `src/`, `data/`, `models/`, `notebooks/`, `configs/`, `tests/`  
- 설정 분리(.yaml), 시드 고정, 데이터 누수 체크리스트  
- 테스트: 데이터 로더, 전처리 함수, 지표 계산 유닛테스트  
- 문서화: README(재현 단계), 모델카드/데이터카드, 릴리즈 노트

---

## 평가 루브릭(요약)
- **문제정의·가설(20%)**: 비즈니스/과학적 질문이 명확한가  
- **데이터·피처(20%)**: 전처리 일관성, 데이터누수 방지, 피처 품질  
- **모델링·평가(25%)**: 적절한 지표, CV 설계, 에러분석·해석  
- **재현·배포(20%)**: 버저닝, 테스트, API/Docker, 간단 모니터링  
- **커뮤니케이션(15%)**: 리포트/발표, 인사이트→액션으로 연결

---

## 시간표 예시

### 파트타임(10–12h/주)
- **월(2h)**: 이론 학습 + 개념노트  
- **수(2h)**: 실습(노트북/과제)  
- **금(2h)**: 코딩/SQL 문제 풀이 + 미니실험  
- **토(4–6h)**: 프로젝트 진척, 리포트 작성, 깃 PR

### 풀타임(25–30h/주)
- **월–목(하루 4h)**: 이론 1h → 실습 2h → 정리 1h  
- **금(4–5h)**: 주간 통합실험/리뷰/리포트  
- **주말(5–8h)**: 프로젝트 스프린트 & 문서화

---

## 너에게 맞춘 보너스 트랙(선택)
- **NLP 라인 심화**: 토큰화/서브워드, 벡터DB(FAISS/Chroma), 랭킹(RR@k/NDCG), 오프라인 평가셋 설계  
- **실험/비즈 제품분석**: 코호트·LTV·마케팅 믹스 기초, KPI 정의서 작성  
- **도메인 특화**(목재·가구/제조): 공정·품질 데이터 EDA, 이상치·예지보전 PoC

---

## 시작 전 체크리스트
1) Python 3.11+ 환경 생성 및 핵심 라이브러리 설치  
2) GitHub 공개 레포 하나 생성(캡스톤 전용)  
3) W&B 또는 MLflow 로컬 서버 준비(택1)  
4) Kaggle 계정 연동(토큰 저장)  
5) “학습 노트 템플릿” 만들기(개념·실험·결과·TODO)

---

원하면 위 로드맵을 **파트타임 버전 주간 캘린더** 또는 **풀타임 데일리 체크리스트**로 바로 뽑아줄게. 또한 1주차 과제로 사용할 **Python+SQL 진단 문제 세트**와 **리포트 템플릿(Markdown)**도 만들어 드릴 수 있어.

---

### ❓ 질문 (User)
나는 풀타임을 원해. 풀타임 데일리 체크리스트를 뽑아주고 1주차 과제 바로 만들어줘

### 💡 답변 (Assistant)
좋아! 풀타임 기준으로 **매일 뭘 하면 되는지(데일리 체크리스트)**와 **1주차 과제(즉시 진행 가능)**를 한 번에 드릴게. 그대로 따라가면 이번 주 금요일에 “작게 만들어 제대로 끝내는” 첫 산출물이 나온다.

---

# 풀타임 데일리 체크리스트 (공통, 월–금)

**시작 루틴 (15m)**
- 오늘의 1대 목표(One thing) 적기 → 캘린더 블록(4~5h) 확정
- 이슈/PR/실험 로그(W&B/MLflow) 미리 열어두기

**학습 블록 (60–90m)**
- 교재/문서 1개 챕터 + 핵심 개념 5개 요약(노트/Anki 5장)
- 오늘 과제에 바로 쓰일 개념만 집요하게

**실습 블록 (120m)**
- 오늘 목표 기능 1개 완성(데이터 로딩→처리→검증)
- 도중 30분 타임박스: 막히면 로그 남기고 우회

**품질 블록 (30–45m)**
- 코드 포맷/린트/타입체크(black/ruff/mypy) + 간단 테스트(pytest)
- 결과/그래프 캡처 저장, 리드미(근거/수식/결정) 5줄 추가

**결과 정리 (30m)**
- 실험 1건 이상 기록(W&B/MLflow): 파라미터/지표/샘플그래프
- 커밋 1회 + PR(제목: 오늘의 1대 목표, 본문: 변화점/지표/리스크)

**마감 루틴 (15m)**
- 내일 1대 목표 예약 + 할 일 3개만 남기기

> 주 3회(화·목·금) 30m: **SQL/알고리즘 문제 2문항**  
> 주 2회(수·금) 30m: **짧은 글쓰기(리포트/모델카드 항목 1개)**

---

# 1주차 일정 (Phase 1 / Week 1: Python & SQL 집중)

## 월요일 — 환경 세팅 & Python 워밍업
- Conda(or uv), VS Code, Git/GitHub, pre-commit(black/ruff), pytest 세팅
- **Python 과제 A-1**: 파이썬 기초 10제(리스트·딕트·컴프리헨션·파일 I/O)
- 산출물: `setup_log.md`, `tests/` 통과 스크린샷, 첫 커밋/PR

## 화요일 — Pandas/데이터핸들링
- 결측/이상치/타입정리 파이프라인(체크리스트화)
- **Python 과제 A-2**: 판매 데이터 집계(그룹바이, 피벗, KPI 3개)
- 산출물: `notebooks/01_pandas_basics.ipynb`, `src/etl.py`

## 수요일 — SQL 기본(SELECT/JOIN/GROUP BY/HAVING)
- 제공 스키마(`ecommerce`)로 **SQL 진단 1–6번**
- 산출물: `sql/diagnostic_01_06.sql` + 결과 스크린샷

## 목요일 — SQL 중급(CTE/윈도우/Top-N/러닝토탈)
- **SQL 진단 7–12번** + 해설 주석
- 산출물: `sql/diagnostic_07_12.sql`

## 금요일 — 미니프로젝트(EDA & SQL 리포트 1p)
- 문제정의→질문목록→SQL→그래프 2개→인사이트 3개→다음 액션 2개
- 산출물: `reports/week1_sales_report.md`(1p) + `figs/` 이미지 2개
- PR 제목 예: `[W1] Sales EDA & SQL Mini-Report`

## 주말(선택)
- 코드 리팩토링, README 보완, 실험 로그 정리, 체크리스트 회고

---

# 1주차 과제 (즉시 실행 가능)

## 0) 리포 구조(권장)
```
ds-bootcamp/
├─ data/              # (원천/중간/결과 데이터)
├─ notebooks/
├─ sql/
├─ src/
│  ├─ etl.py
│  ├─ metrics.py
│  └─ utils.py
├─ tests/
├─ reports/
├─ figs/
└─ README.md
```

---

## A. Python 과제 (A-1, A-2)

### A-1. 파이썬 기초 10제 (월)
1) 리스트에서 짝수만 제곱해 새 리스트 만들기(컴프리헨션)  
2) `dict`에서 값 기준 상위 3개 키 찾기  
3) 문자열에서 단어 빈도 Top-5(구두점 제거)  
4) 중첩리스트 평탄화(깊이 1, 2가지 방식)  
5) 파일 읽어 줄 수 세기(UTF-8-sig 고려)  
6) 제너레이터로 누적합 산출(yield)  
7) 데코레이터로 실행시간 측정  
8) 예외 안전 파일로딩 함수 만들기  
9) Enum/NamedTuple(or dataclass)로 상수/레코드 정의  
10) 작은 LRU 캐시 직접 구현(딕트+양방향 연결리스트 or `functools.lru_cache` 비교)

> 산출물: `notebooks/00_python_warmup.ipynb` (각 문항 셀/주석 설명)

### A-2. Pandas 집계 & KPI (화)
**입력**: `data/sales_sample.csv` (열: `order_id,order_date,customer_id,product_id,category,city,segment,quantity,unit_price,status`)  
**할 일**
- `load_and_clean(path) -> DataFrame`  
  - 날짜 파싱, 타입 캐스팅, 결측/이상치 규칙 3개 이상 명시
- `daily_sales(df) -> DataFrame`  
  - `status='delivered'`만 매출액(`quantity*unit_price`) 집계
- `sales_by_category(df)` / `top_k_customers(df,k=5)`  
- KPI 3개: 월 매출, 평균 주문금액(AOV), 재구매율(주문≥2 고객 비율)  
- (선택) PR-AUC 대신 간단한 퍼널(장바구니→결제완료 % 가정)

**평가**: 함수 독립성/타입 안정성, 주석/도큐스트링, 단위테스트 통과

**pytest 스켈레톤 예시**
```python
# tests/test_metrics.py
import pandas as pd
from src.etl import load_and_clean, sales_by_category, top_k_customers

def test_sales_by_category():
    df = pd.DataFrame({
        "category": ["A","A","B"],
        "quantity": [1,2,1],
        "unit_price": [100,200,300],
        "status": ["delivered","canceled","delivered"]
    })
    out = sales_by_category(df)
    assert "sales" in out.columns
    assert out.loc[out["category"]=="A","sales"].item() == 100
```

---

## B. SQL 진단 & 미니프로젝트

### B-0. 스키마 & 시드 데이터 (SQLite/MySQL 공통)
`sql/seed_ecommerce.sql`에 아래를 저장해 실행하세요.

```sql
-- 테이블
CREATE TABLE customers(
  customer_id INTEGER PRIMARY KEY,
  name TEXT, signup_date DATE, city TEXT, segment TEXT
);
CREATE TABLE products(
  product_id INTEGER PRIMARY KEY,
  name TEXT, category TEXT, unit_price INTEGER
);
CREATE TABLE orders(
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER, order_date DATE, status TEXT,
  FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE order_items(
  order_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price INTEGER,
  FOREIGN KEY(order_id) REFERENCES orders(order_id),
  FOREIGN KEY(product_id) REFERENCES products(product_id)
);
CREATE TABLE payments(
  payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER, amount INTEGER, method TEXT,
  FOREIGN KEY(order_id) REFERENCES orders(order_id)
);

-- 고객
INSERT INTO customers VALUES
(1,'Kim Min','2024-11-03','Seoul','consumer'),
(2,'Park Ji','2025-01-15','Busan','consumer'),
(3,'Choi Sun','2025-02-20','Seoul','corporate'),
(4,'Lee Hana','2025-02-25','Daegu','consumer'),
(5,'Jung Woo','2025-03-05','Incheon','home office'),
(6,'Han Seo','2025-03-12','Seoul','corporate');

-- 제품
INSERT INTO products VALUES
(1,'Laptop','Electronics',1500000),
(2,'Mouse','Electronics',25000),
(3,'Keyboard','Electronics',45000),
(4,'Desk','Furniture',300000),
(5,'Chair','Furniture',120000),
(6,'Monitor','Electronics',320000),
(7,'Lamp','Home',40000),
(8,'Notebook','Stationery',3000);

-- 주문(12건)
INSERT INTO orders VALUES
(1,1,'2025-02-10','delivered'),
(2,2,'2025-02-14','delivered'),
(3,3,'2025-02-28','delivered'),
(4,1,'2025-03-02','delivered'),
(5,4,'2025-03-10','canceled'),
(6,5,'2025-03-15','delivered'),
(7,3,'2025-03-20','delivered'),
(8,6,'2025-04-01','delivered'),
(9,2,'2025-04-07','returned'),
(10,4,'2025-04-12','delivered'),
(11,1,'2025-04-20','delivered'),
(12,3,'2025-04-25','delivered');

-- 주문항목
INSERT INTO order_items VALUES
(1,1,1,1500000),(1,2,1,25000),
(2,4,1,300000),(2,5,4,120000),
(3,6,2,320000),
(4,3,1,45000),(4,7,2,40000),(4,8,10,3000),
(5,1,1,1500000),
(6,5,2,120000),(6,7,1,40000),
(7,1,1,1500000),(7,6,1,320000),
(8,4,1,300000),(8,2,2,25000),
(9,6,1,320000),
(10,5,2,120000),(10,3,1,45000),
(11,1,1,1500000),
(12,2,5,25000),(12,7,3,40000);

-- 결제(의도적으로 주문 8은 결제 누락)
INSERT INTO payments(order_id,amount,method) VALUES
(1,1525000,'card'),
(2,780000,'bank_transfer'),
(3,640000,'card'),
(4,155000,'card'),
(6,280000,'card'),
(7,1820000,'card'),
(10,285000,'card'),
(11,1500000,'card'),
(12,245000,'bank_transfer');
```

> **주의**: 매출/지표 계산은 `status='delivered'`만 포함하세요.

### B-1. SQL 진단 12문항 (수·목)
1) 전체 매출(₩)  
2) 2025-02~2025-04 월별 매출(YYYY-MM)  
3) 평균 주문금액(AOV)  
4) 고객 매출 Top-3 (이름/도시 포함)  
5) 카테고리별 매출과 매출 비중(%)  
6) 도시별 고객 수와 매출  
7) 재구매 고객 수/비율(주문≥2, delivered 기준)  
8) **윈도우**: 카테고리 내 제품별 매출과 순위(RANK)  
9) **러닝토탈**: 월별 누적 매출  
10) **반연결**: delivered인데 결제 레코드 없는 주문 (→ order_id=8)  
11) 주문이 하나도 없는 고객  
12) 고객별 가장 최근 주문(ROW_NUMBER로 1위만)

**힌트 스니펫**
```sql
-- 월별 매출
WITH d AS (
  SELECT strftime('%Y-%m', order_date) AS ym, 
         SUM(oi.quantity*oi.unit_price) AS sales
  FROM orders o 
  JOIN order_items oi USING(order_id)
  WHERE o.status='delivered'
  GROUP BY 1
)
SELECT * FROM d;

-- 카테고리 내 순위
SELECT p.category, p.name, 
       SUM(oi.quantity*oi.unit_price) AS sales,
       RANK() OVER(PARTITION BY p.category ORDER BY SUM(oi.quantity*oi.unit_price) DESC) AS rnk
FROM orders o 
JOIN order_items oi USING(order_id)
JOIN products p USING(product_id)
WHERE o.status='delivered'
GROUP BY 1,2;
```

### B-2. 미니프로젝트(금) — **Sales EDA & SQL 1pager**
- 비즈 질문 예시: “3~4월 매출 하락/상승 원인은?”, “도시·세그먼트별 차이는?”
- 최소 시각화 2개(월별 매출, 카테고리 파이/바)  
- 의사결정용 인사이트 3개 + 다음 액션 2개

---

## C. 리포트 템플릿 (Markdown, 1p)
```md
# Week1 Sales Mini-Report
## 1) 문제정의
- 이번 주 답하려는 질문 1문장

## 2) 데이터/방법
- 스키마 요약, 포함/제외(Delivered만), 주요 지표 정의

## 3) 핵심 결과
- [그래프1 캡션] 요약 문장 1개
- [그래프2 캡션] 요약 문장 1개
- 표/수치 1개(AOV, Top 고객 등)

## 4) 인사이트 → 액션
- 인사이트 3개(근거 링크: SQL 쿼리/셀)
- 다음 액션 2개(실험/대시보드/데이터 수집)

## 5) 한계/리스크
- 데이터 품질 가정, 누락/편향
```

---

## D. 제출 체크리스트 (금 오후)
- [ ] `sql/diagnostic_01_12.sql` (주석 포함)  
- [ ] `notebooks/01_pandas_basics.ipynb`  
- [ ] `reports/week1_sales_report.md` + `figs/` 2개  
- [ ] `README.md`에 재현 가이드(시드/환경/실행순서)  
- [ ] PR 1개(요약/지표/한계/다음주 계획)

---

## E. 평가 루브릭 (요약)
- **정확성(30%)**: SQL 결과/지표 산출의 정확도  
- **재현성(25%)**: 시드·환경·스크립트 실행 가이드  
- **품질(20%)**: 코드 스타일, 테스트, 폴더 구조  
- **분석력(15%)**: 그래프 해석→인사이트 명료성  
- **커뮤니케이션(10%)**: PR/리포트 요약의 설득력

---

필요하면 **BigQuery용 쿼리 호환 버전**(DATE_TRUNC/FORMAT_DATE 등)과 **Streamlit 대시보드 스캐폴드**까지 바로 만들어줄게. 지금은 이대로 시작해도 충분히 1주차 ‘완주’ 가능합니다.

---
