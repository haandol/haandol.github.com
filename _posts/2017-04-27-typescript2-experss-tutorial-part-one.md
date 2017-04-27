---
layout: post
title: Typescript2 + Express + MongoDB 튜토리얼
excerpt: typescript2 로 만드는 서버 튜토리얼
author: vincent
email: ldg55d@gmail.com
tags: typescript2, express, mongodb, mongoose, nodejs
publish: true
---

## TL;DR

 * 예제마다 뭔가 많이 달라서 뭘로 해야할지 모르겠다구요?
``` 정상입니다. 설정이 제일 쉬워보이는거 정해서 하세요. ```

 * 개발환경 세팅에 손이 많이가서 빡친다구요?
``` 정상입니다. 당을 섭취하면서 하다보면 익숙해집니다. ```


## 시작하며

Python 으로만 서버 개발하다가 지난주부터 nodejs 를 공부하게 되었는데 너무나 다양한 (형태의) 예제들이 오히려 압박이었다.

본 글은 나처럼 다른(Python) 언어로 서버 개발하다가 넘어오는 개발자들을 위해(즉 node 환경에 익숙하지 않은 서버개발자) 작성했다.

글 순서는 아래와 같으며, 전체 시리즈의 끝에는 간단한 채팅 서비스를 만들게 될 것이다.

1. hello world (당연하게도)
1. express + typescript 로 간단한 REST API 개발
1. mongoose + typescript 로 앞서 만든 REST API 에 CRUD 추가
1. socket.io + typescript 로 실시간으로 여러 소스에서 CRUD 기능 추가
1. 앞선 내용을 다 합쳐서 간단한 채팅서버 개발

node 기본과 Typescript 는 알고 있다고 가정하고 진행하겠다.

내 개발 환경은 osx + terminal + vim 이며 IDE 쓰는 사람은 알아서...

## 프로젝트 생성 및 설정

프로젝트 폴더를 생성한다.

```bash
$ mkdir cinnamon
$ cd cinnamon
```

typescript 를 이용해 서버를 돌리려면 무조건 2개를 init 해줘야한다.

**npm** 과 **tsc** 이다. npm 은 패키지 매니저이고 tsc 는 타입스크립트 컴파일러다.

이건 무조건 해야하므로 걍 받아들여라.

### NPM: package.json

최근 python 서버에는 가상환경(virtualenv 모듈) 이 필수고 node 도 마찬가지다.

node 에서 pip 에 해당하는 패키지 매니저는 **npm** 이며 requirements.txt 의 역할을 하는 것은 **package.json** 이다.

npm 환경을 설정하기 위해 아래 명령을 입력한다.

```bash
$ npm init
```

해당 명령은 package.json 파일을 생성해준다. 일단은 입력할 내용이 없다. 엔터만 치면 된다.

package.json 의 모양은 다음과 같을 것이다.

```json
{
    "name": "cinnamon",
        "version": "1.0.0",
        "description": "",
        "main": "index.js",
        "scripts": {
            "test": "echo \"Error: no test specified\" && exit 1"
        },
        "author": "",
        "license": "ISC"
}
```

## TSC: tsconfig.json

이제 타입스크립트를 설지하자.

```bash
$ npm install --save typescript @types/node
```

*--save* 옵션은 package.json 에 자동으로 설치되는 패키지의 의존성을 붙여준다.
*@types/패키지* 은 패키지의 선언(declaration) 을 typescript 에서 사용할 수 있게 해준다.
1.x 에서는 tsd 나 typings 같은 패키지로 복잡하게 했었는데 2.x 에서는 *@types/패키지* 를 npm install 하면 끝난다.

타입스크립트는 TS 형태를 JS 로 컴파일하는 방식이며 컴파일시 **tsconfig.json** 파일을 참조한다.

이제 tsconfig.json 을 만들어보자. 아래 명령어 하나로 끝난다.

```bash
$ tsc --init
```

이제 tsconfig.json 가 생겼다. 파일내용은 다음과 같을 것이다.

outDir 은 직접 추가해주면 되는데 아래에서 설명하겠다.

```json
{
    "compilerOptions": {
        "outDir": "build",      // add this line manually
        "module": "commonjs",
        "target": "es5",
        "noImplicitAny": false,
        "sourceMap": false
    }
}
```

다른건 신경안써도 되고 일단 target 만 보자.

위에서 말했듯 TS 는 JS로 컴파일을 하는데, 어떤 ES 표준버전으로 컴파일 할지 결정할 수 있다.
node 6.4 이상은 es2015 를 지원하기 때문에[^1] node 구 버전을 쓰거나 프론트엔드 작업을 할 게 아니면 굳이 es5 로 컴파일을 할 이유가 없다.
es2015 에는 Promise, Generator, Iterator 같은 편리한 기능들이 많이 있기 때문에 평소에는 *es2015*로 설정해주면 된다.

