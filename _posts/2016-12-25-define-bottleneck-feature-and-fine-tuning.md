---
layout: post
title: Bottleneck feature? Fine-tuning?
excerpt: 처음 보는 단어 보틀넥 피쳐, 파인튜닝을 알아보자
author: vincent
email: ldg55d@gmail.com
tags: bottleneck-feature fine-tuning meaning definition
publish: true
---

## TL;DR

### 보틀넥 피쳐(Bottleneck feature)

모델에서 가장 추상화된 피쳐

특히 CNN 모델에서는 어파인 레이어(Fully-connected layer) 바로전 CNN 블록의 output 값

### 파인 튜닝(Fine-tuning)

모델의 파라미터를 미세하게 조정하는 행위

특히 딥러닝에서는 이미 존재하는 모델에 추가 데이터를 투입하여 파라미터를 업데이트하는 것을 말한다.


## 시작하며

최근 keras 를 이용해 딥러닝을 공부하고 있는데 상당히 좋다.

keras 는 원래 theano 기반이었는데 tf(tensorflow) 가 인기를 끌면서 tf 백엔드를 지원하게 되어 성장이 가장 빠른 딥러닝 프레임워크 2위에 랭크되고 있다.[^1]

keras 블로그에는 keras 튜토리얼이 몇개 올라와 있는데, 그 중 백미는 이미지 분류기 튜토리얼[^2] 이라고 생각한다.

이 튜토리얼은 딥러닝을 이용한 기본적인 문제해결 순서의 거의 모든 것을 담고 있으므로 keras 를 사용할 계획이라면 반드시 읽어보길 바란다.

머신러닝 입문자인 나는, 이 튜토리얼에서 보틀넥 피쳐(bottleneck feature) 라는 단어와 파인튜닝(fine-tuning) 이라는 단어를 처음 접했다.

두 단어로 구글에서 검색해봐도 확 와닿지 않는 설명만 있어서 답답했다.

본 글에서는 내가 이해한대로 간단히 정리해본다. ~~틀리면 알려주세요~~

## 보틀넥 피쳐(Bottleneck feature)

![VGG16 bottleneck feature](https://blog.keras.io/img/imgclf/vgg16_original.png)

그림에 친절하게 체크가 되어있다.

가장 마지막 CNN 블록, 즉 Fully-connected layer(Affine layer 또는 Dense layer 라고도 부름) 직전의 CNN 블록의 결과를 보틀넥 피쳐(Bottleneck feature)라고 부른다.

CNN 모델은 각 CNN 블록의 풀링(pooling) 레이어를 지나면서 피쳐 사이즈가 줄어들기(== 추상화되기) 때문에

피쳐 크기를 기준으로 생각하면 병을 뒤집어둔 모양과 비슷하다.

개인적으로는 `모델에서 가장 추상화된 피쳐` 라고 이해했는데 다른 딥러닝 모델(RNN 등)에서도 같은 의미로 사용되고 있는지 확실하지 않다.

# 파인튜닝(Fine-tuning)

[위키피디어 설명](https://en.wikipedia.org/wiki/Fine-tuning)

파인튜닝은 정교한 파라미터 튜닝이라고 생각하면 되는데 `정교한`과 `파라미터`가 키포인트들 이다.

`고양이와 개 분류기` 를 만드는데 다른 데이터로 학습된 모델(VGG16, ResNet 등) 을 가져다 쓰는 경우[^3] 를 생각해보자.

VGG16 모델의 경우 1000 개의 카테고리를 학습시켰기 때문에 고양이와 개, 2개의 카테고리만 필요한 우리 문제를 해결하는데 모든 레이어를 그대로 쓸 수는 없다.

따라서 가장 쉽게 이용하려면 내 데이터를 해당 모델로 예측(predict)하여 보틀넥 피쳐만 뽑아내고, 이를 이용하여 어파인 레이어(Fully-connected layer) 만 학습시켜서 사용하는 방법을 취하게 된다.

하지만 이 경우는 파인튜닝이라고 부르지 않는다. 피쳐를 추출해내는 레이어의 파라미터를 업데이트 하지 않기 때문이다.

어파인 레이어를 업데이트 하지 않냐고 생각할 수 있지만 내가 새로 구성한 레이어이기 때문에 업데이트가 아니며 초기 웨이트가 랜덤이기 때문에 정교하지도 않다.

파인튜닝을 했다고 말하려면 기존에 학습이 된 레이어에 내 데이터를 추가로 학습시켜 파라미터를 업데이트 해야 한다.

이 때 주의할 점은, 튜토리얼에서도 나오듯, 정교해야 한다.

완전히 랜덤한 초기 파라미터를 쓴다거나 가장 아래쪽의 레이어(일반적인 피쳐를 학습한 덜추상화된 레이어) 의 파라미터를 학습해버리면 오버피팅[^4] 이 일어나거나 전체 파라미터가 망가지는 문제가 생기기 때문이다.

## 마치며

얼마전 앤드류 응 교수의 머신러닝 코세라 강의를 끝냈지만 딥러닝은 완전히 새로운 분야다.

단어부터가 새로운 단어 투성이다. Convolution, Pool, Adaptive Gradient Descent 등 딥러닝에만 사용되는 단어들이 꽤나 많은 것 같다.

`어떤 단어를 남에게 개념을 설명할 정도로도 이해하지 못한다면, 나는 그 단어를 그냥 모르는 것이다.`는 주의라

한동안은 단어설명위주의 글을 쓰며 머리에 정리해 나갈 생각이다.

----

[^1]: [fchollet 의 트위터](https://twitter.com/fchollet/status/810201293151145984)
[^2]: [building-powerful-image-classification-models-using-very-little-data](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)
[^3]: [transfer learning](https://sites.google.com/site/lifeiyagi/computer-science/jeon-ihagseub-ilantransferlearning) 이라고 부른다. 
[^4]: 우리가 학습시킨 모델이 학습데이터만을 잘 설명하게 되어 일반적인 경우를 잘 설명하지 못하는 경우를 말한다. [위키피디어](https://en.wikipedia.org/wiki/Overfitting)
