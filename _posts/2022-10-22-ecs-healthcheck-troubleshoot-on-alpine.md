---
layout: post
title: Amazon ECS 에서 헬스체크 실패시 확인할 내용
excerpt: Amazon ECS Troubleshooting - Healthcheck on Alpine
author: haandol
email: ldg55d@gmail.com
tags: troubleshoot amazon ecs healthcheck alpine curl
publish: true
---

## TL;DR

이미지가 alpine 이면 도커 빌드시 curl 을 깔아주자.

## 시작하며

아주 간단한 문제인데, 인터넷에 아무리 찾아도 없길래 기록삼아 남겨둔다.

## 문제

ECS 에 로드밸런서를 연결하는 경우에는 로드밸런서가 컨테이너 헬스체크를 해주므로, 따로 설정할 필요가 없다. (대부분 비워두거나 - 기본값은 체크안함, `["CMD-SHELL", "echo hello"]` 이런식으로 설정해두는 경우가 많다.)

Dockerfile 에도 헬스체크를 설정할 수 있는데[^1], ECS 에서 ContainerDefinition 에 지정하는 헬스체크 부분이 동일한 역할을 한다고 보면 된다.[^2]

ECS 가이드[^2] 에는 `[ "CMD-SHELL", "curl -f http://localhost/ || exit 1" ]` 이런식으로 가이드되어 있다.

다만, 대부분의 경우 스테이지를 나눠서 빌드할텐데 최종 스테이지는 alpine 을 쓰는 경우가 많다. 하지만 위의 명령을 쓰면 많은 alpine 이미지들 에서는 curl 이 없어서 헬스체크가 실패한다.

ECS 는 healthcheck 실패시 로그가 따로 남지 않기 때문에, 에러 메시지만 봐서는 알기가 어렵다. (ECS 배포시 헬스체크용 endpoint 는 로그도 꺼버리는 경우가 많기 때문에..)

## 해결방법

이미지에 curl 명령어가 포함되어 있는지 확인해보자.

```bash
$ docker run --rm golang:1.19.2-alpine curl -f http://google.com
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: exec: "curl": executable file not found in $PATH: unknown.
```

없다면 Dockerfile 빌드할 때 curl 을 설치해주자.

```dockerfile
FROM golang:1.19.2 AS builder

# build something
...

FROM golang:1.19.2-alpine AS server
RUN apk --no-cache add curl

...
EXPOSE 80

```

이후 healthcheck 는 공식문서 가이드처럼 설정하면 된다. (포트가 80 이고 healthcheck endpoint 는 / 라고 가정)

```bash
[ "CMD-SHELL", "curl -f http://localhost/ || exit 1" ]
```

위의 명령어는 ECS 에이전트가 사이드카에서 확인하기 때문에 포트를 따로 매핑해주거나 시큐리티 그룹을 열어줄 필요는 없다.

## 마치며

그 외에 일반적인 헬스체크 문제들은 여기[^3] 에 있다.

---

[^1]: [Dockerfile reference - HealthCheck](https://docs.docker.com/engine/reference/builder/#healthcheck)
[^2]: [ECS HealthCheck](https://docs.aws.amazon.com/ko_kr/AmazonECS/latest/developerguide/task_definition_parameters.html#container_definition_healthcheck)
[^3]: [Fargate에서 Amazon ECS 작업에 대한 상태 확인 실패 문제를 해결하려면 어떻게 해야 합니까?](https://aws.amazon.com/ko/premiumsupport/knowledge-center/ecs-fargate-health-check-failures/)
