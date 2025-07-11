---
layout: post
title: 세이지메이커 그라운드 트루스로 바운딩박스 라벨링 하기
excerpt: Draw bounding box using Sagemaker Ground Truth
author: haandol
email: ldg55d@gmail.com
tags: aws sagemaker ground-truth object-detection bounding-box bbox labeling deeplearning yolo
publish: true
---

## TL;DR

코드는 여기[^1]. Jupyter Notebook 이므로 위에서부터 읽어가며 따라하면 된다.

여러 사람과 함께 바운딩박스를 그려야 할 때는 Ground Truth 가 가장 좋은 선택이다.(사실 혼자서도 좋다.)

## 시작하며

Yolo, SSD, FasterRCNN 등의 객체 탐지(Object Detection) 모델 학습을 위해 데이터를 만들면 반드시 바운딩 박스를 그려야 한다.

오픈 소스 툴들도 몇몇 보이곤 하지만 여러 사람과 함께 데이터를 쌓고 처리하기에 가장 편리한 툴은 Sagemaker Ground Truth(이하 GT) 라고 생각한다.

이 글에서는 GT를 이용하여 개와 고양이 이미지에 바운딩 박스를 그리는 과정(라벨링)을 다룬다.

## 세이지메이커 그라운드 트루스

![](/assets/img/20200430/sagemaker.png)

세이지메이커 콘솔에 들어가보면 위와 같은 메뉴들을 볼 수 있다. 앞에서부터 순서대로 

1. 데이터 준비 (GT)
2. 학습 (인스턴스 / 트레이닝 잡)
3. 배포 (엔드포인트 / 마켓플레이스)

와 같은 역할을 담당하는 서비스들이다.

세이지메이커의 각 서비스는 데이터가 S3 에 업로드 되어 있다고 가정한다.

일단 S3 에 데이터를 업로드하고 나면 라벨을 달고, 해당 데이터로 학습을 한 뒤에, 엔드포인트를 통해 REST API 로 배포하는 모든 과정을 세이지메이커를 통해 진행할 수 있다.

이 글에서 다루는 모든 내용은 코드[^1] 에 쥬피터 노트북형태로 작성되어 있기 때문에, 본 글에서는 중요한 내용 위주로 간략히 설명한다.

## 이미지 S3에 업로드하기

본 튜토리얼을 위해 images 폴더 아래에 8장을 넣어두었다.
이미지는 개, 고양이 그리고 개도 고양이도 아닌 동물 사진들로 구성되어있다.

앞서 언급했듯이 세이지메이커의 모든 작업은 S3 에 데이터를 올려둔 상태라고 가정한다.

따라서 준비된 이미지들을 원하는 버킷에 업로드 해준다.

코드에서는 세이지메이커가 계정마다 기본으로 생성해주는 버킷(Bucket)을 사용한다고 가정했다.
기본 버킷이름은 *sagemaker-리젼-아이디* 의 형태를 가진다

```python
from glob import glob
import boto3
import sagemaker

session = boto3.session.Session()
BUCKET_NAME = sagemaker.Session().default_bucket()
s3 = session.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

for filepath in glob("./images/*.jpg"):
    filename = filepath.rsplit("/", 1)[1]
    print(f"upload file: {filename}")
    bucket.upload_file(filepath, f"images/{filename}")
```

기본 버킷 아래의 *images* 폴더 밑에 이미지들이 저장된다.

## manifest 파일 생성하기

GT 라벨링 잡(Labeling Job)은 S3 에 업로드된 *manifest* 라고 부르는 파일을 입력값으로 받는다.

*manifest* 파일 각 행이 json dictionary 형태로된 텍스트파일이다.
각 행은 아래와 같이 *source-ref* 를 키로 하고 값은 이미지의 s3 주소를 가진다.

```json
{"source-ref": "s3://sagemaker-ap-northeast-2-929831892372/images/8.jpg"}
```

앞서 업로드한 이미지들의 정보를 가지고 *catdog.manifest* 파일을 만들고 s3 에 업로드 한다.

```python
os.makedirs(f"manifests", exist_ok=True)
manifest_loc = f"manifests/catdog.manifest"

with open(manifest_loc, "w") as fp:
    for filename in filenames:
        source_ref = f"s3://{bucket.name}/images/{filename}"
        fp.write(json.dumps({"source-ref": source_ref})+"\n")

bucket.upload_file(manifest_loc, manifest_loc)
```

## Private Workforce 생성하기

