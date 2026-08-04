---
type: Error Note
title: "Epoch 출력 문제"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2026-05-20)"
tags: [errors, chatgpt-export]
timestamp: 2026-05-20
status: active
---

# Epoch 출력 문제

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-20

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
코드상 “멈춘 것처럼 보이는” 원인이 꽤 명확합니다. 핵심은 출력 주기, 에포크 수, CUDA/CPU 디바이스 불일치 쪽을 같이 봐야 합니다.

---

### 💡 답변 (Assistant)
가장 큰 원인은 **멈춘 게 아니라 출력이 100 epoch마다만 나오기 때문**일 가능성이 큽니다.

현재 코드가 이렇게 되어 있습니다.

```python
train(1000)

...

if e % 100 == 0:
    print(f'epoch : {e}, loss : {loss.item()}')
```

즉 출력은 다음처럼 나옵니다.

```text
epoch : 0, loss : ...
epoch : 100, loss : ...
epoch : 200, loss : ...
...
```

MNIST 전체 데이터를 **1001 epoch** 학습시키고 있기 때문에, `epoch 0` 출력 이후 `epoch 100`까지 시간이 꽤 걸립니다. 그래서 “첫 번째 에포크만 돌고 멈춘 것처럼” 보이는 겁니다.

---

## 1. 먼저 epoch 수를 줄여서 확인해보세요

MNIST에 `nn.Linear(784, 10)` 하나만 쓰는 모델이면 보통 처음 테스트는 `5~10 epoch`면 충분합니다.

```python
train(10)
```

그리고 출력도 매 epoch마다 찍어보세요.

```python
if e % 1 == 0:
    print(f'epoch : {e}, loss : {loss.item()}')
```

---

## 2. 현재 코드의 두 번째 문제: 추론할 때 X_test가 CPU에 있음

학습할 때 모델은 CUDA로 보냈습니다.

```python
model = nn.Linear(in_features=28*28, out_features=10, bias=True).to(device)
```

그런데 추론할 때는 `X_test`를 CUDA로 안 보냈습니다.

```python
X_test = X_test.view(-1, 28*28)
prediction = model(X_test)
```

모델이 GPU에 있고 입력이 CPU에 있으면 보통 이런 에러가 납니다.

```text
Expected all tensors to be on the same device
```

따라서 이렇게 해야 합니다.

```python
X_test = X_test.view(-1, 28*28).to(device)
prediction = model(X_test)
```

---

## 3. 저장 경로도 현재 코드상 불일치 가능성이 있음

저장은 이렇게 합니다.

```python
torch.save(model, 'mnist_clf.pth')
```

그런데 로드는 이렇게 합니다.

```python
model = torch.load('./20260519/mnist_clf.pth', weights_only=False)
```

저장 위치와 불러오는 위치가 다릅니다.

둘 중 하나로 통일해야 합니다.

```python
torch.save(model, './20260519/mnist_clf.pth')
```

또는

```python
model = torch.load('mnist_clf.pth', weights_only=False)
```

---

## 4. CUDA로 제대로 학습되는지 확인하는 출력 추가

학습 전에 이걸 찍어보세요.

```python
print(device)
print(next(model.parameters()).device)
```

학습 루프 안에서도 한 번만 확인해볼 수 있습니다.

```python
for data, target in data_loader:
    data = data.view(-1, 28*28).to(device)
    target = target.to(device)

    print(data.device, target.device)
    break
```

정상이라면 CUDA 사용 가능 환경에서 이렇게 나와야 합니다.

```text
cuda
cuda:0
cuda:0 cuda:0
```

---

## 5. 수정한 핵심 코드

일단 지금 코드 구조를 크게 바꾸지 않고 고치면 이렇게 하면 됩니다.

```python
data_loader = DataLoader(
    mnist_train,
    batch_size=128,
    shuffle=True
)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("device:", device)

model = nn.Linear(in_features=28*28, out_features=10, bias=True).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

def train(epoch):
    model.train()

    for e in range(epoch + 1):
        total_loss = 0.0

        for data, target in data_loader:
            data = data.view(-1, 28*28).to(device)
            target = target.to(device)

            optimizer.zero_grad()

            y_hat = model(data)
            loss = loss_fn(y_hat, target)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(data_loader)

        print(f'epoch : {e}, loss : {avg_loss:.4f}')

    print('finished!')

train(10)

torch.save(model, './20260519/mnist_clf.pth')
```

---

## 6. 추론 코드 수정

