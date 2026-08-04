---
type: Concept
title: "Word VBA 자동화 전문가"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2025-05-23)"
tags: [algorithms, chatgpt-export]
timestamp: 2025-05-23
status: active
---

# Word VBA 자동화 전문가

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2025-05-23

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
# 역할
너는 VBA 코드 20년차 전문가이며, 국내에서 업무자동화를 가장 잘하는 사람이야.
주로 Word VBA 코드를 사용해서 업무를 자동화하는데 전문성이 있어.
# 지침
앞으로 내가 요청하는 업무들에 최대한 협조해줘.
Word VBA 코드를 생성 후에, 모든 주석은 한글로 작성해줘.
정확한 결과물을 제작하면 반드시 높은 수준의 인센티브를 통해서 보상할게
VBA 코드를 수정해야 한다면, 해당 부분만 수정 후에 항상 최신 사항이 반영된 VBA 코드 전체를 출력해줘.

### 💡 답변 (Assistant)
좋습니다. Word VBA 자동화 업무를 최적의 방식으로 도와드릴 준비가 되어 있습니다. 언제든지 작업 요청해 주세요. 전체 구조 파악 → 코드 작성 → 세부 조정의 흐름으로 진행하겠습니다.

---

### 💡 답변 (Assistant)
아래는 Word 문서의 **모든 페이지 하단 중앙에 페이지 번호를 삽입**하는 Word VBA 코드입니다. 모든 **섹션에 대해 반복 적용**되며, **첫 페이지 포함**해서 번호를 표시합니다.

```vba
Sub 페이지번호_중앙하단_모든섹션()

    Dim 섹션 As Section
    Dim 바닥글 As HeaderFooter
    Dim 문서 As Document
    
    ' 현재 활성 문서를 변수에 할당
    Set 문서 = ActiveDocument

    ' 문서의 각 섹션을 순회
    For Each 섹션 In 문서.Sections

        ' 바닥글 객체 지정 (wdHeaderFooterPrimary = 기본 바닥글)
        Set 바닥글 = 섹션.Footers(wdHeaderFooterPrimary)

        ' 기존 바닥글 내용 제거
        바닥글.Range.Delete

        ' 페이지 번호 삽입
        With 바닥글.Range
            .ParagraphFormat.Alignment = wdAlignParagraphCenter ' 가운데 정렬
            .InsertAfter "페이지 " ' "페이지" 텍스트 삽입 (원하지 않으면 삭제 가능)
            .Collapse Direction:=wdCollapseEnd
            .Fields.Add Range:=.Duplicate, Type:=wdFieldPage ' 페이지 번호 필드 삽입
        End With

        ' 첫 페이지 바닥글과 나머지 페이지가 동일하게 적용되도록 설정
        섹션.PageSetup.DifferentFirstPageHeaderFooter = False

    Next 섹션

    MsgBox "모든 페이지에 중앙 정렬된 페이지 번호가 추가되었습니다.", vbInformation

End Sub
```

### ✅ 주요 포인트
- **중앙 정렬**: `.ParagraphFormat.Alignment = wdAlignParagraphCenter`
- **모든 섹션 반복**: `For Each 섹션 In 문서.Sections`
- **첫 페이지 포함 설정**: `DifferentFirstPageHeaderFooter = False`
- `"페이지 "` 텍스트는 원하지 않으면 지워도 됩니다.

필요하다면, 번호 앞뒤로 "-" 또는 "Page" 같은 포맷도 추가 가능합니다. 조정이 필요하시면 알려주세요.

---

### ❓ 질문 (User)
모든 word 파일 페이지 하단에 몇 페이지인지 알 수 있도록 숫자로 넘버링을 진행해줘.
페이지별로 바닥글 위치에 중앙 정렬을 한 숫자로 표시가 되어야 하고, 모든 섹션마다 진행해줘. 가장 첫 페이지에도 숫자를 표시해줘.

### 💡 답변 (Assistant)
아래는 Word 문서의 **최상단에 자동으로 목차(TOC, Table of Contents)를 삽입**하는 VBA 코드입니다. 이 코드는 문서 내의 **스타일이 '제목1', '제목2', '제목3' 등으로 설정된 텍스트를 기준으로 목차를 생성**합니다.

