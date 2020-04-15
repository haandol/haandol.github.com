---
layout: post
title: AWS ECS + CodePipeline(CodeDeploy) 트러블슈팅
excerpt: ECS CodePipeline(CodeDeploy) Trouble shooting
author: vincent
email: ldg55d@gmail.com
tags: aws codepipeline ecs troubleshooting bug-report bug
publish: true
---

## TL;DR

`The provided role does not have sufficient permissions to access CodeDeploy`

ECS Fargate 로 CodeDeploy 를 쓸때 권한이 없다고 하면 `taskdef.json`, `appspec.yaml`, `imageDetail.json` 이 정상적인 값으로 생성되었는지 먼저 확인해보자.

## 시작하며

![](/assets/img/20200416/fargate-cicd.png)

요새 대략 위와 같은 작업을 CDK 를 이용해서 구성하고 있는데 삽질을 많이 하게 된다.

관련된 내용은 시간이 나면 정리하고, 오늘은 삽질을 많이 했던 부분만 공유해본다.

위의 구성을 만들때 다른건 다 쉬웠는데, 아래의 3개가 대부분의 시간을 잡아먹었다.

1. CodePipline 의 CodeDeploy 스테이지에서 ECS 로 디플로이 할 때, `The provided role does not have sufficient permissions to access CodeDeploy` 가 나오는 문제
2. CodeDeploy ECS 로 배포할때 AllAtOnce 가 아니라 Canary 옵션으로 배포하면 배포실패하는 문제(에러메시지가 뭐였는지는 잘 모르겠다)
3. API Gateway 에서 ALB 로 Proxy 연결시 `Internal Server Error` 가 나오는 문제 (ALB 로 접근하면 문제가 없이 잘 출력되고, 클라우드 워치에도 제대로 된 로그가 안나옴)

이 글에서는 1번만 간단하게 설명한다.

## 문제상황

내 경우는 Docker 이미지를 빌드하고 결과를 아티팩트로 전달하는데 이 때, 이미지 주소가 잘못되어서 생긴 문제였다.

CodeDeploy 는 빌드 과정에서 *taskdef.json* 에 있는 *placeholder*(여기서는 <IMAGE>) *imageDetail.json* 에 들어있는 이미지 주소로 대체해서 ECS Fargate Task 를 배포한다. 

따라서 `prototyping.aws.com/myapp:14` 를 빌드했다고 하면 해당 이미지를 여기[^1] 에 나온대로 `imageDetail.json` 파일로 저장해서 `containerImageInputs` 파라미터로 전달해줘야 한다.

```typescript
    const devDeployStage = pipeline.addStage({ stageName: 'DevDeploy' });
    devDeployStage.addAction(new cpactions.CodeDeployEcsDeployAction({
      actionName: `DevDeploy`,
      deploymentGroup,
      taskDefinitionTemplateFile: codepipeline.ArtifactPath.artifactPath(output.artifactName!, 'taskdef.json'),
      appSpecTemplateFile: codepipeline.ArtifactPath.artifactPath(output.artifactName!, 'appspec.yaml'),
      containerImageInputs: [
        {
          input: output,
          taskDefinitionPlaceholder: 'IMAGE'
        },
      ],
    }));
```

위의 코드에서 `output` artifact 는  *taskdef.json*, *appspec.yaml*, 그리고 *imageDetail.json* 이 루트위치에 들어있다.

> appspec.yaml 의 기본값 확장자는 yml 이 아니라 yaml 이다. 참고하자.

이 때 *imageDetail.json* 안에 들어가는 이미지주소가 존재하지 않는 주소이면, 예를 들어 tag 가 `14` 가 아니라 `latest` 라던가, *The provided role does not have sufficient permissions to access CodeDeploy* 코드파이프라인 상에서 이런 에러가 발생한다.

## 해결방법

대부분 템플릿 설정파일을 만들어두고, sed 등을 써서 PLACEHOLDER 를 replace 하는 식으로 설정파일들을 완성하게 될텐데, 이 과정에서 문제가 생기는 경우가 많다.

*output* 아티팩트를 작성할때 위의 3개 파일값을 echo 로 찍어주고 값이 제대로 들어가있는지 확인해보자.

## 마치며

구현이 급하면 매뉴얼을 잘 안읽게 되는데, 프레임워크 등을 다룰 때는 try & error 방식이 더 오래걸리는 경우가 많다.
급할수록 마음을 좀 가다듬고 매뉴얼을 잘 읽어보자.

----

[^1]: [File Reference ECS BlueGreen](https://docs.aws.amazon.com/ko_kr/codepipeline/latest/userguide/file-reference.html#file-reference-ecs-bluegreen)