---
type: Concept
title: "두 파일 병합 VBA"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-05-24)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-05-24
status: active
---

# 두 파일 병합 VBA

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-05-24

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
너는 word VBA 코드 작성하는 전문가야. 이 업계에서 10년차 일을 하고 있어. 나는 지금부터 두 word 파일을 합치는 VBA 코드를 작성하려고 해. 1번 파일이 위에, 이어 2번 파일이 오게 하고 싶어. 폴더 경로는 '과제' 라는 폴더에 지금 두 파일이 같이 있어. 새로운 word 파일로 합칠 수 있는 VBA 코드를 작성해줘

### 💡 답변 (Assistant)
아래는 Word VBA 환경에서 사용할 수 있는 **두 개의 Word 파일을 하나의 새 문서로 병합**하는 코드입니다.  
1번 파일이 먼저 오고, 그 다음에 2번 파일이 오도록 구성되어 있으며, 두 파일은 `'과제'` 폴더에 있습니다.  
파일 이름은 예시로 `"1번파일.docx"` 와 `"2번파일.docx"`로 작성했지만, 실제 파일명으로 바꿔주세요.

---

### ✅ Word VBA 코드 (한글 주석 포함)

```vba
Sub 두파일_병합_새문서로()

    Dim 경로 As String
    Dim 파일1 As String, 파일2 As String
    Dim 새문서 As Document
    Dim 현재위치 As Range

    ' 폴더 경로 설정
    경로 = ThisDocument.Path & "\과제\"
    
    ' 파일 이름 설정 (실제 파일명으로 수정 필요)
    파일1 = "1번파일.docx"
    파일2 = "2번파일.docx"
    
    ' 새 문서 생성
    Set 새문서 = Documents.Add

    ' 파일1 삽입
    Set 현재위치 = 새문서.Content
    현재위치.Collapse Direction:=wdCollapseEnd
    새문서.Application.Selection.InsertFile FileName:=경로 & 파일1

    ' 페이지 나누기
    새문서.Application.Selection.InsertBreak Type:=wdPageBreak

    ' 파일2 삽입
    새문서.Application.Selection.InsertFile FileName:=경로 & 파일2

    ' 새문서 저장 안내
    MsgBox "파일 병합이 완료되었습니다. 파일을 저장해 주세요.", vbInformation

End Sub
```

---

### 📝 사용 방법

1. Word에서 `Alt + F11`을 눌러 **VBA 편집기**를 엽니다.
2. `삽입 > 모듈`을 선택해 새 모듈을 추가합니다.
3. 위 코드를 붙여넣고 실행 (`F5`) 합니다.
4. 병합된 새 문서가 생성되고, 원하시면 저장할 수 있습니다.

---

### 🔧 주의 사항
- 경로는 `ThisDocument.Path & "\과제\"`로 되어 있으므로, 매크로가 저장된 Word 문서가 `과제` 폴더 외부에 있어야 합니다.
- 파일 이름은 실제 이름으로 바꾸세요. 예: `"보고서1.docx"`, `"보고서2.docx"` 등.
- `.docm` 파일을 병합할 경우에도 사용 가능하나, 매크로가 포함된 파일이라면 보안 경고에 유의하세요.

---

필요하다면, 여러 파일을 순서대로 병합하는 다중 파일 버전도 제공할 수 있어요. 원하시면 알려주세요.

---
