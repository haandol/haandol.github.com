---
layout: post
title: Typescript2 서버 튜토리얼 - 2/5
excerpt: Typescript + Express
author: vincent
email: ldg55d@gmail.com
tags: typescript2, express, mongodb, mongoose, nodejs
publish: true
---

## TL;DR

코드는 여기[^1]


## 시작하며

본 글은 **typescript 를 이용하여** express 를 쓰는 것이 목적이므로일단 express 의 기본은 안다고 가정한다.
express 기본 사용법은 공식 홈페이지의 문서로도 충분한 것 같다.
~~어차피 경량 웹 프레임워크는 라우팅, 미들웨어, 렌더링, 세션만 배우면 되니깐~~

본 글에서는 express 를 이용하여 밀짚모자 해적단~~히익 오따꾸!!~~ 등장인물의 정보를 조회할 수 있는 간단한 REST API를 만들어보자.

우리가 만들 API는 아래 2개의 기능만 제공한다.

* 전체 해적 목록 가져오기
* 이름으로 정보 가져오기


## 프로젝트 생성

본 글은 ts-tutorial v1[^2]의 프로젝트 구조를 기반으로 진행하겠다.

```bash
$ git clone git@github.com:haandol/ts-tutorial.git
$ cd ts-tutorial
$ git checkout v1.0
```

프로젝트 구조는 다음과 같다.

```bash
.
├── LICENSE
├── README.md
├── package.json
├── src
│   └── index.ts
└── tsconfig.json
```

서비스를 개발하는 순서는 개인별로 다양할 수 있다. 본 글에서는~~개인적으로~~ 아래 순서를 선호한다.

 1. 도메인 정의(DB 모델)
 2. API 설계(인풋/아웃풋)
 3. 로직 작성 ~~및 테스트 작성~~ 
 4. 라우팅 테이블에 추가 ~~및 인수테스트 작성~~

원래는 유닛 테스트 등을 작성하는게 맞지만 글이 복잡해~~길어~~지니깐, 본 글에서는 테스트를 작성하는 부분은 제외한다.~~기회가 되면 다음에 다루거나~~


## 도메인 정의

일단 우리 API에서 다룰 엔티티는 *Pirate(해적)* 뿐이다.

src/domain 폴더를 만들고 models.ts 파일을 추가한 뒤 아래 내용을 넣자.

```bash
$ mkdir -p src/domain
$ touch src/doamin/models.ts
```

```typescript
// src/domain/models.ts

export class Pirate {
    constructor(
        public name: string,
        public bounty: number,
        public isEsper: boolean
    ) {}

}
```

위에 선언한 Pirate 클래스가 데이터베이스의 스키마 역할을 한다.

이제 로직에서 데이터를 가져올 수 있도록 아주 간단한 DB 를 만들자.

src/domain/db.ts 파일을 생성하고 아래의 내용을 채운다.

```bash
$ touch src/doamin/db.ts
```

```typescript
// db.ts

import { Pirate } from './models';

const pirates: Pirate[] = [
    new Pirate('루피', 5, true),
    new Pirate('상디', 1.7, false),
    new Pirate('조로', 3.2, false),
    new Pirate('우솝', 2, false),
    new Pirate('로빈', 1.3, true),
    new Pirate('브룩', .83, true),
    new Pirate('나미', .66, false)
]

class DB {
    constructor() {}

    public query = (name?: string): Pirate[] => {
        if (!name) {
            return pirates;
        }

        return pirates.filter(
            (pirate, i): boolean => { return pirate.name === name; }, pirates
        );
    }
}

export const db = new DB();
```

DB 가 하는 일은 매우 간단하다. 

1. models 에서 Pirate 모델을 임포팅 한다
2. Pirate[] 배열에 정적인 데이터를 로드하고
3. 사용자 쿼리시 name 파라미터가 입력되면 이름으로 검색하고 파라미터가 없으면 전체 목록을 반환한다.

