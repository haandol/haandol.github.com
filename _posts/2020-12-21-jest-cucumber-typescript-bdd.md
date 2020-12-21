---
layout: post
title: Jest+cucumber 로 BDD 환경 구축하기
excerpt: Do BDD using jest-cucumber and typescript
author: vincent
email: ldg55d@gmail.com
tags: bdd jest cucumber jest-cucumber typescript ts-jest gherkin
publish: true
---

## TL;DR

코드는 여기[^1].

BDD 는 이벤트 스토밍 결과를 가지고 개발을 진행할 때 상당히 유용하게 쓸 수 있다.

## 시작하며

프로젝트를 시작할때 범위를 정하는 것이 중요하다. 빠르게 범위를 정하기 위해서는 사용자 스토리가 여로모로 좋은 도구라고 생각한다.

다만 사용자 스토리를 쓰라고 하면, 사람마다 제각각으로 쓰기 때문에 요구사항을 정형화해서 관리할 필요가 느껴졌다.

몇년전 인수테스트 때 썼던 lettuce, pycurracy 가 기억나서 그 형태로 스토리를 작성하면 좋을 것 같다고 생각했다.
(BDD 에서 쓰는 gherkin 문법이다.)

요즘 Typescript 로 작업을 주로 하고 있기 때문에 cucumber 를 쓰기로 했고,
CDK 의 기본 테스트 프레임워크가 jest 라서 결국 `jest + cucumber + typescript` 로 된 BDD 테스트 환경을 마련해보기로 했다.

원래는 cucumber.js 를 쓰려고 했는데 jest-cucumber[^2] 가 좀 더 인터페이스가 편해서 jest-cucumber 로 구성해봤다.

## 설치하기

설치가 안되어 있다면 typescript, jest, ts-jest 를 global 로 설치해준다.

```bash
$ npm i -g typescript ts-jest jest @types/node
```

npm, typescript, jest 를 각각 init 해준다.

```bash
$ npm init
$ tsc --init
$ jest --init

$ ls
jest.config.ts
package.json
tsconfig.json
```

jest.config.ts 의 내용을 다음과 같이 수정해준다.
testMatch 는 테스트 타겟이 되는 파일들을 지정해주는 부분이고, transform 은 해당 파일들을 실행할때 실행명령이라고 보면 된다.
```typescript
export default {
  clearMocks: true,
  coverageProvider: "v8",
  testEnvironment: "node",
  testMatch: [
    "**/__tests__/**/*.[jt]s?(x)",
    "**/?(*.)+(spec|test|steps).[tj]s?(x)"
  ],
  transform: {
    "^.+\\.tsx?$": "ts-jest"
  },
};
```

transform 에 사용할 ts-jest 만 설치해주면 끝.
ts-jest 는 ts-node 처럼 jest 를 ts 파일로 바로 테스트 할 수 있게 해준다.

```bash
$ npm i --save ts-jest 
```

이 후 jest-cucumber[^2] 의 예제를 똑같이 하되 파일만 ts 파일로 작성해주면 된다.

사용법 및 설정이 완료된 내용은 코드[^1] 에 있다.

## 마치며

이벤트 스토밍에도 잠깐 언급 했지만, 이벤트 스토밍과 사용자 스토리가 잘 맞는거 같다.

그리고 사용자 스토리를 기술태스크로 만들때나 이벤트 스토밍의 프로세스 모델링 단계에서 BDD 의 example mapping 도 꽤 잘 어울리는 것 같다.

----

[^1]: [jest-cucumber tutorial](https://github.com/haandol/jest-cucumber-tutorial)
[^2]: [jest-cucumber](https://www.npmjs.com/package/jest-cucumber)