---
layout: post
title: 쉽게 설명한 C4Model
excerpt: Demystifying C4Model
author: haandol
email: ldg55d@gmail.com
tags: c4model plantuml c4-plantuml diagram-as-code
publish: true
---

## TL;DR

C4Model 은 다음의 4종류의 다이어그램으로 시스템을 표현하며, 다이어그램의 추상화를 통해 세부구현의 변경에서 다이어그램을 보호한다.

각 다이어그램의 목적은 아래와 같다.

- Context: 가장 추상화된 다이어그램. 외부의 시스템과 얽혀있는 디펜던시(주로 시스템)를 확인한다.
- Container: 목표 시스템을 구성하는 서비스들을 표현하는 다이어그램. 서비스간의 데이터의 흐름을 확인한다.
- Component: 서비스내의 컴포넌트(클래스 등)을 표현하는 다이어그램. 서비스내의 데이터 흐름을 확인한다.
- Code: 최신화(up-to-date) 유지가 불가능하므로 쓰지 않는다.

## 시작하며

개인적으로 다이어그램은 시스템을 설명하기 위한 가장 효과적인 수단이라고 생각하며,

실제로 일을 하다보면, 다른 개발자 또는 다른 부서의 사람들과 다이어그램을 통해서 소통하는 경우가 매우 많다.

다이어그램의 가장 큰 문제점은 같은 시스템을 그리더라도 주제에 따라 그림이 달라진다는 것이다.

같은 시스템을 표현하는 다이어그램이라도 다이어그램을 그리는 의도, 대상으로 하는 청중, 담아야 하는 정보의 양에 따라 달라진다.

또한 위의 요소가 어느정도 고정된 상황에서도 다이어그램을 그리는 사람에 따라 조금씩 다른 그림이 나오기 마련이다.

C4Model 은 이런 문제를 해결하기 위한 다이어그래밍 프레임워크라고 할 수 있다.

개인적으로 생각하는 C4Model 장점은 커뮤니케이션 비용을 크게 줄여줄 수 있다는 것이다.

화이트보딩을 하거나 회의를 할 때, 다이어그램의 이름만 봐도 추상화 정도를 직관적으로 예측할 수 있으며, 다이어그램을 요청할 때 필요한 만큼의 정보를 담고 있는 다이어그램을 요청할 수 있기 때문이다.

예를 들면, 관리자 페르소나 대상으로 주문관리 서비스 컴포넌트 다이어그램 그려둔거 있나요? 같은 식으로 요청할 수 있고, 요청 받은 사람 입장에서도 상대방이 기대하는 추상화 정도와 의도를 정확히 이해할 수 있기 때문에, 커뮤니케이션 비용을 크게 줄일 수 있다.

최근 몇 개의 프로젝트를 C4Model 을 통해 진행하면서 굉장히 만족스러워서, C4Model 에 대한 기본적인 내용들과 실무에 쓸 때 유용한 팁 한두개를 공유하려고 한다.

본 글에서의 다이어그램들은 여행예약시스템[^2] 을 예로 설명한다.

## C4Model 이란

새로운 개념에 대한 공부는 원작자의 발표자료[^1]로 시작하면 좋다.

C4Model 은 `Context, Container, Component, Code` 4종류의 다이어그램으로 시스템을 표현한다.

아래로 내려갈수록 추상화 단계가 낮아지며 시스템의 세부사항을 더 많이 담게 된다. Code 는 실무에서는 거의 사용하지 않는다.

<img src="https://c4model.com/img/c4-overview.png" />

- Context: 가장 추상화된 다이어그램. 외부의 시스템과 얽혀있는 디펜던시(주로 시스템)를 확인한다.
- Container: 목표 시스템을 구성하는 서비스들을 표현하는 다이어그램. 서비스간의 데이터의 흐름을 확인한다.
- Component: 서비스내의 컴포넌트(클래스 등)을 표현하는 다이어그램. 서비스내의 데이터 흐름을 확인한다.
- Code: 최신화(up-to-date) 유지가 불가능하므로 쓰지 않는다.

