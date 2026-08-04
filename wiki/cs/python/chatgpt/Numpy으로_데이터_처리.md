---
type: Concept
title: "Numpy으로 데이터 처리"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2023-10-23)"
tags: [cs, chatgpt-export]
timestamp: 2023-10-23
status: active
---

# Numpy으로 데이터 처리

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-10-23

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
학습목표: Numpy



스토리


화성 기지의 돔을 복구하고 나니 그래도 한숨 돌릴 수 있게 되었다. 하지만 한송희 박사가 급하게 만들어서 올려둔 돔 구조로 인해서 화성 기지의 전체적인 구조 강도가 어떻게 바뀌었을지 궁금해졌다. 미션 컴퓨터 쿡북을 통해서 확인해 보니 화성 기지의 주요 부품들에 대한 데이터가 mars_base_main_parts-001.csv, mars_base_main_parts-002.csv, mars_base_main_parts-003.csv 파일에 저장되어 있는 것을 확인했다. 이 파일들의 내용을 분석하고 약한 부분들을 보강하는 작업이 필요했다.


수행과제


· numpy를 사용하기 위해서 import를 한다.

· mars_base_main_parts-001.csv,
  mars_base_main_parts-002.csv,
  mars_base_main_parts-003.csv 파일들을
  모두 numpy를 사용해서 읽어들여서 각각 arr1, arr2, arr3 과 같이 ndarray 타입으로 가져온다.

· 3개의 배열을 하나로 합치고(merge) 이름을 parts 라는 ndarray 를 생성한다.

· parts를 이용해서 각 항목의 평균값을 구한다.

· 평균값이 50 보다 작은 값을 뽑아내서 parts_to_work_on.csv 라는 파일로 별도로 저장한다.


보너스 과제


· parts_to_work_on.csv를 읽어서 parts2라는 ndarray에 저장한다.

· parts2의 내용을 기반으로 전치행렬을 구하고 그 내용을 parts3에 저장하고 출력한다.

### 💡 답변 (Assistant)
아래는 주어진 과제에 따른 Python 코드 예제입니다. 주어진 스토리와 수행과제에 따라 코드를 구성했습니다.

```python
import numpy as np
import csv

# mars_base_main_parts-001.csv, mars_base_main_parts-002.csv, mars_base_main_parts-003.csv 파일을 읽어서 ndarray로 가져옵니다.
arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',')
arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',')
arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',')

# 3개의 배열을 하나로 합칩니다.
parts = np.concatenate((arr1, arr2, arr3))

# parts 배열을 이용해서 각 항목의 평균값을 구합니다.
average_values = np.mean(parts, axis=0)

# 평균값이 50 미만인 행을 필터링합니다.
below_50 = parts[average_values < 50]

# 결과를 parts_to_work_on.csv 파일로 저장합니다.
np.savetxt('parts_to_work_on.csv', below_50, delimiter=',')

# 보너스 과제: parts_to_work_on.csv 파일을 읽어서 parts2에 저장하고 전치행렬을 생성합니다.
parts2 = np.genfromtxt('parts_to_work_on.csv', delimiter=',')
parts3 = parts2.T

# 전치행렬을 출력합니다.
print("전치행렬 (parts3):")
print(parts3)
```

위 코드를 실행하면 요구사항에 따라 데이터를 읽고 처리한 후, 평균값이 50 미만인 행을 필터링하여 `parts_to_work_on.csv` 파일로 저장하고, 보너스 과제로 전치행렬을 생성하여 출력할 것입니다.

---

### ❓ 질문 (User)
parts,strength
Concrete,36
Steel,45
Brick,71
Wood,11

csv파일 안의 데이터가 이런 형식이면 어떻게 데이터 처리 하는 것이 좋을까?

### 💡 답변 (Assistant)
주어진 데이터는 CSV 파일의 형식으로 구성되어 있고, 데이터에는 "parts"와 "strength"라는 두 개의 열이 있습니다. 이러한 데이터를 처리하기 위해 Python에서는 `csv` 모듈을 사용하여 CSV 파일을 읽고 데이터를 쉽게 처리할 수 있습니다.

먼저, CSV 파일을 읽어서 데이터를 처리하는 방법을 보여드리겠습니다. 예를 들어, 주어진 데이터를 읽어들이고 각 부품의 강도가 50보다 작은 부품을 필터링하려면 다음과 같이 할 수 있습니다:

