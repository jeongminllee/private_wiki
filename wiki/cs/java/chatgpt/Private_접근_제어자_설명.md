---
type: Concept
title: "Private 접근 제어자 설명"
description: "CS - Java 프로그래밍 - ChatGPT 대화 추출 노트 (2026-03-10)"
tags: [cs, chatgpt-export]
timestamp: 2026-03-10
status: active
---

# Private 접근 제어자 설명

> **카테고리**: `CS - Java 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-03-10

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
정보처리기사 시험 관점에서 핵심 개념을 중심으로 설명하겠습니다.

---

# ✅ 문제 분석

질문의 핵심 포인트는 다음입니다.

- `sum()` 메서드의 접근 제어자가 **private**
- 그런데 `main()`에서 **문제없이 호출 가능**
- **private인데 왜 접근이 가능한가?**

→ 핵심 키워드  
**접근 제어자 / 클래스 내부 접근 / private 범위**

---

# 🎯 정답 개념  
👉 **private 접근 제어자의 범위**

📌 **같은 클래스 내부에서는 private 멤버 접근이 가능하다.**

---

# 📌 정답인 이유

Java의 접근 제어자(access modifier)는 **접근 가능한 범위(scope)** 를 기준으로 동작합니다.

| 접근제어자 | 같은 클래스 | 같은 패키지 | 자식 클래스 | 다른 패키지 |
|---|---|---|---|---|
| private | ✔ 가능 | ✖ 불가 | ✖ 불가 | ✖ 불가 |
| default | ✔ 가능 | ✔ 가능 | ✖ 불가 | ✖ 불가 |
| protected | ✔ 가능 | ✔ 가능 | ✔ 가능 | ✖ 불가 |
| public | ✔ 가능 | ✔ 가능 | ✔ 가능 | ✔ 가능 |

여기서 **private 특징**은 다음과 같습니다.

> **같은 클래스 내부에서는 언제든 접근 가능**

---

### 현재 코드 구조

```java
public class Hello {

    public static void main(String[] args) {
        s = sum(i, 10);
    }

    private static int sum(int i, int j) {
        return i + j;
    }
}
```

구조를 보면

```
Hello 클래스
 ├─ main()
 └─ sum()
```

즉

```
main() → sum()
```

**같은 클래스 내부 메서드 호출**

따라서 **private이어도 접근 가능**합니다.

---

# 🔎 헷갈릴 수 있는 오해

### ❌ private이면 어디서도 접근 못한다

이건 **틀린 이해**입니다.

정확한 의미는

> **다른 클래스에서 접근 불가능**

입니다.

---

### 예시 (접근 불가능)

```java
class Test {
    public static void main(String[] args) {
        Hello.sum(10,10);  // 컴파일 에러
    }
}
```

왜냐하면

```
Test 클래스 → Hello 클래스 private 메서드 접근
```

이기 때문입니다.

---

# 📚 추가로 공부해야 할 것 (시험에서 매우 중요)

정보처리기사에서 **자주 출제되는 Java 접근 제어자**

### 1️⃣ 접근 제어자 범위

| 제어자 | 범위 |
|---|---|
| private | 같은 클래스 |
| default | 같은 패키지 |
| protected | 같은 패키지 + 상속 |
| public | 모든 곳 |

시험에서는 이런 식으로 나옵니다.

> "같은 패키지에서만 접근 가능한 접근 제어자"

정답  
👉 **default**

---

### 2️⃣ static 메서드 특징

현재 코드에서 또 중요한 포인트가 있습니다.

```java
private static int sum(int i, int j)
```

왜 `static`이냐?

`main()`이 **static 메서드**이기 때문입니다.

Java 규칙

> static 메서드에서는 static 메서드만 직접 호출 가능

그래서

```
main() → sum()
```

가능하려면 `sum()`도 **static**이어야 합니다.

---

# 🧠 실기시험 포인트 정리

✔ **private → 같은 클래스 내부에서만 접근 가능**  
✔ **다른 클래스에서는 접근 불가**  
✔ **main()은 static 메서드**  
✔ **static 메서드에서는 static 메서드 호출**

---

원하시면 제가 **정보처리기사에서 100% 나오는 Java 문제 유형 5개 (접근제어자 / static / 객체생성)**도 같이 정리해 드리겠습니다.  
이 부분은 **실기에서 반복 출제되는 영역**입니다.

---

### ❓ 질문 (User)
```
public class Hello {
	public static void main(String[] args) {
		int i = 20;
		int s;
		char a;
		String b;

		s = sum(i, 10);
		// s = i + 10;
		a = '?';
		b = "Hello";
		System.out.println(a);
		System.out.println(b);
		System.out.println(s);

	}

	private static int sum(int i, int j) { // TODO Auto-generated method stub
		return i + j;
	}

}
```
클래스 sum 에서 public 이 아니라 private에서도 접근이 가능한데, 원리가 궁금해.
