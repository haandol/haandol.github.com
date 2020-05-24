---
layout: post
title: AWS 로 서버리스 메일링 서비스 만들어보기
excerpt: Making serverless mailing service on AWS
author: vincent
email: ldg55d@gmail.com
tags: cdk serverless mailing tutorial aws dynamodb sqs lambda ses
publish: true
---

## TL;DR

코드는 여기[^1].

배치 / 실시간으로 메일을 보낼 수 있는 서버리스 서비스를 만들어보자.

## 시작하며

AWS에는 Simple Email Service(SES) 라는 서비스가 있다. SES 를 이용하면 AWS SDK 방식이나 SES 에서 제공하는 SMTP 를 이용하여 메일을 직접 발송할 수 있다.

따라서 가장 단순하게 구현하는 방법으로는 Http API 하나를 만들고 email 목록을 전달하면 SDK 를 통해 발송하면 될 것이다.

```bash
$ http post http:/sendmail.example.com/dev body="ldg55d@gmail.com,ldg55d2@gmail.com ..." message="Hi customer..."'
```

만약 개개인의 이름을 메일에 언급해주는 주는 것이 첨부된 캠페인의 반응성을 10% 올려준다고 하자. 개인화된 요소를 추가해서 메일을 발송해야한다는 요청이 들어올 것이다.

이렇게 개인화된 요소들이 하나 둘 추가될 때마다 API 페이로드가 커지게되고 로직도 점점 무거워질 것이다. 게다가 1만명의 사용자에게 1분 이내로 보내고 싶다면, API를 적절히 스케일 아웃을 위한 작업들도 해줘야한다.(어떤 작업이 필요할지는 개인적으로 생각해보자.)

이러한 문제를 해결하기 위해 많은 회사에서는 내부에 자체적으로 구성한 메일링 서비스를 운영하고 있다. 

해당 서비스는 비동기 시스템으로 구성되며, 대부분 아래와 같은 순서로 동작하게 된다.

1. 메일박스로 사용하는 테이블에 메일을 보낼 정보와 개인화된 정보를 넣는다
2. DB 트리거 또는 polling 방식으로 해당 데이터를 읽어서 발송한다.
3. 필요한 경우 처리 과정을 DB에 업데이트 해준다. (READY - SENDING - SUCCESS/FAILED)

이 글에서는 바로 위에 설명한 메일링 서비스를, AWS 위에서 서버리스로 구현해본다.

## 아키텍쳐

코드[^1] 를 provision 하면 아래와 같은 아키텍쳐가 개인 AWS 계정에 프로비젼 된다.

![](/assets/img/20200512/architecture.png)

### 정상발송

메시지가 발송되는 과정은 직관적이며 아키텍쳐의 아래 5개 서비스를 사용한다. 메시지 발송은 아래의 순서로 진행된다.

1. DynamoDB 에 아이템을 추가한다.
2. DynamoDB 스트리밍 서비스를 통해 새로 등록된 아이템이 Stream Batch 람다에 전달된다.
3. 해당 람다는 전달받은 아이템이 사용자가 정한 조건에 일치하는 경우 메일큐(SQS) 에 아이템을 쌓아준다.
4. 메일큐에 쌓인 메시지는 Mail Sender 람다에 전달된다. 해당 람다는 SES 를 통해 메일을 전송해준다.
5. 메시지에 대한 메일이 정상발송되면 해당 메시지를 메일큐에서 삭제해준다.

### 에러처리

위의 3개 서비스는 failover 를 위한 부분이며, 서비스 동작은 다음과 같다.

1. 만약 Mail Sender 의 메일전송 로직이 실패하면 메일큐에 다시 쌓는다
2. 동일한 메시지가 일정회수이상 다시 쌓이면 해당 메시지를 Dead Letter Queue(DLQ) 에 넣는다.
3. DLQ 에 쌓인 메시지는 Logger 람다에 전달된다. 해당 람다는 stdout 으로 로깅하고 메시지를 삭제해준다.

## 코드 설명

각 서비스의 핵심 부분을 간단히 설명해본다.

### DynamoDB

DynamoDB 는 NoSQL 서비스로, 필요에 따라 필드를 추가하고 변경하기에 매우 용이하다.

현재 사용한 테이블의 모양은 다음과 같다. 아래는 코드의 *dynamodb-stack.ts* 의 내용이다.

```javascript
this.table = new dynamodb.Table(this, `${tableName}Table${ns}`, {
  tableName,
  partitionKey: {
    name: 'id',
    type: dynamodb.AttributeType.STRING
  },
  sortKey: {
    name: 'event_type',
    type: dynamodb.AttributeType.STRING,
  },
  stream: dynamodb.StreamViewType.NEW_IMAGE,
  ...
```

