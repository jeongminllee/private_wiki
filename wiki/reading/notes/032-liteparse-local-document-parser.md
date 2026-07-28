---
type: Reference
title: "LiteParse: 로컬 문서 파싱과 선택적 OCR"
description: "PDFium 기반 공간 텍스트 추출과 선택적 OCR을 결합한 빠른 로컬 문서 파서의 구조와 한계"
resource: https://discuss.pytorch.kr/t/liteparse-pdf/10524
notion: https://app.notion.com/p/3881a73cf20b818fa313cfe79cc31714
tags: [reading, pdf, ocr, document-parsing, local-first]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

LiteParse는 LlamaIndex가 공개한 로컬 우선 문서 파서다. PDF의 모든 페이지를 이미지로 바꿔 OCR하는 대신 PDFium으로 원래 텍스트와 위치 정보를 먼저 읽고, 텍스트가 부족한 영역이나 이미지에만 OCR을 적용한다. 빠른 1차 수집, 개인정보가 있는 로컬 문서, 대량 배치 처리에 적합한 방향이다.

# 처리 구조

- PDF에서는 PDFium으로 글자와 bounding box를 추출한다.
- native text와 OCR 결과를 위치 기준으로 합치고, grid projection으로 줄과 레이아웃을 복원한다.
- PDF, DOCX, XLSX, PPTX, 이미지를 입력으로 받는다. 비PDF 문서는 LibreOffice 또는 ImageMagick을 통한 변환이 필요할 수 있다.
- 구조화 JSON, 레이아웃을 살린 텍스트, 페이지 스크린샷을 출력한다.
- Rust 코어 위에 Python, Node.js, WASM, CLI 바인딩을 제공한다.
- Tesseract를 기본 OCR로 사용할 수 있고 EasyOCR, PaddleOCR, 사용자 정의 HTTP OCR API도 연결할 수 있다.

CLI는 단일 문서 파싱과 배치 파싱, 스크린샷 생성 같은 흐름을 제공한다. 로컬 실행이므로 외부 SaaS에 원문을 보내지 않고 파이프라인을 구성할 수 있다는 점이 중요하다.

# 이 wiki에 적용하기

정보처리기사 PDF처럼 native text와 스캔 이미지가 섞인 자료는 먼저 LiteParse로 구조와 텍스트를 추출하고, 품질이 낮은 페이지만 별도 OCR과 원본 이미지 대조 대상으로 보내는 방식이 가능하다. 출력 JSON의 좌표를 유지하면 Markdown에서 깨진 문장이 어느 페이지·영역에서 왔는지 추적하기도 쉽다.

권장 파이프라인은 다음과 같다.

1. native text 비율과 OCR 적용 영역을 기록한다.
2. 표, 코드, 수식 페이지를 별도 분류한다.
3. 자동 교정 전 추출 JSON을 `raw/`에 보존한다.
4. 교정한 Markdown과 페이지 번호를 연결한다.
5. 샘플 페이지를 이미지와 비교해 누락·순서 뒤섞임을 검사한다.

# 한계

복잡한 표, 다단 편집, 차트, 필기, 품질이 낮은 스캔에서는 읽기 순서와 셀 구조를 안정적으로 복원하지 못할 수 있다. 이런 문서는 시각 모델이나 LlamaParse 같은 무거운 파서와 사람 검토가 필요하다. 로컬이라는 사실만으로 개인정보 보호가 끝나는 것도 아니며 변환 도구가 만드는 임시 파일의 위치와 삭제 정책을 확인해야 한다.

# 관련 문서

- [정보처리기사 자료 인덱스](../../cs/engineer_info_processing/index.md)

# 출처

- [PyTorchKR 소개 글](https://discuss.pytorch.kr/t/liteparse-pdf/10524)
- [run-llama/liteparse](https://github.com/run-llama/liteparse)
- [OCR API 명세](https://github.com/run-llama/liteparse/blob/main/OCR_API_SPEC.md)

