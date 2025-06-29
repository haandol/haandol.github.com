---
layout: post
title: SLM 파인튜닝 하기 전에 알아두면 좋은 내용 - 1/2
excerpt: Demystifying Small Language Model(SLM) Fine-tuning - 1/2
author: haandol
email: ldg55d@gmail.com
tags: ai llm slm fine-tuning fsdp deepspeed aws sagemaker
publish: true
---

## TL;DR

- 도메인 특화 모델을 만들어야 한다면 SLM 파인튜닝을 고려해보자
- 아니면 일단 LLM + RAG 로 시작하자

## 시작하며

팀에서 코드 생성용 모델을 파인튜닝할 일이 생겨서 한번 해보기로 했다.

SDXL 파인튜닝 같이 HuggingFace 공식 recipe 나 남들이 올려둔 코드를 적당히 수정해서 쓰면 될 줄 알았는데, 생각보다 알아야 할 것이 많았다.

나처럼 처음 SLM (Smaller Language Model)을 파인튜닝을 할 때 알아두면 좋은 점들을 정리해본다.

글은 2개로 나눠서, 이 글은 추상화된 내용을 다루고, 다음 글에서는 실제로 파인튜닝을 하는 코드와 주요 파라미터들을 간단히 설명하는 식으로 진행할 예정이다.

## SLM vs LLM

인터넷에 검색해보면 SLM 과 LLM 을 비교할 때 운영 비용에 집중해서 말하는 경향이 있다. 하지만 단순 운영 비용은 전체 비용대비 작은 부분이라고 생각한다.

이것은 마치 IDC 를 운영하는 것과 AWS 를 쓰는 것과 같은 차이와 유사하다. IDC 는 운영해본 사람이 많기 때문에 AWS 를 썼을때 IDC 를 직접 운영하는 것대비 어떠한 작업들이 줄어드는지 알기 쉽고, 그에 대한 장단점과 비용적인 이득을 계산하기 용이하다.

이 운영 비용 중, 특히 토큰당 비용을 계산할 때 query per day 같이 동시성을 무시한 메트릭으로 대충 계산하는 경향이 있는데, 동시성이 높아져도 사용자 경험을 해치지 않으려면 추가적인 비용이 발생하고, 이것은 생각보다 비용이 많이 들어간다. (이 부분은 SLM 뿐만 아니라 SDXL 같은 이미지 생성 모델도 마찬가지다.)

또한 운영비용 외에도 SLM 클러스터를 직접 운영하는 순간부터 API 기반으로 LLM 을 쓰던 것보다 엄청나게 많은 일을 감당하게 된다. 우리는 대부분 ChatGPT 나 Anthropic 같은 LLM 플랫폼을 직접 운영해본 경험 없기 때문에, 이런 시스템을 직접 운영하면 무엇이 추가적으로 필요한 지 잘 알지 못한다.

실제로는 기존 AI 시스템에서 하던 모델 버전 관리, 모델 배포, 모델 평가, 모델 튜닝 등의 MLOps 작업은 물론이고 LLM 의 특성에 따른 시멘틱 캐싱, 모델별 동시성 제어, 가드레일, 벡터 데이터베이스 운영 등의 추가적인 작업들이 요구된다. 각각의 작업이 어려운 내용은 아니지만 기존과 다른 기술 스택이나 개념을 도입하고 운영하는 것은 팀의 리소스를 많이 필요로 하기 마련이다.

## RAG vs Fine-tuning

SLM 과 LLM 의 선택의 문제는 자연스럽게 RAG 와 Fine-tuning 의 선택의 문제로 이어진다. 실제로 내부 실험결과 LLM + RAG 로는 원하는 결과가 나오지 않아서, 파인튜닝을 해야 하기 때문에 SLM 을 선택하는 경우가 많다.

