---
type: Error Note
title: "Modify Python simulation code."
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2023-10-27)"
tags: [errors, chatgpt-export]
timestamp: 2023-10-27
status: active
---

# Modify Python simulation code.

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-10-27

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
너는 Python 개발자야. 지금부터 내가 주는 코드를 보고 수정해줘
₩₩₩
import random
import time
import datetime
import json
import platform
import psutil
from threading import Thread, Event
from multiprocessing import Process, Manager

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature' : None,
            'mars_base_external_temperature' : None,
            'mars_base_internal_humidity' : None,
            'mars_base_external_illuminance' : None,
            'mars_base_internal_co2' : None,
            'mars_base_internal_oxygen' : None
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"'{current_time}' : \n"\
            "{ \n"\
            f"  'Internal Temp' : {self.env_values['mars_base_internal_temperature']} (°C),\n"\
            f"  'External Temp' : {self.env_values['mars_base_external_temperature']} (°C), \n"\
            f"  'Internal Humidity' : {self.env_values['mars_base_internal_humidity']} (%), \n"\
            f"  'External Illuminance' : {self.env_values['mars_base_external_illuminance']} (W/m2), \n"\
            f"  'Internal CO2' : {self.env_values['mars_base_internal_co2']} (%), \n"\
            f"  'Internal Oxygen' : {self.env_values['mars_base_internal_oxygen']} (%) \n"\
            "} \n"

        with open("./data/mars_environment.log", 'a', encoding='utf-8') as a :
            a.write(log + "\n")
        return log

class MissionComputer :
    def __init__(self, sensor):
        self.sensor = sensor
        self.stop_event = Event()

        self.environment_data = {
            'mars_base_internal_temperature' : [],
            'mars_base_external_temperature' : [],
            'mars_base_internal_humidity' : [],
            'mars_base_external_illuminance' : [],
            'mars_base_internal_co2' : [],
            'mars_base_internal_oxygen' : []
        }

        self.setting = self.load_setting()

    def get_mission_computer_info(self):
        memory_size_byte = psutil.virtual_memory().total if self.setting.get('memory_size') else None
        memory_size_gb = round(memory_size_byte / (1024 ** 3), 2) if memory_size_byte else None
        while not self.stop_event:
            try:
                info = {
                    'os': platform.system() if self.setting.get('os') else None,
                    'os_version': platform.version() if self.setting.get('os_version') else None,
                    'cpu_type': platform.processor() if self.setting.get('cpu_type') else None,
                    'cpu_cores': psutil.cpu_count() if self.setting.get('cpu_cores') else None,
                    'memory_size': f"{memory_size_gb} GB"
                }
                return json.dumps(info, indent=4, ensure_ascii=False)
            except Exception as e:
                return str(e)

            print("Getting mission computer info...")
            print(self.get_mission_computer_info())
            time.sleep(20)

    def get_mission_computer_load(self) :
        while not self.stop_event:

            try :
                load = {
                    "cpu_usage" : psutil.cpu_percent() if self.setting.get('cpu_usage') else None,
                    'memory_usage' : psutil.virtual_memory().percent if self.setting.get("memory_usage") else None
                }
                return json.dumps(load, indent=4, ensure_ascii=False)
            except Exception as e :
                return str(e)

            print("Getting mission computer load...")
            print(self.get_mission_computer_load())
            time.sleep(20)


    def get_sensor_data(self):
        while not self.stop_event :
            self.sensor.set_env()
            sensor_data = self.sensor.get_env()

            self.environment_data['mars_base_internal_temperature'].append(
                self.sensor.env_values['mars_base_internal_temperature'])
            self.environment_data['mars_base_external_temperature'].append(
                self.sensor.env_values['mars_base_external_temperature'])
            self.environment_data['mars_base_internal_humidity'].append(
                self.sensor.env_values['mars_base_internal_humidity'])
            self.environment_data['mars_base_external_illuminance'].append(
                self.sensor.env_values['mars_base_external_illuminance'])
            self.environment_data['mars_base_internal_co2'].append(
                self.sensor.env_values['mars_base_internal_co2'])
            self.environment_data['mars_base_internal_oxygen'].append(
                self.sensor.env_values['mars_base_internal_oxygen'])


            if len(self.environment_data['mars_base_internal_temperature']) >= 60 :
                self.print_five_min_means()
                self.clear_data()

            print(sensor_data)

            time.sleep(5)

    def stop_program(self):
        self.stop_event.set()

    def clear_data(self) :
        for key in self.environment_data :
            self.environment_data[key].clear()
    def print_five_min_means(self) :
        averages = {
            'mars_base_internal_temperature': sum(self.environment_data["mars_base_internal_temperature"]) / len(self.environment_data['mars_base_internal_temperature']),
            'mars_base_external_temperature': sum(self.environment_data["mars_base_external_temperature"]) / len(self.environment_data['mars_base_external_temperature']),
            'mars_base_internal_humidity': sum(self.environment_data["mars_base_internal_humidity"]) / len(self.environment_data['mars_base_internal_humidity']),
            'mars_base_external_illuminance': sum(self.environment_data["mars_base_external_illuminance"]) / len(self.environment_data['mars_base_external_illuminance']),
            'mars_base_internal_co2': sum(self.environment_data["mars_base_internal_co2"]) / len(self.environment_data['mars_base_internal_co2']),
            'mars_base_internal_oxygen': sum(self.environment_data["mars_base_internal_oxygen"]) / len(self.environment_data['mars_base_internal_oxygen']),
        }

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        five_min_log = f"'{current_time}', 5분 평균 : \n"\
            "{ \n"\
            f"  'Internal Temp' : {averages['mars_base_internal_temperature']} (°C),\n"\
            f"  'External Temp' : {averages['mars_base_external_temperature']} (°C), \n"\
            f"  'Internal Humidity' : {averages['mars_base_internal_humidity']} (%), \n"\
            f"  'External Illuminance' : {averages['mars_base_external_illuminance']} (W/m2), \n"\
            f"  'Internal CO2' : {averages['mars_base_internal_co2']} (%), \n"\
            f"  'Internal Oxygen' : {averages['mars_base_internal_oxygen']} (%) \n"\
            "} \n"
        with open("./data/mars_environment_5_min.log", 'a', encoding='utf-8') as a :
            a.write(five_min_log + "\n")

        return five_min_log

    def load_setting(self):
        try :
            with open('./data/setting.txt', 'r', encoding='utf-8') as f :
                return json.load(f)
        except FileNotFoundError :
            print('파일을 찾을 수 없습니다.')
            return {}


