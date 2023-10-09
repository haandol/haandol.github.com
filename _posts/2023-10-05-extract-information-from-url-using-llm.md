---
layout: post
title: LLM 을 이용해서 웹에서 데이터 추출하기
excerpt: Extract information from URL text using LLM
author: vincent
email: ldg55d@gmail.com
tags: llm gen-ai web-crawler data bedrock claude2
publish: true
---

## TL;DR

코드는 여기[^1]

## 시작하며

요새 다양한 이유로 웹 크롤링을 해야하는 경우가 많다. 그리고 웹 크롤링은 대부분 귀찮다.

웹 크롤링에서 귀찮음은 목적에 따라 크게 2개로 나눠볼 수 있는데,

1. 자바스크립트 헤비한 특정 서비스/페이지에서 데이터를 뽑아내야하는 귀찮음
2. 다양한 페이지에서 텍스트 데이터를 뽑아내야하는 귀찮음

1번은 네이버 키워드 광고 자동관리, 티케팅 사이트에서 정보가져오기 등의 워크로드를 처리해야하는 경우이다. 이 경우, purpeteer 나 selenium 등을 이용하여 selector 쿼리로 데이터를 직접 뽑아내야 하기 때문에 페이지별로 코드를 따로 짜줘야하는 경우가 많다.

2번은 서로다른 마크업 구조를 가진 웹페이지에서 의미있는 텍스트를 찾아내고 해당 텍스트를 추출하는 경우이다. 머신러닝을 위한 데이터를 수집하거나 최근 유행하는 LLM 을 이용한 질문답변을 위한 데이터를 수집하기 위해 많이 사용하게 된다.

본문에서는 2번에 해당하는 케이스를 간단히 다뤄본다.
엄밀한 데이터 추출보다는 해당 웹 페이지의 대략적인 문맥을 파악하면서도 주요한 내용을 놓치지 않도록 하는데 좋은 방법이라고 생각한다. (즉, 정확도보다는 리콜에 치중한 확률기반 텍스트 추출이라고 볼 수 있을 것이다.)

## 주요 툴

이후 설명을 간결하게 하기 위해, 먼저 사용한 툴들을 간단히 설명해본다.

### Claude on Bedrock

얼마전에 AWS 판 ChatGPT 인 Bedrock[^2] 이 GA (Generally Available) 릴리즈 되어서 us-east-1 리전에서 사용할 수 있게 되었다.

Bedrock 을 통해서 ChatGPT 3.5-turbo 모델보다 성능이 좋다고 알려진 Claude2[^3] 를 사용할 수 있는데 코드[^1]에서는 이 모델을 사용한다.

현재 최대 토큰길이가 ChatGPT 3.5 turbo 는 16k, 최신 라마2도 32k 인데 반해 Claude2 는 100k 토큰을 처리할 수 있고, 긴 컨텍스트 처리시 성능도 좋은 편[^4]이기 때문에 긴 문서요약이나 RAG 같은 작업에 유용한 것 같다.

### Trafilatura

위에서 소개한 1번 작업의 웹 크롤링은 일반적으로 scrapy 나 beautifulsoup 같은 툴로 직접 DOM 을 순회하면서 작성하지만 2번 작업은 해당 방식으로 처리하기 쉽지 않다.

Trafilatura[^5] 는 웹 페이지에서 텍스트를 추출하기 위해 만들어진 크롤링 라이브러리 (혹은 CLI) 로 웹 페이지에서 데이터 추출이나 텍스트마이닝을 쉽게 해주는 툴이다.

### Langchain

Langchain[^6] 은 다양한 LLM 을 쉽게 쓸 수 있게 해주는 프레임워크로 LLM 을 이용한 대부분의 작업을 쉽게 할 수 있는 도구를 제공한다.

개인적으로는 프레임워크 수준의 추상화를 별로 안좋아해서 좀 더 가벼운 griptape 같은 걸 쓰려고 하는 편이지만, 여튼 짧은 코드로 빠르게 LLM 으로 실험할 때는 제일 무난한 도구이다.

Bedrock 도 랭체인과 통합이 되어 있어서 바로 쓸 수 있지만, 코드에서는 aws sdk (boto3) 를 사용해서 추상화를 최대한 적게 사용했다.

## 코드 설명

### 데이터 크롤링

trafilatura 를 이용하면 크롤러 구현은 매우 쉽다.

텍스트만 추출할 계획이므로 불필요한 정보들은 추출하지 않도록 파라미터를 조정하고 json 으로 내보낸뒤 `text` 필드만 가져오면 된다.

```python
import json
import trafilatura

def crawl(url):
    downloaded = trafilatura.fetch_url(url)
    contents = trafilatura.extract(
        downloaded, output_format="json",
        include_comments=False, include_links=False, with_metadata=True,
        date_extraction_params={'extensive_search': True, 'original_date': True},
    )
    json_output = json.loads(contents)
    return json_output['text']

print(crawl('https://en.wikipedia.org/wiki/Lee_Byung-hun'))
```

github 코드에는 trafilatura 가 크롤링 실패했을 때, beautifulsoup 으로 fallback 크롤링을 한다. 같은 url 에 대해서 두가지를 다 해보면 trafilatura 가 텍스트 추출면에서 더 나은 것을 확인할 수 있을 것이다.

### Refining text using LLM