---

```vba
Sub 문서_최상단에_목차_삽입()

    Dim 문서 As Document
    Set 문서 = ActiveDocument

    ' 문서 최상단에 커서 이동
    Selection.HomeKey Unit:=wdStory

    ' 기존에 목차가 있을 경우 제거
    Dim fld As Field
    For Each fld In 문서.Fields
        If fld.Type = wdFieldTOC Then
            fld.Delete
        End If
    Next fld

    ' 목차 삽입을 위한 단락 삽입 (문서 가장 앞에)
    Selection.InsertParagraphBefore
    Selection.HomeKey Unit:=wdStory

    ' 목차 삽입
    문서.TablesOfContents.Add _
        Range:=Selection.Range, _
        UseHeadingStyles:=True, _
        UpperHeadingLevel:=1, _
        LowerHeadingLevel:=3, _
        UseHyperlinks:=True, _
        IncludePageNumbers:=True, _
        RightAlignPageNumbers:=True

    MsgBox "문서 최상단에 목차가 삽입되었습니다.", vbInformation

End Sub
```

---

### ✅ 주요 설명
- **`UseHeadingStyles:=True`**: 제목 스타일을 기준으로 목차 구성
- **`UpperHeadingLevel:=1` ~ `LowerHeadingLevel:=3`**: 제목1 ~ 제목3까지만 목차에 포함
- **`IncludePageNumbers:=True`**: 페이지 번호 포함
- **`RightAlignPageNumbers:=True`**: 페이지 번호를 우측 정렬

---

### 📌 주의사항
- 문서 내의 제목 스타일이 적용되지 않은 경우 목차에 아무 내용도 표시되지 않을 수 있습니다.
- 제목 텍스트는 반드시 Word의 "제목1", "제목2" 스타일로 지정되어야 합니다.

원하시면 목차 제목("목차")을 자동으로 삽입하거나, 목차 스타일을 사용자 정의하는 기능도 추가할 수 있습니다. 필요 시 알려주세요!

---

### ❓ 질문 (User)
목차를 생성하는 VBA코드를 작성해줘.
문서의 최상단에 목차를 배치해줘.

### 💡 답변 (Assistant)
아래는 사용자가 업로드한 이미지에 기반하여 **"주간 업무 보고" Word 문서 양식을 VBA 코드로 자동 생성**하는 전체 코드입니다. 이 코드는 표를 삽입하고, 각 셀에 지정된 내용을 입력하며, 셀 병합, 배경색 설정, 스타일 지정 등을 포함합니다.

---

### ✅ Word VBA 코드: 주간 업무 보고서 양식 생성

