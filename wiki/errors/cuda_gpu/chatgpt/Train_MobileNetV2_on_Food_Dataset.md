---
type: Error Note
title: "Train MobileNetV2 on Food Dataset"
description: "Errors - CUDA & GPU - ChatGPT 대화 추출 노트 (2023-07-17)"
tags: [errors, chatgpt-export]
timestamp: 2023-07-17
status: active
---

# Train MobileNetV2 on Food Dataset

> **카테고리**: `Errors - CUDA & GPU`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-07-17

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
import torch
from torch import nn
import torchvision
import albumentations as A
import matplotlib.pyplot as plt
import pandas as pd
from albumentations.pytorch import ToTensorV2
from torchvision.models.mobilenetv2 import mobilenet_v2
from torch.optim import SGD, AdamW
from torch.nn import CrossEntropyLoss
from tqdm import tqdm
from torch.utils.data import DataLoader
from ex_01_0717_customdataset import MyFoodDataset


def train(model, train_loader, val_loader, epochs, optimizer, criterion, device):
    best_val_acc = 0.0
    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []
    print("Train...")

    for epoch in range(epochs):
        train_loss = 0.0
        val_loss = 0.0
        train_acc = 0.0
        val_acc = 0.0

        model.train()
        # tqdm info
        train_loader_iter = tqdm(train_loader, desc=(f"Epoch : {epoch + 1}/{epochs}"), leave=False)

        for i, (data, target) in enumerate(train_loader_iter):
            data = data.to(device)
            target = target.to(device)

            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, target)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

            # train_acc
            _, pred = torch.max(outputs, 1)
            train_acc += (pred == target).sum().item()

            train_loader_iter.set_postfix({"Loss" : loss.item()})

        train_loss /= len(train_loader)
        train_acc = train_acc / len(train_loader.dataset)

        # eval
        model.eval()
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)

                output = model(data)
                pred = torch.max(output, 1)
                val_acc += (pred == target).sum().item()
                val_loss += criterion(output, target).item()
            val_loss /= len(val_loader)
            val_acc = val_acc / len(val_loader.dataset)

            train_losses.append(train_loss)
            train_accs.append(train_acc)
            val_losses.append(val_loss)
            val_accs.append(val_acc)

            # save model
            if val_acc > best_val_acc :
                torch.save(model.state_dict(), "./ex01_0701_mobilenet_v2_best.pt")
                best_val_acc = val_acc

            print(f"Epoch [{epoch + 1} / {epochs}] , Train loss [{train_loss:.4f}],"
                  f"Val loss [{val_loss :.4f}], Train ACC [{train_acc:.4f}],"
                  f"Val ACC [{val_acc:.4f}]")

    torch.save(model.state_dict(), "./ex01_0701_mobilenet_v2_last.pt")
    # save train and val result to csv
    df = pd.DataFrame({
        'Train Loss' : train_losses,
        'Train Accuracy' : train_accs,
        'Validation Loss' : val_losses,
        'Validation Accuracy' : val_accs
    })
    df.to_csv('train_val_results_0717.csv', index=False)
    # Plot and save train and val loss, acc
    plt.figure()
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label = "Validation Loss")
    plt.xlabel('Epoch')
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig("loss_plot.png")

    plt.figure()
    plt.plot(train_accs, label='Train Accuracy')
    plt.plot(val_accs, label = "Validation Accuracy")
    plt.xlabel('Epoch')
    plt.ylabel("Accuracy")
    plt.legend()
    plt.savefig("accuracy_plot.png")




