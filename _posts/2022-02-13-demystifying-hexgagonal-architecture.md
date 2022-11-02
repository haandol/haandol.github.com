---
layout: post
title: 쉽게 설명한 클린 / 헥사고날 아키텍쳐
excerpt: Demystifying hexagonal(ports and adapters) architecture
author: vincent
email: ldg55d@gmail.com
tags: hexagonal-architecture clean-architecture architecture ports-and-adapters onion
publish: true
---

## TL;DR

Ports: 인터페이스, DI(Dependency Inversion) 를 위한 추상화

Adapters: 포트를 통해 인프라와 실제로 연결하는 부분만 담당하는 구현체

Domain Model: 실제 핵심 비즈니스 로직을 처리하는 부분

Domain Service(클린 아키텍쳐에서의 UseCase): 도메인 모델과 어댑터를 이용해서 비즈니스 로직과 인프라를 오케스트레이션 하는 dumb한 레이어

> 도메인 모델이 빈약(amnemic) 하다면, 그냥 레이어드 아키텍쳐에 SOLID 를 잘 지켜서 개발하기만 해도 충분하다.

## 시작하며

너무 빨리 적응하려고 나댔던 탓인지, 입사 둘째주부터 바로 서비스 개발을 시작하게 되었다.

이제는 프로토타이핑이 아니라 프로덕션용 코드(생명주기가 길 것으로 예상되는 코드)를 작성하다보니 기존의 코드스타일로는 테스트 작성과 유지보수가 쉽지 않을 것이 눈에 선했다.

그래서 예전부터 공부만 해두고 써먹지 못했던 헥사고날(a.k.a 포트앤어댑터 / 어니언) 아키텍쳐를 적용해보기로 했다. (개인적으로는 포트앤어댑터로 부르는 것을 더 좋아한다.)

약 4주 동안 다양한 아티클과 영상을 보고, 코드를 쉴새 두드리고 다듬은 뒤에 제대로 된 서비스가 만들어졌고, 그 결과 헥사고날에 대해 가벼운 토론을 할 수 있을 정도로는 이해할 수 있게 되었다.

본 글에서는 헥사고날 아키텍쳐에 대한 설명과 각 컴포넌트들, 그리고 특별히 웹서비스 구현시에 고려할만한 내용을 정리해본다.

## 헥사고날 아키텍쳐가 무엇인가?

어떤 과정을 거쳐서 지금의 클린/헥사고날 아키텍쳐가 나오게 되었는지 이 글[^1] 에서 상당히 잘 설명해주고 있다.

헥사고날 아키텍쳐와 클린 아키텍쳐를 섞어서 설명하기 때문에 그림이나 전체적인 개념이 좀 뒤섞여 있지만, 근본적으로 해결하고 싶은 문제는 동일하기 때문에 대략의 개념을 잡기 위해 읽는데는 문제가 없는 것 같다.

<img src="https://miro.medium.com/max/1400/0*mL1DFwnX4TU5kQZJ"/>

클린/헥사고날 아키텍쳐를 요약하면 `비즈니스 로직(도메인 모델)을 인프라(외부세계)에서 분리한다` 는 것이다.

위의 그림에서 보듯이 엔티티(또는 도메인 모델) 가 가장 안에 있고, 엔티티에 접근하기 위해서는 밖의 레이어들을 거쳐서 들어올 수 밖에 없다.

의존성은 반드시 밖에서 안으로만 존재하며 안쪽에 있는 레이어는 밖의 레이어에 대해서 알면 안된다.

클린 아키텍쳐와 헥사고날 아키텍쳐는 위의 `분리`를 구현하는 방식의 차이가 있을 뿐 실제로 동작하는 코드를 보면 데이터의 흐름은 비슷한 형태로 흐른다.

클린 아키텍쳐의 동작과정은 이 영상[^3] 을 보면 쉽게 이해할 수 있다.

개인적으로는 클린 아키텍쳐보다 헥사고날 아키텍쳐를 더 좋아하는데, 다른 이름인 포트와 어댑터라는 이름과 동작이 더 직관적이며, 조금이나마 더 단순한 형태라 람다와 잘 맞기 때문이다..

