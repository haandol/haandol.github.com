---
layout: post
title: 개인 프로젝트 시작을 위한 가이드라인
excerpt: Simple guideline to start your own pet project
author: vincent
email: ldg55d@gmail.com
tags: pet-project guideline best-practice
publish: true
---

## TL;DR

- **최종 제품에 대한 PR 작성**
- **사용자 스토리 작성**
- 이벤트 스토밍
- 아키텍쳐 다이어그램 작성
- **주요 페이지 목업 그려보기**
- API Spec 및 테이블 스키마 작성
- 개발 시작

## 시작하며

모든 프로젝트는 `내가 생각한 문제를 내 나름의 방식으로 해결하고 그것을 다른 사람들에게 인정받으려고 하는 과정`이다.

내가 생각한 문제가 잘못되었거나, 내 방식이 잘못되었거나, 문제 또는 해결방법을 다른 사람들이 인정해주지 않으면(내 솔루션을 쓰지 않으면) 결국 아무런 의미 없는 노력이 될 뿐이다.

정리하면 문제의 정의, 해결방법의 정의가 잘못된 순간 뒤쪽의 모든 노력은 무가치한 노동의 시간으로 변할 가능성이 높다.

그래서 비즈니스에 조금이라도 관심이 있는 개발자들은, 실제로 가장 큰 노력이 들어가는 `구현`을 최대한 뒤로 미루고 앞쪽에서 `고민`을 하는데 시간을 최대한 쓰는 것을 쉽게 볼 수 있다.

아마존에서도 이렇게 중요한 고민을 먼저하고 구현을 미루는 마인드셋을 매우 장려하고 있고, Working Backward 라는 매커니즘으로 만들어서 사용하고 있다.(아마존의 매커니즘화 하는 프로세스도 할 말이 좀 있지만, 기본적인 내용은 이 글[^3] 정도면 충분할 것 같다.)

본 글에서는 이 마인드셋 위에서, 프로젝트를 진행하는 구체적인 순서를 살펴보려고 한다.

개인적으로 제안하는 순서는 아래와 같다. 각 항목은 경우에 따라 생략가능 하지만, 생략 불가능한 항목은 **굵게** 처리했다.

- **최종 제품에 대한 PR 작성**
- **사용자 스토리 작성**
- 이벤트 스토밍
- 아키텍쳐 다이어그램 작성
- **주요 페이지 목업 그려보기**
- API Spec 및 테이블 스키마 작성
- 개발 시작

아래에는 핵심적인 순서들 몇개에 대해서 살펴보겠다.

(모든 순서에 대해서 설명하기에는 가성비가 안나오기 때문에, 페이지뷰가 일정 수준 이상 되면 하나씩 추가해보겠다.)

## PR(PressRelease) 작성

모든 프로젝트의 시작은 Problem Space 를 정의하고, 이것을 Solution Space 로 변환해 나가는 과정으로 시작한다.

일반적으로 Problem Space 는 풀고 싶은 문제와 해당 문제를 해결하기 위한 현실적인 문제점(리소스 등)을 포함하고 있다.

그리고 그 문제를 해결하기 위한 구체적인 접근 방법과 현재 상태를 고려한 내용들이 Solution Space 에 표현된다.

두 Space 들의 공통점은 최대한 추상화된 내용을 담고 있다는 점이다.

아마존에서는 Solution Space 를 PR/FAQ[^2] 로 표현하곤 한다.

PR/FAQ 는 PR 과 FAQ 로 이뤄져있다.

PressRelease 또는 PR 은 내가 만든 최종 제품이 공개되었을때 시장이나 도메인에 미칠 임팩트를 미리 고민하게 해준다.
FAQ는 제품의 사용자들이 궁금해 할만한 내용을 미리 고민하게 해준다.

PR 에는 해결하려는 문제와, 문제가 해결되어서 얻게되는 결과를 객관적인 시선으로 기록하게 된다.

꼭 PR을 이름처럼 보도자료형태로 작성할 필요는 없다. 해당 솔루션을 한번도 접해보지 않은 사람에게 설명한다는 느낌으로, 평문으로 작성하는 것으로 충분하다.

많은 아이디어들이 내 머리속에서는 노벨상감이지만, 주변사람에게 설명하기 위해 입밖으로 나왔을땐 지극히 평범해지는 경우가 많다. 대부분의 경우 아이디어 자체는 평범한데 본인이 객관적인 관점으로 보지 못해서이다.

PR 을 작성해서 스스로 읽어보는 것 만으로도 객관적으로 문제와 해결방법을 볼 수 있는 계기를 제공해주고, 불필요한 이후의 노력을 막아줄 수 있다.

## 사용자 스토리

사용자 스토리의 목적은 사용자가 서비스를 사용하는 시나리오를 미리 생각해보는 것이다.

또한 프로젝트를 스토리 단위로 관리하면 진행상황을 사용자 테스트 가능한(feasible) 기능 단위로 추적할 수도 있다.

뿐만 아니라 사용자 스토리를 작성해두면 이벤트 스토밍이나, 아키텍쳐 다이어그램 심지어 시큐리티에 대한 점검을 할때도 매우 유용하게 사용할 수 있다.

스토리 템플릿에 대해서는 gherkin 문법을 쓰는 것을 추천하고, 템플릿의 상세 내용은 이 글[^1] 을 참고해보자.

종종 사용자 스토리를 cucumber 같은 도구로 테스트하는 것을 원하는 경우도 있겠지만 대부분의 경우 가성비가 좋지 않다.

경험상 테스트 피라미드를 잘 쌓아두는 것만으로도 충분한 경우가 많다.

## 목업 (Materialized View)

이 목업(Mockup) 에서 가장 중요한 것은 화면에 표시될 데이터를 결정하는 과정이라는 점이다.

사용자가 이 화면에서 어떤 형태의 데이터가 필요한지, 어떠한 인터랙션이 필요한지를 예상할 수 있고,

이를 바탕으로 API 의 Spec, 동기/비동기 로 동작할 내용을 결정할 수 있다. 

특히 NoSQL 기반으로 데이터를 다룰 예정이라면 테이블간 Join 이 불가능 하므로 반드시 View 를 먼저 예상해서 그려둬야 불필요한 테이블생성(예, CQRS 를 통한 Materialized View)을 피할 수 있다.

## 마치며

개인적으로는 본인이 사용자가 아닌 어떠한 사이드 프로젝트도 진행하지 않는 것을 추천한다.

사용자에게 주는 가치와 불편함 등을 직접 얻고 해결하는 것이 프로젝트 초기에 엄청나게 중요하기 때문이다.

----

[^1]: [올바른 유저 스토리 작성을 위한 엔지니어링 가이드](https://wholeman.dev/posts/guide-to-writing-correct-user-stories/)
[^2]: [Amazon PR-FAQ Approach](https://medium.com/intrico-io/strategy-tool-amazons-pr-faq-72b3e49aa167)
[^3]: [Good intentions don't work; mechanisms do.](https://www.linkedin.com/pulse/good-intentions-dont-work-mechanisms-do-jv-roig/)