파티션키와 정렬키가 있는데, 파티션키는 mongodb 의 샤드키와 primary key 를 합친것이라고 이해할 수 있다. 

레코드는 파티션키에 따라 다른 샤드에 저장되므로 샤드키의 분포는 universal 할수록 좋다. 또한 파티션키는 primary key 이므로 모든 레코드에 대해 유니크 해야한다.

정렬키는 파티션키의 샤드안에서 정렬키를 기준으로 정렬되어 저장된다. 정렬키는 옵셔널이지만 위와 같이 지정된 경우, 파티션키와 정렬키를 합쳐서 primary key 처럼 사용하게 된다.
(즉, query 를 할 때 파티션키와 정렬키 모두 입력해줘야 검색할 수 있다.)

정렬키는 파티션키에 대해서만 유니크하면 된다.

이 외의 필드들은 필요에 따라 추가할 수 있다.

*src/mail.py* 를 보면 쉽게 이해할 수 있다.

```python
from datetime import datetime

now = datetime.now()
records = [{
    'id': now + 'dongkly',
    'event_type': 'mail',
    'email': 'dongkyl@amazon.com',
    'first_name': 'DongGyun',
    'last_name': 'Lee',
},
{
    'id': now + 'ldg55d',
    'event_type': 'mail',
    'email': 'ldg55d@gmail.com',
    'first_name': 'Vincent',
    'last_name': 'Lee',
}]

for record in records:
  table.put_item(Item=record)
```

위에 미리 정의한 *id*, *event_type* 필드를 제외하면(필수) *email*, *first_name/last_name* 등의 필드는 맘대로 추가할 수 있다.

위의 모양으로 아이템을 DyanmoDB에 쌓으면 stream 기능에 의해 *functions/ddb-stream.py* 람다함수가 실행된다.

### DDB Stream

DDB 는 데이터의 모든 변경에 대해 stream 으로 노출할 수 있다.
위에 살짝 공유한 코드에서 보듯이, 새로운 내용에 대해서만 스트림에 보내도록 했다.

```bash
stream: dynamodb.StreamViewType.NEW_IMAGE,
```

해당 스트림에 데이터가 쌓이면 *functions/ddb-stream.py* 에 이벤트가 전달된다.
 
아이템의 삭제/수정에 대해서도 스트리밍에 전달되는데 우리는 추가된 내용에만 관심이 있기 때문에 람다에서는 *Insert* 이벤트에 대해서만 처리하고 나머지 부분은 무시한다.

```python
for record in event['Records']:
    if 'INSERT' != record['eventName']:
        continue
```

정렬키로 지정했던 *event_type* 에 따라서 적절한 SQS 에 전달되도록 하여 메일링 뿐만 아니라 다양한 알람방식으로 해당 서비스를 확장할 수 있다.

현재는 메일링을 위한 SQS 로 데이터가 전달된다.

```python
if mail_entries:
    logger.info(f'send {len(mail_entries)} messages to SQS...')
    response = sqs.send_message_batch(
        QueueUrl=MAIL_QUEUE_URL,
        Entries=mail_entries
    )
    logger.info(response)

if sns_entries:
    logger.info(f'send {len(sns_entries)} messages to SNS...')
```

### SQS

SQS 는 이름그대로 메시지큐이다.
SQS 는 주로 아래와 같이 point to point 방식으로 작업을 디스패칭하는 용도로 사용한다.

![](/assets/img/20200512/sqs.png)

만약 fanout 형태로 메시지를 여러곳에 전달하려면 SNS 를 사용해야한다.

SQS 에 메시지가 전달되면 해당 메시지는 지정된 Subscriber (여기서는 람다)로 전달된다.

### Simple Email Service(SES)

*functions/mail-sender.py* 는 SQS 로부터 전달받은 메시지를, SES를 통해 메일로 전송한다.

```python
SENDER = "DongGyun Lee <dongkyl@amazon.com>"

response = ses.send_email(
    Destination={
        'ToAddresses': [email],
    },
    Message={
        'Body': {
            'Html': {
                'Charset': CHARSET,
                'Data': BODY_HTML.format(first_name, last_name),
            },
            'Text': {
                'Charset': CHARSET,
                'Data': BODY_TEXT.format(first_name, last_name),
            },
        },
        'Subject': {
            'Charset': CHARSET,
            'Data': SUBJECT,
        },
    },
    Source=SENDER,
)
```