C4Model 은 대상 시스템에 대해서, 어떤 사람이 해당 시스템을 파악하려고 하든 같은 멘탈모델로 접근할 수 있는 정형화된 문서를 제공한다는 점에서 유용하다.

## Context diagram

> A System Context diagram is a good starting point for diagramming and documenting a software system, allowing you to step back and see the big picture. Draw a diagram showing your system as a box in the centre, surrounded by its users and the other systems that it interacts with. Detail isn't important here as this is your zoomed out view showing a big picture of the system landscape. The focus should be on people (actors, roles, personas, etc) and software systems rather than technologies, protocols and other low-level details.[^3]

컨텍스트 다이어그램은 가장 추상화된 형태의 다이어그램으로 다음의 목적을 가진다.

- 대상 시스템을 중심으로 외부 시스템들과의 디펜던시 또는 데이터의 개략적인 흐름을 확인
- 도메인 바운더리를 확인
- 기술적인 내용을 표시하지 않거나 최소로 표현

아래는 여행예약시스템[^2]의 컨텍스트 다이어그램 예제이다.

<img src="https://github.com/haandol/hexagonal-saga-architecture/blob/main/docs/exports/saga-context.png?raw=true" />

위의 다이어그램으로 시스템에 대해 알수 있는 정보는 다음과 같다.

- 차량, 호텔, 비행기를 한번에 예약해주는 예약시스템이다.
- 대상 시스템은 매우 간단한 시스템으로 디펜던시가 없다.
- 사용자가 직접 이용하는 시스템이다.
- 메시징 시스템을 이용하여 저장소에 데이터를 저장한다.
- 아웃박스 트랜잭션 패턴[^4]을 사용한다.

여행예약시스템이 무엇인지에 대해, 신입사원들이나 마케팅팀에 설명하고자 한다면 이정도 정보로 충분할 것이다. (아웃박스 관련 내용은 빼버려도 될 것이다.)

하지만 개발자들과 이야기하기에는 좀 더 기술적인 정보가 필요할 수 있다. 이럴 때 여행예약 시스템을 줌-인 한, 컨테이너 다이어그램이 유용하다.

## Container diagram

> The next step is to illustrate the high-level technology choices with a Container diagram. _A "container" is something like a web application, mobile app, desktop application, database, file system, etc_. Essentially, a container is a separately deployable unit that executes code or stores data. The Container diagram shows the high-level shape of the software architecture and how responsibilities are distributed across it. It also shows the major technology choices and how the containers communicate with one another

컨테이너 다이어그램은 아래의 목적을 가진다.

- 시스템을 구성하는 바운더리 컨텍스트(e.g. 마이크로 서비스) 를 확인
- 전반적인 데이터의 흐름을 확인
- 데이터를 사용하는 주체가 여럿이면 (사용자, 관리자, 외부 벤더사 등) 여러개의 컨테이너 다이어그램을 만든다.
- 사용된 기술에 대해 최대한 추상적인 정보만 기술 (가능하다면 툴과 버전 정도만 기술한다)

아래는 여행예약시스템의 전체 컨테이너 다이어그램이다.

<img src="https://github.com/haandol/hexagonal-saga-architecture/blob/main/docs/exports/overall-service-container.png?raw=true" />

여행예약시스템은 아웃박스 트랜잭션 패턴을 사용하여 구현되었기 때문에, 총 5개의 마이크로 서비스와 1개의 데몬서비스로 구성되어 있다.

위의 다이어그램은 전체 마이크로 서비스들간의 데이터 흐름과 서비스간의 의존성을 확인할 수 있다.

복잡한 세부 사항들을 한 다이어그램에 모두 담으면 다이어그램을 읽기가 어려워질 수 있다. 따라서, 한 다이어그램은 하나의 목적을 가지게끔 하고, 모든 단계에서 필요하다면 여러개의 다이어그램을 그리는 것을 추천한다.

여행예약시스템의 컨테이너 다이어그램도 두 개로 나누어서 그렸다. 서비스간의 데이터 흐름에 대한 다이어그램(위) 와 각 서비스가 아웃박스 패턴을 어떻게 사용하는지에 대한 다이어그램이 그것이다.

