---
layout: post
title: 개발자로서 LLM 사용을 위해 알아두면 좋은 내용들
excerpt: Large Language Model for ordinary developers
author: vincent
email: ldg55d@gmail.com
tags: llm large-language-model gpt lora peft
publish: true
---

## TL;DR

코드는 여기[^17].

notebook 폴더 아래에 있는 노트북들을 세이지메이커 gpu 인스턴스에서 실행하면 된다.

## 시작하며

최근 몇 주동안 LLM 모델로 프로토타이핑을 진행하게 되었는데, 그 몇 주동안 너무 많은 모델들이 쏟아져나와서 굉장히 고생을 한 것 같다.

대략 사용자 입장에서 공부하면서 어려웠던 점은,

1. 너무 다양한 모델들이 나오고 있는데 추구하는 바가 조금씩 다르다는 점
2. 파인튜닝 기법이 다양하게 있고 다행히도 LoRA 라는 기법으로 통합되고 있지만 또 새로운 기법이 나오고 있다는 점(IA3 라던가)
3. 여튼 모델을 배포하고나서 generation 을 해야하는데 이때도 다양한 기법들이 있다는 점

본 글에서는 이미 나온 모델을 간단한 파인튜닝 정도만 해서 사용하는 일반 개발자 입장에서 위의 내용을 공부할 때 도움이 될만한 내용을 정리해본다.

## 배경지식

### 트랜스포머

일단 시작은 트랜스포머다. 뒤에 나오는 PEFT 라고 불리는 파인튜닝 기법들이 어텐션 기법과 연관되어 있는데, 어텐션은 트랜스포머의 핵심 아이디어중 하나이기 때문이다.

트랜스포머는 여기[^1]를 참고하자.

어텐션은 키, 쿼리, 밸류로 구성되어 각 위치의 중요도를 결정하는데 도움을 준다는 점 정도만 기억해두자.

### GPT

GPT 는 트랜스포머를 사용한 언어 모델이다. 트랜스포머의 인코더 부분을 제거하고 디코더 부분만 남겨두었다고 생각하면 된다.

세부적인 기술을 빼고 나면 GPT2 나 3나 3.5는 모델의 크기의 차이만 있다고 봐도 무방하며, 상세한 내용은 여기[^2]를 참고하자.

GPT2 는 파라미터수가 백만(M) 단위이지만 gpt3 부터는 십억(B) 단위로 올라가며, GPT3 는 175B 의 파라미터를 가지고 있다.

### ChatGPT

LLM 의 민주화에 대한 시작은 ChatGPT 라고 볼 수 있다. ChatGPT 는 GPT3.5 기반으로 턴바이턴 생성을 할 수 있는 LLM 플랫폼 이다.

GPT3 에 인스트럭션 파인튜닝 기법(FLAN)과 RLHF (Reinforcement Learning with Human Feedback) 라는 학습 방법을 적용하여 사람이 좀 더 선호할만한 답변을 생성하도록 학습시킨 모델이다.

ChatGPT 가 학습되고 동작하는 방식은 아래에서 잘 설명하고 있다.

<iframe width="560" height="315" src="https://www.youtube.com/embed/bSvTVREwSNw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## 최신 모델들

아래 영상에서 최신 모델의 대충의 흐름 정도를 볼 수 있다.

<iframe width="560" height="315" src="https://www.youtube.com/embed/qu-vXAFUpLE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

개인적으로 최신 모델은 크게 2갈래로 나뉘고 있는 것 같은데, GPT-J 기반의 모델들과 라마기반의 모델들이다. (둘다 디코더 기반의 모델이며, seq2seq 인 t5 등 다른 모델들은 위의 두 모델에 비해 메리트가 좀 떨어지는 것 같다.)

2023년 3월에 메타에서 Llama[^3] 를 공개하고나서 (정확히는 모델의 코드와 파라미터가 유출되어 풀리고 나서) 다양한 모델들이 나오기 시작했다. 스탠포드 대학에서 만든 Alpaca 도 라마를 기반으로 instruction learning (self-instruct) 기법을 적용한 모델이다.

라마는 3B 부터 65B 까지 크기가 다양하게 공개되어 있으며, KoAlpaca 같이 한국어를 데이터를 보강한 모델들도 있다.(최신 KoAlpaca 는 백본을 라마 모델이 아니라 polyglot 을 쓰는거 같고, 해당 모델은 이름대로 여러 언어를 지원하지만 일반적인 인스트럭션 기반으로 동작하는 성능 자체는 라마보다 떨어지는 것 같다.)

