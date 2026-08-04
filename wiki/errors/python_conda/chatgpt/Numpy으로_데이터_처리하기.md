---
type: Error Note
title: "Numpy으로 데이터 처리하기"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2023-10-24)"
tags: [errors, chatgpt-export]
timestamp: 2023-10-24
status: active
---

# Numpy으로 데이터 처리하기

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-10-24

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
아래는 주어진 과제에 대한 Python 코드 예제입니다. 코드는 numpy를 사용하여 데이터를 처리하고 원하는 작업을 수행합니다.

```python
import numpy as np
import pandas as pd

# mars_base_main_parts-001.csv, mars_base_main_parts-002.csv, mars_base_main_parts-003.csv 파일 읽기
arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',', skip_header=1)
arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',', skip_header=1)
arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',', skip_header=1)

# 3개의 배열 합치기
parts = np.concatenate((arr1, arr2, arr3))

# 각 항목의 평균값 구하기
mean_values = np.mean(parts, axis=0)

# 평균값이 50보다 작은 값을 뽑아내서 parts_to_work_on.csv 파일로 저장
selected_parts = parts[mean_values < 50]
pd.DataFrame(selected_parts).to_csv('parts_to_work_on.csv', header=False, index=False)

# 보너스 과제: parts_to_work_on.csv 파일 읽기
parts2 = np.genfromtxt('parts_to_work_on.csv', delimiter=',')

# 전치행렬 계산 및 출력
parts3 = parts2.T
print(parts3)
```

이 코드를 실행하면 주어진 CSV 파일을 numpy 배열로 읽어들이고, 배열을 합치고 각 항목의 평균값을 구한 후, 평균값이 50 미만인 항목을 선택하여 "parts_to_work_on.csv" 파일로 저장합니다. 보너스 과제로 "parts_to_work_on.csv" 파일을 읽어서 전치행렬을 계산하고 출력합니다.

---

### ❓ 질문 (User)
제약사항


· Python에서 기본 제공되는 명령어만 사용해야 하며 별도의 라이브러리나 패키지를 사용해서는 안된다.

· numpy는 추가로 사용 할 수 있다.

· 파일로 저장하는 부분에는 반드시 예외처리가 되어 있어야 한다.

### 💡 답변 (Assistant)
아래는 Python의 기본 제공 명령어와 numpy만을 사용하여 주어진 제약 사항을 준수하도록 수정한 코드입니다. 파일 저장 부분에는 파일 예외처리가 포함되어 있습니다.

```python
import numpy as np

try:
    # mars_base_main_parts-001.csv, mars_base_main_parts-002.csv, mars_base_main_parts-003.csv 파일 읽기
    arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',', skip_header=1)
    arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',', skip_header=1)
    arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',', skip_header=1)

    # 3개의 배열 합치기
    parts = np.concatenate((arr1, arr2, arr3))

    # 각 항목의 평균값 구하기
    mean_values = np.mean(parts, axis=0)

    # 평균값이 50보다 작은 값을 뽑아내서 parts_to_work_on.csv 파일로 저장
    selected_parts = parts[mean_values < 50]
    np.savetxt('parts_to_work_on.csv', selected_parts, delimiter=',')
    
    # 보너스 과제: parts_to_work_on.csv 파일 읽기
    parts2 = np.genfromtxt('parts_to_work_on.csv', delimiter=',')

    # 전치행렬 계산
    parts3 = parts2.T

    # parts3 출력
    print(parts3)

except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except Exception as e:
    print("오류 발생:", e)
```

이 코드는 주어진 제약 사항을 준수하며 파일 저장 부분에 파일 예외처리를 추가하였습니다.

---

### ❓ 질문 (User)
parts,strength
Concrete,36
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

csv 파일 내 데이터가 이건데 1, 2, 3 csv 파일 모두 parts열은 동일하고 strength 만 달라 
어떻게 처리해야 할까?

