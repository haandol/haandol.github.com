---
layout: post
title: 세이지메이커 파이프라인으로 YOLOv8 파인튜닝 해보기
excerpt: Fine-tune YOLOv8 using AWS Sagemaker Pipeline
author: vincent
email: ldg55d@gmail.com
tags: yolov8 sagemaker-pipeline sagemaker aws fintune object-detection mot
publish: true
---

## TL;DR

코드는 여기[^1]

## 시작하며

옛날에는 세이지메이커 파이프라인 대신 스텝펑션으로 파이프라인을 구성해서 썼지만, 세이지메이커 스튜디오와 세이지메이커 파이프라인이 생기면서 이쪽을 이용해서 MLOps 파이프라인을 구성하는 것이 대세가 되고 있다.

개인적으로 세이지메이커 스튜디오의 몇몇 단점들 때문에 쓰기 싫어서 미루고 미루다가 결국 흐름에 떠밀려 공부를 하게 되었고, 샘플만들고 공부한건 몇달전이지만 이제서야 정리해본다.

본 글에서는 세이지메이커 파이프라인을 이용해서 YOLOv8 모델을 피카츄를 찾을 수 있는 모델로 파인튜닝하는 예제를 보여준다.

## 세이지메이커 스튜디오

세이지메이커 파이프라인을 쓰려면 반드시 세이지메이커 스튜디오를 설정해야 한다.

세이지메이커 스튜디오를 콘솔에서 직접 만들거나 다음[^2] CDK 프로젝트를 배포해서 만들 수 있다.

CDK 프로젝트로 배포후, 노트북을 실행하기 전 콘솔에서 README 에 있는 **Enable Project templates** 단계 진행해야 배포용 Project 를 생성할 수 있다.

이렇게 스튜디오가 강제된다는 점이, 개인적으로 생각하는 세이지메이커 파이프라인의 가장 큰 단점이다.

세이지메이커 스튜디오 안에서 만든 몇몇 리소스들은 (예, 파이프라인, 모델 레지스트리) AWS 콘솔에서 확인할 수 없다.

따라서 해당 리소스들을 확인 하려면 반드시 세이지메이커 스튜디오나 AWS CLI를 이용해야 한다. 운영팀과 모델 개발팀이 분리되어 있는 경우에 운영팀 입장에서는 상당히 불편한 부분이다. (즉, DS 쓰라고 만들어둔 툴을 운영팀도 쓸 줄 알아야 한다.)

## 코드 다운로드

세이지메이커 스튜디오를 열고 터미널을 열어서 다음 명령어를 실행한다.

```bash
git clone https://github.com/haandol/sagemaker-pipeline-yolov8-example
```

왼쪽 파일 탐색기에서 `sagemaker-pipeline-yolov8-example` 폴더아래에 `notebook/pikachu_sagemaker.ipynb` 노트북을 더블클릭해서 실행한다.

데이터 다운로드부터 시작해서 모델 훈련까지 모든 과정을 노트북에서 실행할 수 있다.

### 빌드용 이미지 배포

세이지메이커 파이프라인을 VPC 에 붙여서 실행하는 경우 ECR 이미지만 쓸 수 있다.

그리고 세이지메이커 스튜디오에는 도커가 없다.

따라서 Cloud9 이나 로컬에서 도커를 이용해서 빌드용 이미지를 만들어서 ECR 에 배포해야 한다.

```bash
cd sagemaker-pipeline-yolov8-example/train
./build_and_push
```

### 사용한 데이터

