---
type: Error Note
title: "PHP 코드 오류 수정"
description: "Errors - General Troubleshooting - ChatGPT 대화 추출 노트 (2026-05-08)"
tags: [errors, chatgpt-export]
timestamp: 2026-05-08
status: active
---

# PHP 코드 오류 수정

> **카테고리**: `Errors - General Troubleshooting`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-08

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
에러 원인은 **바로 위 줄의 세미콜론(`;`) 누락**입니다.

현재 코드에서 이 부분이 문제입니다.

```php
$stock = $_POST['stock']
    
$sql = "INSERT INTO Book SET bookname='$bookname' publisher='$publisher' price='$price' stock='$stock'";
```

PHP는 문장 끝에 `;`가 필요합니다. 그래서 다음 줄의 `$sql`을 갑자기 만난 것으로 해석해서:

```text
unexpected variable "$sql"
```

오류가 난 것입니다.

수정하면:

```php
$stock = $_POST['stock'];
```

그런데 추가로 아래 줄도 세미콜론이 빠져 있습니다.

```php
$result = mysqli_query($conn, $sql)
```

이것도 이렇게 고쳐야 합니다.

```php
$result = mysqli_query($conn, $sql);
```

그리고 SQL 문법도 현재는 틀렸습니다. `SET` 방식에서는 컬럼 사이에 **쉼표**가 필요합니다.

현재 코드:

```php
$sql = "INSERT INTO Book SET bookname='$bookname' publisher='$publisher' price='$price' stock='$stock'";
```

수정:

```php
$sql = "INSERT INTO Book SET bookname='$bookname', publisher='$publisher', price='$price', stock='$stock'";
```

정리하면 최소 수정 코드는 이렇습니다.

```php
$bookid = $_POST['bookid'];
$bookname = $_POST['bookname'];
$publisher = $_POST['publisher'];
$price = $_POST['price'];
$stock = $_POST['stock'];

$sql = "INSERT INTO Book SET bookname='$bookname', publisher='$publisher', price='$price', stock='$stock'";
$result = mysqli_query($conn, $sql);
```

다만 `bookid`까지 넣으려면 이렇게 해야 합니다.

```php
$sql = "INSERT INTO Book SET bookid='$bookid', bookname='$bookname', publisher='$publisher', price='$price', stock='$stock'";
```

또는 더 일반적인 `INSERT INTO ... VALUES` 방식으로는:

```php
$sql = "INSERT INTO Book(bookid, bookname, publisher, price, stock)
        VALUES('$bookid', '$bookname', '$publisher', '$price', '$stock')";
```

지금 에러의 직접 원인은 **`$stock = $_POST['stock']` 뒤에 세미콜론이 없어서**입니다.  
그다음 실행하면 SQL 문법 오류가 날 가능성이 높으니, 쉼표와 `mysqli_query` 뒤 세미콜론까지 같이 고치면 됩니다.

---

### ❓ 질문 (User)
```
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href="book.css" rel="stylesheet">
</head>
<body>
<h2 class="styled-header">마당서점 도서목록</h2>
<?php
	$conn = mysqli_connect('localhost', 'madang', 'madang', 'bookstore');
	if (!$conn){
		echo 'Connection Error';
		echo mysqli_connect_error();
		exit();
	}

    $bookid = $_POST['bookid'];
    $bookname = $_POST['bookname'];
    $publisher = $_POST['publisher'];
    $price = $_POST['price'];
    $stock = $_POST['stock']
    
    $sql = "INSERT INTO Book SET bookname='$bookname' publisher='$publisher' price='$price' stock='$stock'";
    $result = mysqli_query($conn, $sql)
?>
<b><?=$sql?></b>
<br>

<?php
    if($result) {
        echo '<p>추가 완료</p>';
    } else {
        echo "<p>추가 실패</p>";
    }
     
?>
<br>
<a href="/booklist_ver2.php" class="w-brn">뒤로</a>
</body>
</html>
```
Parse error: syntax error, unexpected variable "$sql" in C:\xampp\htdocs\action_insertbook.php on line 22

### 💡 답변 (Assistant)
이번 에러는 PHP 문법 문제가 아니라 **DB 테이블 구조 문제**입니다.

에러 메시지:

```text
Field 'custid' doesn't have a default value
```

뜻은:

> `Customer` 테이블의 `custid` 컬럼은 반드시 값이 있어야 하는데, INSERT 할 때 `custid` 값을 안 넣었고, DB에도 자동 기본값이 설정되어 있지 않다.

현재 코드에서 `custid`를 주석 처리했죠.

```php
// $custid = $_POST['custid'];
```

그리고 SQL에도 `custid`가 없습니다.