query 함수를 간단히 설명하면

* *(name?: string)* 에서 `?` 는 해당 파라미터가 생략될 수도 있다는 것을 말한다. 생략되면 undefined 가 자동으로 들어간다.
* 따라서 name 이 입력되면 해당 name 과 동일한 해적을 반환하고 name 이 생략되면 전체 해적목록을 반환한다.


## API 설계

모델이 있다면 해당 모델을 API 로 CRUD 할 수 있어야 한다.
우리의 예제는 두개의 R(read) 기능만 제공하므로 간단하게 설계할 수 있다.

요청은 아래와 같은 API 형태로 요청하면 될 것이다.

```bash
$ http GET http://localhost:3000/pirate
전체목록 표시
```

특정 이름으로 가져오는 경우에는 *name* 파라미터만 있으면 되며, 요청은 다음과 같을 것이다.

```bash
$ http GET http://localhost:3000/pirate/루피
루피의 해적정보 표시
```

위 예제 요청에 사용된 httpie[^3] 는 curl 에서 제공하는 기능을 직관적으로 사용할 수 있게 해주는 프로그램이다.
본인이 curl 을 자주 쓴다면 httpie 도 한번 보면 좋을 것 같다.

```bash
$ brew install httpie
```


## Express.js 설치

API 로직 작성을 하기 전에 express 를 설치해보자

```bash
$ npm install --save express
$ npm install --save-dev @types/express
```

*@types/express* 는 typescript 타입정의(declarations)를 저장해둔 파일이며 해당 타입정의가 있어야 컴파일이 가능하다.
*--save-dev* 옵션으로 개발환경에 설치하는 이유는 컴파일된 JS 를 배포 할 것이기 때문에 배포 환경에서는 타입스크립트 관련 모듈이 필요가 없기 때문이다.


## 로직 작성

이제 로직을 작성해보자.

index.ts 에 모든 로직을 다 때려넣어서 만들어도 되지만
실제 프로젝트에서는 도메인이나 기능별로 파일을 구분해서 관리하는 것이 일반적이다.
여기서는 도메인 별로(그래봤자 Pirate 하나지만) 구분해서 파일을 생성해보겠다.

먼저 src/apps/pirate/controller.ts 를 생성하자.

```bash
$ mkdir -p src/apps/pirate
$ touch src/apps/pirate/controller.ts
```

해당 controller.ts 파일의 내용을 아래와 같이 채우자.

```typescript
// src/apps/pirate/controller.ts

import { Router, Request, Response } from 'express';

import { db } from '../../domain/db';
import { Pirate } from '../../domain/models';

const router: Router = Router();

router.get('/', (req: Request, res: Response) => {
    let data: Pirate[] = db.query()
    res.send(JSON.stringify(data));
});

router.get('/:name', (req: Request, res: Response) => {
    let { name } = req.params;
    let data: Pirate[] = db.query(name)
    res.send(JSON.stringify(data));
});

export const PirateController: Router = router;
```

엄청 간단한 코드라 express 튜토리얼을 끝낸 수준이면 읽고 이해 할 수 있을 것이다.
그래도 코드를 간단히 짚고 넘어가면

1. 먼저 db 를 로딩한다.
2. express.Router 기능을 이용해 /pirate 이하 서브패스를 처리할 라우터를 만든다.
3. 해당 라우터에 전체목록, 이름검색에 해당하는 라우트를 등록해준다. 각 라우트는 데이터를 json 문자열로 반환한다.

물론 express.Router 기능을 쓰지 않고 index.ts 에서 *app.get('/pirate/:name')* 과 같이 index.ts 안에서 모든 패스를 다 직접 지정해줄 수도 있다. ~~이 경우 conroller.ts 자체도 필요없어짐~~
하지만 위처럼 라우팅을 모듈화 해두면 여러 서브패스가 생기더라도 쉽게 관리할 수 있다.
또 지금은 src/apps/pirate/controller.ts 만 있지만 로직이 비대해지거나 하면 conroller(View), service(Controller), repository(Model) 로 MVC 를 적용할 수도 있다.