### 💡 답변 (Assistant)
주어진 데이터가 3개의 CSV 파일에 있는데, "parts" 열은 동일하고 "strength" 열만 다른 데이터를 포함하고 있다는 것을 이해했습니다. 이러한 경우, 먼저 각 파일을 읽어서 numpy 배열로 변환한 다음, 각 파일의 "strength" 값을 분리하고 하나의 배열로 합칠 수 있습니다.

다음은 이를 수행하는 Python 코드의 예제입니다.

```python
import numpy as np

# 파일에서 데이터 읽어오기
def read_csv(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=1)
    parts = data[:, 0]
    strength = data[:, 1].astype(int)
    return parts, strength

# 3개의 CSV 파일에서 데이터 읽기
parts1, strength1 = read_csv('mars_base_main_parts-001.csv')
parts2, strength2 = read_csv('mars_base_main_parts-002.csv')
parts3, strength3 = read_csv('mars_base_main_parts-003.csv')

# "parts" 열은 동일하므로 하나의 배열로 합치기
all_parts = np.concatenate((parts1, parts2, parts3))

# "strength" 값을 하나의 배열로 합치기
all_strength = np.concatenate((strength1, strength2, strength3))

# 필요한 작업 수행
# 이 부분에서 원하는 작업을 수행할 수 있습니다.

# 예를 들어, "strength"가 50 이상인 부분을 선택하는 경우:
selected_parts = all_parts[all_strength >= 50]

# 선택된 "parts" 및 "strength"를 출력 또는 다른 처리에 사용할 수 있습니다.
print(selected_parts)

# 필요한 추가 작업 수행 가능

# "parts" 및 "strength"를 다시 저장하거나 다른 연산을 수행할 수 있습니다.
```

이 코드는 3개의 CSV 파일에서 "parts" 열을 합쳐 하나의 배열로 만들고, "strength" 열도 합쳐서 하나의 배열로 만든 후, 필요한 작업을 수행하고 나머지 데이터 처리를 수행하는 예제입니다.

---

### ❓ 질문 (User)
내가 한 질문을 종합해서 코드로 짜줄래?

### 💡 답변 (Assistant)
물론, 아래는 주어진 데이터를 종합하여 처리하는 Python 코드입니다. 이 코드는 3개의 CSV 파일에서 "parts" 열을 합치고, "strength" 열을 각각 분리한 다음 원하는 작업을 수행합니다.

```python
import numpy as np

# 파일에서 데이터 읽어오기
def read_csv(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=1)
    parts = data[:, 0]
    strength = data[:, 1].astype(int)
    return parts, strength

# 3개의 CSV 파일에서 데이터 읽기
parts1, strength1 = read_csv('mars_base_main_parts-001.csv')
parts2, strength2 = read_csv('mars_base_main_parts-002.csv')
parts3, strength3 = read_csv('mars_base_main_parts-003.csv')

# "parts" 열은 동일하므로 하나의 배열로 합치기
all_parts = np.concatenate((parts1, parts2, parts3))

# "strength" 값을 하나의 배열로 합치기
all_strength = np.concatenate((strength1, strength2, strength3))

# 필요한 작업 수행
# 이 부분에서 원하는 작업을 수행할 수 있습니다.

# 예를 들어, "strength"가 50 이상인 부분을 선택하는 경우:
selected_parts = all_parts[all_strength >= 50]

# 선택된 "parts" 및 "strength"를 출력 또는 다른 처리에 사용할 수 있습니다.
print(selected_parts)

# 필요한 추가 작업 수행 가능

# "parts" 및 "strength"를 다시 저장하거나 다른 연산을 수행할 수 있습니다.
```

이 코드는 주어진 제약 사항에 따라 데이터를 처리하며, "parts"와 "strength"를 적절하게 다룹니다. 필요에 따라 코드를 수정하여 추가 작업을 수행할 수 있습니다.

---

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

제약사항


· Python에서 기본 제공되는 명령어만 사용해야 하며 별도의 라이브러리나 패키지를 사용해서는 안된다.

