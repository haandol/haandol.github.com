---
layout: post
title: Sagemaker 에서 SDXL LoRA Multi-GPU 파인튜닝하기
excerpt: Fine-tune SDXL LoRA on Sagemaker with Multi-GPU
author: vincent
email: ldg55d@gmail.com
tags: sdxl lora stable-diffusion sagemaker multi-gpu fine-tuning
publish: true
---

## TL;DR

코드는 여기[^1]

## 시작하며

최근에 SDXL 로 파인튜닝 해야할 일이 있어서 파인튜닝을 하려고 했는데, Sagemaker 에서 Multi-GPU 로 파인튜닝을 하는 방법을 찾아보니 없어서 만들어봤다.

당연히 Single GPU 로도 파인튜닝 할 수 있지만, 세이지메이커 비용책정상 같은 비용일 때 속도차이가 많이 나기 때문에 Multi-GPU 로 파인튜닝을 하는 것이 좋다.

코드는 그냥 diffusers[^2] 에 있는 코드를 거의 그대로 가져왔고, Sagemaker training-job 환경에서 Multi-GPU 로 파인튜닝을 할 수 있도록 수정했다.

## 커스텀 도커 이미지 빌드

코드의 예전 히스토리를 보면 Single-GPU 를 사용하는 코드를 둔 적이 있는데, 그 때는 빌드 없이 그냥 사용했었다. (태그를 만들어둘껄)

하지만 8000 스텝 돌리는 데 g5.16xlarge 로 20시간쯤 걸리는데, 같은 스텝을 Multi-GPU 로 돌리면 5시간 정도면 된다. 굳이 Single-GPU 를 쓸 이유가 없다.

여튼 Sagemaker Training-job 에서 accelerate 를 이용하여 multi-GPU 를 사용하려면 커스텀 도커 이미지를 빌드해야한다.

공용 레지스트리에 올려두고 가져다 쓰면 안될까 하는 생각을 할 수 있지만, Sagemaker Estimator 에서 같은 계정의 ECR 에 있는 이미지만 사용할 수 있기 때문에 불가능하다.

CuDA 가 내장된 이미지를 빌드해야하기 때문에 이미지가 크다. (16GB 정도) 따라서 ECR 에 올리고 할거 생각하면 그냥 빌드용 세이지메이커 노트북을 따로 만들어서 빌드하는 것이 낫다.

## Model merge

LoRA 로 학습하고 나면 추가적인 학습을 하기 위해서 쓰는 방식은 크게 2가지 이다.

1. 체크포인트
2. 그냥 데이터만 추가해서 처음부터 학습하기
3. LoRA 로 학습한 모델을 원본 모델에 합치기

1번은 코드상 로컬에서 돌리는 것을 기반으로 작성되어 있어서, S3 기반으로 고치려면 쉽게 고칠 수 있지만 그러고 싶지는 않았다. (diffusers 코드를 많이 고치면 버전업이 되었을때 diff 로 고칠때 손이 많이 가기 때문) 뿐만 아니라 체크포인트 스텝수를 기준으로 추가 학습을 하는 식으로 되어 있어서 하이퍼파라미터 관리하기 어렵다.

보통 추가 학습시에는 서로 다른 이미지셋으로 진행하는 경우가 많은데, 이 경우 그냥 LoRA 를 2번 따로 학습하고 2개를 한번에 로드해서 사용하는 것이 사용에 좀 더 유연하기 때문에 2번을 추천한다.

여튼 그 외의 경우에는 모델을 합쳐서 배포하거나 추가학습을 하게 된다. 다행히 diffusers 에는 model fuse 라는 기능을 제공하고 있기 때문에 이를 사용하면 된다.

코드에도 merge 폴더 아래에 해당 코드가 있으니 참고하면 된다.

## TCD - Trajectory Consistency Distillation

코드에는 테스트할 때 LCM (Latent Consistent Model) 을 사용하고 있었는데, 최근에 나온 TCD LoRA 를 사용하면 더 좋은 성능을 낼 수 있다.

LCM 은 Consistency Distillation 을 Latent space 에 적용한 방법으로 적은 스텝으로도 높은 퀄리티의 이미지를 생성할 수 있게 해준다. 다만 LCM 은 샘플링 과정에서 디테일한 정보들을 잘 생성하지 못하는 문제가 있었다.

TCD 는 TCF (Trajectory Consistency Function) 과 SSS (Strategic Stocastic Sampling) 을 사용하여 이 문제를 해결한다.

LCM LoRA 와 사용방법은 거의 동일하며, 이상하게 LCM LoRA 는 컨트롤넷에 붙이면 잘 동작하지 않는데(unet 을 직접 붙이면 잘 됨...), TCD LoRA 는 컨트롤넷에서도 잘 되는 것으로 보인다.

성능도 좀 더 낫고, 사용하기도 쉬운데, 감마 값으로 디테일을 추가적으로 조정할 수 있기 때문에 TCD LoRA 를 사용하는 것이 좋다.

## 마치며

SD 3 가 곧 나오는데 DiT 기반이기 때문에 해당 내용은 곧 out of date 가 되지 않을까 한다.

다만 SD 3 는 800M 부터 8B 까지 나올 예정인데, 가장 큰 모델은 이미지 생성에 30초 정도 걸린다고 한다.

SDXL 이 나온 시점에도 학습이나 서빙 비용때문에 SD 1.5 를 쓰는 사람이 아직 있는거 보면, 성능보다 비용을 더 중요하게 생각하는 경우 SDXL 도 한동안은 옵션으로 고려될 수 있을 것 같다.

SD Cascade 는 Latent space 를 좀 더 활용하기 위한 방법으로 보이는데, SD 3 가 나올 예정이기 때문에 개인적으로 SD Cascade 는 그냥 넘어가도 될 것 같다.

---

[^1]: [Sagemaker Stable Diffusion XL](https://github.com/haandol/sagemaker-stable-diffusion-xl)
[^2]: [Diffusers Train SDXL Lora](https://github.com/huggingface/diffusers/blob/v0.27.2/examples/text_to_image/train_text_to_image_lora_sdxl.py)
