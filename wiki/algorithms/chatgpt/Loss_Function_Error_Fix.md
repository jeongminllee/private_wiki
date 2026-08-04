---
type: Concept
title: "Loss Function Error Fix"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-05-12)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-05-12
status: active
---

# Loss Function Error Fix

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-12

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
에러 원인은 여기입니다.

```python
return loss.data
```

`loss.data`는 **autograd 그래프에서 loss를 떼어낸 Tensor**를 반환합니다.  
그래서 아래에서

```python
loss.backward()
```

를 호출하면, PyTorch 입장에서는 이 `loss`가 더 이상 `w`, `b`와 연결되어 있지 않기 때문에:

```text
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

가 발생합니다.

---

## 핵심 수정

### 기존 코드

```python
return loss.data
```

### 수정 코드

```python
return loss
```

그리고 `loss_fn()` 안에서 gradient를 초기화하는 것도 빼는 게 좋습니다.  
gradient 초기화는 이미 학습 루프 안에서 하고 있습니다.

```python
optimizer.zero_grad()
```

---

## 수정된 전체 코드

```python
import torch
import torch.optim as optim

# ==============
def sigmoid(x: torch.Tensor, w, b):
    return 1 / (1 + torch.exp(-(x @ w + b)))

def loss_fn(y_true, y_pred):
    """
    Binary Cross Entropy Loss 직접 구현
    y_pred = sigmoid(x @ w + b)
    """
    equation = -y_true * torch.log(y_pred) - (1 - y_true) * torch.log(1 - y_pred)
    loss = torch.mean(equation)
    return loss


# ==============
x_data = [[1, 2], [2, 3], [3, 1], [4, 3], [5, 3], [6, 2]]
y_data = [[0], [0], [0], [1], [1], [1]]

X_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)

w = torch.zeros((2, 1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

optimizer = optim.SGD([w, b], lr=1e-2)
n_epoch = 10000

for epoch in range(n_epoch + 1):
    # 1. hypothesis
    hx = sigmoid(X_train, w, b)

    # 2. loss
    loss = loss_fn(y_train, hx)

    # 3. gradient 초기화 -> 역전파 -> 파라미터 업데이트
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # 4. loss 확인
    if epoch % 1000 == 0:
        print(f'epoch : {epoch}, loss : {loss.item():.6f}')

prediction = torch.sigmoid(X_train.matmul(w) + b)
print(prediction)

pred = []

for i in prediction:
    if i.item() > 0.5:
        pred.append(1)
    else:
        pred.append(0)

print(pred)

result = prediction >= torch.FloatTensor([0.5])
print(result)
```

---

## 추가로 중요한 부분

지금 학습률이 너무 작습니다.

```python
optimizer = optim.SGD([w, b], lr=1e-6)
```

`1e-6`이면 학습이 거의 안 됩니다. 그래서 위 코드에서는 일단

```python
lr=1e-2
```

로 바꿨습니다.

---

## 정리하면

문제는 크게 2개입니다.

```python
return loss.data
```

이 부분 때문에 `loss`가 계산 그래프에서 끊겼습니다. 따라서 반드시:

```python
return loss
```

로 해야 합니다.

그리고 이 부분은 `loss_fn()` 안에 있으면 안 됩니다.

```python
for param in [w, b]:
    if param.grad is not None:
        param.grad.data.zero_()
```

gradient 초기화는 학습 루프 안의:

```python
optimizer.zero_grad()
```

가 담당합니다.

정리하면 PyTorch 학습 흐름은 항상 이 순서로 보면 됩니다.

```python
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

이 3개가 핵심입니다.

---

### ❓ 질문 (User)
```
import torch
import torch.optim as optim
import numpy as np
# ==============
def sigmoid(x:torch.Tensor, w, b) :
    return 1 / (1 + torch.exp(-(x@w + b)))

def loss_fn(y_true, y_pred):
    r"""
    default
    hx : sigmoid(x @ w + b)
    """
    equation = -y_true * torch.log(y_pred) - (1 - y_true) * torch.log(1 - y_pred)
    loss = torch.mean(equation)
    # 누적 미분 방지
    for param in [w, b]:
        if param.grad is not None:
            param.grad.data.zero_()
            
    return loss.data
    


# ==============
# x_data = 6, 2
# y_data = 6, 1
x_data = [[1,2], [2,3], [3,1], [4,3], [5,3], [6,2]]
y_data = [[0], [0], [0], [1], [1], [1]]
X_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)

# 6, 2 @ 2, 1 => 6, 1 => w_size : 2, 1
# w = torch.randn((2, 1), requires_grad=True)
w = torch.zeros((2, 1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

optimizer = optim.SGD([w, b], lr=1e-6)
n_epoch = 1000

for epoch in range(n_epoch + 1)  :
    # 1. hypothesis (sigmoid)
    hx = sigmoid(X_train, w, b)

    # 2. loss function (-y(log(h(x)) - (1-y)log(1-h(x)))
    loss = loss_fn(y_train, hx)

    # 3. gradient descent algorithm & update params
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # 4. loss 값이 잘 떨어지고 있는지 확인
    if epoch % 100 == 0 :
        print(f'epoch : {epoch}, loss : {loss}')

# 학습이 잘 되었으면 w, b 값을 sigmoid 함수에 적용하면
# 앞 3개는 0.5보다 작은 값, 뒤는 0.5보다 큰 값
prediction = torch.sigmoid(X_train.matmul(w) + b)
print(prediction)
pred = []

for i in list(prediction) :
    if i > 0.5 :
        pred.append(1)
    else :
        pred.append(0)
print(pred)

result = prediction >= torch.FloatTensor([0.5])
print(result)
```
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