### 레이어드 아키텍쳐와의 차이

위의 내용만 읽어보면 기존에 잘 사용하고 있던 레이어드 아키텍쳐와 큰 차이가 안느껴지는 것 같다.

<img src="https://scontent-gmp1-1.xx.fbcdn.net/v/t31.18172-8/1540295_692860860764154_1601487017_o.jpg?_nc_cat=108&ccb=1-5&_nc_sid=09cbfe&_nc_ohc=ytmLlCBSmpUAX9kEVog&_nc_ht=scontent-gmp1-1.xx&oh=00_AT_Sd9C-BGX__Z6beUOeao_E-0UpeoGTJhV0Mdq-XvOH_A&oe=622E2795"/>

레이어드 아키텍쳐도 비즈니스 로직 레이어를 외부와 분리하기 위해서 나온 아키텍쳐이기 때문이다.

실제로 SOLID를 잘 적용한 레이어드 아키텍쳐는 클린아키텍쳐의 장점을 상당부분 누릴 수 있다고 생각한다.

하지만 이 글[^2]에 설명되어 있듯이, UseCase 또는 포트 라는 추상화를 도입해서 의존성을 역전하는 것이 가장 큰 차이점이라고 볼 수 있으며, 대부분 추상화 계층을 도입하면 의존성을 줄일 수 있지만 복잡도가 올라간다.

클린 아키텍쳐에서 이렇게 복잡도를 올리면서까지 외부에 대한 의존성을 완전히 제거한 것이 `엔티티 또는 도메인 모델`이므로, 클린 아키텍쳐와 레이어드 아키텍쳐의 가장 큰 차이점은 도메인모델의 유무라고도 볼 수 있다.

도메인 모델은 기존의 데이터 중심의 비즈니스 로직이 구성이 아니라 사용자의 유즈케이스를 중심으로 비즈니스 로직이 구성된다.

따라서 비즈니스 로직이 레이어 아키텍쳐의 전체 레이어 관통하는 유즈케이스의 집합으로 구성된다. (그리고 각 유즈케이스간에는 의존성이 없다.)

<img src="https://jimmybogardsblog.blob.core.windows.net/jimmybogardsblog/3/2018/Picture0030.png"/>

따라서 도메인 모델이 빈약하거나 없다시피 한 설계에서는 SOLID 를 잘 고려한 레이어드 아키텍쳐가 더 좋을 것이다.

## 헥사고날 아키텍쳐를 구성하는 요소

너무 클린 아키텍쳐 중심으로 설명되었는데, 이 영상[^4]은 좀 더 헥사고날에 집중해서 잘 설명하고 있다.

<img src="https://res.cloudinary.com/practicaldev/image/fetch/s--43uphorj--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/33ru7jmqzice8bfsq8of.png"/>

다른 글들에서는 여러가지 새로운 컴포넌트들을 추가해서 구현하는 경우가 많은데, 위의 그림에 나온 컴포넌트들만으로도 충분히 구현할 수 있다.

사용자의 요청은 왼쪽에서 들어와서 오른쪽으로 처리되며, 사용자 요청의 처리흐름을 대략 소개하면,

1. 좌측의 Adapters 를 통해 사용자의 요청을 받아서 어플리케이션 서비스에 전달한다. 이 때 서비스와 어댑터는 포트를 이용해서 인터페이스를 맞춘다. (어댑터 디자인패턴 같은 느낌)
2. 어플리케이션 서비스는 들어온 요청을 도메인 모델로 전달한다.
3. 도메인 모델은 전달받은 요청으로 비즈니스 모델을 처리하고 우측에 있는 어댑터들을 통해 외부의 데이터를 가져오거나 처리된 데이터를 외부로 저장한다.
4. 어플리케이션 서비스는 도메인 모델의 결과를 사용자에게 반환해준다.

위에 소개했던 링크들만 읽어도 여기까지 이해가 잘 되지만, 막상 구현을 하려면 무슨 컴포넌트를 어떤 식으로 만들고 사용해야 하는지가 막막하다.

