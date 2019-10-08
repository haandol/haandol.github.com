---
layout: post
title: Node.js 를 이용한 MQTT 튜토리얼
excerpt: MQTT tutorial using Node.js
author: vincent
email: ldg55d@gmail.com
tags: mqtt, nodejs, k8s, kubernetes, docker, tutorial, helm
publish: false
---

## TL;DR

MQTT 는 클라이언트가 직접 pub/sub 를 해야 하는 경우 효과적이다.

클러스터링을 지원하는 브로커를 찾는다면 EMQ 와 VerneMQ 가 있다.

## 시작하며

MQTT 는 페북에서 메신저에 쓰면서 좀 많이 알려졌고 요즘은 IoT 단말에서 양방향 메시지를 전달할 때 많이 쓰인다.

잘 알려진 메시지큐는 크게 AMQP, Kafka, MQTT 정도가 있고 각각 사용처가 명확한 편이다.

내가 자주 쓰던 MQ 는 AMQP 기반의 RabbitMQ 였다. AMQP 는 큐-익스체인지 를 이용하여 복잡한 구조로 메시지를 전달할 수 있기 때문에 MSA 에서 메시지 버스로 쓰기 좋아서 적극적으로 사용하고 있었다. 

하지만 몇차례의 개선을 통해 구조를 단순화 하면서 좀 더 경량 프로토콜인 MQTT 라는 녀석에 눈이 가길래 사용해보았다.

MQTT 자체에 대해서는 여기[^1]에서 잘 설명하고 있기 때문에 다루지 않는다.

본 글에서는 VernMQ + Node.js 를 이용하여 아주 단순한 형태의 fan-out 서비스를 구현해본다.

참고로, Kafka 는 AWS Kinesis Streams 와 비슷한 느낌으로 구조화된 토픽구조를 소화할 수 없어서 배제하였다.

## 브로커

MQTT 는 프로토콜이고 해당 프로토콜을 구현한 구현체인 브로커(메시지큐)를 통해 메시지를 주고 받을 수 있다. (AMQP 와 RabbitMQ 와의 관계처럼)

가장 유명한 브로커로는 mosquitto 를 들 수 있겠지만 고가용성 또는 부하분산 시스템을 위한 클러스터를 직접 구축해야 하므로 스케일을 고려해야 하는 상황에서는 부담이 된다.

클러스터를 기본으로 지원하는 브로커로는 EMQ, VerneMQ 등이 있는데, 개인적으로 조사해봤을땐 큰 차이가 없었다.

본 문서에서는 VerneMQ 가 초기설정부터 첫 사용까지의 과정이 더 쉬웠고, 주로 사용하는 k8s 에서 설치가 더 쉬워서 VerneMQ 를 사용하기로 했다.

## 시나리오

## 구현

## 환경설치

먼제 vernemq 를 도커로 띄운다.

```bash
$ docker run -e "DOCKER_VERNEMQ_ALLOW_ANONYMOUS=on" --name vernemq1 -d erlio/docker-vernemq
```

### 구조

### 코드설명

## 마치며

----

[^1]: [Facebook 메신저와 MQTT](https://d2.naver.com/helloworld/1846)