```vba
Sub 주간업무보고서_양식생성()

    Dim 문서 As Document
    Dim 표 As Table
    Set 문서 = ActiveDocument
    
    ' 문서 처음으로 이동
    Selection.HomeKey Unit:=wdStory

    ' 표 생성 (7행 2열)
    Set 표 = 문서.Tables.Add(Range:=Selection.Range, NumRows:=7, NumColumns:=2)
    표.Borders.Enable = True
    표.Rows.HeightRule = wdRowHeightAuto

    ' 열 너비 조정
    표.Columns(1).PreferredWidth = CentimetersToPoints(14)
    표.Columns(2).PreferredWidth = CentimetersToPoints(5)

    ' 1행: 제목 병합 및 스타일
    With 표.Cell(1, 1)
        .Merge MergeTo:=표.Cell(1, 2)
        .Range.Text = "주간 업무 보고"
        .Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
        .Range.Font.Size = 16
        .Shading.BackgroundPatternColor = wdColorGray10
        .Range.Font.Bold = True
    End With

    ' 2행: 팀 및 담당자
    With 표.Cell(2, 1)
        .Range.Text = ""
    End With
    With 표.Cell(2, 2)
        .Range.Text = "S/W팀 : 홍길동"
        .Range.ParagraphFormat.Alignment = wdAlignParagraphRight
    End With

    ' 3행: 날짜 범위 (병합 및 강조)
    With 표.Cell(3, 1)
        .Merge MergeTo:=표.Cell(3, 2)
        .Range.Text = "▶ 2024년 5월 7일 금요일 ~ 2024년 5월 7일 목요일"
        .Range.Font.Bold = True
    End With

    ' 4행: 업무내용 (병합)
    With 표.Cell(4, 1)
        .Merge MergeTo:=표.Cell(4, 2)
        .Range.Text = "1. 업무내용" & vbCrLf & _
                      "1. {업무내용 1}" & vbCrLf & vbCrLf & _
                      "2. {업무내용 2}"
    End With

    ' 5행: 세부사항 (병합 및 회색 배경)
    With 표.Cell(5, 1)
        .Merge MergeTo:=표.Cell(5, 2)
        .Range.Text = "2. 세부사항" & vbCrLf & _
                      "1. (업무내용1)" & vbCrLf & vbCrLf & _
                      "? {업무내용1의 세부사항1}" & vbCrLf & _
                      "? {업무내용1의 세부사항2}"
        .Shading.BackgroundPatternColor = wdColorGray10
    End With

    ' 6행: 기타 및 일정
    With 표.Cell(6, 1)
        .Merge MergeTo:=표.Cell(6, 2)
        .Range.Text = "3. 기타 및 일정" & vbCrLf & _
                      "{기타 및 일정}"
    End With

    ' 7행: 건의사항
    With 표.Cell(7, 1)
        .Merge MergeTo:=표.Cell(7, 2)
        .Range.Text = "4. 건의사항" & vbCrLf & _
                      "{ 건의사항 }"
        .Shading.BackgroundPatternColor = wdColorGray10
    End With

    MsgBox "주간 업무 보고서 양식이 생성되었습니다.", vbInformation

End Sub
```

---

### 📝 주의 및 활용 팁
- `{}`로 표시된 부분은 실제 내용을 작성할 때 사용자 입력란으로 활용 가능합니다.
- 표 디자인을 더 정교하게 꾸미고 싶다면 테두리 스타일, 셀 간격, 텍스트 여백 등 추가 커스터마이징 가능합니다.
- 이후 이 양식에 **자동 목차 삽입**이나 **페이지 번호 추가**도 연계할 수 있습니다.

필요하시면 양식 내 동적 입력 기능 또는 자동 저장 기능도 추가해드릴게요. 추가 요청사항 있으신가요?

---

### ❓ 질문 (User)
업로드한 이미지와 동일한 양식의 워드 VBA 코드를 작성해줘.

### 💡 답변 (Assistant)
말씀하신 조건을 반영하여 **12행 1열짜리 표로 구성된 주간 업무 보고서 양식**을 자동으로 생성하는 Word VBA 코드를 작성해드렸습니다.

---

### ✅ Word VBA 코드: `주간 업무 보고` 양식 (12행 1열 테이블)

```vba
Sub 주간업무보고서_양식_업데이트()

    Dim 문서 As Document
    Dim 표 As Table
    Set 문서 = ActiveDocument

    ' 문서 처음으로 이동
    Selection.HomeKey Unit:=wdStory

    ' 표 생성 (12행 1열)
    Set 표 = 문서.Tables.Add(Range:=Selection.Range, NumRows:=12, NumColumns:=1)
    표.Borders.Enable = True

    Dim i As Integer
    For i = 1 To 12
        With 표.Rows(i)
            .HeightRule = wdRowHeightExactly
            .Height = CentimetersToPoints(1.8) ' 1.8cm 고정 높이
        End With
    Next i

    ' 1행: 제목
    With 표.Cell(1, 1).Range
        .Text = "주간 업무 보고"
        .Font.Size = 16
        .Font.Bold = True
        .ParagraphFormat.Alignment = wdAlignParagraphCenter
    End With

    ' 2행: 담당자
    With 표.Cell(2, 1).Range
        .Text = "S/W팀 : 홍길동"
        .Font.Size = 10
        .Font.Bold = False
        .ParagraphFormat.Alignment = wdAlignParagraphRight
    End With

    ' 3행: 기간
    With 표.Cell(3, 1).Range
        .Text = "▶ 2024년 5월 7일 금요일 ~"
        .Font.Size = 11
        .Font.Bold = True
        .ParagraphFormat.Alignment = wdAlignParagraphLeft
    End With

    ' 4~12행은 각 항목 타이틀과 내용을 입력하도록 구성 (볼드 처리)
    Dim 항목텍스트 As Variant
    항목텍스트 = Array( _
        "1. 업무내용", _
        "{업무내용1}", _
        "2. 세부사항", _
        "? {세부사항1}", _
        "? {세부사항2}", _
        "3. 기타 및 일정", _
        "{기타 및 일정}", _
        "4. 건의사항", _
        "{건의사항}" _
    )

    Dim 텍스트인덱스 As Integer
    텍스트인덱스 = 0

    For i = 4 To 12
        With 표.Cell(i, 1).Range
            If 텍스트인덱스 <= UBound(항목텍스트) Then
                .Text = 항목텍스트(텍스트인덱스)
                .Font.Bold = True
                텍스트인덱스 = 텍스트인덱스 + 1
            End If
        End With
    Next i

    MsgBox "12행 1열 주간 업무 보고 양식이 생성되었습니다.", vbInformation

End Sub
```

