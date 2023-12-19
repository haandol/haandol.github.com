---
layout: post
title: 개발자를 위한 Graph Neural Network (GNN)
excerpt: Graph Neural Network (GNN) for Software Developers
author: vincent
email: ldg55d@gmail.com
tags: graph gnn deeplearning machinelearning
publish: true
---

## TL;DR

GNN 은 인풋도 그래프 아웃풋도 그래프

## 시작하며

최근에 맡은 업무에서 fraud prevention 을 하고 싶다는 요구사항이 있었다.

대충 들었을 때 기존 임베딩 대신 GNN (Graph Neural Network) 임베딩을 쓰면 성능이 올라가지 않을까 싶어서 GNN 을 공부하게 되었다.

기존 ML 모델들과 달리, GNN 은 그래프와 관련된 지식이 없으면 사용하기가 어려운 것 같다. 그리고 그래프를 공부하는 것도 어디를 얼마나 공부하는게 좋을 감을 잡기가 어렵다.

본 글에서는 GNN 을 처음 접하는 개발자가 GNN 기반 모델들을 쓰려고 할 때 필요한 기본적인 지식들을 정리하고자 한다.

## 그래프 공부 자료

전체적인 그래프 이론과 GNN 의 이론적인 내용은 스탠포드 대학교의 CS224W[^1] 강의를 듣는 것이 가장 좋은 것 같다.

주의할 점은, 앞쪽의 많은 부분은 GNN 이 아니라 그래프 ML 등의 내용이므로 GNN 에서 해결된 문제들을 많이 다루고 있다. 따라서 앞쪽에 너무 많은 시간을 쏟지 않는 것이 좋다. 또한 전체적으로 모델을 설계하는 사람의 입장에서 디테일하게 설명하고 있으므로, 한번에 다 이해하려고 하지 말고 전체적으로 대충 한두번 읽고 필요한 내용을 영상과 함께 다시보는 것이 좋다.

유튜브에도 2019년 강의 영상이 있고, 한글로 강의자료 정리한 내용들도 인터넷에 있지만, 수업 공식자료 슬라이드가 너무 잘 되어 있어서 그냥 슬라이드만 몇번 읽어보고 모르는 내용만 유튜브를 봐도 대략적인 내용은 파악할 수 있다.

코드 부분은 아래에서 잠깐 설명하겠지만 PyTorch Geometric (PyG) 공식 예제들과 github 의 example 코드들을 보는 것이 가장 좋은 것 같다.

## GNN 이란?

GNN 은 Graph Neural Network 의 약자로 그래프를 인풋으로 받아서 그래프를 아웃풋으로 내는 모델을 말한다.

대부분 GNN 의 목적은 그래프의 노드들을 임베딩 하는 것으로, 노드를 임베딩할 때 그래프의 구조(노드의 이웃)를 반영하여 임베딩을 하게 된다.

이런 식으로 그래프의 이웃 노드들의 정보를 반영하는 것을 메시지 패싱(Message Passing) 이라고 한다. (CNN 의 컨볼루션 연산과 비슷한 개념)

여느 ML 이 그렇듯 GNN 도 분류 문제에 주로 사용하게 되며, GNN 으로 풀 수 있는 분류 문제는 크게 3가지로 나눌 수 있다.

- Node Classification: 노드의 클래스를 예측
- Link Prediction: 노드 사이의 연결 여부를 예측
- Graph Classification: 그래프의 클래스를 예측

무슨 문제가 되었든 GNN 을 이용해서 임베딩을 하고, 임베딩 된 결과를 이용해서 prediciton head 를 붙여서 분류 문제를 푸는 것이 일반적이다.

## GNN 의 어려운 점

개인적으로 GNN 공부를 처음 시작했을 때 어려운 점이 두가지가 있었다.

- 데이터를 어떻게 변환할 것인가?
- 새로운 데이터를 어떻게 예측할 것인가?

### Tabular data to Graph

일반적인 회사는 행렬로 이뤄진 tabular 형태로 데이터를 쌓는다. 그래서 GNN 을 쓰기 위해서는 tabular data 를 그래프로 변환해야 한다. 즉 학습 데이터, 테스트 데이터, 그리고 예측하고자 하는 데이터 모두 그래프 형태로 가공해야 한다는 의미이다.

