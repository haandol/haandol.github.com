---
layout: post
title: Typescript2 서버 튜토리얼 - 3/4
excerpt: Typescript + MongoDB
author: haandol
email: ldg55d@gmail.com
tags: typescript2 typescript express mongodb mongoose nodejs
publish: true
---

## TL;DR

코드는 여기[^1]


## 시작하며

본 글은 typescript 를 이용하여 mongodb 를 쓰는 것이 목적이므로 일단 mongodb 의 기본은 안다고 가정한다. 
mongodb 기본 사용법은 공식 홈페이지의 문서로도 충분한 것 같다.

본 글에서는 mongodb 를 이용하여 밀짚모자 해적단 등장인물의 정보를 다룰(CRUD) 수 있는 클래스를 작성해본다.


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

## MongoDB 서버 준비

일단 homebrew 로 mongodb를 설치하고 */data/db* 폴더(기본폴더)를 생성해준다.

```bash
$ brew install mongodb
$ sudo mkdir -p /data/db
$ mongod
```

mongo 명령어로 서버에 접속이 되면 정상적으로 실행된 것이다.

```bash
$ mongo
```

## typescript, mongoose 설치

이제 typescript 와 mongodb 드라이버인 *mongoose* 패키지를 설치해보자. 
*@types/패키지명* 으로 타입정의를 함께 설치하는 것도 잊지 말자.

```bash
$ npm install --save mongoose typescript
$ npm install --save-dev @types/mongoose @types/node
```

## 스키마 정의

mongodb 는 아래와 같이 Schema 를 이용해 Model을 생성하고, 이를 이용하여 DB 에 Document 를 추가한다.

```javascript
var mongoose = require('mongoose');

var schema = new mongoose.Schema({
    name:   {type: String, required: true},
    age:    {type: Number, required: true}
});
var User = mongoose.model('User', schema);

var robin = new User({name: 'robin', age: 30});

function printAge(pirate) {
    console.log(pirate.age);
}

printAge(robin);                // 30
printAge({name: 'robin'});      // this prints 'undefined'
```

*printAge* 함수의 경우 User 모델의 age 필드를 참조하여 처리를 하지만
javascript 특성상 아무 객체나 다 던져줘도 처리할 수 있다.

Typescript 를 사용하면, 아래처럼 파라미터가 스키마에 맞는 객체가 아니면 컴파일타임에 에러를 낸다.

```typescript
// src/index.ts

import * as mongoose from 'mongoose';

interface User extends mongoose.Document {
    name: string;
    age: number;
}

const schema = new mongoose.Schema({
    name:   {type: String, required: true},
    age:    {type: Number, required: true}
});
const UserModel = mongoose.model<User>('User', schema);

let robin = new UserModel({name: 'robin', age: 30});

function printAge(pirate: User) {
    console.log(pirate.age);
}

printAge(robin);            // 30
printAge({name: 'robin'});  // CompileError: can not convert to User
```

Typescript 를 쓰면서 추가된 사항은 아래와 같다.

1. mongoose.Document 를 상속받은 Pirate 인터페이스를 정의하고
2. 모델 생성시 Pirate 인터페이스를 제너릭 파라미터로 전달해준다.


### IPirate 정의하기

~~당연하게도~~ 타입체크를 하기 위해서 먼저 인터페이스나 클래스를 만들어야 한다.

해적 정보를 저장하기 위해 src/domain/pirate.ts 를 만들고 Pirate 인터페이스를 추가하자

참고로 많은 인터넷 예제들이 `IPirate` 이런 식으로 `I` 를 앞에 붙여서 인터페이스를 명명하는데
공식 스타일가이드는 인터페이스 앞에 `I`를 붙이지 않도록 권장한다.

```bash
$ mkdir -p src/domain
$ touch pirate.ts
```

```typescript
// src/domain/pirate.ts

import * as mongoose from 'mongoose';

export interface Pirate extends mongoose.Document {
    name: string;
    bounty: number;
    isEsper: boolean;
};

const pirateSchema = new mongoose.Schema({
    name:     {type: String, required: true},
    bounty:   {type: Number, required: true},
    isEsper:  {type: Boolean, required: true}
});
export const PirateModel = mongoose.model<Pirate>('Pirate', pirateSchema);
```


## DB 클래스 만들기

mongodb 의 CRUD 기능을 쉽게 쓸 수 있도록 wrapper 클래스를 하나 만들자.

먼저 src/domain/db.ts 를 만들고 아래 내용을 추가하자.