if __name__ == "__main__":
    ds = DummySensor()
    RunComputer = MissionComputer(ds)
    try:
        system_info = RunComputer.get_mission_computer_info()
        print(json.dumps(system_info, indent=4))

        # 시스템 부하 정보 출력
        load_info = RunComputer.get_mission_computer_load()
        print(json.dumps(load_info, indent=4))


    except KeyboardInterrupt:
            RunComputer.stop_program()
            print("System stopped...")
₩₩₩

### 💡 답변 (Assistant)
이 코드는 Python으로 작성된 시뮬레이션 코드로, 가상 환경 데이터를 생성하고 관리하는 기능을 가지고 있습니다. 코드에 몇 가지 수정이 필요해 보입니다. 아래는 수정 사항입니다:

1. `print` 문을 제거합니다.
2. `MissionComputer` 클래스의 `get_mission_computer_info` 및 `get_mission_computer_load` 메서드에서 무한 루프에 빠진 문제를 수정합니다. 이렇게 하면 루프가 무한히 돌기 때문에 코드가 중단되지 않습니다.

아래는 수정된 코드입니다:

```python
import random
import time
import datetime
import json
import platform
import psutil
from threading import Thread, Event
from multiprocessing import Process, Manager

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature' : None,
            'mars_base_external_temperature' : None,
            'mars_base_internal_humidity' : None,
            'mars_base_external_illuminance' : None,
            'mars_base_internal_co2' : None,
            'mars_base_internal_oxygen' : None
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-d %H:%M:%S")
        log = f"'{current_time}' : \n"\
            "{ \n"\
            f"  'Internal Temp' : {self.env_values['mars_base_internal_temperature']} (°C),\n"\
            f"  'External Temp' : {self.env_values['mars_base_external_temperature']} (°C), \n"\
            f"  'Internal Humidity' : {self.env_values['mars_base_internal_humidity']} (%), \n"\
            f"  'External Illuminance' : {self.env_values['mars_base_external_illuminance']} (W/m2), \n"\
            f"  'Internal CO2' : {self.env_values['mars_base_internal_co2']} (%), \n"\
            f"  'Internal Oxygen' : {self.env_values['mars_base_internal_oxygen']} (%) \n"\
            "} \n"

        with open("./data/mars_environment.log", 'a', encoding='utf-8') as a:
            a.write(log + "\n")
        return log

class MissionComputer:
    def __init__(self, sensor):
        self.sensor = sensor
        self.stop_event = Event()

        self.environment_data = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': []
        }

        self.setting = self.load_setting()

    def get_mission_computer_info(self):
        memory_size_byte = psutil.virtual_memory().total if self.setting.get('memory_size') else None
        memory_size_gb = round(memory_size_byte / (1024 ** 3), 2) if memory_size_byte else None
        while not self.stop_event:
            try:
                info = {
                    'os': platform.system() if self.setting.get('os') else None,
                    'os_version': platform.version() if self.setting.get('os_version') else None,
                    'cpu_type': platform.processor() if self.setting.get('cpu_type') else None,
                    'cpu_cores': psutil.cpu_count() if self.setting.get('cpu_cores') else None,
                    'memory_size': f"{memory_size_gb} GB"
                }
                print(json.dumps(info, indent=4))  # 출력 정보
                time.sleep(20)
            except Exception as e:
                print(str(e))
                time.sleep(20)

    def get_mission_computer_load(self):
        while not self.stop_event:
            try:
                load = {
                    "cpu_usage": psutil.cpu_percent() if self.setting.get('cpu_usage') else None,
                    'memory_usage': psutil.virtual_memory().percent if self.setting.get("memory_usage") else None
                }
                print(json.dumps(load, indent=4))  # 출력 정보
                time.sleep(20)
            except Exception as e:
                print(str(e))
                time.sleep(20)

    def get_sensor_data(self):
        while not self.stop_event:
            self.sensor.set_env()
            sensor_data = self.sensor.get_env()

            self.environment_data['mars_base_internal_temperature'].append(
                self.sensor.env_values['mars_base_internal_temperature'])
            self.environment_data['mars_base_external_temperature'].append(
                self.sensor.env_values['mars_base_external_temperature'])
            self.environment_data['mars_base_internal_humidity'].append(
                self.sensor.env_values['mars_base_internal_humidity'])
            self.environment_data['mars_base_external_illuminance'].append(
                self.sensor.env_values['mars_base_external_illuminance'])
            self.environment_data['mars_base_internal_co2'].append(
                self.sensor.env_values['mars_base_internal_co2'])
            self.environment_data['mars_base_internal_oxygen'].append(
                self.sensor.env_values['mars_base_internal_oxygen'])

            if len(self.environment_data['mars_base_internal_temperature']) >= 60:
                self.print_five_min_means()
                self.clear_data()

            time.sleep(5)

    def stop_program(self):
        self.stop_event.set()

    def clear_data(self):
        for key in self.environment_data:
            self.environment_data[key].clear()

    def print_five_min_means(self):
        averages = {
            'mars_base_internal_temperature': sum(self.environment_data["mars_base_internal_temperature"]) / len(self.environment_data['mars_base_internal_temperature']),
            'mars_base_external_temperature': sum(self.environment_data["mars_base_external_temperature"]) / len(self.environment_data['mars_base_external_temperature']),
            'mars_base_internal_humidity': sum(self.environment_data["mars_base_internal_humidity"]) / len(self.environment_data['mars_base_internal_humidity']),
            'mars_base_external_illuminance': sum(self.environment_data["mars_base_external_illuminance"]) / len(self.environment_data['mars_base_external_illuminance']),
            'mars_base_internal_co2': sum(self.environment_data["mars_base_internal_co2"]) / len(self.environment_data['mars_base_internal_co2']),
            'mars_base_internal_oxygen': sum(self.environment_data["mars_base_internal_oxygen"]) / len(self.environment_data['mars_base_internal_oxygen']),
        }

---

### 💡 답변 (Assistant)
current_time = datetime.datetime.now().strftime("%Y-%m-d %H:%M:%S")
        five_min_log = f"'{current_time}', 5분 평균 : \n"\
            "{ \n"\
            f"  'Internal Temp' : {averages['mars_base_internal_temperature']} (°C),\n"\
            f"  'External Temp' : {averages['mars_base_external_temperature']} (°C), \n"\
            f"  'Internal Humidity' : {averages['mars_base_internal_humidity']} (%), \n"\
            f"  'External Illuminance' : {averages['mars_base_external_illuminance']} (W/m2), \n"\
            f"  'Internal CO2' : {averages['mars_base_internal_co2']} (%), \n"\
            f"  'Internal Oxygen' : {averages['mars_base_internal_oxygen']} (%) \n"\
            "} \n"
        with open("./data/mars_environment_5_min.log", 'a', encoding='utf-8') as a:
            a.write(five_min_log + "\n")

    def load_setting(self):
        try:
            with open('./data/setting.txt', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print('파일을 찾을 수 없습니다.')
            return {}

if __name__ == "__main__":
    ds = DummySensor()
    RunComputer = MissionComputer(ds)
    try:
        system_info_thread = Thread(target=RunComputer.get_mission_computer_info)
        system_info_thread.start()

        load_info_thread = Thread(target=RunComputer.get_mission_computer_load)
        load_info_thread.start()

        sensor_data_thread = Thread(target=RunComputer.get_sensor_data)
        sensor_data_thread.start()

        input("Press Enter to stop the program...")

        RunComputer.stop_program()
        system_info_thread.join()
        load_info_thread.join()
        sensor_data_thread.join()
        print("System stopped...")
    except KeyboardInterrupt:
        RunComputer.stop_program()
        print("System stopped...")
```