RAG 와 Fine-tuning 중 무엇을 도입해야 하는가에 대해서는 다양한 관점이 있다. 최근에 MS 에서 나온 논문[^1]에서는 아래와 같은 기준을 제시한다. 

- RAG (Retrieval-Augmented Generation)가 유리한 경우:
  - 데이터가 맥락적으로 관련성이 높을 때
  - 초기 비용이 낮아야 할 때
  - 외부 데이터를 실시간으로 활용해야 할 때
  - 대규모 데이터셋에서 관련 정보를 효과적으로 검색해야 할 때
- Fine-Tuning이 유리한 경우:
  - 특정 도메인에 대한 새로운 지식이나 기술을 모델에 학습시켜야 할 때
  - 간결하고 정확한 답변 생성이 필요할 때
  - 도메인 특화된 성능 향상이 필요할 때
  - 장기적으로 모델의 성능을 개선하고자 할 때

즉, RAG 는 초기 비용이 낮아야 하거나, 외부 데이터를 실시간으로 활용해야 할 때 유리하고, Fine-tuning 은 특정 도메인에 대한 새로운 지식이나 기술을 모델에 학습시켜야 할 때 유리하다.

개인적으로, SDXL 파인튜닝 경험을 비춰봤을땐 학습 비용이 너무 많이 나오지 않을까 고민했었다. 실제로 예전에는 파인튜닝을 위한 비용이 커서 부담이 되는 정도였지만, 요즘은 하드웨어 비용도 계속 내려가고 있으며, QLoRA[^2] 같은 최신 기법들의 지원으로 파인튜닝에 대한 비용과 시간이 많이 줄어드는 추세이다.
(예로 Gemma2-9b 을 15k 정도 되는 데이터로 3 에폭 동안 파인튜닝하는데 g5.16xlarge 로 11시간정도 걸리고 비용으로는 $50 정도 든다. 그리고 p4d.24xlarge 등의 멀티 GPU 환경에서 FSDP 나 DeepSpeed 를 쓰면 시간과 비용을 줄일 수 있다.)

그리고 SLM 을 쓴다고 해서, 모든 요청을 꼭 SLM 만 써야하는 것은 아니므로, RAG 와 Fine-tuning 을 혼합해서 쓰는 것도 좋은 방법이다. 예를 들면, 시멘틱 라우팅이나 RouteLLM[^3] 같은 방법을 통해 도메인 특화된 요청과 아닌 요청을 구분해서 도메인 특화된 내용은 SLM + Fine-tuning 로 처리하고 그외는 LLM + RAG 로 처리하는 방법이 있겠다.

## 모델 고르기

여튼 본 글에서는 SLM 을 파인튜닝 하기로 했으니, 이제 어떤 모델을 쓸 지 고민해볼 차례이다.

모델 평가 벤치마크들도 다양하게 있기 때문에 이를 참고해서 모델을 선택하면 된다. 일반 챗봇을 만든다면 LMSys 의 Chatbot area leaderboard[^6] 를 참고할 수 있고, 코드 생성을 위한 모델을 찾는다면 EvalPlus leaderboard[^7] 를 참고할 수 있으며, SQL 쿼리 생성을 위한 모델을 찾는다면 Spider leaderboard[^8] 를 참고할 수 있다.

여튼 파인튜닝은 도메인 특화된 정보를 학습시키기 위한 것이므로, 도메인에 맞는 모델을 선택하는 것이 중요하다. 

### 라이센스

학습한 모델을 상업적으로 사용해야 한다면 모델의 라이센스도 반드시 체크해야한다.

이 때, 모델 코드의 라이센스와 모델의 가중치에 대한 라이센스가 다를 수 있으며, 특히 가중치의 라이센스는 데이터의 라이센스와도 연관이 있기 때문에, 세가지를 모두 체크해야 한다.

