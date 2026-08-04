---
type: Error Note
title: "Iris 원핫인코딩 방법"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-05-15)"
tags: [errors, chatgpt-export]
timestamp: 2026-05-15
status: active
---

# Iris 원핫인코딩 방법

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-15

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
iris 붓꽃 classifier 하려고 하는데 target 데이터를 원핫인코딩으로 하려고 하니까 0 1 2 로 되어있어서 쉽지가 않네. 하는 방법 좀 알려줘

### 💡 답변 (Assistant)
좋아요. Iris 붓꽃 데이터셋의 `target`은 보통 이렇게 되어 있죠.

```python
0 = setosa
1 = versicolor
2 = virginica
```

즉, 이미 **정수 라벨 encoding**이 되어 있는 상태입니다.  
여기서 원핫인코딩을 하면 다음처럼 바꾸면 됩니다.

```text
0 → [1, 0, 0]
1 → [0, 1, 0]
2 → [0, 0, 1]
```

---

## 1. pandas로 원핫인코딩하는 방법

```python
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()

X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target, name="target")

y_onehot = pd.get_dummies(y)

print(y.head())
print(y_onehot.head())
```

출력 예시는 대략 이렇게 나옵니다.

```python
0
0
0
0
0
Name: target, dtype: int64
```

```python
       0      1      2
0   True  False  False
1   True  False  False
2   True  False  False
3   True  False  False
4   True  False  False
```

정수형 `0, 1`로 보고 싶으면 이렇게 하면 됩니다.

```python
y_onehot = pd.get_dummies(y).astype(int)

print(y_onehot.head())
```

결과:

```python
   0  1  2
0  1  0  0
1  1  0  0
2  1  0  0
3  1  0  0
4  1  0  0
```

---

## 2. 컬럼명을 클래스 이름으로 바꾸기

`0, 1, 2`보다 실제 이름을 붙이면 더 보기 좋습니다.

```python
y_onehot = pd.get_dummies(y).astype(int)
y_onehot.columns = iris.target_names

print(y_onehot.head())
```

결과:

```python
   setosa  versicolor  virginica
0       1           0          0
1       1           0          0
2       1           0          0
3       1           0          0
4       1           0          0
```

---

## 3. sklearn의 OneHotEncoder 사용하기

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.datasets import load_iris

iris = load_iris()
y = iris.target.reshape(-1, 1)

encoder = OneHotEncoder(sparse_output=False)
y_onehot = encoder.fit_transform(y)

print(y_onehot[:5])
```

결과:

```python
[[1. 0. 0.]
 [1. 0. 0.]
 [1. 0. 0.]
 [1. 0. 0.]
 [1. 0. 0.]]
```

주의할 점은 `OneHotEncoder`는 입력을 2차원으로 받아야 해서,

```python
iris.target.reshape(-1, 1)
```

이렇게 바꿔줘야 합니다.

---

## 4. PyTorch에서 원핫인코딩하는 방법

PyTorch로 classifier를 만들 거면 이렇게 할 수 있습니다.

```python
import torch
import torch.nn.functional as F
from sklearn.datasets import load_iris

iris = load_iris()

y = torch.tensor(iris.target, dtype=torch.long)

y_onehot = F.one_hot(y, num_classes=3).float()

