---
type: Concept
title: "FastAPI 알아보기"
description: "CS - Software Architecture - ChatGPT 대화 추출 노트 (2023-11-04)"
tags: [cs, chatgpt-export]
timestamp: 2023-11-04
status: active
---

# FastAPI 알아보기

> **카테고리**: `CS - Software Architecture`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-11-04

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
Fast API 에 대해 알아?

### 💡 답변 (Assistant)
FastAPI는 Python을 사용하여 웹 애플리케이션 및 API를 빠르게 개발할 수 있도록 도와주는 모던하고 빠른 웹 프레임워크입니다. FastAPI는 ASGI (Asynchronous Server Gateway Interface)를 기반으로 하며, 비동기 코드 작성을 지원하여 높은 처리량과 효율적인 성능을 제공합니다.

FastAPI의 주요 특징과 이점은 다음과 같습니다:

1. 빠른 개발: FastAPI는 빠르게 개발할 수 있도록 설계되었습니다. 이를 통해 개발자는 적은 코드로 강력한 API를 작성할 수 있습니다.

2. 자동 문서화: FastAPI는 Pydantic 모델과 주석을 통해 자동 API 문서 생성을 지원합니다. Swagger UI와 ReDoc과 같은 도구를 사용하여 API 문서를 생성하고 브라우징할 수 있습니다.

3. 유형 검사: Pydantic 모델을 사용하여 입력 및 출력 데이터의 유효성 검사를 자동화할 수 있으며, 이는 코드의 안정성을 향상시키고 버그를 사전에 찾을 수 있도록 도와줍니다.

4. 비동기 지원: FastAPI는 비동기 코드 작성을 쉽게 처리하며, 비동기 I/O 작업을 처리할 때 높은 성능을 제공합니다.

5. 자동 응답 처리: FastAPI는 JSON 및 HTML과 같은 다양한 응답 형식을 자동으로 처리할 수 있으며, 개발자가 직접 처리하는 데 필요한 작업을 최소화합니다.

6. 보안: FastAPI는 기본적으로 보안 관련 헤더를 설정하고, CSRF 및 CORS 공격과 같은 일반적인 보안 문제를 방지하기 위한 내장 지원을 제공합니다.

7. 플러그인 및 확장성: FastAPI는 다양한 플러그인 및 확장을 통해 기능을 확장할 수 있으며, 기존 Python 라이브러리와 통합하기 쉽습니다.

FastAPI는 많은 개발자들 사이에서 인기가 높고, 빠른 개발과 뛰어난 성능을 통해 웹 애플리케이션 및 API 개발을 간편하게 만들어줍니다. FastAPI 공식 문서와 튜토리얼을 통해 더 많은 정보와 예제를 얻을 수 있습니다.

---

### ❓ 질문 (User)
import sys
import os
import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, \
    QFileDialog, QLabel, QApplication, QSizePolicy, QWidget, QStatusBar
from PySide6 import QtGui
from fastapi import FastAPI

