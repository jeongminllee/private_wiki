---
type: Concept
title: "Organize Files: JSON & JPG"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2023-08-08)"
tags: [cs, chatgpt-export]
timestamp: 2023-08-08
status: active
---

# Organize Files: JSON & JPG

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-08-08

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
json 파일과 jpg 파일들로 이루어진 폴더 안에 jpg 파일은 images 폴더로, json 파일은 labels 폴더로 이동하고, 만약 폴더들이 존재하지 않는다면, 생성하는 코드를 작성해줘

### 💡 답변 (Assistant)
아래는 Python을 사용하여 해당 작업을 수행하는 코드 예제입니다. 코드를 실행하기 전에 해당 작업을 수행하고자 하는 폴더 구조를 미리 확인하고, 코드를 실행하기 전에 필요한 라이브러리를 설치해야 할 수 있습니다.

```python
import os
import shutil

# 원본 폴더 경로 설정
source_folder = "원본_폴더_경로"

# 목표 폴더 경로 설정
target_folder = "목표_폴더_경로"

# images 폴더와 labels 폴더 생성
if not os.path.exists(os.path.join(target_folder, "images")):
    os.makedirs(os.path.join(target_folder, "images"))
if not os.path.exists(os.path.join(target_folder, "labels")):
    os.makedirs(os.path.join(target_folder, "labels"))

# 폴더 내 파일 이동
for filename in os.listdir(source_folder):
    if filename.endswith(".jpg"):
        source_file = os.path.join(source_folder, filename)
        target_file = os.path.join(target_folder, "images", filename)
        shutil.move(source_file, target_file)
    elif filename.endswith(".json"):
        source_file = os.path.join(source_folder, filename)
        target_file = os.path.join(target_folder, "labels", filename)
        shutil.move(source_file, target_file)

print("파일 이동 완료!")
```

위의 코드를 본인의 상황에 맞게 수정하여 사용하시면 됩니다. 주의해야 할 점은 반드시 파일 경로를 올바르게 설정하고, 이미지 파일이 ".jpg" 확장자로 끝나며 JSON 파일이 ".json" 확장자로 끝나야 한다는 점입니다. 코드를 실행하기 전에 원본 폴더와 목표 폴더의 경로를 정확히 지정하고, 데이터를 백업하거나 테스트 환경에서 먼저 실행해보는 것을 권장합니다.

---

### ❓ 질문 (User)
with open("./Website_Screenshots_Data/train/labels/_annotations.coco.json", 'r', encoding='utf-8') as f :
    json.loads()
loads() 괄호 안에 들어갈 인자 가르쳐줘

### 💡 답변 (Assistant)
`json.loads()` 함수는 JSON 형식의 문자열을 Python 객체로 변환하는 함수입니다. 해당 함수를 사용하여 JSON 파일을 Python 객체로 로드하려면 다음과 같이 코드를 작성할 수 있습니다:

```python
import json

file_path = "./Website_Screenshots_Data/train/labels/_annotations.coco.json"

with open(file_path, 'r', encoding='utf-8') as f:
    json_data = json.loads(f.read())

# json_data 이제 Python 객체로 로드되었습니다
```

위 코드에서 `file_path` 변수에는 JSON 파일의 경로가 들어가야 합니다. 그리고 `with open(...)` 블록 안에서 파일을 열고 `json.loads()` 함수를 호출하여 JSON 파일의 내용을 Python 객체로 변환합니다. 변환된 데이터는 `json_data` 변수에 저장됩니다.

참고: `json.loads()` 함수의 인자로는 JSON 형식의 문자열이 전달되어야 합니다. 따라서 `f.read()`를 사용하여 파일의 내용을 문자열로 읽어와야 합니다.

---
