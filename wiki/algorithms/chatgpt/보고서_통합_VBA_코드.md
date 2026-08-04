---
type: Concept
title: "보고서 통합 VBA 코드"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-05-23)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-05-23
status: active
---

# 보고서 통합 VBA 코드

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-05-23

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
아래는 Word VBA를 사용하여 `'보고서'` 폴더 내의 `3월 보고서.docx`, `4월 보고서.docx`, `5월 보고서.docx`를 하나의 문서로 통합하는 코드입니다.

> 📁 모든 파일이 동일한 폴더(`보고서`)에 있고, 실행하는 이 매크로는 **새 문서에서** 실행된다고 가정합니다.

---

### ✅ Word VBA 코드 (한글 주석 포함)

```vba
Sub 보고서_통합()

    Dim 문서 As Document
    Dim 병합문서 As Document
    Dim 파일경로 As String
    Dim 보고서폴더 As String
    Dim 파일이름 As Variant
    Dim 파일목록 As Variant
    Dim i As Integer

    ' 병합할 보고서 폴더 경로 (필요 시 경로 수정)
    보고서폴더 = ThisDocument.Path & "\보고서\"

    ' 통합할 문서 목록 (순서 중요)
    파일목록 = Array("3월 보고서.docx", "4월 보고서.docx", "5월 보고서.docx")

    ' 새 문서 생성
    Set 병합문서 = Documents.Add

    ' 파일들을 차례대로 열어서 복사 후 병합
    For i = 0 To UBound(파일목록)
        파일경로 = 보고서폴더 & 파일목록(i)

        ' 문서 열기
        Set 문서 = Documents.Open(FileName:=파일경로, ReadOnly:=True)

        ' 전체 내용 선택 후 복사
        문서.Content.Copy

        ' 병합문서 끝으로 이동 후 붙여넣기
        With 병합문서.Range
            .Collapse Direction:=wdCollapseEnd
            .Paste
            ' 문서 구분을 위해 페이지 나누기 삽입
            .InsertBreak Type:=wdPageBreak
        End With

        ' 원본 문서 닫기
        문서.Close SaveChanges:=False
    Next i

    MsgBox "보고서 병합이 완료되었습니다.", vbInformation

End Sub
```

---

### 📌 사용법

1. Word에서 새 문서를 열고 `Alt + F11` 눌러 **VBA 편집기** 실행
2. `삽입 > 모듈`을 클릭하여 새 모듈 추가
3. 위 코드를 붙여넣기
4. `F5` 또는 실행 버튼으로 매크로 실행

---

### 📁 주의사항

- `ThisDocument.Path`는 이 매크로가 있는 Word 문서가 저장된 경로를 기준으로 합니다.
- `보고서` 폴더는 매크로 실행 파일과 같은 위치에 있어야 합니다.
- 보고서 이름이 다를 경우 `파일목록 = Array(...)` 부분을 수정해 주세요.

필요 시 PDF로 저장하거나 목차 삽입까지도 도와드릴 수 있습니다.

---

### ❓ 질문 (User)
'보고서'폴더에 3개의 word 문서가 있어. 3월 보고서, 4월 보고서, 5월 보고서야.
세 개의 파일을 하나로 통합하는 word VBA 코드를 작성해줘.

### 💡 답변 (Assistant)
좋은 관찰이에요! 말씀하신 것처럼 **5월 보고서 아이콘이 다르다**는 것은 중요한 단서입니다. 해당 차이로 인해 **Word VBA 코드가 '5월 보고서'를 정상적으로 열지 못했을 가능성**이 매우 큽니다. 문제의 원인을 아래와 같이 정리해드릴게요.

---

### 🔍 아이콘이 다른 이유는?

#### ✅ 원인 가능성 1: **확장자가 .docx가 아님**
- 예: `.doc`, `.docm`, `.dotx`, `.rtf`, `.txt` 등일 수 있음
- 파일 확장자명이 달라서 VBA 코드에서 찾지 못한 것일 수 있어요.

#### ✅ 원인 가능성 2: **파일이 임시 파일 또는 바로가기일 수 있음**
- 아이콘이 살짝 투명하거나 바로가기 화살표가 있다면 `.lnk` 파일일 가능성이 있어요.
- 이 경우 Word 문서가 아니라 Word로 연결된 *바로가기*라 열 수 없습니다.

#### ✅ 원인 가능성 3: **파일 이름에 공백이 추가되었거나 다른 특수문자가 있을 수 있음**
- 육안으로는 `5월 보고서`처럼 보이지만, 실제 이름은 `5월 보고서 .docx` (공백 포함) 등일 수 있습니다.

---

### ✅ 해결 방법