print(y[:5])
print(y_onehot[:5])
```

결과:

```python
tensor([0, 0, 0, 0, 0])
```

```python
tensor([[1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.]])
```

---

## 5. 그런데 중요한 점: PyTorch의 `CrossEntropyLoss`는 원핫인코딩이 필요 없습니다

Iris classifier를 PyTorch로 만든다면 보통 이렇게 씁니다.

```python
loss_fn = torch.nn.CrossEntropyLoss()
```

이 경우 정답 `y`는 원핫인코딩하면 안 됩니다.

즉, 정답은 이렇게 생겨야 합니다.

```python
tensor([0, 1, 2, 0, 1, 2])
```

모델 출력은 이렇게 생겨야 합니다.

```python
# shape: [batch_size, num_classes]
tensor([
    [2.1, 0.3, -1.2],
    [0.1, 1.8, 0.4],
    [-0.5, 0.2, 2.7]
])
```

`CrossEntropyLoss`는 내부적으로 다음을 같이 처리합니다.

```python
Softmax + Negative Log Likelihood Loss
```

그래서 모델 마지막에 `softmax`도 직접 붙이지 않는 경우가 많습니다.

---

## 6. 상황별 추천

### pandas / sklearn 연습용이면

```python
y_onehot = pd.get_dummies(iris.target).astype(int)
```

또는

```python
encoder = OneHotEncoder(sparse_output=False)
y_onehot = encoder.fit_transform(iris.target.reshape(-1, 1))
```

---

### PyTorch에서 `MSELoss` 같은 걸로 직접 비교하려면

```python
y_onehot = F.one_hot(y, num_classes=3).float()
```

---

### PyTorch에서 일반적인 다중분류 classifier를 만들 거면

원핫인코딩하지 말고 그대로 씁니다.

```python
y = torch.tensor(iris.target, dtype=torch.long)

loss_fn = torch.nn.CrossEntropyLoss()
```

이게 가장 정석입니다.

---

## 가장 추천하는 방식

Iris classifier를 PyTorch로 할 거라면 이렇게 가는 게 좋습니다.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import torch

iris = load_iris()

X = torch.tensor(iris.data, dtype=torch.float32)
y = torch.tensor(iris.target, dtype=torch.long)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(X_train.shape)
print(y_train.shape)
print(y_train[:10])
```

출력:

```python
torch.Size([120, 4])
torch.Size([120])
tensor([0, 2, 1, 1, 0, 2, ...])
```

그리고 loss는:

```python
loss_fn = torch.nn.CrossEntropyLoss()
```

정리하면:

```python
원핫인코딩이 꼭 필요한 상황 → F.one_hot 사용
일반적인 PyTorch 다중분류 → 원핫인코딩하지 말고 0, 1, 2 그대로 사용
```

Iris classifier에서는 **0, 1, 2 그대로 쓰는 방식이 더 자연스럽고 실무적으로도 맞는 방식**입니다.

---

### ❓ 질문 (User)
```
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch import nn, optim
from sklearn import datasets
from sklearn.model_selection import train_test_split
from Classifier_module import Classifier

iris = datasets.load_iris()

train_dataset = torch.FloatTensor(iris['data'])
test_dataset = torch.LongTensor(iris['target'])

# one-hot encoding
target_one_hot = F.one_hot(test_dataset)

# dataset_split
X_train, X_test, y_train, y_test = train_test_split(train_dataset, target_one_hot, test_size=0.2, random_state=42, shuffle=True)

model = Classifier(in_dim=4, out_dim=3, dim=1)
optimizer = optim.AdamW(model.parameters(), lr=1e-3)

n_epochs = 3000
for epoch in range(n_epochs + 1) :
    # 1. hypothesis (softmax)
    hx = model(X_train)

    # 2. Loss Func
    loss = F.cross_entropy(hx, y_train)

    # 3. gradient descent algorithm and update params
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch%100 == 0 :
        print(f"epoch : {epoch}, loss : {loss}")
```
```
import torch
from torch import nn, optim
import torch.nn.functional as F

class Classifier(nn.Module) :
    def __init__(self, in_dim, out_dim, dim) :
        r"""
        in_dim = input feature
        out_dim = output feature(Num. of class)
        dim = softmax : dim (0, 1) 0:row, 1:column
        """
        super().__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.dim = dim
        self.softmax = nn.Softmax(dim=dim)
        self.linear = nn.Linear(in_features=in_dim,
                                out_features=out_dim)
        
    def forward(self, x) :
        return self.softmax(self.linear(x))
    

```

