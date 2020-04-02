---
layout: post
title: Python 에서 Numpy 배열을 효과적으로 Serialization 하는 방법
excerpt: Serialize numpy array efficiently in Python
author: vincent
email: ldg55d@gmail.com
tags: serialization python array numpy sagemaker-endpoint
publish: true
---

## TL;DR

base64 인코딩을 꼭 해야하는 게 아니라면 `numpy.tobytes()`

# 시작하며

Sagemaker Endpoint 로 모델을 서빙하다보면 이미지를 포함해서 다양한 형태의 벡터를 직렬화/역직렬화 해야한다.

아래와 같이 아무생각없이(하던대로) base64 로 인코딩해서 전달하다보니,

```python
import json
import numpy as np
from base64 import encodebytes, decodebytes

size = (9, 128, 64, 3)
x = np.random.uniform(0.0, 1.0, size=size)

serialized = encodebytes(json.dumps(x.tolist()).encode('utf-8')).decode('utf-8')
deserialized = json.loads(decodebytes(serialized.encode('utf-8')).decode('utf-8'))
print(np.asarray(deserialized).shape)

>>> (9, 128, 64, 3)
```

엔드포인트에서 전달받은 배열을 가공하는 시간이 전체 round-robin 시간의 대부분을 잡아먹게 되었다.

마침 Sagemaker Endpoint 는 사용자 지정 형태의 content type 을 받을 수 있게 되어 있다.

content type 이 반드시 string 이 아니어도 되는 경우 더 좋은 방법이 없을까?

# Benchmark 참고

여기[^1] 를 보면 대부분의 직렬화/역직렬화 에 대한 벤치마크를 해놨다.

저 벤치마크를 한줄 요약하면 `msgpack` 을 쓰면 된다. RabbitMQ 도 메시지를 직렬화하는 기본 알고리즘으로 *msgpack* 을 사용하고 있을 정도로 검증된 방법이다.

msgpack 으로 *(9, 128, 64, 3) shaped numpy.array* 를 직렬화 하는 것은 아래와 같다

```python
import msgpack
import numpy as np

size = (9, 128, 64, 3)
x = np.random.uniform(0.0, 1.0, size=size)

array = msgpack.packb(x.tolist(), use_bin_type=True)
restored = msgpack.unpackb(array, use_list=True, raw=False)
print(np.asarray(restored).shape)

>>> (9, 128, 64, 3)
```

msgpack 을 쓰면 base64 결과보다 크기가 1/3로 줄어들고 속도도 15% 정도 더 빨라진다.

base64 코드는 평균 0.192초 정도 걸리고 msgpack 은 평균 0.156초 정도 걸린다.

엄청 느리지는 않지만 내가 원하는만큼 빠르지는 않다.

# 더 나은방법은 없는가?

내가 가지고 있는 배열은 이미 numpy 이다.

numpy 를 바로 보내면 이런저런 처리 하는 것보다 속도가 빠르지 않을까?

`numpy.tolist()` 가 아니라 `numpy.bytes()` 를 이용해서 보내면 좋을 것 같다.

```python
import msgpack
import numpy as np

size = (9, 128, 64, 3)
x = np.random.uniform(0.0, 1.0, size=size)

serialized = msgpack.packb(x.tobytes(), use_bin_type=True).decode('utf-8')
deserialized = msgpack.unpackb(serialized, use_list=False, raw=True)
print(np.frombuffer(deserialized, dtype=x.dtype).reshape(x.shape).shape)

>>> (9, 128, 64, 3)
```

`np.tolist()` 를 `np.tobytes()` 로 바꾸면 대략 `3000배` 차이가 난다. *0.000051* 초 정도 걸린다. 데이터 크기는 tolist 와 큰 차이는 없다.

*np.tobytes()* 의 단점은 shape 가 보존되지 않는다는 점이다. *frombuffer* 로 읽어낸 뒤에 기존의 shape 를 전달받아 *reshape* 를 해줘야한다.

엔드포인트에 외부 라이브러리 임포팅을 하기 싫었지만 3000배 차이면 임포팅을 할 수 밖에 없었다. 결국 msgpack 도 지워버리고 `application/x-npy` 형태로 numpy.array 를 그대로 보내서 50% 이상 속도를 올릴 수 있었다. (shape 는 헤더에 실어서 보냈다.)

# 마치며

base64 는 스트링 형태로 데이터를 가공해야한다면 어쩔 수 없이 써야한다. 하지만 어플리케이션이 페이로드를 byte 형태로 받을 수 있다면 msgpack 을 쓰는게 낫다.

Protobuffer 는 크기를 줄이는데는 효과적이지만, 직렬화/역직렬화를 빠르게 처리하는데는 큰 강점이 없다.

여기엔 적어두지 않았지만 Arrow(with ray)[^2] 가 큰 벡터를 처리하는데 효과적으로 설계되었다고 해서 실험해봤다. 하지만 msgpack 이랑 속도차이가 엄청 크지 않았다.

----

[^1]: [Python Serialization Benchmarks](https://medium.com/@shmulikamar/python-serialization-benchmarks-8e5bb700530b)
[^2]: [Fast Python Serialization with Ray and Apache Arrow](https://arrow.apache.org/blog/2017/10/15/fast-python-serialization-with-ray-and-arrow/)