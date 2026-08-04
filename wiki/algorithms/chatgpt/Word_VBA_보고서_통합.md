---
type: Concept
title: "Word VBA 보고서 통합"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-05-23)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-05-23
status: active
---

# Word VBA 보고서 통합

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-05-23

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
아래는 Word VBA를 사용해 `보고서` 폴더에 있는 `3월 보고서.docx`, `4월 보고서.docx`, `5월 보고서.docx` 파일을 하나의 문서로 통합하는 코드입니다.

```vba
Sub 보고서_통합()

    Dim 통합문서 As Document
    Dim 파일경로 As String
    Dim 폴더경로 As String
    Dim 파일목록 As Variant
    Dim i As Integer

    ' 보고서 폴더 경로 (필요시 경로를 사용자 환경에 맞게 수정)
    폴더경로 = "C:\Users\사용자이름\Documents\보고서\"
    
    ' 통합 대상 파일명 리스트
    파일목록 = Array("3월 보고서.docx", "4월 보고서.docx", "5월 보고서.docx")
    
    ' 새 문서 생성
    Set 통합문서 = Documents.Add
    
    ' 각 보고서 파일을 불러와서 복사 후 붙여넣기
    For i = LBound(파일목록) To UBound(파일목록)
        파일경로 = 폴더경로 & 파일목록(i)
        
        If Dir(파일경로) <> "" Then
            Dim 개별문서 As Document
            Set 개별문서 = Documents.Open(FileName:=파일경로, ReadOnly:=True)
            
            ' 내용 복사
            개별문서.Content.Copy
            
            ' 통합 문서에 붙여넣기
            With 통합문서
                .Content.Collapse Direction:=wdCollapseEnd
                .Content.InsertBreak Type:=wdPageBreak
                .Content.Paste
            End With
            
            개별문서.Close SaveChanges:=False
        Else
            MsgBox 파일목록(i) & " 파일을 찾을 수 없습니다.", vbExclamation
        End If
    Next i
    
    MsgBox "보고서 통합이 완료되었습니다.", vbInformation

End Sub
```

### ✅ 사용 전 확인사항
1. `폴더경로`는 실제 파일이 저장된 경로로 정확히 수정하세요.
2. 파일명이 정확히 `3월 보고서.docx`와 같은지 확인하세요.
3. 기존 열려 있는 문서는 모두 저장하고 닫아두는 것이 좋습니다.

필요 시 자동으로 문서 저장까지 추가해드릴 수도 있습니다. 원하시나요?

---

### ❓ 질문 (User)
'보고서' 폴더에 3개의 word 문서가 있어. 3월 보고서, 4월 보고서, 5월 보고서야.
세 개의 파일을 하나로 통합하는 word VBA 코드를 작성해줘.

### 💡 답변 (Assistant)
알겠습니다. 아래는 Word VBA 환경에서 안정적으로 작동하는 **보고서 통합 매크로 코드**입니다. 세 개의 Word 문서(3월, 4월, 5월 보고서)를 하나의 새 문서에 **순차적으로 병합**합니다.

---

### ✅ **최종 코드:**

```vba
Sub 보고서_통합_최종()

    Dim 통합문서 As Document
    Dim 대상문서 As Document
    Dim 파일경로 As String
    Dim 폴더경로 As String
    Dim 파일이름들 As Variant
    Dim i As Integer

    ' === 폴더 경로를 사용자 환경에 맞게 수정하세요 ===
    폴더경로 = "C:\Users\사용자이름\Documents\보고서\"
    
    ' 병합할 파일 이름들 (확장자까지 정확히)
    파일이름들 = Array("3월 보고서.docx", "4월 보고서.docx", "5월 보고서.docx")
    
    ' 새 문서 생성 (통합 문서)
    Set 통합문서 = Documents.Add

    ' 반복문으로 각 파일 열고 복사 후 붙여넣기
    For i = LBound(파일이름들) To UBound(파일이름들)
        
        파일경로 = 폴더경로 & 파일이름들(i)
        
        If Dir(파일경로) <> "" Then
            ' 대상 문서 열기
            Set 대상문서 = Documents.Open(FileName:=파일경로, ReadOnly:=True)

            ' 대상 문서의 모든 내용 복사
            대상문서.Range.Copy

            ' 통합 문서에 페이지 구분 후 붙여넣기
            With 통합문서
                If .Range.End > 0 Then
                    .Range.Collapse Direction:=wdCollapseEnd
                    .Range.InsertBreak Type:=wdPageBreak
                End If
                .Range.Collapse Direction:=wdCollapseEnd
                .Range.Paste
            End With

            ' 대상 문서 닫기
            대상문서.Close SaveChanges:=False
        Else
            MsgBox "파일 없음: " & 파일경로, vbExclamation
        End If
    Next i
    
    MsgBox "보고서 통합이 완료되었습니다.", vbInformation

End Sub
```

---

### 📌 **사용법 요약**
1. Word VBA 편집기(Alt + F11)에서 위 코드를 `Module`에 붙여넣기.
2. `폴더경로`를 실제 경로로 수정 (`C:\Users\Jeongmin\Documents\보고서\` 형태 등).
3. 매크로 실행 (F5 또는 Word에서 매크로 실행).

---

필요하시면 다음 기능도 추가해드릴 수 있어요:
- 병합한 문서를 자동 저장
- 각 문서 앞에 제목(예: `# 3월 보고서`) 삽입
- 병합 후 목차 생성

어떤 게 더 필요하신가요?

---

### ❓ 질문 (User)
통합이 이루어지지 않는데 다시 한 번 작성해줘
