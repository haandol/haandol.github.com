---
layout: post
title: Bedrock + NLI (Natural Language Inference) 로 제로샷 분류기 만들기
excerpt: Building zero-shot classifier using NLI (Natural Language Inference) and Bedrock
author: haandol
email: ldg55d@gmail.com
tags: llm gen-ai web-crawler data bedrock claude2 nli natural-language-inference classifier zero-shot
publish: true
---

## TL;DR

코드는 여기[^1]

## 시작하며

LLM 텍스트 작업을 하다보면 문장이나 문서에 대한 간단한 분류기가 필요한 경우가 많다.

예전에는 분류기가 필요하면 데이터를 수집해서 모델을 학습해쓰는 것 말고는 딱히 방법이 없었지만, 트랜스포머가 나온 이후로는 학습데이터없이 제로-샷 분류기를 만들어 쓰는 것도 고려해볼 수 있게 되었다.

제로샷 분류기를 만들 때, 프롬프트 체이닝으로 LLM 을 통해 분류기를 구성하는 것도 좋은 방법이다. 다양한 제약조건이나 전처리를 하면서 분류를 할 수 있기 때문이다.

하지만 분류 카테고리가 일반적이거나 분류에 필요한 사전 조건이 없는 경우 NLI (Natural Language Inference) 가 더 좋은 선택지일 수도 있다.

본문에서는 NLI 를 이용하여 간단한 분류기를 만들어 보고, 이를 LLM 을 이용해서 개선하는 내용을 소개한다.

## 주요 툴

이후 설명을 간결하게 하기 위해, 먼저 사용한 툴들을 간단히 설명해본다.

### Claude on Bedrock

얼마전에 AWS 판 ChatGPT 인 Bedrock[^2] 이 GA (Generally Available) 릴리즈 되어서 us-east-1 리전에서 사용할 수 있게 되었다.

Bedrock 을 통해서 ChatGPT 3.5-turbo 모델보다 성능이 좋다고 알려진 Claude2[^3] 를 사용할 수 있는데 코드[^1]에서는 이 모델을 사용한다.

현재 최대 토큰길이가 ChatGPT 3.5 turbo 는 16k, 최신 라마2도 32k 인데 반해 Claude2 는 100k 토큰을 처리할 수 있고, 긴 컨텍스트 처리시 성능도 좋은 편[^4]이기 때문에 긴 문서요약이나 RAG 같은 작업에 유용한 것 같다.

### Multi-NLI

인코더 기반인 BERT 대신 Seq2Seq 방식으로 처리할 때 임베딩(인코딩) 및 번역 작업에서 성능이 더 좋다는 것이 알려졌있고, 그 대표적인 모델이 BART 라고 할 수 있다.

BART 를 샴 네트워크 방식으로 학습해서 임베딩간 유사도를 판단할 수 있게 만든것이 MNLI 모델이다. 해당 모델은 성능이 준수하지만 영어만 지원하기 때문에 한국어를 사용하고 싶다면 XNLI (Cross-lingual Natural Language Inference) 모델을 사용해야 한다.

코드의 예제에서는 `mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` 를 사용했다.

### Langchain

Langchain[^6] 은 다양한 LLM 을 쉽게 쓸 수 있게 해주는 프레임워크로 LLM 을 이용한 대부분의 작업을 쉽게 할 수 있는 도구를 제공한다.

개인적으로는 프레임워크 수준의 추상화를 별로 안좋아해서 좀 더 가벼운 griptape 같은 걸 쓰려고 하는 편이지만, 여튼 짧은 코드로 빠르게 LLM 으로 실험할 때는 제일 무난한 도구이다.

Bedrock 도 랭체인과 통합이 되어 있어서 바로 쓸 수 있지만, 코드에서는 aws sdk (boto3) 를 사용해서 추상화를 최대한 적게 사용했다.

## 코드 설명

### Raw data 로 분류하기

코드[^1] 는 ACL (Anti-corruption layer pattern) 에 대한 인터넷 아티클을 NLI 모델을 이용하여, `'software engineer', 'web designer', 'digital marketer'` 중 하나의 카테고리로 분류하는 내용이다.

