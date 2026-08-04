---
type: Concept
title: "Resize JPG files (28x28)"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2023-07-03)"
tags: [cs, chatgpt-export]
timestamp: 2023-07-03
status: active
---

# Resize JPG files (28x28)

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-07-03

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
start resize 'jpg' file to (28, 28) size 10 picture

### 💡 답변 (Assistant)
Certainly! I can help you resize JPG files to a size of 28x28 pixels. Please provide the 10 JPG files that you would like to resize, and I will assist you in the process.

(Note: Please provide the JPG files in a format that can be shared in this text-based conversation, such as by uploading them or providing direct links to the files.)

---

### 💡 답변 (Assistant)
To resize 10 'jpg' files to a (28, 28) size, you can use various programming languages and libraries, but I'll provide an example using Python and the popular `PIL` (Python Imaging Library) or its newer version, `Pillow`:

1. First, make sure you have `Pillow` installed. If you don't have it, you can install it using pip:

```bash
pip install Pillow
```

2. Place the 10 'jpg' files you want to resize in a folder. Let's assume the folder is named 'input' and it contains the files 'file1.jpg', 'file2.jpg', ..., 'file10.jpg'.

3. Create a new folder named 'output' to store the resized images.

Now, you can use the following Python script to resize the images:

```python
from PIL import Image
import os

def resize_image(input_path, output_path, new_size):
    with Image.open(input_path) as img:
        resized_img = img.resize(new_size, Image.ANTIALIAS)
        resized_img.save(output_path)

# Path to the input and output folders
input_folder = 'input'
output_folder = 'output'

# Desired new size
new_size = (28, 28)

# Make sure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        resize_image(input_path, output_path, new_size)
        print(f"{filename} resized and saved to {output_path}")
```

Place this Python script in the same directory where the 'input' and 'output' folders exist. When you run the script, it will resize all the 'jpg' images from the 'input' folder and save them to the 'output' folder with the specified size of (28, 28).

---

### ❓ 질문 (User)
1. 학습자료 - 손글씨_데이터 폴더 다운로드 (14:00 기준 520장 - 깨진 파일 30장 = 490장)

2. 해당 폴더 내용물을 토대로 Custom Dataset 작성
2-1. __init__, __getitem__, __len__ 내부 함수 작성
2-2. 라벨은 이미지 파일 이름에 포함된 숫자 사용 (0~9, 한자리 숫자)
2-3. 이미지 사이즈 28x28로 변환해서 반환

3. CNN 모델 작성
3-1. __init__에서 각 레이어 정의
3-2. forward에서 순전파 정의

4. 작성한 모델을 토대로 학습(10 Epochs), 평가 진행
4-1. 손실함수: CrossEntropyLoss
4-2. 옵티마이저: SGD, Adam 등 자유 선택

5. 학습시에는 각 Epoch 별로 Loss 출력 (print문),
    평가시에는 평가 종류 후 최종 정확도 백분율로 출력(print문)

### 💡 답변 (Assistant)
I see you have a specific task at hand. Let's break it down into steps and go through each one:

Step 1: Download the '손글씨_데이터' folder containing handwritten digit images.

Before we proceed, please provide a link or specify where I can download the '손글씨_데이터' folder. Once you provide the download link or information, we can move on to the next steps.

---

### 💡 답변 (Assistant)
To complete the tasks, you can use Python with PyTorch as the deep learning framework. Here's a step-by-step guide to accomplish each task:

1. Download the dataset:

Assuming the '손글씨_데이터' folder is downloaded and contains 490 images with numerical labels.

2. Custom Dataset:

Create a custom dataset class for loading the images and their corresponding labels.

```python
import os
from PIL import Image
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.data = os.listdir(root_dir)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.data[idx])
        image = Image.open(img_name)

        if self.transform:
            image = self.transform(image)

        label = int(self.data[idx].split('.')[0])  # Extract label from the image filename

        return image, label
```

3. CNN Model:

Define the CNN model with convolutional and fully connected layers.

```python
import torch.nn as nn

class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc_layers = nn.Sequential(
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)  # Output layer with 10 classes (0-9)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)  # Flatten the feature map
        x = self.fc_layers(x)
        return x
```

4. Training and Evaluation:

Train the model and evaluate it after each epoch.

```python
import torch
import torch.optim as optim
import torch.nn.functional as F
from torchvision.transforms import transforms
from torch.utils.data import DataLoader

# Constants
ROOT_DIR = '손글씨_데이터'  # Replace with the path to the downloaded dataset
BATCH_SIZE = 32
NUM_EPOCHS = 10

# Define transformations to resize images and convert them to tensors
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor()
])

# Create the custom dataset and data loader
dataset = CustomDataset(ROOT_DIR, transform=transform)
data_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# Create the CNN model and move it to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CNNModel().to(device)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training and evaluation
for epoch in range(NUM_EPOCHS):
    model.train()
    total_loss = 0.0

    for images, labels in data_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step

---

### 💡 답변 (Assistant)
()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{NUM_EPOCHS} Loss: {total_loss/len(data_loader):.4f}")

# Evaluation
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for images, labels in data_loader:
        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Accuracy: {100 * correct / total:.2f}%")
```

Note: Make sure you have PyTorch installed (`pip install torch`) and that the 'torchvision' package is available as well (`pip install torchvision`).

---

### ❓ 질문 (User)
png, jpg 확장자를 동시에 불러오려면 어떻게 해야 돼?

### 💡 답변 (Assistant)
To load both PNG and JPG file extensions together, you can modify the `CustomDataset` class to handle multiple file extensions. Here's an updated version of the class that loads both PNG and JPG images:

```python
import os
from PIL import Image
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.data = []
        self.load_data()

    def load_data(self):
        file_extensions = ['.png', '.jpg']  # Supported file extensions
        for filename in os.listdir(self.root_dir):
            ext = os.path.splitext(filename)[1].lower()
            if ext in file_extensions:
                self.data.append(filename)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.data[idx])
        image = Image.open(img_name)

        if self.transform:
            image = self.transform(image)

        label = int(self.data[idx].split('.')[0])  # Extract label from the image filename

        return image, label
```

In this updated version, the `load_data` method checks the file extension of each file in the dataset folder and only adds the filenames with extensions '.png' or '.jpg' to the dataset. This way, when you create an instance of the `CustomDataset` class, it will load images with both PNG and JPG file extensions.

---