이제 코드는 각 스레드에서 시스템 정보, 부하 정보 및 센서 데이터를 주기적으로 가져와 출력하며, 사용자가 Enter 키를 누르면 프로그램이 정지합니다.

---

### ❓ 질문 (User)
지금 내가 원하는건 
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


이거야 혹시 이거에 맞게 수정해줄수있어?

### 💡 답변 (Assistant)
당신이 요청한 내용에 맞게 코드를 수정하고, 멀티 스레드와 멀티 프로세스를 사용하여 실행하는 예제를 제공하겠습니다. 또한, 중간에 특정 키를 입력받아 출력을 멈출 수 있도록 코드도 포함하겠습니다.

먼저, 코드를 수정한 후 멀티 스레드로 실행하는 예제를 제공하겠습니다. 다음은 수정된 코드입니다:

```python
import random
import time
import datetime
import json
import platform
import psutil
from threading import Thread, Event
from multiprocessing import Process, Manager

class DummySensor:
    # (이전 코드와 동일)

class MissionComputer:
    # (이전 코드와 동일)

if __name__ == "__main":
    ds = DummySensor()
    
    # runComputer 인스턴스 생성
    runComputer = MissionComputer(ds)
    
    # 미션 컴퓨터 정보 및 부하 정보를 가져오는 스레드 생성
    system_info_thread = Thread(target=runComputer.get_mission_computer_info)
    load_info_thread = Thread(target=runComputer.get_mission_computer_load)
    
    # 스레드 시작
    system_info_thread.start()
    load_info_thread.start()
    
    try:
        while True:
            # 사용자 입력을 대기하며, 입력을 받으면 프로그램 종료
            user_input = input("Press Enter to stop the program...")
            if user_input:
                break
    except KeyboardInterrupt:
        pass

    # 프로그램 종료 시, 스레드 중지
    runComputer.stop_program()
    system_info_thread.join()
    load_info_thread.join()
    
    print("System stopped...")
```