tabular data 를 그래프로 변환하는 여러가지 방법중 개발자가 익숙한 방법은 ERD (Entity Relationship Diagram) 를 그려보는 것이다. ERD 는 엔티티와 엔티티 사이의 관계를 그래프로 표현한 것으로 좋은 시작점이 될 수 있다.

### Homogeneous vs Heterogeneous

ERD 그래프도 노드와 엣지로 이루어져 있다. 대충 `G = (V, E)` 같이 표현할 수 있을 것이다. 그런데 ERD 를 그리고 보면 각 엔티티의 속성들이 서로 다르다는 것을 알 수 있다. 그래프의 장점은 (V, E) 를 입력으로 받아 관계를 학습할 수 있다는 점이며, 이를 극대화 하려면 무엇이 노드이고 무엇이 속성인지 정의해야 한다. 각 테이블이 노드가 될 수도 있지만 테이블의 특정 속성이 노드가 될 수도 있다. 이런 것들을 정의하는 것이 GNN 을 쓰기 위해 가장 중요한 일이다.

여튼 노드와 엣지의 종류가 하나가 아니라는 것을 이해한다는 것이 중요하다. 이런 여러 종류의 노드와 엣지를 이용해 구성된 그래프를 Heterogeneous Graph 라고 한다.

정리하면 GNN 을 사용하려면 tarbular data 를 Heterogeneous 한 그래프로 변환하는 작업이 필요하며, 이를 위해 여러 툴들을 사용하게 된다.

### Transductive vs Inductive

GNN 을 사용할 때 한가지 더 고려해야 하는 것이 Transductive 인지 Inductive 인지이다.

Transductive 는 하나의 그래프에서 일부를 학습한 뒤에 나머지 부분을 예측하는 것이고(즉, subgraph 를 뽑아내더라도 그래프의 구조 자체가 변하지는 않는다.), Inductive 는 매번 새로운 그래프로 학습하고 새로운 그래프를 예측하는 것이다.

많은 예제가 Transductive 한 예제이며, Homogeneous graph 를 다룬다. 하지만 실제로는 Inductive 한 워크로드가 많고(사기/이상 탐지 등), Heterogeneous graph 를 다루는 것이 일반적이다.

## Framework

많이 쓰이는 툴은 DGL, PyTorch Geometric (PyG)[^2] 등이 있지만 PyG (Pytorch Geometric) 이 개인적으로 가장 직관적이고 좋은 것 같다. (스탠포드 강의도 PyG 기반의 GraphGym 을 사용하고 있다.)

예제도 많이 제공해주고 문서도 잘 되어 있어서 PyG 를 사용하면 다른 툴들보다 접근성이 좋으며, PyTorch 문법을 거의 그대로 사용할 수 있어서 코드도 이해하기 쉬운 것 같다.

DGL 은 AWS 에서 공식적으로 밀고 있는 느낌인데 TensorFlow1.x 와 PyTorch 를 보는 것 같다. (AWS 그래프 데이터베이스인 neptune 에서도 쿼리언어로 gremlin 을 밀고 있는것 같은데 neo4j 의 (open)cyhper 가 좀 더 쉬운 것 같다. 여튼 전체적으로 AWS 방향은 java 쪽이라 개인적으로 너무 안맞다..)

## GNN 모델 종류 간단 정리

PyG 는 Cheatsheet[^3] 로 모델들을 대략적으로 설명해주고 있다. 자주 쓰이는 모델들의 특성만 간단히 정리해보면 다음과 같다.

먼저 알아둘 내용은, 모든 GNN 은 message passing + aggregation 과정을 통해 학습한다. 이 과정 때문에 레이어를 조금만 쌓아도 over smoothing[^4] 문제가 생긴다.