```php
$sql = "INSERT INTO Customer SET name='$name', address='$address', phone='$phone', email='$email'";
```

그래서 MySQL이 이렇게 말하는 겁니다.

> `custid` 값은 어떻게 넣으라는 거야?

---

## 해결 방법 1: custid를 직접 입력해서 INSERT 하기

폼에서 `custid`를 입력받는 구조라면 이렇게 해야 합니다.

```php
$custid = $_POST['custid'];
$name = $_POST['name'];
$address = $_POST['address'];
$phone = $_POST['phone'];
$email = $_POST['email'];

$sql = "INSERT INTO Customer SET custid='$custid', name='$name', address='$address', phone='$phone', email='$email'";
$result = mysqli_query($conn, $sql);
```

또는 일반적인 INSERT 문법으로 쓰면:

```php
$sql = "INSERT INTO Customer(custid, name, address, phone, email)
        VALUES('$custid', '$name', '$address', '$phone', '$email')";
$result = mysqli_query($conn, $sql);
```

---

## 해결 방법 2: custid를 AUTO_INCREMENT로 바꾸기

보통 회원번호 같은 `custid`는 직접 입력하지 않고 DB가 자동으로 증가시키는 방식이 더 자연스럽습니다.

MySQL에서 `Customer` 테이블의 `custid`를 자동 증가 컬럼으로 바꾸면 됩니다.

```sql
ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT;
```

단, `custid`가 기본키가 아니라면 먼저 기본키 설정도 필요할 수 있습니다.

```sql
ALTER TABLE Customer
ADD PRIMARY KEY (custid);
```

이미 기본키가 있으면 이 명령은 필요 없습니다.

그 후에는 PHP 코드에서 `custid` 없이 INSERT 해도 됩니다.

```php
$sql = "INSERT INTO Customer(name, address, phone, email)
        VALUES('$name', '$address', '$phone', '$email')";
$result = mysqli_query($conn, $sql);
```

---

## 지금 코드에서 최소 수정

`custid`를 자동 증가로 설정하지 않은 상태라면, 최소 수정은 이렇게입니다.

```php
$custid = $_POST['custid'];
$name = $_POST['name'];
$address = $_POST['address'];
$phone = $_POST['phone'];
$email = $_POST['email'];

$sql = "INSERT INTO Customer(custid, name, address, phone, email)
        VALUES('$custid', '$name', '$address', '$phone', '$email')";
$result = mysqli_query($conn, $sql);
```

그리고 이것도 세미콜론 붙여주는 게 좋습니다.

```php
$result = mysqli_query($conn, $sql);
```

---

## 결론

현재 에러의 핵심 원인은 이것입니다.

```php
// $custid = $_POST['custid'];
```

`custid`를 주석 처리했는데, DB에서는 `custid`가 필수값으로 설정되어 있습니다.

따라서 둘 중 하나를 선택해야 합니다.

1. **폼에서 custid를 받아서 INSERT에 포함한다.**
2. **DB에서 custid를 AUTO_INCREMENT로 설정한다.**

회원번호라면 보통은 **2번, AUTO_INCREMENT 방식**이 더 좋습니다.

---

### ❓ 질문 (User)
```
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href="book.css" rel="stylesheet">
</head>
<body>
<h2 class="styled-header">마당서점 회원목록</h2>
<?php
	$conn = mysqli_connect('localhost', 'madang', 'madang', 'bookstore');
	if (!$conn){
		echo 'Connection Error';
		echo mysqli_connect_error();
		exit();
	}

    // $custid = $_POST['custid'];
    $name = $_POST['name'];
    $address = $_POST['address'];
    $phone = $_POST['phone'];
    $email = $_POST['email'];
    
    $sql = "INSERT INTO Customer SET name='$name', address='$address', phone='$phone', email='$email'";
    $result = mysqli_query($conn, $sql)
?>
<b><?=$sql?></b>
<br>

<?php
    if($result) {
        echo '<p>추가 완료</p>';
    } else {
        echo "<p>추가 실패</p>";
    }
     
?>
<br>
<a href="/customerlist.php" class="w-brn">뒤로</a>
</body>
</html>
```
Fatal error: Uncaught mysqli_sql_exception: Field 'custid' doesn't have a default value

### 💡 답변 (Assistant)
아니요. **기본키 `PRIMARY KEY`라고 해서 `AUTO_INCREMENT`가 자동으로 적용되지는 않습니다.**

정확히는 두 개가 서로 다른 설정입니다.

```sql
custid INT PRIMARY KEY
```

이건:

> `custid`는 중복 불가 + NULL 불가인 기본키다.

라는 뜻이고,

```sql
custid INT PRIMARY KEY AUTO_INCREMENT
```