아래 다이어그램은 트립서비스를 기준으로 아웃박스 패턴이 어떤 데이터 흐름을 가지는지 표현하는 컨테이너 다이어그램이다.

<img src="https://github.com/haandol/hexagonal-saga-architecture/blob/main/docs/exports/trip-service-container.png?raw=true" />

위의 다이어그램을 통해 트립서비스가 아웃박스 패턴을 이용하여 사가 서비스 / 릴레이 서비스와 데이터를 주고받는 과정을 확인할 수 있다.

만약 트립서비스 내에서 데이터의 흐름에 대한 논의가 더 필요하다면, 트립서비스를 줌-인 한 컴포넌트 다이어그램을 그리면 된다.

## Component diagram

> Next you can zoom in to each container further to visualise the major structural building blocks and their interactions. The Component diagram shows how a container is made up of a number of components, what each of those components are, their responsibilities and the technology/implementation details. If your components don’t all fit on a single diagram, create multiple versions showing different portions of the container.

컴포넌트 다이어그램은 아래의 목적을 가진다.

- 서비스 내의 데이터 흐름을 확인
- 서비스 구현시 고려해야 할 주요 컴포넌트를 확인. 단, 모든 컴포넌트를 표현할 필요는 없으며, 주로 데이터 흐름에 필수적인 컴포넌트만 표현해도 된다.
- 구현 기술에 대해 가능한 추상적인 정보를 기술. (e.g. trip-service 토픽을 Consume 한다. 등 네트워크 통신방법이나 클래스 단위의 구현만 기술)

## Diagram as Code - C4-PlantUML

일반적인 UI 기반 다이어그램 툴들은 WYSWYG 방식이므로 다이어그램의 수정이 다소 귀찮고(개발자 입장에서), 결과물이 이미지 파일등의 바이너리 이므로 이력추적이 쉽지 않다.

이러한 단점들을 극복하기 위해 다이어그램을 코드로 그리는 경우가 많다.

다이어그램을 XML 형태로 표현하는 Diagrams[^5] 도 있지만 코드만 봐서는 바로 다이어그램을 머리속에 떠올리기 어렵기 때문에, 표준 형태는 아니지만 DSL 를 사용하는 PlantUML 과 Mermaid 를 많이 사용한다.

그 중에서도 PlantUML 은 C4Model 을 좀 더 쉽게 사용할 수 있는 확장인 C4-PlantUML[^6]을 제공하고 있기 때문에, 개인적으로 PlantUML 을 추천한다.

PlantUML 은 아래 글을 읽어보면 대략 사용법을 익힐 수 있다.

- https://github.com/awslabs/aws-icons-for-plantuml/blob/master/AWSSymbols.md
- https://crashedmind.github.io/PlantUMLHitchhikersGuide/aws/aws.html#id1

위에서 예제로 소개한 시스템인, 여행예약 시스템의 C4-PlantUML 예제는 여기[^7]에 있다.

## 마치며

C4Model 의 핵심은, 추상화를 통해 세부사항의 수정으로부터 다이어그램을 지키는 것이다.

코드에서의 추상화와 마찬가지로, 각 다이어그램에서 구체적인 내용을 적을수록 코드의 수정에 따라 다이어그램의 정보가 out-dated 되기 때문이다.

Context 나 Container 다이어그램에서 기술의 세부정보를 넣고 싶더라도 최대한 참는 것이, 문서와 코드를 분리하는 좋은 방법이 된다는 점을 꼭 명심하자.

---

[^1]: [Visualising software architecture with the C4 model](https://www.youtube.com/watch?v=x2-rSnhpw0g)
[^2]: [샘플 시스템 코드](https://github.com/haandol/hexagonal-saga-architecture)
[^3]: [C4Model Cheatsheet](https://c4model.com/assets/visualising-software-architecture.pdf)
[^4]: [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html)
[^5]: [Diagrams](https://www.diagrams.net/)
[^6]: [C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML)
[^7]: [C4 Example](https://github.com/haandol/hexagonal-saga-architecture/tree/main/docs/c4)
