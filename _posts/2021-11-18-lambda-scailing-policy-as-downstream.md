---
layout: post
title: 람다가 다운스트림일때 동시성 스케일링 정책
excerpt: How Lambda scales when it is a downstream
author: vincent
email: ldg55d@gmail.com
tags: aws lambda scale concurrency downstream
publish: true
---

## TL;DR

서비스별로 스케일링 하는 방식이 다 다르다.

## 시작하며

`SQS 에 데이터가 엄청 많을때 람다가 얼마나 빨리 데이터를 처리할 수 있을까?`

일하면서 자주 듣는 질문중의 하나다.

람다도 AWS 입장에서는 마이크로 서비스중의 하나일 뿐이기 때문에,

람다를 어떤방식으로 호출할지, 어떤 기준으로 스케일링할지는 람다와 통합된 다른 서비스들에서 결정하게 된다.

따라서 람다와 S3, SQS, SNS 등을 연결할때 람다가 얼마나 많은 이벤트를 처리할 수 있는지는 람다 자체가 아니라 연결된 서비스의 문서를 확인해야한다.

대부분 람다문서[^1]에 잘 나와있지만, 본 글에서는 주요서비스들에 대해서 어떻게 스케일링을 하는지 정리해본다.

## AWS Lambda 

먼저 람다 자체의 기본적인 내용만 간단히 짚고 실제 다른 서비스들과의 연결을 살펴보자.

아래 내용을 깊게 들어가면 본 글의 범위를 벗어나기 때문에 관계된 내용만 간단히 다룬다.

### 호출방식

람다를 호출하는 방식은 2가지가 있다.[^2]

* 동기호출(Synchronous Invocation)
* 비동기호출(Asynchronous Invocation)

각 호출방식을 알아야 하는 이유는 람다는 호출 방식에 따라 에러처리가 다르기 때문이다.

예를 들어, 동기호출은 로직에러에 대해서 재시도를 하지 않지만 비동기호출의 경우 2번의 재시도를 자동으로 해준다.

본 글에서는 호출방식에 따른 특징을 상세히 다루지는 않고, 각 서비스를 분류할 때 기준으로만 사용한다.

### 동시성

람다는 API Gateway 와 마찬가지로 토큰버킷 알고리즘을 통해서 요청수를 제한하고 있다.

문서[^3]에 따르면 람다는 이니셜버스트(initial burst) 이후 분당 500씩 동시성이 늘어난다. (분당 filling rate가 500인 토큰버킷[^4]이라고 생각하면 된다.)

버스트 리밋(burst limit)은 어카운트 내의 모든 함수호출에 대한 동시성을 기준으로 계산하기 때문에, 어카운트 내에서 람다를 쓰는 모든 유즈케이스들도 고려해야 한다.

즉, 다른 서비스들에서 람다를 호출할 때 버스트를 고려해야 최대 호출이 가능한 동시성을 정확히 계산할 수 있다. (물론 버스트리밋도 soft limit 이므로 요청을 통해 늘릴 수 있다.)

## 주요 서비스들이 람다를 스케일링 하는 방법

### 비동기 호출

* 비동기 호출은 람다서비스 자체의 동시성 제한을 제외하면 스케일링에 제한은 없다.
  * push 방식으로 메시지큐에 들어오면 바로 바로 호출한다.
  * 따라서 에러 핸들링 방식을 잘 알고 있어야 한다.
* 로직 에러의 경우 2회 재시도 한다. 
* 50x(시스템 에러) 또는 429(throttling) 의 경우에 1초부터 5분까지의 인터벌을 점점 올리면서 최대 6시간동안 재시도하고 그래도 처리가 안되면 이벤트를 버린다.
  * 단, 서비스에 DLQ 설정이 있는 경우 위에 기재한 내용이 아닌 DLQ 설정을 따른다.

#### EventBridge

https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents.html

* 이벤트 브릿지로 들어오는 이벤트는 이벤트소스에 따라 유실될수도 있다. 이것은 이벤트 브릿지 특성이니 링크[^6]를 참조하자.

#### SNS

https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html

* SNS 는 많이 쓰니깐 혹시나해서 섹션을 넣어둔다.
* 하지만 글에서 다루지 않은 다른 비동기 호출들과 마찬가지로 이벤트당 람다함수가 호출된다. (비동기 호출의 기본동작방식)
* 기본은 전송 실패시 즉시 3번 재시도, pre - backoff - post 로 나눠서 23일간 10만번넘게 재시도후 DLQ 전송 또는 폐기한다.[^7]

#### S3

https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html

* S3 도 많이 쓰니깐 혹시나해서 섹션을 넣어둔다.
* 다른 비동기 호출 서비스들과 동일하다.

