---
layout: post
title: 카카오 로그인으로 Amazon Cognito 연동하기
excerpt: Integrate Kakaotalk signin to Amazon Cognito Userpool
author: vincent
email: ldg55d@gmail.com
tags: kakao login signin cognito userpool serverless aws amazon
publish: true
---

## TL;DR

코드는 여기[^1].

> Update 2023-12-23. OIDC 방식으로 로그인을 하려면 이 코드[^3] 를 참고하면 된다.

## 시작하며

카카오 로그인으로 Amazon Cognito(이하 코그니토) 과 통합할 일이 있어서 작업내용을 공유한다.

## 설치하기

설치방법은 코드[^1] 의 README 를 읽고 그대로 따라하면 된다.

CDK 를 이용해서 코드를 배포하면 아래와 같은 리소스가 개인 계정에 배포된다.

![](https://github.com/haandol/cognito-kakao-example/raw/main/img/architecture.png)

## 인증흐름 설명

코그니토는 현재 구글, 아마존, 애플, OIDC 방식, SAML 방식 외에는 유저풀에서 인증을 지원하지 않는다.

따라서 사용자가 위에 언급되지 않는 방식으로 OAuth2 토큰을 가지고 로그인 요청시,

1. 토큰에 대한 검사 - API 를 통해 값을 가져오면서 validation 까지 한번에 해도 되고, 가능하다면 JWT 토큰을 decode 만 해서 값만 체크해도 된다.
2. 회원가입이 되어 있지 않다면 코그니토에 사용자를 생성
3. 회원가입이 되어 있다면 코그니토에 로그인후 인증키 전달

을 대신해주는 API 가 필요하다.

만약 토큰에 대한 검사가 필요하지 않다면, 회원가입에 대한 부분까지는 클라이언트에서 처리할 수 있다.

코드에서는 임의의 이메일로 쉽게 가입하지 못하도록, 위의 단계를 모두 서버쪽 API 를 통해서 처리하는 방법으로 구현한다.

### 회원가입

![](https://github.com/haandol/cognito-kakao-example/raw/main/img/signup.png)

카카오 로그인시에는 먼저 사용자의 카카오톡 액세스 토큰을 입력으로 API Gateway 를 통해 `kakao.ts` 를 호출한다.

입력받은 토큰으로 카카오API 를 이용하여 사용자의 이메일주소를 가져온다.

이후 이 이메일주소를 이용하여 코그니토에 사용자를 생성하게 된다.

해당 이메일 주소로 가입된적이 없다면 회원가입 단계를 진행하고, 이미 가입된 사용자라면 로그인 단계를 진행한다.

코그니토는 인증의 각 단계별로 람다를 호출할 수 있는 트리거를 지원한다.[^2]

일반 사용자가 회원가입시 코그니토 sdk 를 이용해서 `signUp()` 을 호출하면 계정 생성되기 전 **PreSignup** 트리거가 호출된다.

트리거가 없거나 트리거 호출결과 문제가 없다면, 가입시 사용되는 이메일이나 휴대폰을 인증하기 위해 *확인코드*가 발송된다.

이 때 받은 확인코드를 이용하여 confirm 을 하게 되면 **PostConfirmation** 트리거가 호출되며, 해당 트리거는 이미 계정생성이 완료된 뒤에 호출되므로 생성과는 무관하게 후처리를 하는 트리거이다.

해당 인증과정이 따로 필요없기 때문에, **PreSignup** 트리거에서 사용자에 대한 인증과 이메일주소에 대한 인증을 자동으로 진행하도록 플래그를 세팅해준다.

**PreSignup** 트리거에서 자동이메일 인증 설정을 하면, 이메일 전송을 하지 않고 계정이 생성된뒤 바로 **PostConfirmation** 트리거가 호출된다.

> 이 때, SDK 의 adminCreateUser를 이용해서 사용자를 생성하면 **PostConfirmaion** 트리거가 호출되지 않는다. 관리자가 직접 추가한 계정이므로 버그라기 보다는 디자인인 것 같다.

### 로그인

![](https://github.com/haandol/cognito-kakao-example/raw/main/img/signin.png)

위에서 설명한대로 이미 가입이 된 유저이거나, 계정을 생성하고 나면 로그인 단계를 진행한다.

카카오톡 사용자는 비밀번호를 입력하지 않고도 로그인을 해야하기 때문에 관리용 API 를 호출하여 랜덤한 비밀번호를 강제로 설정하고, 해당 비밀번호로 로그인을 하고 결과를 사용자에게 전달한다.

> 카카오로 가입한 사용자가 이메일로 로그인 시도시 pre-authentication 훅을 통해 로그인 시도가 막힌다.

## 테스트

코드의 web 폴더에서 `npm run dev` 등을 이용해서 리액트 웹을 실행하고 로그인을 테스트해보면 된다.

## OIDC

카카오도 OIDC 를 지원하므로, OIDC 방식으로 로그인을 하고 싶다면, 코드[^3] 을 참고하면 된다. OIDC 코드는 username 을 기준으로 사용자를 생성하고, 이메일을 요청하지 않는다.

전체적으로 OIDC 방식이 훨씬 간편하고 좋다.. 고 생각하지만, 카카오톡에서 email 을 oidc scope 에서 제공하지 않기 때문에, userinfo endpoint 를 통해 추가적으로 가져오는 과정이 필요하다.

따라서 카카오톡을 OIDC 로 연결할 경우 코드니토 유저풀에 email 을 alias 로 설정할 수 없기 때문에, 유저풀을 분리해주거나 별도의 로직을 연결해주어야 하는데 (post confirmation 훅을 이용하면 될 듯) 이런 부분을 잘 고민해서 선택하면 될 것 같다.

## 마치며

코드니토에서 UserPool 은 Authentication 을 위해서 사용하고, IdentityPool 은 Authorization 을 위해서 사용한다.

IdentityPool 을 이용해서도 API Gateway 에 대한 접근권한을 Authorize 해주어 API 를 호출할 수 있게 할 수 있다.

이러한 사용은 보통 IoT 에서 기기가 특정 리소스에 접근할때나, 클라이언트가 appsync 를 이용해서 graphql 을 직접 쿼리할때 (이경우는 이제 cognito sync 로 대체) 만 사용한다.

따라서 개별 사용자라는 개념이 필요하면 IdentityPool 이 아니라 UserPool 을 써야한다.

---

[^1]: [Cognito Kakao Example](https://github.com/haandol/cognito-kakao-example)
[^2]: [Lambda 트리거를 사용하여 사용자 풀 워크플로우 사용자 지정](https://docs.aws.amazon.com/ko_kr/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html)
[^3]: [Cognito Kakao Example OIDC](https://github.com/haandol/cognito-kakao-example/tree/oidc)
