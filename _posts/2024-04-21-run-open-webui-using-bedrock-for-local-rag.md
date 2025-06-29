---
layout: post
title: Open WebUI 와 Amazon Bedrock 으로 이용해서 로컬에서 RAG UI 돌려보기
excerpt: Run Open WebUI using Amazon Bedrock for local RAG
author: haandol
email: ldg55d@gmail.com
tags: rag ollama open-webui amazon bedrock claude3
publish: true
---

## TL;DR

- 코드[^1]는 여기

## 시작하며

최근에 다수의 논문을 쉽게 읽으려고 ChatGPT 를 결제해서 쓰고 있었는데, Amazon Bedrock 에도 Claude3.5 Sonnet 이 나와서 결제를 해지하고 이걸 활용하는 방법을 찾아보고 있다.

Open WebUI 를 이용하면 로컬에서도 쉽게 RAG UI 를 돌려볼 수 있어서 정리할 겸 적어본다.

## 도커로 실행하기

로컬 환경에서 AWS Credential 을 설정해두고, Amazon Bedrock 에서 모델 사용을 설정해뒀다면[^2], 코드[^1] 에 정리해둔대로 도커를 실행하면 된다.

```bash
$ docker-compose up -d
$ open localhost:3000
```

처음 사용할 경우 회원가입 및 로그인을 하고(로컬환경이지만 로그인이 필요하다),

이후 모델 선택하는 부분에서 `bedrock-claude-v3` 를 선택하고 사용하면 된다.

<img src="/assets/img/2024/0421/open-webui.png" alt="Open WebUI" style="width: 100%;"/>

현재는 개인 사정상 Claude3 Sonnet 으로 되어 있는데, 3.5 Sonnet 으로 쓰는 것이 모든 면에서 더 낫다.

`config.yaml` 에서 `litellm_params.model` 을 `anthropic.claude-3-5-sonnet-20240620-v1:0` 로 바꿔서 쓰면 된다.

기본 임베딩 설정은 sentence-transformers[^3] 의 all-MiniLM-v6 를 쓰고 있는데, 이 모델은 멀티링구얼 모델이 아니라 성능이 떨어진다. 또 기본 청크 사이즈도 1500 정도로 매우 작기 때문에 설정을 이것저것 바꿔가면서 적당한 설정을 찾아보자.

나는 ollama 모델로 며칠전 나온 snowflake-arctic-embed[^4] 를 쓰고 있는데 나쁘지 않은 것 같다.

## 마치며

대충 쓰기에는 적당한거 같은데, RAPTOR[^5] 같은 방식으로 RAG 성능을 올리려면 결국 streamlit 으로 직접 구현해야 하는 것 같다.

---

[^1]: [Open WebUI for Amazon Bedrock](https://github.com/haandol/open-webui-bedrock)
[^2]: [AWS 블로그 Claude3 설정](https://aws.amazon.com/ko/blogs/korea/anthropics-claude-3-haiku-model-is-now-available-in-amazon-bedrock/)
[^3]: [Sentence Transformers](https://www.sbert.net/)
[^4]: [Snowflake arctic embed](https://ollama.com/library/snowflake-arctic-embed)
[^5]: [RAPTOR](https://github.com/parthsarthi03/raptor)
