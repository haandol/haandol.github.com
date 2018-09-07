---
layout: post
title: Redis cluster 튜토리얼
excerpt: Redis cluster + Proxy
author: vincent
email: ldg55d@gmail.com
tags: redis, redis-cluster, proxy, predixy
publish: true
---

## TL;DR

코드는 여기[^1]

## 시작하며

기존엔 redis 를 대규모로 쓰려면 sentinel 로 master-slave 를 구성하고 각 마스터들을 twemproxy 로 묶어서 샤딩할 수 밖에 없었다.

그러나 twemproxy 의 구조상 redis-cli 를 이용하여 콘솔에서 특정한 작업을 처리하는 것은 굉장히 귀찮은 작업이고, 무엇보다 twemproxy 는 유지보수를 안한지 오래되어 더 이상 쓰기가 좀 꺼려진다.

redis 3.0 부터 도입된 redis-cluster 를 쓰면 샤딩없이 redis 를 HA 하게 만들 수 있다.

cluster 이므로 sentinel 을 쓰지 않아도 되어 아키텍처가 간단해 지는 것은 덤.

redis-cluster 를 이용하여 클러스터를 구축하고 

redis-cluster 용 proxy 인 predixy 를 이용하여 redis-cli 에서 쉽게 작업할 수 있는 환경을 구축해보자.

## redis-cluster 특징

요즘 나오는 일반적인 클러스터 서비스의 특징을 다 갖추고 있다. (docker 안되는거 빼고)

- reids `3.0` 에서 추가되었다.
- `최대 1000 노드`까지 선형적으로 scaleout 할 수 있도록 설계되었다.
- docker 로 쓰려면 net=host 로 써야한다. `NAT 지원 안함.`
- 최대한 write 를 safe 하게 한다. (메이저 파티션의 요청이 우선처리된다. 기존 sentinel 도 마이너 파티션 에 대한 failover 는 하지 않는다.)
- 파티셔닝 복구 기능. (replicas migration 을 이용해서 슬레이브가 하나도 없는 마스터들은 여러 슬레이브를 가진 애들로부터 슬레이브를 받게 된다.)
- hash tags 라는 컨셉으로 구현되었다. (얼핏봐서는 consistency hashing 느낌)
- 하나의 db (0번) 만 쓴다.
- TCP 연결로 하트비트(ping-pong) 을 쏴서 클러스터를 유지한다. 이 TCP 연결을 클러스터 버스라고 부르고 `기본포트 + 10000` 포트로 통신한다. (offset 10000 은 고정)
- 클러스터는 완전 그래프로 되어 있으므로 100개의 노드가 있으면 노드당 99개의 하드비트를 쏘게 되어 있다. 단, node_timeout 이라는 게 있어서 이 타임아웃안에 하트비트를 다 전송하도록 전체 하트비트 주기를 조정해주는 식으로 된다. (부하분산)
- strong consistency 를 보장하지 않는다. 대부분의 클러스터가 그렇듯 eventually consistency.

## redis-cluster 구성

클러스터 구성방법은 여기[^2] 에 잘 나와있으므로 생략한다.

## proxy 설정

클러스터 구성 후 아무 노드나 redis-cli 로 들어가서 get/set 해보면 키가 샤딩된 노드에 맞춰 커넥션이 이리저리 redirection 된다.

클라이언트가 직접 사용한다면 얼핏봐도 엄청난 오버헤드가 있을 것 같은 일이므로 프록시를 앞에 두고 클라이언트는 프록시랑만 통신하도록 하자.

redis-cluster proxy 로 검색해서 이리저리 보다 보면 결국 codis, corvus, predixy 3개로 압축된다. (star 순서대로)

개인적으로는 Predixy[^3] 라는 녀석을 쓰기로 했는데 codis 는 기능이 너무 많고, corvus 는 관리가 안되고 있는 느낌이 들기 때문이다.

설치는 엄청 쉽다. 그냥 받아서 g++ 로 make 해버리면 된다. 하지만 요즘 이런 툴들은 내 컴에 깔기보다 도커로 까는 것이 낫다. 그래서 docker[^4] 로 구워놨다.
(용량을 줄이기 위해 alpine 으로 구우려고 했으나 musl glibc 와 리눅스용 glibc 가 함수 시그너처가 다른게 많아서 안구워져서 그냥 ubuntu 로 구웠다.)

여튼 일단 프로젝트를 클로닝한다.

```bash
$ git clone https://github.com/haandol/predixy
$ cd predixy
```

자신의 redis-cluster 구성대로 conf 아래의 cluster.conf, predixy.conf 를 수정한다.
servers 만 바꿔주면 된다. (앞의 + 는 오타가 아니며 꼭 붙여줘야함.)

```bash
# conf/cluster.conf
ClusterServerPool {
    MasterReadPriority 60
    StaticSlaveReadPriority 50
    DynamicSlaveReadPriority 50
    RefreshInterval 1
    ServerTimeout 1
    ServerFailureLimit 10
    ServerRetryTimeout 1
    KeepAlive 120
    Servers {
        + 127.0.0.1:7001
        + 127.0.0.1:7002
        + 127.0.0.1:7003
    }
}

# conf/predixy.conf
Name PredixyExample
Bind 0.0.0.0:7617
WorkerThreads 4
MaxMemory 0
ClientTimeout 300
BufSize 4096
Log ./predixy.log
LogRotate 1d
LogVerbSample 0
LogDebugSample 0
LogInfoSample 10000
LogNoticeSample 1
LogWarnSample 1
LogErrorSample 1

Include auth.conf
Include cluster.conf
Include latency.conf
```

수정후 아래의 명령으로 실행해본다.

```bash
$ docker-compose up -d
```

별 에러메시지가 없다면 실행된 상태임. 셸을 새로 띄워서 접속해보자.

```bash
$ redis-cli -p 7617 info
# Proxy
Version:1.0.5-pre
Name:PredixyExample
Bind:0.0.0.0:7617
...
 
# Servers
Server:127.0.0.1:7000
Role:master
Group:7921290b7deb00d57650357fe73c3fa03f54e209
DC:
CurrentIsFail:1
Connections:4
Connect:405
Requests:829
Responses:22
SendBytes:488
RecvBytes:9095
 
Server:127.0.0.1:7001
Role:master
Group:f2bf617ccf931843539083bdfa4ef54decd16188
DC:
CurrentIsFail:0
Connections:4
Connect:4
Requests:164
Responses:164
SendBytes:4496
RecvBytes:114951
...
 
LatencyMonitorName:blist
```

## 마치며

twemproxy 에 비해 안정적이고 설정도 간편하다. 이미 대규모 서비스 들에서 잘 쓰고 있다고 하고, redis 를 쓸거면 대안이 없기도 하다. (dynomite 같은 걸로 옮겨가면 몰라도)

단점은 redis 들을 host=net 으로 띄워야 한다는 것인데, 포트를 적절히 열어주는 것이 sentinel 설정하고 관리하는 거보다는 쉽기 때문에 극복할 수 있다.

(회사 컨플에만 글을 열심히 쓰다보니 개인 블로그에는 글을 안쓰게 된다. 이번 글도 억지로 쓰다보니 너무 날림 글이 되어버린 느낌..)

----

[^1]: [haandol/predixy](https://github.com/haandol/predixy)
[^2]: [leocat redis cluster](http://blog.leocat.kr/notes/2017/11/07/redis-simple-cluster)
[^3]: [Predixy](https://github.com/joyieldInc/predixy)
[^4]: [dockerized predixy](https://hub.docker.com/r/haandol/predixy/)