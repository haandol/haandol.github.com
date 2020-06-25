---
layout: post
title: AWS API Gateway + Lambda 로 A/B 테스트하기
excerpt: Use AWS API Gateway and Lambda for A/B Testing
author: vincent
email: ldg55d@gmail.com
tags: aws tutorial abtest apigw api-gateway lambda version alias stage stage-variables
publish: true
---

## TL;DR

코드는 여기[^1]

API Gateway Stage 와 Lambda Alias 를 이용하면 클라이언트 수정 없이 A/B 테스트를 해볼 수 있다.

## 시작하며

Personalize 등으로 새로운 추천 모델을 학습시키거나, 검색 엔진을 적용한다거나 하는 경우 A/B 테스트를 진행하여 성능(혹은 성과)을 측정하게 된다.

이러한 서버 기반의 A/B 테스트는 보통 클라이언트 코드를 수정을 하지 않고 서버의 설정이나 서버 배포만으로 진행하는 것이 가장 좋으며, 테스트를 위한 트래픽의 라우팅(분배) 의 경우 아래의 방법을 사용한다.

- 트래픽 기준 x:y 비율로 라우팅 한다. - x% 트래픽은 a 모델, y% 트래픽은 b 모델.
- 사용자를 기준으로 라우팅한다. - A 사용자는 a 모델, B 사용자는 b 모델.

이 글에서는 API Gateway 와 Lambda 의 기능을 이용하여, 클라이언트 수정없이 A/B 테스팅을 하는 방법을 알아본다.

## 대상 아키텍쳐

![](/assets/img/2020/0625/architecture.png)

위의 그림과 같은 아주 기본적인 아키텍쳐를 가지고 있고, A/B 테스팅을 진행한다고 가정한다.

## Lambda Version and Alias

먼저 람다 Version 과 Alias 에 대해서 알아보자.

### Lambda Version

![](/assets/img/2020/0625/version-actions.png)

람다의 버전(Version)을 만드는 것은 아주 쉽다.
위와 같이 콘솔에서 *Publish New Version* 을 클릭하면 즉시 버전이 생성된다.

버전은 현재 람다의 스냅샷이다.
그리고 이 스냅샷에 포함되는 내용에는 **환경변수** 도 포함이 되어 있다.
이를 이용하여 사용자가 동일한 코드이지만 환경변수별로 다른 액션을 하게끔 만들 수 있다.

예를 들어 아래와 같은 람다 함수가 있을 때,

```python
import os

name = os.environ['name']

def handler(event, context):
  return f'Hello, {name}'
```

Version1 에서 환경변수로 `{'name': 'dongkyl'}` 로 설정해두고 Version2 에서는 환경변수로 `{'name': 'haandol'}` 로 해두었다면 동일한 코드이지만 버전별로 출력하는 결과가 각각 다르게 된다.

### Lambda Alias

람다의 별칭(Alias) 은 함수 버전에 대한 포인터이다. 즉 별칭 *live* 를 만들어두고 *Version 3* 을 가리키게 해두면 *live* 를 호출하는 것이나 *Version 3* 을 직접 호출하는 것이나 동일한 효과를 가지게 된다.

![](/assets/img/2020/0625/alias.png)

위의 그림에서 볼 수 있듯 별칭의 가장 큰 특징은 2개의 버전에 대해서 Weight(트래픽) 를 지정할 수 있다는 것이다. 위의 설정대로면 *alias34* 라는 별칭을 호출하면 70%의 트래픽을 *Version 3* 으로 호출하고 30% 트래픽을 *Version 4* 로 호출하게 된다.

## API Gateway Stage

API Gateway 는 리소스에 대한 수정을 반영(Deploy)할 때, 스테이지(Stage) 를 이용하게 된다.

보통 아래와 같이 *dev* 스테이지와 *prod* 스테이지로 구분하여 리소스에 대한 수정이 정상적인지 *dev* 스테이지에서 체크하고 이상이 없으면 *prod* 스테이지로 반영하는 식으로 사용하게 된다.

![](/assets/img/2020/0625/api-stage.png)

각 스테이지는 람다의 환경변수와 같은 스테이지변수(stageVarialbles) 가 존재한다. 대상 아키텍쳐에서 람다를 호출하려면 API Gateway 에서는 *LambdaIntegration* 을 통해 람다를 API 의 endpoint 에 매핑을 해주게 되는데, 이 때 람다 함수의 ARN(주소) 가 필요하다.

이 주소를 직접 입력하지 않고 아래와 같이 스테이지 변수를 이용하여 동적으로 변하도록 할 수 있다. 이렇게 하면 리소스를 수정할 때마다 전체 API 를 디플로이하지 않고 스테이지 변수만 제어할 수 있다.

![](/assets/img/2020/0625/api-stage-lambda.png)

## 테스팅 시나리오

원래는 가이드만 하는 것이 아니라 A/B 테스트를 코드 레벨로 제공하려고 했는데 노력이 생각보다 많이 들어서...
(조회수가 많이 나오면 테스팅 하는 코드도 스크립트 형태로 제공해보겠다.)

여기서는 각 시나리오별로 A/B 테스트를 어떻게 진행하는지에 대해 가이드만 제공한다.

아래와 같은 람다코드가 있다고 가정하고 (실제 personalize recommendation 에 사용하는 코드) 시나리오를 진행한다.

