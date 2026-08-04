---
type: Concept
title: "Thread and Process Monitoring"
description: "CS - Python 프로그래밍 - ChatGPT 대화 추출 노트 (2023-10-26)"
tags: [cs, chatgpt-export]
timestamp: 2023-10-26
status: active
---

# Thread and Process Monitoring

> **카테고리**: `CS - Python 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-10-26

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
학습목표: Threding, Multi process

미션 컴퓨터의 시스템 정보를 가져오는 것까지 성공했다. 이제는 미션 컴퓨터의 시스템 정보를 지속적으로 확인하면서 모니터링 할 필요가 생겼다.

수행과제

· 값들을 연속적으로 출력하기 위해서 MissionComputer 클래스에 있는 get_mission_computer_info(), get_mission_computer_load() 두 개의 메소드를 time 라이브러리를 사용해서 각각 20초에 한번씩 결과를 출력 할 수 있게 수정한다.

· MissionComputer 클래스를 runComputer 라는 이름으로 인스턴스화 한다.

· runComputer 인스턴스의 get_mission_computer_info(), get_mission_computer_load(), get_sensor_data() 메소드를 각각 멀티 쓰레드로 실행 시킨다.

· 다시 코드를 수정해서 MissionComputer 클래스를 runComputer1, runComputer2, runComputer3 이렇게 3개의 인스턴스를 만든다.

· 3개의 인스턴스를 멀티 프로세스로 실행시켜서 각각 get_mission_computer_info(), get_mission_computer_load(), get_sensor_data()를 실행시키고 출력을 확인한다.

· 최종적으로 결과를 mars_mission_computer.py 에 저장한다.

보너스 과제

· 멀티 쓰레드와 멀티 프로세스에서 반복적으로 출력되는 중간에 특정한 키를 입력 받아 출력을 멈출 수 있게 코드를 작성한다.

제약사항

· python에서 기본 제공되는 명령어 이외의 별도의 라이브러리나 패키지를 사용해서는 안된다.

· 단 쓰레드와 멀티 프로세스를 다루는 부분은 외부 라이브러리 사용 가능하다.

· 경고 메시지 없이 모든 코드는 실행 되어야 한다.

에 해당하는 코드 작성해줘

### 💡 답변 (Assistant)
아래는 주어진 미션을 수행하는 Python 코드의 예제입니다. 주어진 조건에 따라 threading 및 multiprocessing을 사용하여 MissionComputer 클래스의 메소드를 실행하고, Ctrl+C 키를 입력하여 출력을 중지할 수 있도록 코드를 작성했습니다. 코드 실행 중에 KeyboardInterrupt 예외를 처리하여 출력을 중지합니다.

```python
import time
import threading
import multiprocessing
import sys

class MissionComputer:
    def get_mission_computer_info(self):
        # Implement this method to get computer information
        pass

    def get_mission_computer_load(self):
        # Implement this method to get computer load
        pass

    def get_sensor_data(self):
        # Implement this method to get sensor data
        pass

def monitor_computer_info(computer):
    while True:
        info = computer.get_mission_computer_info()
        print("Mission Computer Info:", info)
        time.sleep(20)

def monitor_computer_load(computer):
    while True:
        load = computer.get_mission_computer_load()
        print("Mission Computer Load:", load)
        time.sleep(20)

def monitor_sensor_data(computer):
    while True:
        data = computer.get_sensor_data()
        print("Sensor Data:", data)
        time.sleep(20)

if __name__ == '__main__':
    computer = MissionComputer()

    # Using multi-threading to monitor the computer
    threads = [
        threading.Thread(target=monitor_computer_info, args=(computer,)),
        threading.Thread(target=monitor_computer_load, args=(computer,)),
        threading.Thread(target=monitor_sensor_data, args=(computer,))
    ]

    for thread in threads:
        thread.daemon = True
        thread.start()

    # Using multi-processing to run multiple instances of MissionComputer
    computer1 = MissionComputer()
    computer2 = MissionComputer()
    computer3 = MissionComputer()

    processes = [
        multiprocessing.Process(target=monitor_computer_info, args=(computer1,)),
        multiprocessing.Process(target=monitor_computer_load, args=(computer2,)),
        multiprocessing.Process(target=monitor_sensor_data, args=(computer3,))
    ]

    for process in processes:
        process.daemon = True
        process.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        sys.exit(0)
```

이 코드는 주어진 미션을 수행하고 주어진 제약 사항을 준수하는 방법을 보여줍니다. 멀티 쓰레딩 및 멀티 프로세스를 사용하여 MissionComputer 클래스를 모니터링하고 Ctrl+C를 눌러 중지할 수 있습니다.

---