TypeError: expected TensorOptions(dtype=float, device=cpu, layout=Strided, requires_grad=false (default), pinned_memory=false (default), memory_format=(nullopt)) (got TensorOptions(dtype=__int64, device=cpu, layout=Strided, requires_grad=false (default), pinned_memory=false (default), memory_format=(nullopt)))

### 💡 답변 (Assistant)
좋습니다. 지금 에러의 핵심은 **`F.cross_entropy()`에 넣는 `y_train`의 형태와 dtype이 맞지 않아서**입니다.

현재 코드 흐름은 이렇습니다.

```python
test_dataset = torch.LongTensor(iris['target'])

target_one_hot = F.one_hot(test_dataset)
```

이때 `target_one_hot`은 다음처럼 만들어집니다.

```python
tensor([[1, 0, 0],
        [1, 0, 0],
        ...
        [0, 0, 1]])
```

그런데 dtype은 `torch.int64`, 즉 `LongTensor`입니다.

```python
print(target_one_hot.dtype)
# torch.int64
```

반면 `F.cross_entropy()`는 보통 정답을 **원핫인코딩이 아닌 클래스 번호**로 받습니다.

```python
y_train = tensor([0, 1, 2, 0, 1, ...])
```

그래서 지금은 원핫인코딩을 하지 않는 게 정석입니다.

---

# 가장 좋은 수정 방법

## 1. 원핫인코딩 제거

이 부분을:

```python
test_dataset = torch.LongTensor(iris['target'])

# one-hot encoding
target_one_hot = F.one_hot(test_dataset)
```

이렇게 바꾸세요.

```python
target_dataset = torch.LongTensor(iris['target'])
```

그리고 `train_test_split`도 이렇게 바꿉니다.

```python
X_train, X_test, y_train, y_test = train_test_split(
    train_dataset,
    target_dataset,
    test_size=0.2,
    random_state=42,
    shuffle=True
)
```

---

## 2. 모델에서 Softmax 제거

현재 모델은 이렇게 되어 있습니다.

```python
def forward(self, x) :
    return self.softmax(self.linear(x))
```

그런데 `F.cross_entropy()`는 내부적으로 이미 다음 처리를 포함합니다.

```text
LogSoftmax + NLLLoss
```

그래서 모델 출력에는 `softmax`를 직접 적용하면 안 됩니다.

모델을 이렇게 바꾸세요.

```python
import torch
from torch import nn

class Classifier(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.linear = nn.Linear(in_features=in_dim, out_features=out_dim)

    def forward(self, x):
        return self.linear(x)
```

즉, 모델은 각 클래스에 대한 **logit 점수**만 출력하면 됩니다.

---

# 전체 수정 코드

## `Classifier_module.py`

```python
import torch
from torch import nn

class Classifier(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.linear = nn.Linear(in_features=in_dim, out_features=out_dim)

    def forward(self, x):
        return self.linear(x)
```

---

## 학습 코드

```python
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch import nn, optim
from sklearn import datasets
from sklearn.model_selection import train_test_split
from Classifier_module import Classifier

iris = datasets.load_iris()

# X: 입력 데이터
X = torch.FloatTensor(iris['data'])

# y: 정답 라벨, 원핫인코딩 하지 않음
y = torch.LongTensor(iris['target'])

# dataset split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    shuffle=True,
    stratify=y
)

model = Classifier(in_dim=4, out_dim=3)
optimizer = optim.AdamW(model.parameters(), lr=1e-3)

n_epochs = 3000

for epoch in range(n_epochs + 1):
    # 1. hypothesis
    logits = model(X_train)

    # 2. loss
    loss = F.cross_entropy(logits, y_train)

    # 3. update
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"epoch : {epoch}, loss : {loss.item():.6f}")
```

---

# 예측할 때는 Softmax를 써도 됩니다

학습할 때는 `softmax`를 빼야 하지만, 예측 확률을 보고 싶을 때는 사용해도 됩니다.

```python
with torch.no_grad():
    logits = model(X_test)
    probs = F.softmax(logits, dim=1)
    preds = torch.argmax(probs, dim=1)

print(preds)
print(y_test)
```

