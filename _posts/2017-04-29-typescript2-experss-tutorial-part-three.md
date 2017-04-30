---
layout: post
title: Typescript2 서버 튜토리얼 - 3/5
excerpt: Typescript + MongoDB
author: vincent
email: ldg55d@gmail.com
tags: typescript2, express, mongodb, mongoose, nodejs
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
개발모드에 *@types/패키지명* 으로 타입정의를 함께 설치하는 것도 잊지 말자.

```bash
$ npm install --save mongoose typescript
$ npm install --save-dev @types/mongoose @types/node
```

## 스키마 정의

mongodb 는 아래와 같이 Schema 를 이용해 Model을 생성하고, 해당 Model 을 이용하여 DB 에 데이터를 추가한다.

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

Typescript 를 사용하면 해당 함수가 스키마에 맞는 객체가 아니면 컴파일타임에 에러를 낸다.

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

### IPirate 정의하기

해적 정보를 저장하기 위해 src/domain/models.ts 를 만들고 IPirate 인터페이스를 추가하자

```bash
$ mkdir -p src/domain
$ touch models.ts
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

    create(pirate: Pirate: Promise<Pirate> {
        let p = new PirateModel(pirate);
        return p.save();
    }
}
```

*PirateModel* 은 mongoose.Model 을 상속받아 만들어지며
Model.save 는 해당 모델을 mongodb 에 Document 를 생성해준다.

이 때 반환된 값은 *Promise<T>* 의 제너릭 형태인데,
*<T>* 제너릭은 런타임에 타입을 지정할 수 있게 해주는 기법으로
Model 생성시 Pirate 로 우리가 지정해줬었다.

Promise 를 쓰지 않고 전통적인 콜백방식으로도 호출 할 수 있는데 아래와 같이 해주면 된다.
```typescript
let p = new PirateModel(pirate);
p.save((err, raw) => {
    console.log('Document is created successfully');
});
```

콜백방식은 여러 비동기 요청을 다룰 때 굉장히 복잡한 코드를 만들게 되므로 Promise 와 친해지는 것이 좋다.
최근에는 generator 나 async/awaits 를 이용한 코루틴 기법도 많이 사용되고 있다.

본 글에서는 mongoose 에서도 잘 지원하고 있고, 범용적으로 많이 쓰는 Promise 방법을 사용하기로 한다.


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

    create(pirate: Pirate: Promise<Pirate> { ... }
}
```

Model.find 함수는 *mongoose.DocumentQuery<Pirate[], Pirate>* 를 반환하며 DocumentQuery 인터페이스는 Promise 타입을 상속받는다.
따라서 실제로 반환하는 것은 *Promise<Pirate[], Pirate>* 형태라고 생각해도 무방하다.

마찬가지로 read 함수도 콜백을 이용해 리턴없이 구현할 수도 있다.

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

    create(pirate: Pirate: Promise<Pirate> { ... }
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
    create(pirate: Pirate: Promise<Pirate> { ... }
}
```

Model.update 함수는 *mongoose.Query<number>* 를 반환하며 Query 인터페이스는 DocumentQuery 를 상속받으므로, 역시 Promise 타입을 상속받는다.
따라서 실제로 반환하는 것은 *Promise<number>* 형태라고 생각해도 무방하다.


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
    create(pirate: Pirate: Promise<Pirate> { ... }
}
```

Model.delete 함수의 반환값은 update 와 같으며 Promise 타입이라고 보면 된다.
따라서 실제로 반환하는 것은 *Promise<void>* 형태라고 생각해도 무방하다.


## 테스트

모든 준비가 끝났다. 이제 우리가 만든 DB 클래스를 이용하여 루피의 정보를 CRUD 해보자.

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
반환되는 Promise(Thenable 은 then 을 포함하는 인터페이스)를 connection 변수에 저장해둔다.

그리고 luffy 객체를 만들고 Pirate 형태로 타입캐스팅 한다. 

해당 객체를 mongodb 에 저장하기 위해 db.create 에 파라미터로 전달하고 Promise 를 반환받아서 리턴해준다.
create가 Promise 를 리턴했기 때문에 해당 Promise 를 이용하여 작업을 이어나갈 수 있다.

그럼 이어서 name 이 'luffy' 인 해적목록을 가져와보자.

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

db.create 는 Model.save 를 바로 리턴하고 Model.save 는 *Promise<Pirate>* 을 리턴한다.
이때 Pirate 은 저장된 도큐먼트를 반환하므로 다음 then 의 콜백에서 raw 를 이용해 해당 도큐먼트를 사용할 수 있다.

db.read 의 경우 Promise 를 리턴하지만 출력만 하면 되기 때문에 read 의 Promise 는 따로 리턴하지 않는다.
Promise 콜백(resolve) 는 리턴하지 않으면 *Promise<void>* 를 자동으로 리턴한다.

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

db.update 도 Promise 를 리턴하는데 반환값은 Promise<number> 로 몇개의 도큐먼트가 업데이트 되었는지만 반환해준다.
사용하지 않을 파라미터(n) 는 생략해도 상관없다.
db.read 를 이용해 실제로 데이터가 다 수정되었는지도 확인해보았다.

이제 거의 끝이다.
db.delete 함수를 이용해 luffy 를 현상수배명단에서 삭제하자.

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

마지막으로 mongodb 커넥션을 닫아주자.

```typescript
.then(() => {
  mongoose.connection.close();
});
```

실행은 여느때와 마찬가지로 `npm start` 해주면 되겠다.

```bash
$ npm start

> cinnamon@1.0.0 start /Users/haandol/git/ts-tutorial
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

참고로 mongoose.mpromise 관련 warning 이 나오는데 typescript 에서는 Promise 를 global.Promise 로 대체할 수가 없어서 해결을 못했다.
~~그냥 무시해도 상관없긴하지만~~

## 마치며

이런저런 기능이나 다양한 Promise 활용법도 넣으려고 했는데 코드가 복잡해져서 다 빼고 핵심적인 부분만 담았다.

이상한 점은 댓글이나 QnA 로 티켓을 만들어주면 빠르게 반영하도록 하겠다.

----

[^1]: [ts-tutorial v3](https://github.com/haandol/ts-tutorial/tree/v3.0)
[^2]: [ts-tutorial v1](https://github.com/haandol/ts-tutorial/tree/v1.0)