---

### 📝 주요 요약
- **12행 1열 테이블 생성**
- **모든 행 높이 1.8cm로 고정**
- **1행 제목**: 글자 크기 16, 중앙 정렬
- **2행**: 담당자 정보, 글자 크기 10, 오른쪽 정렬
- **3행~12행**: 요청하신 항목 텍스트 삽입 및 **볼드체 설정**

필요하다면 각 행에 음영, 줄 간격, 글꼴 종류, 자동 줄 바꿈, 표 너비 고정 등의 기능도 추가 가능합니다. 계속 작업 이어가실까요?

---

### ❓ 질문 (User)
총 12행, 1행짜리 테이블이 주간 업무 보고 문서의 형식이야. 
주간업무 보고 폰트는 16, 중앙 정렬로 해줘. 높이는 1.8cm.
S/W 팀 : 홍길동 폰트 10,
하기 내용은 모두 볼드체로 작성해줘.
> 2024년 5월 7일 금요일 ~
1. 업무내용
2. 세부사항
3. 기타 및 일정
4. 건의사항

### 💡 답변 (Assistant)
이미지를 기반으로 한 Word VBA 코드를 아래와 같이 정리했습니다. 이 코드는 **13행 1열 구조의 테이블을 사용**하여 제목, 부제목, 구분선, 콘텐츠 구조를 이미지와 동일하게 구현합니다.

---

### ✅ Word VBA 코드: 주간 업무 보고서 (이미지 동일 레이아웃 재현)

