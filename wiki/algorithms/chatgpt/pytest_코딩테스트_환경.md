---
type: Concept
title: "pytest 코딩테스트 환경"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2026-07-19)"
tags: [algorithms, chatgpt-export]
timestamp: 2026-07-19
status: active
---

# pytest 코딩테스트 환경

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-07-19

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
pytest 로 코딩테스트 환경을 만들려고 해.

### 💡 답변 (Assistant)
좋아. 코딩테스트용 `pytest` 환경은 **알고리즘 코드와 입출력 처리를 분리**하는 방식으로 만들면 가장 관리하기 편해.

## 1. 프로젝트 구조

```text
coding-test/
├─ pyproject.toml
├─ pytest.ini
├─ src/
│  ├─ __init__.py
│  └─ problems/
│     ├─ __init__.py
│     └─ problem_001.py
└─ tests/
   └─ test_problem_001.py
```

`src/problems`에는 실제 제출 코드를 두고, `tests`에는 테스트 케이스를 둔다.

---

## 2. 프로젝트 생성

평소 사용하는 `uv` 기준이다.

```bash
mkdir coding-test
cd coding-test

uv init
uv add --dev pytest
```

테스트 실행:

```bash
uv run pytest
```

상세 출력:

```bash
uv run pytest -v
```

실패한 테스트의 출력까지 확인:

```bash
uv run pytest -v -s
```

---

## 3. `pyproject.toml`

```toml
[project]
name = "coding-test"
version = "0.1.0"
description = "Coding test practice environment"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.0",
]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-ra"
```

이렇게 설정하면 테스트 코드에서 다음처럼 가져올 수 있다.

```python
from problems.problem_001 import solve
```

---

# 권장 구현 방식

코딩테스트 문제는 아래처럼 작성하는 것이 좋다.

```python
# src/problems/problem_001.py

from collections.abc import TextIO
import sys


def solve(reader: TextIO = sys.stdin, writer: TextIO = sys.stdout) -> None:
    a, b = map(int, reader.readline().split())
    print(a + b, file=writer)


if __name__ == "__main__":
    solve()
```

핵심은 다음 두 부분이다.

```python
reader: TextIO = sys.stdin
writer: TextIO = sys.stdout
```

실제 제출 환경에서는 평범한 표준 입출력으로 동작하고, 테스트에서는 `StringIO`를 주입할 수 있다.

---

## 4. 기본 테스트 코드

```python
# tests/test_problem_001.py

from io import StringIO

from problems.problem_001 import solve


def run_solution(input_data: str) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader, writer)

    return writer.getvalue().strip()


def test_example_1() -> None:
    input_data = """\
1 2
"""
    expected = """\
3
"""

    assert run_solution(input_data) == expected.strip()


def test_example_2() -> None:
    input_data = """\
100 200
"""
    expected = """\
300
"""

    assert run_solution(input_data) == expected.strip()
```

실행:

```bash
uv run pytest -v
```

결과:

```text
tests/test_problem_001.py::test_example_1 PASSED
tests/test_problem_001.py::test_example_2 PASSED
```

---

# 여러 테스트 케이스를 한 번에 관리하기

`pytest.mark.parametrize`를 쓰는 방식이 가장 효율적이다.

```python
from io import StringIO

import pytest

from problems.problem_001 import solve


def run_solution(input_data: str) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader, writer)

    return writer.getvalue().strip()


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        ("1 2\n", "3"),
        ("10 20\n", "30"),
        ("-5 7\n", "2"),
        ("0 0\n", "0"),
    ],
)
def test_solve(input_data: str, expected: str) -> None:
    assert run_solution(input_data) == expected
```

테스트 하나를 추가할 때는 목록에 데이터만 추가하면 된다.

```python
("100 300\n", "400"),
```

---

# 이미 `input()`과 `print()`로 작성한 코드 테스트하기

기존 코드를 크게 바꾸고 싶지 않을 수도 있다.

```python
# src/problems/problem_002.py

def solve() -> None:
    a, b = map(int, input().split())
    print(a * b)


if __name__ == "__main__":
    solve()
```

이 경우 `monkeypatch`와 `capsys`를 사용할 수 있다.

```python
# tests/test_problem_002.py

from io import StringIO
import sys

from problems.problem_002 import solve


def test_solve(monkeypatch, capsys) -> None:
    input_data = """\
3 5
"""

    monkeypatch.setattr(sys, "stdin", StringIO(input_data))

    solve()

    captured = capsys.readouterr()

    assert captured.out.strip() == "15"
```

다만 장기적으로는 `reader`, `writer`를 받도록 설계하는 첫 번째 방식을 더 추천한다. 전역 표준 입출력을 교체하지 않아서 테스트 간 간섭이 적다.

---

# BFS 문제 예제

## 구현

```python
# src/problems/shortest_path.py

from collections import deque
from collections.abc import TextIO
import sys


def shortest_path(
    graph: list[list[int]],
    start: int,
    end: int,
) -> int:
    distances = [-1] * len(graph)
    distances[start] = 0

    queue: deque[int] = deque([start])

    while queue:
        current = queue.popleft()

        if current == end:
            return distances[current]

        for next_node in graph[current]:
            if distances[next_node] != -1:
                continue

            distances[next_node] = distances[current] + 1
            queue.append(next_node)

    return -1


def solve(reader: TextIO = sys.stdin, writer: TextIO = sys.stdout) -> None:
    node_count, edge_count = map(int, reader.readline().split())

    graph: list[list[int]] = [[] for _ in range(node_count + 1)]

    for _ in range(edge_count):
        a, b = map(int, reader.readline().split())
        graph[a].append(b)
        graph[b].append(a)

    start, end = map(int, reader.readline().split())

    answer = shortest_path(graph, start, end)
    print(answer, file=writer)


if __name__ == "__main__":
    solve()
```

## 테스트

```python
# tests/test_shortest_path.py

from io import StringIO

import pytest

from problems.shortest_path import shortest_path, solve


def run_solution(input_data: str) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader, writer)

    return writer.getvalue().strip()


def test_shortest_path_function() -> None:
    graph = [
        [],
        [2, 3],
        [1, 4],
        [1, 4],
        [2, 3],
    ]

    assert shortest_path(graph, 1, 4) == 2


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (
            """\
4 4
1 2
1 3
2 4
3 4
1 4
""",
            "2",
        ),
        (
            """\
4 2
1 2
3 4
1 4
""",
            "-1",
        ),
        (
            """\
3 2
1 2
2 3
1 1
""",
            "0",
        ),
    ],
)
def test_solve(input_data: str, expected: str) -> None:
    assert run_solution(input_data) == expected
```

여기서는 두 종류를 모두 테스트한다.

1. `shortest_path()` 알고리즘 함수 자체
2. `solve()`의 입력 파싱과 출력 형식

이 구성이 디버깅하기 가장 좋다.

---

# 공통 실행 함수 분리

문제가 많아지면 `run_solution()`이 모든 테스트 파일에 반복된다. 이를 `tests/conftest.py`에 넣을 수 있다.

