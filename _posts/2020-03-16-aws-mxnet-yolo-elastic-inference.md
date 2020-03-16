---
layout: post
title: MXNet SSD 디텍터를 AWS Elastic Inference 에 올리기
excerpt: MXNet SSD Detector on AWS EI
author: vincent
email: ldg55d@gmail.com
tags: mxnet ssd eia aws ei elastic-inference
publish: true
---

## TL;DR

코드는 여기[^1]

EI 는 아직 한계점이 명확히 있다.(지원안되는 모델들이라던가 고정크기의 이미지 라던가)

이런 한계점들만 걸리지 않고 EI 를 쓸 수 있다면 무조건 쓰는게 이득이다.

## 시작하며

P3 모델로 세이지메이커 엔드포인트를 서비스하는데 비용이 너무 많이 드는 문제가 있었다.

이런저런 대안을 찾다가 Elastic Inference 를 사용해보기로 했는데 결과가 너무 맘에 들어서 공유차원으로 올린다.

## Elastic Inference 는 어떻게 동작하는가?

여기[^2]에 EI 가 어떻게 동작하는지 잘 나오니 참고하자.

쉽게 말하면 EIA 지원 엔드포인트를 생성하면 EI 를 호출할 수 있는 VPC Endpoint 를 포함한 컨테이너에 엔드포인트가 생성되고 호출시 warm start 과정을 거쳐서 EI 기능을 사용할 수 있다.(프로비전된 람다 느낌)

## 코드 설명

레포[^1]에 있는 노트북을 보면 내용이 쉽고 짧기 때문에 자세한 설명은 하지 않는다. 핵심 사항들만 몇가지 짚고 넘어가자.

### Role

세이지메이커 노트북을 만들고 해당 레포를 clone 해서 진행하는 것이 제일 편하지만, 로컬에서도 돌리고 싶은 경우가 있어서~~나의 경우~~ 로컬에서도 돌릴 수 있도록 작업이 되어 있다.

다만, 해당 노트북의 기능을 사용하기 위해서 *AmazonSageMakerFullAccess* 폴리시를 가진 Role이 필요한데, 해당 폴리시에는 S3 업로드/다운로드 를 포함한 다양한 권한들이 포함되어 있다.

해당 폴리시를 부여한 롤을 생성하고, 롤 이름을 노트북의 *role_name* 에 값을 바꿔서 적어준다.

또, 노트북은 아래와 같이 기본 버킷을 사용한다.

```python
BUCKET_NAME = sagemaker.Session().default_bucket()
session = boto3.session.Session()
s3 = session.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
```

처음엔 해당 버킷이 없기 때문에 *BUCKET_NAME* 을 확인해서 직접 생성해주도록 하자. 위에서 언급한 롤의 폴리시에 *sagemaker* 라는 단어가 포함된 버킷에 접근할 권한을 가지고 있기 때문에 따로 권한을 생성해줄 필요는 없다.

### model.tar.gz

mxnet inference 컨테이너는 처음 인스턴스 생성시 *model.tar.gz* 파일을 */opt/ml/models* 아래에 다운받고 압축을 풀어준다. 이 안에는 일반적으로 *model.params* 과 같이 학습된 모델 파라미터가 포함된다. 

`src/inference.py` 를 보면 알 수 있지만, 여기서는 따로 학습된 모델을 쓰지 않고 MXNet 에서 제공하는 pretrained 모델을 사용한다. 따라서 빈 model.tar.gz 를 미리 생성해두고 그냥 업로드만 한다.

```python
# upload emtpy model.tar.gz
bucket.upload_file('model.tar.gz', Key='ssd_test/model.tar.gz')
```

### inference.py

마지막으로 inference.py 내용만 간단히 살펴보자.

inference 모듈은 4개의 함수로 되어 있다. 각각 mode_fn, input_fn, predict_fn, output_fn 이다.

* model_fn - 모델로드. 최초 인스턴스가 생성될때 모델을 로드하고 로드한 모델을 리턴한다. 이 모델은 캐시되어 있다가 인퍼런스시 predict_fn 으로 전달된다.
* input_fn - 전처리. 엔드포인트 요청시 *request_body* 와 *content_type* 이 입력된다. 입력데이터에 대해 전처리를 하고 predict_fn 에 전달된다.
* predict_fn - 인퍼런스. model_fn 에서 전달받은 모델을 이용하여 인퍼런스를 하고 결과를 반환하여 output_fn 으로 보낸다.
* output_fn - 후처리. 인퍼런스 결과를 받아서 가공할 필요가 있으면 적절히 가공해서 반환한다.

함수 이름이나 데이터 흐름은 직관적이기 때문에 큰 어려움은 없을 것이다.

본문에서는 이미지 데이터를 다루기 때문에 bas64 를 이용하여 이미지를 encode/decode 하고 있으며, 해당 내용을 제외하면 튜토리얼[^3] 등에서 모델을 사용하는 것과 완전히 동일하다.

## 마치며

동일한 모델을 cpu 에서 0.8초 정도 걸리는데 ei 를 사용하면 대략 0.08초안에 처리가 된다.(10배)

----
[^1]: [mxnet-elastic-inference](https://github.com/haandol/mxnet-elastic-inference)
[^2]: [Amazon Elastic Inference Basics](https://docs.aws.amazon.com/elastic-inference/latest/developerguide/basics.html)
[^3]: [Predict with pre-trained SSD models](https://gluon-cv.mxnet.io/build/examples_detection/demo_ssd.html)