### 동기 호출

* 람다에 destination 설정해도 반영이 안된다.
* 로직 에러로 실패시 재시도가 없이 종료된다.
* 50x(시스템 에러)나 429(throttling) 의 경우에는 2회 재시도한다.

#### SQS

https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html#events-sqs-scaling

* 스탠다드는 한번에 5개까지 배치를 읽는다. 즉, 메시지가 50개이상 쌓여있으면 한번에 동시성이 5까지 늘어난다.
* 그리고 분당 최대 60개까지 람다 인스턴스가 늘어난다.
  * 계산하면 대략 12초마다 한번씩 5개의 인스턴스가 늘어난다.
* FIFO 큐는 메시지그룹 개수와 1:1 비율로 람다 함수를 실행한다.(메시지그룹 개수는 quota 가 없다)[^5]
  

#### Kinesis Streams

https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html

* 키네시스 스트림의 컨슈머를 설정할 때 각각 standard 모드와 enhanced fan-out(EFO) 모드로 설정할 수 있다.
  * standard 는 HTTP, EFO 는 HTTP/2 를 사용한다.
  * 따라서 각각 poll, push 방식으로 호출된다.
* 각 샤드는 1초에 최대 5개의 읽기 트랜잭션(GetRecords API Invocation)을 처리 할 수 있다.
  * 즉, 한 샤드에 최대 5개의 람다 함수까지 붙을 수 있다.
  * 이 때, 5개의 트랜잭션이 2MB(샤드 상한) 씩 레코드를 가져가면 (10MB) 다음 5초동안 GetRecords 가 블록된다.
* 람다로 컨슈머를 설정하면 샤드마다 람다가 1개씩 할당되고, 각 람다는 초당 1회 샤드를 폴링한다.
* 이벤트 소스 매핑의 ParallelizationFactor 를 이용해서 10까지 설정 가능하다.
  * 람다 서비스가 샤드에서 데이터를 폴링하고 람다 함수를 호출하는 과정에서 키별로 PF가 적용되므로 5이상 설정가능하다.
  * 즉, 샤드가 100개고 ParallelizationFactor 를 2로 설정해두면 200개까지 동시성이 늘어난다. (메시지의 IterationAge 가 낮아진다.)

#### DynamoDB Streams 

https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html

* 람다는 초당 네번 샤드를 폴링한다.
* 한 스트림에 2개의 람다 함수까지 붙을 수 있다. (컨슈머가 최대 2개)
* DDB 는 샤드를 수동으로 늘릴 수 없다. 데이터 볼륨과 IO 를 기반으로 DDB 가 자동으로 조절해준다. (그래서 로드테스트 등으로 강제로 늘리거나 한다.)
* 이벤트 소스 매핑의 ParallelizationFactor(PF) 를 이용해서 10까지 설정 가능하다. *하지만 on-demand 모드일때 최대 2이상은 권장하지 않는다.*
  * on-demand 모드에서 트래픽이 2배로 몰리면 샤드개수가 2배로 늘어날 수 있는데, 이때 PF 가 10이면 대략 현재의 **20배의 람다함수**가 실행된다.

#### Managed Service Kafka(MSK)

https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html

* 이벤트 소스 설정상 람다와 토픽이 1:1 매핑 된다.
* 스케일링을 설정할 수 있는 방법이 따로 없다.
* 매 15분마다 람다서비스가 offset-lag 을 판단해서, 폴링 타이밍을 조절하거나 토픽의 컨슈머 개수를 늘리거나 줄인다.

#### AmazonMQ

https://docs.aws.amazon.com/lambda/latest/dg/with-mq.html

* 스케일링에 대해 아무런 정보가 없다.
* 대략 MSK랑 비슷할 것으로 생각된다. (내부에 정의된 폴리시에 따라 자동으로 스케일링을 처리해주는 방식)

## 마치며

잘못된 정보가 있다면 댓글로..

----

[^1]: [Using AWS Lambda with other services](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html)
[^2]: [Invoking AWS Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html)
[^3]: [Lambda function scaling](https://docs.aws.amazon.com/lambda/latest/dg/invocation-scaling.html)
[^4]: [Rate Limiting system design | TOKEN BUCKET, Leaky Bucket, Sliding Logs](https://www.youtube.com/watch?v=mhUQe4BKZXs)
[^5]: [New for AWS Lambda – SQS FIFO as an event source](https://aws.amazon.com/ko/blogs/compute/new-for-aws-lambda-sqs-fifo-as-an-event-source/)
[^6]: [Events from AWS services](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event.html)
[^7]: [Amazon SNS message delivery retries](https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html)