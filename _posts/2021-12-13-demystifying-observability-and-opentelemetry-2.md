---
layout: post
title: 쉽게 설명한 옵저버빌리티와 오픈텔레메트리 - 2/2
excerpt: Demystifying Observability and Opentelemtry, 2 of 2
author: haandol
email: ldg55d@gmail.com
tags: observability opentelemetry otel lightstep xray aws
publish: true
---

## TL;DR

`오픈텔레메트리(OpenTelemetry) = 오픈트레이싱(OpenTracing) + 오픈컨세서스(OpenConsesus)`

오픈트레이싱 = Tracing, 오픈컨세서스 = Tracing + Metrics. 로깅 = 알아서 structured log 를 쌓아야 한다.

오픈텔레메트리(OpenTelemetry) 를 통해서 옵저버빌리티에 필요한 데이터(Tracing, Metrics, Logging)를 쉽게 쌓을 수 있다.

## 시작하며

지난 옵저버빌리티 글에 이어 오픈텔레메트리[^1]에 대해 간단히 살펴보자. 

## 오픈텔레메트리란?

옵저버빌리티의 3가지 핵심 컴포넌트(Pillars) 는 

- 메트릭(Metics)
- 로그(Logs)
- 트레이싱(Traces)

이라고 했다.

기존에는 오픈트레이싱(OpenTracing) 과 오픈컨세서스(OpenConsesus) 가 있었고, 오픈트레이싱은 이름 그대로 트레이싱 부분을 커버하고 있는 표준이고, 오픈컨세서스는 트레이싱과 메트릭을 커버하는 표준이다.

오픈텔레메트리는 `오픈트레이싱 + 오픈컨세서스 + 로그에 대한 표준` 이라고 이해하면 된다. (기존에 로그에 대한 표준이 없었던 것은, 텍스트를 쌓는 작업이므로 표준이 필요 없을 정도로 단순하며, 대부분의 경우 비슷한 프로세스를 거쳐 로그를 쌓고 조회하고 있었기 때문이라고 생각하고 있다.)

아래의 그림을 보면 좀 더 쉽게 이해할 수 있을 것이다.

<img src="/assets/img/2021/1213/otel-before.png" />

기존에는 옵저버빌리티의 핵심 컴포넌트들을 추적하기 위해서 컴포넌트별로 쌓고 해당 서비스로 내보냈어야 했다. 라이브러리에 따라 비즈니스 로직과 인프라가 너무 밀접하게 얽힌다는 것도 큰 문제이다.

오픈텔레메트리를 이용하면 단일한 라이브러리와 단일한 방법을 통해 옵저버빌리티를 확보할 수 있다. 또한 서비스 코드는 개발자가 어떤 분석도구를 쓰느냐를 알필요가 없어져서 비즈니스 로직과 인프라를 최대한 분리할 수 있다.

(비즈니스로직과 인프라관련된 내용을 분리한다는 측면에서 서비스 매쉬와 방향성이 같고, 앞으로 많은 툴들이 이러한 방향성으로 발전할 것이라고 예상해볼 수 있다.)

종합해보면 오픈텔레메트리는 옵저버빌리티를 쉽게 확보할 수 있도록 도와주는 툴이라고 볼 수 있다.

## 오픈텔레메트리 동작방식

본 글에서는 오픈텔레메트리의 기본적인 구성과 동작방식에 대해서만 간단히 소개해본다. (오픈텔레메트리 자체가 사용이 별로 어렵지 않기 때문..)

<img src="https://raw.github.com/open-telemetry/opentelemetry.io/main/iconography/Reference_Architecture.svg" />

위의 그림이 오픈텔레메트리의 동작방식을 가장 직관적으로 설명한 그림이라고 할 수 있다. (역시 공식문서)

좌우측의 베이지색 박스가 노드이다. ec2 node, k8s pod, ecs task 또는 람다 샌드박스 라고 볼 수 있다.

우리가 작성한 어플리케이션에 오픈텔레메트리 라이브러리를 통해 트레이싱, 메트릭, 로그를 적절히 쌓으면, 라이브러리는 해당 내용을 컬렉터(Collector)로 전송한다.

컬렉터는 그림처럼 에이전트(agent) 와 서비스(service) 로 나눠져있고, 에이전트는 보통 사이드카나 데몬으로 떠서 노드의 처리를 오픈텔레메트리 서비스나 커스텀 서비스로 전달하는 역할을 한다.

<img src="https://images.ctfassets.net/8057oncvx5dp/1bE0ZiTDAhmp75SJTKP3cA/7d99ef9fa1f8a243e7582e3afb3bf020/diagram.png" />

에이전트가 서비스와 주고받을때는 OTLP 라는 프로토콜을 써서 주고 받게 되어 있으며 [^1]의 위의 그림에는 안나와있지만, 로그데이터도 메트릭이나 트레이스와 동일한 방식으로 쌓을 수 있다.

컬렉터를 좀 더 확대해보면 아래와 같이 구성되어 있다.

<img src="https://aws1.discourse-cdn.com/elastic/original/3X/6/1/61b274a7d1392f1a928c43c063140a4e5c736803.png" />

컬렉터 에이전트가 exporter 를 통해 내보내면 컬렉터 서비스가 receiver 를 통해 받고 다시 export 할 수 있다. 그림에는 없지만 컬렉터들은 내부에서 processor 를 통해 tranformation 이나 batch 같은 추가적인 처리를 할 수 있다.

## AWS와 오픈텔레메트리

오픈텔레메트리는 온프레미스 환경이나 하이브리드 환경에서 마이크로 서비스들을 직접 운영하는 경우에는 필수적이라고 볼 수 있다.

하지만 클라우드는 자체적인 옵저버빌리티 툴들을 이미 제공하고 있다. 특히 AWS 는 클라우드워치와 x-ray 를 통해 모든 옵저버빌리티 편의를 제공하고 있다.

하지만 AWS 도 완벽하지는 않은데, 아직 x-ray 를 통해 트레이스Id 전달하는 부분들이 모든 서비스들에 다 지원되는 것이 아니며, 특히 람다의 경우에는 context 가 immutable 하기 때문에 `sqs -> lambda` 와 같은 워크로드에서는 람다가 트레이스Id 를 넘겨받은 것으로 사용하지 못하고 새로 만들어버린다. (이것을 우회하는 shims 들이 있지만 파이썬은 또 잘 안됨..)

## Observability 를 적용하는 방법

## OpenTelemetry 예제

코드는 여기[^2] 에 있다.

요새 한창 잘 나가고 있는 LightStep[^3] 이라는 서비스를 이용해서, 람다의 데이터를 오픈텔레메트리를 통해 트레이싱하는 예제이다.
 
(조회수가 늘어나면 해당 내용을 따로 글로 써보는 쪽으로 하겠다.)

## 마치며

좀 날림으로 썼지만(컬렉터 쪽이라던가..) 마찬가지로 조회수가 늘어나면 보완하는 것으로..

----

[^1]: [OpenTelemetry](https://opentelemetry.io)
[^2]: [AWS Lambda OpenTelemetry Example](https://github.com/haandol/aws-lambda-otel-example)
[^3]: [LightStep](https://lightstep.com/)