class VideoViewer(QMainWindow) :

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Viewer")
        self.resize(800, 600)

        self.video_file_button = QPushButton("file open")
        self.video_file_button.clicked.connect(self.open_video_file_dialog)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_video)

        self.capture_button = QPushButton("Capture")
        self.capture_button.clicked.connect(self.capture_frame)

        self.video_view_label = QLabel()
        self.video_view_label.setAlignment(Qt.AlignCenter)
        self.video_view_label.setSizePolicy(QSizePolicy.Expanding,
                                            QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_file_button)
        main_layout.addWidget(self.play_button)
        main_layout.addWidget(self.stop_button)
        main_layout.addWidget(self.capture_button)
        main_layout.addWidget(self.video_view_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.video_path = ""
        self.video_width = 640
        self.video_height = 480

        self.video_capture = None
        self.video_timer = QTimer()
        self. video_timer.timeout.connect(self.display_next_frame)

        self.paused = False
        self.current_frame = 0
        self.capture_count = 0

        os.makedirs('../data/cctv/', exist_ok=True)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def open_video_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi *.mov *.mkv)")
        if file_dialog.exec() :
            selected_files = file_dialog.selectedFiles()
            if selected_files :
                self.video_path = selected_files[0]
                self.status_bar.showMessage(f"video path >>> {self.video_path}")

    def play_video(self):
        if self.video_path:
            if self.paused:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            else:
                self.video_capture = cv2.VideoCapture(self.video_path)
                self.current_frame = 0

            self.play_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.capture_button.setEnabled(True)
            self.video_timer.start(30)

    def display_next_frame(self):
        if self.video_path:
            ret, frame = self.video_capture.read()

            if ret :
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resize = self.resize_frame(frame_rgb)
                h, w, _ = frame_resize.shape   # fix -> frame_resize.shape
                if w > 0 and h > 0 :
                    frame_image = QtGui.QImage(frame_resize, w, h,
                                               QtGui.QImage.Format_RGB888)   # fix -> frame_resize
                    pixmap = QtGui.QPixmap.fromImage(frame_image)
                    self.video_view_label.setPixmap(pixmap)
                    self.video_view_label.setScaledContents(True)

                self.current_frame += 1
            else :
                self.video_timer.stop()

    def stop_video(self):
        self.video_timer.stop()
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.capture_button.setEnabled(not self.paused)
        self.paused = True

    def capture_frame(self):
        ret, frame = self.video_capture.read()

        if ret :
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resize = self.resize_frame(frame_rgb)
            h, w, _ = frame_resize.shape  # fix -> frame_resize.shape
            if w > 0 and h > 0:
                file_name = os.path.splitext(os.path.basename(self.video_path))[0]
                image_name = f"{file_name}_{self.capture_count:04d}_image.png"
                image_save_path = os.path.join('../data', image_name)
                cv2.imwrite(image_save_path, frame_resize) # fix -> frame_resize
                self.capture_count += 1
                self.status_bar.showMessage(f"capture ok : {image_save_path}")

    def resize_frame(self, frame):
        height, width, _ = frame.shape

        if width > self.video_width :
            ratio = self.video_width / width
            frame = cv2.resize(frame, (self.video_width, int(height * ratio)))
        if height > self.video_height :
            ratio = self.video_height / height
            frame = cv2.resize(frame, (int(width * ratio), self.video_height))

        return frame

if __name__ == "__main__" :
    app=QApplication(sys.argv)
    window = VideoViewer()
    window.show()
    app.exec()

이 코드를 PySide 를 사용하지 않고 Fast API 를 사용해서 완성해줘

### 💡 답변 (Assistant)
FastAPI를 사용하여 위의 PySide 코드를 대체하는 것은 가능하지만, FastAPI는 웹 API 서버를 만드는 것에 주로 사용되기 때문에 동영상 재생과 캡처 기능을 직접 지원하지 않습니다. 그러나 FastAPI를 사용하여 동영상 처리 API를 구축하고, 이 API를 통해 동영상을 업로드하고 재생할 수 있는 웹 애플리케이션을 구축할 수 있습니다. 아래는 FastAPI를 사용하여 동영상 업로드 및 재생 API를 만드는 예제입니다.