- GCN (Graph Convolutional Network): CNN 의 컨볼루션 연산과 비슷한 방식으로 인접 노드들을 이용하여 임베딩을 한다. over smoothing 문제를 해결하기 위해 skip connection 등의 방법을 사용한다.
- GraphSAGE: neighbor sampling 을 이용한 mini-batch 로 학습한다. 여러 서브그래프를 만들어서 학습하므로 inductive 하다.
- GAT (Graph Attention Network): 트랜스포머의 attention 을 그래프에 적용한 것이다. 노드의 이웃들의 정보를 통해 얼마나 중요한지를 고려하여 (attention) 임베딩을 한다.
- GIN (Graph Isomorphic Network): 그래프의 구조 (isomorph) 를 고려하여 표현력을 최대화 하여 임베딩한다. 그래프의 구조는 루프의 개수, 루프의 길이 등을 고려한다.
- GAE (Graph Auto Encoder): 그래프의 구조를 잘 반영하는 임베딩을 하기 위해 auto encoder 를 사용한다. 인코더는 그래프의 구조를 잘 반영하는 임베딩을 하고(가까운 노드들을 가깝게 먼 노드들을 멀게), 디코더는 임베딩을 이용해 그래프의 구조를 재구성한다. auto encoder 의 특성상 unsupervised learning 이다.

이 외에도 Contrastive Learning 을 이용한 모델들도 있고 (GraphCL, InfoGraph 등), GNN 을 이용한 모델들은 계속해서 나오고 있다.

위에 설명한 GNN 특성상 레이어를 깊이 쌓기가 어렵기 때문에, LLM 이나 CV 처럼 각 모델간의 성능 차이가 극심하게 나는 경우는 드문 것 같다.

## Real-time Inference with graph sampling

데이터를 가공해서 그래프로 변환하고, 학습까지 했다면 이제 예측을 해야 한다.

대부분의 예제는 이미 주어진 데이터셋을 이용해 학습을 하고, 학습된 모델을 이용해 예측을 한다. 하지만 실제로는 매번 새로운 데이터를 받아서 예측을 해야 한다.

GNN 은 그래프를 받아서 그래프를 반환한다고 했다. 그래서 예측을 하려면 그래프를 만들어야 한다.

학습에 사용한 그래프는 대부분 엄청 큰 그래프일 거고, 해당 그래프를 사용하여 예측하는 것은 메모리 문제를 야기한다.

따라서 Graph sampling 이라는 방법을 사용하게 된다. Graph sampling 은 학습에 사용한 그래프에서 새로운 노드(예측 대상이 되는) 의 이웃에 해당하는 노드들과 엣지를 뽑아내서 새로운 그래프를 만드는 것이다.

과정을 대략 생각해보면 아래와 같다.

1. 새로운 노드를 기존 그래프에 붙이고
2. 기존 그래프에서 새 노드 기준으로 서브 그래프를 샘플링
3. 해당 서브 그래프를 이용하여 GNN 을 통해 예측

결국 기존 그래프를 가지고 있고 변경해서 다시 쿼리해야하므로, 외부저장소가 필요하다. 이 때 외부저장소는 그래프를 저장하고 그래프를 반환하면 변환작업에 대한 부담이 적을 것이다.(쿼리 성능도 훨씬 좋을 것이고)
그래서 GNN 으로 문제를 푸는 경우 neo4j, neptune 등의 그래프 데이터베이스를 사용하여 위의 작업을 하는 것이 일반적이다. [^5]

## 마치며

코드 레벨에서도 기존과 많이 다르다.

모델은 언급한대로 레이어는 몇개 없고 기존 NN 구조를 그대로 쓰기 때문에 별로 어렵지 않지만, 오히려 데이터 로더 같은 부분이 동작 방식을 이해하기 전에 헤멘 부분이 많았던거 같다.

---

[^1]: [CS224W](http://web.stanford.edu/class/cs224w/)
[^2]: [PyG Introduction by Example](https://pytorch-geometric.readthedocs.io/en/latest/get_started/introduction.html)
[^3]: [PyG Cheatsheet](https://pytorch-geometric.readthedocs.io/en/latest/notes/cheatsheet.html)
[^4]: [Over smoothing](https://towardsdatascience.com/over-smoothing-issue-in-graph-neural-network-bddc8fbc2472)
[^5]: [Build a GNN-based real-time fraud detection solution](https://aws.amazon.com/blogs/machine-learning/build-a-gnn-based-real-time-fraud-detection-solution-using-amazon-sagemaker-amazon-neptune-and-the-deep-graph-library/)
