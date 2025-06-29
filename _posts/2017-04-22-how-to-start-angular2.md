---
layout: post
title: 내가 Angular 를 선택한 이유
excerpt: Reactive 처음 시작한 서버개발자
author: haandol
email: ldg55d@gmail.com
tags: angularjs start-blog machine-learning progmatic
publish: true
---

## TL;DR

Typescript 쓰려면 그냥 Angular2 쓰세요. 속편합니다.

## 난 왜 Angular2 를 쓰기로 했는가

최근 리액티브한 프론트 개발을 시작하면
React(Redux), Angular2, Vue 셋 중 하나를 선택하는데 고민을 하게 된다.

서버 렌더링과 클라이언트 렌더링을 적절히 써야하는 일이 많기 때문에
서버렌더링과 거의 무관한 Vue 는 별로 고려하지 않았다.

각 프레임워크의 특징은 많은 글들이 있으니 알아서 판단하면 되고
본 글에서는 개인적으로 왜 Angular 를 선택했는지만 간략히 적어본다.

## Typescript

나는 테스팅이 매우 중요하다고 생각하는 편이다.
특히 타입체킹은 코드 작성 뿐아니라 테스팅에도 큰 안정성을 안겨다 주기 때문에
JS 에도 타입체킹을 써야겠다고 생각했다.

JS 에서 타입체킹을 위한 툴은 크게 Flow 와 Typescript 가 있다.

내가 단순 툴인 Flow 보다 언어에 가까운 Typescript 를 선택한 이유는
구글에서도 인정한 툴[^2]이며 MS 에서 안정적으로 관리하고 있고
coffee 같은 새로운 문법이 아니라 ES 표준을 지향하는 슈퍼셋 언어이기 때문이다.

Angular2 는 Typescript 를 기본으로 채택하고 있고
Vue 와 React 는 Facebook 에서 만든 Flow 라는 툴로 타입체킹을 하고 있다.

이 말은 Vue 와 React 에 빠진 기능들을 메꾸기 위한 서드파티 라이브러리들이
Typescript 를 적절히 지원하지 않을 가능성이 있으며 stable 하지 않은 버전일수록 더욱 그렇다.

또 Typescript + React + Redux 는 설정이 너무나 귀찮았다.

## 학습곡선

React 는 내가 기술들을 선택해서 조합한다는 것에 의미가 있다.
Angular 는 자주 사용되는 기능들이 내장되어서 빠르게 개발하는 데 의미가 있다.

나는 이 차이점 때문에 Angular 가 React 보다 더 이해가 잘되었다.

React 를 공부할 때 Babel, Webpack, Gulp 등의 메인 기능은 아니지만 
자주 사용되는 툴들이 나오면 해당 기술을 공부안하고 넘어가기가 매우 찝찝했다.

각각은 범용성을 가진 외부 패키지 이므로
내가 쓴 패키지가 내 프로젝트에 무슨 영향을 미치는지를 어느정도 파악하지 않고 그냥 넘어가는 것을
싫어하기 때문이다. (각 프로젝트가 앞으로도 잘 관리될지도 예상해 봐야하고)

그리고 툴 공부하는 시간이 React, Redux 공부하는 시간보다 더 오래 걸렸다..

반면 Angular 는 왠만큼 지식의 흐름에 빈 공간이 나와도
(component, injector 데코레이터가 어떻게 구현되는지 등) 넘어가게 되었다.

내장된 기능은 프레임워크에서 알아서 처리해줄 것이라는 기대가 있었기 때문이다.
(프레임워크에 내장된 기능 중 하나기 때문에 크게 바뀌거나 하지도 않을 거 같고)

이런 측면에서 나는 Angular 를 훨씬 빨리 공부할 수 있었다.

실제로 React+Redux+Typescript 는 3일 넘게 봐서 튜토리얼을 겨우 끝냈다. 그렇지만 지금 공부한 것으로 그럴듯 한 것을 만들 수 있을 거 같다는 느낌을 받기는 힘들었다.

반면 Angular 는 2일 만에 튜토리얼을 다 끝내고 간단한 투두리스트를 혼자 만들 수 있었다.
(RxJS 도 이 글[^5] 을 읽고 봤더니 굉장히 이해가 쉬웠다.)

## 속도

서버 언어로 Python 을 사용해온 입장에서 `언어의 속도는 생각만큼 중요하지 않다.` 라는 생각에 동의한다.[^4]

React 는 Angular 보다 1.5배쯤 빠르지만[^3] 저 프레임워크들은 서버가 아니라 클라이언트의 리소스를 쓴다.

요즘같은 리치 클라이언트 환경에서 저 정도 속도 차이는 Angular 를 통해 얻는 생산성 향상에 비해 미미한 수준이라고 생각했다.

## 코드구조

코드 모양은 취향문제라고 본다.

나는 React 의 JSX 보다는 Angular2 의 템플릿 모양이 더 맘에 들었다.
간단하게 html, css 파일을 컴포넌트와 분리시킬 수 있다는 점에서 더 그랬다.

코드 구조는 좀 다른 이야기인데 코드 구조는 커뮤니케이션과 연관되어 있기 때문이다.

예로, 내가 `RxJS가 옵저버(Observer) 패턴으로 stream 을 구성한 프레임워크다.` 라고 설명했다면
해당 패턴을 아는 사람에게 설명해야하는 부분이 엄청나게 줄어들며
서로 코드에 대해 이야기 할 때도 마찬가지이다.

React 는 구조가 자유롭기 때문에 많은 부분에 대해 설계를 해줘야 한다.
여러 사람이 작업할 때 특정한 구조가 나온 이유에 대한 설명이 항상 필요하다.
그러지 않으면 각 사람은 자기가 생각한 구조대로 만들 것이기 때문이다.

Angular 는 특정한 형태로 구조를 강제하는 부분이 많다.
다양한 사람이 만든 앱이라도 코드의 구조가 크게 달라지지 않을 것 같았다.
새로운 사람이 와도 코드구조에 대한 설명은 짧게만 언급해도 되고 컴포넌트 구조만 설명하면 된다.

# 정리하며

나에겐

내가 중요하게 생각하는 것들을
언어나 프레임워크도 중요하게 생각하는지 여부가 중요하다.
그 다음엔 개념이나 구조가 어렵지 않고 사용할 때 재미있는 지가 중요하다.

이런 성향인지라
인터넷에 돌아다니는 장단점 정리한 글 몇 개 읽어보고 결정하는 건 잘 안먹혔다.

이런저런 글을 읽어봐도 감이 안오면 그냥 튜토리얼을 해보자.

----

[^1]: [andrestaltz의 글](https://gist.github.com/staltz/868e7e9bc2a7b8c1f754)
[^2]: [ZDNET 기사](https://gist.github.com/staltz/868e7e9bc2a7b8c1f754)
[^3]: [Auth0 Benchmark](https://auth0.com/blog/more-benchmarks-virtual-dom-vs-angular-12-vs-mithril-js-vs-the-rest/)
[^4]: [Yes, Python is Slow, and I Don’t Care](https://hackernoon.com/yes-python-is-slow-and-i-dont-care-13763980b5a1)
[^5]: [The introduction to Reactive Programming you've been missing](https://gist.github.com/staltz/868e7e9bc2a7b8c1f754)