```python
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import shutil
import cv2
from io import BytesIO
import mimetypes

app = FastAPI()

# CORS 미들웨어 설정 (크로스 오리진 문제 해결)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안을 위해서 "*" 대신 원하는 도메인을 설정하세요.
    allow_methods=["*"],
    allow_headers=["*"],
)

# 동영상 업로드를 위한 엔드포인트
@app.post("/upload/")
async def upload_video(file: UploadFile):
    # 업로드된 동영상을 저장
    with open(file.filename, "wb") as f:
        f.write(file.file.read())

    return {"message": "Video uploaded successfully"}

# 동영상 재생을 위한 엔드포인트
@app.get("/play/{video_path}")
async def play_video(video_path: str):
    # 업로드된 동영상 파일을 읽어서 바이트 스트림으로 반환
    if os.path.exists(video_path):
        with open(video_path, "rb") as video_file:
            return FileResponse(video_path, headers={"Content-Type": mimetypes.guess_type(video_path)[0]})

    return {"message": "Video not found"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

이 코드는 FastAPI를 사용하여 동영상 업로드 및 재생 API를 만드는 예제입니다. 동영상을 업로드하려면 `/upload/` 엔드포인트를 사용하고, 동영상을 재생하려면 `/play/{video_path}` 엔드포인트를 사용합니다. FastAPI를 실행하기 위해 `uvicorn`을 사용하고, CORS 미들웨어를 설정하여 크로스 오리진 문제를 해결합니다. 이 코드를 통해 동영상을 업로드하고 재생할 수 있는 웹 API를 구축할 수 있습니다.

또한, 동영상 캡처 기능을 구현하려면 위의 코드에 동영상 프레임을 캡처하고 이미지로 저장하는 부분을 추가해야 할 것입니다. OpenCV를 사용하여 프레임을 캡처하고 이미지로 저장하는 기능을 추가하면 됩니다.

---

### ❓ 질문 (User)
Traceback (most recent call last):
  File "/Users/ijeongmin/Desktop/project2/main.py", line 21, in <module>
    @app.post("/upload/")
     ^^^^^^^^^^^^^^^^^^^^
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/fastapi/routing.py", line 921, in decorator
    self.add_api_route(
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/fastapi/routing.py", line 860, in add_api_route
    route = route_class(
            ^^^^^^^^^^^^
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/fastapi/routing.py", line 496, in __init__
    self.body_field = get_body_field(dependant=self.dependant, name=self.unique_id)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/fastapi/dependencies/utils.py", line 809, in get_body_field
    check_file_field(final_field)
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/site-packages/fastapi/dependencies/utils.py", line 101, in check_file_field
    raise RuntimeError(multipart_not_installed_error) from None
RuntimeError: Form data requires "python-multipart" to be installed. 
You can install "python-multipart" with: 

pip install python-multipart

### 💡 답변 (Assistant)
이 오류는 FastAPI에서 업로드한 파일을 처리하기 위해 필요한 `python-multipart` 라이브러리가 설치되어 있지 않을 때 발생합니다. `python-multipart` 라이브러리는 FastAPI에서 파일 업로드를 처리하기 위해 사용됩니다. 오류 메시지에 따라 아래의 명령을 사용하여 `python-multipart` 라이브러리를 설치하실 수 있습니다:

```bash
pip install python-multipart
```

설치 후 FastAPI 애플리케이션을 다시 실행하면 이 오류가 해결되어야 합니다. 필요한 라이브러리가 설치되면 파일 업로드와 관련된 엔드포인트가 올바르게 작동해야 합니다.

---

### ❓ 질문 (User)
INFO:     Started server process [6652]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:50375 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:50375 - "GET /favicon.ico HTTP/1.1" 404 Not Found

### 💡 답변 (Assistant)
FastAPI 애플리케이션이 성공적으로 시작되었고 0.0.0.0:8000에서 실행 중입니다. 그러나 "404 Not Found" 오류 메시지가 나타나는 것은 해당 URL 경로에 대한 핸들러가 없을 때 발생합니다. 이것은 FastAPI 애플리케이션에 루트 경로 ("/") 또는 "/favicon.ico" 경로를 처리하는 핸들러가 없기 때문에 발생하는 것입니다.

FastAPI는 경로를 설정하고 해당 경로에 대한 핸들러를 등록해야 합니다. 이 코드에서는 `/upload/` 및 `/play/{video_path}` 경로에 대한 핸들러가 설정되어 있으므로 이러한 경로에 요청을 보내야 합니다.

예를 들어 동영상을 업로드하려면 `/upload/` 엔드포인트로 POST 요청을 보내고, 동영상을 재생하려면 `/play/{video_path}` 엔드포인트로 GET 요청을 보내야 합니다.

브라우저에서 FastAPI 애플리케이션을 열 때 "/" 또는 "/favicon.ico" 경로로 접근하지 않도록 주의하십시오. 대신 "/upload/" 및 "/play/{video_path}"와 같은 설정된 경로를 사용하여 요청을 보내십시오.

---