def main() :
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = mobilenet_v2(pretrained=True)
    model.classifier[1] = nn.Linear(1280, 20)
    model.to(device)

    # print(model) # classifier 의 요소들을 알아내기 위해서 print
    train_transforms = A.Compose([
        A.SmallestMaxSize(max_size=256),
        A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=15, p=0.6),
        A.RandomShadow(),
        A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.4),
        A.RandomBrightnessContrast(p=0.5),
        A.Resize(height=224, width=224),
        ToTensorV2(),
    ])

    val_transforms = A.Compose([
        A.SmallestMaxSize(max_size=256),
        A.Resize(height=224, width=224),
        ToTensorV2(),
    ])

    # dataset, dataloader
    train_dataset = MyFoodDataset('./food_dataset/train', transform=train_transforms)
    val_dataset = MyFoodDataset('./food_dataset/validation', transform=val_transforms)

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

    # hyper parameters -> loss function, epoch, optimizer
    epochs = 20
    criterion = CrossEntropyLoss().to(device)
    optimizer = AdamW(model.parameters(), lr=0.001, weight_decay=1e-2)

    train(model, train_loader, val_loader, epochs, optimizer, criterion, device)


if __name__ == "__main__" :
    main()

### 💡 답변 (Assistant)
This code seems to be training a MobileNetV2 model on a food dataset. Let me explain the code step by step:

1. The necessary libraries are imported, including torch, torchvision, albumentations, matplotlib, pandas, and tqdm.

2. The `train` function is defined. It takes the model, train and validation data loaders, number of epochs, optimizer, criterion, and device as inputs. Inside the function, it iterates over the epochs and performs the training and evaluation steps. It keeps track of train and validation losses and accuracies. At the end of each epoch, it saves the model if the validation accuracy improves. Finally, it saves the train and validation results to a CSV file and plots the train and validation losses and accuracies.

3. The `main` function is defined. Inside this function, the device is set to GPU if available, and the MobileNetV2 model is loaded with pretrained weights. The last layer of the model's classifier is replaced with a new linear layer with 20 output units to match the number of classes in the food dataset. The model is moved to the specified device.

4. Transformation pipelines are defined for both training and validation datasets using the Albumentations library. These pipelines include various data augmentation techniques such as resizing, shifting, rotating, random shadow, RGB shift, and random brightness/contrast adjustment.

5. The `MyFoodDataset` class is imported from the `ex_01_0717_customdataset` module. This class is assumed to be a custom dataset class specific to the food dataset, responsible for loading and preprocessing the data.

6. Train and validation datasets are created using the `MyFoodDataset` class and the respective transformation pipelines.

7. Train and validation data loaders are created using the `DataLoader` class, specifying the batch size and whether to shuffle the data.

8. Hyperparameters such as the number of epochs, the loss criterion (CrossEntropyLoss), and the optimizer (AdamW) are set.

9. The `train` function is called with the necessary arguments to start the training process.

10. The `main` function is called to initiate the entire process.

Overall, this code trains a MobileNetV2 model on a food dataset, performs data augmentation, and saves the trained model along with train and validation results.

---

### ❓ 질문 (User)
RuntimeError: stack expects each tensor to be equal size, but got [1000, 1000, 3] at entry 0 and [384, 640, 3] at entry 1

### 💡 답변 (Assistant)
The error message you encountered indicates a size mismatch between two tensors that are being stacked together using the `torch.stack` function. In this case, the error occurs because the dimensions of the tensors you're trying to stack are not compatible.

Based on the error message, the first tensor has a size of [1000, 1000, 3], while the second tensor has a size of [384, 640, 3]. To resolve this issue, you need to ensure that both tensors have the same shape along the dimensions you want to stack.

Here are a few steps you can take to fix this issue:

1. Check the code that precedes the line where the error occurs. Look for any operations or transformations that might be affecting the size of the tensors. Make sure that the tensors being passed to the `torch.stack` function have the same shape.

2. Verify that the data in both tensors is properly loaded and processed. Check if the dimensions of the data match your expectations. You may need to resize or reshape the tensors to ensure they have the same dimensions before stacking.

3. If the tensors have different sizes due to a difference in resolution, consider resizing or cropping the tensors to match a common size before stacking them.

4. If the tensors have different sizes due to an inconsistency in the dataset, you may need to preprocess the data to ensure all samples have the same size. This could involve resizing, cropping, or padding the images.

