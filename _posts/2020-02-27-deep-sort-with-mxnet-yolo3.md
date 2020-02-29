---
layout: post
title: DeepSORT with MXNet YOLO3
excerpt: person tracker using DeepSORT
author: vincent
email: ldg55d@gmail.com
tags: deepsort mxnet yolo yolov3 object-tracking machine-learning
publish: true
---

## TL;DR

SORT = 디텍터 + 칼만필터 + 헝가리안 알고리즘
DeepSORT = 딥러닝 + SORT

코드는 여기[^1], MXNet 의 YOLO3 을 디텍터로 하여 딥소트 알고리즘을 구현하였다. MXNet YOLO3 를 디텍터로 사용해서 Deep SORT 를 사용한다.

## 시작하며

영상 데이터에서 사람을 트래킹 하는 프로젝트를 진행하고 있는데, 적절한 알고리즘을 찾아보다가

DeepSORT(이하 딥소트) 를 보게되었고 프로덕션에 사용하기에도 나쁘지 않은 것 같아 정리해본다.

딥소트 알고리즘의 개념은 복잡하지 않지만 상당히 다양한 기술들을 사용하고 있기 때문에 상세히 설명하기 쉽지 않다. 정말 잘 설명된 글들[^2][^3] 도 많기 때문에 내가 따로 글을 쓰는 것보다 해당 글을 보는 것이 훨씬 나을 것이다.

딥소트 알고리즘의 개략적인 내용과 해당 알고리즘을 이해하는데 필요한 내용들을 간단히 소개해본다.

## Kalman Filter

칼만 필터는 여기[^4] 에 아주 잘 설명되어 있다.

칼만 필터는 베이지안 추정과 같이 직접확률을 계산할 수 없는 경우 관련 된 값을 이용하여 원래 값을 구하는 것으로 `predict <-> update` 사이클로 이루어져 있다.

![](https://miro.medium.com/max/1128/1*wk0AZNEjcdsqiQo5P5A0pw.png)

1. 과거의 값을 이용하여 현재값을 예측하고
2. 예측값과 측정값에 각각 노이즈를 반영한 뒤, 실제값을 예측한다.
3. 이 실제값을 다시 다음 측정에 사용한다.

측정값을 그냥 쓰면 되는거 아니냐고 생각할 수 있지만 노이즈라는 개념이 들어가면 (원래 센서퓨전에 쓰려고 만든 알고리즘이므로) 측정값도 100% 신뢰할 수 없다는 것을 알 수 있다.

또 칼만필터는 기본적으로 가우시안 분포로 값이 분포되어 있다고 가정하고 있으며(즉, 예측 값은 평균과 분산으로 표현될 수 있다.), 측정값의 분포가 가우시안이 아닐 경우에는 해당 분포에 맞는 변형된 칼만 알고리즘을 사용해야 한다.

칼만 필터를 좀 더 자세히 알고 싶다면 이 책[^5] 을 추천한다.

## SORT

DeepSORT 는 기존에 있던 SORT[^6] 알고리즘에 딥러닝 피쳐를 반영한 것이 가장 큰 차이점이라고 할 수 있다. 따라서 딥소트가 어떻게 동작하는지 알려면 먼저 SORT 를 알아야 한다.

SORT 는 칼만필터와 헝가리안 알고리즘[^7] 으로 이뤄져 있다. 헝가리안 알고리즘은 최저비용의 할당을 하려고 하는 최적화 문제를 해결하기 위한 알고리즘으로 알고리즘의 개념은 크게 어렵지 않다. python 에는 scipy 라이브러리에 linear_assignment 라는 함수로 구현되어 있으며 대부분의 구현체는 해당 라이브러리를 사용하고 있는 것 같다.

## Non Maxmimum Suppressions

NMS[^8] 는 여러개의 바운딩 박스가 겹쳐있을때 어떤 것을 선택하고 어떤 것을 버릴지 판단하는 알고리즘이다. 알고리즘은 단순한데 모든 바운딩 박스에 대해,

1. 가장 높은 confidence score 를 가진 박스를 선택하고
2. 해당 박스와의 IOU가 threshold 이상이면 제외(suppresion) 해준다.

딥소트에서는 YOLO3 가 디텍팅한 바운딩 박스들을 트래커로 넘기기전 프리프로세싱 용으로 사용하고 있다.

## MARS: Re-id dataset

딥소트에서는 이전의 트래킹 결과와 현재 디텍팅 결과의 바운딩 박스들을 매칭하는데 헝가리안 알고리즘을 사용한다.
이 때 사용하는 최적화 팩터는 3가지인데 KNN(K Nearest Neighbour), 딥러닝 피쳐 그리고 IOU 이다. 

여기서 딥러닝 피쳐는 바운딩 박스내의 이미지간 유사도를 나타내며, 해당 모델을 학습시킬 때 사용되는 데이터셋은 Market1501 과 MARS 가 있다. 둘다 re-id 를 위해서 만들어진 데이터 셋이며 특히 MARS 는 비디오와 같은 타임시리즈 데이터에 특화시켜 Market1501을 확장한 버전이라고 보면 된다.

딥소트는 주로 CCTV 에서 보행자를 트래킹 하는 등, 비디오 데이터를 이용하여 트래킹 하는 데 많이 사용하기 때문에 MARS 로 학습된 딥러닝 모델로 re-id 점수를 매겼을때 좀 더 성능이 잘 나온다.

## 마치며

SORT = 칼만필터 + 헝가리안 알고리즘
DeepSORT = 딥러닝 + SORT

딥소트는 위와 같은 느낌으로, 실제로 코드를 보면 각 코드의 영역이 무엇을 하는지 파악하는 것이 크게 어렵지 않다. 개인적으로 딥소트의 트래킹 성능에 가장 크게 영향을 끼치는 것은 디텍션으로, 디텍션을 맡고 있는 YOLO3 의 성능이 가장 중요한 것 같다.

----

[^1]: [mxnet-deepsort-yolo3](https://github.com/haandol/mxnet-deepsort-yolo3)
[^2]: [DeepSORT](https://nanonets.com/blog/object-tracking-deepsort/#deep-sort)
[^3]: [Computer Vision for tracking](https://towardsdatascience.com/computer-vision-for-tracking-8220759eee85)
[^4]: [sensor fusion](https://towardsdatascience.com/sensor-fusion-90135614fde6)
[^5]: [칼만 필터는 어렵지 않아](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=193043129)
[^6]: [SORT](https://jjeamin.github.io/paper/2019/04/25/sort/)
[^7]: [헝가리안 알고리즘](https://gazelle-and-cs.tistory.com/29?category=794321)
[^8]: [Pedestrian Detection using NMS](https://towardsdatascience.com/pedestrian-detection-using-non-maximum-suppression-b55b89cefc6)
[^9]: [Person Re Id](https://amberer.gitlab.io/papers_in_ai/person-reid.html)