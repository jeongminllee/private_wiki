---
type: Concept
title: "PDF 부분 추출 방법"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2025-06-30)"
tags: [cs, chatgpt-export]
timestamp: 2025-06-30
status: active
---

# PDF 부분 추출 방법

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-06-30

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
pdf 파일에서 내가 필요로 하는 부분만 새파일로 만들고싶어.

### 💡 답변 (Assistant)
물론 가능합니다! PDF 파일에서 필요한 부분만 추출해 새 파일로 만드는 방법에는 다음 두 가지 주요 방법이 있습니다:

---

### ✅ 1. **직접 범위 지정해서 추출하기 (페이지 수로 지정)**

예를 들어, 1~3페이지와 7페이지만 새 파일로 만들고 싶다면:

#### 💻 Python 코드 사용 예시 (PyPDF2 또는 PyPDF 라이브러리)
```python
from PyPDF2 import PdfReader, PdfWriter

# 원본 PDF 파일 열기
reader = PdfReader("원본파일.pdf")
writer = PdfWriter()

# 필요한 페이지 추가 (0부터 시작하므로 1페이지는 0번 인덱스)
for i in [0, 1, 2, 6]:  # 1~3페이지 + 7페이지
    writer.add_page(reader.pages[i])

# 새 파일로 저장
with open("새파일.pdf", "wb") as f:
    writer.write(f)
```

---

### ✅ 2. **키워드나 특정 문단을 기준으로 추출하고 싶다면**

이 경우는 텍스트 분석이 필요하기 때문에, 먼저 PDF 텍스트를 추출한 후 필요한 내용만 필터링해서 새 PDF로 만드는 방식이 적합합니다.

#### 예시: 특정 키워드가 포함된 페이지만 추출
```python
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("원본파일.pdf")
writer = PdfWriter()

keyword = "원하는 키워드"

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text and keyword in text:
        writer.add_page(page)

with open("키워드_포함_페이지.pdf", "wb") as f:
    writer.write(f)
```

---

### ✅ 3. **간편하게 할 수 있는 툴 추천 (코딩 없이)**

- **SmallPDF**: https://smallpdf.com/kr/split-pdf  
- **ILovePDF**: https://www.ilovepdf.com/ko/split_pdf  
  → 원하는 페이지만 선택해서 새 PDF로 저장 가능

---

### 📌 제가 도와드릴 수 있는 방법
1. PDF 파일을 업로드해주시면,
2. **필요한 부분이 어떤 기준인지** (페이지 번호 / 키워드 / 제목 등) 알려주시면,
3. 바로 새 PDF로 만들어드릴 수 있어요.

필요하시면 파일을 올려주세요!

---

### ❓ 질문 (User)
이 파일에서 가장 마지막 장과 그 이전 장만 추출해줘

### 💡 답변 (Assistant)
PDF 파일에서 **마지막 2페이지**를 추출하여 새 파일로 만들었습니다. 아래 링크에서 다운로드하실 수 있습니다:

👉 [마지막 2장 추출 PDF 다운로드](sandbox:/mnt/data/맞막_2장_추출.pdf)  

더 필요한 작업이 있으면 알려주세요!

---
