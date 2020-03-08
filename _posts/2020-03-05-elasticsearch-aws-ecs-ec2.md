---
layout: post
title: 엘라스틱서치 7.6 을 ECS EC2 에서 사용해보자
excerpt: Elasitcsearch 7.6 cluster on AWS ECS with CDK
author: vincent
email: ldg55d@gmail.com
tags: elasticsearch aws ecs ec2 cluster es cdk
publish: true
---

## TL;DR

코드는 여기[^1]

ES 의 특이한 초기 클러스터 설정 때문에 마스터를 2 개의 태스크로 분리해야 한다.
따라서 총  init-master, master 그리고 data 3개의 태스크로 구성한다.

## 시작하며

2020년 3월 기준 AWS Elasticsearch 는 7.1 까지만 지원하기 때문에, 7.3+ 를 AWS 위에서 사용하려면 마켓플레이스나 베어메탈 등을 이용하여 EC2 기반으로 운영해야한다.

그냥 EC2 를 써도 되지만, EC2 위에 도커 컨테이너로 배포하려고 하는 경우에는 ECS 를 이용해서 처리하는 것이 전체적인 복잡도를 줄일 수 있기 때문에 ECS를 이용해본다.

### CDK

본 글은 CDK[^2] 를 이용하여 진행되므로 CDK 에 대한 개략적인 이해가 필요하다.
CDK 는 IaaC(Infrastructure as a Code) 의 AWS 버전이라고 할 수 있으며 AWS 를 자주 사용하는 Devops 또는 개발자 라면 반드시 사용해야 하는 툴이라고 할 수 있다.

cdkworkshop[^3] 을 통해 쉽게 배울 수 있으며, 코드의 결과는 CloudFormation 으로 변환되어 AWS 상에서는 CloudFormation 으로 관리할 수 있기 때문에 다중 사용자가 동일 인프라를 관리하는 경우에도 쉽게 사용할 수 있다.

## Limitations of ECS EC2

EC2 에 ES 클러스터를 올리는 것은 공홈에 있는 discovery-ec2 플러그인으로 잘 된다.

ECS EC2 로 ES 클러스터를 올리는 것은, 그냥 EC2 와는 전혀 다른 문제인데 네트워크 방식과 ES의 클러스터 부트스트래핑, 그리고 인스턴스 시스템 설정 때문이다.

### 네트워킹 설정

먼저 네트워킹을 보면, ECS EC2 에서 사용할 수 있는 방식은 `BRIDGE`, `HOST`, `AWSVPC` 3가지가 있다.

일단, ES 공홈에 소개된 방식 그대로 하려면 `HOST` 방식 외에는 동작하지 않는다.

> ES 공홈에 나와있는 방식이 EC2 스탠드얼론으로 하나의 EC2 인스턴스에 엘라스틱 서치가 하나 떠 있다는 전제로 설정방법을 안내하고 있기 때문인데, 이 방식과 동일한 것이 HOST 방식이다.
> BRIDGE 는 오버레이 네트워크 방식이고, AWSVPC 방식은 ENI 를 생성해서 할당해주는 방식인데, 둘다 EC2 의 실제 호스트이름과 다른 주소로 컨테이너의 CNI 가 설정된다.
> 따라서 advertise 하는 주소를 EC2 인스턴스의 주소가 아니라 해당 컨테이너 주소로 설정해주면 클러스터 디스커버리에도 큰 문제는 없을 것이다.

이것을 해결하는 것은 본 글의 취지에서 벗어나므로, 일단은 HOST 모드를 사용하여 `One Task per Instance(distinctInstance)` 로 배포하는 방식으로 진행한다.
(BRIDGE, AWSVPC 는 하나의 EC2 인스턴스에 여러개의 도커 인스턴스를 띄우는 것을 전제로 하는 방식인데 하나의 EC2 에 하나의 ES 노드만 떠 있는 것이 안정적이기 때문)

### 클러스터 부트스트래핑
두번째로 클러스터 부트스트래핑을 보자.

ES7.x 는 처음 클러스터가 생성될 때 `cluster.initial_master_nodes` 에 최초 마스터 노드를 지정해야한다.
즉, 동적인 마스터를 자동으로 찾아서 그 마스터들이 클러스터를 구성하는 방식은 안되고, 반드시 최초 설정시에는 initial_master_node 들을 기준으로 클러스터를 구성해야한다.
(클러스터가 한번 구성되고 나면 더이상 필요 없다.)

ECS 를 쓰는 가장 큰 이유는 EC2 인스턴스에 대해서 서비스를 분리할 수 있다는 점인데, 인스턴스의 실제 호스트 주소를 엘라스틱서치 설정파일에 넣어줘야 하는 점 때문에 해당 장점이 퇴색된다.

하지만 이런 비슷한 경우는 실제 MSA 구현시에도 빈번히 발생하며, 이것을 해결하는 잘 알려진 방법으로 서비스 디스커버리가 있다.

본 글에서는 단순 키밸류 스토어정도만의 기능이 필요하므로 AWS SSM Parameter Store 를 사용한다.

intial-master-node 가 부트업되면 자신의 호스트명을 등록해두고 나머지 마스터들은 엘라스틱서치를 실행하기전 해당 값을 읽어들여 `cluster.initial_master_nodes` 필드를 설정값에 추가해준다.

### 인스턴스 시스템 설정

Fargate 에서 ES 클러스터를 돌리는 것은 사실 이 문제 때문에 안된다고 보면 되는데, ES7.x 는 `vm.max_map_count` 가 `262144` 보다 작게 시스템 설정이 되어 있으면 동작하지 않는다.
따라서 EC2 에서 인스턴스를 부트업할 때 `UserData` 기능을 통해 아래처럼 해당 값을 설정해줘야한다.

```bash
echo vm.max_map_count=262144 >> /etc/sysctl.conf
sysctl -w vm.max_map_count=262144
```

## 구조

이러한 이유로 CDK 를 디플로이 하면 구축되는 시스템의 모양은 아래와 같다.

![](/assets/img/20200307/elasticsearch.png)

## 마치며

initial master 태스크를 따로 생성해야 한다는 점 때문에, EKS 를 사용하는 것이 더 나은 것 같다는 생각이다. (나혼자만 쓰는 거면 Fargate 도 안쓰고 전부 EKS 로 처리했을 것이다.)

하지만 팀의 상황이 k8s 를 새로 배우고 익히기에는 시간이 부족하기 때문에 저정도의 비직관은 감수할만 한 선택인 것 같다.
또 이미 CDK 만으로 전체 아키텍쳐를 관리하게 구성해둔 경우, EKS 를 적용하는 것은 관리포인트의 증가를 가져오기 때문에 ECS 가 더 나은 선택이다. (굳이 오케스트레이션 툴을 두 개 쓸 필요가 없다..)

----

[^1]: [elasticsearch-cluster-ecs](https://github.com/haandol/elasticsearch-cluster-ecs)
[^2]: [AWS CDK](https://github.com/aws/aws-cdk)
[^3]: [CDKWorkshop](https://cdkworkshop.com/)