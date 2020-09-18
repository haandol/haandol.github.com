---
layout: post
title: Amazon API Gateway 에서 웹소켓 채팅방 만들기
excerpt: Amazon API Gateway websocket chatroom tutorial
author: vincent
email: ldg55d@gmail.com
tags: aws api-gateway websocket cdk chatroom tutorial
publish: true
---

## TL;DR

코드는 여기[^1]

## 시작하며

Amazon API Gateway 에는 웹소켓기능이 있는데 CDK 로 된 예제가 찾기 힘들어서, 간단한 채팅방 예제를 만들었다.

웹소켓은 API Gateway 와 연결하고 실제 요청은 람다가 처리하게 되어 있기 때문에 실제 처리는 Stateless 하게 해야하며

만약 Sticky Session 이 필요하다면, 본 예제가 아니라 HTTP Integration 을 이용해서 구현해야 한다.

> CDK 로 뭔가 만들기 전에 콘솔로 먼저 만들어보는 것을 항상 추천한다.

## 설치

설치방법은 코드[^1]의 README.md 에 나와있다.

콘솔로 한번 API Gateway Websocket API 를 만들어봤다면 기능이 매우 단순하다는 사실을 알 수 있다.

따라서 본 글에서 웹소켓 API 자체를 설명하지는 않고 코드 사용위주로 설명하려고 한다.

## 코드설명

해당 코드 예제는 로컬캐시를 이용한 채팅방을 구현했다.

모든 메시지는 Route 기준으로 처리된다. 기본 Route는 $connect, $disconnect, $default 가 있다.

내가 지정한 Route 에 해당하는 메시지가 아니라면 $default Route 가 메시지를 처리한다.

본 예제에서는 *$request.body.action* 을 기준으로 *join*, *send* 가 아닌 모든 메시지는 $default Route 가 처리한다.

코드 자체가 짧기 때문에 상세한 설명은 하지 않고, 전체 구조를 설명하면 

1. 사용자가 *join* 액션을 통해서 채팅방에 입장하고 
2. *send* 액션을 통해서 메시지를 방에 전송한다.

Redis 등의 외부 스토리지를 사용하지 않으려고 하다보니, join_and_send 라는 냄새나는 함수가 나왔지만 의도를 전달하기에는 이 방법이 제일 좋아보인다.

## 사용

1. 터미널을 하나 열고 (사용자 A) wscat 을 이용하여 웹소켓을 연다. 위에 설명한 대로 invalid 한 메시지는 $default 에 의해 echo 로 동작한다.

```bash
$ wscat -c wss://xyz.execute-api.ap-northeast-2.amazonaws.com/alpha 
> hi there
< hi there
```

2. join action 을 통해 방에 접속한다.

```bash
> {"action": "join", "room": "room1"}
< S_5YUerFoE0CJng= has joined to Room room1
> {"action": "join", "room": "room1"}
< You have already joined to room1.
```

3. send action 을 통해 메시지를 전송해본다.

```bash
> {"action": "send", "room": "room1", "msg": "this is AWS"}
< [S_5YUerFoE0CJng=]: this is AW
```

4. 새로운 터미널을 열고 웹소켓에 접속한다. (사용자 B)

```bash
$ wscat -c wss://xyz.execute-api.ap-northeast-2.amazonaws.com/alpha
```

5. join action 을 통해 A 사용자가 접속해 있는 room1 방에 접속한다.

```bash
> {"action": "join", "room": "room1"}
< S_579fEDoE0CJng= has joined to Room room1
```

6. send action 을 통해 메시지를 보내고, 두 터미널 모두에서 메시지가 출력되는지 확인한다.

```
> {"action": "send", "room": "room1", "msg": "this is AWS User B"}
< [S_7SxeJSIE0CIRQ=]: this is AWS User B
```

## 마치며

웹소켓은 최대연결 2시간에 idle 연결이 10분인데, hard limit 이라 조정할 수 없다.

IoT Core 의 MQTT 를 이용하면 24 시간 까지 연결을 유지할 수 있으므로 좀 더 긴 연결을 유지해야한다면 MQTT 도 고려해볼만 하다.
(어차피 재연결 처리해야하는 건 같지만)

----

[^1]: [API Gateway Websocket](https://github.com/haandol/api-gateway-websocket-example)