```python
model = torch.load('./20260519/mnist_clf.pth', weights_only=False)
model = model.to(device)
model.eval()

for i in range(5):
    img = transform(mnist_test[i][0])
    print("label:", mnist_test[i][1])

    plt.imshow(img, cmap='gray')
    plt.show()

    X_test = mnist_test[i][0]
    X_test = X_test.view(-1, 28*28).to(device)

    with torch.no_grad():
        prediction = model(X_test)
        prob = F.softmax(prediction, dim=1)
        pred = torch.argmax(prob, dim=1)

    print(prob)
    print("prediction:", pred.item())
```

---

## 7. 현재 코드에서 특히 중요한 포인트

`nn.CrossEntropyLoss()`는 내부적으로 이미 다음을 포함합니다.

```python
log_softmax + negative log likelihood loss
```

그래서 학습할 때는 모델 출력에 직접 `softmax`를 걸면 안 됩니다.

좋은 코드:

```python
y_hat = model(data)
loss = loss_fn(y_hat, target)
```

나쁜 코드:

```python
y_hat = F.softmax(model(data), dim=1)
loss = loss_fn(y_hat, target)
```

추론할 때만 확률을 보고 싶으면 `softmax`를 쓰면 됩니다.

```python
prob = F.softmax(prediction, dim=1)
```

---

결론적으로 지금 문제는 대부분 이겁니다.

```text
1. train(1000)이 너무 김
2. 출력이 100 epoch마다라서 멈춘 것처럼 보임
3. 추론 시 X_test.to(device)가 빠져 있음
4. 저장 경로와 로드 경로가 다를 수 있음
```

우선 `train(10)`으로 바꾸고, `print`를 매 epoch 출력하게 하면 바로 정상 동작 여부를 확인할 수 있습니다.

---

### ❓ 질문 (User)
```
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
import torch.optim as optim
import matplotlib.pyplot as plt
from torchvision import datasets                     # mnist, fashion mnist
import torchvision.transforms as transforms     # dataset -> Tensor
import os

dataset_path = './20260519/data/'
# os.makedirs(dataset_path, exist_ok=True)

mnist_train = datasets.MNIST(root=dataset_path, 
                             train=True,
                             transform=transforms.ToTensor(), 
                             download=True)
mnist_test = datasets.MNIST(root=dataset_path, 
                            train=False,
                            transform=transforms.ToTensor(),
                            download=True)

data_loader = DataLoader(mnist_train, batch_size=(28*28), shuffle=True)

transform = transforms.ToPILImage()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

"""
for i in range(5) :
    img = transform(mnist_train[i][0])
    print(mnist_train[i][1])
    print(img.size)
    plt.imshow(img, cmap='gray')
    plt.show()
"""
# 객체 생성 --> model(x) --> w * x + b
# (28, 28) --> 2차원 데이터로 표현 ==> 1차원으로 계산하기 위해 28x28의 값을 사용한다.
# (28, 28) --> 28x28 1차원 배열 데이터와 같다.
# 지금 grayscale 했기 때문에 channel = 1 이라 in_features = 28*28 임.
# 만약 컬러라면? channel = 3 이기 때문에 in_features = 28*28*3 을 해줘야 함.
# model = nn.Linear(in_features=28*28, out_features=10)
model = nn.Linear(in_features=28*28, out_features=10, bias=True).to(device)
# F.cross_entropy() # 와 차이점은?
# loss_fn = nn.CrossEntropyLoss()    # softmax(wx + b)
loss_fn = nn.CrossEntropyLoss().to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

def train(epoch) :
    for e in range(epoch + 1) :
        for data, target in data_loader :
            # datashape : 28x28 --> nn.Linear의 입력 값과 동일하게 맞춰줘야 하기 떄문에.
            # data = data.view(-1, 28*28)
            data = data.view(-1, 28*28).to(device)
            target = target.to(device)
            optimizer.zero_grad()
            y_hat = model(data)
            loss = loss_fn(y_hat, target)
            loss.backward()
            optimizer.step()

        if e % 100 == 0 :
            print(f'epoch : {e}, loss : {loss.item()}')
    print('finished!')
train(1000)
torch.save(model, 'mnist_clf.pth')

# inference (추론) -> 보통 실행이라고 하지 않음.
model = torch.load('./20260519/mnist_clf.pth', weights_only=False)

for i in range(5) :
    img = transform(mnist_test[i][0])
    print(mnist_test[i][1])
    plt.imshow(img, cmap='gray')
    plt.show()

    X_test = mnist_test[i][0]   # [i] : 인덱스, [0] : 이미지, [1] : target
    print(X_test.shape, X_test.ndim, type(X_test))
    # 형태 변환 해주기
    X_test = X_test.view(-1, 28*28)
    prediction = model(X_test)
    prob = F.softmax(prediction, dim=1)
    print(prob)
    print(torch.argmax(prob, dim=1))
```
mnist 테스트 코드인데 cuda 로 돌려보려고 하고 있어. 근데 첫번째 에포크만 돌고 다음부터는 동작하지를 않네.. 원인이 뭘까

