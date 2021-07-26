---
layout: post
title: NextJS 앱을 로컬환경에서 https 로 서빙하기
excerpt: Serve NextJS via https on localhost using Caddy
author: vincent
email: ldg55d@gmail.com
tags: nextjs next.js https ssl dev caddy
publish: true
---

## TL;DR

```bash
$ caddy reverse-proxy --from localhost:3030 --to localhost:3000
```

## 시작하며

개발중인 next.js 앱을 로컬환경에서 https 로 서빙해야할 경우가 있다. (인스타그램 콜백이라던지) 

대충 찾아봤는데 좀 이상한 방법들로 알려주는게 많은거 같다. 

mkcert 나 express.js 를 쓰면 next.js 를 typescript 로 개발하는 입장에서는 빌드를 계속해야해서 엄청 불편하고, ngrok 은 뭔가 외부 트래픽을 타니깐 좀 꺼려진다.

사실 케이스를 보자마자 Caddy 로 리버스 프록시 하면 되겠다 싶어서 해봤는데 나름 잘 되는것 같아서 간단히 공유한다.

## Caddy 설치

Caddy[^1] 는 옛날에 https 를 겁나 쉽게 만들어준다는 프록시로 잠깐 이슈가 됐었다.

홈페이지 나온대로 직접 설치해도 되지만 osx 는 그냥 homebrew 로 설치하자

```bash
$ brew install caddy
```

## Caddy 를 리버스 프록시로 띄우기

next.js 는 대략 이렇게 띄울것이다.
```bash
$ npm run dev

> insta-dev@0.1.0 dev
> next dev

ready - started server on 0.0.0.0:3000, url: http://localhost:3000
info  - Using webpack 5. Reason: Enabled by default https://nextjs.org/docs/messages/webpack5
```

그리고나서 caddy 를 3030 포트로 띄우고 모든 트래픽을 3000 포트로 포워딩해준다.

```bash
$ caddy reverse-proxy --from localhost:3030 --to localhost:3000
```

끝.


## 테스트

웹 브라우저에서나 터미널에서 https://localhost:3030 으로 접근해보자.

```bash
$ pip install httpie
$ http get https://localhost:3030 --verify no
```

----

[^1]: [Caddy](https://caddyserver.com/)