1. **파일 확장자 확인**
   - 파일 탐색기에서 `보기 → 파일 확장명`을 체크하세요.
   - 확장자가 `.docx`인지 확인하세요.
   - 아니라면 `.docx`로 저장해 주세요.

2. **파일 이름 복사로 정확하게 확인**
   - `5월 보고서`에서 **오른쪽 클릭 → 이름 바꾸기 → Ctrl + A → Ctrl + C**로 이름을 복사하세요.
   - 그 이름을 VBA 코드의 `파일목록`에 그대로 붙여 넣으세요.

3. **수정된 이름 기반으로 VBA 코드 수정**
   예를 들어 실제 이름이 `5월 보고서.doc`라면 다음처럼 고칩니다.

   ```vba
   파일목록 = Array("3월 보고서.docx", "4월 보고서.docx", "5월 보고서.doc")
   ```

---

### 📌 추가 팁: 폴더 내 모든 Word 문서 자동 병합

위 문제를 방지하기 위해, 폴더 안에 있는 모든 `.doc` 또는 `.docx` 파일을 자동으로 불러오는 방식도 가능합니다.

필요하시면 이 방식으로도 VBA 코드를 수정해드릴게요.

---

확장자 확인해보시고, 필요하시면 수정된 파일 이름을 말씀해주세요. 바로 적용된 코드를 드릴 수 있어요!

---

### ❓ 질문 (User)
지금 통합이 안되고 있어. 5월 보고서가 존재하지 않는다고 시스템에서 알려주고 있어. 5월 보고서만 아이콘이 조금 다른데 이 부분은 뭐가 문제일까? 혹시 이 부분 때문에 통합이 되지 않는걸까?

### 💡 답변 (Assistant)
훌륭한 질문이에요!

### ✅ `.docm` 확장자란?

`.docm`은 **매크로(Macro)**가 포함된 Microsoft Word 문서 파일의 확장자입니다.

---

### 🔍 .docx vs .docm 차이점

| 확장자 | 설명 | 매크로 포함 가능 여부 |
|--------|------|------------------|
| `.docx` | 일반 Word 문서 (XML 기반) | ❌ 매크로 불가능 |
| `.docm` | 매크로 지원 Word 문서 | ✅ 매크로 가능 |

즉, `.docm`은 문서 안에 VBA 매크로 코드가 들어갈 수 있는 파일 형식이에요. 기능은 `.docx`와 거의 동일하지만, 보안상 매크로 실행을 경고할 수 있습니다.

---

### ⚠️ 왜 `.docm`은 VBA 코드에서 열리지 않았을까?

기본적으로 `.docm`도 `Documents.Open`으로 문제없이 열립니다. 다만 다음과 같은 경우 문제가 생길 수 있습니다.

1. **VBA 코드에서 확장자를 `.docx`로 지정했기 때문에** `"5월 보고서.docx"`를 찾았지만 실제 파일은 `.docm` → "파일 없음" 오류 발생
2. **보안 설정**에 의해 `.docm` 파일 열기가 차단되는 경우 (회사 환경에서)

---

### ✅ 해결 방법

현재 파일이 `.docm`이면, 다음처럼 VBA 코드를 **정확한 파일명으로 수정**하면 해결됩니다:

```vba
파일목록 = Array("3월 보고서.docx", "4월 보고서.docx", "5월 보고서.docm")
```

---

### 🔄 또는 모든 `.docx` 및 `.docm` 자동 병합 코드로 전환

```vba
Sub 보고서_자동병합()

    Dim 병합문서 As Document
    Dim 파일 As String
    Dim 보고서폴더 As String

    보고서폴더 = ThisDocument.Path & "\보고서\"
    Set 병합문서 = Documents.Add

    ' .docx 및 .docm 파일 병합
    파일 = Dir(보고서폴더 & "*.doc*")
    Do While 파일 <> ""
        If Right(파일, 1) <> "~" Then ' 임시파일 제외
            Dim 문서 As Document
            Set 문서 = Documents.Open(FileName:=보고서폴더 & 파일, ReadOnly:=True)
            문서.Content.Copy
            With 병합문서.Range
                .Collapse Direction:=wdCollapseEnd
                .Paste
                .InsertBreak Type:=wdPageBreak
            End With
            문서.Close SaveChanges:=False
        End If
        파일 = Dir
    Loop

    MsgBox "모든 보고서 문서가 성공적으로 통합되었습니다.", vbInformation

End Sub
```

이 코드는 `.docx`와 `.docm` 파일을 **자동으로 모두 통합**합니다. 훨씬 유연하고 오류에 강한 방식이니 이걸 사용하셔도 좋아요.

원하시는 방식으로 이어서 도와드릴게요!

---

### ❓ 질문 (User)
5월 보고서는 5월 보고서.docm 확장자로 되어있어. .docm은 어떤 확장자야?
