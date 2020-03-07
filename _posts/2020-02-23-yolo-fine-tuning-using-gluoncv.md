---
layout: post
title:  MXNet YOLO 파인튜닝으로 피카츄를 찾아보자
excerpt: Finetune YOLO3
author: vincent
email: ldg55d@gmail.com
tags: yolo yolov3 object-detection finetuning transfer-learning gluon mxnet pikachu machine-learning
publish: false
---

## TL;DR

코드는 여기[^1]


## 시작하며

Gluon CV 의 디텍션 모델 파인튜닝 예제를[^2] SSD 대신 YOLO3 로 파인튜닝한다.

----

[^1]: [mxnet-yolo-pikachu](https://github.com/haandol/mxnet-yolo-pikachu)
[^2]: [Finetune a pretrained detection model](https://gluon-cv.mxnet.io/build/examples_detection/finetune_detection.html)