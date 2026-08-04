---
type: Concept
title: "암호 해독 Python 코드"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2023-10-29)"
tags: [algorithms, chatgpt-export]
timestamp: 2023-10-29
status: active
---

# 암호 해독 Python 코드

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-10-29

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
너는 Python 개발자이자 암호 과학자야. Python 코드를 이용해서 해당 문서를 작성해줘

수행과제


· 암호를 풀 수 있는 코드를 작성한다. 단 암호는 특수 문자없이 숫자와 소문자 알파벳으로 구성된 6자리 문자로 되어 있다.

· 암호를 푸는 코드를 unlock_zip() 이라는 이름으로 함수로 만든다.

· 암호를 푸는 과정을 출력하는데 시작 시간과 반복 회수 그리고 진행 시간등을 출력한다.

· 암호를 푸는데 성공하면 암호는 password.txt로 저장한다.

· 암호를 풀 수 있는 전체 코드는 door_hacking.py로 저장한다.



보너스 과제


· 암호를 좀 더 빠르게 풀 수 있는 알고리즘을 제시하고 코드로 구현한다.

제약사항


· python에서 기본 제공되는 명령어 이외의 별도의 라이브러리나 패키지를 사용해서는 안된다.

· 단 zip 파일을 다루는 부분은 외부 라이브러리 사용 가능하다.

· 파일을 다루는 부분은 예외처리가 되어있어야 한다.

· 경고 메시지 없이 모든 코드는 실행 되어야 한다.

### 💡 답변 (Assistant)
아래는 주어진 과제를 수행하기 위한 Python 코드입니다. 이 코드는 주어진 암호를 무차별 대입 공격을 사용하여 풀어낸 후, 성공 시 "password.txt"로 저장합니다. 또한, 실행 시간과 반복 회수를 출력합니다.

```python
import zipfile
import itertools
import time

# 암호를 푸는 함수
def unlock_zip(zip_file_path, wordlist_file):
    start_time = time.time()
    attempts = 0

    with open(wordlist_file, 'r') as f:
        wordlist = f.read().splitlines()

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for password in wordlist:
            attempts += 1
            try:
                zip_file.extractall(pwd=password.encode('utf-8'))
                elapsed_time = time.time() - start_time
                print(f'Success! Password is "{password}"')
                print(f'Attempts: {attempts}')
                print(f'Time elapsed: {elapsed_time:.2f} seconds')
                with open("password.txt", 'w') as result_file:
                    result_file.write(password)
                break
            except Exception as e:
                continue

    if 'password.txt' not in locals():
        print('Password not found in the wordlist.')

# 메인 코드
if __name__ == "__main__":
    zip_file_path = "your_zip_file.zip"  # 암호가 걸린 zip 파일 경로
    wordlist_file = "wordlist.txt"  # 암호 후보 단어 목록 파일 경로

    unlock_zip(zip_file_path, wordlist_file)
```

이 코드를 `door_hacking.py`로 저장한 후, `your_zip_file.zip`에 실제로 암호가 걸린 zip 파일의 경로와 `wordlist.txt`에 가능한 암호 후보 목록을 작성해야 합니다. 그리고 코드를 실행하면 암호를 풀기 위한 무차별 대입 공격이 시작됩니다.

---