이건:

> `custid`는 기본키이고, INSERT 할 때 값을 안 넣으면 MySQL이 자동으로 1, 2, 3… 증가시켜 넣는다.

라는 뜻입니다.

즉, `PRIMARY KEY`만 있으면 **반드시 직접 값을 넣어야 합니다.**

---

현재 테이블이 아마 이런 상태일 가능성이 높습니다.

```sql
CREATE TABLE Customer (
    custid INT PRIMARY KEY,
    name VARCHAR(40),
    address VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(50)
);
```

이 상태에서 이렇게 INSERT 하면:

```sql
INSERT INTO Customer(name, address, phone, email)
VALUES('홍길동', '서울', '010-1111-2222', 'test@test.com');
```

`custid` 값을 안 넣었기 때문에 에러가 납니다.

```text
Field 'custid' doesn't have a default value
```

---

## 확인 방법

MySQL에서 아래 명령을 실행해보세요.

```sql
DESC Customer;
```

또는:

```sql
SHOW CREATE TABLE Customer;
```

`DESC Customer;` 결과에서 `Extra` 컬럼에 `auto_increment`가 있어야 자동 증가가 적용된 상태입니다.

예상되는 현재 상태는 아마 이런 식일 겁니다.

| Field | Key | Extra |
|---|---|---|
| custid | PRI |  |

정상적으로 자동 증가가 적용되어 있으면 이렇게 나와야 합니다.

| Field | Key | Extra |
|---|---|---|
| custid | PRI | auto_increment |

---

## 해결 방법

`custid`를 자동 증가로 바꾸려면:

```sql
ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT;
```

만약 오류가 나면 기존 기본키가 제대로 잡혀 있는지 확인한 뒤, 필요하면 이렇게 합니다.

```sql
ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT PRIMARY KEY;
```

다만 이미 기본키가 있으면 `PRIMARY KEY`를 또 붙이면 중복 기본키 오류가 날 수 있습니다. 그래서 먼저 이걸 확인하는 게 좋습니다.

```sql
SHOW CREATE TABLE Customer;
```

---

## PHP 코드는 이렇게 쓰면 됩니다

`custid`가 `AUTO_INCREMENT`로 설정된 후에는 `custid`를 INSERT에 넣지 않는 게 맞습니다.

```php
$name = $_POST['name'];
$address = $_POST['address'];
$phone = $_POST['phone'];
$email = $_POST['email'];

$sql = "INSERT INTO Customer(name, address, phone, email)
        VALUES('$name', '$address', '$phone', '$email')";
$result = mysqli_query($conn, $sql);
```

핵심은 이겁니다.

> **기본키 = 중복/NULL 방지 역할**  
> **AUTO_INCREMENT = 값을 자동 생성하는 역할**

`custid`가 기본키인 것과 자동으로 번호가 증가하는 것은 별개의 설정입니다.

---

### ❓ 질문 (User)
custid 가 기본키 이면 auto_increment 는 자동으로 적용 되는거 아니야?> custid는 기본키 맞는데

### 💡 답변 (Assistant)
에러 원인은 SQL을 이렇게 **`MODIFY ...`만 단독으로 실행했기 때문**입니다.

`MODIFY`는 반드시 `ALTER TABLE 테이블명` 뒤에 붙어야 합니다.

```sql
ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT;
```

즉, 전체 문장은 이렇게 실행해야 합니다.

```sql
ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT;
```

---

그런데 `custid`가 기본키가 맞다면 위 명령으로 보통 됩니다.  
만약 그래도 오류가 나면 테이블 구조를 먼저 확인해보세요.

```sql
DESC Customer;
```

또는 더 정확하게:

```sql
SHOW CREATE TABLE Customer;
```

`custid`가 실제로 기본키인지, 타입이 `INT`인지, 이미 다른 설정이 있는지 확인할 수 있습니다.

---

## 만약 기본키가 아직 제대로 안 잡혀 있다면

이 경우는 이렇게 해야 합니다.

```sql
ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT,
ADD PRIMARY KEY (custid);
```

하지만 이미 `custid`가 기본키라면 `ADD PRIMARY KEY`를 또 하면 오류가 납니다.

---

## 추천 순서

먼저 이것부터 실행하세요.

```sql
SHOW CREATE TABLE Customer;
```

그 결과에서 `custid` 부분이 현재 이렇게 되어 있을 가능성이 큽니다.

```sql
`custid` int NOT NULL
```

또는:

```sql
`custid` int NOT NULL,
PRIMARY KEY (`custid`)
```

그러면 아래 명령만 실행하면 됩니다.

```sql
ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT;
```

---

그리고 PHP 코드는 `custid` 없이 INSERT하면 됩니다.

