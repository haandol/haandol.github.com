---
layout: post
title: MSK(Managed Streaming for Kafka) + 람다(Lambda) 써보기
excerpt: MSK(Managed Streaming for Kafka) Lambda tutorial
author: haandol
email: ldg55d@gmail.com
tags: aws msk kafka lambda tutorial
publish: true
---

## TL;DR

코드는 여기[^1].

> MSK 와 람다통신에는 NAT Gateway 가 필요하다. NAT Gateway 를 쓰려면 MSK가 반드시 Private Subnet 에 배포되어야 한다.[^2]
> NAT Gateway 없이 MSK 람다 이벤트 소스를 만들면 `PROBLEM: Connection error, Please check your event source connection configuration.` 에러를 만나게 된다.

## 시작하며

며칠전 MSK 가 Lambda 에서 이벤트 소스로 사용할 수 있는 기능이 GA 가 되어서 테스트 해보려고 했는데,
스트리밍 서비스를 쓸일이 없어서 Kafka 를 처음 써보는데 생각보다 귀찮은 내용들이 많았다.

여튼 람다와 MSK 를 연결해서 사용하려면 어떻게 하는지 간단한 예제로 살펴보자.

## 아키텍쳐

코드[^1] 를 CDK 를 이용하여 provision 하면 아래와 같은 아키텍쳐가 개인 AWS 계정에 프로비젼 된다.

![](/assets/img/2020/0816/architecture.png)

일반적으로 클릭스트림을 저장하는데 사용하기 때문에 비슷한 느낌으로 최소한의 구성으로 만들어봤다. 

1. API Gateway 를 통해 POST 요청을 하면 
2. Producer 람다가 호출되어 카프카에 요청 내용이 저장되고,
3. 배치사이즈 100개가 넘거나 버퍼가 6Mb 이상 차면 컨슈머가 호출되어,
4. Cloudwatch 에 이벤트 내용을 기록한다.

## 설치방법

아직 새로운 기능이라 MSK와 람다를 연결하는 작업이 CDK 만으로는 처리할 수 없다. (조만간 되겠지...)

코드의 README.md 에 다 나와있지만 큰 순서만 정리하면,

1. CDK 를 이용하여 프로비전을 해서 인프라를 설치해주고,
2. MSK 의 *client information* 을 클릭해서 bootstrap 주소를 업데이트해서 다시 deploy 를 한번 해준다.
3. 람다에 가서 수동으로 MSK 이벤트 소스를 등록해준다.

## 테스트

API Gateway 에는 2개의 API가 있다.

1. `POST /` - body 를 전달하여 Kafka 에 데이터로 쌓는다.
2. `POST /topic` - 토픽을 생성한다.

![](/assets/img/2020/0816/apigw.png)

설정을 수정하면 토픽 생성을 자동으로 할 수 있지만, 여기서는 수동으로 생성하고 해당 토픽에 데이터를 보낸다.

### Bootstrap 엔드포인트 설정

1. MSK 서비스 페이지에서 간다.

![](/assets/img/2020/0816/msk-cluster.png)

2. *View client information* 버튼을 클릭해서 *Bootstrap servers* 주소를 복사한다.

![](/assets/img/2020/0816/msk-client-info.png)

3. 해당 주소를 `lib/interfaces/constant.ts` 의 *MskBootstrapServers* 변수에 복사해준다.

```javascript
export const MskBootstrapServers = 'b-2.mskexamplealphacluste.pnrfbb.c12.kafka.us-east-1.amazonaws.com:9094,b-1.mskexamplealphacluste.pnrfbb.c12.kafka.us-east-1.amazonaws.com:9094';
```

4. cdk deploy 로 수정된 코드를 배포해준다.

### 이벤트 소스 설정

1. 람다 서비스 페이지에서 Consumer 함수를 선택한다.

![](/assets/img/2020/0816/lambda-consumer.png)

2. *Add Trigger* 를 클릭해서 MSK 이벤트 소스를 등록한다. 토픽명은 `mytopic` 으로 한다.

![](/assets/img/2020/0816/lambda-msk-event-source.png)

### 토픽 생성

본 글에서는 Httpie[^2] 를 이용하여 요청을 보내며, Postman 등을 이용해도 관계없다.

`mytopic` 이라는 이름으로 카프카 토픽을 생성해준다.

```bash
$ http post https://z2bc7anee7.execute-api.us-east-1.amazonaws.com/dev/topic name=mytopic
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: false
Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent
Access-Control-Allow-Methods: OPTIONS,POST,GET
Access-Control-Allow-Origin: *
Connection: keep-alive
Content-Length: 4
Content-Type: application/json
Date: Mon, 17 Aug 2020 15:39:10 GMT
X-Amzn-Trace-Id: Root=1-5f3aa49c-2fa1d3e57e4977bf96267892;Sampled=0
x-amz-apigw-id: Ra6oeH89oAMF_gg=
x-amzn-RequestId: 85433fef-d309-4d78-850c-df78f89a0b64

"ok"
```

### 데이터 보내기

생성된 토픽에 스트링 데이터를 넣어준다. 해당 API 는 동일한 데이터를 100개 반복해서 카프카에 보낸다.

```bash
$ http post https://z2bc7anee7.execute-api.us-eastt-1.amazonaws.com/dev topic=mytopic data="Hello MSK"
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: false
Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent
Access-Control-Allow-Methods: OPTIONS,POST,GET
Access-Control-Allow-Origin: *
Connection: keep-alive
Content-Length: 4
Content-Type: application/json
Date: Mon, 17 Aug 2020 15:40:14 GMT
X-Amzn-Trace-Id: Root=1-5f3aa4dd-00933f9a2471b5680fe69ff6;Sampled=0
x-amz-apigw-id: Ra6ykEo6IAMF6uQ=
x-amzn-RequestId: ac315665-2b02-422c-bc87-0840c89954dc

"ok"
```

### 데이터 확인

클라우드 워치에 가면 전송한 이벤트가 그대로 출력되어 있는 것을 확인할 수 있다.

## 마치며

~~AWS 최신 서비스는 GA 라고 해서 발표해도, 최소 6개월은 지나고 쓰는 것이 안정적인 것 같다.~~

매뉴얼과 관련 글 들을 잘 읽어보자..

----

[^1]: [haandol/msk-lambda-example](https://github.com/haandol/msk-lambda-example)
[^2]: [Using Amazon MSK as an event source for AWS Lambda](https://aws.amazon.com/jp/blogs/compute/using-amazon-msk-as-an-event-source-for-aws-lambda/)