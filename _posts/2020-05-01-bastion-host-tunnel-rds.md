---
layout: post
title: AWS SSM 배스천호스트 터널링으로 RDS(PGDB) 에 연결하기
excerpt: Connect to RDS from localhost using AWS SSM BastionHost portforwarding
author: vincent
email: ldg55d@gmail.com
tags: cdk rds portforward aws bastion-host tunneling pgdb postgresql postgres socat
publish: true
---

## TL;DR

코드는 여기[^1].

AWS 계정이 있다면 *README.md* 읽고 따라해볼 수 있다.

## 시작하며

보통 RDS 를 프라이빗 서브넷에 띄우고 배스천 호스트를 퍼블릭에 띄워서, 배스천 호스트를 통해서 RDS 에 접근하는 것이 일반적이다.
(그리고 배스천 호스트는 시큐리티 그룹으로 아이피 접근을 제어한다.)

AWS Systems Manager(SSM) 을 사용하면 아래와 같이, 이 배스천호스트도 프라이빗 서브넷에 두고 쓸 수 있다.

![](/assets/img/20200501/bastionhost.png)

이 글에서는 위의 구조를 기반으로 [RDS(PGDB)] - [배스천호스트] - [로컬호스트] 간의 터널링을 세팅하고, 이를 이용해 로컬호스트에서 RDS 에 접근을 하는 내용을 다뤄본다.

코드의 *README.md* 에 상세한 실습과정을 다 기록해두었으므로 중요한 내용 위주로 글을 작성해본다.

## 인프라 설정

일반적으로는 콘솔에서 VPC(Public Subnet, Private Subnet, Routing Table, IGW 등등), RDS, EC2 인스턴스(BastionHost) 를 만들어야 한다. 

하지만 콘솔로 일일이 만들면 귀찮기 때문에, 여기서는 CDK 라는 IaC(Infrastructure as Code) 툴을 이용해서 필요한 인프라들을 AWS 위에 프로비젼한다.

CDK 는 다양한 언어로 제공되는데, 해당 언어들을 통해 클라우드포메이션 템플릿을 생성해주고 클라우드포메이션을 통해 배포한다. 따라서 CDK로 배포하는 내용은 모두 클라우드포메이션에서 관리할 수 있다.

## 터널링 설정

여기서 만들고자하는 터널의 모양은 대충 아래와 같다.

```
[RDS] <====> [BastionHost] <====> [Localhost]

[5432] <====> [5432:8888] <====> [8888:5432]
```

RDS 의 5432 포트를 배스천호스트에서 8888로 포트포워딩 해주고, 배스천호스트의 8888포트를 로컬호스트의 5432 포트로 포워딩함으로써 `localhost:5432` 에 데이터베이스 클라이언트가 커넥션 요청을 하면 RDS 에 접근할 수 있게 된다.

### BastionHost 연결

[RDS] - [BastionHost] 간의 연결은 배스천호스트에서 `socat(Socket Concatenator)`[^2] 를 통해 할 수 있다.

따라서 배스천호스트에 먼저 접속을 해서 *socat* 프로그램을 실행해줘야한다.
SSM 을 통해 배스천호스트에 연결하는 것은 아주 쉽다.

```bash
$ aws ssm start-session --target YOUR_INSTANCE_ID

sh-4.2$
```

배스천호스트의 인스턴스 아이디는 클라우드포메이션의 Output 탭이나 콘솔의 EC2 서비스 페이지에서 얻을 수 있다.

코드에서는 작업에 필요한 리소스 정보를 클라우드 포메이션의 Output 으로 노출되게끔 CDK 에서 작업해두었기 때문에, 굳이 여기저기 콘솔 서비스들을 찾아다니며 정보를 얻을 필요가 없다.

### 배스천호스트 포트포워딩 설정 (RDS - BastionHost)

접속이 잘 되었으면 *socat* 을 설치하고 RDS 의 *5432* 포트를 배스천호스트의 *8888*로 포트포워딩 해주자.