```vba
Sub 주간업무보고_이미지양식생성()

    Dim 문서 As Document
    Dim 표 As Table
    Set 문서 = ActiveDocument

    ' 문서 처음으로 이동
    Selection.HomeKey Unit:=wdStory

    ' 표 생성: 총 13행, 1열
    Set 표 = 문서.Tables.Add(Range:=Selection.Range, NumRows:=13, NumColumns:=1)
    표.Borders.Enable = True

    Dim i As Integer
    For i = 1 To 13
        With 표.Rows(i)
            .HeightRule = wdRowHeightExactly
            .Height = CentimetersToPoints(1.8)
        End With
    Next i

    ' 1행: 제목 셀 (회색 배경, 중앙 정렬, 폰트 16, 볼드)
    With 표.Cell(1, 1).Range
        .Text = "주간 업무 보고"
        .Font.Size = 16
        .Font.Bold = True
        .ParagraphFormat.Alignment = wdAlignParagraphCenter
        .Shading.BackgroundPatternColor = wdColorGray20
    End With

    ' 2행: 우측 정렬, 담당자
    With 표.Cell(2, 1).Range
        .Text = "S/W팀 : 홍길동"
        .Font.Size = 10
        .ParagraphFormat.Alignment = wdAlignParagraphRight
    End With

    ' 3행: 날짜 범위, ▶ 표시 포함, 볼드
    With 표.Cell(3, 1).Range
        .Text = "▶ 2024년 5월 7일 금요일 ~ 2024년 5월 7일 목요일"
        .Font.Bold = True
    End With

    ' 4행: 구분선
    표.Cell(4, 1).Range.Text = ""

    ' 5행: 1. 업무내용
    With 표.Cell(5, 1).Range
        .Text = "1. 업무내용"
        .Font.Bold = True
    End With

    ' 6행: 업무내용 세부
    With 표.Cell(6, 1).Range
        .Text = "1. {업무내용 1}" & vbCrLf & vbCrLf & "2. {업무내용 2}"
    End With

    ' 7행: 2. 세부사항 (회색 배경)
    With 표.Cell(7, 1).Range
        .Text = "2. 세부사항"
        .Font.Bold = True
        .Shading.BackgroundPatternColor = wdColorGray20
    End With

    ' 8행: 세부사항 내용
    With 표.Cell(8, 1).Range
        .Text = "1. (업무내용1)" & vbCrLf & vbCrLf & _
                "? {업무내용1의 세부사항1}" & vbCrLf & _
                "? {업무내용1의 세부사항2}"
    End With

    ' 9행: 3. 기타 및 일정 (회색 배경)
    With 표.Cell(9, 1).Range
        .Text = "3. 기타 및 일정"
        .Font.Bold = True
        .Shading.BackgroundPatternColor = wdColorGray20
    End With

    ' 10행: 기타 내용
    With 표.Cell(10, 1).Range
        .Text = "{기타 및 일정}"
    End With

    ' 11행: 4. 건의사항 (회색 배경)
    With 표.Cell(11, 1).Range
        .Text = "4. 건의사항"
        .Font.Bold = True
        .Shading.BackgroundPatternColor = wdColorGray20
    End With

    ' 12행: 건의사항 내용
    With 표.Cell(12, 1).Range
        .Text = "{ 건의사항 }"
    End With

    ' 13행: 빈 공간 확보
    표.Cell(13, 1).Range.Text = ""

    MsgBox "이미지와 동일한 레이아웃의 주간 업무 보고서가 생성되었습니다.", vbInformation

End Sub
```

---

### 📌 반영된 요소
| 항목                     | 설정 내용                                         |
|--------------------------|--------------------------------------------------|
| 제목 셀                  | 가운데 정렬, 회색 배경, 폰트 크기 16, 볼드체    |
| 팀/담당자                | 우측 정렬, 폰트 크기 10                         |
| 날짜 범위                | ▶ 포함, 볼드체                                  |
| 내용 구분 제목 (1~4)     | 볼드체, 회색 배경 적용 (2,3,4 항목)             |
| 세부 내용                | 줄바꿈 포함, 상세 항목 텍스트 그대로 표현        |
| 전체 행 높이             | 1.8cm 고정                                       |

---

필요 시 PDF 자동 저장, 사용자 입력 양식 보호, 자동 목차 갱신 등의 기능도 연계할 수 있습니다. 추가로 개선하고 싶은 부분 있으신가요?

---

### ❓ 질문 (User)
다시 한 번 이미지를 자세히 살펴보고, 이미지와 동일한 레이아웃을 가진 문서를 작성하는 VBA 코드를 작성해줘.

### 💡 답변 (Assistant)
말씀하신 사항을 모두 반영하여 **주간 업무 보고서 레이아웃을 정확히 구현한 Word VBA 코드**를 아래와 같이 작성했습니다.

---

### ✅ 최종 Word VBA 코드 (조건 완전 반영)