예를 들면, SAM[^4] 같은 모델이 있는데, 코드의 라이센스는 Apache 2.0 이지만, 가중치의 라이센스는 명시적으로 적혀있지 않다. 하지만 사용된 데이터인 SA-1B[^5] 의 라이센스가 research-only 라고 명시되어 있기 때문에 SAM 을 기반으로 프로덕션 서비스를 만드는 것은 불가능 하다고 할 수 있다. (SemanticSAM 등 SA-1B 데이터를 사용한 파생모델들 모두 마찬가지다.)

## 데이터셋 준비하기

일반적으로 파인튜닝은 Supervised Fine-tuning 이며, 데이터셋은 Alpaca 스타일의 인스트럭션 데이터셋을 많이 사용한다. 이 때, 목적에 따라 인스트럭션 데이터셋을 만들어 내는 기법이 다양하게 있기 때문에 이를 참고해서 데이터셋을 만들어야 한다.

대표적인 예가 Orca[^9] 모델과 사용된 데이터 셋이 있다. 이 데이터셋은 SLM 의 추론 능력을 향상시키기 위해서 LLM(e.g. GPT-4)의 응답을 기반으로 만들어진 데이터 셋이다. 이 데이터 셋은 라이센스 문제로 사용할 수 없다. 그래서 커뮤니티에서는 같은 방식으로 MIT 라이센스의 OpenOrca[^10] 라는 데이터셋을 만들었고, 우리는 이를 이용하여 파인튜닝하면 복잡한 추론 문제를 풀 수 있는 모델을 만들 수 있다.

## 학습환경

라이브러리는 그냥 trl[^11] 을 쓰자. 이름만 봐서는 강화학습만 할 것 같지만, 현재 일반적인 LM 강화학습의 단계가 SFT(Supervised Fine-tuning), Reward Modeling, PPO(or DPO) 로 이뤄져 있어서 3 단계를 모두 다 커버하고 있다. SFT 만 하는 경우에도 사용하기 무난하다.

회사내에서 학습한다면, 기존에 있던 MLOps 환경을 그대로 써야겠지만(Amazon Sagemaker 등), 초기 설정 단계라 환경 선택에 자유롭다면 Unlsoth[^12] 를 사용해보는 것을 추천한다. 최신 기법들 (Flash attention  등)을 자동 적용한 트레이너를 라이브러리로 제공하고 있어서, trl 라이브러리와 유사하게 학습하면 학습 속도를 줄이고 메모리 사용량도 줄일 수 있다. (메모리 사용량을 줄여서 배치사이즈를 키우거나 컨텍스트 길이를 늘릴 수 있다.)

### 멀티 GPU 환경에서 파인튜닝

위에서 언급한대로 멀티 GPU 를 이용하여 학습하면 시간과 비용을 줄 일수 있다. 

llama3 를 FSDP + QLoRA 로 Sagemaker Training job 으로 학습하는 예제[^13] 를 참고하면 좋다.

FSDP(Fully Sharded Data Parallel) 방식은 Pytorch 에서 제공하는 기능으로, 멀티 GPU  환경에서 GPU 사용 메모리를 줄이기 위해 모델의 파라미터를 여러 GPU 에 샤딩하는 방식이다.

Deepspeed 는 MS 에서 학습/추론 최적화를 위한 라이브러리로 ZeRO(zero redundancy optimzer) 기법을 구현해두었다.

실제 내부 동작 방식은 다소 다르겠지만, 그냥  개발자 입장에서 보면 FSDP 와 Deepspeed 둘다 멀티 GPU 환경에서 샤딩 전략을 선택해서 큰 모델을 여러 GPU 에 분산하여 추론할 수 있게 해주거나, 학습할  수 있게 도와주는 라이브러리라고 생각하면 될 것 같다.

### QLoRA

QLoRA 는 Quantization 기법을 LoRA 학습과정에 사용하는 방법으로, LoRA 에 비해 메모리 사용량을 더 줄일 수 있다. 보통 4bit quatization 을 사용한다.[^2] huggingface 의 peft 라이브러리를 사용하면 쉽게 적용할 수 있다.