```python
# tests/conftest.py

from collections.abc import Callable
from io import StringIO
from typing import Protocol


class ReaderWriterSolution(Protocol):
    def __call__(self, reader: StringIO, writer: StringIO) -> None:
        ...


def execute_solution(
    solution: ReaderWriterSolution,
    input_data: str,
) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solution(reader, writer)

    return writer.getvalue().strip()
```

테스트 코드:

```python
from problems.problem_001 import solve


def test_example() -> None:
    input_data = "10 20\n"
    expected = "30"

    assert execute_solution(solve, input_data) == expected
```

다만 `conftest.py` 안의 일반 함수는 자동으로 import되지는 않는다. 가장 깔끔한 방법은 별도의 유틸리티 모듈을 두는 것이다.

```text
tests/
├─ __init__.py
├─ utils.py
└─ test_problem_001.py
```

```python
# tests/utils.py

from io import StringIO
from typing import Protocol


class Solution(Protocol):
    def __call__(self, reader: StringIO, writer: StringIO) -> None:
        ...


def run_solution(solution: Solution, input_data: str) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solution(reader, writer)

    return writer.getvalue().strip()
```

사용:

```python
from problems.problem_001 import solve
from tests.utils import run_solution


def test_example() -> None:
    assert run_solution(solve, "1 2\n") == "3"
```

---

# 추천 최종 구조

```text
coding-test/
├─ pyproject.toml
├─ src/
│  ├─ __init__.py
│  └─ problems/
│     ├─ __init__.py
│     ├─ boj_1000.py
│     ├─ boj_1260.py
│     └─ shortest_path.py
└─ tests/
   ├─ __init__.py
   ├─ utils.py
   ├─ test_boj_1000.py
   ├─ test_boj_1260.py
   └─ test_shortest_path.py
```

## 자주 사용하는 명령어

전체 테스트:

```bash
uv run pytest
```

상세 테스트:

```bash
uv run pytest -v
```

특정 파일만:

```bash
uv run pytest tests/test_shortest_path.py -v
```

특정 테스트만:

```bash
uv run pytest tests/test_shortest_path.py::test_shortest_path_function -v
```

실패한 테스트부터 다시 실행:

```bash
uv run pytest --lf
```

첫 번째 실패에서 중단:

```bash
uv run pytest -x
```

출력 확인:

```bash
uv run pytest -s
```

실패 시 지역변수 표시:

```bash
uv run pytest -l
```

## 가장 권장하는 원칙

```python
def algorithm(...) -> ...:
    ...
```

```python
def solve(reader=sys.stdin, writer=sys.stdout) -> None:
    ...
```

이 두 계층을 분리하자. 그러면 알고리즘의 정확성과 입출력 형식을 각각 독립적으로 검증할 수 있고, 백준·SWEA·프로그래머스 유형을 한 프로젝트에서 일관되게 관리할 수 있다.

---

### ❓ 질문 (User)
[project]
name = "codingtest"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pytest>=9.1.1",
]
pyproject 구조는 이렇고 codingtest 최상위폴더에서 그냥 main.py로 코딩테스트 문제를 해결하고 테스트 케이스으는 tests/아래에 둘거야.

### 💡 답변 (Assistant)
좋아. 그러면 `src` 구조 없이 아주 단순하게 아래처럼 구성하면 돼.

```text
codingtest/
├── pyproject.toml
├── main.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

## 1. `pyproject.toml`

현재 구조에 `pytest` 설정만 추가하면 된다.

```toml
[project]
name = "codingtest"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pytest>=9.1.1",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "-ra",
]
```

`codingtest` 최상위 폴더에서 실행하면 `main.py`를 그대로 import할 수 있다.

```bash
pytest
```

`uv`를 사용한다면:

```bash
uv run pytest
```

---

## 2. `main.py`

코딩테스트 제출 코드와 테스트 가능한 함수를 분리하는 구성이 좋다.

```python
import sys
from collections.abc import TextIO


def solution(a: int, b: int) -> int:
    return a + b


def solve(
    reader: TextIO = sys.stdin,
    writer: TextIO = sys.stdout,
) -> None:
    a, b = map(int, reader.readline().split())
    answer = solution(a, b)

    print(answer, file=writer)


if __name__ == "__main__":
    solve()
```

각 부분의 역할은 다음과 같다.

- `solution()`: 실제 알고리즘
- `solve()`: 입력 파싱과 출력
- `if __name__ == "__main__"`: 직접 실행하거나 온라인 저지에 제출할 때 동작

직접 실행:

```bash
python main.py
```

```text
1 2
3
```

---

## 3. `tests/test_main.py`

```python
from io import StringIO

import pytest

from main import solution, solve


def run_solve(input_data: str) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader=reader, writer=writer)

    return writer.getvalue().strip()


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 2, 3),
        (10, 20, 30),
        (-5, 3, -2),
        (0, 0, 0),
    ],
)
def test_solution(a: int, b: int, expected: int) -> None:
    assert solution(a, b) == expected


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        ("1 2\n", "3"),
        ("10 20\n", "30"),
        ("-5 3\n", "-2"),
        ("0 0\n", "0"),
    ],
)
def test_solve(input_data: str, expected: str) -> None:
    assert run_solve(input_data) == expected
```

이 테스트는 두 계층을 검증한다.

```text
test_solution → 알고리즘 자체 검증
test_solve    → 입력과 출력까지 포함한 전체 검증
```

---

## 더 단순하게 작성하는 방식

코딩테스트 중에는 함수 분리가 번거로울 수 있다. `solve()` 하나만 테스트해도 된다.

### `main.py`

```python
import sys
from collections.abc import TextIO


def solve(
    reader: TextIO = sys.stdin,
    writer: TextIO = sys.stdout,
) -> None:
    n = int(reader.readline())
    numbers = list(map(int, reader.readline().split()))

    print(sum(numbers[:n]), file=writer)


if __name__ == "__main__":
    solve()
```

### `tests/test_main.py`

```python
from io import StringIO

import pytest

from main import solve


def run_solve(input_data: str) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader, writer)

    return writer.getvalue().strip()


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (
            """\
5
1 2 3 4 5
""",
            "15",
        ),
        (
            """\
3
10 20 30
""",
            "60",
        ),
        (
            """\
4
-1 -2 -3 -4
""",
            "-10",
        ),
    ],
)
def test_solve(input_data: str, expected: str) -> None:
    assert run_solve(input_data) == expected
```

---

## 여러 줄 출력 비교

출력 끝의 개행만 무시하려면 현재처럼 `.strip()`을 사용하면 된다.

```python
return writer.getvalue().strip()
```

예를 들어 출력이 다음과 같다면:

```text
1
2
3
```

테스트는 이렇게 작성할 수 있다.

```python
def test_solve() -> None:
    input_data = """\
3
"""

    expected = """\
1
2
3
"""

    assert run_solve(input_data) == expected.strip()
```

다만 공백까지 정확히 검사해야 하는 문제에서는 `.strip()`이 오류를 숨길 수 있다. 그런 경우에는 마지막 개행만 정규화하는 편이 안전하다.

```python
def normalize_output(output: str) -> str:
    return output.rstrip("\n")