```python
import csv

# CSV 파일을 읽어서 데이터를 저장할 리스트를 초기화합니다.
data = []

# CSV 파일을 열고 데이터를 읽어서 리스트에 저장합니다.
with open('data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# 데이터를 출력해 봅니다.
for row in data:
    print(f"Part: {row['parts']}, Strength: {int(row['strength'])}")

# 강도가 50보다 작은 부품을 필터링합니다.
weak_parts = [row for row in data if int(row['strength']) < 50]

# 필터링된 결과를 출력합니다.
print("\n강도가 50보다 작은 부품:")
for weak_part in weak_parts:
    print(f"Part: {weak_part['parts']}, Strength: {int(weak_part['strength'])}")
```

위 코드는 CSV 파일을 읽어서 데이터를 리스트에 저장하고, 그 중에서 강도가 50보다 작은 부품을 필터링하여 출력하는 예제입니다. 필요한 데이터 처리 작업에 따라 코드를 수정할 수 있습니다.

주의할 점은 CSV 파일의 구분자 (일반적으로 쉼표) 및 열 이름이 실제 데이터와 일치해야 한다는 것입니다.

---

### ❓ 질문 (User)
import csv 를 사용하지 않고 코드 짜줘

### 💡 답변 (Assistant)
CSV 파일을 사용하지 않고 순수한 Python 코드로 데이터 처리를 수행하려면 주어진 데이터를 직접 파싱하고 처리해야 합니다. 아래는 CSV 모듈을 사용하지 않고 주어진 데이터를 처리하는 예제 코드입니다:

```python
# 주어진 데이터를 문자열로 표현합니다.
data_str = """parts,strength
Concrete,36
Steel,45
Brick,71
Wood,11"""

# 데이터를 줄로 분할합니다.
lines = data_str.split('\n')

# 첫 번째 줄은 열 이름입니다.
header = lines[0].split(',')
data = []

# 데이터를 처리합니다.
for line in lines[1:]:
    parts, strength = line.split(',')
    data.append({'parts': parts, 'strength': int(strength)})

# 데이터를 출력합니다.
for row in data:
    print(f"Part: {row['parts']}, Strength: {row['strength']}")

# 강도가 50보다 작은 부품을 필터링합니다.
weak_parts = [row for row in data if row['strength'] < 50]

# 필터링된 결과를 출력합니다.
print("\n강도가 50보다 작은 부품:")
for weak_part in weak_parts:
    print(f"Part: {weak_part['parts']}, Strength: {weak_part['strength']}")
```

이 코드는 CSV 파일을 직접 파싱하여 데이터를 처리하고, 강도가 50보다 작은 부품을 필터링하는 예제입니다. 이렇게 순수한 Python 코드를 사용하여 데이터 처리를 수행할 수 있습니다.

---

### ❓ 질문 (User)
· mars_base_main_parts-001.csv,
  mars_base_main_parts-002.csv,
  mars_base_main_parts-003.csv 파일들을
  모두 numpy를 사용해서 읽어들여서 각각 arr1, arr2, arr3 과 같이 ndarray 타입으로 가져온다.
이 부분이 이해가 잘 가지 않아

### 💡 답변 (Assistant)
아래는 주어진 요구사항에 따라 주어진 CSV 파일들을 NumPy 배열로 읽어오는 과정을 설명한 코드입니다. 주어진 요구사항대로 코드를 이해하기 위해 간단한 설명을 추가하겠습니다.

1. `mars_base_main_parts-001.csv`, `mars_base_main_parts-002.csv`, `mars_base_main_parts-003.csv` 파일을 모두 읽어 NumPy 배열로 가져오는 작업을 수행합니다.

```python
import numpy as np

# CSV 파일을 NumPy 배열로 읽어옵니다.
arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',')
arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',')
arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',')
```

여기서 `np.genfromtxt` 함수를 사용하여 CSV 파일을 NumPy 배열로 읽어옵니다. `delimiter=','`는 파일의 데이터가 쉼표로 구분되어 있음을 나타냅니다.

이렇게 읽어온 `arr1`, `arr2`, `arr3`는 각각 CSV 파일의 데이터를 NumPy 배열로 저장한 것입니다. 이제 이 배열들을 조합하여 하나의 배열을 만들 수 있습니다.