라마 기반으로 가장 각광받는 모델들은 Alpaca[^4], Vicuna[^5], StableLM/StableVicuna, WizardLM 이 있다.

GPT-J 는 6B 정도의 상대적으로 크지 않은 모델이지만, 파인튜닝을 적절히 해주면 175B 의 GPT3 보다 성능이 잘 나온다고 알려져 있다.

GPT-J 기반으로 최근 각광받는 모델들은 nomic-ai 의 GPT4ALL-J[^6], databrics 의 Dolly[^7] 가 있다.

위의 모델들이 인기있는 이유는 모델크기가 작더라도 좋은 데이터를(특히 인스트럭션) 충분히 학습시키면 생각보다 성능이 잘나온다는 것이 검증되었기 때문이고, 이러한 특성 때문에 LoRA 같은 아이디어가 나온거 같다.

### 라이센스

라마 모델이 CC-BY-NC 라이센스를 사용하므로 라마를 기반으로 파생된 모든 모델은(정확히는 라마 파라미터를 쓰는 모델) 상업용으로 사용할 수 없다.

LightiningAI 에서 만든 Lit-Llama 같은 게 있지만, 코드에 대해서만 라이센스를 우회했지 모델의 파라미터는 그대로 GPL을 따르게 된다. 직접 처음부터 학습하지 않으면 상업적으로 쓸 수 없기는 매한가지다.

또한 대부분의 모델들은 추가 학습데이터를 만들때 ChatGPT 의 GPT3.5 또는 GPT4 를 사용했기 때문에 역시나 라이센스에서 완전히 자유롭지 못하다.

반면, Dolly 나 GPT4ALL-J 같은 모델들은 아파치2.0 라이센스를 따르므로 상업적으로도 자유롭게 사용할 수 있다.

하지만 현재 개인적으로 백본이 되는 라마의 성능이 GPT-J 에 비해 우월하다고 생각되어서, 라이센스만 보고 선뜻 GPT-J 기반 모델들에 손이 가지는 않는 현실이다.

### 모델 크기

라마가 유출된 덕분에 GPU 카드를 가지고 있는 개인 개발자들이 다양한 컨트리뷰션을 하고 있으며, 이 때문에 모델의 크기를 하나의 GPU 에 넣는 시도도 많아 지고 있다.

일반적으로 6B, 7B 크기를 가진 모델들은 float16 을 사용할 때, 14GB 정도의 GPU 메모리를 사용한다. (float32 를 사용하면 GPU 28GB 가 필요하다.)

하지만 상용으로 팔린 모델들의 GPU 메모리 크기가 보통 8~12GB 이므로 단순 float16 으로는 개인 컴퓨터에 모델을 올리기 어렵다. 따라서 다소 속도를 희생하더라도 이 안에 모델을 구겨넣는 방법들이 많이 나오고 있다.

대표적으로 4bit/8bit quantization 이 있고, cpu offload(주로 스테이블 디퓨전에서 쓰는) 방식이 있다.

quantization 은 float16 의 공간을 8bit int 공간으로 사상해서 메모리를 절약하는 방식인데, 대신 모델 추론 시에는 다시 float16 으로 변환해서 사용하므로 추론 속도가 느려진다는 단점이 있다. (마찬가지로 서비스를 하기에는 속도가 걸린다.)

참고로 AWS 의 G4DN 이나 P3 인스턴스들은 16GB GPU 메모리를 가지고 있는데, float16 으로 7B 모델을 실행하더라도 동시에 여러개의 추론을 실행하면 메모리 문제 때문에 한두개의 추론만 실행할 수 있다. 따라서 7B 모델을 여러 사용자에게 서비스하려면 속도를 다소 희생하고 quantization 을 사용하거나, 하나의 모델을 여러 GPU 에 분산해서 올리고 generation 하는 방식을 써야한다.

### 데이터

요새 모델들은 대부분 the Pile 데이터를 기반으로, 다양한 추가 데이터를 합쳐서 학습을 한다.

대부분의 추가 데이터 인스트럭션 데이터들이며, 사람이 직접 만들어내거나 LLM(ChatGPT, GPT4 등) 을 이용해서 자동으로 만들어 낸다.

대표적으로 Alpaca, Dolly 15k, Evo-instruct 가 잘 알려져 있지만, 별의 별 곳에서 다양한 인스트럭션을 만들어내고 있다.

## 파인튜닝, PEFT