```

```python
def run_solve(input_data: str) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader, writer)

    return writer.getvalue().rstrip("\n")
```

---

## `input()`을 그대로 쓰고 싶다면

`reader`, `writer` 인자를 사용하지 않고 백준 제출 형태 그대로 작성할 수도 있다.

### `main.py`

```python
def solve() -> None:
    a, b = map(int, input().split())
    print(a + b)


if __name__ == "__main__":
    solve()
```

### `tests/test_main.py`

```python
from io import StringIO
import sys

import pytest

from main import solve


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        ("1 2\n", "3\n"),
        ("10 20\n", "30\n"),
    ],
)
def test_solve(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    input_data: str,
    expected: str,
) -> None:
    monkeypatch.setattr(sys, "stdin", StringIO(input_data))

    solve()

    captured = capsys.readouterr()

    assert captured.out == expected
```

이 방식도 가능하지만, 테스트 코드가 조금 복잡해진다. 코딩테스트 연습 환경이라면 다음 형태가 가장 깔끔하다.

```python
def solve(reader=sys.stdin, writer=sys.stdout) -> None:
    ...
```

---

## 추천 최종 구성

### `main.py`

```python
import sys
from collections.abc import TextIO


def solve(
    reader: TextIO = sys.stdin,
    writer: TextIO = sys.stdout,
) -> None:
    # 입력
    a, b = map(int, reader.readline().split())

    # 알고리즘
    answer = a + b

    # 출력
    print(answer, file=writer)


if __name__ == "__main__":
    solve()
```

### `tests/test_main.py`

```python
from io import StringIO

import pytest

from main import solve


def run_solve(input_data: str) -> str:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader, writer)

    return writer.getvalue().rstrip("\n")


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        ("1 2\n", "3"),
        ("10 20\n", "30"),
        ("-5 3\n", "-2"),
    ],
)
def test_solve(input_data: str, expected: str) -> None:
    assert run_solve(input_data) == expected
