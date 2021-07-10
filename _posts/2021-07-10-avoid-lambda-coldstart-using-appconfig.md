---
layout: post
title: AWS AppConfig 를 이용해서 람다 콜드스타트 우회하기
excerpt: Avoid AWS Lambda cold start using AWS AppConfig
author: vincent
email: ldg55d@gmail.com
tags: serverless lambda aws cold-start appconfig cloud extensions
publish: true
---

## TL;DR

코드는 여기[^1].

## 시작하며

람다는 대부분의 수정에 대해서(코드, 환경변수) 버전을 올려야 하고, 
버전이 변경될 때마다 새로운 내부에서 새로운 컨테이너가 뜨기 때문에 콜드스타트를 하게 된다.
특히 람다가 VPC 환경을 쓰도록 설정되어 있으면 배포시간 및 콜드스타트 시간이 더 길어진다.

`비즈니스 로직에 대한 변경은 어쩔 수 없지만, 함수에서 사용하는 설정데이터나 메타데이터를 변경했을 때는 컨테이너를 그대로 사용할 수 있으면 좋겠다`

라는 요구사항에서 AWS AppConfig 서비스가 만들어졌다.

람다에서는 AppConfig 를 람다 익스텐션 형태로 사용할 수 있고, 
이 람다 익스텐션은 콘솔상에서 봤을땐 람다 레이어와 동일한 형태로 사용하는 것처럼 보인다.

이 글에서는 AWS 에서 제공하는 빌트인(?) 익스텐션인 AppConfig 익스텐션을 이용해서, 
설정데이터를 동적으로 변경하더라도 람다 컨테이너는 변경없이 사용하는 방법을 살펴본다.

## 설치하기

설치방법은 코드[^1] 의 README 를 읽고 따라하면 된다.

CDK 를 이용해서 코드를 배포하면 람다함수 하나와 AppConfig 환경이 배포가 된다.

## 테스트

배포된 람다함수는 AppConfig 에 저장된 JSON 형태의 스트링을 가져와서 그대로 리턴해주는 간단한 함수이다.

```typescript
import os
import json
import urllib.request

app_name = os.environ['APP_NAME']
env_name = os.environ['ENV_NAME']
profile_name = os.environ['PROFILE_NAME']


def handler(event, context):
    return {
       'configuration': json.loads(get_configuration(app_name, env_name, profile_name))
    }


def get_configuration(app, env, profile):
    url = f'http://localhost:2772/applications/{app}/environments/{env}/configurations/{profile}'
    return urllib.request.urlopen(url, timeout=2).read()
```

배포가 끝났으면 람다 함수를 호출해본다. 스크린샷처럼 대부분의 IDE 플러그인으로 나와있는 AWS Toolkit 을 사용하면 편하다.

<img src="/assets/img/2021/0710/invoke lambda.png" />

```bash
Loading response...
Invocation result for arn:aws:lambda:ap-northeast-2:929831892372:function:AppConfigDemoAppConfigTestFunction
Logs:
START RequestId: 697985b8-d042-4181-95a7-2e8912ff006e Version: $LATEST
END RequestId: 697985b8-d042-4181-95a7-2e8912ff006e
REPORT RequestId: 697985b8-d042-4181-95a7-2e8912ff006e	Duration: 76.18 ms	Billed Duration: 77 ms	Memory Size: 128 MB	Max Memory Used: 75 MB	Init Duration: 249.81 ms	
XRAY TraceId: 1-60e9b697-42ab67dc772d98dc6a288677	SegmentId: 709a046878a0a112	Sampled: true	


Payload:
{"configuration": [{"username": "dongkyl"}, {"username": "haandol"}]}
```

첫 실행시에는 `Init Duration` 이 표시되며 함수가 콜드스타트로 호출되었다는 것을 의미한다.

```bash
oading response...
Invocation result for arn:aws:lambda:ap-northeast-2:929831892372:function:AppConfigDemoAppConfigTestFunction
Logs:
START RequestId: 513f495a-950a-4ac4-9c30-3bcda222d206 Version: $LATEST
END RequestId: 513f495a-950a-4ac4-9c30-3bcda222d206
REPORT RequestId: 513f495a-950a-4ac4-9c30-3bcda222d206	Duration: 67.07 ms	Billed Duration: 68 ms	Memory Size: 128 MB	Max Memory Used: 79 MB	
XRAY TraceId: 1-60e9b6e8-42db11e71e44663532cd5064	SegmentId: 60f2b3fe75cafee1	Sampled: true	

Payload:
{"configuration": [{"username": "dongkyl"}, {"username": "haandol"}]}
```

두번째 실행시에는 위와 같이 Init duration 이 없는 것을 볼 수 있다.

### 설정업데이트

`infra/lib/interfaces/config.ts` 안에 configContent 변수를 적절히 업데이트 하고 `cdk deploy` 를 통해 배포해보자.
람다 코드나 환경변수를 변경한 것이 없기 때문에 AppConfig 에만 변경사항이 적용되고, 현재 떠 있는 람다 컨테이너는 재사용된다.

여기서는 `{"username": "haandol"}` 부분만 지우고 deploy 해보았다.

```bash
Loading response...
Invocation result for arn:aws:lambda:ap-northeast-2:929831892372:function:AppConfigDemoAppConfigTestFunction
Logs:
START RequestId: 28b7a013-c4a1-43e9-a1a7-bf1c64b87ceb Version: $LATEST
END RequestId: 28b7a013-c4a1-43e9-a1a7-bf1c64b87ceb
REPORT RequestId: 28b7a013-c4a1-43e9-a1a7-bf1c64b87ceb	Duration: 6.04 ms	Billed Duration: 7 ms	Memory Size: 128 MB	Max Memory Used: 79 MB	
XRAY TraceId: 1-60e9b7f5-7ec9ccec7a74f3bb3d1abed7	SegmentId: 6834d581170e357f	Sampled: true	


Payload:
{"configuration": [{"username": "dongkyl"}]}
```

배포가 완료되고 호출하면 변경한 config value 가 잘 반영되었지고, init duration 도 여전히 없는 것을 확인할 수 있다.(웜스타트)


## 마치며

PC 를 사용하거나, VPC를 이용할 때 소소한 설정 변경에도 배포시간이 엄청 길어지는데,
AppConfig 를 이용하면 불필요한 람다 배포를 줄일 수 있다.

익스텐션을 이용하면 람다 런타임 API 와 별도로 epspagon, datadog 등 다양한 서드파티툴과도 쉽게 연결할 수 있기 때문에,
다양하게 많이 사용될 것 같다.

----

[^1]: [Lambda AppConfig Example](https://github.com/haandol/lambda-appconfig-example)