알파카가 7B 라마 모델에 52k 데이터를 3에폭만큼 파인튜닝 하는데 A100 8 GPU 로 3시간 걸렸다고 한다. (AWS 로 치면 p3.24xlarge 정도인데, 비용은 대략 100불정도 들었다고 한다)

사실 GPU 개수만큼 GPU 메모리도 중요한데, 7B 학습시 최소 70GB 의 메모리가 필요하므로 (bfloat16 기준) GPU 를 몇개 쓰느냐와 무관하게 메모리때문에 강제로 높은 사양의 GPU 인스턴스를 써야하기도 한다.

여튼 LLM 은 52k 정도의 작은 데이터를 7B 정도의 크지 않은 모델에 학습하는데 들어가는 비용과 시간도 크기 때문에, 비용효율적으로 학습하는 여러 방법들이 나왔고 이런 방법들을 PEFT (Parameter Efficient Fine Tuning) 이라고 부른다.

현재 잘 알려진 PEFT 방식은 adapter tuning, prefix tuning, prompt tuning, LoRA, IA3 가 있으며 각 방식의 공통점은 백본 모델의 파라미터를 건드리지 않고, 추가적인 파라미터를 학습하는 방식이라고 볼 수 있다.

### LoRA (Low-rank Adaptation)

![LoRA](https://huggingface.co/datasets/trl-internal-testing/example-images/resolve/main/blog/stackllama/lora-animated.gif)

그리고 이중에 현재 가장 많이 쓰이는 방식은 low-rank adaptation 또는 LoRA[^8] 라고 불리는 방식이다. 어느 트랜스포머에서나 적용할 수 있기 때문에, 스테이블디퓨전에서도 이미 많이 쓰이고 있었다.

대충 LoRA 보다 앞서 나온 방법들은 추론시 속도에 영향을 주거나(adapter), 학습시 모델의 제약을 걸게 되는데(prefix) LoRA 는 그런 단점을 다 우회하고 적은 파라미터로 빠르게 학습할 수 있다는 장점이 있다. (매트릭스 Rank 에 대한 내용은 여기[^9]를 참조하자.)

LoRA 의 아이디어는 대충 GPT3 175B 있지만 실제로 파라미터의 랭크는 낮을 것이라는 가정이고, 파라미터의 랭크가 낮다면 백프로퍼게이션시 파라미터 델타값도 랭크가 낮을 것이기 때문에, 파라미터 델타값을 계수가 높은 더 작은 행렬로 근사시켜서 학습하면 된다는 것이다. (이 때 어텐션의 키와 밸류에 LoRA 를 적용한다.)

infused adapter by inhibiting and amplifying inner activations or IA3 는 더 최근에 나온 방식인데 어텐션의 키와 밸류 매트릭스, FF 레이어 를 스케일링 하는 어댑터(?) 를 추가하는 방식인데, 얘는 내가 공부를 제대로 안해서 잘 모르겠지만, 여튼 LoRA 보다 다소 복잡한 대신 LoRA 의 1/10 파라미터인데 성능은 더 좋은 것 같다.(파라미터가 적으니 속도도 더 빠르고.. 약간 사기?)

### RAG (Retrieval Augmented Generation)

일반적으로 LLM 에 요청해서 답변을 받는 것은 closed-book query 라고 볼 수 있다. LLM 이 사전학습을 통해 가지고 있는 정보에 의존하기 때문이다.

그런데 closed-book query 방식은 할루시네이션(hallucination) 이 잘 일어난다. 최신의 데이터를 요청하면 최신의 답변을 내놓아야 하는데, closed-book query 방식은 이미 학습 된 데이터를 기반으로 최대한 근접한 답변을 내놓기 때문이다. (이런 현상을 할루시네이션 이라고 한다.)

이런 할루시네이션을 해결하는 대표적인 방법으로 위에 살펴본 fine-tuning 방식과 RAG 방식이 있다.

파인튜닝은 모델이 너무 큰 경우 PEFT 를 쓰더라도 학습이 오래 걸리고, 데이터의 추가가 빈번할 경우 파인튜닝 주기를 짧게 해야하기 때문에 잦은 배포에 대한 부담도 동반된다. 또한 LLM이 새로 학습 시킨 데이터를 반드시 사용한다는 보장을 할 수 없다는 점도 문제이다.

<img src="https://jalammar.github.io/images/retro/Large-GPT-vs-Retro-transformer-world-knowledge-information.png" />

이런 문제를 해결하기 위해 외부 저장소를 open-book query 모델로 전환하는 방식이 RAG 이다.

방법은 대략 아래와 같다.

<img src="https://nextbigfuture.s3.amazonaws.com/uploads/2023/04/Screen-Shot-2023-04-05-at-8.58.22-AM-1024x588.jpg" />

1. 필요한 문서들을 모두 임베딩해서 저장해둔다. (보통 OpenAI text-embedding-ada-002, SentenceBERT 등을 쓴다)
2. 쿼리에 근접한 문서 상위 k 를 가져온다.
3. 프롬프트 컨텍스트에 추가해서 제너레이션을 한다.

### Vector database

RAG 에서 임베딩 데이터를 저장해두는 곳을 vector database 라고 한다.

해당 서비스의 특성에 대해서 잘 설명한 글[^18] 을 참고하면 직접 구현할 때도 도움이 될 것 이다.

여튼 vector database 는 임베딩 데이터를 저장하고 쿼리할 수 있는 저장소이며, 예전에 이미지 검색을 위해 사용했던 방식과 완전히 동일하다.

위의 글에 나온대로 LSH, Elasticsearch(or Opensearch) 등을 이용하면 직접 구현할 수 있지만, 테스트나 연구용으로는 Pinecone 이나 ChromaDB 등의 서비스를 많이 쓰고 있다.

## 추론

추론은 huggingface 공식문서 두개[^10][^11] 만 참조하면 된다.

### temperature 와 top_p

중요한 파라미터는 temperature 와 top_k 또는 top_p 이며, 해당 파라미터를 조절하면서 적절한 값을 찾아야 한다.

원리는 위의 링크에 잘 나와있지만, 대충 temperature 와 top_p 를 올리면 아무말을 잘하게 되고, 낮추면 variation 이 떨어지지만 더 일관된 말을 하게 된다.

그리고 do_sample 파라미터를 줘야 샘플링을 하고 없으면 greedy search 를 하게 된다.

### num_return_sequences

다양한 생성결과를 위해 num_return_sequences 파라미터도 설정할 수 있는데 생성시 토큰 수와 메모리에 영향을 준다. (토큰수에 영향을 주기 때문에 속도에도 영향을 준다고 봐야...)

따라서 메모리를 좀 더 쓰더라도 다양한 생성결과를 원한다면 해당 파라미터를 활용하면 좋다.

### repetition_penalty or no_repeat_ngram_size

반복되는 문장을 제거하기 위해 repetition_penalty 또는 no_repeat_ngram_size 파라미터를 설정할 수 있는데, repetition_penalty 는 반복되는 토큰에 패널티를 주는 방식이고, no_repeat_ngram_size 는 ngram 을 설정해서 해당 ngram 이 반복되지 않도록 하는 방식이다.

reptition_penalty 는 명확하게 반복을 막는것이 아니며 경우에 따라 반복 자체는 나쁘지 않은 경우도 많기 때문에(e.g. Amazon 서비스에 대한 설명을 하는 봇의 경우 AWS, Amazon 이라는 단어를 서비스 앞에 계속 붙여줘야 한다.), no_repeat_ngram_size 를 사용하는 것이 긴 문장 생성시 더 좋은 결과를 얻을 수 있는 것 같다.

### 스트리밍

챗UI 를 위해 보통 Gradio[^12] 를 쓰는거 같지만 이 툴은 모델을 빠르게 테스트 하라고 만든 툴이지 실제 사용자한테 서빙하라고 만든 툴은 아니다. (vicuna 는 fastchat 이라는 툴을 직접 만들어서 제공한다.)

결국 서버는 FastAPI 를 기반으로 직접 만들어야 하는데 7B 모델을 512 길이로 GPU 로 추론시 보통 20초 정도가 걸리기 때문에 스트리밍이 없이 그냥 요청을 받아서 처리하면 사용자 경험이 너무 안좋다.

다행히 최근에 huggingface 모델의 generate 함수에서 streamer 파라미터를 지원해주고 있어서 (preview 라 아직 불안정 하지만) 이걸로 스트리밍을 구현할 수 있다.

채팅이긴 하지만 서버측의 레이턴시가 굉장히 길기 때문에 웹소켓 보다는 그냥 SSE 정도만 해줘도 된다.

## 프롬프트 엔지니어링

프롬프트 엔지니어링 가이드[^13] 를 보면 대충 어떻게 프롬프트를 만들어야 하는지 나와있다.

프롬프트 엔지니어링은 LLM 모델이 내가 원하는 결과를 잘 내놓지 않을 때, 내가 원하는 결과를 잘 내놓도록 모델을 조정하는 방법이다. 모델의 파라미터를 업데이트 하지 않고 인풋 파라미터를 조정하는 방식이므로 훨씬 빠르고 쉽게 모델을 개선할 수 있다. (in-context learning, instruct gpt 이나 flan 등의 다양한 인스트럭션 방식에서 프롬프트 엔지니어링이 효과적이라는 점을 보여주고 있다.)

현실적으로는 프롬프트 엔지니어링이 필요하지만 너무 휴리스틱하고 모델별로, 학습된 데이터의 형태에 따라서 다 달라지기 때문에 일관성이 없다.

특히 모델의 성능이 충분히 좋아야만 효과가 있기 때문에 작은 모델의 경우 프롬프트 엔지니어링만으로 원하는 결과를 내기가 어렵다.

요새 많이들 쓰는 LangChain[^15] 이나 Auto-GPT[^16] 도 ReAct[^14] 를 근거로 한 프롬프트 엔지니어링 기반으로 동작하고 있기 때문에 백본 모델의 성능에 따라 동작하던 체인이 동작하지 않더라도 전혀 이상할게 없다.

물론 모델 성능은 앞으로 계속 우상향하면서 올라가겠지만 사내에서 한두가지의 작업을 하기 위해 작은 모델을 여러개 운영을 하려고 하면 해당 툴이 사용하는 일반적인 방식은 동작하지 않을 가능성이 높다. (그럼 결국 그냥 손으로 프롬프트 엔지니어링 하는거랑 큰 차이가 없다.)

따라서 좀 더 정형화되어서 모든 모델에 적용할 수 있는 방식이 나와서 프롬프트 엔지니어링을 더이상 안해도 되는 상황이 왔으면 좋겠다.

## 왜 7B 이 인기인가?

<iframe width="560" height="315" src="https://www.youtube.com/embed/ORYQU0RYn_M" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

위의 영상에서 현재 7B 가 가장 활발히 연구되는 이유로 연구비용 대비 성능의 균형을 들고 있다.

실제로 대부분의 온프레미시 연구장비 및 클라우드가 16GB vram 을 제공하고 있고, 7B 를 fp16 으로 로드하면 vram 을 14GB 정도 사용하게 되므로, 생성에 필요한 메모리 등을 고려하면 7B 가 가성비상 가장 좋은 모델이 된다.

## 마치며

최근 공부한 내용중 일부를 정리겸 적은거라 다소 두서가 없지만 이 글에 나온 단어들만 대략 이해하고 있어도 최근 나온 모델을 실행하고 테스트하는 데는 전혀 문제가 없을 것이다.

개인적으로 주로 보는 채널은 아래와 같은데 colab 노트북도 대부분 제공하고 있어서 예제도 딱히 필요가 없다. 그냥 그대로 colab 에서 실행하거나 세이지메이커 노트북에 업로드후 실행하면 된다.

- [https://www.youtube.com/@code4AI](https://www.youtube.com/@code4AI)
- [https://www.youtube.com/@samwitteveenai](https://www.youtube.com/@samwitteveenai)

---

[^1]: [The Illustrated Transformer](https://nlpinkorean.github.io/illustrated-transformer/)
[^2]: [The Illustrated BERT](https://nlpinkorean.github.io/illustrated-bert/)
[^3]: [Introducing LLaMA](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/)
[^4]: [Alpaca Lora](https://github.com/tloen/alpaca-lora)
[^5]: [Vicuna](https://github.com/lm-sys/FastChat)
[^6]: [GPT4ALL-J](https://github.com/nomic-ai/gpt4all)
[^7]: [Dolly](https://github.com/databrickslabs/dolly)
[^8]: [LoRA](https://www.youtube.com/watch?v=BJqwmDpa0wM)
[^9]: [행렬의 계수](https://www.youtube.com/watch?v=HMST0Yc7EXE)
[^10]: [Text generation strategies](https://huggingface.co/docs/transformers/v4.28.1/en/generation_strategies)
[^11]: [How to generate text](https://huggingface.co/blog/how-to-generate)
[^12]: [Gradio](https://gradio.app/)
[^13]: [Prompt Engineering](https://www.promptingguide.ai/)
[^14]: [ReAct](https://www.promptingguide.ai/techniques/react)
[^15]: [LangChain](https://python.langchain.com/en/latest/index.html)
[^16]: [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT)
[^17]: [LLM Examples](https://github.com/haandol/LLM-Examples)
[^18]: [Vector Database](https://www.pinecone.io/learn/vector-database/)