### 샤딩 전략

샤딩 전략만 ZeRO 를 기준으로 간단히 설명하고 마친다. accelerate 를 이용하면 FSDP 를 사용하더라도 ZeRO 의 각 Stage 에 대응하는 전략을 사용하여 학습할 수 있다.

먼저 LLM 학습시 GPU 에 올려둬야하는 메모리는 크게 3종류가 있다.
- 모델 파라미터
- 그래디언트
- 옵티마이저 상태 (Adam, SGD 등)

특히 옵티마이저는 계산 방식에 따라 (AdamW, SGD 등) 메모리 사용량이 달라진다. AdamW 의 경우 모멘텀 계산을 위해 평균과 분산을 저장해둬야 하기 때문에, 옵티마이저에만 모델 파라미터 개수의 2배를 사용한다. (7B 모델이면 7B * 4bytes = 28GB)

따라서 ZeRO 는 위의 3가지를 적절히 멀티 GPU 에 샤딩하는 방법을 제공한다.

- ZeRO Stage 1
  - 옵티마이저 상태(optimizer states)를 분할한다.
  - 각 GPU는 전체 모델 파라미터와 그래디언트를 유지하지만, 옵티마이저 상태의 일부만 저장한다.
- ZeRO Stage 2
  - Stage 1의 기능에 더해 그래디언트(gradients)도 분할한다.
  - 각 GPU는 전체 모델 파라미터만 유지하고, 그래디언트와 옵티마이저 상태는 부분적으로 저장한다.
- ZeRO Stage 3
  - 모델 파라미터(parameters), 그래디언트, 옵티마이저 상태 모두를 분할한다.
  - 각 GPU는 모든 모델 상태의 일부만 저장한다.
  - 메모리 사용량이 데이터 병렬화 정도에 비례하여 감소한다.
  - 통신 오버헤드가 약간 증가하지만, 매우 큰 모델 학습이 가능해진다.
- ZeRO-Infinity
  - ZeRO Stage 3를 확장한 버전.
  - CPU 메모리와 NVMe SSD를 활용하여 GPU 메모리 제한을 극복한다 .
  - 효율적인 오프로딩 엔진을 통해 대역폭 문제를 최소화한다 .
  - 수조 개의 파라미터를 가진 모델도 학습할 수 있게 해준다.
- ZeRO-Offload
  - ZeRO Stage 2와 유사하지만, 옵티마이저 연산과 메모리를 CPU로 오프로드한다.
  - 단일 GPU에서도 대규모 모델 학습이 가능해진다.

---

[^1]: [Whast is better? RAG? Fine-tuning?](https://x.com/_philschmid/status/1751207473535393999)
[^2]: [QLora](https://medium.com/@dillipprasad60/qlora-explained-a-deep-dive-into-parametric-efficient-fine-tuning-in-large-language-models-llms-c1a4794b1766)
[^3]: [RouteLLM](https://github.com/lm-sys/RouteLLM)
[^4]: [SAM](https://segment-anything.com/)
[^5]: [SA-1B Datset](https://ai.meta.com/datasets/segment-anything/)
[^6]: [LMSYS Chatbot Arena Leadboard](https://chat.lmsys.org/?leaderboard)
[^7]: [EvalPlus Leaderboard](https://evalplus.github.io/leaderboard.html)
[^8]: [Sipder2-V](https://spider2-v.github.io/)
[^9]: [Orca](https://www.microsoft.com/en-us/research/blog/orca-2-teaching-small-language-models-how-to-reason/)
[^10]: [OpenOrca](https://huggingface.co/datasets/Open-Orca/OpenOrca)
[^11]: [trl](https://huggingface.co/docs/trl/index)
[^12]: [Unlsoth](https://unsloth.ai/)
[^13]: [fine-tune llama3 with fsdp and q-lora](https://www.philschmid.de/fsdp-qlora-llama3)