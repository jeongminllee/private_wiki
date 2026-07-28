---
type: Concept
title: "르베그 측도의 연속성"
description: "단조 증가·감소하는 가측집합 열에서 측도와 극한이 교환되는 조건"
resource: https://m.blog.naver.com/mykepzzang/222999304836
notion: https://app.notion.com/p/24b1a73cf20b831b9c07015bb9a3d362
tags: [reading, mathematics, measure-theory]
timestamp: 2026-07-24
status: summarized
---

# 한눈에 보기

르베그 측도의 가산가법성에서 따라오는 중요한 성질은 단조롭게 변하는 가측집합 열의 극한과 측도가 잘 맞는다는 것이다. 함수의 단조수렴정리와 비슷하게 집합의 근사를 다룰 때 반복해서 사용된다.

# 아래에서의 연속성

가측집합 열이

```text
A_1 subset A_2 subset A_3 subset ...
```

처럼 증가하면 다음이 성립한다.

```text
mu(union A_n) = lim mu(A_n)
```

각 단계에서 새로 추가되는 서로소 부분으로 집합을 분해한 뒤 측도의 가산가법성을 적용하면 된다.

# 위에서의 연속성

가측집합 열이

```text
A_1 superset A_2 superset A_3 superset ...
```

처럼 감소하고 `mu(A_1) < infinity`이면 다음이 성립한다.

```text
mu(intersection A_n) = lim mu(A_n)
```

첫 집합의 측도가 유한하다는 조건이 중요하다. 이 조건 없이 무한대에서 무한대를 빼는 식으로 증명하면 결론이 실패할 수 있다.

# 왜 중요한가

복잡한 집합을 단순한 집합의 증가·감소 열로 근사해 측도를 계산할 수 있다. 이후 가측함수의 수렴, 적분, 확률론의 사건 열을 다룰 때 기초 도구가 된다.

# 출처

- [르베그 측도 (2)](https://m.blog.naver.com/mykepzzang/222999304836)