```typescript
// src/domain/db.ts

import * as mongoose from 'mongoose';
import { Pirate, PirateModel } from './pirate';

export class DB {
    constructor() { }
}
```

이제 DB 클래스에 기능을 하나씩 추가해보자.

### 데이터 추가하기(Create)

```typescript
// src/domain/db.ts

import * as mongoose from 'mongoose';
import { Pirate, PirateModel } from './pirate';

export class DB {
    constructor() { }

    create(pirate: Pirate): Promise<Pirate> {
        let p = new PirateModel(pirate);
        return p.save();
    }
}
```

*PirateModel* 은 mongoose.Model 을 상속받아 만들어지며,
Model.save() 는 해당 모델을 이용해 mongodb 에 Document 를 생성한다.

이 때 반환된 값은 `Promise<T>` 의 제너릭 형태인데,
`<T>` 제너릭은 런타임에 타입을 지정할 수 있게 해주는 기법으로
처음 *PirateModel* 생성시 Pirate 로 지정해줬었다.

Promise 를 쓰지 않고 콜백(callback) 방식으로 호출 할 수도 있는데 아래와 같이 해주면 된다.

```typescript
let p = new PirateModel(pirate);
p.save((err, raw) => {
    console.log('Document is created successfully');
});
```

콜백 방식은 여러 비동기 요청을 다룰 때 복잡한 코드를 만들게 되므로 가급적 Promise 와 친해지는 것이 좋다.
최근에는 generator 나 async/awaits 를 이용한 코루틴 기법도 많이 사용되고 있으니 참고하기 바란다.

본 글에서는 CRUD 비동기 요청을 위해 Promise 방법을 사용하기로 한다.


### 데이터 가져오기(Read)

생성한 데이터를 읽어 들이는 read 함수를 추가해보자

```typescript
// src/domain/db.ts

...

export class DB {
    constructor() { }

    read(query: any): mongoose.DocumentQuery<Pirate[], Pirate> {
        return PirateModel.find(query);
    }

    create(pirate: Pirate): Promise<Pirate> { ... }
}
```

Model.find 함수는 `mongoose.DocumentQuery<Pirate[], Pirate>` 를 반환하며
mongoose.DocumentQuery 인터페이스는 Promise 타입을 상속받는다.
따라서 실제로 반환하는 것은 `Promise<Pirate[], Pirate>` 형태라고 생각하면 편하다.

마찬가지로 read 함수도 아래와 같이 콜백 방식으로 구현할 수도 있다.

```typescript
// src/domain/db.ts

...

export class DB {
    constructor() { }

    read(query: any): void {
        PirateModel.find(query, (err, pirates) => {
            console.log(pirates.length);
        });
    }

    create(pirate: Pirate): Promise<Pirate> { ... }
}
```

### 데이터 수정하기(Update)

계속해서 데이터를 수정하는 update 함수를 추가해보자

```typescript
// src/domain/db.ts

...

export class DB {
    constructor() { }

    update(pirate: Pirate): mongoose.Query<number> {
        return PirateModel.update({name: pirate.name}, {...pirate});
    }

    read(query: any): mongoose.DocumentQuery<Pirate[], Pirate> { ... }
    create(pirate: Pirate): Promise<Pirate> { ... }
}
```

Model.update 함수는 `mongoose.Query<number>` 를 반환하며
Query 인터페이스는 DocumentQuery 를 상속받으므로, 역시 Promise 타입을 상속받는다.
따라서 실제로 반환하는 것은 `Promise<number>` 형태라고 생각하면 된다.


### 데이터 삭제하기(Delete)

마지막으로 데이터를 수정하는 delete 함수를 추가해보자

```typescript
// src/domain/db.ts

...

export class DB {
    constructor() { }

    delete(pirate: Pirate): mongoose.Query<void> {
        return PirateModel.remove({name: pirate.name});
    }

    update(pirate: Pirate): mongoose.Query<number> { ... }
    read(query: any): mongoose.DocumentQuery<Pirate[], Pirate> { ... }
    create(pirate: Pirate): Promise<Pirate> { ... }
}
```

Model.delete 함수의 반환값은 update 와 같은데 대신 삭제한 개수를 반환하지 않는다. 
따라서 실제로 반환하는 것은 `Promise<void>` 형태라고 생각하면 편하다.


## 테스트

마지막으로 우리가 만든 DB 클래스를 이용하여 Document 를 다뤄(CRUD) 보자.

