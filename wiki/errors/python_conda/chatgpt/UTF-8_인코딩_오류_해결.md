---
type: Error Note
title: "UTF-8 인코딩 오류 해결"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2025-08-26)"
tags: [errors, chatgpt-export]
timestamp: 2025-08-26
status: active
---

# UTF-8 인코딩 오류 해결

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-08-26

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
이 에러는 **`.env` 파일 인코딩이 UTF-8이 아닐 때**(대부분 Windows 메모장 “Unicode”=UTF-16 LE로 저장) 발생합니다.  
첫 바이트 `0xFF` 는 **UTF-16 BOM(FF FE/FE FF)** 신호예요. `python-dotenv`가 기본으로 UTF-8로 읽다가 깨진 거죠.

아래 중 편한 방법으로 고치면 바로 해결됩니다.

---

## 해결 1) `.env`를 UTF-8(무 BOM)으로 다시 저장 (추천)

### VS Code
1. `.env` 파일 열기  
2. 우하단 인코딩 표시(예: `UTF-16 LE`) 클릭 → **“Save with Encoding…”**  
3. **UTF-8** 선택 후 저장  
   - 가능하면 **UTF-8 (no BOM)** 으로 저장

### 메모장(Windows)
1. 파일 → 다른 이름으로 저장  
2. **인코딩: UTF-8** 선택 → 저장

> 저장 후 Streamlit 다시 실행.

---

## 해결 2) 코드에서 올바른 인코딩으로 읽기

`.env`가 당장 UTF-16으로 되어 있다면, 일단 이렇게 불러도 됩니다.

```python
# utils.py
from dotenv import load_dotenv
from pathlib import Path

# (권장) 명시적으로 .env 경로와 인코딩 지정
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=dotenv_path, encoding="utf-16")  # 임시로 utf-16
```

정상 실행되는지 확인한 뒤, **나중엔 꼭 파일을 UTF-8로 변환**하세요. (항상 UTF-16로 두면 협업/배포 때 또 문제 납니다.)

---

## 해결 3) 어떤 `.env`를 읽는지/바이트 확인 (빠른 점검)

```python
from pathlib import Path
p = Path(__file__).resolve().parent / ".env"
print("env path:", p)
print("first 4 bytes:", open(p, "rb").read(4))
```

- `b'\xff\xfe'` 또는 `b'\xfe\xff'` 면 UTF-16입니다.

---

## 해결 4) PowerShell로 UTF-8(무 BOM) 변환

- **PowerShell 7 이상**:
```powershell
Get-Content .env -Raw | Set-Content .env -NoNewline -Encoding UTF8NoBOM
```

- **PowerShell 5.1**(무 BOM 옵션 없음 → .NET 사용):
```powershell
$path = ".env"
$text = Get-Content $path -Raw
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Resolve-Path $path), $text, $utf8NoBom)
```

---

## 추가 체크포인트
- **경로 혼동 방지:** `load_dotenv()`는 현재 작업 디렉터리부터 상위로 올라가며 `.env`를 찾습니다. 의도치 않은 `.env`(예: 다른 폴더의 바이너리 파일)를 잡지 않도록 **경로를 명시**하세요.
- **내용 형식:** `.env`는 `KEY=VALUE` 텍스트만 있어야 합니다. 바이너리/엑셀/워드로 저장하면 안 됩니다.
- **BOM 주의:** UTF-8 with BOM은 파싱시 키 이름 앞에 보이지 않는 문자(`\ufeff`)가 섞일 수 있으므로 **무 BOM(plain UTF-8)** 을 권장합니다.

위 중 하나 적용하면 `UnicodeDecodeError`는 사라질 거예요. 필요하면 `.env` 내용이나 `utils.py` 일부를 보여주시면, 더 정확히 점검해서 고쳐드릴게요.

---

### ❓ 질문 (User)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

File "C:\Users\USER\Desktop\daegu_lec\app.py", line 62, in <module>
    start_chat()
File "C:\Users\USER\Desktop\daegu_lec\app.py", line 52, in start_chat
    llm = load_model(st.session_state.model_name)  # 선택된 모델을 로드합니다.
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\USER\Desktop\daegu_lec\utils.py", line 30, in load_model
    load_dotenv()
File "C:\Users\USER\anaconda3\Lib\site-packages\dotenv\main.py", line 342, in load_dotenv
    return dotenv.set_as_environment_variables()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\USER\anaconda3\Lib\site-packages\dotenv\main.py", line 85, in set_as_environment_variables
    if not self.dict():
           ^^^^^^^^^^^