· numpy는 추가로 사용 할 수 있다.

· 파일로 저장하는 부분에는 반드시 예외처리가 되어 있어야 한다.

parts,strength
Concrete,36
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

csv 파일 내 데이터가 이건데 1, 2, 3 csv 파일 모두 parts열은 동일하고 strength 만 달라 
어떻게 처리해야 할까?

### 💡 답변 (Assistant)
주어진 요구사항과 제약 사항을 만족시키기 위해 Python과 numpy를 사용하여 데이터를 처리하는 코드를 작성해보겠습니다. 주어진 CSV 파일들의 "parts" 열은 동일하며, "strength" 열만 다른 데이터를 포함하고 있습니다.

```python
import numpy as np

# 파일에서 데이터 읽어오기
def read_csv(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=1)
    parts = data[:, 0]
    strength = data[:, 1].astype(int)
    return parts, strength

try:
    # 3개의 CSV 파일에서 데이터 읽기
    parts1, strength1 = read_csv('mars_base_main_parts-001.csv')
    parts2, strength2 = read_csv('mars_base_main_parts-002.csv')
    parts3, strength3 = read_csv('mars_base_main_parts-003.csv')

    # "parts" 열은 동일하므로 하나의 배열로 합치기
    all_parts = np.concatenate((parts1, parts2, parts3))

    # "strength" 값을 하나의 배열로 합치기
    all_strength = np.concatenate((strength1, strength2, strength3))

    # 평균값이 50 미만인 "parts" 선택
    selected_parts = all_parts[all_strength < 50]

    # 선택된 "parts"를 파일로 저장
    with open('parts_to_work_on.csv', 'w') as file:
        file.write("parts\n")
        for part in selected_parts:
            file.write(f"{part}\n")

    # 보너스 과제: parts_to_work_on.csv 파일 읽어서 전치행렬 계산
    selected_data = np.genfromtxt('parts_to_work_on.csv', delimiter=',', dtype=str, skip_header=1)
    parts2 = selected_data[:, 0]
    parts3 = parts2.T

    # 전치행렬 내용 출력
    print(parts3)

except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except Exception as e:
    print("오류 발생:", e)
```

이 코드는 주어진 제약 사항을 준수하며, "parts"와 "strength"를 적절하게 다룹니다. 필요한 작업을 수행한 후, "parts_to_work_on.csv" 파일에 약한 부분의 "parts"를 저장하고, 보너스 과제로 "parts_to_work_on.csv" 파일을 읽어 전치행렬을 계산하고 출력합니다.

---

### ❓ 질문 (User)
배열을 새로 만들어야 겠어
strength 1,2,3 에서 각 위치에 해당하는 수들을 뽑은 다음 배열로 만들어서 0번 배열에 3개의 숫자, 1번 배열에 3개의 숫자 ... 총 100개의 배열을 각각의 3개의 숫자로 이루어지게 만들려고 해 그리고 해당하는 인덱스는 parts1,2,3 모두 동일하기 때문에 3개 중 하나를 쓰고 싶어 
해당하는 코드 짜줄 수 있어?

### 💡 답변 (Assistant)
이해했습니다. 주어진 CSV 파일에서 "strength"를 각 위치에 해당하는 숫자로 뽑아서 3개의 숫자로 이루어진 배열을 만들고, 해당 인덱스를 모두 공유하려는 것이 맞습니다. 다음은 그렇게 처리하는 코드입니다.

```python
import numpy as np

# 파일에서 데이터 읽어오기
def read_csv_strength(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=int, skip_header=1)
    return data

try:
    # 3개의 CSV 파일에서 "strength" 읽기
    strength1 = read_csv_strength('mars_base_main_parts-001.csv')
    strength2 = read_csv_strength('mars_base_main_parts-002.csv')
    strength3 = read_csv_strength('mars_base_main_parts-003.csv')

    # "strength" 배열을 3개씩 합치기
    all_strength = np.column_stack((strength1, strength2, strength3))

    # all_strength 배열에서 각 위치에 해당하는 3개의 숫자로 이루어진 배열들을 추출
    selected_strengths = [all_strength[:, i] for i in range(all_strength.shape[1])]

    # 선택된 3개의 숫자로 이루어진 배열들 출력
    for i, selected_strength in enumerate(selected_strengths):
        print(f"Selected Strength {i + 1}:")
        print(selected_strength)

except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except Exception as e:
    print("오류 발생:", e)
```

