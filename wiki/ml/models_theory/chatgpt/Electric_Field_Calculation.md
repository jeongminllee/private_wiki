---
type: Concept
title: "Electric Field Calculation"
description: "ML - Models & Theory - ChatGPT 대화 추출 노트 (2025-01-01)"
tags: [ml, chatgpt-export]
timestamp: 2025-01-01
status: active
---

# Electric Field Calculation

> **카테고리**: `ML - Models & Theory`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-01-01

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
A 3-phase, 4-wire industrial electrical distribution system operates at 480V and supplies a load with a power consumption of 100kW and a power factor of 0.75 lagging. The system includes a 300kVA transformer, with an efficiency of 95%, and a 10,000uf, 3-phase capacitor bank connected in delta configuration. If the system's cables and other components have a total capacitance of 500nF, what is the magnitude of the electric field, in kV/m, at a point 10cm from the center of one of the capacitor's plates, when the capacitor bank is connected to correct the power factor to 0.95?
Assume the plates are square, with a side length of 20cm, and that the space between the plates is filled with air.

### 💡 답변 (Assistant)
To determine the electric field at a point 10 cm from the center of one of the capacitor's plates, we must calculate the voltage across the capacitor bank first and then use the geometry of the capacitor to compute the electric field.

### Step 1: Correct the power factor
The capacitor bank is used to correct the power factor from 0.75 lagging to 0.95 lagging.

1. **Calculate the initial reactive power (\( Q_\text{initial} \)):**
   The apparent power (\( S \)) is:
   \[
   S = \frac{\text{Real Power}}{\text{Power Factor}} = \frac{100\,\text{kW}}{0.75} = 133.33\,\text{kVA}.
   \]
   The reactive power (\( Q_\text{initial} \)) is:
   \[
   Q_\text{initial} = \sqrt{S^2 - P^2} = \sqrt{133.33^2 - 100^2} = 88.19\,\text{kVAR}.
   \]

2. **Calculate the final reactive power (\( Q_\text{final} \)):**
   After correction to a power factor of 0.95:
   \[
   S_\text{new} = \frac{P}{0.95} = \frac{100}{0.95} = 105.26\,\text{kVA}.
   \]
   \[
   Q_\text{final} = \sqrt{S_\text{new}^2 - P^2} = \sqrt{105.26^2 - 100^2} = 32.87\,\text{kVAR}.
   \]

3. **Determine the reactive power provided by the capacitor bank (\( Q_\text{capacitor} \)):**
   The capacitor bank must supply:
   \[
   Q_\text{capacitor} = Q_\text{initial} - Q_\text{final} = 88.19 - 32.87 = 55.32\,\text{kVAR}.
   \]

### Step 2: Voltage across the capacitor bank
The total capacitance of the capacitor bank is \( C = 10,000\,\mu\text{F} = 10\,\text{mF} \), and it is connected in delta configuration. The reactive power in a 3-phase capacitor bank is:
\[
Q_\text{capacitor} = 3 \cdot V_\text{line}^2 \cdot 2\pi f C_\text{phase},
\]
where \( C_\text{phase} \) is the capacitance per phase and \( f = 60\,\text{Hz} \) is the frequency. Since the capacitor is connected in delta, \( C_\text{phase} = C / 3 \):
\[
C_\text{phase} = \frac{10\,\text{mF}}{3} = 3.33\,\text{mF}.
\]

Rearranging to solve for \( V_\text{line} \):
\[
V_\text{line}^2 = \frac{Q_\text{capacitor}}{3 \cdot 2\pi f C_\text{phase}}.
\]
Substitute the known values:
\[
V_\text{line}^2 = \frac{55,320}{3 \cdot 2\pi \cdot 60 \cdot 3.33 \times 10^{-3}} = \frac{55,320}{3 \cdot 1.256 \cdot 3.33 \times 10^{-3}}.
\]
\[
V_\text{line}^2 = \frac{55,320}{0.01251} = 4.42 \times 10^6 \, \text{V}^2.
\]
\[
V_\text{line} = \sqrt{4.42 \times 10^6} = 2102.4\,\text{V}.
\]

### Step 3: Electric field calculation
For square plates of side length \( L = 20\,\text{cm} = 0.2\,\text{m} \), the effective surface area is:
\[
A = L^2 = 0.2^2 = 0.04\,\text{m}^2.
\]
The electric field between the plates is given by:
\[
E = \frac{V_\text{line}}{d},
\]
where \( d \) is the separation between the plates. Assuming a typical air gap for such capacitors, let \( d = 1\,\text{cm} = 0.01\,\text{m} \).

Substitute \( V_\text{line} \):
\[
E = \frac{2102.4}{0.01} = 210,240\,\text{V/m} = 210.24\,\text{kV/m}.
\]

Thus, the electric field magnitude at 10 cm (outside the plates) will still approximate this value within the plane of the plates due to the uniformity of the field.

---