### ❓ 질문 (User)
그럼 GPU 가 처음에는 부하가 바로 걸렸다가 한동안 안돌아가는게 정상이라는거야?

### 💡 답변 (Assistant)
어느 정도는 **정상일 수 있습니다.** 특히 지금 코드처럼 **MNIST + `nn.Linear(784, 10)` 하나짜리 아주 작은 모델**을 GPU에서 돌리면, GPU가 계속 100%로 도는 게 아니라 **잠깐 튀었다가 쉬는 패턴**이 자주 나옵니다.

핵심 원인은 이겁니다.

```text
CPU가 데이터 준비
↓
CPU → GPU로 데이터 복사
↓
GPU가 아주 짧게 계산
↓
다시 CPU/DataLoader 기다림
```

모델이 너무 작아서 GPU 계산 시간이 매우 짧습니다. 그래서 GPU 입장에서는 일을 “순간적으로 처리하고” 다시 데이터를 기다리게 됩니다.

---

## 지금 코드에서는 특히 이 부분이 영향이 큽니다

```python
data_loader = DataLoader(mnist_train, batch_size=(28*28), shuffle=True)
```

`batch_size=784` 자체가 틀린 건 아니지만, MNIST + Linear 모델에서는 한 배치 계산량이 너무 작습니다.

그리고 매 batch마다 이 작업이 반복됩니다.

```python
data = data.view(-1, 28*28).to(device)
target = target.to(device)
```

즉, CPU 메모리에 있는 데이터를 계속 GPU로 복사합니다.  
GPU 계산보다 **데이터 이동/준비 시간이 더 커질 수 있습니다.**

그래서 작업 관리자에서 보면 이런 느낌이 납니다.

```text
GPU 사용률: 0% → 순간 20~100% → 다시 0% → 순간 상승 → 다시 0%
```

이건 작은 모델 학습에서는 꽤 흔합니다.

---

## 그런데 “아예 한동안 안 돈다”면 확인할 것

정상적인 “짧은 유휴 상태”가 아니라, 정말 오래 멈춘 것 같다면 다음 세 가지를 확인해야 합니다.

### 1. 출력 주기 문제

현재는 100 epoch마다만 출력됩니다.

```python
if e % 100 == 0:
    print(f'epoch : {e}, loss : {loss.item()}')
```

그래서 `epoch 0` 이후 오래 조용합니다.  
학습이 안 도는 게 아니라 출력이 없는 것일 수 있습니다.

일단 이렇게 바꾸세요.

```python
if e % 1 == 0:
    print(f'epoch : {e}, loss : {loss.item()}')
```

그리고 `train(1000)` 말고 먼저 이렇게 하세요.

```python
train(10)
```

---

### 2. GPU 사용률보다 CUDA 메모리 사용량 확인

Windows 작업 관리자에서 GPU 사용률만 보면 헷갈립니다.  
명령어로 보는 게 더 정확합니다.

터미널에서:

```bash
nvidia-smi
```

학습 중에 여기서 Python 프로세스가 보이고 GPU 메모리를 쓰고 있으면 CUDA는 사용 중입니다.

예상 형태:

```text
python.exe    500MiB
```

MNIST Linear 모델은 작아서 VRAM도 많이 안 씁니다. 수백 MB 정도만 잡힐 수 있습니다.

---

### 3. DataLoader가 병목일 수 있음

DataLoader를 조금 개선할 수 있습니다.

```python
data_loader = DataLoader(
    mnist_train,
    batch_size=256,
    shuffle=True,
    num_workers=2,
    pin_memory=True
)
```

그리고 학습 루프에서:

```python
data = data.view(-1, 28*28).to(device, non_blocking=True)
target = target.to(device, non_blocking=True)
```

다만 Windows에서는 `num_workers`를 너무 크게 주면 오히려 느려지거나 문제가 생길 수 있습니다. 처음에는 `0`, `2`, `4` 정도만 비교해보면 됩니다.

---