이 코드는 "strength"를 각 위치에 해당하는 숫자로 뽑아서 3개의 숫자로 이루어진 배열로 만든 후, 3개의 숫자로 이루어진 배열들을 출력합니다.

---

### ❓ 질문 (User)
selected_strengths = [all_strength[:, i] for i in range(all_strength.shape[1])]
이건 무슨 의미야?

### 💡 답변 (Assistant)
`selected_strengths`는 주어진 `all_strength` 배열에서 3개의 숫자로 이루어진 배열들을 선택한 리스트입니다. 코드에서 이 부분은 리스트 컴프리헨션을 사용하여 구성됩니다. 각 요소 `i`는 `all_strength` 배열의 열을 나타냅니다.

구체적으로, `all_strength.shape[1]`은 `all_strength` 배열의 열의 개수를 나타내며, 이 경우 3개의 숫자로 이루어진 배열이므로 3입니다. 그리고 `for i in range(all_strength.shape[1])`는 `i`가 0부터 2까지 반복하도록 합니다.

따라서 `selected_strengths` 리스트에는 `all_strength` 배열의 열을 나타내는 3개의 배열이 저장됩니다. 이러한 배열은 `strength1`, `strength2`, 및 `strength3`에서 가져온 데이터의 위치에 해당합니다.

---

### ❓ 질문 (User)
그럼 여기서 나는 all_strength를 가지고 각 list 별로 나누어진 수의 평균을 내고 싶어 그러면 총 100개의 배열 내의 3개의 숫자가 총 100개의 배열 내에 평균 숫자 1개로 나타내어 지는 코드를 얻고 싶어

### 💡 답변 (Assistant)
이해했습니다. 각 리스트의 숫자들을 평균 내고, 3개의 숫자가 하나의 평균 숫자로 대체되어야 합니다. 다음은 그렇게 하는 코드입니다:

```python
import numpy as np

# 파일에서 데이터 읽어오기
def read_csv_strength(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=int, skip_header=1)
    return data

try:
    # 3개의 CSV 파일에서 "strength" 읽기
    strength1 = read_csv_strength('mars_base_main_parts-001.csv')
    strength2 = read_csv_strength('mars_base_main_parts-002.csv')
    strength3 = read_csv_strength('mars_base_main_parts-003.csv')

    # "strength" 배열을 3개씩 합치기
    all_strength = np.column_stack((strength1, strength2, strength3))

    # 각 리스트의 숫자들을 평균 내고, 3개의 숫자가 하나의 평균 숫자로 대체하기
    averaged_strengths = np.mean(all_strength, axis=1)

    # 평균 숫자로 이루어진 배열들 출력
    for i, averaged_strength in enumerate(averaged_strengths):
        print(f"Average Strength {i + 1}: {averaged_strength}")

except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except Exception as e:
    print("오류 발생:", e)
```

이 코드는 각 리스트의 숫자들을 평균 내고, 3개의 숫자가 하나의 평균 숫자로 대체되는 방식으로 작동합니다. 출력에는 100개의 평균 숫자가 나타납니다.

---

### ❓ 질문 (User)
axis = 1의 의미를 알고 싶어

### 💡 답변 (Assistant)
`axis=1`은 numpy 배열에서 연산을 수행할 때 열(column) 방향을 나타냅니다. 이것은 배열의 각 행(row)에 대해 연산을 수행하라는 의미입니다.

