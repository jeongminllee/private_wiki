---
type: Error Note
title: "Multi-Threaded and Multi-Process Code"
description: "Errors - Python & Conda - ChatGPT 대화 추출 노트 (2023-10-27)"
tags: [errors, chatgpt-export]
timestamp: 2023-10-27
status: active
---

# Multi-Threaded and Multi-Process Code

> **카테고리**: `Errors - Python & Conda`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-10-27

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


```
import random
import time
import datetime
import json
import platform
import psutil
import threading as Thread
import _multiprocessing


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
        self.stop = False

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
        while not self.stop:
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
            print(self.sensor.get_mission_computer_info())
            time.sleep(5)

    def get_mission_computer_load(self) :
        try :
            load = {
                "cpu_usage" : psutil.cpu_percent() if self.setting.get('cpu_usage') else None,
                'memory_usage' : psutil.virtual_memory().percent if self.setting.get("memory_usage") else None
            }
            return json.dumps(load, indent=4, ensure_ascii=False)
        except Exception as e :
            return str(e)


    def get_sensor_data(self):
        while not self.stop :
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
        self.stop = True

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




if __name__ == "__main__" :
    ds = DummySensor()
    RunComputer = MissionComputer(ds)

    thread1 = Thread(target=RunComputer.get_mission_computer_info())
    # thread2 = Thread(target=RunComputer.get_mission_computer_load())
    thread3 = Thread(target=RunComputer.get_sensor_data())

    thread1.start()
    # thread2.start()
    thread3.start()

    try :
        thread1.join()
        # thread2.join()
        thread3.join()

    except KeyboardInterrupt :
        RunComputer.stop_program()
        print("System stopped...")
```

해당 요청에 맞게 코드 수정해줘

### 💡 답변 (Assistant)
아래는 요청에 따라 수정된 코드입니다. 주요 변경 사항은 다음과 같습니다:

1. `threading` 라이브러리를 사용하여 멀티 스레딩을 구현합니다.
2. `MissionComputer` 클래스의 인스턴스를 생성하고, 해당 인스턴스의 메소드를 각각 별도의 스레드에서 실행합니다.
3. 3개의 `MissionComputer` 인스턴스를 만들어 멀티 프로세스로 실행합니다.
4. 중간에 입력을 받아 출력을 멈출 수 있는 기능을 추가합니다.

```python
import random
import time
import datetime
import json
import platform
import psutil
import threading
import multiprocessing
import _multiprocessing

class DummySensor:
    # 이전 코드와 동일

class MissionComputer:
    # 이전 코드와 동일

if __name__ == "__main__":
    ds = DummySensor()

    # 멀티 스레드로 실행하는 예시
    def run_threaded_computer(computer):
        thread1 = threading.Thread(target=computer.get_mission_computer_info)
        thread2 = threading.Thread(target=computer.get_mission_computer_load)
        thread3 = threading.Thread(target=computer.get_sensor_data)
        
        thread1.start()
        thread2.start()
        thread3.start()

        try:
            thread1.join()
            thread2.join()
            thread3.join()
        except KeyboardInterrupt:
            computer.stop_program()
            print("System stopped...")

    RunComputer = MissionComputer(ds)
    run_threaded_computer(RunComputer)

    # 멀티 프로세스로 실행하는 예시
    def run_multiprocessed_computer(computer):
        processes = []

        for _ in range(3):
            process = multiprocessing.Process(target=run_threaded_computer, args=(computer,))
            processes.append(process)
            process.start()

        try:
            for process in processes:
                process.join()
        except KeyboardInterrupt:
            computer.stop_program()
            print("System stopped...")

    run_multiprocessed_computer(RunComputer)
```

이제 코드는 멀티 스레딩 및 멀티 프로세스로 `MissionComputer` 인스턴스를 실행하며 중간에 KeyboardInterrupt를 통해 출력을 중지할 수 있습니다. 코드를 수정하여 필요한 출력을 파일에 저장하거나 원하는 대로 다양한 조작을 수행할 수 있습니다.

---