파인튜닝에 사용할 데이터는 Roboflow 의 [Pikachu dataset](https://universe.roboflow.com/oklahoma-state-university-jyn38/pikachu-detection/dataset/1) 이다.

코드에 포함된 노트북을 통해 다운받고 S3 에 업로드할 수 있다.

## 세이지메이커 파이프라인

현재 세이지메이커 파이프라인을 이용한 MLOps 베스트 프랙티스는 아래와 그림과 같으며

- 모델 빌드
- 모델 배포

2개의 파트로 되어 있다.

<img src="https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/01/12/SageMaker-Pipelines-Architecture.jpg" alt="SageMaker Pipelines Architecture" style="zoom:50%;" />

위의 노트북을 실행하면 좌측 모델 빌드에 관련된 세이지메이커 파이프라인이 생성되고 실행된다.

```bash
...
execution = pipeline.start()
execution.describe()
```

학습은 `m5.xlarge` 에서 진행되며 대략 20분정도 소요된다.

## 파이프라인 확인

세이지메이커 스튜디오 좌측 사이드바의 **홈버튼->Pipelines->pikachu-yolo-pipeline** 로 이동하여 파이프라인 실행 상태를 확인할 수 있다.

## 배포용 파이프라인 생성

<img src="https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/01/12/SageMaker-Pipelines-Architecture.jpg" alt="SageMaker Pipelines Architecture" style="zoom:50%;" />

우측의 배포용 파이프라인 생성은 스튜디오의 프로젝트를 통해 하면 쉽게 할 수 있다.
세이지메이커 프로젝트는 원하는 형태의 인프라 템플릿과 설정을 미리 저장해두고 재사용할 수 있게 도와주는 기능이다.

1. 세이지메이커 스튜디오 좌측 사이드바의 **홈버튼->Deployments->Projects** 로 이동하여
   **Sagemaker templates** 탭에서, **Model Deployments** 템플릿을 클릭하고 **Select project template** 버튼을 클릭한다.

2. **Name** 에 pikachu-deployments 를 입력하고, **Project template parameters** 에는 **PikachuYOLOv8** 을 입력해서 프로젝트를 생성한다.

생성후 사이드바의 **Deployments->Projects** 메뉴에 가보면 프로젝트가 생성되어 있을 것이다.

해당 프로젝트는 코드커밋 레포지토리 및 [코드파이프라인](https://ap-northeast-2.console.aws.amazon.com/codesuite/codepipeline/pipelines?region=ap-northeast-2)을 생성해준다. (그렇다, 세이지메이커 파이프라인이 아니다. 배포는 코드파이프라인을 쓴다..)

이렇게 생성된 배포 파이프라인은 모델레포지토리에서 모델상태를 변경하거나, 코드커밋 레포지토리에 변경이 발생하면 자동으로 실행된다.

본 글에서는 모델 레포지토리에서 상태변경으로만 파이프라인을 실행해보겠지만, 필요하면 프로젝트가 생성해준 레포지토리를 클론받아서 코드를 직접 수정하고 배포할 수 있다.

## 모델 승인

세이지메이커 스튜디오 좌측 사이드바의 **홈버튼->Models->Model Registry** 로 이동하여 **PikachuYOLOv8** 을 선택하고 가장 최근에 등록된 모델의 Status 를 Approved 로 변경해준다.

위에서 배포한 [배포용 코드파이프라인](https://ap-northeast-2.console.aws.amazon.com/codesuite/codepipeline/pipelines?region=ap-northeast-2)으로 가보면 코드가 자동으로 배포되는 것을 확인할 수 있다.

기본 설정은 가장 최근에 생성된 모델중 Approved 상태인 모델을 배포한다.

## 세이지메이커 엔드포인트 테스트

노트북 하단에 엔드포인트를 통해 테스트 하는 코드가 있다. 해당코드로 테스트 해보자.

## 마치며

모델 레지스트리에 등록하는 부분까지는 세이지메이커 스튜디오 및 세이지메이커 파이프라인에서 진행하고,

모델 레지스트리에 등록된 모델을 배포하는 부분은 코드파이프라인을 통해 진행한다는 점이 약간 헷갈릴 수 있지만

그래도, 해당 내용을 직접 만드는거에 비해서 세이지메이커 파이프라인을 쓰면 MLOps 프로세스를 쉽게 만들고 관리할 수 있다.

---

[^1]: [Sagemaker Pipeline YOLOv8 Example](https://github.com/haandol/sagemaker-custom-docker-yolov8)
[^2]: [CDk Sagemaer Studio](https://github.com/haandol/cdk-sagemaker-studio)