```typescript
// src/index.ts

import * as mongoose from 'mongoose';

import { Pirate, PirateModel } from './domain/pirate';
import { DB } from './domain/db';


let uri = 'mongodb://localhost/onepiece';
const connection: mongoose.MongooseThenable = mongoose.connect(uri);

const db = new DB();

let luffy = <Pirate>{name: 'luffy', bounty: 0.3, isEsper: true};

connection.then(() => {
  return db.create(luffy)
})
```

먼저 mongodb 에 mongoose.connect 를 이용하여 연결하고
반환되는 Promise ~~Thenable 은 then 을 포함하는 인터페이스~~ 를 connection 변수에 저장해둔다.

그리고 *luffy* 객체를 만들고 Pirate 로 타입캐스팅 한다. 

해당 객체를 mongodb 에 저장하기 위해 db.create() 에 파라미터로 전달하고 Promise 를 반환받아서 리턴한다. 
create가 Promise 를 리턴했기 때문에 해당 Promise 를 이용하여 작업을 이어나갈 수 있다.

그럼 데이터가 잘 저장되었는지 확인하기 위해 mongoDB 에서 name 이 *luffy* 인 Document 를 가져와보자.

```typescript
connection
.then(() => {
  return db.create(luffy)
})
.then((raw) => {
    db.read({name: raw.name}).then((pirates) => { 
        console.log('Created');
        console.log(pirates);
    });
})
```

db.create 는 Model.save 를 바로 리턴하고 Model.save 는 `Promise<Pirate>` 을 리턴한다.
이때 Pirate 은 저장된 Document 를 반환하므로
다음 then 의 콜백에서 raw 를 이용해 해당 Document 를 사용할 수 있다.

db.read 의 경우 Promise 를 리턴하지만 출력만 하면 되기 때문에 read 의 Promise 는 따로 리턴하지 않는다.
Promise 콜백(resolve) 는 리턴하지 않으면 `Promise<void>` 를 자동으로 리턴한다.

계속해서 db.update 함수를 이용해 luffy 의 현상금을 3천만에서 5억으로 올려보자.

```typescript
.then(() => {
  luffy.bounty = 5;
  return db.update(luffy);
})
.then((n) => {
  db.read({name: 'luffy'}).then((pirates) => { 
    console.log('Updated');
    console.log(pirates);
  });
})
```

db.update 도 Promise 를 리턴하는데 반환값은 Promise<number> 로
몇개의 Document 가 업데이트 되었는지만 반환해준다.
db.read 를 이용해 실제로 데이터가 다 수정되었는지도 확인해보았다.

마지막으로 db.delete 함수를 이용해 luffy 를 현상수배명단에서 삭제하자.

```typescript
.then(() => {
  return db.delete(luffy);
})
.then(() => {
    db.read({name: 'luffy'}).then((pirates) => { 
        console.log('Deleted');
        console.log(pirates);
    });
})
```

db.delete 도 Promise 를 반환하는데 Promise<void> 를 반환한다. 따라서 파라미터가 없는 것을 볼 수 있다.
db.read 를 이용해 실제로 데이터가 다 지워졌는지도 확인해보았다.

모든 작업을 마쳤으면 mongodb 커넥션을 닫아주자.

```typescript
.then(() => {
  mongoose.connection.close();
});
```

## 실행결과

실행은 여느때와 마찬가지로 `npm start` 해주면 되겠다.

```bash
$ npm start

> ts-tutorial@1.0.0 start /Users/haandol/git/ts-tutorial
> tsc; node ./build/index.js

Created
[ { _id: 5905f3efb1b5611171a5bccd,
name: 'luffy',
bounty: 0.3,
isEsper: true,
__v: 0 } ]

Updated
[ { _id: 5905f3efb1b5611171a5bccd,
name: 'luffy',
bounty: 5,
isEsper: true,
__v: 0 } ]

Deleted
[]
```

> 참고로 mongoose.mpromise 관련 warning 이 나오는데 ~~그냥 무시해도 상관없음~~
> typescript 에서는 Promise 를 global.Promise 로 대체할 수가 없어서 해결을 못했다.

## 마치며

넣고 싶은 내용은 많았지만 다 빼고 핵심적인 부분만 담으려고 했다.
이상한 내용은 댓글이나 티켓을 보내주시면 빠르게 수정하겠다.

다음은 typescript + socket.io 를 이용하여 아주 간단한 채팅서비스를 만들어보자.

----

[^1]: [ts-tutorial v3](https://github.com/haandol/ts-tutorial/tree/v3.0)
[^2]: [ts-tutorial v1](https://github.com/haandol/ts-tutorial/tree/v1.0)