```php
$sql = "INSERT INTO Customer(name, address, phone, email)
        VALUES('$name', '$address', '$phone', '$email')";
$result = mysqli_query($conn, $sql);
```

핵심은 이겁니다.

```sql
MODIFY custid INT NOT NULL AUTO_INCREMENT;
```

이건 단독 SQL이 아니라,

```sql
ALTER TABLE Customer MODIFY custid INT NOT NULL AUTO_INCREMENT;
```

처럼 **ALTER TABLE과 함께 써야 합니다.**

---

### ❓ 질문 (User)
12:05:59	MODIFY custid int not null AUTO_INCREMENT	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'MODIFY custid int not null AUTO_INCREMENT' at line 1	0.000 sec

### 💡 답변 (Assistant)
이번 에러는 아주 중요한 내용입니다.

```text
Cannot change column 'custid': used in a foreign key constraint 'orders_ibfk_1' of table 'bookstore.orders'
```

뜻은:

> `Customer.custid`가 `Orders` 테이블에서 외래키로 참조되고 있기 때문에, 그냥 컬럼 구조를 바꿀 수 없다.

즉 구조가 아마 이런 관계입니다.

```text
Customer.custid  ←  Orders.custid
   기본키              외래키
```

`Orders` 테이블이 `Customer`의 `custid`를 참조하고 있으므로 MySQL이 함부로 변경하지 못하게 막은 것입니다.

---

## 해결 순서

외래키를 잠시 삭제한 뒤, `Customer.custid`를 `AUTO_INCREMENT`로 바꾸고, 다시 외래키를 걸어야 합니다.

먼저 현재 외래키 이름을 확인합니다.

```sql
SHOW CREATE TABLE Orders;
```

에러 메시지에 이미 이름이 나와 있습니다.

```text
orders_ibfk_1
```

그러면 아래 순서로 실행하면 됩니다.

```sql
ALTER TABLE Orders
DROP FOREIGN KEY orders_ibfk_1;
```

그다음 `Customer.custid`를 `AUTO_INCREMENT`로 변경합니다.

```sql
ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT;
```

그다음 다시 외래키를 추가합니다.

```sql
ALTER TABLE Orders
ADD CONSTRAINT orders_ibfk_1
FOREIGN KEY (custid) REFERENCES Customer(custid);
```

---

## 전체 실행 코드

```sql
ALTER TABLE Orders
DROP FOREIGN KEY orders_ibfk_1;

ALTER TABLE Customer
MODIFY custid INT NOT NULL AUTO_INCREMENT;

ALTER TABLE Orders
ADD CONSTRAINT orders_ibfk_1
FOREIGN KEY (custid) REFERENCES Customer(custid);
```

---

## 주의할 점

`Orders.custid`와 `Customer.custid`의 타입이 서로 같아야 합니다.

예를 들어 `Customer.custid`가:

```sql
INT NOT NULL AUTO_INCREMENT
```

이면 `Orders.custid`도 보통:

```sql
INT
```

여야 합니다.

확인은 이렇게 합니다.

```sql
DESC Customer;
DESC Orders;
```

---

## 더 안전한 방식

작업 전에 현재 테이블 구조를 먼저 확인하세요.

```sql
SHOW CREATE TABLE Customer;
SHOW CREATE TABLE Orders;
```

그리고 `Orders`에 `Customer`에 없는 `custid`가 들어 있으면 외래키를 다시 추가할 때 실패합니다. 확인 쿼리는 이겁니다.

```sql
SELECT DISTINCT o.custid
FROM Orders o
LEFT JOIN Customer c ON o.custid = c.custid
WHERE c.custid IS NULL;
```

아무 결과도 안 나오면 괜찮습니다.

---

## 결론

현재 문제는 `custid`가 기본키라서가 아니라, **다른 테이블에서 외래키로 참조 중이기 때문에 컬럼 변경이 막힌 것**입니다.

이 순서로 처리하면 됩니다.

```sql
ALTER TABLE Orders DROP FOREIGN KEY orders_ibfk_1;

ALTER TABLE Customer MODIFY custid INT NOT NULL AUTO_INCREMENT;

ALTER TABLE Orders
ADD CONSTRAINT orders_ibfk_1
FOREIGN KEY (custid) REFERENCES Customer(custid);
```

그 후에는 PHP에서 `custid` 없이 회원을 추가할 수 있습니다.

---

### ❓ 질문 (User)
12:08:13	alter table customer MODIFY custid int not null AUTO_INCREMENT	Error Code: 1833. Cannot change column 'custid': used in a foreign key constraint 'orders_ibfk_1' of table 'bookstore.orders'	0.016 sec
