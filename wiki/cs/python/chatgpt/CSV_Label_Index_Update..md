---
type: Concept
title: "CSV Label Index Update."
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2023-07-21)"
tags: [cs, chatgpt-export]
timestamp: 2023-07-21
status: active
---

# CSV Label Index Update.

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-07-21

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
각 다른 2개의 csv 파일에 'label' 인덱스가 같다면,  한 csv 파일의 'label'값을 다른 csv 파일의 'index' 인덱스로 바꿔주는 python 코드 짜줘

### 💡 답변 (Assistant)
두 개의 CSV 파일을 읽어서 'label' 인덱스가 같다면 한 CSV 파일의 'label' 값을 다른 CSV 파일의 'index' 인덱스로 바꿔주는 Python 코드를 아래와 같이 작성할 수 있습니다. 이 코드는 Pandas 라이브러리를 사용하여 데이터를 처리합니다.

```python
import pandas as pd

def update_labels(csv_file1, csv_file2):
    # CSV 파일 1 읽기
    df1 = pd.read_csv(csv_file1)

    # CSV 파일 2 읽기
    df2 = pd.read_csv(csv_file2)

    # 'label' 인덱스가 같은 행을 찾아서 'index' 값을 업데이트
    for index, row in df1.iterrows():
        label_value = row['label']
        matching_row = df2.loc[df2['label'] == label_value]
        if not matching_row.empty:
            df1.at[index, 'label'] = matching_row['index'].values[0]

    # 변경된 'label' 값을 가진 CSV 파일 1을 다시 저장
    df1.to_csv(csv_file1, index=False)

# 사용 예시
csv_file1 = 'file1.csv'
csv_file2 = 'file2.csv'
update_labels(csv_file1, csv_file2)
```

이 코드는 두 개의 CSV 파일을 불러온 후에, 첫 번째 파일의 'label' 값이 두 번째 파일의 'label' 값과 일치하는 경우에만 해당 값을 두 번째 파일의 'index' 값으로 바꿉니다. 그 후, 첫 번째 CSV 파일을 변경된 'label' 값으로 저장합니다. 이 때, 두 번째 파일에 일치하는 'label' 값이 없는 경우 해당 'label' 값을 그대로 유지하게 됩니다.

---

### ❓ 질문 (User)
위 코드에서 'label' 인덱스를 'index'로 변경하지 말고 df1 의 3번째 행으로 추가하는 python 코드로 알려줘

### 💡 답변 (Assistant)
두 개의 CSV 파일을 읽어서 'label' 인덱스가 같다면 한 CSV 파일의 'label' 값을 다른 CSV 파일의 세 번째 행으로 추가하는 Python 코드를 아래와 같이 작성할 수 있습니다. 이 코드도 Pandas 라이브러리를 사용하여 데이터를 처리합니다.

```python
import pandas as pd

def update_labels(csv_file1, csv_file2):
    # CSV 파일 1 읽기
    df1 = pd.read_csv(csv_file1)

    # CSV 파일 2 읽기
    df2 = pd.read_csv(csv_file2)

    # 'label' 인덱스가 같은 행을 찾아서 'label' 값을 CSV 파일 2의 세 번째 열로 추가
    for index, row in df1.iterrows():
        label_value = row['label']
        matching_row = df2.loc[df2['label'] == label_value]
        if not matching_row.empty:
            df1.at[index, 'new_column'] = matching_row['label'].values[0]

    # 변경된 'label' 값을 가진 CSV 파일 1을 다시 저장
    df1.to_csv(csv_file1, index=False)

# 사용 예시
csv_file1 = 'file1.csv'
csv_file2 = 'file2.csv'
update_labels(csv_file1, csv_file2)
```

위 코드에서는 'label' 값이 일치하는 경우, CSV 파일 1의 각 행에 'new_column'이라는 새로운 열을 추가하고, 해당 열에 CSV 파일 2에서 해당하는 'label' 값을 넣어줍니다. 이렇게 하면 'label' 인덱스를 'index'로 변경하는 대신, 새로운 열에 값을 추가할 수 있게 됩니다.

---