예를 들어, `np.mean(array, axis=1)`는 주어진 `array`의 각 행의 평균을 계산하라는 의미입니다. 결과는 각 행에 대한 하나의 평균값이 들어있는 배열이 됩니다. 열 방향으로 평균을 구하려면 `axis=0`을 사용하면 됩니다.

간단한 예시를 통해 설명하겠습니다:

```python
import numpy as np

array = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# 각 행의 평균 (axis=1을 사용)
row_means = np.mean(array, axis=1)
print("행별 평균:", row_means)

# 각 열의 평균 (axis=0을 사용)
column_means = np.mean(array, axis=0)
print("열별 평균:", column_means)
```

이 코드에서 `axis=1`을 사용하여 각 행의 평균을 구하고, `axis=0`을 사용하여 각 열의 평균을 구합니다.

---

### ❓ 질문 (User)
혹시 저 np.arr에서 소수점 3자리 까지만 표현할 수 없어?

### 💡 답변 (Assistant)
네, numpy의 배열에서 특정 소수점 자릿수까지만 표현하려면 출력 형식을 지정해야 합니다. 이를 위해 `np.set_printoptions` 함수를 사용하여 배열의 출력 형식을 지정할 수 있습니다.

예를 들어, 소수점 3자리까지만 표현하고 싶다면 다음과 같이 설정할 수 있습니다:

```python
import numpy as np

# 배열 생성
array = np.array([[1.234567, 2.345678, 3.456789],
                  [4.567890, 5.678901, 6.789012],
                  [7.890123, 8.901234, 9.012345]])

# 출력 형식 설정 (소수점 3자리까지)
np.set_printoptions(precision=3)

# 배열 출력
print(array)
```

이렇게 하면 배열의 출력이 소수점 3자리까지만 나타납니다. `np.set_printoptions`를 사용하면 numpy 배열 출력의 형식을 사용자 지정할 수 있습니다.

---

### ❓ 질문 (User)
지금 문제가 평균 강도가 50 미만인 parts들을 구하고, 그 수치 까지 구했는데 이를 csv 파일로 작성하려고 해. 
내가 원하는 포맷은 parts, strength 가 첫줄에 나오고
이하로 parts 열은 selected_parts , strength 열은 selected_strength 가 쓰여지게 하고싶어

### 💡 답변 (Assistant)
이해했습니다. 원하는 포맷으로 CSV 파일을 작성하려면 다음과 같이 코드를 수정할 수 있습니다:

```python
import numpy as np

# 파일에서 데이터 읽어오기
def read_csv_strength(filename):
    data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=1)
    return data

try:
    # 3개의 CSV 파일에서 "strength" 읽기
    strength1 = read_csv_strength('mars_base_main_parts-001.csv')
    strength2 = read_csv_strength('mars_base_main_parts-002.csv')
    strength3 = read_csv_strength('mars_base_main_parts-003.csv')

    # "strength" 배열을 3개씩 합치기
    all_strength = np.column_stack((strength1, strength2, strength3))

    # 각 리스트의 숫자들을 평균 내고, 3개의 숫자가 하나의 평균 숫자로 대체하기
    averaged_strengths = np.mean(all_strength, axis=1)

    # 평균 숫자로 이루어진 배열들을 selected_strength로 변경
    selected_strength = averaged_strengths

    # 평균 강도가 50 미만인 "parts" 선택
    selected_parts = np.array([parts for i, parts in enumerate(all_parts) if selected_strength[i] < 50])

    # CSV 파일로 저장
    with open('selected_parts_and_strength.csv', 'w') as file:
        file.write("parts,selected_strength\n")
        for i in range(len(selected_parts)):
            file.write(f"{selected_parts[i]},{selected_strength[i]}\n")

except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except Exception as e:
    print("오류 발생:", e)
```

이 코드는 "selected_parts_and_strength.csv"라는 CSV 파일을 작성하고, 첫 줄에 "parts"와 "selected_strength"가 나타나도록 합니다. "selected_parts"와 "selected_strength" 배열을 사용하여 파일에 데이터를 작성합니다.

---