이제 멀티 스레드로 시스템 정보 및 부하 정보를 지속적으로 확인하고, Enter 키를 누르면 프로그램을 종료합니다. 이제 멀티 프로세스로 실행하는 코드를 제공하겠습니다.

```python
import random
import time
import datetime
import json
import platform
import psutil
from threading import Thread, Event
from multiprocessing import Process, Manager

class DummySensor:
    # (이전 코드와 동일)

class MissionComputer:
    # (이전 코드와 동일)

if __name__ == "__main__":
    ds = DummySensor()
    
    # runComputer1, runComputer2, runComputer3 인스턴스 생성
    runComputer1 = MissionComputer(ds)
    runComputer2 = MissionComputer(ds)
    runComputer3 = MissionComputer(ds)
    
    # 멀티 프로세스로 실행
    processes = []

    processes.append(Process(target=runComputer1.get_mission_computer_info))
    processes.append(Process(target=runComputer2.get_mission_computer_load))
    processes.append(Process(target=runComputer3.get_sensor_data))
    
    for process in processes:
        process.start()
    
    try:
        while True:
            # 사용자 입력을 대기하며, 입력을 받으면 프로그램 종료
            user_input = input("Press Enter to stop the program...")
            if user_input:
                break
    except KeyboardInterrupt:
        pass
    
    # 프로그램 종료 시, 프로세스 중지
    for process in processes:
        process.terminate()
        process.join()
    
    print("System stopped...")
```