이렇게 추출한 텍스트를 바로 토픽 모델링이나 마이닝에 쓰기에는 너무 노이즈가 많다. 대부분의 자연어 기반 작업에서는 텍스트를 전처리 해서 노이즈를 삭제하는 작업을 하게 되는데, 여기서는 LLM (Claude2) 을 이용한 텍스트 요약을 통해 노이즈를 줄여본다.

개인적으로 LLM 의 성능에서 가장 중요한 부분은 프롬프트 엔지니어링이라고 생각한다. 프롬프트 엔지니어링에 대해서 익숙하지 않다면 Deeplearning.ai 의 무료코스[^7] 를 꼭 수강해보기 바란다.

프롬프트 엔지니어링만으로도 강의코스를 만들 수 있을 정도이므로, 여기서는 건너뛰고 Chain of Thought 기법만 간단히 살펴본다.

프롬프트를 통해 LLM 에게 복잡한 작업을 시킬 때 가장 중요한 것은, 모델(LLM 모델) 에게 `생각할 여유를 주는 것`이다. 이것은 모델이 답을 바로 말하게 하는 대신 답을 도출(reasoning)할 때 생각해야 할 내용들을 프롬프트에서 언급해주어 해당 과정을 반영하여 답을 도출하게 하는 것이다.

그리고 이 생각할 여유를 만들어주는 방법들 중 하나가 CoT (Chain of Thought)[^8] 이다.

이 원리는 모델이 수십억개 이상으로 이뤄진 벡터공간에서 어느 부분을 참고해야하는지를 프롬프트를 통해서 가이드를 해주는 것이라고 보면 된다. ICL(in context learning), RAG 와도 비슷하다고 볼 수 있는데, 모델이 해당 공간을 스스로 찾아내는지, 외부에서 공간의 위치를 지정해주는지 정도만 다르다고 보면 된다.

```python
instruction_prompt = """
You are information extractor. You extract the key informations from the user text to help him to build a topic model. \
The user text is enclosed in text tags, <text></text>.

Let's think step by step and follow below steps to respond to the user. \
Make sure each step starts with four hashes as delimiter, ####.

####Step 1: List informative keywords that helps to understand the text.

####Step 2: If the text contains informative name of entities, List them.

####Step 3: Provide summary of the text in about 50 words. \
The summary should use as many keywords and entities extracted in the previous steps as possible. \
The information must not contain any code. Do not provide any sample code in the information.

####Step 4: Respond the result in JSON format with following keys: keywords, entities, summary.
""".strip())
```

위의 내용은 코드에서 사용한 CoT 프롬프트로 총 4개의 스텝으로 구성했다.

1. 키워드 추출
2. 고유명사 추출
3. 입력된 chunk 에 대한 요약작성
4. JSON 형태로 컨버팅

일반적으로 ChatGPT, Llama2, Claude2 에서 잘 동작하는 프롬프트 형태가 다 다르며, 각 스텝에 사용할 내용도 try & error 를 통해 몇차례 개선을 해야(iterate) 원하는 결과를 주는 프롬프트를 만들 수 있다.

### Chunking

Claude2 는 최대 100k 개의 토큰을 한 프롬프트에서 처리할 수 있으므로 (출력토큰 개수 포함이지만) 웬만한 웹페이지는 한번에 처리할 수 있다.

하지만 이렇게 대량의 텍스트를 주고 그냥 요약을 하게 되면 디테일한 내용들이 많이 사라지게 된다. 예를 들어, imdb 스타워즈 시놉시스를 10 단어로 이내로 요약하라고 하면 `우주 전쟁과 제다이의 이야기, 다스 베이더 vs 루크 스카이워커.` 라고 요약해주는데 포스, 데스스타 와 같은 주요 단어들이 많이 사라진다.

이런 경우 적절한 단위 (스타워즈 에피소드) 로 요약을 해서 이어붙이는 것이 디테일한 내용을 더 많이 살릴 수 있다.

```python
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter.from_tiktoken_encoder(
    model_name='gpt-3.5-turbo',
    chunk_size=1446,
    chunk_overlap=20,
)
each_info = []
for chunk_idx, chunk in enumerate(splitter.split_text(doc)):
    info = extract_info(chunk)
    each_info.append(info)
```

langchain TextSplitter 는 토큰단위로 자를 수 있고 각 자른 단위(chunk) 가 겹칠 토큰 개수도 지정할 수 있다. (griptape 의 splitter 는 겹치기 기능이 없다.)

RAG 나 긴글요약의 경우 텍스트를 나눌 수 밖에 없는데, 이 때 어떤 기준으로 나누느냐에 따라 결과물의 성능(질문에 대한 정확도 또는 리콜) 에 큰 영향을 미치게 된다.

## 마치며

Bedrock Claude2 는 마지막 토큰을 `{` 로 두면 에러가 나서
ChatGPT 나 Llama2 Chat 모델에 비해서 JSON 아웃풋으로 제어하는게 더 어려운 느낌.

---

[^1]: [LLM Examples on github](https://github.com/haandol/LLM-Examples/blob/main/notebook/crawlers)
[^2]: [AWS Bedrock](https://aws.amazon.com/ko/bedrock/)
[^3]: [Claude2](https://www.anthropic.com/index/claude-2)
[^4]: [Prompting Long Context](https://www.anthropic.com/index/prompting-long-context)
[^5]: [Trafilatura](https://trafilatura.readthedocs.io/en/latest/)
[^6]: [Langchain](https://www.langchain.com/)
[^7]: [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)
[^8]: [Chain of Thought](https://www.promptingguide.ai/techniques/cot)