아래에서는 각 컴포넌트들에 대한 설명과, 구현시에 각 컴포넌트들의 역할을 좀 더 명확히 설명해보겠다.

### Adapters

앞에서 본 그림에서 어댑터는 2가지 종류가 있는데, 왼쪽에 사용자의 요청을 받아들일때 사용되는 어댑터를 primary adapter 라고 부르고, 우측에 있는 도메인 모델의 처리에 사용되는 어댑터를 secondary adapter 라고 부른다.

### Primary Adapter

실제로 구현하는 경우 이벤트 드리븐 서비스로 구성될 경우에는 primary adapter 의 역할이 명확하지만, 웹 서비스의 경우에는 약간 모호해지는 것 같다.

따라서 primary adapter 는 웹 프레임워크들의 controller 또는 람다의 handler 와 같은 개념에 통합되어 사용되며 아래에 소개할 어플리케이션 서비스를 인스턴스화 하여 비즈니스 로직을 실행하고 결과를 사용자에게 반환해준다.

아래 코드는 MSK 토픽의 다운스트림으로 설정한 람다 핸들러 코드이다.

```typescript
import TaskRepository from '../adapters/dynamodb-task-repository';
import JobRepository from '../adapters/dynamodb-job-repository';

var taskService: TaskService;
var coldStart: boolean = true;

function bootstrap() {
  if (coldStart) {
    const tableName = process.env.TABLE_NAME!;
    assert.ok(tableName, 'env TABLE_NAME is required');
    const gs1IndexName = process.env.GS1_INDEX_NAME!;
    assert.ok(gs1IndexName, 'env GS1_INDEX_NAME is required');

    const dynamodb = new AWS.DynamoDB.DocumentClient({ service: new AWS.DynamoDB() });
    taskService = new TaskService(
      new TaskRepository(dynamodb, tableName),
      new JobRepository(dynamodb, tableName, gs1IndexName),
    );
    coldStart = false;
  }
}

export const handler = async (event: MSKEvent, context: Context): Promise<void> => {
    console.debug(JSON.stringify(event));

    bootstrap();

    const records = filterRecords(event);
    const commands = records.map<CreateTaskCommand>(decodeRecord);

    const tasks = commands.map(command => command.task).filter(Boolean);

    const results = await taskService.createTasksAndJobs(tasks);

    return;
  }
);
```

primary adapter 는 먼저 클라이언트로 부터 입력받은 값의 유효성을 체크하고 적절한 형태로 가공한다.

TaskRepository, JobRepository 라는 `dynamodb 어댑터`들을 가져와서 `어플리케이션 서비스`인 TaskService 를 생성하고 호출한다.

TaskService 는 도메인 모델을 통해 비즈니스 로직을 실행하여, 태스크와 잡들을 생성해준다.

(실제 만들어지는 객체들의 의미보다 primary adapter 로서의 handler 역할에 집중하자.)

## Secondary Adapter

생성된 어플리케이션 서비스는 내부에서 도메인모델을 호출하게 된다.

도메인 모델도 외부와의 통신이 필요한 작업이 있을 수 있다.

이 경우 도메인 모델은 포트를 통해 우측에 있는 어댑터를 호출 할 수 있다.

아래는 다이나모디비와 통신할때 사용하는 어댑터이다.

```typescript
import { Task } from '../interfaces/task';
import { TaskRepository } from '../ports/task';

class DynamoDBAdapter implements TaskRepository {
  constructor(
    readonly client: AWS.DynamoDB.DocumentClient,
    readonly tableName: string,
  ) { }

  async save(task: ITask): Promise<boolean> {
    if (await this.isExists(task.id)) {
      return false;
    }

    await this.client.put({
      TableName: this.tableName,
      Item: {
        PK: TaskSchema.Task.PK(task.id),
        SK: TaskSchema.Task.SK(task.id),
        ...task,
      },
      ConditionExpression: 'attribute_not_exists(PK) AND attribute_not_exists(SK)',
    }).promise();
    return true;
  }

  async listTasks(): Promise<ITask[]> {
    const items = await this.client.query({
      TableName: this.tableName
      Key: {
        PK: 'TASK#RECENT',
      },
    });
    return items.Item ? items.Item as ITask[] : [];
  }
}
```

