---
layout: post
title: CosineSimilarity using Elasticsearch
excerpt: use dense_vector on Elasticsearch
author: vincent
email: ldg55d@gmail.com
tags: elasticsearch dense_vector cosineSimiarity dotProduct es
publish: true
---

## TL;DR

코드는 여기[^1]

Elasticsearch 7.3+ 부터 지원되는 `dotProduct` 또는 `consineSimiarity` 를 사용하여 유사도를 계산한다. (`dense_vector` 는 7.0 부터 지원되었지만 위의 기능들이 없기 때문에 플러그인이나 직접 구현을 통해 사용해야한다.)

## 시작하며

몇년 전에 이미지를 입력하면 동일한 상품 목록을 가져오는 프로젝트를 한 적 이 있다.
이미지에서 SIFT를 뽑고 LSH 로 해싱한 뒤, 해당 결과를 Elasticsearch(이하 ES) 에 쌓아서 동일한 상품 검색을 구현했다. 동일한 상품은 잘 찾지만 비슷한 상품을 검색하는 것에 있어서 SIFT 피쳐의 성능은 상당히 떨어졌었다. 

이번에 진행한 프로젝트에서는 동일한 상품 뿐만 아니라 비슷한 상품도 잘 찾아야 했는데, 입력값의 피쳐의 분포를 보니 cosineSimiarity 가 가까울 수록 비슷한 상품이라는 특성을 가지고 있었다. 대량의 모집단에 대해서 consineSimiarity 를 빠르게 수행할 수 있는 툴로 예전에 썼던 ES가 생각나서 사용했 고 결과가 나쁘지 않았다.

본 글에서는 `ES` 에서 `dotProduct` 를 사용하는 방법을 알아본다. 단 위에서 설명한 작업에서는 dotProduct 와 consineSimiarity 는 사실상 같은 역할을 하기 때문에 앞으로 `dotProduct` 로 통일해서 말하겠다. ~~타이핑 하기 편함~~

## 요구사항

ES 에서 dotProduct 를 사용하려면 `dense_vector` 타입으로 인덱스의 필드가 매핑되어 있어야 한다.

`dense_vector` 타입은 ES 7.x 에서 지원된다.[^2] 문서에는 7.x 로 퉁쳐져서 모든 기능이 지원되는 것처럼 나오지만, `dotProduct` 함수는 7.3+ 에서만 지원된다.[^3]
따라서 `7.5.1` 버전을 설치해서 진행하는 것을 추천한다. ~~사용할 파이썬 라이브러리 최신이 7.5.1 이라서~~

## Elasticsearch 설치

제일 쉬운방식은 역시 도커로 설치하는 것이다.

```bash
$ docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.5.1
```

이후 curl 을 날려서 확인해보면 잘 뜨는 것을 확인할 수 있다.

```bash
$ curl -X GET http://localhost:9200
{
  "name" : "1c993be83823",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "-RlyuqqhTEKY9N2StM-WjA",
  "version" : {
    "number" : "7.5.1",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "7f634e9f44834fbc12724506cc1da681b0c3b1e3",
    "build_date" : "2020-02-06T00:09:00.449973Z",
    "build_snapshot" : false,
    "lucene_version" : "8.4.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

## 인덱스 생성 및 매핑

ES 는 인덱스에 대한 POST 요청시 인덱스가 없으면 알아서 필드를 판단해서 인덱스를 생성하고 매핑해준다.

하지만 vector 형태의 데이터를 밀어넣으면 double 형태로 구성을 하기 때문에 dotProduct 가 동작하지 않는다. 또한 double 형태의 필드에 대해 직접 dot을 구현해서 처리하려고 해도, 필드 인덱싱을 해버리기 때문에 원하는 결과를 얻을 수 없다. (즉,  [.4, .1, .2, .3] 을 넣으면 [.1, .2, .3, .4] 로 정렬해서 저장한다.) 프로덕션에서도 모종의 이유로~~버그?!~~ 동일한 필드에 숫자, 문자가 섞여서 들어오는 경우도 있기 때문에 보통은 인덱스를 먼저 매핑해두고 사용하는 것이 안전하다.

python을 이용하여 인덱스를 매핑해보자.(curl 로 해도 되지만 재사용을 위해서) 먼저 ES 버전에 맞는 클라이언트 라이브러리를 설치한다.

```bash
$ pip install elasticsearch==7.5.1
```

이후 로컬호스트에 설치된 ES 에 인덱스를 생성해준다. 여기서는 `features` 라는 이름의 인덱스를 생성하고, 인덱스의 `feature` 필드를 `dense_vector` 로 설정해준다. `dims` 에서 해당 벡터의 차원수를 입력해줘야하는데 다차원 지원은 하지 않기 때문에, 다차원 데이터를 인덱싱할 땐 flatten 작업을 해야한다. 여기서는 128 차원으로 입력했다.

```python
from pprint import pprint
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=['http://localhost'], port='9200')

es.indices.create(index='features', body={
  "mappings": {
    "properties": {
      "feature": {
        "type": "dense_vector",
        "dims": 128,
      },
      "image_id": {
        "type": "text"
      }
    }
  }
}, ignore=400)
```

인덱스가 잘 생성되었는지 확인해본다.

```python
pprint(es.indices.get(index='features'))
```

## 인덱스 쿼리

생성한 인덱스에 dotProduct 를 이용하여 쿼리를 해보자.

```python
import random
from pprint import pprint
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=['http://localhost'], port='9200')

res = es.search(index='features', body={
      'query': {
        'script_score': {
          'query': {
            'match_all': {}
          },
          'script': {
            'source': "dotProduct(params.query_vector, doc['feature']) + 1.0",
            'params': {
              'query_vector': [random.gauss(0, 0.432) for _ in range(128)],
            }
          }
        }
      }
    })
pprint(res['hits']['hits'])
```

현재는 데이터가 없기 때문에 빈 리스트가 보이겠지만 에러가 없다면 성공이다.
피쳐를 넣고 뽑는 것은 글의 범위를 벗어나기 때문에 ~~귀찮고 쉽다~~ 생략한다.

## 마치며

dotProduct, consineSimialrity 같은 쿼리를 쉽게 할 수 있는 분산 저장소가 딱히 없어서 고민이었는데 ES 에서 지원해줘서 정말 편안하게 개발할 수 있다.

하지만 Amazon Elasticsearch 는 아직 7.1 까지 밖에 지원을 안하고 있어서[^4] AWS 와 연동해서 쓰려면 ECS EC2 등으로 직접구성해서 써야한다는 점이 아쉽다. ~~현재 열심히 건의하고 있으니 곧 지원해주지 않을까...~~

----

[^1]: [es-dense-vector-tutorial](https://github.com/haandol/es-dense-vector-tutorial/blob/master/Elasticsearch.ipynb)
[^2]: [Script Score Query](https://www.elastic.co/guide/en/elasticsearch/reference/7.x/query-dsl-script-score-query.html)
[^3]: [Elasticsearch 7.3.0 released](https://www.elastic.co/kr/blog/elasticsearch-7-3-0-released)
[^4]: [Amazon Elasticsearch Service FAQ](https://aws.amazon.com/ko/elasticsearch-service/faqs/?nc=sn&loc=6)