By identifying the specific code section causing the error and examining the tensor sizes, you should be able to determine the appropriate modifications to make in order to stack the tensors successfully.

---

### ❓ 질문 (User)
translate Korean

### 💡 답변 (Assistant)
Certainly! I'd be happy to help you with the translation. Could you please provide the Korean text that you would like me to translate into English?

---

### ❓ 질문 (User)
yes

### 💡 답변 (Assistant)
Please provide the Korean text that you would like me to translate into English, and I'll be glad to assist you.

---

### ❓ 질문 (User)
한국어로 번역해줘

### 💡 답변 (Assistant)
물론이죠! 어떤 한국어 문장을 영어로 번역해 드릴까요? 번역을 원하는 한국어 텍스트를 제공해주시면 도와드리겠습니다.

---

### ❓ 질문 (User)
The error message you encountered indicates a size mismatch between two tensors that are being stacked together using the torch.stack function. In this case, the error occurs because the dimensions of the tensors you're trying to stack are not compatible.

Based on the error message, the first tensor has a size of [1000, 1000, 3], while the second tensor has a size of [384, 640, 3]. To resolve this issue, you need to ensure that both tensors have the same shape along the dimensions you want to stack.

Here are a few steps you can take to fix this issue:

Check the code that precedes the line where the error occurs. Look for any operations or transformations that might be affecting the size of the tensors. Make sure that the tensors being passed to the torch.stack function have the same shape.

Verify that the data in both tensors is properly loaded and processed. Check if the dimensions of the data match your expectations. You may need to resize or reshape the tensors to ensure they have the same dimensions before stacking.

If the tensors have different sizes due to a difference in resolution, consider resizing or cropping the tensors to match a common size before stacking them.

If the tensors have different sizes due to an inconsistency in the dataset, you may need to preprocess the data to ensure all samples have the same size. This could involve resizing, cropping, or padding the images.

By identifying the specific code section causing the error and examining the tensor sizes, you should be able to determine the appropriate modifications to make in order to stack the tensors successfully.

### 💡 답변 (Assistant)
발생한 오류 메시지는 torch.stack 함수를 사용하여 함께 쌓여지는 두 개의 텐서 사이에 크기 불일치가 있다는 것을 나타냅니다. 이 경우, 오류가 발생하는 이유는 쌓으려는 텐서들의 차원이 호환되지 않기 때문입니다.

오류 메시지를 기반으로 첫 번째 텐서의 크기는 [1000, 1000, 3]이고, 두 번째 텐서의 크기는 [384, 640, 3]임을 알 수 있습니다. 이 문제를 해결하려면 쌓을 차원을 따라 두 텐서가 동일한 형태를 가지도록 해야 합니다.

다음은 이 문제를 해결하기 위해 수행할 수 있는 몇 가지 단계입니다:

- 오류가 발생하는 줄 앞에 있는 코드를 확인하세요. 텐서의 크기에 영향을 주는 작업이나 변환을 확인하세요. torch.stack 함수에 전달되는 텐서들이 동일한 모양을 가지도록 해야 합니다.

- 두 텐서의 데이터가 올바르게 로드되고 처리되었는지 확인하세요. 데이터의 차원이 예상과 일치하는지 확인하세요. 텐서를 쌓기 전에 크기를 조정하거나 재구성해야 할 수도 있습니다.

- 해상도의 차이로 인해 텐서가 서로 다른 크기를 가지고 있는 경우, 쌓기 전에 텐서의 크기를 일치시키기 위해 크기 조정이나 자르기를 고려해야 합니다.

- 데이터셋의 일관성으로 인해 텐서의 크기가 다른 경우, 모든 샘플이 동일한 크기를 가지도록 데이터 전처리를 수행해야 할 수 있습니다. 이미지의 크기 조정, 자르기, 패딩 등이 필요할 수 있습니다.

오류를 발생시키는 특정 코드 섹션을 식별하고 텐서의 크기를 조사함으로써 텐서를 성공적으로 쌓기 위해 필요한 수정 사항을 확인할 수 있을 것입니다.

---