```

실행 명령은 이것 하나면 충분하다.

```bash
uv run pytest
```

특정 테스트만 실행할 때는:

```bash
uv run pytest tests/test_main.py
```

실패한 테스트부터 다시 실행할 때는:

```bash
uv run pytest --lf
```

첫 실패에서 즉시 중단할 때는:

```bash
uv run pytest -x
```

---

### ❓ 질문 (User)
나는 이렇게 관리 하고 싶어. tests.py 를 실행하면 테스트케이스를 실행한다. 테스트케이스는 .txt나 이런 파일로 불러올거야. 아마 txt만 해도 괜찮을거 같은데,

### 💡 답변 (Assistant)
좋아. 그러면 **`tests.py`를 직접 실행하고, `testcases/*.txt`에서 입력과 정답을 읽어오는 구조**로 맞추는 게 가장 단순하고 관리하기 좋아.

---

### 💡 답변 (Assistant)
좋아. 아래처럼 **`tests.py`가 테스트 실행기 역할**을 하고, 각 테스트 케이스는 `testcases/*.txt` 한 파일에 입력과 기대 출력을 함께 저장하면 돼.

## 프로젝트 구조

```text
codingtest/
├── pyproject.toml
├── main.py
├── tests.py
└── testcases/
    ├── case01.txt
    ├── case02.txt
    └── case03.txt
```

실행은 다음처럼 한다.

```bash
uv run python tests.py
```

---

## 1. 테스트 케이스 파일 형식

`testcases/case01.txt`

```text
[INPUT]
1 2

[OUTPUT]
3
```

`testcases/case02.txt`

```text
[INPUT]
10 20

[OUTPUT]
30
```

여러 줄 입력과 출력도 그대로 작성하면 된다.

`testcases/case03.txt`

```text
[INPUT]
5
1 2 3 4 5

[OUTPUT]
15
```

`[INPUT]`, `[OUTPUT]`을 기준으로 `tests.py`가 입력값과 정답을 분리한다.

---

## 2. `main.py`

`solve()`가 입력 스트림과 출력 스트림을 받을 수 있게 작성한다.

```python
import sys
from collections.abc import TextIO


def solve(
    reader: TextIO = sys.stdin,
    writer: TextIO = sys.stdout,
) -> None:
    a, b = map(int, reader.readline().split())

    answer = a + b

    print(answer, file=writer)


if __name__ == "__main__":
    solve()
```

이렇게 작성하면 온라인 저지 제출 시에는 일반적인 표준 입출력으로 동작한다.

```bash
uv run python main.py
```

테스트할 때는 `StringIO`를 전달한다.

---

## 3. `tests.py`

```python
from io import StringIO
from pathlib import Path

import pytest

from main import solve


BASE_DIR = Path(__file__).resolve().parent
TESTCASE_DIR = BASE_DIR / "testcases"

INPUT_MARKER = "[INPUT]"
OUTPUT_MARKER = "[OUTPUT]"


def load_testcase(path: Path) -> tuple[str, str]:
    """
    하나의 테스트 케이스 파일에서 입력값과 기대 출력을 읽는다.

    파일 형식:

    [INPUT]
    입력 데이터

    [OUTPUT]
    기대 출력
    """
    content = path.read_text(encoding="utf-8")
    content = content.replace("\r\n", "\n")

    if not content.startswith(INPUT_MARKER):
        raise ValueError(
            f"{path.name}: 파일이 {INPUT_MARKER!r}로 시작하지 않습니다."
        )

    if OUTPUT_MARKER not in content:
        raise ValueError(
            f"{path.name}: {OUTPUT_MARKER!r} 구분자가 없습니다."
        )

    body = content[len(INPUT_MARKER):].lstrip("\n")
    input_data, expected_output = body.split(OUTPUT_MARKER, maxsplit=1)

    # 입력은 마지막에 개행 하나를 보장한다.
    input_data = input_data.rstrip("\n") + "\n"

    # 정답은 파일 앞뒤의 개행만 제거한다.
    expected_output = expected_output.strip("\n")

    return input_data, expected_output


def discover_testcases() -> list[Path]:
    """testcases 디렉터리의 모든 txt 파일을 이름순으로 반환한다."""
    if not TESTCASE_DIR.exists():
        raise RuntimeError(
            f"테스트 케이스 디렉터리가 존재하지 않습니다: {TESTCASE_DIR}"
        )

    testcase_paths = sorted(TESTCASE_DIR.glob("*.txt"))

    if not testcase_paths:
        raise RuntimeError(
            f"테스트 케이스가 없습니다: {TESTCASE_DIR}/*.txt"
        )

    return testcase_paths


def normalize_output(output: str) -> str:
    """
    운영체제별 개행 차이와 마지막 개행을 정규화한다.

    줄 중간의 공백은 그대로 유지한다.
    """
    return output.replace("\r\n", "\n").strip("\n")


TESTCASES = [
    pytest.param(
        *load_testcase(path),
        id=path.stem,
    )
    for path in discover_testcases()
]


@pytest.mark.parametrize(
    ("input_data", "expected_output"),
    TESTCASES,
)
def test_solve(
    input_data: str,
    expected_output: str,
) -> None:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader=reader, writer=writer)

    actual_output = writer.getvalue()

    assert normalize_output(actual_output) == normalize_output(expected_output)


if __name__ == "__main__":
    raise SystemExit(
        pytest.main(
            [
                str(Path(__file__).resolve()),
                "-v",
                "-ra",
            ]
        )
    )
```

---

## 4. 실행 결과

```bash
uv run python tests.py
```

정상적으로 통과하면 다음과 비슷하게 출력된다.

```text
============================= test session starts =============================
collected 3 items

tests.py::test_solve[case01] PASSED
tests.py::test_solve[case02] PASSED
tests.py::test_solve[case03] PASSED

============================== 3 passed ======================================
```

테스트 케이스 파일 이름이 pytest의 테스트 ID로 표시된다.

```text
case01.txt → test_solve[case01]
case02.txt → test_solve[case02]
```

---

## 여러 줄 출력 예시

`main.py`

```python
import sys
from collections.abc import TextIO


def solve(
    reader: TextIO = sys.stdin,
    writer: TextIO = sys.stdout,
) -> None:
    n = int(reader.readline())

    for number in range(1, n + 1):
        print(number, file=writer)


if __name__ == "__main__":
    solve()
```

`testcases/case01.txt`

```text
[INPUT]
5

[OUTPUT]
1
2
3
4
5
```

이것도 그대로 비교된다.

---

## 특정 테스트 케이스만 실행하기

파일 이름이 `case03.txt`라면 다음처럼 실행할 수 있다.

```bash
uv run python tests.py -k case03
```

하지만 현재 `tests.py`에서는 명령행 인자를 pytest에 전달하지 않으므로, 이를 지원하려면 마지막 부분을 조금 수정하는 편이 좋다.

```python
if __name__ == "__main__":
    import sys

    pytest_args = [
        str(Path(__file__).resolve()),
        "-v",
        "-ra",
        *sys.argv[1:],
    ]

    raise SystemExit(pytest.main(pytest_args))
```

그러면 다음 명령이 가능해진다.

```bash
uv run python tests.py -k case03
```

첫 실패에서 중단:

```bash
uv run python tests.py -x
```

실패한 테스트만 재실행:

```bash
uv run python tests.py --lf
```

출력까지 표시:

```bash
uv run python tests.py -s
```

최종적으로는 명령행 인자를 전달하는 두 번째 형태를 사용하는 것을 추천한다. 그러면 `tests.py`가 일반적인 pytest 실행기처럼 동작한다.

---

### ❓ 질문 (User)
케이스도 인풋 아웃풋 따로 관리하자. 01.in.txt 01.out.txt 뭐 이런식으로

### 💡 답변 (Assistant)
좋아. 입력과 정답을 완전히 분리해서 다음처럼 관리하면 된다.

```text
codingtest/
├── pyproject.toml
├── main.py
├── tests.py
└── testcases/
    ├── 01.in.txt
    ├── 01.out.txt
    ├── 02.in.txt
    ├── 02.out.txt
    ├── 03.in.txt
    └── 03.out.txt
```

`01.in.txt`와 `01.out.txt`가 하나의 테스트 케이스 쌍이다.

## `main.py`

```python
import sys
from collections.abc import TextIO


def solve(
    reader: TextIO = sys.stdin,
    writer: TextIO = sys.stdout,
) -> None:
    a, b = map(int, reader.readline().split())
    print(a + b, file=writer)


if __name__ == "__main__":
    solve()
```

## 테스트 케이스

### `testcases/01.in.txt`

```text
1 2
```

### `testcases/01.out.txt`

```text
3
```

### `testcases/02.in.txt`

```text
100 200
```

### `testcases/02.out.txt`

```text
300
```

## `tests.py`

```python
import sys
from io import StringIO
from pathlib import Path

import pytest

from main import solve


BASE_DIR = Path(__file__).resolve().parent
TESTCASE_DIR = BASE_DIR / "testcases"

INPUT_SUFFIX = ".in.txt"
OUTPUT_SUFFIX = ".out.txt"


def normalize_newlines(text: str) -> str:
    """Windows와 Unix의 줄바꿈 차이를 통일한다."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def normalize_output(text: str) -> str:
    """
    줄바꿈 형식을 통일하고 마지막 개행만 제거한다.

    줄 내부 공백과 각 줄 끝의 공백은 그대로 비교한다.
    """
    return normalize_newlines(text).rstrip("\n")


def load_text(path: Path) -> str:
    """UTF-8 텍스트 파일을 읽는다."""
    return path.read_text(encoding="utf-8")


def get_case_name(input_path: Path) -> str:
    """
    01.in.txt에서 테스트 케이스 이름인 01을 추출한다.
    """
    filename = input_path.name

    if not filename.endswith(INPUT_SUFFIX):
        raise ValueError(f"올바르지 않은 입력 파일 이름입니다: {filename}")

    return filename.removesuffix(INPUT_SUFFIX)


def discover_testcases() -> list[tuple[str, Path, Path]]:
    """
    testcases 디렉터리에서 입력 파일과 출력 파일의 쌍을 찾는다.

    반환 형식:
        [
            ("01", Path("01.in.txt"), Path("01.out.txt")),
            ("02", Path("02.in.txt"), Path("02.out.txt")),
        ]
    """
    if not TESTCASE_DIR.exists():
        raise RuntimeError(
            f"테스트 케이스 디렉터리가 존재하지 않습니다: {TESTCASE_DIR}"
        )

    input_paths = sorted(TESTCASE_DIR.glob(f"*{INPUT_SUFFIX}"))

    if not input_paths:
        raise RuntimeError(
            f"입력 테스트 케이스가 없습니다: {TESTCASE_DIR}/*{INPUT_SUFFIX}"
        )

    testcases: list[tuple[str, Path, Path]] = []

    for input_path in input_paths:
        case_name = get_case_name(input_path)
        output_path = TESTCASE_DIR / f"{case_name}{OUTPUT_SUFFIX}"

        if not output_path.exists():
            raise RuntimeError(
                f"입력 파일과 대응하는 출력 파일이 없습니다.\n"
                f"입력 파일: {input_path.name}\n"
                f"필요한 파일: {output_path.name}"
            )

        testcases.append((case_name, input_path, output_path))

    return testcases


def load_testcase(input_path: Path, output_path: Path) -> tuple[str, str]:
    """입력 파일과 출력 파일을 읽는다."""
    input_data = normalize_newlines(load_text(input_path))
    expected_output = normalize_output(load_text(output_path))

    # 마지막 줄도 readline()으로 안정적으로 읽을 수 있도록 개행을 보장한다.
    if input_data and not input_data.endswith("\n"):
        input_data += "\n"

    return input_data, expected_output


TESTCASES = [
    pytest.param(
        *load_testcase(input_path, output_path),
        id=case_name,
    )
    for case_name, input_path, output_path in discover_testcases()
]


@pytest.mark.parametrize(
    ("input_data", "expected_output"),
    TESTCASES,
)
def test_solve(
    input_data: str,
    expected_output: str,
) -> None:
    reader = StringIO(input_data)
    writer = StringIO()

    solve(reader=reader, writer=writer)

    actual_output = normalize_output(writer.getvalue())

    assert actual_output == expected_output


if __name__ == "__main__":
    pytest_args = [
        str(Path(__file__).resolve()),
        "-v",
        "-ra",
        *sys.argv[1:],
    ]

    raise SystemExit(pytest.main(pytest_args))
```

## 실행

```bash
uv run python tests.py
```

출력 예시:

```text
tests.py::test_solve[01] PASSED
tests.py::test_solve[02] PASSED
```

특정 테스트 케이스만 실행할 수도 있다.

```bash
uv run python tests.py -k 01
```

첫 번째 실패에서 종료:

```bash
uv run python tests.py -x
```

실패한 테스트만 다시 실행:

```bash
uv run python tests.py --lf
```

## 여러 줄 입출력

### `testcases/03.in.txt`

```text
5
1 2 3 4 5
```

### `testcases/03.out.txt`

```text
15
```

파일 내용은 별도 구분자 없이 온라인 저지에 입력하고 출력되는 내용을 그대로 저장하면 된다.

테스트 케이스를 추가할 때는 다음 두 파일만 함께 만들면 자동으로 인식한다.

```text
04.in.txt
04.out.txt
```

---

### ❓ 질문 (User)
ERROR: usage: pytest [options] [file_or_dir] [file_or_dir] [...]
pytest: error: unrecognized arguments: --v                                                                  
  inifile: D:\codingtest\pyproject.toml                                                                     
  rootdir: D:\codingtest

### 💡 답변 (Assistant)
원인은 단순해. `pytest`의 verbose 옵션은 `--v`가 아니라 아래 둘 중 하나야.

```bash
-v
```

또는

```bash
--verbose
```

아마 다음처럼 실행한 것으로 보여.

```bash
uv run python tests.py --v
```

이를 아래처럼 바꾸면 된다.

```bash
uv run python tests.py -v
```

또는:

```bash
uv run python tests.py --verbose
```

현재 `tests.py`는 이미 내부에서 `-v`를 넣고 있으므로, 사실 옵션 없이 실행해도 상세 출력이 나온다.

```bash
uv run python tests.py
```

현재 코드가 다음 형태이기 때문이다.

```python
pytest_args = [
    str(Path(__file__).resolve()),
    "-v",
    "-ra",
    *sys.argv[1:],
]
```

따라서 사용자가 `--v`를 추가하면 실제로 pytest에는 대략 이렇게 전달된다.

```bash
pytest tests.py -v -ra --v
```

마지막 `--v`가 잘못된 인자라 오류가 발생한 것이다.

## 권장 실행 명령

전체 실행:

```bash
uv run python tests.py
```

특정 케이스만 실행:

```bash
uv run python tests.py -k 01
```

첫 실패 시 중단:

```bash
uv run python tests.py -x
```

출력을 숨기지 않고 표시:

```bash
uv run python tests.py -s
```

상세 출력을 더 늘리기:

```bash
uv run python tests.py -vv
```

결론적으로 이번 오류는 코드 문제가 아니라 명령어 옵션 오타다.

```text
잘못된 옵션: --v
올바른 옵션: -v 또는 --verbose
```

---

### ❓ 질문 (User)
uv run pytest -v 이렇게 하니까 되네

### 💡 답변 (Assistant)
맞아. `pytest`를 직접 실행할 때는 이 명령이 정석이야.

```bash
uv run pytest -v
```

- `uv run`: 프로젝트 가상환경에서 실행
- `pytest`: 테스트 수집 및 실행
- `-v`: 각 테스트 케이스 이름과 결과를 자세히 출력

`--v`는 지원하지 않고, 긴 옵션을 쓰려면 `--verbose`를 사용해야 해.

```bash
uv run pytest --verbose
```

앞으로는 `uv run pytest -v`를 기본 실행 명령으로 사용하면 된다.

---

### ❓ 질문 (User)
아 아니구나 --v 가 오류구나 -v -vv 가 맞는거 같애

### 💡 답변 (Assistant)
맞아. pytest에서는 다음이 올바른 옵션이야.

```bash
uv run pytest -v
```

```bash
uv run pytest -vv
```

차이는 출력 상세 수준이야.

- `-v`: 테스트 함수와 케이스 이름을 자세히 표시
- `-vv`: 테스트 ID와 수집 정보 등을 더 자세히 표시
- `--verbose`: `-v`와 동일
- `--v`: 존재하지 않는 옵션이라 오류 발생

보통 지금처럼 파일 기반 테스트 케이스를 확인할 때는 이 정도면 충분해.

```bash
uv run pytest -v
```

테스트 케이스 이름이 잘리지 않거나 더 자세한 정보를 보고 싶을 때는:

```bash
uv run pytest -vv
```

---

### ❓ 질문 (User)
main.py 는 왜 이러냐... 여기에 문제를 풀건데 음,... 너 알고리즘 테스트 모르는거 아니지?

### 💡 답변 (Assistant)
맞아. 내가 **테스트 편의성을 위해 `main.py` 구조를 과하게 바꿨다.** 코딩테스트 환경이라면 `main.py`는 제출 코드 그대로 작성하고, `tests.py`가 별도 프로세스로 실행해 검증하는 게 맞아.

## 구조

```text
codingtest/
├─ pyproject.toml
├─ main.py
├─ tests.py
└─ testcases/
   ├─ 01.in.txt
   ├─ 01.out.txt
   ├─ 02.in.txt
   └─ 02.out.txt
```

## `main.py`

여기에는 평소 코딩테스트 풀듯이 작성하면 된다.

```python
import sys

input = sys.stdin.readline


def main() -> None:
    a, b = map(int, input().split())
    print(a + b)


if __name__ == "__main__":
    main()
```

함수조차 필요 없으면 이렇게 작성해도 된다.

```python
import sys

input = sys.stdin.readline

a, b = map(int, input().split())
print(a + b)
```

즉, `reader`, `writer`, `StringIO` 같은 테스트용 코드를 `main.py`에 넣을 필요가 없다.

## `tests.py`

`main.py`를 실제 프로그램처럼 실행하고, `.in.txt` 내용을 표준 입력으로 전달한다.

```python
import subprocess
import sys
from pathlib import Path

import pytest


BASE_DIR = Path(__file__).resolve().parent
MAIN_FILE = BASE_DIR / "main.py"
TESTCASE_DIR = BASE_DIR / "testcases"

INPUT_SUFFIX = ".in.txt"
OUTPUT_SUFFIX = ".out.txt"


def normalize_output(text: str) -> str:
    """운영체제별 개행 차이와 마지막 개행을 정규화한다."""
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")


def discover_testcases() -> list[tuple[str, Path, Path]]:
    input_files = sorted(TESTCASE_DIR.glob(f"*{INPUT_SUFFIX}"))

    if not input_files:
        raise RuntimeError(
            f"테스트 케이스를 찾을 수 없습니다: "
            f"{TESTCASE_DIR}/*{INPUT_SUFFIX}"
        )

    testcases: list[tuple[str, Path, Path]] = []

    for input_file in input_files:
        case_name = input_file.name.removesuffix(INPUT_SUFFIX)
        output_file = TESTCASE_DIR / f"{case_name}{OUTPUT_SUFFIX}"

        if not output_file.exists():
            raise RuntimeError(
                f"{input_file.name}에 대응하는 "
                f"{output_file.name}이 없습니다."
            )

        testcases.append((case_name, input_file, output_file))

    return testcases


TESTCASES = [
    pytest.param(input_file, output_file, id=case_name)
    for case_name, input_file, output_file in discover_testcases()
]


@pytest.mark.parametrize(
    ("input_file", "output_file"),
    TESTCASES,
)
def test_main(input_file: Path, output_file: Path) -> None:
    input_data = input_file.read_text(encoding="utf-8")
    expected_output = output_file.read_text(encoding="utf-8")

    try:
        result = subprocess.run(
            [sys.executable, str(MAIN_FILE)],
            input=input_data,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=BASE_DIR,
            timeout=3,
            check=False,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(
            f"{input_file.name}: 실행 제한 시간을 초과했습니다."
        )

    if result.returncode != 0:
        pytest.fail(
            f"{input_file.name}: 실행 중 오류가 발생했습니다.\n"
            f"\n"
            f"[stderr]\n"
            f"{result.stderr}"
        )

    actual_output = normalize_output(result.stdout)
    expected_output = normalize_output(expected_output)

    assert actual_output == expected_output
```

## `pyproject.toml`

파일 이름을 반드시 `tests.py`로 쓸 거라면 pytest 수집 설정이 필요하다. 기본 pytest는 보통 `test_*.py`, `*_test.py`만 자동 수집한다.

```toml
[project]
name = "codingtest"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pytest>=9.1.1",
]

[tool.pytest.ini_options]
python_files = ["tests.py"]
python_functions = ["test_*"]
addopts = ["-ra"]
```

## 테스트 케이스

`testcases/01.in.txt`

```text
1 2
```

`testcases/01.out.txt`

```text
3
```

## 실행

```bash
uv run pytest -v
```

또는 더 자세히:

```bash
uv run pytest -vv
```

특정 케이스만:

```bash
uv run pytest -v -k 01
```

이 방식의 핵심은 명확하다.

- `main.py`: 온라인 저지에 그대로 제출할 코드
- `tests.py`: `main.py`를 외부 프로세스로 실행
- `*.in.txt`: 표준 입력
- `*.out.txt`: 기대 출력

이게 네가 말한 **실제 알고리즘 코딩테스트 환경**에 맞는 구조야.

---

### ❓ 질문 (User)
```main


if __name__ == "__main__":
    N, T = map(int, input().split())
    print(N, T)
```

니가 준 tests.py 넣고 돌렸는데 아무것도 안나와. 
tests/01.in.txt의 내용
4 2
TTCC
TTTM
CCMM
CMMM
1 3 3 3
2 23 16 8
12 6 7 8
12 8 3 5

### 💡 답변 (Assistant)
두 가지가 겹쳤어.

첫째, `tests.py`가 `subprocess.run(..., capture_output=True)`로 `main.py`의 출력을 **캡처**하기 때문에 터미널에 `4 2`가 직접 출력되지 않아.  
둘째, 이전 코드의 테스트 경로가 `testcases/`였는데 지금 파일은 `tests/01.in.txt`에 있어. 경로를 맞춰야 해.

## 권장 구조

```text
codingtest/
├── pyproject.toml
├── main.py
├── tests.py
└── tests/
    ├── 01.in.txt
    └── 01.out.txt
```

`tests/01.out.txt`에는 현재 `main.py`의 예상 출력인 다음 내용을 넣어야 해.

```text
4 2
```

## `main.py`

지금 코드는 정상적이야.

```python
if __name__ == "__main__":
    N, T = map(int, input().split())
    print(N, T)
```

첫 줄만 읽기 때문에 나머지 입력은 사용하지 않아도 문제없어.

## 수정된 `tests.py`

```python
import subprocess
import sys
from pathlib import Path

import pytest


BASE_DIR = Path(__file__).resolve().parent
MAIN_FILE = BASE_DIR / "main.py"
TEST_DIR = BASE_DIR / "tests"

INPUT_SUFFIX = ".in.txt"
OUTPUT_SUFFIX = ".out.txt"


def normalize_output(text: str) -> str:
    return (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
        .rstrip()
    )


def discover_testcases() -> list[tuple[str, Path, Path]]:
    input_files = sorted(TEST_DIR.glob(f"*{INPUT_SUFFIX}"))

    if not input_files:
        raise RuntimeError(
            f"입력 테스트 케이스가 없습니다: "
            f"{TEST_DIR}/*{INPUT_SUFFIX}"
        )

    testcases: list[tuple[str, Path, Path]] = []

    for input_file in input_files:
        case_name = input_file.name.removesuffix(INPUT_SUFFIX)
        output_file = TEST_DIR / f"{case_name}{OUTPUT_SUFFIX}"

        if not output_file.exists():
            raise RuntimeError(
                f"{input_file.name}에 대응하는 "
                f"{output_file.name} 파일이 없습니다."
            )

        testcases.append((case_name, input_file, output_file))

    return testcases


TESTCASES = [
    pytest.param(
        input_file,
        output_file,
        id=case_name,
    )
    for case_name, input_file, output_file in discover_testcases()
]


@pytest.mark.parametrize(
    ("input_file", "output_file"),
    TESTCASES,
)
def test_main(
    input_file: Path,
    output_file: Path,
) -> None:
    input_data = input_file.read_text(encoding="utf-8")
    expected_output = output_file.read_text(encoding="utf-8")

    try:
        result = subprocess.run(
            [sys.executable, str(MAIN_FILE)],
            input=input_data,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=BASE_DIR,
            timeout=3,
            check=False,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(
            f"{input_file.name}: 제한 시간을 초과했습니다.",
            pytrace=False,
        )

    if result.returncode != 0:
        pytest.fail(
            f"{input_file.name}: 실행 중 오류가 발생했습니다.\n\n"
            f"[stderr]\n{result.stderr}",
            pytrace=False,
        )

    actual_output = normalize_output(result.stdout)
    expected_output = normalize_output(expected_output)

    assert actual_output == expected_output
```

## 실행

```bash
uv run pytest -vv
```

정상이라면 이렇게 보여.

```text
tests.py::test_main[01] PASSED
```

`main.py`가 실제로 출력한 내용까지 터미널에서 보고 싶으면 테스트 함수 안에 임시로 다음 줄을 추가해.

```python
print(f"\n[01 실제 출력]\n{result.stdout}")
```

예를 들면:

```python
actual_output = normalize_output(result.stdout)
expected_output = normalize_output(expected_output)

print(f"\n[{input_file.name} 실제 출력]")
print(result.stdout)

assert actual_output == expected_output
```

그리고 캡처를 해제해서 실행해.

```bash
uv run pytest -vv -s
```

그러면 다음처럼 출력돼.

```text
[01.in.txt 실제 출력]
4 2

tests.py::test_main[01] PASSED
```

즉, 기존에 아무것도 안 나온 것은 `main.py`가 실행되지 않은 게 아니라, `tests.py`가 출력을 캡처해서 정답 비교에만 사용했기 때문일 가능성이 가장 커.

---

### ❓ 질문 (User)
[project]
name = "codingtest"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pytest>=9.1.1",
]  혹시 컨피그 파일 고쳐야돼?>

### 💡 답변 (Assistant)
네. **`uv run pytest -v`만 실행해서 최상위의 `tests.py`를 자동으로 찾게 하려면 pytest 설정을 추가해야 해.**

pytest 기본 수집 파일명은 보통 `test_*.py` 또는 `*_test.py`라서, `tests.py`는 자동 수집 대상이 아니야.

```toml
[project]
name = "codingtest"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pytest>=9.1.1",
]

[tool.pytest.ini_options]
python_files = ["tests.py"]
python_functions = ["test_*"]
addopts = ["-ra"]
```

프로젝트 구조는 이렇게 두면 된다.

```text
codingtest/
├── pyproject.toml
├── main.py
├── tests.py
└── tests/
    ├── 01.in.txt
    ├── 01.out.txt
    ├── 02.in.txt
    └── 02.out.txt
```

이제 다음 명령으로 실행된다.

```bash
uv run pytest -v
```

설정 파일을 수정하지 않고 실행하려면 파일명을 직접 지정하면 된다.

```bash
uv run pytest tests.py -v
```

또는 `tests.py`의 이름을 pytest 표준에 맞춰 변경해도 된다.

```text
tests.py → test_main.py
```

그러면 별도의 `python_files` 설정 없이도 자동 수집된다.

현재처럼 **테스트 데이터 디렉터리는 `tests/`, 실행기는 `tests.py`**로 유지하려면 위의 `[tool.pytest.ini_options]` 설정을 추가하는 방식이 맞아.

---

### ❓ 질문 (User)
input_file = WindowsPath('D:/codingtest/tests/01.in.txt')
output_file = WindowsPath('D:/codingtest/tests/01.out.txt')

    @pytest.mark.parametrize(
        ("input_file", "output_file"),
        TESTCASES,
    )
    def test_main(
        input_file: Path,
        output_file: Path,
    ) -> None:
        input_data = input_file.read_text(encoding="utf-8")
        expected_output = output_file.read_text(encoding="utf-8")
    
        try:
            result = subprocess.run(
                [sys.executable, str(MAIN_FILE)],
                input=input_data,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=BASE_DIR,
                timeout=3,
                check=False,
            )
        except subprocess.TimeoutExpired:
            pytest.fail(
                f"{input_file.name}: 제한 시간을 초과했습니다.",
                pytrace=False,
            )
    
        if result.returncode != 0:
            pytest.fail(
                f"{input_file.name}: 실행 중 오류가 발생했습니다.\n\n"
                f"[stderr]\n{result.stderr}",
                pytrace=False,
            )
    
        actual_output = normalize_output(result.stdout)
        expected_output = normalize_output(expected_output)
    
>       assert actual_output == expected_output
E       AssertionError: assert '4 2' == '33 0 0 14 17...9 0 1 10 21 4'
E         
E         + 4 2
E         - 33 0 0 14 17 31 7
E         - 35 9 0 1 10 21 4

tests.py:98: AssertionError
======================================== short test summary info =========================================
FAILED tests.py::test_main[01] - AssertionError: assert '4 2' == '33 0 0 14 17...9 0 1 10 21 4'

### 💡 답변 (Assistant)
지금 테스트 환경은 **정상적으로 동작하고 있어.** 실패 원인은 `main.py` 출력과 `01.out.txt`의 정답이 다르기 때문이야.

현재 `main.py`:

```python
if __name__ == "__main__":
    N, T = map(int, input().split())
    print(N, T)
```

따라서 실제 출력은 첫 줄을 그대로 읽은:

```text
4 2
```

그런데 `tests/01.out.txt`에는 다음 정답이 들어 있어.

```text
33 0 0 14 17 31 7
35 9 0 1 10 21 4
```

pytest가 비교한 내용도 정확히 이것이야.

```text
실제 출력: 4 2
기대 출력:
33 0 0 14 17 31 7
35 9 0 1 10 21 4
```

즉, `tests.py`나 `pyproject.toml` 문제가 아니라 **아직 `main.py`에 문제 풀이 로직이 구현되지 않은 상태**라서 실패한 거야.

## 현재 단계에서 테스트 통과 여부만 확인하려면

임시로 `01.out.txt`를 다음처럼 바꾸면 통과해.

```text
4 2
```

하지만 실제 문제를 풀려는 목적이라면 `01.out.txt`는 그대로 두고, `main.py`에서 전체 입력을 처리해서 해당 결과를 출력해야 해.

입력 구조만 읽어보면 아마 다음 형태로 보인다.

```python
import sys

input = sys.stdin.readline


if __name__ == "__main__":
    N, T = map(int, input().split())

    grid = [list(input().strip()) for _ in range(N)]
    costs = [list(map(int, input().split())) for _ in range(N)]

    print(N, T)
    print(grid)
    print(costs)
```

주어진 입력에서는:

```python
N == 4
T == 2

grid == [
    ["T", "T", "C", "C"],
    ["T", "T", "T", "M"],
    ["C", "C", "M", "M"],
    ["C", "M", "M", "M"],
]

costs == [
    [1, 3, 3, 3],
    [2, 23, 16, 8],
    [12, 6, 7, 8],
    [12, 8, 3, 5],
]
```

테스트는 입력 파일 전체를 `main.py`의 표준 입력으로 정상 전달하고 있어. 이제 `main.py`가 기대 정답을 계산하도록 알고리즘만 작성하면 된다.

참고로 실패 메시지에서:

```text
+ 4 2
- 33 0 0 14 17 31 7
- 35 9 0 1 10 21 4
```

`+`는 실제 출력이고, `-`는 기대 출력이야. 현재 테스트 러너는 의도대로 잘 만들어진 상태다.

---

### ❓ 질문 (User)
ㅇㅇ 아니 이제 제대로 동작한다고

### 💡 답변 (Assistant)
좋아, 이제 환경은 제대로 잡혔네.

앞으로는:

- `main.py`에 코딩테스트 풀이 작성
- `tests/01.in.txt`, `tests/01.out.txt`처럼 케이스 추가
- `uv run pytest -v`로 전체 검증

이 흐름으로 계속 쓰면 돼. 특히 실패할 때 pytest가 실제 출력과 기대 출력을 바로 비교해 주니까 디버깅도 훨씬 편해질 거야.

---

### ❓ 질문 (User)
이거 쓸 려면 내가 직접 코드를 다 짜야하잖아. 튜토리얼 코드 같은거 있나 템플릿코드나

### 💡 답변 (Assistant)
있어. 한 번만 만들어 두면 이후에는 **`main.py`와 입출력 파일만 수정**하면 되는 템플릿으로 구성하면 돼.

## 최종 구조

```text
codingtest/
├─ pyproject.toml
├─ main.py
├─ tests.py
├─ new_case.py
└─ tests/
   ├─ 01.in.txt
   └─ 01.out.txt
```

---

## 1. `pyproject.toml`

```toml
[project]
name = "codingtest"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pytest>=9.1.1",
]

[tool.pytest.ini_options]
python_files = ["tests.py"]
python_functions = ["test_*"]
testpaths = ["."]
addopts = [
    "-ra",
]
```

이제 다음 명령으로 `tests.py`가 자동 실행돼.

```bash
uv run pytest -v
```

---

## 2. `main.py`

온라인 저지에 그대로 제출할 수 있는 기본 템플릿이야.

```python
import sys

input = sys.stdin.readline


def solve() -> None:
    # 입력
    n, t = map(int, input().split())

    # 문제 풀이
    answer = n + t

    # 출력
    print(answer)


if __name__ == "__main__":
    solve()
```

문제를 풀 때는 사실상 `solve()` 내부만 바꾸면 돼.

### 격자 문제 기본형

```python
import sys

input = sys.stdin.readline


def solve() -> None:
    n, t = map(int, input().split())

    board = [
        list(input().strip())
        for _ in range(n)
    ]

    values = [
        list(map(int, input().split()))
        for _ in range(n)
    ]

    # 알고리즘 작성
    answer = 0

    print(answer)


if __name__ == "__main__":
    solve()
```

---

## 3. 재사용할 `tests.py`

이 파일은 이후에 거의 수정하지 않아도 돼.

```python
import os
import subprocess
import sys
from pathlib import Path

import pytest


BASE_DIR = Path(__file__).resolve().parent
MAIN_FILE = BASE_DIR / "main.py"
TEST_DIR = BASE_DIR / "tests"

INPUT_SUFFIX = ".in.txt"
OUTPUT_SUFFIX = ".out.txt"

TIMEOUT_SECONDS = 3


def normalize_output(text: str) -> str:
    """
    운영체제별 줄바꿈 차이를 제거한다.

    마지막 개행과 각 줄 끝의 불필요한 공백은 무시하지만,
    줄 내부 공백은 그대로 비교한다.
    """
    normalized = (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    return "\n".join(
        line.rstrip()
        for line in normalized.strip().splitlines()
    )


def discover_testcases() -> list[tuple[str, Path, Path]]:
    """
    tests 디렉터리에서 다음과 같은 파일 쌍을 찾는다.

    01.in.txt
    01.out.txt
    """
    if not MAIN_FILE.exists():
        raise RuntimeError(
            f"main.py를 찾을 수 없습니다: {MAIN_FILE}"
        )

    if not TEST_DIR.exists():
        raise RuntimeError(
            f"tests 디렉터리를 찾을 수 없습니다: {TEST_DIR}"
        )

    input_files = sorted(TEST_DIR.glob(f"*{INPUT_SUFFIX}"))

    if not input_files:
        raise RuntimeError(
            f"테스트 입력 파일이 없습니다: "
            f"{TEST_DIR}/*{INPUT_SUFFIX}"
        )

    testcases: list[tuple[str, Path, Path]] = []

    for input_file in input_files:
        case_name = input_file.name.removesuffix(INPUT_SUFFIX)
        output_file = TEST_DIR / f"{case_name}{OUTPUT_SUFFIX}"

        if not output_file.exists():
            raise RuntimeError(
                f"{input_file.name}에 대응하는 "
                f"{output_file.name} 파일이 없습니다."
            )

        testcases.append(
            (case_name, input_file, output_file)
        )

    return testcases


TESTCASES = [
    pytest.param(
        input_file,
        output_file,
        id=case_name,
    )
    for case_name, input_file, output_file
    in discover_testcases()
]


@pytest.mark.parametrize(
    ("input_file", "output_file"),
    TESTCASES,
)
def test_main(
    input_file: Path,
    output_file: Path,
) -> None:
    input_data = input_file.read_text(encoding="utf-8")
    expected_output = output_file.read_text(encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                str(MAIN_FILE),
            ],
            input=input_data,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=BASE_DIR,
            env=env,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )

    except subprocess.TimeoutExpired:
        pytest.fail(
            f"{input_file.name}: "
            f"{TIMEOUT_SECONDS}초 제한 시간을 초과했습니다.",
            pytrace=False,
        )

    if result.returncode != 0:
        pytest.fail(
            f"{input_file.name}: 실행 중 오류가 발생했습니다.\n\n"
            f"[표준 오류]\n"
            f"{result.stderr}",
            pytrace=False,
        )

    actual_output = normalize_output(result.stdout)
    expected_output = normalize_output(expected_output)

    assert actual_output == expected_output, (
        f"\n\n"
        f"[입력]\n"
        f"{input_data}\n"
        f"\n"
        f"[기대 출력]\n"
        f"{expected_output}\n"
        f"\n"
        f"[실제 출력]\n"
        f"{actual_output}\n"
    )
```

이 테스트 러너는 다음을 자동 처리해.

- 모든 `*.in.txt` 파일 탐색
- 같은 이름의 `*.out.txt` 연결
- `main.py`를 실제 프로그램처럼 별도 실행
- 표준 입력 전달
- 출력 비교
- 런타임 에러 표시
- 무한루프 및 시간 초과 감지
- Windows UTF-8 처리

---

## 4. 테스트 파일 자동 생성기 `new_case.py`

매번 직접 `01.in.txt`, `01.out.txt`를 만들기 번거로우니 자동 생성기를 두면 편해.

```python
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TEST_DIR = BASE_DIR / "tests"


def find_next_case_number() -> int:
    TEST_DIR.mkdir(exist_ok=True)

    numbers: list[int] = []

    for path in TEST_DIR.glob("*.in.txt"):
        case_name = path.name.removesuffix(".in.txt")

        if case_name.isdigit():
            numbers.append(int(case_name))

    return max(numbers, default=0) + 1


def main() -> None:
    case_number = find_next_case_number()
    case_name = f"{case_number:02d}"

    input_file = TEST_DIR / f"{case_name}.in.txt"
    output_file = TEST_DIR / f"{case_name}.out.txt"

    input_file.touch()
    output_file.touch()

    print(f"생성 완료: {input_file}")
    print(f"생성 완료: {output_file}")


if __name__ == "__main__":
    main()
```

실행:

```bash
uv run python new_case.py
```

처음 실행하면:

```text
tests/01.in.txt
tests/01.out.txt
```

다시 실행하면:

```text
tests/02.in.txt
tests/02.out.txt
```

자동으로 다음 번호가 만들어져.

---

## 5. 실제 사용 방법

### `tests/01.in.txt`

```text
4 2
TTCC
TTTM
CCMM
CMMM
1 3 3 3
2 23 16 8
12 6 7 8
12 8 3 5
```

### `tests/01.out.txt`

```text
33 0 0 14 17 31 7
35 9 0 1 10 21 4
```

테스트 실행:

```bash
uv run pytest -v
```

더 자세히:

```bash
uv run pytest -vv
```

특정 케이스만:

```bash
uv run pytest -v -k 01
```

첫 번째 실패에서 중단:

```bash
uv run pytest -v -x
```

이제부터는 대부분 다음 순서만 반복하면 돼.

```text
1. main.py에 문제 풀이
2. new_case.py로 케이스 생성
3. .in.txt와 .out.txt에 예제 복사
4. uv run pytest -v 실행
```

---