정확도 계산은 이렇게 합니다.

```python
acc = (preds == y_test).float().mean()
print(f"accuracy: {acc.item():.4f}")
```

---

# 핵심 정리

지금 코드에서 고쳐야 할 점은 2개입니다.

```python
target_one_hot = F.one_hot(test_dataset)
```

이걸 쓰지 말고:

```python
y = torch.LongTensor(iris['target'])
```

그대로 쓰세요.

그리고 모델의 마지막 출력에서:

```python
return self.softmax(self.linear(x))
```

이걸 쓰지 말고:

```python
return self.linear(x)
```

로 바꾸세요.

즉, `CrossEntropyLoss` 계열을 쓸 때는:

```text
모델 출력: softmax 없는 logits
정답 y: 원핫인코딩 없는 클래스 번호 0, 1, 2
```

이 조합이 정석입니다.

---

### ❓ 질문 (User)
그러면 classifier 하기 위해서 softmax 를 써야된다고 할 때, 너가 생각하는 코드를 작성해줘

### 💡 답변 (Assistant)
좋아요. **“classifier니까 softmax를 쓰고 싶다”**는 생각은 맞습니다.  
다만 정확히 나누면 이렇게 됩니다.

```text
학습할 때:
Linear 출력 logits → CrossEntropyLoss

예측할 때:
logits → softmax → class probability
```

즉, **softmax는 classifier에서 필요하지만, 보통 loss 계산 직전에는 직접 쓰지 않습니다.**  
그래도 “softmax를 명시적으로 쓰는 코드”를 원한다면 아래처럼 작성할 수 있습니다.

---

# 1. 추천 코드: 학습은 logits, 예측에서 softmax 사용

이 방식이 PyTorch 다중분류의 정석입니다.

## `Classifier_module.py`

```python
import torch
from torch import nn


class Classifier(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()

        self.linear = nn.Linear(
            in_features=in_dim,
            out_features=out_dim
        )

    def forward(self, x):
        # softmax를 적용하지 않은 raw score
        # 이것을 logits라고 부름
        logits = self.linear(x)
        return logits

    def predict_proba(self, x):
        # 예측 확률이 필요할 때만 softmax 사용
        logits = self.forward(x)
        probs = torch.softmax(logits, dim=1)
        return probs

    def predict(self, x):
        # 가장 확률이 높은 class 선택
        probs = self.predict_proba(x)
        preds = torch.argmax(probs, dim=1)
        return preds
```

---

## 학습 코드

```python
import torch
import torch.nn.functional as F
from torch import optim
from sklearn import datasets
from sklearn.model_selection import train_test_split
from Classifier_module import Classifier


iris = datasets.load_iris()

# input data
X = torch.FloatTensor(iris.data)

# target label: 0, 1, 2 그대로 사용
y = torch.LongTensor(iris.target)

# train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    shuffle=True,
    stratify=y
)

model = Classifier(in_dim=4, out_dim=3)
optimizer = optim.AdamW(model.parameters(), lr=1e-3)

n_epochs = 3000

for epoch in range(n_epochs + 1):
    # 1. forward
    logits = model(X_train)

    # 2. loss
    # cross_entropy 내부에 log_softmax가 포함되어 있음
    loss = F.cross_entropy(logits, y_train)

    # 3. update
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"epoch: {epoch}, loss: {loss.item():.6f}")
```

---

## 예측 코드

```python
with torch.no_grad():
    probs = model.predict_proba(X_test)
    preds = model.predict(X_test)

print("예측 확률:")
print(probs[:5])

print("예측 class:")
print(preds[:5])

print("실제 class:")
print(y_test[:5])

accuracy = (preds == y_test).float().mean()
print(f"accuracy: {accuracy.item():.4f}")
```

예측 확률은 이런 느낌입니다.