이제 멀티 프로세스로 시스템 정보, 부하 정보 및 센서 데이터를 병렬로 실행하고, Enter 키를 누르면 프로그램을 종료합니다. 이 코드를 `mars_mission_computer.py` 파일에 저장하고 실행할 수 있습니다.

---

### ❓ 질문 (User)
근데 이렇게 넣으니까 runComputer1 2. 는 null 값이 나오던데 어떻게 해야되?

### 💡 답변 (Assistant)
runComputer1, runComputer2, runComputer3가 `None`으로 나오는 이유는 멀티 프로세스가 서로 다른 프로세스에서 실행되기 때문입니다. 각 프로세스는 별도의 메모리 공간을 가지며, 따라서 runComputer1, runComputer2, runComputer3 인스턴스가 서로 공유되지 않습니다.

멀티 프로세스 간에 데이터를 공유하기 위해서는 `multiprocessing.Manager`를 사용하여 데이터를 공유해야 합니다. 아래는 수정된 코드입니다:

```python
import random
import time
import datetime
import json
import platform
import psutil
from threading import Thread, Event
from multiprocessing import Process, Manager

class DummySensor:
    # (이전 코드와 동일)

class MissionComputer:
    # (이전 코드와 동일)

if __name__ == "__main__":
    ds = DummySensor()
    
    # Manager를 사용하여 데이터 공유
    with Manager() as manager:
        # runComputer1, runComputer2, runComputer3 인스턴스 생성
        runComputer1 = MissionComputer(ds)
        runComputer2 = MissionComputer(ds)
        runComputer3 = MissionComputer(ds)
    
        # 멀티 프로세스로 실행
        processes = []

        # Manager를 사용하여 데이터 공유
        runComputer1.environment_data = manager.dict(runComputer1.environment_data)
        runComputer2.environment_data = manager.dict(runComputer2.environment_data)
        runComputer3.environment_data = manager.dict(runComputer3.environment_data)
    
        processes.append(Process(target=runComputer1.get_mission_computer_info))
        processes.append(Process(target=runComputer2.get_mission_computer_load))
        processes.append(Process(target=runComputer3.get_sensor_data))
    
        for process in processes:
            process.start()
    
        try:
            while True:
                # 사용자 입력을 대기하며, 입력을 받으면 프로그램 종료
                user_input = input("Press Enter to stop the program...")
                if user_input:
                    break
        except KeyboardInterrupt:
            pass
    
        # 프로그램 종료 시, 프로세스 중지
        for process in processes:
            process.terminate()
            process.join()
    
        print("System stopped...")
```

이렇게 하면 멀티 프로세스 간에 데이터를 공유하고, runComputer1, runComputer2, runComputer3 인스턴스가 각각 별도의 프로세스에서 올바르게 작동합니다.

---