---

### ❓ 질문 (User)
csv 파일 내 데이터는 
parts,strength
oncrete,36
Steel,45
Brick,71
Wood,11
Glass,32
Roofing,71
Insulation,96
Asphalt,81
Plaster,37
Insulation material,83
Rebar,35
Tile,100
Stone,37
Cement,3
Wallpaper,9
Ceiling material,25
Drywall,96
Non-ferrous metal,31
Aluminum,93
Steel frame,10
Plywood,76
PVC (Plastic),99
Wire,48
Soil,77
Steel frame structure,28
Asphalt shingles,63
Concrete blocks,26
Fiberglass,31
Fasteners,12
Metal mesh,34
Adhesive,84
Oil paint,92
Brick mortar,34
Iron railing,52
Door frame,99
Insulation crafts,50
Scaffolding,92
Concrete mixer,34
Ladder,57
Ceiling molding material,63
Rebar tie,51
Jackhammer,21
Ceiling grid,47
Scale,43
Window casing,18
Brickwork,50
Ceiling panel,60
Blinds,12
Corner bead,22
Joint compound,5
Wire mesh,61
Radiator,24
Rebar ceiling grid,59
Drywall screws,60
Hydraulic push,62
Door handle,67
Plumbing,27
Metal base,91
Wire cable,60
Block wall,88
Reinforced concrete block,22
Outlet box,41
Wooden ladder,35
Roof bumper,73
Steel roof truss,76
Meter box,91
Roofing,39
Gypsum base,8
Building paper,18
Countertop,9
Projection base,23
Exterior brick,12
Control point,85
Door frame,86
Building trim,3
Ceramic tile,8
Projection window,98
Hasp,27
Conduit box,73
Building tag,61
Vinyl flooring,30
Rebar drawing,64
Door stop,91
Rebar installation,66
Spray art,98
Faucet,13
Brick wall,83
Ironwork,85
Air filter,29
Scale,97
Slab,91
Cliff,58
Curtain wall,57
Roofing wave board,46
Vinyl ceiling,99
Tile joint material,44
Sink,100
Building frame,47
Ladder rack,58
Stair runner,49

이렇게 되어있는데 ndarray가 문자도 읽을 수 있을까?

### 💡 답변 (Assistant)
NumPy는 문자열을 포함한 다양한 데이터 유형을 처리할 수 있습니다. 주어진 CSV 파일의 데이터에 문자열 열이 포함되어 있는 경우, NumPy 배열은 해당 문자열 데이터를 처리할 수 있습니다.

주어진 데이터를 NumPy 배열로 읽어들이는 경우, 문자열 데이터는 해당 열의 데이터 유형이 문자열 (dtype='U')로 인식됩니다. 이를 통해 문자열 데이터를 NumPy 배열에 포함할 수 있으며 해당 데이터를 처리할 수 있습니다.

따라서 주어진 데이터를 NumPy 배열로 읽어올 때 문자열 데이터를 처리하는 데 문제가 없습니다. 이러한 NumPy 배열을 사용하여 문자열 데이터를 검색, 필터링 및 처리할 수 있습니다.

---

### ❓ 질문 (User)
그러면 이 경우에는 전부다 문자열로 받은 다음에 0번 열은 문자 그대로 두고 1번 열은 int든 float든 다시 받아야겠네

### 💡 답변 (Assistant)
네, 주어진 데이터를 읽을 때 문자열 데이터를 문자 그대로 유지하고 1번 열의 데이터는 정수 또는 부동 소수점 숫자로 변환하려면 다음과 같이 처리할 수 있습니다.

```python
import numpy as np

# CSV 파일을 읽어옵니다.
data = np.genfromtxt('your_file.csv', delimiter=',', dtype=[('parts', 'U50'), ('strength', float)], skip_header=1)

# data 배열에는 'parts' 열은 문자열, 'strength' 열은 숫자로 저장됩니다.
```

위 코드에서 `dtype` 매개변수를 사용하여 데이터 유형을 지정합니다. `'U50'`는 최대 50 문자로 된 문자열을 나타내고, `float`는 부동 소수점 숫자를 나타냅니다. 이렇게 하면 'parts' 열은 문자열로 유지되고, 'strength' 열은 숫자로 변환됩니다.