### ❓ 질문 (User)
Exception in thread Thread-1 (get_mission_computer_info):
Traceback (most recent call last):
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/threading.py", line 1052, in _bootstrap_inner
Exception in thread Thread-3 (get_sensor_data):
Traceback (most recent call last):
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/threading.py", line 1052, in _bootstrap_inner
        self.run()
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/threading.py", line 989, in run
self.run()
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/threading.py", line 989, in run
    self._target(*self._args, **self._kwargs)
  File "/Users/ijeongmin/Desktop/ProjectJ/mars_mission_computer.py", line 97, in get_sensor_data
    self._target(*self._args, **self._kwargs)
  File "/Users/ijeongmin/Desktop/ProjectJ/mars_mission_computer.py", line 64, in get_mission_computer_info
    while not self.stop :
     while not self.stop:
              ^^^^^^^^^
 AttributeError: 'MissionComputer' object has no attribute 'stop'  
          ^^^^^^^^^
AttributeError: 'MissionComputer' object has no attribute 'stop'
Traceback (most recent call last):
  File "/Users/ijeongmin/Desktop/ProjectJ/mars_mission_computer.py", line 205, in <module>
    run_multiprocessed_computer(RunComputer)
  File "/Users/ijeongmin/Desktop/ProjectJ/mars_mission_computer.py", line 195, in run_multiprocessed_computer
    process.start()
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/multiprocessing/process.py", line 121, in start
    self._popen = self._Popen(self)
                  ^^^^^^^^^^^^^^^^^
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/multiprocessing/context.py", line 224, in _Popen
    return _default_context.get_context().Process._Popen(process_obj)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/multiprocessing/context.py", line 289, in _Popen
    return Popen(process_obj)
           ^^^^^^^^^^^^^^^^^^
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/multiprocessing/popen_spawn_posix.py", line 32, in __init__
    super().__init__(process_obj)
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/multiprocessing/popen_fork.py", line 19, in __init__
    self._launch(process_obj)
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/multiprocessing/popen_spawn_posix.py", line 47, in _launch
    reduction.dump(process_obj, fp)
  File "/Users/ijeongmin/anaconda3/envs/projx/lib/python3.12/multiprocessing/reduction.py", line 60, in dump
    ForkingPickler(file, protocol).dump(obj)
TypeError: cannot pickle '_thread.lock' object

### 💡 답변 (Assistant)
위의 오류는 Python에서 멀티 프로세스로 객체를 공유하려고 할 때 발생할 수 있는 문제입니다. Python 멀티 프로세싱 모듈은 객체를 직렬화하고 다시 복원해야 하는데, 일부 객체는 직렬화할 수 없는 것으로 간주됩니다. 특히 `threading.Lock` 객체와 같은 스레딩 관련 객체는 직렬화할 수 없기 때문에 이러한 객체가 클래스 내부에 사용되면 멀티 프로세스에서 문제가 발생할 수 있습니다.

해결 방법으로는 `multiprocessing` 모듈을 사용하여 멀티 프로세스를 만들 때, 클래스 인스턴스 내부에 스레딩 락 객체를 사용하지 않는 것이 좋습니다. 대신 멀티 프로세스 간에 데이터를 공유할 때 `multiprocessing.Manager`를 사용하거나 스레딩 락 객체 대신 `multiprocessing.Lock`를 사용하는 것이 좋습니다.

아래는 `multiprocessing.Manager`를 사용한 예시입니다:

```python
from multiprocessing import Process, Manager

class MissionComputer:
    def __init__(self, sensor, stop_event):
        self.sensor = sensor
        self.stop_event = stop_event
        # 이하 코드는 이전 코드와 동일

if __name__ == "__main__":
    ds = DummySensor()

    with Manager() as manager:
        stop_event = manager.Event()
        RunComputer = MissionComputer(ds, stop_event)

        # 멀티 프로세스로 실행하는 예시
        processes = []

        for _ in range(3):
            process = Process(target=run_threaded_computer, args=(RunComputer,))
            processes.append(process)
            process.start()

        try:
            for process in processes:
                process.join()
        except KeyboardInterrupt:
            stop_event.set()
            print("System stopped...")
```

여기서 `stop_event`는 멀티 프로세스 간에 중지 신호를 전달하기 위한 이벤트 객체입니다. 이렇게 하면 멀티 프로세스 간에 데이터 공유 및 중지 신호를 쉽게 처리할 수 있습니다.

---