### ❓ 질문 (User)
def get_mission_computer_info(self):
        memory_size_byte = psutil.virtual_memory().total if self.setting.get('memory_size') else None
        memory_size_gb = round(memory_size_byte / (1024 ** 3), 2) if memory_size_byte else None
        while not self.stop_event:
            try:
                info = {
                    'os': platform.system() if self.setting.get('os') else None,
                    'os_version': platform.version() if self.setting.get('os_version') else None,
                    'cpu_type': platform.processor() if self.setting.get('cpu_type') else None,
                    'cpu_cores': psutil.cpu_count() if self.setting.get('cpu_cores') else None,
                    'memory_size': f"{memory_size_gb} GB"
                }
                return json.dumps(info, indent=4, ensure_ascii=False)
            except Exception as e:
                return str(e)

            print("Getting mission computer info...")
            print(self.get_mission_computer_info())
            time.sleep(20)

    def get_mission_computer_load(self) :
        while not self.stop_event:

            try :
                load = {
                    "cpu_usage" : psutil.cpu_percent() if self.setting.get('cpu_usage') else None,
                    'memory_usage' : psutil.virtual_memory().percent if self.setting.get("memory_usage") else None
                }
                return json.dumps(load, indent=4, ensure_ascii=False)
            except Exception as e :
                return str(e)

            print("Getting mission computer load...")
            print(self.get_mission_computer_load())
            time.sleep(20)
이 데이터가 결국 출력되지 않는데 해결방법 없을까?

### 💡 답변 (Assistant)
문제는 `return` 문이 스레드 내에서 실행되는 함수에서 사용되어, 함수가 실행을 종료하기 때문에 이후의 코드와 루프가 실행되지 않는 것입니다. 또한, 무한 루프 내에서 `print` 문도 계속 호출되므로 스레드가 무한 루프에 갇히게 됩니다.

대신, 정보를 출력하기 위해 `print`를 사용하고, `return` 문을 제거해야 합니다. 또한, `time.sleep(20)`을 사용하여 주기적으로 정보를 가져오고 출력할 수 있습니다. 아래는 수정된 코드입니다:

```python
def get_mission_computer_info(self):
    memory_size_byte = psutil.virtual_memory().total if self.setting.get('memory_size') else None
    memory_size_gb = round(memory_size_byte / (1024 ** 3), 2) if memory_size_byte else None
    while not self.stop_event:
        try:
            info = {
                'os': platform.system() if self.setting.get('os') else None,
                'os_version': platform.version() if self.setting.get('os_version') else None,
                'cpu_type': platform.processor() if self.setting.get('cpu_type') else None,
                'cpu_cores': psutil.cpu_count() if self.setting.get('cpu_cores') else None,
                'memory_size': f"{memory_size_gb} GB"
            }
            print(json.dumps(info, indent=4, ensure_ascii=False))  # 출력 정보
            time.sleep(20)
        except Exception as e:
            print(str(e))
            time.sleep(20)

def get_mission_computer_load(self):
    while not self.stop_event:
        try:
            load = {
                "cpu_usage": psutil.cpu_percent() if self.setting.get('cpu_usage') else None,
                'memory_usage': psutil.virtual_memory().percent if self.setting.get("memory_usage") else None
            }
            print(json.dumps(load, indent=4, ensure_ascii=False))  # 출력 정보
            time.sleep(20)
        except Exception as e:
            print(str(e))
            time.sleep(20)
```

이제 정보가 주기적으로 출력되며, 루프가 무한하게 실행되지 않습니다. `return` 문은 삭제되었으며, 대신 정보를 `print`를 사용하여 출력하고 20초마다 쉬는 것으로 변경되었습니다.

---

### ❓ 질문 (User)
혹시 dummy computer 에 해당하는 세팅이 들어가야되는거 아니야?

### 💡 답변 (Assistant)
DummySensor 클래스의 세팅을 수정해야 하는 경우, 해당 클래스 내에서 필요한 설정을 수정하면 됩니다. 현재 코드에서는 DummySensor 클래스에 특별한 설정이 없으므로, 만약 미션 컴퓨터와 관련된 설정을 DummySensor에 추가해야 한다면 다음과 같이 할 수 있습니다.

1. DummySensor 클래스에 설정을 추가합니다.

```python
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

        self.setting = {
            'temperature_range': (18, 30),
            'external_temperature_range': (0, 21),
            'humidity_range': (50, 60),
            'illuminance_range': (500, 715),
            'co2_range': (0.02, 0.1),
            'oxygen_range': (4, 7)
        }
```

2. 해당 설정을 사용하여 데이터를 생성하는 부분을 수정합니다.