secondary adapter 는 외부와의 통신에 대한 구현만 담당한다. (primary adapter 도 마찬가지)

두 어댑터의 가장 큰 특징은, DIP(Dependency Inversion Principal) 를 기반으로 하고 있다는 점이다.

primary adapter 는 서비스에 주입(injection) 되어 서비스에 의해 호출되고,

```typescript
// Inside Primary Adapter

taskService = new TaskService(
  new TaskRepository(dynamodb, tableName),
  new JobRepository(dynamodb, tableName, gs1IndexName),
);
```

secondary adapter 는 도메인 모델에 주입되어 도메인 모델에 의해 호출된다.

```typescript
// Inside Domain Model

async save(repo: TaskRepository): Promise<void> {
  await repo.save({
    id: this.id,
    name: this.name,
    topic: this.topic,
    startAt: this.startAt,
    meta: this.meta,
    description: this.description,
  });
}
```

그리고 두 어댑터 모두 비즈니스 로직은 전혀 들어가지 않는다.

### Ports 

포트는 단순히 인터페이스이다. 어댑터는 이 포트를 implements 하여 실제 동작을 구현하게 된다.

```typescript
import { ITask } from '../interfaces/task';

export interface TaskRepository {
  save(task: ITask): Promise<boolean>; 
  listTasks(): Promise<ITask[]>;
}
```

파이썬3을 쓰는 경우 ABC 보다 Protocol 을 쓰는 것이 좀 더 유연하게 작업할 수 있다.

### Applcation Service / UseCase

<img src="/assets/img/2022/0213/hexagonal.jpg" />

사용자 요청이 왼쪽에서 오른쪽으로만 들어온다는 것을 확실히 인지하고 있다면, 2중 헥사곤의 첫 그림도 명확하게 다가올 것이다.

하지만 처음 헥사고날을 접하는 사람에게는 위의 그림이 조금 더 어플리케이션 서비스를 명확히 보여주는 것 같기도 하다. 

위의 그림대로 primary adapter 를 통해 어플리케이션 서비스를 생성(instantiation) 해주고 해당 서비스가 클라이언트에 대한 반환을 책임진다.

```typescript
import { ITask } from '../interfaces/task';
import { Task } from '../domain/task';
import { TaskRepository } from '../ports/task';
import { JobRepository } from '../ports/job';

class TaskService {
  constructor(
    private readonly taskRepo: TaskRepository,
    private readonly jobRepo: JobRepository,
  ) { }

  toTask(task: ITask) {
    return new Task({ ...task });
  }

  async createJobsForTasks() {
    const dtoTasks = await taskRepo.listTasks();
    const tasks = dtoTasks.map(toTask);
    await Promise.all(
      tasks.map(task => task.schedulNextJob()),
    );
  }
}

export default TaskService;
```

<img src="https://res.cloudinary.com/practicaldev/image/fetch/s--43uphorj--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/33ru7jmqzice8bfsq8of.png"/>

위의 그림에서 어플리케이션 서비스에서만 도메인 모델과 포트에 모두 대한 의존성이 있다. 의존성은 import 가 가능하다고 해석해도 틀리지 않다.

따라서 어플리케이션 서비스는 어댑터들과 도메인모델의 오케스트레이션을 담당하게 된다.
(도메인 이벤트를 이벤트 버스로 보내준다거나 하는 작업도 여기서 한다.)

#### 도메인 객체는 어디서 만들지?

원래 DDD 에서 레포지토리는 도메인 객체를 직접 외부에서 가져오고 저장하는 것이 자연스럽다. 그래서 많은 예제들에서도 레포지토리는 예외적으로 도메인객체를 바로 리턴한다.

그래서 DDD 를 아는 사람은 서비스에서 도메인 객체를 만드는 toTask 부분이 이상하다고 볼 수도 있는데, 사실 이는 선택의 문제이다.