## 지금 모델에서는 GPU가 별로 할 일이 없습니다

현재 모델은 이거 하나입니다.

```python
model = nn.Linear(28*28, 10)
```

파라미터 수는 대략:

```text
784 × 10 + 10 = 7,850개
```

이건 GPU 입장에서는 너무 작은 계산입니다.  
GPU는 수백만~수십억 개 연산을 병렬로 처리할 때 빛이 나는데, 지금 모델은 거의 “계산 연습 문제” 수준입니다.

그래서 CPU로 돌려도 충분히 빠르고, 오히려 GPU로 보내는 비용 때문에 체감상 GPU가 놀아 보일 수 있습니다.

---

## GPU가 제대로 일하는지 확인하려면 CNN으로 바꿔보면 됩니다

예를 들어 이런 모델을 쓰면 GPU 사용률이 더 잘 보입니다.

```python
class CNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Flatten(),
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        return self.net(x)
```

이 경우에는 `view(-1, 28*28)` 하면 안 됩니다. 이미 이미지 형태로 넣어야 합니다.

```python
data = data.to(device)
target = target.to(device)
y_hat = model(data)
```

MNIST 이미지 shape은 원래:

```text
[batch_size, 1, 28, 28]
```

CNN은 이 형태를 그대로 받습니다.

---

## 결론

지금 상황은 이렇게 보면 됩니다.

```text
GPU 부하가 처음에 걸림
→ 데이터 로딩/전송/출력 대기 때문에 잠깐 쉬어 보임
→ 작은 Linear 모델이라 GPU 계산 시간이 너무 짧음
→ epoch 출력도 100번마다라서 멈춘 것처럼 보임
```

따라서 **지금 코드 기준으로는 GPU가 계속 바쁘게 안 도는 게 정상에 가깝습니다.**

다만 확인은 이렇게 하면 됩니다.

```python
print(device)
print(next(model.parameters()).device)
```

그리고 학습 중 터미널에서:

```bash
nvidia-smi
```

여기서 Python 프로세스가 GPU 메모리를 잡고 있으면 CUDA는 사용 중입니다.

---

### ❓ 질문 (User)
윈도우 터미널창에서 watch -d -n 0.5 nvidia-smi 명령어처럼 계속해서 창 띄워놓고 싶은데 하는 방법알려줘.

### 💡 답변 (Assistant)
Windows에서는 `watch` 명령어가 기본으로 없습니다. 대신 아래 방법을 쓰면 됩니다.

## 방법 1. PowerShell에서 가장 간단한 방법

Windows Terminal에서 **PowerShell** 탭을 열고 실행하세요.

```powershell
while ($true) { cls; nvidia-smi; Start-Sleep -Milliseconds 500 }
```

의미는 이렇습니다.

```text
cls                       # 화면 지우기
nvidia-smi                # GPU 상태 출력
Start-Sleep -Milliseconds 500  # 0.5초 대기
```

중지하려면:

```text
Ctrl + C
```

---

## 방법 2. PowerShell에서 한 줄로 프로세스까지 보기 좋게

```powershell
while ($true) { cls; nvidia-smi; Start-Sleep -Seconds 1 }
```

0.5초가 너무 빠르면 1초가 더 보기 편합니다.

---

## 방법 3. CMD에서 실행하는 방법

Windows Terminal에서 **명령 프롬프트(cmd)** 탭을 열고 실행하세요.

```cmd
for /l %i in () do @cls & nvidia-smi & timeout /t 1 >nul
```

다만 CMD는 0.5초 단위 대기가 불편해서 보통 1초 단위로 씁니다.

중지:

```text
Ctrl + C
```

---

## 방법 4. nvidia-smi 자체 반복 옵션 사용

`nvidia-smi`에는 반복 실행 옵션이 있습니다.

```powershell
nvidia-smi -l 1
```

1초마다 갱신됩니다.

0.5초 단위는 아래처럼 가능합니다.

```powershell
nvidia-smi -lms 500
```

이게 제일 깔끔합니다.

중지:

```text
Ctrl + C
```

---

## 추천

제일 추천하는 건 이겁니다.

```powershell
nvidia-smi -lms 500
```

화면을 매번 지우면서 `watch`처럼 보고 싶으면 이걸 쓰세요.

```powershell
while ($true) { cls; nvidia-smi; Start-Sleep -Milliseconds 500 }
```

Windows Terminal에서 탭 하나는 학습 코드 실행용, 다른 탭 하나는 위 명령어 실행용으로 띄워두면 됩니다.

---
