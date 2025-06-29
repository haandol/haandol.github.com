---
layout: post
title: Python arcade 를 이용해서 멀티플레이어 게임 만들기
excerpt: Develop multiplayer game using Python arcade
author: haandol
email: ldg55d@gmail.com
tags: python arcade multiplay network game
publish: true
---

## TL;DR

유튜브 참고[^1]

전체 코드는 필요하면 공유하는 걸로...

## 시작하며

IoT 센서를 이용한 게임형 프로토타입을 구현할 일이 생겨서 파이썬으로 구현해보기로 했다.

(사실 html5 엔진으로 만들고 싶었는데 센서 + 웹서버 띄우고 통신하고 하면 더 복잡해지므로 그냥 단일 클라이언트로 진행하기로 했다. 이런 요구사항에는 파이썬 엔진이 제일 적합한 것 같다.)

실제 게임쪽 코드는 튜토리얼을 보고 만들면 충분하기 때문에 본 글에서는 네트워크 연결쪽을 위주로 설명해보려고 한다.

## Python arcade

진짜 게임을 만들건 아니고 게임형으로 동작하는 비주얼이 필요한 것 이었다. 따라서 낮은 학습곡선에 사용하기 쉽고 문서화가 잘된 엔진이 필요했다.

찾다보니 개발도상국[^2]에서 소개한 Ursina[^3] 엔진을 알게 되었는데 진짜 쉽게 구현할 수 있도록 추상화가 잘 되어 있었지만 문서화가 너무나 아쉬웠고 실제로 동작하는 예제들이 별로 없었다.

문서화가 잘되어 있고 예제 코드들이 적당한 것으로 PyGame 과 Python Arcade[^4] 가 있었는데 문서화가 우월하고 좀 더 추상화 되어 있는 Python Arcade 를 쓰기로 했다.

### Platformer 게임 만들기

마리오나 소닉 같이 발판(플랫폼)을 이용한 게임 장르를 플랫포머 게임이라고 부른다.

간단한 2D 플랫포머 튜토리얼[^5]을 따라하면 1~2시간 남짓만에 플랫포머 게임을 맘대로 만들 수 있다.(Ursina 보다 약간 손이 가지만 아이워너비더가이도 쉽게 만들 수 있음)

위의 내용과 크게 다르지는 않고 좀 더 복잡한 형태의 튜토리얼도 제공하고 있다.


## 네트워크 연결 추가하기

캐릭터 2개를 보여주고 적절히 움직이게 하는 것은 위의 예제로 충분한데, 목표는 멀티플레이어게임으로써 네트워크연결을 통해 데이터를 받아서 캐릭터를 움직이도록 해야 한다.

네트워크 연결을 제일 쉽게 처리하는 방법은 socket.io, mqtt 나 웹소켓 방식으로 tcp 연결을 열어두고 메시지를 받는 방법일 것이다.

이 영상[^1] 에서 어떻게 해당 작업을 하는지 코드와 함께 보여준다. (강연에 사용된 코드를 따로 공유하고 있지는 않는 것 같다.)

이후 내용은 해당 영상의 내용을 기반으로 조금 살을 붙여서 소개한다. (사실 해당 영상 내용으로 충분한 것 같음.)

### 네트워크 루프 쓰레드 추가하기

일단 arcade.Window.run() 이 메인루프를 점유하기 때문에 메인쓰레드를 통해서는 네트워크 통신을 할 수가 없다.

따라서 네트워크 메시지 블로킹 부분을 쓰레드를 통해서 처리하는 일반적인 방법을 사용한다.

```python
import arcade

...

def run():
    window = MyGame()
    window.setup()
    return window


def worker(window: arcade.Window):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main(window))
    loop.run_forever()


def main():
    window = run()
    thread = threading.Thread(target=worker, args=(window,), daemon=True)
    thread.start()
    arcade.run()


if __name__ == '__main__':
    main()
```