도메인 객체는 서비스를 벗어날 수 없기 때문에, 서비스에서 레포지토리를 통해 받은 도메인 객체를 primary adapter 로 전달할 때 어차피 dto 로 변환해줘야한다.

따라서 레포지토리에서 다룰 값을 dto로 할지 도메인 객체로 할지를 정해야하는데(선택의 문제), 서비스만이 도메인객체를 인스턴스화 할 수 있다고 룰을 정해두고 쓰는 것이 위의 그림과 동일하므로, 가능하면 서비스에서만 도메인객체를 다루려고 하는 편이다.

### Domain Model / Entities

도메인 모델은 모든 비즈니스 로직이 포함된다.

도메인 모델은 서비스를 벗어나서는 안된다. 서비스를 벗어나야 하는 경우 반드시 사전에 DTO(Data Transfer Object)로 변경되어야 한다.

아래는 예제를 위해 간단한 작업만 있지만, 실제로 엔티티에 변경이 일어나야 하는 모든 작업이 여기에 구현되어 있어야 한다.

```typescript
import { JobRepository } from '../ports/job';
import { TaskRepository } from '../ports/task';

export interface TaskProps {
  readonly id: string,
  readonly name: string,
  readonly topic: string,
  readonly startAt: string,
  readonly meta: { [key: string]: string };
  readonly description?: string,
  readonly updatedAt?: string,
}

export class Task {
  readonly id: string;
  readonly name: string;
  readonly topic: string;
  readonly startAt: string;
  readonly description?: string;

  constructor(props: TaskProps) {
    this.id = props.id;
    this.name = props.name;
    this.topic = props.topic;
    this.startAt = props.startAt,
    this.description = props.description;
  }

  async save(repo: TaskRepository): Promise<void> {
    await repo.save({
      id: this.id,
      name: this.name,
      topic: this.topic,
      startAt: this.startAt,
      description: this.description,
    });
  }

  async scheduleJob(repo: JobRepository): Promise<void> {
    await repo.save({
      id: this.id,
      taskId: this.id,
      taskName: this.name,
      topic: this.topic,
      startAt: this.startAt,
      status: JobStatus.Initialized,
    });
  }
}
```

## 왜 헥사고날 아키텍쳐를 쓰는가?

### 관심사의 분리

각 컴포넌트의 역할이 명확해지기 때문에 봐야하는 포인트를 고민하지 않아도 되고, 새로운 개발자가 들어오더라도 쉽게 봐야할 곳을 찾을 수 있다.

외부와의 연결에 문제가 생기면? 어댑터를 보면 된다.

인터페이스는? 포트를 보면 된다.

처리중간에 EventBridge 에 이벤트를 보내고 싶다면? 서비스를 보면 된다.

비즈니스 로직이 제대로 동작하지 않으면? 도메인 모델을 보면 된다.

### 좀 더 쉬운 테스트

각 컴포넌트의 역할만큼이나 의존성이 명확히기 때문에 테스트의 범위도 명확해진다.

* primary adapter 는 서비스의 내부 구현을 mocking 할 필요 없이, 외부에서 들어온 데이터가 잘 가공되어 서비스에 전달되는지만 확인한다.
* 서비스는 각 어댑터나 도메인 객체가 정상적으로 동작하는지 확인할 필요 없이, 순서대로 오케스트레이션 잘 되는지만 확인한다. 이 때 모든 어댑터는 포트를 기반으로 하기 때문에, 쉽게 FakeAdapter 를 작성하여 서비스를 테스트 해볼 수 있다.
* secondary 어댑터는 다이나모디비나 카프카, 레디스 등의 본인이 담당하는 외부서비스를 mocking 해서 파라미터값이 의도대로 전달되는지를 확인한다.
* 도메인 로직은 모든 비즈니스 로직에 대한 테스트를 작성하게 되지만 의존성이 없기 때문에 mocking 할 필요가 거의 없다. (있더라도 포트를 통해 secondary adapter 를 쉽게 모킹할 수 있다.)
* 마지막으로 위의 모든 과정에서 포트는 검증이 되기 때문에 포트는 따로 테스트할 필요가 없다.