```python
import json
from transformers import pipeline


with open('acl.txt', 'r') as fp:
    doc = fp.read()

classifier = pipeline(
    task='zero-shot-classification',
    model='facebook/bart-large-mnli',
)

candidate_labels = ['software engineer', 'web designer', 'digital marketer']
res = classifier(doc, candidate_labels)
print(f'{json.dumps(res, indent=2)}\n')
```

위의 코드가 전체 코드이다. 입력된 문서는 대략 1만자 정도의 텍스트이며 cpu 로 인퍼런스해도 몇 초안에 할 수 있을 정도로 빠르게 처리 된다.

결과는 약간 실망스럽다. 다음과 같이 `software engineer` 로 분류를 해주기는 하지만, 점수 자체도 낮고 (40% 미만) 다른 카테고리와 큰 차이도 없다. (4% 정도)

```json
{
  "sequence": "Anti-corruption layer pattern\n\nIntent\nT...",
  "labels": ["software engineer", "web designer", "digital marketer"],
  "scores": [0.37129560112953186, 0.3353971540927887, 0.29330718517303467]
}
```

### Summary 해서 분류하기

전처리를 해서 다시 분류를 해보자. 코드에서는 Bedrock 의 Claude 모델로 langchain 의 summarize_chain 을 호출하여 요약본을 만든다.

```python
import ...

llm = Bedrock(
    model_id='anthropic.claude-v2',
    model_kwargs={
        "max_tokens_to_sample": 4096,
        "top_p": 0.9,
        "temperature": 0,
    },
    client=bedrock,
)

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n"],
    chunk_size=3000,
    chunk_overlap=100,
)
docs = text_splitter.create_documents([doc])

summary_chain = load_summarize_chain(
    llm=llm,
    chain_type="map_reduce",
    verbose=False,
)
output = summary_chain(docs)
summary = output['output_text'].strip()
print(summary)
```

해당 요약본은 대략 770 자로 1만자 정도의 기존 텍스트 대비 7% 정도의 길이를 가지게 되었다. 원본 텍스트 대신 해당 요약본으로 동일한 분류요청을 해보면 다음과 같은 결과가 나온다.

```json
{
  "sequence": "Here is a concise summary of the key points:\n\nThe anti-corruption layer (ACL) pattern provides an abstraction between a monolithic application and a microservice. It translates calls between the incompatible interfaces, allowing incremental migration without disrupting the monolith. The ACL can be implemented as a facade within the monolith or an independent service. It enables decoupling but adds overhead. The ACL should be decommissioned after full migration. Key considerations are technical debt, latency, scaling, and implementation strategy. The provided C# code demonstrates an ACL implementation that transforms monolith data models into the microservice format and handles integration. The ACL isolates the monolith from microservice changes during migration.",
  "labels": ["software engineer", "web designer", "digital marketer"],
  "scores": [0.692902147769928, 0.1681481897830963, 0.13894963264465332]
}
```

분류에 대한 확실성도 올라갔고, 다른 카테고리들과의 변별력도 커졌다.

### 한글분류

마지막으로 한글지원 모델로 간단한 감성(Sentimental) 분류기를 만들어보고 마친다.

NLI 는 대부분 단일 언어로 학습되며, 다중언어를 지원하는 문제는 XNLI(Cross Langual) 문제로 따로 분류하고 있다.

따라서 모델도 XNLI 문제를 푸는 모델로 사용해야한다. 코드에서는 `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` 모델을 사용한다. (그냥 좋아요가 가장 많아서..)

파이프라인은 똑같고 모델명만 바꿔주면 된다.

```python
ko_classifier = pipeline(
    task='zero-shot-classification',
    model='MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7',
)
```

감성분석은 대체로 복합적(mixed signal)이기 때문에 분류가 어렵다. 현실과 비슷하게 만들기 위해, 배송과 포장에 대해서는 약한 불만이 있지만 제품 자체에 대해서는 큰 만족도를 가진 리뷰를 만들어봤다.