`main` 함수에 window 객체를 인젝트 했기 때문에, 네트워크에서 전달받은 메시지에 따라 window 내의 모든 객체(사실상 게임전체) 를 통제할 수 있게 된다.

### main 함수

인증부분을 제외한 `main` 함수는 대략 아래와 같이 생겼다.

여기서는 websockets[^6] 라이브러리를 썼는데, 최근 py3 의 네트워크 관련 라이브러리들은 대부분 asyncio 기반의 코루틴을 사용하고 있기 때문에 익숙해지는 것이 좋은 것 같다.

```python
import websockets

async def main(window):
    uri = 'wss://xxxx.execute-api.ap-northeast-2.amazonaws.com/dev'
    ws = await websockets.connect(uri)

    connection_id = await get_player_id(ws)
    window.player_conn_id = connection_id

    session_id = await create_session(ws)
    window.session_id = session_id

    async def recv_message():
        while True:
            resp = await ws.recv()
            command = json.loads(resp)
            if 'action' not in command:
                print(f'Invalid command: {command}')
                continue
 
            if command['action'] == 'join-session':
                await on_join_session(window, command['data'])
                await ready_game(ws, session_id)
            elif command['action'] == 'ready-game':
                await on_ready_game(window, command['data'])
            elif command['action'] == 'start-game':
                await on_start_game(window, command['data'])
            elif command['action'] == 'update-tick':
                await on_update_tick(window, command['data'])
                if is_finished(window):
                    await end_game(ws, window.session_id, window.player_tick)
            elif command['action'] == 'end-game':
                await on_end_game(window, command['data'])
            else:
                print(f'Invalid action: {command}')
            
    try:
        await asyncio.gather(recv_message())
    finally:
        await ws.close()
```

위의 코드는 일반적인 웹소켓 기반으로 json 형태로 메시지를 주고 받는 방식으로 구성되었다.

peer-to-peer 통신이 아니라 클라이언트-서버 간 통신 방식이며 pub-sub 에 가깝다.

1. host가 게임세션(게임룸)을 만들고 (create-session)
2. 상대방(client) 가 join-session 한다.
3. 양쪽이 ready-game 를 하면 서버에서 start-game 이벤트를 발생해준다.
4. 프로토타입이므로 지연에 대한 보정은 하지 않고 스테이트 관리는 lockstep 과 비슷한 방식으로 처리한다.
5. 정해진 주기마다 데이터를 update-tick 으로 브로드캐스팅 한다.
6. 지정된 조건이 만족되면 클라이언트에서 end-game 을 보낸다.
7. 서버에서 tick 정보를 확인해서 winner 를 판정해서 브로드캐스팅 한다.

MQTT(IoT Core) 나 socket.io 를 이용하면 코드 자체는 훨씬 명료하게 만들 수 있겠지만, 데이터 주고받는 구조는 비슷할 것이다.


### 테스트

<img src="/assets/img/2021/0816/game.png" />

클라이언트는 동일한 코드로 헤드레스로 작업했는데, 잘 동작하는 것을 볼 수 있었다. (즉, 영상[^1] 내용대로 코딩하면 잘 동작한다는 이야기)

## 마치며

약 1주일 만에 웹소켓 기반으로 네트워크 플레이가 가능한 게임을 만들어봤는데, 학교에서 공부를 이런걸로 가르치면 재미있게 공부했을 것 같다.

----

[^1]: [Multiplayer 2D games with Python Arcade](https://www.youtube.com/watch?v=2SMkk63k6Ik)
[^2]: [파이썬으로 아이워너비더보시 게임 만들기](https://www.youtube.com/watch?v=FewuiyWLxbg)
[^3]: [Ursina Engine](https://www.ursinaengine.org/)
[^4]: [Python Arcade Engine](https://api.arcade.academy/en/latest/)
[^5]: [Simple platformer](https://api.arcade.academy/en/latest/examples/platform_tutorial/index.html)
[^6]: [Python websockets](https://websockets.readthedocs.io/en/stable/intro.html)