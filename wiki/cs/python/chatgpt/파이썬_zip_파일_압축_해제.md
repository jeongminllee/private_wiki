---
type: Concept
title: "파이썬 zip 파일 압축 해제"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2024-10-04)"
tags: [cs, chatgpt-export]
timestamp: 2024-10-04
status: active
---

# 파이썬 zip 파일 압축 해제

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2024-10-04

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
zip 파일 푸는 파이썬 코드 작성해줘

### 💡 답변 (Assistant)
여기 zip 파일을 푸는 파이썬 코드를 작성해 드릴게요. 먼저 zipfile 모듈을 사용하여 압축을 풀 수 있습니다:

```python
import zipfile
import os

def unzip_file(zip_path, extract_to):
    # 폴더가 없으면 생성
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    
    # zip 파일 열기
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Files extracted to: {extract_to}")

# 사용 예시
zip_path = 'example.zip'  # 압축 파일 경로
extract_to = 'extracted_files'  # 파일을 추출할 폴더
unzip_file(zip_path, extract_to)
```

### 설명:
1. `zipfile.ZipFile`: zip 파일을 열기 위한 클래스입니다.
2. `extractall()`: zip 파일 내 모든 파일을 지정된 폴더로 추출하는 메소드입니다.
3. `os.makedirs()`: 추출할 폴더가 없으면 새로 생성합니다.

이 코드를 사용하여 zip 파일을 지정된 경로에 풀 수 있습니다.

---