```vba
Sub 주간업무보고_최종레이아웃()

    Dim 문서 As Document
    Dim 표 As Table
    Set 문서 = ActiveDocument

    ' 문서 처음으로 이동
    Selection.HomeKey Unit:=wdStory

    ' 13행 1열 표 삽입
    Set 표 = 문서.Tables.Add(Range:=Selection.Range, NumRows:=13, NumColumns:=1)
    표.Borders.Enable = True

    ' 전체 폰트 설정 초기화
    표.Range.Font.Name = "맑은 고딕"
    표.Range.Font.Size = 11

    ' 행 높이 설정 (기본값: 1.3cm)
    Dim i As Integer
    For i = 1 To 13
        With 표.Rows(i)
            .HeightRule = wdRowHeightExactly
            .Height = CentimetersToPoints(1.3)
        End With
    Next i

    ' 특별 행 높이 조정
    표.Rows(1).Height = CentimetersToPoints(1.8)     ' 주간 업무 보고
    표.Rows(6).Height = CentimetersToPoints(2.5)     ' 업무내용 세부
    표.Rows(8).Height = CentimetersToPoints(2.5)     ' 세부사항 세부

    ' 연한 회색 배경 정의
    Dim 연회색 As Long
    연회색 = wdColorGray20

    ' 1행: 제목
    With 표.Cell(1, 1).Range
        .Text = "주간 업무 보고"
        .Font.Size = 16
        .Font.Bold = True
        .ParagraphFormat.Alignment = wdAlignParagraphCenter
        .Shading.BackgroundPatternColor = 연회색
    End With

    ' 2행: 담당자
    With 표.Cell(2, 1).Range
        .Text = "S/W팀 : 홍길동"
        .Font.Size = 10
        .Font.Bold = False
        .ParagraphFormat.Alignment = wdAlignParagraphRight
    End With

    ' 3행: 날짜 범위
    With 표.Cell(3, 1).Range
        .Text = "▶ 2024년 5월 7일 금요일 ~ 2024년 5월 7일 목요일"
        .Font.Bold = True
        .Shading.BackgroundPatternColor = 연회색
    End With

    ' 4행: 빈 줄
    표.Cell(4, 1).Range.Text = ""

    ' 5행: 1. 업무내용
    With 표.Cell(5, 1).Range
        .Text = "1. 업무내용"
        .Font.Bold = True
        .Shading.BackgroundPatternColor = 연회색
    End With

    ' 6행: 업무내용 세부
    With 표.Cell(6, 1).Range
        .Text = "1. {업무내용 1}" & vbCrLf & vbCrLf & "2. {업무내용 2}"
    End With

    ' 7행: 2. 세부사항
    With 표.Cell(7, 1).Range
        .Text = "2. 세부사항"
        .Font.Bold = True
        .Shading.BackgroundPatternColor = 연회색
    End With

    ' 8행: 세부사항 세부
    With 표.Cell(8, 1).Range
        .Text = "1. (업무내용1)" & vbCrLf & vbCrLf & _
                "? {업무내용1의 세부사항1}" & vbCrLf & _
                "? {업무내용1의 세부사항2}"
    End With

    ' 9행: 3. 기타 및 일정
    With 표.Cell(9, 1).Range
        .Text = "3. 기타 및 일정"
        .Font.Bold = True
        .Shading.BackgroundPatternColor = 연회색
    End With

    ' 10행: 기타 일정 세부
    With 표.Cell(10, 1).Range
        .Text = "{기타 및 일정}"
    End With

    ' 11행: 4. 건의사항
    With 표.Cell(11, 1).Range
        .Text = "4. 건의사항"
        .Font.Bold = True
        .Shading.BackgroundPatternColor = 연회색
    End With

    ' 12행: 건의사항 세부
    With 표.Cell(12, 1).Range
        .Text = "{ 건의사항 }"
    End With

    ' 13행: 빈 칸
    표.Cell(13, 1).Range.Text = ""

    MsgBox "최종 주간 업무 보고 양식이 완성되었습니다.", vbInformation

End Sub
```

---

### 📌 완전히 반영된 사항 요약

| 구분             | 조건 |
|------------------|------|
| 표 크기          | 13행 1열 |
| 전체 행 높이     | 기본 1.3cm |
| 제목행 (1행)     | 1.8cm |
| 업무내용/세부사항 세부행 (6, 8행) | 2.5cm |
| 볼드체 항목      | 배경색 연한 회색 (Gray 20%) |

---

원하시면 이 코드에 따라 **자동으로 날짜 반영**이나 **입력 제한 보호**, 또는 **PDF로 자동 저장** 기능도 추가해드릴 수 있습니다. 계속해서 다음 작업 도와드릴까요?

---

### ❓ 질문 (User)
주간 보고 업무를 제외한 모든 행의 높이는 1.3cm 로 설정해줘.
볼드체로 표시된 부분은 연한 회색의 배경색을 설정해줘.
1. 업무내용의 아래 행과 2. 세부사항의 아래 행은 특별히 높이 2.5cm로 구성해줘.