아래는 어플리케이션 서비스에 대한 테스트 일부이다. ports 를 이용해서 가짜 어댑터를 쉽게 생성하고 테스트해볼 수 있다.

```typescript
import TaskService from '../../services/task';
import { TaskRepository } from '../../ports/task';
import { JobRepository } from '../../ports/job';
import { Task as ITask } from '../../interfaces/task';
import { Task } from '../../domain/task';

class FakeTaskRepository implements TaskRepository {
  save = jest.fn();
  delete = jest.fn();
}

class FakeJobRepository implements JobRepository {
  save = jest.fn();
  delete = jest.fn();
  updateStatus = jest.fn();
  listStartableJobs = jest.fn();
}

describe('create task and job', () => {
  it('success', async () => {
    const taskRepo = new FakeTaskRepository();
    const jobRepo = new FakeJobRepository();

    const taskService = new TaskService(
      taskRepo,
      jobRepo,
    );

    const dtoTask: ITask = {
      id: 'test-task-1',
      name: 'test-task-1',
      topic: 'test-topic-1',
      startAt: DateTime.now().toISO(),
    };

    const task = taskService.toTask(dtoTask);
    await taskService.createTaskAndJob(task);
    expect(taskRepo.save).toBeCalledTimes(1);
    expect(jobRepo.save).toBeCalledTimes(1);
  });
});
```

일반적으로 테스트 피라미드[^5] 가 잘 지켜질수록 좋은 테스트 / 서비스코드이다. 

실제로 도메인 모델을 잘 작성했을수록 서비스와 도메인 로직의 유닛테스트가 가장 많은 테스트를 가지게 되고,

통합테스트 부분인 secondary 어댑터들이 좀더 적은 테스트, 그리고 primary adapter 가 가장 적은 테스트를 가지게 된다.

## 마치며

헥사고날의 예제 코드는 여기[^7]. 다만 본글의 예제에 사용한 코드들과 무관한 내용이다.

golang 으로 작성되었고 saga 패턴을 transational outbox[^8] 패턴으로 구현한다. 특정 목적을 가지고 만든 예제코드라 헥사고날만 보기에는 어려울 수 있지만 도커만 있으면 일단 로컬에서 돌려볼 수 있게 되어 있다. 사용한 패턴들도 시간나면 블로그에 써야겠다.

모든 서비스가 마이크로 서비스 일 필요가 없듯이,

내 도메인 모델이 빈약하거나, 아예 DDD 를 하지 않는 상황이라면 굳이 클린아키텍쳐 스타일을 쓸 필요가 없다.

*이럴거면 그냥 레이어드 아키텍쳐 쓰는거보다 크게 나은것도 없는데 왜 이짓을 하고 있지?* 라는 생각을 하게 되기 때문이고, 이런 경우 실제로 레이어 아키텍쳐가 더 나을 수도 있다.

비즈니스 목적에 맞는 툴이 최고의 툴이라는 사실을 잊지 말자.

> 람다에 좀 더 가볍게 적용할 수 있는 형태로 이 글[^6]을 참고하자. 클래스 없이 함수만으로 구현한 포트앤어댑터 람다 예제.

----

[^1]: [Clean and Hexagonal Architectures for Dummies](https://medium.com/codex/clean-architecture-for-dummies-df6561d42c94)
[^2]: [Comparing Three-Layered and Clean Architecture for Web Development](https://betterprogramming.pub/comparing-three-layered-and-clean-architecture-for-web-development-533bda5a1df0)
[^3]: [Leonardo Giordani-Python의 깨끗한 아키텍처](https://youtu.be/bieO6YOZ4uc?t=809)
[^4]: [More Testable Code with the Hexagonal Architecture](https://www.youtube.com/watch?v=ujb_O6myknY)
[^5]: [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)
[^6]: [Developing evolutionary architecture with AWS Lambda](https://aws.amazon.com/blogs/compute/developing-evolutionary-architecture-with-aws-lambda/)
[^7]: [Hexagonal Saga Architecture](https://github.com/haandol/hexagonal-saga-architecture)
[^8]: [Transational Outbox](https://microservices.io/patterns/data/transactional-outbox.html)