```python
import os
import boto3

client = boto3.client('personalize-runtime')
campaign_arn = os.environ['campaign_arn']

def handler(event, context):
    user_id = event.get('user_id', '')
    if not user_id:
        raise RuntimeError('user_id should be provided')

    num_results = int(event.get('num_results', 25))

    response = client.get_recommendations(
        campaignArn=campaign_arn,
        userId=user_id,
        numResults=num_results,
    )
    return response['itemList']
```

위에 설명한 내용대로 *campaign_arn* 이 람다의 환경변수에 지정되어 있고 각 버전은 서로 다른 campaign_arn 을 환경변수에 가지고 있다.

배포(Production) 환경에서는 API Gateway 에서 LambdaIntegration 을 사용할때는 별칭(또는 버전)을 사용해야 한다.
아무런 버전이나 별칭을 설정하지 않으면 `$LATEST` 라는 예약된 버전을 사용하게 되는데, 이 버전은 항상 최신의 코드를 참조하고 있다.
이럴 경우, 새로운 버전을 생성하기 위해서 코드나 환경변수를 수정하고 저장하면 해당 내용이 바로 사용자에게 반영된다.

따라서 배포환경에서는 안정된 코드를 publish 해서 버전으로 만들고 해당 버전을 *live* 등의 별칭으로 포인팅해서 API Gateway 등에서 사용하는 것이 좋다.

### 사전작업

1. 현재 람다에서 버전1(V1) 의 환경변수는 아래와 같이 설정한다.
```json
{ "campaign_arn": "arn::aws::...:campaign_version_1" }
```

2. 람다에서 별칭(Alias) *live* 를 생성하고 live 는 V1 버전을 가리키고 있다.

3. API Gateway 의 LambdaIntegration 에서 람다의 아래와 같이 설정되어 있다.
```
arn::aws::lambda::...:LAMBDA_FUNCTION:${stageVariable.lambdaAlias}
```

4. 스테이지이름은 *dev* 이며 스테이지 변수는 아래와 같이 설정되어 있다.
```json
{ "lambdaAlias": "live" }
```

### 트래픽 기준 라우팅

해당 람다에 들어오는 트래픽을 랜덤하게 x:y 비율로 라우팅하는 방식이다.

![](/assets/img/2020/0625/personalize-apigw.png)

1. 새 모델의 *campaign_arn* 을 환경변수에 등록하고 새 버전(V2)을 만든다.
2. 람다의 별칭 *live* 를 수정하여 V1 에 90%, V2 에 10% 의 weight 를 준다.
3. 테스트가 끝나면 live 의 버전을 V1 또는 V2 하나로 설정해준다.

### 사용자 기준 라우팅

해당 사용자의 등급이 VIP 일 경우 V1, 일반 사용자일 경우 V2 로 보낸다고 해보자. 이 경우 사용자를 구분하는 값은 *grade* 라는 키로 이미 전달되고 있다고 가정한다.

![](/assets/img/2020/0625/personalize-lambda.png)

1. 람다의 환경변수에 *campaign_arn2* 키로 새로운 모델의 값을 입력한다.

2. 코드를 아래와 같이 수정한다.

```python
import os
import boto3

client = boto3.client('personalize-runtime')
campaign_arn = os.environ['campaign_arn']
campaign_arn2 = os.environ['campaign_arn2']

def handler(event, context):
    user_id = event.get('user_id', '')
    if not user_id:
        raise RuntimeError('user_id should be provided')

    num_results = int(event.get('num_results', 25))

    if event['grade'] == 'vip':
      response = client.get_recommendations(
          campaignArn=campaign_arn,
          userId=user_id,
          numResults=num_results,
      )
    elif event['grade'] == 'normal':
      response = client.get_recommendations(
          campaignArn=campaign_arn2,
          userId=user_id,
          numResults=num_results,
      )
    else:
      raise RuntimeError(f'Invalid customer grade: {event['grade']}')

    return response['itemList']
```

3. 새로운 버전을 생성한다. (V2)

4. 별칭 live 의 버전을 기존 V1 에서 V2 로 바꾼다.

5. 테스트가 끝나면 live 의 버전을 적절히 수정해준다.

### (번외) Route53 을 이용한 트래픽 기준 라우팅

API Gateway 를 라이브와 개발용을 따로 운영하는 경우 라이브 환경을 직접 건드리는 것이 부담스러울 수 있다.

이럴 경우 Route53 의 weighted routing 기능을 이용하여 아래와 같이 테스팅할 수도 있다.

![](/assets/img/2020/0625/personalize-r53.png)

장점은 어떠한 코드나 인프라의 수정도 필요없고 Route53 의 필드만 수정해주면 된다.

단점은 Route53 을 이미 사용하고 있어야 한다는 점과, 경우에 따라서 다른 API 들과 분리해야 한다. (즉, 잘 정의된 MSA 구조가 아니면 적용하기 힘들다.)

## 마치며

CodeDeploy 로 람다를 디플로이하면 *트래픽 기준 라우팅*과 완전히 동일하게 동작한다.

그래서 CodeDeploy 를 A/B 테스트 툴로 사용하면 되지 않을까? 하는 생각이 들어 찾아봤었다.

하지만 보통 A/B 테스트는 주단위로 진행하고 결과를 취합하는데, CodeDeploy 는 48시간 이내에 디플로이가 완료되어야 하기 때문에 적합하지 않은 툴이었다.

위의 내용을 자동으로 진행하는 것은 StepFunctions 을 통해서 코드를 만들고 진행하는 것이 가장 좋은 방법일 것 같다.(StepFunctions 의 Execution 은 최대 1년까지 진행할 수 있다.)

----

[^1]: [AWS Serverless A/B Test](https://github.com/haandol/aws-serverless-abtest)