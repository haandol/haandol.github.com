---
layout: post
title: MSK 카프카 모니터링 메트릭
excerpt: basic metrics for monitoring MSK(Kafka)
author: vincent
email: ldg55d@gmail.com
tags: msk kafka monitoring metrics cdk
publish: true
---

## TL;DR

코드는 여기[^1]

## MSK Configuration

https://docs.aws.amazon.com/msk/latest/developerguide/metrics-details.html

- MSK 는 4 단계의 모니터링 설정을 제공하고 있으며 기본 메트릭은 무료로 제공되나 상세 메트릭들은 비용 발생
  - DEFAULT
    - 클러스터 및 브로커 단위의 기본 메트릭 제공(CPU 사용량, 디스크 사용량, 네트워크 사용량 등)
  - PER_BROKER
    - 브로커단위 상세한 모니터링 제공
  - PER_TOPIC_PER_BROKER
    - 토픽 단위 모니터링 제공
  - PER_TOPIC_PER_PARTITION
    - 파티션 단위 모니터링
- MSK 의 설정화면에서 언제든 변경 가능하다.
  - 일부 모니터링 메트릭은 카프카 버전 2.2.1 이상 필요
  - 기본 권장 버전은 2.8.1
- 해당 설정을 마치고 나면 클라우드워치에서 각 메트릭을 확인할 수 있다.

## Key metrics to watch

https://docs.aws.amazon.com/msk/latest/developerguide/bestpractices.html
https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/
https://www.youtube.com/watch?v=R6OKibnXpBs

- 브로커 사이드(인프라)의 모니터링, 컨슈머/프로듀서(어플리케이션) 사이드의 모니터링이 필요
- 각 매트릭은 모두 클라우드워치에 쌓이게 되며, 알람을 설정해서 모니터링 할 수 있다.

### Infrastructure metric

- Number of active controller [1] - `ActiveControllerCount`
  - 클러스터에 액티브 컨트롤러는 반드시 1개여야 한다.
  - 브로커중의 한개가 주키퍼를 통해 액티브 컨트롤러로 지정된다.
- Number of under-replicated partitions [0] - `UnderReplicatedPartitions`
  - 노드의 CPU, 메모리 혹은 디스크 공간이 부족하여 파티션 리더로부터 데이터 싱크가 이뤄지지 않고 있는 파티션 개수
- Number of offline partitions [0] - `OfflinePartitionsCount`
  - CPU, 메모리 혹은 디스크 공간이 부족하여 파티션 리더가 데이터를 더이상 적재하지 못하는 경우 0 이상이 된다.
- Number of partitions per broker (< 4000) - `PartitionCount`
  - 브로커가 커버할 수 있는 파티션개수는 브로커의 종류에 따라 다르다. 최대 4000개 까지 권장되며,
  - 해당 수치가 넘으면 브로커의 기능은 동작하지만 MSK 를 통한 브로커 설정 등의 불가능해진다.
- CPU/Mem usage (< 60%) - `CpuUser`
  - CPU User + CPU System < 60%
  - 브로커 노드가 죽거나 추가되면 파티션이 각 노드로 재배치되는데, 재배치는 파티션의 복제를 의미함.
  - 기존에 처리중인 작업들의 영향이 없이, 추가로 재배치 작업을 노드가 처리하려면 대략 40% 의 CPU 가 가용하도록 유지하는 것을 추천
  - 메모리도 동일한 기준
- Disk usage (< 85%) - `KafkaDataLogsDiskUsed`
  - 카프카는 각 토픽별 리텐션 정책에 맞춰서 데이터를 디스크에 가지고 있기 때문에 디스크 사용량을 확인해줘야한다.

### Application metrics

- Maximum offset lag across all partitions in the topic - MaxOffsetLag
  - 토픽에 포함된 파티션중 가장 높은 오프셋 렉, 특정 파티션의 문제는 특정 노드의 문제일 가능성이 높다.
  - 0에 가까울 수록 좋다.
- Partition lag per consumer (< depends on service) - OffsetLag
  - 각 파티션에 현재 쌓인 메시지수 - 컨슈머의 파티션 오프셋 = 컨슈머가 처리하는 속도가 메시지 쌓이는 속도를 못따라갈 경우 발생.
  - 0에 가까울 수록 좋다.
- Number of messages received per topic - MessagesInPerSec
  - 토픽에 메시지가 들어오는 수.
  - 0 이면 토픽에 프로듀서에 문제가 있을 수도 있다.

## Datadog / Prometheus

https://docs.datadoghq.com/integrations/amazon_msk/#installationhttps://quip-amazon.com/hgaOA3QTzbrm

- 카프카에서 제공하는 메트릭은 대부분 클라우드워치에서 제공된다.
- MSK 에서 제공하는 모니터링 및 메트릭을 쓰지 않고 데이터독이나 프로메테우스로 직접 모니터링 시스템을 구축할 경우 open monitoring 을 옵션을 켜고 모니터링 환경을 직접 구성할 수 있다.
- 데이터독에서 제공하는 매뉴얼대로 설정하면 된다.
  - msk 에서 open monitoring 활성화
  - EC2 를 msk vpc 에 띄운다.
  - datadog agent 를 설정한다.

---

[^1]: [MSK Observability Demo](https://github.com/haandol/msk-observability)