다만 여기서는 컴파일된 코드와의 차이를 보기 위해 es5 를 그대로 놔두겠다.

마지막으로 outDir 옵션을 추가해주자. 맨 윗줄에 추가한 이유는 *쉼표(,)* 때문에 잘못입력할까봐 그런것인데 위치는 사실 상관없다.

outDir 은 컴파일된 JS 파일이 어디에 위치할지 결정해주는 것으로 없으면 소스파일(.ts) 과 동일한 폴더로 위치하게 된다.
이렇게 ts 파일과 js 파일이 섞이면 굉장히 보기 안좋기 때문에, 특별한 이유가 없으면 outDir 로 ts 와 js 위치를 구분해주는 것이 정신건강에 좋다.

## Hello world!

typescript 는 src 폴더아래에 위치시키는 것이 관례이다. 스타일가이드를 잘 지키면 여러모로 편리하다. src 폴더를 만들자.

```bash
$ mkdir src
```

이제 첫 ts 파일을 만들어보자.

```bash
$ touch index.ts
```

좋아하는 편집기로 아래 내용을 index.ts 에 입력한다.

```typescript
class Greeter {
    constructor(public name: string) { }

    greet() {
        return `Hello world, ${this.name}!!`;
    }
};

const greeter = new Greeter("Vincent");
console.log(greeter.greet());
```

*es6* 에 추가된 *class* 와 *formatting* 를 써야 구분이 될 것 같아서 다소 위와 같은 복잡한 hello world 예제를 작성했다.

이제 ts 파일을 tsc 를 이용해 컴파일 해보자.

```bash
$ tsc
```

컴파일을 하면 *build* 폴더가 생기고 안에 index.js 파일이 es5 형태로(엄청 복잡함) 컴파일 되어 있을 것이다.

현재까지의 구조는 아래와 같을 것이다.

```bash
├── build
│   └── index.js
├── package.json
├── src
│   └── index.ts
└── tsconfig.json
```

생성된 파일을 실행해보자.

```bash
$ node build/index.js
Hello world, Vincent!!
```

잘 출력되는 것을 볼 수 있다.

## npm start

NPM 은 패키지 매니저이지만 간단한 빌드명령도 수행할 수 있다.

```bash
$ npm install
npm WARN cinnamon@1.0.0 No description
npm WARN cinnamon@1.0.0 No repository field.

$ npm test
> cinnamon@1.0.0 test /Users/haandol/git/cinnamon
> echo "Error: no test specified" && exit 1

Error: no test specified
npm ERR! Test failed.  See above for more details.
```

*npm test* 명령은 어디서 온것인가?
아까 작성된 package.json 의 **scripts** 필드를 보면 **test** 필드가 있는데 필드명은 npm 파라미터이고 값은 셸에서 실행되는 명령어이다.
```json
...
"scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
},
...
```

대부분의 인터넷 예제들은 *npm start* 를 이용해 실행되도록 설정되어 있는데 우리도 해보자.

우리는 tsc 를 이용하여 typescript 를 컴파일한 뒤 node 를 이용해 index.js 를 실행하기만 하면 된다.

아래와 같이 scripts 필드에 *start* 를 추가하고 저장한다.

```json
...
"scripts": {
    "start": "tsc; node ./build/index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
},
...
```

제대로 적용이 되는지 확인하기 위해 index.js 를 수정해보자.

```typescript
class Greeter {
    constructor(public name: string) { }

    greet() {
        return `Hello world, ${this.name}!!`;
    }

    // Add hugeGreet method
    hugeGreet() {
        return `HELLO WORLD, ${this.name}!!!!!`;
    }
};

const greeter = new Greeter("Vincent");
console.log(greeter.hugeGreet());
```

이제 *npm start* 명령만 입력하면 자동으로 index.ts 를 JS 로 컴파일하고 해당 파일을 실행하는 것을 볼 수 있다.

```bash
$ npm start

> cinnamon@1.0.0 start /Users/haandol/git/cinnamon
> tsc; node ./build/index.js

HELLO WORLD, Vincent!!!!!
```

## 마치며

Typescript 는 기본적으로 서버 뿐만이 아니라 Angular, React, React Native 등의 다양한 환경에서 쓸 수 있게 범용으로 만든 (MS 니까..) 언어이므로
튜토리얼도 너무나 다양한 내용을 다루고 있어서 혼란스러웠다.

구글 검색에 나온 다른 예제들 역시 대부분 프론트 개발자가 풀스택을 하면서 쓴 글이라 마찬가지로 돌잔치에서 돌잡이하는 기분이었다. ~뭘 잡아도 뭔지도 모르고 잡음~

위 내용은 막 Node 개발을 시작한 서버 개발자로서 내가 궁금해하던 내용들만 짚어서 만들었기 때문에 다른 부분은 다른 예제들을 찾아보며 공부하면 될 것 같다.

짧게 쓴다고 썼는데도 겁나 기네...

----

[^1]: [node.green](http://node.green/)
