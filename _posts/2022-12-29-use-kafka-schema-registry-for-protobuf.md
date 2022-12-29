---
layout: post
title: Kafka Schema Registry 에서 Protobuf 사용하기
excerpt: Use Kafka schema-registry with Protobuf
author: vincent
email: ldg55d@gmail.com
tags: kafka schema-registry protocol-buffer protobuf
publish: true
---

## TL;DR

코드는 여기[^1]

## 시작하며

이벤트 기반 서비스를 만들다보면 이벤트 스키마가 점점 복잡해지기 마련이다.

이벤트 스키마가 변경되면 보내는 쪽과 받는 쪽을 모두에 영향이 가기 마련인데, 보내는 쪽에서 수정했을 때 받는쪽의 영향을 최소화 하기 위해서는 이벤트 스키마의 compatibility 를 잘 관리해야 한다.

이벤트 스키마의 compatibility 를 관리하는 방법으로 보통, IDL 로 스키마를 표현한 뒤, 이를 코드로 변환하는 방법을 사용한다.

IDL 로 쓰는 언어로는 대표적으로 Avro, Protocol Buffer 가 있다. 이 글에서는 Protocol Buffer 를 기반으로 Confluent 의 Schema Registry 를 사용하는 방법을 설명한다.

## Protocol Buffer

프로토콜 버퍼를 깊이 설명하는 것은 이 글의 범위를 벗어나므로, 간단하게 설명하자면, 구글에서 만든 데이터 직렬화 방식이며, IDL 로 스키마를 표현하고, 이를 코드로 변환하는 방식이다.

코드[^1]에서는 현재 두개의 proto 파일을 이용해서 지정되어 있다.

부모 또는 공용으로 사용되는 idl.Message 와 구체적인 메시지를 나타내는 idl.command.BookCar 가 그것이다.

`idl.Message` 정의는 다음과 같다. 일반적으로 메시지의 프로퍼티들은 가이드라인[^2] 에 따라서 정의한다.

```protobuf
syntax = "proto3";

package idl;
option go_package = "github.com/haandol/protobuf/pkg/idlpb";

message Message {
  string name = 1;
  string version = 2;
  string id = 3;
  string correlation_id = 4;
  string parent_id = 5;
  string created_at = 6;
}
```

그리고 실제 서비스에서 주고받을 구체화된 메시지 포맷인, `idl.command.BookCarBody` 는 다음과 같다.

해당 메시지 포맷은 `base.proto` 에 저장된 `idl.Message` 를 import 하고, 추가로 BookCarBody 를 body 필드로 정의하고 있다.

```protobuf
syntax = "proto3";

package idl.command;
option go_package = "github.com/haandol/protobuf/pkg/idlpb/commandpb";

import "base.proto";

message BookCarBody {
  int32 trip_id = 1;
  uint32 car_id = 2;
}

message BookCar {
  idl.Message message = 1;
  BookCarBody body = 2;
}
```

코드의 README 에 따라 `task idl` 을 실행하면 go 패키지들이 생성되며, 해당 패키지들은 `idlpb.commandpb` 로 사용할 수 있다.

## Schema Registry

패키지를 생성했으면 스키마 레지스트리에 등록하고, 확인해보자.

README 에 따라 도커 컨테이너로 스키마 레지스트리를 실행하고, `task schema` 를 실행하면 스키마가 등록된다.

스키마 레지스트리에 스키마를 등록할 때, compatibility 를 설정할 수 있으며, 기본적으로 `backward` 로 설정되어 있다.

각 compability 모드에 대한 설명은 여기[^3]에서 찾아볼 수 있다. 참고로 `backward` 는 바로 직전 버전의 스키마와 호환되는지 확인하는 것이며, 예제에서는 기본 모드로 사용한다.

```bash
# 스키마 레지스트리 실행
$ docker-compose --profile backend up

# 스키마 레지스트리에 스키마 등록
$ task schema

# 스키마 레지스트리에 등록된 스키마 확인
$ open http://localhost:8081/subjects
```

참고로 AWS 에서도 Glue Schema Registry 를 제공하고 있으며, AVRO 와 Protobuf 를 지원한다.

하지만 `idl.Message` 와 같이 다른 파일에서 지정한 스키마를 사용하는 기능을 References 라고 하는데, 이 기능은 현재 Glue Schema Registry 에서는 지원하지 않는다.

따라서 구조화되지 않은 스키마를 사용하는 경우에만 glue schema registry 를 사용할 수 있다.

## 스키마 호환성 확인

위에서 언급했듯, `backward` 모드로 설정되어 있기 때문에, 직전 버전의 스키마와 호환되지 않으면 등록이 되지 않는다.

```protobuf
syntax = "proto3";

package idl.command;
option go_package = "github.com/haandol/protobuf/pkg/idlpb/commandpb";

import "base.proto";

message BookCarBody {
  int32 trip_id = 1;
  uint32 car_id = 2;
}

message BookCar {
  // 메시지 순서때문에 이전 버전의 스키마와 호환되지 않는다.
  required string source = 1;
  idl.Message message = 2;
  BookCarBody body = 3;
}
```

위와 같이 `car.proto`[^4] 를 수정하고 스키마를 등록하면 아래와 같은 에러가 발생한다.

```bash
$ task schema
2022-12-28T23:38:09.672+0900    ERROR   schema/main.go:37       failed to check compatibility   {"module": "main", "error": "unable to POST \"http://schema-registry:8081/compatibility/subjects/message.Message/versions/latest?verbose=true\": Post \"http://schema-registry:8081/compatibility/subjects/message.Message/versions/latest?verbose=true\": EOF"}
```

## 마치며

개인적으로 카프카만 고려할 땐 AVRO 가 더 좋은 선택일거 같지만, gRPC 를 사용할 것을 고려하면 IDL 을 하나로 통일하는게 좋을 것 같다.

따라서 팀에서 gRPC 를 쓰는 경우는 Protobuf 를 사용하고, 그렇지 않은 경우는 AVRO 를 사용하는 것을 추천한다.

또한 직렬화 하면 데이터 크기가 확연히 줄어들긴 하지만, 직렬화를 도입해서 생기는 복잡성 또한 만만치 않게 크기 때문에 직렬화를 도입할 때는 신중하게 고려해야 한다.

---

[^1]: [Go kafka schema-registry using Protobuf](https://github.com/haandol/go-protobuf-schema-registry)
[^2]: [Message Properties](https://codeopinion.com/message-properties/)
[^3]: [Schema Evolution and Compatibility](https://docs.confluent.io/platform/current/schema-registry/avro.html)
[^4]: [car proto 파일](https://github.com/haandol/go-protobuf-schema-registry/blob/main/idl/commandpb/car.proto)
