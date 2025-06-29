---
layout: post
title: 파이썬 슬랙봇 튜토리얼
excerpt: Honey 로 만드는 스크립터블 파이썬 슬랙봇
author: haandol
email: ldg55d@gmail.com
tags: slack scriptable plugin slackbot honey tutorial
publish: true
---

## TL;DR

Honey[^1] 는 이곳에서.

## 시작하며

파이썬이 주력 언어인 회사내에서 쉽게 기능을 추가하려고 주말에 간단히 만든 슬랙봇[^1] 이 있었다.

gevent 를 사용하여 동시성 문제를 해결했었지만, gevent 의 몽키패칭은 마음의 짐이었다.

이번에 gevent 를 Honey 에서 걷어내고 Py3 의 `async / await` 으로 대체하면서 튜토리얼을 써보기로 했다.

튜토리얼이 다루는 내용은 아래와 같다.

1. Honey 설치
2. Honey 를 말하게 하기
3. REST 요청으로 결과 출력하는 앱 추가하기

## 설치

### Slack 봇 추가

봇을 추가하는 방법은 App 등록과 Custom Integration 방법이 있는데
여기서는 Custom Integration 으로 진행한다. (엄청 간단하기 때문)

1. 웹으로 [slack](slack.com) 에 로그인 한다.
2. [봇 추가](https://my.slack.com/services/new/bot) 페이지에서 봇을 추가한다.
3. 바로 나오는 설정페이지에서 Integration Settings 메뉴의 API Token 을 복사해서 메모장에 붙여둔다.

### Honey 설치

1. [Python3.5.3](http://python.org) 이상을 설치한다.

2. 아래 명령으로 Honey 를 clone 한다.

```bash
$ git clone https://github.com/haandol/honey
```

3. pip 또는 pip3 명령으로 의존성을 설치한다.

```bash
$ cd honey
$ pip install -r requirements.txt
```

4. 원하는 에디터로 settings.py 를 열어서 SLACK_TOKEN 변수에 붙여넣기 해준다.

```bash
$ vim settings.py
...
SLACK_TOKEN = 'xoxb-621727845940-616854617227-hWvglOuZvg3UwYIqQH8VKfGK'
...
```

### Honey 띄워보기

1. robot.py 를 실행하고 봇이 채널에 온라인으로 표시되는지 확인한다.

```bash
$ python robot.py
INFO:honey:RTM Connected.
```

![](/assets/img/20190430/honey-online.png)

2. honey 에게 DM 으로 `!help` 라고 보내보고 적절히 응답이 오는지 확인한다.
![](/assets/img/20190430/honey-response.png)

## 앱 추가하기

Honey도 Hubot 처럼 내가 원하는 스크립트를 맘대로 플러그인 할 수 있다.
Honey 에서는 이러한 스크립트를 `App` 이라고 부른다.

이번 섹션에서는 REST API 요청을 받아와서 반환해주는 앱을 추가해본다.

1. `apps` 폴더 아래에 fake.py 를 추가한다.

```bash
$ vim apps/fake.py
```

2. `apps/fake.py` 에 아래내용을 입력한다.

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

4. `settings.py` 를 열고 `APPS` 에 `fake` 를 추가해준다.

```bash
$ vim settings.py
```
```python
...
APPS = ['helper', 'hello_world', 'fake']                                        
...
```

5. robot.py 를 실행하여 슬랙봇을 띄워준다.

```bash
$ python robot.py
$ tail -F honey.log
2019-05-01 16:50:06,266 - honey - INFO - RTM Connected.
...
```

6. 적당한 슬랙채널에 @honey 를 초대하고 !help, !fake 를 입력해본다.

![](/assets/img/20190430/honey-invite.png)
![](/assets/img/20190430/honey-send-command.png)

## Redis 저장소 사용하기

Honey 는 redis_brain 을 통해 Redis 에 데이터를 넣고 가져올 수 있다.
이번 섹션에서는 내장된 redis_brain 을 이용하여 메모하는 방법을 알아보자.

1. docker 로 redis 를 띄워본다.

```bash
$ docker run --name redis -d --publish 6379:6379 redis
57eef9fc911f5b0eb468a55688fc33897ba0a52e0d3f96e9fe7ca9628bb986e5
$ docker ps
```

2. settings.py 에 Redis 주소를 추가해주고 `redis_brain` 앱을 추가해주자.

```bash
$ vim settings.py
...
REDIS_URL = 'localhost'
REDIS_PORT = 6379
...
APPS = ['helper', 'hello_world', 'fake', 'redis_brain']
```

3. Honey 를 재시작해준다.

```bash
$ python robot.py
2019-05-01 16:50:06,266 - honey - INFO - RTM Connected.
```

4. honey 가 초대되어 있는 채널에서 `!memo` 명령으로 값을 저장하고 가져와본다.

![](/assets/img/20190430/honey-memo.png)

입력 순서는 다음과 같다.
```bash
!help
!memo
!memo hi
!memo hi there
!memo hi
``` 

hi 에 대해서 there 값을 저장해두고 잘 가져오는 것을 확인할 수 있다. Redis 를 이용하면 봇을 껐다키더라도 데이터를 유지할 수 있다.

내가 만든 앱에서 무언가 저장하고 가져오고 싶다면 `run()` 함수의 파라미터인 robot.brain 을 사용하면 된다.

## 마치며

휴봇의 파이썬 버전이 필요해서 시작한 프로젝트 였는데 node 기반 회사로 옮기니 그냥 휴봇을 쓰게 되어 시간을 많이 들이지 못해서 약간 안타까운 맘이 있었다.

언제든 필요한 내용들을 PR 해주면 좋겠다.

----

[^1]: [haandol/honey](https://github.com/haandol/honey)