```bash
$ sudo yum install socat -y
$ sudo socat -d -d TCP4-LISTEN:8888,fork TCP4:YOUR_RDS_CLUSTER_URL:5432 &

2020/04/30 13:26:34 socat[3074] N listening on AF=2 0.0.0.0:8888
...
```

인스턴스 아이디와 마찬가지로 클러스터 주소도 클라우드포메이션의 Output 메뉴에서 확인할 수 있다. (물론 RDS 콘솔 페이지에서도 확인 가능하다.)

### 로컬호스트 포트포워딩 설정 (BastionHost - Localhost)

그럼 로컬호스트의 5432 포트를 배스천호스트의 8888로 포워딩해준다. 원래는 SSM의 SSH 연결정보를 이용하여 터널링하고 그 터널을 통해 포트포워딩 해야하기 때문에 로컬호스트에서도 socat 을 써야하지만 다행히 SSM 에서는 로컬포트에 대한 포트포워딩을 지원한다.

```bash
$ aws ssm start-session \                                                            
--target YOUR_INSTANCE_ID \
--document-name AWS-StartPortForwardingSession \                                   
--parameters '{"portNumber":["8888"], "localPortNumber":["5432"]}'

Starting session with SessionId: dongkyl-0b20f77120a8efd8f
Port 5432 opened for sessionId dongkyl-0b20f77120a8efd8f.
```

코드기준으로 *scripts/tunnel.sh* 를 실행하면 인스턴스 아이디를 가져오고 위의 명령을 한번에 실행해준다.

## AWS Secrets Manager 에서 RDS 비밀번호 가져오기

RDS 에 접속하기 위해서는 접속정보가 필요하다.

여기서는 `AWS Secrets Manager` 를 사용하여 RDS 접속정보를 관리한다.

![](/assets/img/20200501/secrets.png)

AWS Secrets Manager 는 고도로 암호화된 키-밸류 스토어이다. 저장된 내용을 확인할 때, 위와 같이 AWS Secrets Manager 에서 직접 확인해볼 수도 있고, 아래처럼 프로그램 방식으로 가져와서 사용할 수도 있다.

## RDS 접속하기

모든 준비가 끝났다. 로컬에서 아래의 코드를 이용하거나 *PSQL*, *DBeaver* 등의 프로그램으로 *localhost:5432* 를 통해 RDS PGDB 연결을 해보자.

아래의 코드처럼 *AWS Secrets Manager* 에 RDS 접속에 관련된 정보들(호스트정보, 아이디, 비번 등)을 넣어두고 사용하면, 코드에서 RDS 접속에 관련되어 하드코드된 내용들을 모두 지울 수 있다.

```python
import json
import boto3
import psycopg2 as pg2

client = boto3.client('secretsmanager')

secret_value = client.get_secret_value(SecretId='arn:aws:secretsmanager:ap-northeast-2:929831892372:secret:RdsClusterAlphaSecret22E649-H6f7k6fXTacP-RSqbEc')

D = json.loads(secret_value['SecretString'])
dbname = D['dbname']
user = D['username']
password = D['password']

conn = pg2.connect(
    host='localhost',
    dbname=dbname,
    user=user,
    password=password,
    port=5432
)

cursor = conn.cursor()
cursor.execute('SELECT version()')

cursor.fetchall()

conn.close()
```

## 마치며

AWS Sytems Manager, AWS Secrets Manager 등은 좀 생소할 것이다.(참고로 Systems Manager 안에는 Parameter Store 라는 서비스가 있는데 Secrets manager 와 비슷하다.) AWS 에는 다양한 워크로드를 처리하기 위한 서비스들이 추가되고 있다. 

목적에 맞는 서비스들을 적절히 사용하면 동일한 워크로드를 훨씬 간단한 방법으로 해결할 수 있는 경우가 많다.

----

[^1]: [BastionHost RDS Tutorial](https://github.com/haandol/bastionhost-rds-tutorial)
[^2]: [socat](https://medium.com/@copyconstruct/socat-29453e9fc8a6)