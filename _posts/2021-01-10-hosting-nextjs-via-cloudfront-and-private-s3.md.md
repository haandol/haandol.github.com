---
layout: post
title: Nextjs 프로젝트 Cloudfront + Private S3 로 호스팅하기
excerpt: Hosting Nextjs project via Cloudfront and private S3
author: haandol
email: ldg55d@gmail.com
tags: nextjs react cloudfront s3 hosting cdk origin-access-identity oai
publish: true
---

## TL;DR

코드는 여기[^1].

Origin Access Identity(OAI)[^2] 를 이용하면 S3 콘텐츠를 public open 하지 않아도 호스팅 할 수 있다.

## 시작하며

최근 작업중 nextjs 를 s3 로 호스팅 해야 할 일이 생겼는데, 모든 퍼블릭 엑세스를 블록해야한다는 제약이 있었다.

Origin Access Identity(OAI) 를 사용하면 S3 에 대한 퍼블릭엑세스를 허용하지 않고도 리액트 웹 호스팅이 가능하다.

OAI 를 사용하는 법은 다른 링크[^3] 들에도 많이 있기 때문에 딱히 소개할 건 없고,

이 글에서는 OAI 를 CI/CD 와 합쳐서 제공하는 기능을 구현한 내용을 소개한다.

## 설치하기

CDK 를 이용해서 코드[^1]를 배포하면 아래와 같은 리소스가 배포된다.

![](/assets/img/2021/0110/architecture.png)

아무 수정없이 배포만 한 뒤 코드파이프라인 콘솔에 가면 실패화면이 나오는데 config.ts 에 지정된 Codecommit 레포지토리가 없어서 그렇다.

샘플 프로젝트로 쓸 수 있는 nextjs 코드[^4] 를 clone 하고 codecommit 레포를 만들어서 푸시해준다.

```bash
$ aws codecommit create-repository --repository-name nextjs-example
$ git clone https://github.com/haandol/nextjs-example
$ cd nextjs-example
$ git remote set-url origin codecommit::ap-northeast-2://nextjs-example
$ git push
```

nextjs-example 에 푸시할 때마다 파이프라인이 트리거 되면서 cloudfront invalidation 까지 완료가 될 것이다.

![](/assets/img/2021/0110/pipeline.png)

이 후 Cloudformaion 의 Output 에 표시된 DomainName 으로 접속하면 정상적인 react web page 를 볼 수 있다.

![](/assets/img/2021/0110/demo.png)

----

[^1]: [nextjs s3 deploy block](https://github.com/haandol/nextjs-s3-deploy-block)
[^2]: [원본 액세스 ID를 사용하여 Amazon S3 콘텐츠에 대한 액세스 제한](https://docs.aws.amazon.com/ko_kr/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
[^3]: [AWS CLI로 Amazon CloudFront OAI 설정하기](https://dev.classmethod.jp/articles/aws-cli-cloudfront-oai-kr/)
[^4]: [nextjs-example](https://github.com/haandol/nextjs-example)