라벨링 잡을 만들기 전에 한가지 더 해야할 일이 있는데, 누가 라벨링 잡을 처리할 것인지, 작업자를 결정하는 것이다.

GT는 라벨링 잡을 처리하기 위해 3종류의 작업자를 선택할 수 있다.

* Amazon Mechanical Turk - 아마존에서 관리하는 외주업체에 라벨링작업을 맡긴다. 장당 고정 비용이 청구된다.
* Private Workers - Cognito UserPool 을 이용하여 팀원을 초대하고 팀원들에게 작업을 분배할 수 있다.
* Vendor - AWS Marketplace 에 등록된 서비스를 이용하여 라벨링 작업을 할 수 있다. 서비스 별로 책정된 비용이 청구된다.

여기서는 *Private Workers* 를 이용하여 작업을 진행한다. 생성방법은 코드에 자세히 나와있다.

![](https://github.com/haandol/sagemaker-groundtruth-tutorial/raw/49bdc7e4064f9e648e1501306234288ee8120d0b/assets/PrivateWorkforce.png)

## GT 라벨링 작업 생성하기

![](https://github.com/haandol/sagemaker-groundtruth-tutorial/raw/49bdc7e4064f9e648e1501306234288ee8120d0b/assets/SetupGroundTruth.png)

라벨링 잡 메뉴의 *Create labeling job* 버튼을 클릭해서 작업을 생성할 수 있다.

* Job name: 적절한 작업이름을 적어준다. e.g. catdog-label-0
* Label name (The override checkbox): *labels* 로 오버라이딩(override) 해준다. 기본은 my-annotations 이다.
* Input data location: 앞서 만든 *catdog.manifest* 의 위치이다.
* Output data location: 라벨링 결과가 저장될 위치이다.
* IAM role: 적절한 롤이 없다면 자동으로 생성해준다.
* Task type: *Image > Bounding box* 를 선택한다.

## 라벨링 작업 진행하기

라벨링 잡을 생성하고 나면 할당된 Private Worker(작업자) 들에게 작업할당 메일이 발송된다. 각 작업자는 메일링크를 통해 로그인 후 자신에게 할당된 작업 목록을 확인할 수 있다.

![](https://github.com/haandol/sagemaker-groundtruth-tutorial/raw/49bdc7e4064f9e648e1501306234288ee8120d0b/assets/WorkerLabelingJobs.png)

*Start Working* 을 클릭해서 작업을 진행하면 아래와 같이 라벨링 작업을 진행하게 된다.

![](https://github.com/haandol/sagemaker-groundtruth-tutorial/raw/49bdc7e4064f9e648e1501306234288ee8120d0b/assets/2Labels.png)

## 결과확인

![](/assets/img/20200430/result.png)

라벨링 잡의 결과는 콘솔 페이지에서 확인할 수 있다. 하지만 우리가 필요한 것은 디텍션 모델 학습에 사용할 **(class, top, left, width, height)** 형태의 라벨이다.

이런 라벨 데이터는, 모든 라벨링 작업이 완료되고 나면 처음 라벨링 잡을 만들때 지정했던 *output_data_location* 아래에 *output.manifest* 로 저장된다.

*output.manifest* 의 라벨데이터는 다음과 같은 형태로 저장된다.

```json
{"labels": {"annotations": [{"class_id": 1,
                             "height": 386,
                             "left": 98,
                             "top": 89,
                             "width": 339}],
            "image_size": [{"depth": 3, "height": 512, "width": 512}]},
 "labels-metadata": {"class-map": {"1": "Dog"},
                     "creation-date": "2020-04-29T16:38:58.542746",
                     "human-annotated": "yes",
                     "job-name": "labeling-job/catdog-lablel-0",
                     "objects": [{"confidence": 0.09}],
                     "type": "groundtruth/object-detection"},
 "source-ref": "s3://sagemaker-ap-northeast-2-929831892372/images/8.jpg"}
```

이 *output.manifest* 를 적절히 변환하여, 온프레미스 또는 Sagemaker 에서 Object Detection 모델 학습을 진행하면 된다.

## 마치며

라벨링작업을 위해 몇개의 툴을 써봤지만, 팀원들과 수백장의 이미지를 같이 작업하기에 GT 가 제일 나은 것 같다.

----

[^1]: [Sagemaker Ground Truth Tutorial](https://github.com/haandol/sagemaker-groundtruth-tutorial/blob/master/Sagemaker%20Ground%20Truth.ipynb)