File "C:\Users\USER\anaconda3\Lib\site-packages\dotenv\main.py", line 69, in dict
    self._dict = OrderedDict(resolve_variables(raw_values, override=self.override))
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\USER\anaconda3\Lib\site-packages\dotenv\main.py", line 229, in resolve_variables
    for (name, value) in values:
File "C:\Users\USER\anaconda3\Lib\site-packages\dotenv\main.py", line 77, in parse
    for mapping in with_warn_for_invalid_lines(parse_stream(stream)):
File "C:\Users\USER\anaconda3\Lib\site-packages\dotenv\main.py", line 19, in with_warn_for_invalid_lines
    for mapping in mappings:
File "C:\Users\USER\anaconda3\Lib\site-packages\dotenv\parser.py", line 180, in parse_stream
    reader = Reader(stream)
             ^^^^^^^^^^^^^^
File "C:\Users\USER\anaconda3\Lib\site-packages\dotenv\parser.py", line 71, in __init__
    self.string = stream.read()
                  ^^^^^^^^^^^^^
File "<frozen codecs>", line 322, in decode

### 💡 답변 (Assistant)
좋은 포인트예요!  
`utf-8-sig`는 **“BOM(Byte Order Mark)이 붙어 있을 수도 있는 UTF-8 파일을 안전하게 읽기/쓰기 위한 파이썬 코덱 이름”**입니다.

### 왜 필요한가?
- 일부 에디터/도구는 UTF-8 파일 앞에 **BOM(0xEF 0xBB 0xBF)** 을 붙여 저장합니다.
- 이 BOM이 남아 있으면 첫 키가 `\ufeffAPI_KEY`처럼 보이지 않는 문자로 시작해서 파서가 깨지거나 키 이름이 달라집니다.
- 파이썬에서 **`encoding='utf-8-sig'`** 로 읽으면, **읽는 시점에 BOM을 자동으로 제거**해 줍니다.  
  (반대로 **쓸 때** `utf-8-sig`를 쓰면 BOM을 **붙여서** 저장합니다.)

### 어떻게 쓰나? (dotenv 포함)
```python
# 1) 일반 파일 읽기
with open(".env", encoding="utf-8-sig") as f:
    text = f.read()  # BOM이 있었다면 자동으로 제거됨

# 2) python-dotenv
from dotenv import load_dotenv
load_dotenv(encoding="utf-8-sig")  # .env가 UTF-8 BOM일 때 안전
```

### 주의: 당신의 에러는 “UTF-16일 가능성”이 큽니다
처음 올린 스택트레이스는 **`0xff`** 로 시작해서 **UTF-16 (보통 LE: `FF FE`)** 로 저장된 경우에 흔히 보입니다.  
- UTF-8 BOM: `EF BB BF`  
- **UTF-16 LE BOM: `FF FE`**  
- UTF-16 BE BOM: `FE FF`

만약 파일이 **UTF-16** 이라면 `utf-8-sig`로는 해결 안 되고,
```python
load_dotenv(encoding="utf-16")  # 임시 회피
```
로 읽거나, 파일 자체를 **UTF-8(무 BOM)** 으로 변환해야 합니다.

### 빠른 판별 & 변환 팁
```python
# 첫 바이트 검사
with open(".env", "rb") as f:
    print(f.read(4))  # b'\xef\xbb\xbf'면 UTF-8 BOM, b'\xff\xfe'면 UTF-16 LE

# 파이썬으로 UTF-8(무 BOM)로 깨끗하게 재저장
from pathlib import Path
p = Path(".env")
raw = p.read_text(encoding="utf-8-sig")  # UTF-8 BOM이면 제거, UTF-8이면 그대로
p.write_text(raw, encoding="utf-8")      # 무 BOM으로 저장
```

### 무엇을 선택할까?
- **가장 깔끔한 해결:** `.env`를 **UTF-8(무 BOM)** 으로 저장
- **코드로 방어:** `load_dotenv(encoding="utf-8-sig")` (단, 실제가 UTF-16이면 `utf-16`로 읽은 뒤 변환)

요약:  
레딧에서 말한 “인코더 코덱을 ‘utf-8-sig’로”는 **BOM이 붙은 UTF-8 파일을 다룰 때 `encoding='utf-8-sig'`로 읽어라**는 뜻이에요. 다만 현재 오류 패턴은 **UTF-16일 공산**이 커서, 먼저 바이트 시그니처를 확인한 뒤 **UTF-8(무 BOM)** 으로 바꿔 주는 걸 추천합니다.

---

### ❓ 질문 (User)
이거 BOM 있는 utf8 파일일 수도 있겠다

인코더 코덱을 ‘utf-8-sig’로 설정해 봐
---
레딧에 있는 해결방법인데 이게 무슨말 하는건지 알려줘