코드 자체는 설명할 내용이 필요없을 정도로 직관적이다. 주의할 점으로, SENDER 로 지정된 사용자는 SES 콘솔에서 이메일 인증을 받아야만 한다. (코드의 README.md 에 적혀있다.)

다만, SES를 사용할 때, `limitation increase` 요청을 하지 않았다면 자동으로 `sandbox` 모드에서 동작하게 된다.

*sandbox* 모드는 하루에 200건, 초당 1건으로 발송이 제한되며 무엇보다 **SES 에서 Verified 되지 않은 이메일주소로 발송이 안된다.**
(SES 를 스팸메일 발송자로 사용하는 것을 막기 위해서이다.)

따라서 해당 아키텍쳐를 사내에서 또는 프로덕션에서 사용할 때는 AWS 콘솔에서 SES 에 대해서 *limitation increase* 를 요청하여 일 발송 건수와 초당 발송율을 증가시키고 사용하면 된다.
~~어차피 일 200건이면 뭐 하기도 힘드니깐~~

### Lambda

람다는 마이크로 컨테이너 위에 동작하는 함수이다.

이상적으로는 논리적으로 독립된 기능하나를 함수하나가 담당하는 것이 좋다. 

우리가 만드는 메일링 서비스는 이상적인 형태에 가깝다고 할 수 있다.

코드에는 3개의 람다가 있다.
설명하지 않은 *functions/dlq.py* 는 코드가 매우 쉬우므로 따로 코드를 설명하지는 않는다.

* **ddb-stream.py** - DynamoDB 스트림에서 데이터를 읽어서 기준에 따라 적절한 SQS 로 전달한다.
* **mail-sender.py** - 1:1로 매핑된 SQS에서 메시지를 가져와서 메일을 보낸다.
* **dlq.py** - 메일보내기에 실패한 메시지들을 stdout 으로 출력하여 Cloudwatch 에 로깅해둔다.

다만, 람다의 호출방식은 중요하므로 약간 상세히 설명해보자.

람다는 크게 3가지 방식으로 호출이 가능하다. *동기방식, 비동기방식, 스트리밍 방식* 이 그것이다.

호출방식이 중요한 이유는 각 방식에 따라 재시도 로직이 다르기 때문이며 이에 따라 에러처리를 다르게 해줘야 한다.

**동기방식**은 *awscli* 나 *SDK* 등을 통해서 호출하는 방식이다. 동기방식은 함수오류에 대해 재시도를 하지 않는다.

왜냐하면 람다는 기본적으로 함수오류가 발생해도 statusCode 는 200 (정상처리) 를 반환하기 때문이다.

동기방식에서는 409 등 람다의 동시성 제한에 걸리거나 람다자체의 서비스문제가 발생했을 경우에만 2회 재시도한다.

**비동기 방식**은 위에 설명한 SQS, SNS 등의 메시징 서비스를 통해 호출하는 방식이다.

비동기 방식은 함수오류에 대해 2회 재시도 하며, 이후 메시징 서비스의 처리에 따라 재시도한다.

무슨말인가 하면, SQS 의 경우 메시지를 큐에서 삭제하지 않으면 메시지가 람다로 재전송 된다.
지정된 최대재전송 회수를 넘어서면 DLQ 가 지정된 경우 DLQ 로 메시지를 전달하고 자신의 큐에서는 삭제하게 된다.

**스트리밍 방식**은 Kinesis Data Stream, DynamoDB Stream 등의 스트림에서 데이터를 받아서 호출하는 방식이다.

이 때는 함수오류를 포함한 오류 발생시 지정된 회수만큼 (기본은 10000번) 재시도한다.

재시도에 대해서 제대로 처리하지 않으면, 동일한 메시지가 부분적으로 처리되고 무한히 재처리되면서 동시성을 (돈도) 잡아먹게 된다. (로직처리가 끝나고 마지막에 리턴할때 문법오류가 있다거나 한 경우를 생각해보자..)

## 마치며

코드[^1] 의 서비스는 메일 뿐만 아니라 SNS 를 통한 모바일 푸시 등으로 쉽게 확장가능하며 애초에 아래와 같은 아키텍쳐로 설계되었다.

![](/assets/architecture_extent.png)

만약 더 많은 동시성이 필요하거나 하다면, 아키텍쳐 변경없이 각 서비스의 옵션질을 통해서 충분히 해결 가능하다.

----

[^1]: [Serverless Mailing Service on AWS](https://github.com/haandol/aws-serverless-mailing-service)