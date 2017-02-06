---
layout: post
title: 앙상블(ensemble)기법 설명
excerpt: ensemble, bagging, boosting 이 뭘까?
author: vincent
email: ldg55d@gmail.com
tags: ensemble, bagging, boost, machine learning, kaggle
publish: true
---

## TL;DR

앙상블이란 여러개의 weak learners[^1] 를 이용해 최적의 답을 찾아내는 기법이다.

배깅(Bootstrap AGGregatING, Bagging) 이란 테스트 데이터 샘플링(Bootstrap) 통해 여러개의 테스트 데이터를 만들고, 각 테스트 데이터를 이용해 여러개의 weak learner 를 만든다. 최종적으로 각 learner 의 예측결과를 평균내서 종합(aggregate)한다.

부스팅이란(Boosting) 이란 동일한 테스트 데이터로 여러개의 weak learner 들을 순차적으로(iterative) 만드는데, i번째 learner 는 i-1 번째 learner 가 잘못 예측한 데이터에 가중치를 좀 더 주어서(boosting) 학습한다. 최종적으로 마지막에 생성된 learner 를 이용하여 예측한다.


## 시작하며

머신러닝을 안다룬지도 좀 되었고 해서 kaggle 문제 중 쉬운 것들을 풀면서 다시 감을 잡아볼까 했다.

kaggle 문제풀이에 대해서 정보를 수집하던 중,

예전에는 묻지마 모델로 Random Forest 를 썼었는데 요즘에는 XGBoost 를 쓴다고 하더라[^2]

XGBoost와 Random Forest 를 찾아봤더니 앙상블 기법을 쓴다고 한다.

앙상블 기법을 찾아보니 배깅, 부스팅의 두가지 방법을 대표적인 예로 들고 있었다. ~~사실 xgboost 와 random forest 는 두가지와 좀 다르다~~

대체 배깅과 부스팅은 무엇인가?


## 개념 설명엔 유튜브가 최고인듯

이런 문제가 생길 때마다(처음 접하는 개념) 많은 블로그 글과 quora 와 기타 등등을 찾아보지만, 결국 맘에 드는 정보는 Youtube 에 있더라.

유튜브에서 좋은 영상을 찾았는데, 알고보니 Udacity 의 `트레이딩 시스템을 위한 머신러닝 코스중 한 강좌`[^3]였다.

영상을 캡쳐하면서 한글로 설명한 포스팅도 봤는데, 그냥 영상을 보면 바로 이해할 수 있다.

이 글에서도 그냥 영상만 소개하고 넘어가겠다.


## 마치며

사실 learner 를 만드는건 라이브러리를 가져다 쓰면 되기 때문에 모델을 몰라도 된다.

하지만 기본 파라미터를 사용한 learner 의 성능이 잘 나올리가 없다. 어느정도 성능을 내려면 파라미터를 튜닝이 필수다.

이 때, 어떤 파라미터를 어떻게 수정할지 결정해야 하는데, 그러려면 모델의 동작방식과 파라미터의 의미 정도는 알아야 한다.

그럼 모델의 어느정도까지 알아야 하는가?

`내 목표는 라이브러리에서 제공하는 파라미터의 튜닝이 가능한 수준까지` 이며 이 경우 모델을 구성하는 수식을 다 이해하는 것은 낭비라고 생각한다.~~물론 꼭 이해해야하는 수식도 있지만~~

요즘 라이브러리들은 파라미터와 모델과의 관계만 알아도, 미적분 문제도 못푸는 사람이~~나~~ 튜닝을 할 수 있게 잘 만들어져있기 때문이다.

----

[^1]: Learner 란 특정한 데이터를 이용해 인스턴스화 한 모델을 말한다. Weak learner 는 최종적인 결과물보다 상대적으로 정확하지 않은 결과를 보이는 learner 이다.
[^2]: [모델링 그리고 부스팅](http://freesearch.pe.kr/archives/4349)
[^3]: [Ensemble Overview](https://classroom.udacity.com/courses/ud501/lessons/4802710867/concepts/49631985600923)