이제 `data` 배열에는 문자열과 숫자 데이터가 포함되어 있으며, 이를 효과적으로 처리할 수 있습니다.

---

### ❓ 질문 (User)
저 csv 파일 3개를 결합할껀데 0번 열은 동일한 parts들이라 1개만 남겨두고 나머지는 1번 열들만 합하는 식으로 하는게 낫겠지? 혹시 위의 요청에 대한 코드 짜줄 수 있어?

### 💡 답변 (Assistant)
네, 주어진 3개의 CSV 파일을 결합하되, 'parts' 열은 동일한 값만 남기고 1번 열들만 합치려면 다음과 같이 코드를 작성할 수 있습니다:

```python
import numpy as np

# CSV 파일들을 읽어서 NumPy 배열로 변환합니다.
arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',', dtype=[('parts', 'U50'), ('strength', float)], skip_header=1)
arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',', dtype=[('parts', 'U50'), ('strength', float)], skip_header=1)
arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',', dtype=[('parts', 'U50'), ('strength', float)], skip_header=1)

# 'parts' 열의 값을 중복 없이 추출합니다.
unique_parts = np.unique(np.concatenate((arr1['parts'], arr2['parts'], arr3['parts']))

# 중복된 'parts' 값을 가지지 않는 배열을 초기화합니다.
combined_data = np.zeros(unique_parts.size, dtype=[('parts', 'U50'), ('strength', float)])

# 'parts' 열의 값은 중복 없이 남기고, 1번 열을 합산합니다.
for i, part in enumerate(unique_parts):
    combined_data['parts'][i] = part
    combined_data['strength'][i] = np.sum(arr1['strength'][arr1['parts'] == part]) + \
                                 np.sum(arr2['strength'][arr2['parts'] == part]) + \
                                 np.sum(arr3['strength'][arr3['parts'] == part])

# 결과를 출력하거나 저장할 수 있습니다.
print(combined_data)
```

위 코드에서 `unique_parts`에는 중복 없이 나타나는 'parts' 값을 저장하고, 이 값을 기반으로 'parts' 값이 중복되지 않는 `combined_data` 배열을 만듭니다. 그런 다음 'strength' 값을 합산하여 중복 없이 남긴 'parts' 값을 가진 데이터를 생성합니다.

이렇게 하면 중복된 'parts' 값을 하나로 줄이고 1번 열들을 합산한 결과를 얻을 수 있습니다.

---

### ❓ 질문 (User)
먼저 np.concatenate로 결합하고 중복되는걸 unique로 날리는 식이지?

### 💡 답변 (Assistant)
네, 정확하게 말씀드린 것처럼 중복된 'parts' 값을 먼저 `np.concatenate`로 모든 데이터를 결합한 다음, `np.unique`를 사용하여 중복된 'parts' 값을 제거하는 방식을 사용할 수 있습니다. 이렇게 하면 중복된 'parts' 값이 하나로 줄어들고, 그에 따라 1번 열의 값을 합산하여 원하는 결과를 얻을 수 있습니다.

다음은 수정된 코드입니다:

```python
import numpy as np

# CSV 파일들을 읽어서 NumPy 배열로 변환합니다.
arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',', dtype=[('parts', 'U50'), ('strength', float)], skip_header=1)
arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',', dtype=[('parts', 'U50'), ('strength', float)], skip_header=1)
arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',', dtype=[('parts', 'U50'), ('strength', float)], skip_header=1)

# 모든 데이터를 하나로 결합합니다.
all_data = np.concatenate((arr1, arr2, arr3))

# 'parts' 열의 값을 중복 없이 추출합니다.
unique_parts = np.unique(all_data['parts'])

# 중복된 'parts' 값을 가지지 않는 배열을 초기화합니다.
combined_data = np.zeros(unique_parts.size, dtype=[('parts', 'U50'), ('strength', float)])

# 'parts' 열의 값은 중복 없이 남기고, 1번 열을 합산합니다.
for i, part in enumerate(unique_parts):
    combined_data['parts'][i] = part
    combined_data['strength'][i] = np.sum(all_data['strength'][all_data['parts'] == part])

# 결과를 출력하거나 저장할 수 있습니다.
print(combined_data)
```

이 코드는 데이터를 결합한 후 중복을 제거하여 중복 없이 남긴 'parts' 값을 가진 데이터를 생성합니다.

---