```text
tensor([[0.0021, 0.1432, 0.8547],
        [0.9712, 0.0281, 0.0007],
        [0.0114, 0.8195, 0.1691]])
```

여기서 각 행의 합은 거의 `1`입니다.

```python
print(probs.sum(dim=1))
```

결과:

```text
tensor([1.0000, 1.0000, 1.0000, ...])
```

---

# 2. “나는 forward 안에서 softmax를 꼭 쓰고 싶다”면

가능은 합니다.  
대신 이 경우에는 `F.cross_entropy()`를 그대로 쓰면 안 됩니다.

왜냐하면 `F.cross_entropy()`는 내부에서 이미 `log_softmax`를 적용하기 때문입니다.

```text
F.cross_entropy(logits, y)
= log_softmax(logits) + NLLLoss
```

그런데 모델에서 이미 softmax를 해버리면:

```text
softmax 결과 → 다시 cross_entropy에 입력
```

이 되어 학습이 이상해질 수 있습니다.

그래도 softmax를 모델 안에 넣고 싶다면, loss를 직접 만들어야 합니다.

---

## softmax를 forward에 넣는 버전

```python
import torch
from torch import nn


class Classifier(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()

        self.linear = nn.Linear(
            in_features=in_dim,
            out_features=out_dim
        )

    def forward(self, x):
        logits = self.linear(x)
        probs = torch.softmax(logits, dim=1)
        return probs
```

---

## 원핫인코딩 + 직접 cross entropy 계산

```python
import torch
import torch.nn.functional as F
from torch import optim
from sklearn import datasets
from sklearn.model_selection import train_test_split
from Classifier_module import Classifier


iris = datasets.load_iris()

X = torch.FloatTensor(iris.data)
y = torch.LongTensor(iris.target)

# one-hot encoding
y_one_hot = F.one_hot(y, num_classes=3).float()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_one_hot,
    test_size=0.2,
    random_state=42,
    shuffle=True,
    stratify=y
)

model = Classifier(in_dim=4, out_dim=3)
optimizer = optim.AdamW(model.parameters(), lr=1e-3)

n_epochs = 3000
eps = 1e-8

for epoch in range(n_epochs + 1):
    # 1. forward
    probs = model(X_train)

    # 2. manual cross entropy
    loss = -torch.mean(torch.sum(y_train * torch.log(probs + eps), dim=1))

    # 3. update
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"epoch: {epoch}, loss: {loss.item():.6f}")
```

---

## 이 버전에서 예측하기

```python
with torch.no_grad():
    probs = model(X_test)
    preds = torch.argmax(probs, dim=1)

    y_test_label = torch.argmax(y_test, dim=1)

accuracy = (preds == y_test_label).float().mean()

print("예측 확률:")
print(probs[:5])

print("예측 class:")
print(preds[:5])

print("실제 class:")
print(y_test_label[:5])

print(f"accuracy: {accuracy.item():.4f}")
```

---

# 둘 중 뭐가 더 좋냐?

실전에서는 **1번 방식**을 추천합니다.

```python
logits = model(X_train)
loss = F.cross_entropy(logits, y_train)
```

그리고 softmax는 예측할 때만 씁니다.

```python
probs = torch.softmax(logits, dim=1)
preds = torch.argmax(probs, dim=1)
```

---

# 최종적으로 추천하는 구조

```text
입력 X
 ↓
Linear
 ↓
logits
 ↓
CrossEntropyLoss로 학습
 ↓
예측할 때만 softmax
 ↓
argmax로 class 결정
```

즉, classifier에서 softmax의 위치는 보통 여기입니다.

```python
# 학습
logits = model(X_train)
loss = F.cross_entropy(logits, y_train)

# 예측
probs = torch.softmax(logits, dim=1)
preds = torch.argmax(probs, dim=1)
```

정리하면:

```text
classifier라서 softmax를 쓰는 것은 맞다.
하지만 학습 loss에 넣기 전이 아니라, 예측 확률을 해석할 때 쓰는 것이 정석이다.
```

---
