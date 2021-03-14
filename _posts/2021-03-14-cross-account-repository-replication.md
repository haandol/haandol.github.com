---
layout: post
title: 다중 어카운트 아마존 코드커밋 레포지토리 복제하기
excerpt: Replicate Amazon Codecommit repositories across accounts
author: vincent
email: ldg55d@gmail.com
tags: codecommit replication croca repository cross-account
publish: true
---

## TL;DR

코드는 여기[^1].

## 시작하며

예전에 단일 어카운트 내에서 여러 리젼에 퍼져있는 레포지토리들에 대해서 레플리케이션 할 일이 있어서 코드[^2]를 작성한 적이 있었다.

하지만 엔터프라이즈에서는 단일 어카운트보다 다중어카운트 환경을 사용하게 된다. 개발용 어카운트에서 `release` 브랜치에 푸시를 하면, 프로덕션 어카운트에서 해당 내용을 CI/CD 를 통해 빌드하고 배포하는 방식이 가장 대표적인 예일 것이다.

본 글의 코드[^1]는 이러한 시나리오를 처리할 수 있게, 다중 어카운트 상에서 레포지토리간의 동기화를 처리할 수 있는 부분만 제공한다.

각 어카운트의 코드파이프라인은 레포지토리에 사용자가 직접 푸시하는 경우와 동일하게 구성하면 된다.

## 설치하기

설치방법은 코드[^1] 의 README 를 읽고 그대로 따라하면 된다.

CDK 를 이용해서 코드를 배포하면 아래와 같은 리소스가 개인 계정에 배포된다.

![](https://github.com/haandol/croca/raw/main/img/architecture.png)

## 마치며

글이 짧은 것은 이 솔루션을 쓸 사람이 국내에는 많지 않을거라고 생각되어서이다.

github 를 레포로 이용하면 굳이 본 글의 코드를 쓸 필요가 없는데, 국내에는 거의 github 를 코드베이스로 많이 쓰고 있다.

이 경우, 개발 계정은 main 브랜치를 기준으로 파이프라인을 구성하고, 프로덕션 계정은 release 브랜치 기준으로 파이프라인 구성하면, 굳이 어카운트간에 이벤트를 전송할 필요가 없다.

----

[^1]: [Croca](https://github.com/haandol/croca)
[^2]: [Picapica](https://github.com/haandol/croca)