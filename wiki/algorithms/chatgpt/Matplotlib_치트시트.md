---
type: Concept
title: "Matplotlib 치트시트"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-02-02)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-02-02
status: active
---

# Matplotlib 치트시트

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-02-02

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
파이썬 라이브러리 맷플롯립 에 관한 치트시트를 만들어줘.

### 💡 답변 (Assistant)
아래는 **Matplotlib**의 주요 기능과 사용법을 한눈에 볼 수 있는 치트시트입니다. 이 치트시트에서는 기본적인 설정, 다양한 그래프 종류, 커스터마이징 방법 등을 다루고 있으니 필요에 맞게 참고하세요.

---

# Matplotlib 치트시트

## 1. 기본 설정 및 사용법

### 1.1. 라이브러리 임포트
```python
import matplotlib.pyplot as plt
import numpy as np  # 데이터 생성을 위한 NumPy (선택 사항)
```

### 1.2. 간단한 플롯 그리기
```python
# 데이터 생성
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 플롯 생성
plt.plot(x, y)

# 제목 및 레이블 추가
plt.title("Sine Wave")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# 그래프 보여주기
plt.show()
```

---

## 2. 다양한 그래프 종류

### 2.1. 선 그래프 (Line Plot)
```python
plt.plot(x, y, color='blue', linestyle='-', linewidth=2, marker='o', label="sin(x)")
plt.legend()
plt.show()
```

### 2.2. 산점도 (Scatter Plot)
```python
# 무작위 데이터 생성
x = np.random.rand(50)
y = np.random.rand(50)

plt.scatter(x, y, color='red', marker='x')
plt.title("Scatter Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
```

### 2.3. 막대 그래프 (Bar Plot)
```python
categories = ['A', 'B', 'C', 'D']
values = [10, 24, 36, 12]

plt.bar(categories, values, color='green')
plt.title("Bar Chart")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.show()
```

### 2.4. 히스토그램 (Histogram)
```python
data = np.random.randn(1000)  # 정규분포 데이터
plt.hist(data, bins=30, color='purple', edgecolor='black')
plt.title("Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
```

### 2.5. 파이 차트 (Pie Chart)
```python
labels = ['Python', 'Java', 'C++', 'Ruby']
sizes = [45, 30, 15, 10]
explode = (0.1, 0, 0, 0)  # 강조할 파이 조각

plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Programming Languages")
plt.show()
```

---

## 3. 서브플롯 (Subplots)

### 3.1. 여러 그래프를 하나의 Figure에 배치하기
```python
fig, axs = plt.subplots(2, 2, figsize=(10, 8))  # 2x2 그리드

# 각 subplot에 플롯 그리기
axs[0, 0].plot(x, y, 'r')
axs[0, 0].set_title("Plot 1")

axs[0, 1].scatter(x, np.cos(x), color='blue')
axs[0, 1].set_title("Plot 2")

axs[1, 0].bar(categories, values, color='green')
axs[1, 0].set_title("Plot 3")

axs[1, 1].hist(np.random.randn(1000), bins=30, color='orange')
axs[1, 1].set_title("Plot 4")

plt.tight_layout()  # 레이아웃 조정
plt.show()
```

---

## 4. 스타일 및 커스터마이징

### 4.1. 스타일 설정
Matplotlib은 여러 내장 스타일을 제공합니다.
```python
plt.style.use('ggplot')  # ggplot 스타일 사용
# 또는
plt.style.use('seaborn-darkgrid')
```

### 4.2. 축 및 눈금 설정
```python
plt.plot(x, y)
plt.xlim(0, 10)
plt.ylim(-1.5, 1.5)
plt.xticks(np.arange(0, 11, 2))
plt.yticks(np.linspace(-1.5, 1.5, 7))
plt.show()
```

### 4.3. 그리드 추가
```python
plt.plot(x, y)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
```

---

## 5. 이미지 표시 및 저장

### 5.1. 이미지 저장
```python
plt.plot(x, y)
plt.title("Saving Example")
plt.savefig("sine_wave.png", dpi=300, bbox_inches='tight')
plt.show()
```

### 5.2. 이미지 불러오기 및 표시
```python
import matplotlib.image as mpimg

img = mpimg.imread('sine_wave.png')
plt.imshow(img)
plt.axis('off')  # 축 숨기기
plt.show()
```

---

## 6. 고급 기능

### 6.1. 애니메이션 (Animation)
```python
import matplotlib.animation as animation

fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = np.linspace(0, 10, 1000)
    y = np.sin(x + 0.1 * i)
    line.set_data(x, y)
    return line,

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=50, blit=True)
plt.show()
```

### 6.2. 애노테이션 (Annotation)
```python
plt.plot(x, y)
plt.title("Annotation Example")
plt.annotate("Max Value", xy=(np.pi/2, 1), xytext=(np.pi/2 + 1, 1.2),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()
```

---

## 7. 기타 팁

- **Figure와 Axes**: `plt.figure()`를 이용해 Figure를 생성하고, `fig.add_subplot()` 또는 `plt.subplots()`로 Axes를 추가할 수 있습니다.
- **여러 그래프 저장**: 각 그래프를 개별 Figure로 만들거나, 하나의 Figure에 여러 서브플롯을 추가하여 저장할 수 있습니다.
- **인터랙티브 모드**: `plt.ion()`과 `plt.ioff()`을 사용해 인터랙티브 모드에서 작업할 수 있습니다.

---

이 치트시트를 활용하여 Matplotlib의 다양한 기능들을 빠르게 찾아보고 적용해 보세요. 추가적인 정보나 심화된 기능은 [Matplotlib 공식 문서](https://matplotlib.org/stable/contents.html)를 참고하면 좋습니다.

---
