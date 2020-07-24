---
layout: post
title: Beebot - 서버리스 파이썬 슬랙봇
excerpt: Beebot - Serverless python slack bot
author: vincent
email: ldg55d@gmail.com
tags: slack scriptable plugin slackbot beebot tutorial serverless aws
publish: true
---

## TL;DR

Beebot[^1] 은 이곳에서.

## 시작하며

예전에 만들어둔 슬랙봇[^2] 이 있었다.

오랜만에 쓸 일이 있어서 설치해보려고 했는데 슬랙쪽 정책이 바뀌어서 RTM 클라이언트를 사용하려면 Legacy 봇을 생성해야 한다.

슬랙에서도 RTM 보다는 Event API 를 권장하고 있는데, 이를 이용하면 서버리스로 슬랙봇을 구축할 수 있을 것 같아서 만들어보았다.

튜토리얼이 다루는 내용은 아래와 같다.

1. Beebot 설치
2. Beebot 를 말하게 하기
3. REST 요청으로 결과 출력하는 앱 추가하기

## 설치

### 인프라 설정

해당 인프라를 설정하면 아래와 같은 인프라가 배포된다.

![](https://github.com/haandol/bee-bot/raw/master/imgs/architecture.png)

서버리스 어플리케이션이므로 월단위 비용은 없고, 주고받은 메시지만큼만 비용이 청구된다.

월 200만건의 메시지를 주고받는 그룹에서 모든 메시지를 해당 봇이 읽게된다면 월 만원정도의 비용이 청구될 것으로 예상된다.

0. aws cli 를 설정한다.

1. NodeJs.12.x 를 설치한다.

2. 아래 명령으로 Bee-bot 을 clone 한다.

```bash
$ git clone https://github.com/haandol/bee-bot
```

3. npm 으로 의존성을 설치한다.

```bash
$ cd bee-bot
$ npm i
```

4. CDK를 설정한다

```bash
$ npm i -g cdk@1.54.0
$ cdk init
$ cdk bootstrap
```

5. 자신의 AWS 계정에 인프라를 배포한다.

```bash
$ cdk deploy "*" --require-approval never
```

6. 배포하고 나오는 API Gateway 주소에 slack 을 붙여서 복사해둔다. 모양이 아래와 같이 보일 것이다.

`https://xyz.execute-api.ap-northeast-2.amazonaws.com/dev/slack`


### Slack 봇 추가

Legacy 봇을 추가하는 것보다, Event API 추가하기는 약간 복잡하다.

1. [Slack API](https://api.slack.com/) 를 방문해서 *Start Building* 을 클릭한다.
2. *App Home* 에 가서, 아래의 scope 들을 bot 에 추가해준다. `chat:write, channels:history, channels:read, im:read, im:history, im:write, groups:history, groups:write, groups:read`.
3. *Event Subscriptions -> Enable Events* 에 가서, events api 을 활성화 해주고 the Request URL 을 위에서 소개한 API Gateway 주소로 붙여넣어준다.
4. *Event Subscriptions -> Subscribe* 에 가서, 아래의 이벤트들을 추가해준다. `message.channels and message.im`.
5. *OAuth & Permissions -> OAuth Tokens & Redirect URLs* 에 가서, *Install App to Workspace* 버튼을 클릭하고 *Allow* 버튼을 눌러준다.
6. *OAuth & Permissions -> OAuth Tokens & Redirect URLs* 에 가서, *Access Token* 을 복사해준다.
7. *Basic Information -> Verification Token* 에 가서, *Verification Token* 을 복사해준다.

### 토큰 등록해주기

github 에 토큰을 넣어서 커밋하면 슬랙에서 해당 토큰을 revoke 해버린다.(좋은 변화 같다.)

따라서 해당 토큰들을 AWS SSM 에서 제공하는 파라미터 스토어에 저장하여 코드에서 토큰을 분리해주자.

AWS SSM 파라미터 스토어는 비연결성으로 제공되는 키 밸류 스토어이다. 그리고 저장되는 모든 값은 암호화되어 저장된다.

아래와 같이 *scripts/update_slack_token.py* 를 실행해서 토큰을 업데이트 해주자.

```bash
$ ./scripts/update_slack_token.py --access-token YOUR_BOT_ACCESS_TOKEN --verification-token YOUR_VERIFICATION_TOKEN
```

이렇게 서버리스 슬랙봇 설정이 끝났다. 바로 테스트 해보자.

## 봇 테스트해보기

1. beebot 에게 DM 으로 `!hi` 라고 보내보고 응답이 오는지 확인한다.

![](/assets/img/2020/0719/beebot-test1.png)

2. beebot 을 적절한 채널(#general) 에 초대하고 `!hi` 라고 보내서 응답이 오는지 확인한다.

## 앱 추가하기

Beebot도 Hubot 처럼 내가 원하는 스크립트를 맘대로 플러그인 할 수 있다.
Beebot 에서는 이러한 스크립트를 `App` 이라고 부른다.

이번 섹션에서는 REST API 요청을 받아와서 반환해주는 앱을 추가해본다.

1. `libs/functions/slack/apps` 폴더 아래에 `fake.py` 를 추가한다.

```bash
$ vim libs/functions/slack/apps/fake.py
```

2. `fake.py` 에 아래내용을 입력한다.

```python
from . import on_command
import json
import requests

URL = 'https://jsonplaceholder.typicode.com/todos/1'

def fetch():
    res = requests.get(URL).json()
    return res['title']

@on_command(['fake', '테스트'])
def run(robot, channel, user, tokens):
    '''fake rest api 에 요청을 보내고 결과를 받아옵니다'''
    msg = fetch()
    return channel, msg
```

코드를 간단히 설명하면,

1라인의 `@on_command` 데코레이터는 명령어를 등록해준다.
우리가 만든 fake 앱은 honey 에게 `!fake` 또는 `!테스트` 메시지를 보내서 실행할 수 있다.

5라인의 URL에 브라우저로 접속해보면 단순히 아래와 같은 json 문서를 반환하는 것을 확인할 수 있다.
```json
{
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
}
```

`fetch()` 함수는 위의 URL 에서 title 필드를 반환한다. 간단한 기능이지만 함수를 따로 분리한 이유는 run 을 직접실행할 수 없기 때문에 개별기능에 대한 테스트를 편하게 하기 위해서이다.

13라인의 `docstring` 은 `!help` 메시지를 받았을때 사용자에게 표시된다.

3. 앱이 정상적으로 동작하는지 테스트를 해본다.

```bash
$ python
>>> from apps import fake
>>> fake.fetch()
'delectus aut autem'
```

4. `libs/interfaces/constant.ts` 를 열고 `apps` 에 `fake` 를 추가해준다.

```bash
$ vim constant.ts
```
```javascript
...
const apps = ['helper', 'hello_world', 'memo', 'fake']
...
```

5. CDK 를 배포하여 새 코드를 봇에 반영한다.

```bash
$ cdk deploy "*" --require-approval never
```

6. 적당한 슬랙채널에 @beebot 를 초대하고 !help, !fake 를 입력해본다.

> 슬랙봇 이름을 beebot 이라고 지었다고 가정

## AWS SSM 파라미터 스토어 사용하기

Beebot 은 AWS SSM 파라미터 스토어를 데이터를 저장하고 가져올 수 있다.
> 최대 10,000 개 까지 저장할 수 있다. 키밸류를 좀 더 대량으로 쓰고 싶다면 dynamodb 를 이용하는 게 효과적이다.

이번 섹션에서는 내장된 *memo* 앱을 이용하여 메모하는 방법을 알아보자.

1. honey 가 초대되어 있는 채널에서 `!memo` 명령으로 값을 저장하고 가져와본다.

![](/assets/img/20190430/honey-memo.png)

입력 순서는 다음과 같다.
```bash
!help
!memo
!memo hi
!memo hi there
!memo hi
``` 

hi 에 대해서 there 값을 저장해두고 잘 가져오는 것을 확인할 수 있다.

내가 만든 앱에서 무언가 저장하고 가져오고 싶다면 `run()` 함수의 파라미터인 robot.brain 을 사용하면 된다.

## 마치며

Amazon Chime 만 썼는데, 이제 다시 Slack 을 쓰게 될 것 같아 만들어봤다.

----

[^1]: [haandol/bee-bot](https://github.com/haandol/bee-bot)
[^2]: [haandol/honey](https://github.com/haandol/honey)