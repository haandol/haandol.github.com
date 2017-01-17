---
layout: post
title: 거의 정렬된 경우 가장 빠른 알고리즘은?
excerpt: 데이터에 따라 적합한 정렬 알고리즘이 다르다는 사실
author: vincent
email: ldg55d@gmail.com
tags: sort, algorithm, dataset
publish: true
---

## TL;DR

거의 정렬된 경우 `Insertion` 정렬이 가장 빠르고 `Bubble`이 그 다음이다.

둘다 `O(n)`


# 시작하며

어느 회사 면접을 봤다.~~이름을 말할 수가 없다니~~

문제당 2분씩이고 순수 온라인으로만 진행되는데 전부 객관식 문제였다.

C, Ruby, Python, Javascript 으로 된 30 개의 문제에 객관식으로만 답하는 신기한 방식.

`객관식 문제만으로도 개발실력을 검증할 수 있겠구나` 싶어 느낀 바가 많다.

문제 범위도 굉장히 넓고 (알고리즘, 버그찾기, 포인터, 데이터 구조, 컴파일러/CPU 연산방식, 알고리즘 등) 생각보다 어려웠다.


여기 나온 문제중 하나가 `거의 정렬된 경우 가장 빠른 정렬 알고리즘은?` 이었는데

해답이 내 평소 생각과 달라서 간단히 노트해본다.


# 마치며

일단 나머지는 아예 생각하지 않았고 Quick 이냐 Heap 이냐로 고민했는데~~Heap 은 전처리가 되어 있으니깐(?!)~~ 둘다 순위에 한참 밀렸다.

TopTal [^1] 에 상세한 정렬 알고리즘들을 보면 각 알고리즘 별로 `Adaptive` 라는 특성이 있는데 특정 경우에 특수한 성질을 가지는 경우를 적어놨다.

예를 들어, `Merge` 정렬은 아예 Adaptive 하지 않은 알고리즘으로써 데이터의 형태에 관계없이 ~~안정적으로~~ `O(n*logn)` 을 보여준다.

거의 정렬된 경우에는 `Insertion`과 `Bubble` 둘다 `O(n)`으로 나와있지만 이마저도 정렬된 방식에 따라 속도가 다를 수 있다. ~~Insertion 이 좀더 빠름~~

완전 정렬된 상태에서 swap 형태로 섞인 경우에만 두 정렬 방식의 속도가 같지 않을까 생각해본다.

----

[^1]: [Sorting Algorithms Animations](https://www.toptal.com/developers/sorting-algorithms/)