```python
sequence = '''
새벽 배송이라고 써있어서 새벽에 올 줄 알았는데, 오후 늦게 도착해서 실망했습니다.
아이폰 박스에 뽁뽁이로 포장이 안되어 있어서 제품 파손이 약간 우려스러웠습니다.
제가 아이폰만 계속 쓰고 있어서 그런것도 있지만, 제품은 정말 최고의 제품입니다.
아직 안바꾸신 분들 계시면 꼭 바꾸시길 추천합니다.
'''
candidate_labels =['긍정', '부정', '중립']
```

기존과 동일하게 분류하면 복합적이기 때문에 부정이나 긍정이 섞여서 나오고, 확실성도 낮은편이다.

```json
{
  "sequence": "\n새벽 배송이라고 써있어서 새벽에 올 줄 알았는데, 오후 늦게 도착해서 실망했습니다.\n아이폰 박스에 뽁뽁이로 포장이 안되어 있어서 제품 파손이 약간 우려스러웠습니다.\n제가 아이폰만 계속 쓰고 있어서 그런것도 있지만, 제품은 정말 최고의 제품입니다.\n아직 안바꾸신 분들 계시면 꼭 바꾸시길 추천합니다.\n",
  "labels": ["부정", "긍정", "중립"],
  "scores": [0.5180058479309082, 0.2957472503185272, 0.1862468123435974]
}
```

따라서 LLM 으로 분류기를 만들때도 일반적으로 주제에 대한 분류로 조건을 준다. NLI 에서도 비슷한 기능을 추가할 수 있는데, hypothesis_template 이 그것이다.

이를 이용해 제품에 대한 감성을 분류해보면, 0.77 로 긍정으로 분류한다.

```python
ko_classifier(
    sequence,
    candidate_labels,
    hypothesis_template='제품에 대한 만족감은 {} 이다.',
)

>>> {'sequence': '\n새벽 배송이라고 써있어서 새벽에 올 줄 알았는데, 오후 늦게 도착해서 실망했습니다.\n아이폰 박스에 뽁뽁이로 포장이 안되어 있어서 제품 파손이 약간 우려스러웠습니다.\n제가 아이폰만 계속 쓰고 있어서 그런것도 있지만, 제품은 정말 최고의 제품입니다.\n아직 안바꾸신 분들 계시면 꼭 바꾸시길 추천합니다.\n',
 'labels': ['긍정', '부정', '중립'],
 'scores': [0.7716712951660156, 0.1566908359527588, 0.07163792103528976]}
```

또, 배송에 대한 감성을 분류해보면, 0.88 로 부정으로 분류하는 것을 확인할 수 있다.

```python
ko_classifier(
    sequence,
    candidate_labels,
    hypothesis_template='배송에 대한 만족감은 {} 이다.',
)

>>> {'sequence': '\n새벽 배송이라고 써있어서 새벽에 올 줄 알았는데, 오후 늦게 도착해서 실망했습니다.\n아이폰 박스에 뽁뽁이로 포장이 안되어 있어서 제품 파손이 약간 우려스러웠습니다.\n제가 아이폰만 계속 쓰고 있어서 그런것도 있지만, 제품은 정말 최고의 제품입니다.\n아직 안바꾸신 분들 계시면 꼭 바꾸시길 추천합니다.\n',
 'labels': ['부정', '긍정', '중립'],
 'scores': [0.8069165349006653, 0.11074954271316528, 0.08233391493558884]}
```

## 마치며

템플릿 기능이 있는지 몰랐는데 정리하면서 알게되었다. 항상 문서를 잘 읽어야..

---

[^1]: [Zero-shot classifier using NLI](https://github.com/haandol/LLM-Examples/blob/main/notebook/nli/NLI%20Classifier.ipynb)
[^2]: [AWS Bedrock](https://aws.amazon.com/ko/bedrock/)
[^3]: [Claude2](https://www.anthropic.com/index/claude-2)
[^4]: [Prompting Long Context](https://www.anthropic.com/index/prompting-long-context)
[^5]: [BART Multi NLI](https://huggingface.co/facebook/bart-large-mnli)
[^6]: [Langchain](https://www.langchain.com/)
[^7]: [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)
[^8]: [Chain of Thought](https://www.promptingguide.ai/techniques/cot)