```python
def set_env(self):
    self.env_values['mars_base_internal_temperature'] = round(random.uniform(*self.setting['temperature_range']), 2)
    self.env_values['mars_base_external_temperature'] = round(random.uniform(*self.setting['external_temperature_range']), 2)
    self.env_values['mars_base_internal_humidity'] = round(random.uniform(*self.setting['humidity_range']), 2)
    self.env_values['mars_base_external_illuminance'] = round(random.uniform(*self.setting['illuminance_range']), 2)
    self.env_values['mars_base_internal_co2'] = round(random.uniform(*self.setting['co2_range']), 3)
    self.env_values['mars_base_internal_oxygen'] = round(random.uniform(*self.setting['oxygen_range']), 2)
```

이렇게 하면 DummySensor 클래스에 설정이 추가되고, 해당 설정을 사용하여 데이터가 생성됩니다. 설정을 적절하게 조정하여 미션 컴퓨터의 요구 사항에 맞게 데이터를 생성할 수 있습니다.

---

### ❓ 질문 (User)
내가 원하는건 시스템 정보를 원하는데 지금 거기에는 시스템 정보가 포함되어 있지 않잖아

### 💡 답변 (Assistant)
죄송합니다, 이해가 부족했습니다. 시스템 정보를 미션 컴퓨터와 관련된 설정으로 제공하고자 하는 것이라면, 해당 설정은 MissionComputer 클래스에 추가해야 합니다. MissionComputer 클래스 내에서 시스템 정보를 가져오는 메서드를 수정하여 이러한 설정을 활용할 수 있습니다.

다음은 설정을 추가하고 시스템 정보를 MissionComputer 클래스 내에서 가져오는 방법을 보여드립니다:

```python
class MissionComputer:
    def __init__(self, sensor, system_settings):
        self.sensor = sensor
        self.system_settings = system_settings  # 시스템 설정 추가
        self.stop_event = Event()

        # (이전 코드와 동일)

    def get_mission_computer_info(self):
        while not self.stop_event:
            try:
                info = {
                    'os': platform.system() if self.system_settings.get('os') else None,
                    'os_version': platform.version() if self.system_settings.get('os_version') else None,
                    'cpu_type': platform.processor() if self.system_settings.get('cpu_type') else None,
                    'cpu_cores': psutil.cpu_count() if self.system_settings.get('cpu_cores') else None,
                }
                print(json.dumps(info, indent=4, ensure_ascii=False))  # 출력 정보
                time.sleep(20)
            except Exception as e:
                print(str(e))
                time.sleep(20)

    # (다른 메서드는 이전 코드와 동일)
```

위의 코드에서 MissionComputer 클래스에 시스템 설정을 추가하고, `get_mission_computer_info` 메서드에서 이 설정을 활용하여 원하는 시스템 정보를 가져오고 출력합니다. 이제 시스템 정보가 미션 컴퓨터의 설정에 따라 가져와질 것입니다.

---

### ❓ 질문 (User)
그니까 결국 그걸 인쇄를 해야되는데

### 💡 답변 (Assistant)
미션 컴퓨터의 시스템 정보를 인쇄하려면 `get_mission_computer_info` 메서드 내에서 정보를 인쇄하도록 수정해야 합니다. 아래는 수정된 코드 예제입니다:

```python
class MissionComputer:
    def __init__(self, sensor, system_settings):
        self.sensor = sensor
        self.system_settings = system_settings  # 시스템 설정 추가
        self.stop_event = Event()

        # (이전 코드와 동일)

    def get_mission_computer_info(self):
        while not self.stop_event:
            try:
                info = {
                    'os': platform.system() if self.system_settings.get('os') else None,
                    'os_version': platform.version() if self.system_settings.get('os_version') else None,
                    'cpu_type': platform.processor() if self.system_settings.get('cpu_type') else None,
                    'cpu_cores': psutil.cpu_count() if self.system_settings.get('cpu_cores') else None,
                }
                print(json.dumps(info, indent=4, ensure_ascii=False))  # 시스템 정보 인쇄
                time.sleep(20)
            except Exception as e:
                print(str(e))
                time.sleep(20)

    # (다른 메서드는 이전 코드와 동일)
```

이제 `get_mission_computer_info` 메서드에서 시스템 정보를 가져와 인쇄합니다. 이로써 미션 컴퓨터의 시스템 정보가 주기적으로 출력될 것입니다.

---