## express 서버코드 작성

서브패스 라우터를 추가했으니 express 서버코드를 작성하고 서브패스를 라우팅 테이블에 추가해주자.

기존 index.ts 를 모두 지우고 다음의 내용으로 채워준다.

```typescript
// src/index.ts

import * as express from 'express';

import { PirateController } from './apps/pirate/controller';

const app: express.Application = express();
const port: number = 3000;

app.use('/pirate', PirateController);

app.listen(port, () => {
    console.log(`Listening at http://localhost:${port}/`);
});
```

위의 코드 역시 튜토리얼 수준의 간단한 코드로 어려운 내용은 없다. 간단히 짚고 넘어가자.

1. express 를 임포팅 한다. typescript 의 임포팅은 `import * as 이름 from` 방식과 `import { 모듈명 } from`  방식이 있다.
관리측면에서는 후자를 쓸 수 있으면 쓰고 아닌 경우만 전자를 쓰는 것이 좋은 것 같다.
2. PirateController(express.Router 객체) 를 임포팅한다.
3. express app 을 생성한다.
4. app 에서 PirateController 를 사용하여 `/pirate` prefix 뒤에 서브패스로 라우트를 등록한다.
이런 방식을 모듈식 마운팅 이라고 부르며 라우팅 방식들에 대한 자세한 내용은 공식문서[^4] 를 참조하자.


## 서버 실행

서버 실행은 이전과 똑같다.

tsc 로 컴파일하고 src/index.js 를 실행하면 된다.

따라서 전에 설정해둔 `npm start` 명령을 그대로 쓰자. 해당 명령은 package.json 에 scripts 필드에 있다.

```bash
$ npm start
> cinnamon@1.0.0 start /Users/haandol/ts-tutorial
> tsc; node ./build/index.js

Listening at http://localhost:3000/
```

끝이다!!! 마지막으로 httpie 나 curl 로 정상적으로 API 가 동작하는 지 확인해보자.

```bash
$ http GET localhost:3000/pirate
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 325
Content-Type: text/html; charset=utf-8
Date: Fri, 28 Apr 2017 17:55:50 GMT
ETag: W/"145-Bgcrv7/sXVWx01gxwJJb3ocIYDw"
X-Powered-By: Express

[
{
    "bounty": 5, 
        "isEsper": true, 
        "name": "루피"
}, 
{
    "bounty": 1.7, 
    "isEsper": false, 
    "name": "상디"
}, 
...
]

$ http GET localhost:3000/pirate/루피
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 45
Content-Type: text/html; charset=utf-8
Date: Fri, 28 Apr 2017 17:57:37 GMT
ETag: W/"2d-uDyo54UhUxrfUYTLzXVdZEKAOn8"
X-Powered-By: Express

[
{
    "bounty": 5, 
    "isEsper": true, 
    "name": "루피"
}
]
```


## 마치며

구조 등에서 복잡해질 수 있기 때문에 코드적으로는 헷갈릴 요소를 최대한 제외시키고 작성했다. 이상한 내용이 있으면 알려주시라.

본 글과는 별개로 뭔가 블로그 처음 목적이 퇴색되어 가는 것 같다...~~먹고 사는게 힘들어서~~

빨리 연재를 마무리하고 데이터 분석쪽 공부하면서 글을 써야겠다.

----

[^1]: [ts-tutorial v2](https://github.com/haandol/ts-tutorial/tree/v2.0)
[^2]: [ts-tutorial v1](https://github.com/haandol/ts-tutorial/tree/v1.0)
[^3]: [httpie](https://httpie.org/)
[^4]: [express guide for routing](http://expressjs.com/ko/guide/routing.html)
