---
layout: post
title: AI Agent 개발 할 때 고민해볼 내용
excerpt: Demystifying AI Agent for Developers
author: haandol
email: ldg55d@gmail.com
tags: ai agent llm
publish: true
---

## TL;DR

- AI Agent 란 `특정한 작업을 주어진 리소스를 이용하여 완료할 수 있는 인공지능 기반의 프로그램` 이다.
- 바꿔 말하면 특정한 작업을 입력받고, 리소스를 할당받아서, 완료조건을 기준으로 반드시 작업을 완료하는 인공지능 기반 프로그램이다.

## 시작하며

최근 AI 에이전트 기반의 로보틱스 프로젝트를 하게 되었다. 에이전트 방식으로 LMM (Large Multimodal Model) 을 사용해보니 단순 프롬프트로만 처리했을 때보다  훨씬 다양한 문제를 풀 수 있다는 것을 알게되었다.

개인적으로는 AI 에이전트(이하 에이전트) 가 앞으로 대세가 될 것 같은 느낌은 있지만, 다른 사람들에게 설명할 정도로 깊이 고민한 적은 없었다. 

이번 기회에 서버 개발자로서 느낀 에이전트에 대해서 간단히 정리해보려고 한다.

## AI 에이전트란?

일단 AI 에이전트의 정의부터가 조금씩 다르기 때문에 이걸 먼저 정의하고 넘어가야 할 것 같다.

AWS 에서는 AI 에이전트를 다음과 같이 정의한다.[^1]

```text
An artificial intelligence (AI) agent is a software program that can interact with its environment, collect data, and use the data to perform self-determined tasks to meet predetermined goals.
```

GPT-4o 한테 물어보니 다음과 같이 정의해줬다.

```text
AI 에이전트(AI Agent)는 특정 작업을 수행하거나 문제를 해결하기 위해 설계된 소프트웨어 프로그램 또는 시스템으로, 인공지능(AI) 기술을 활용하여 자동화된 방식으로 작동합니다. AI 에이전트는 자율적으로 행동하고, 데이터를 처리하며, 환경과 상호 작용할 수 있습니다
```

다른 곳에서는 각각 자신들의 논지에 맞춰서 위의 설명을 조금씩 바꿔가면서 정의를 내리고 있기 때문에 AI 에이전트라는 단어는 아직 해석이 정립되어 가는 과정에 있는 단어라고 볼 수 있다.

위의 정의를 기반으로 예를 들어보자.
- LLM 프롬프트 하나로만 충분히 처리할 수 있는 작은 프로그램은 에이전트라고 부를 수 없을까? (추가적인 데이터도 필요없고 환경과 상호작용도 필요없는데)
- 혹은, 현재의 날씨를 지난 1주일간의 날씨 데이터를 이용해서 예측하는 프로그램은 에이전트라고 부를 수 있을까? (추가적인 데이터에 접근하고 환경과 상호작용하는 인공지능 기반의 프로그램인데) - 그리고 그런 작업을 엄청 복잡하고 거대한 컴퓨팅 자원을 써서 1주일간 돌리는 프로그램은 어떨까?

답은 아마도 DDD 의 유비쿼터스 언어와 같이 도메인안에서 해석하기 나름이 될 것이다.
여튼 다양한 방식으로 해석할 수 있는 것이 현재 AI 에이전트의 정의이다 보니 고객이나 다른 개발자와 이야기 할 때 커뮤니케이션이 산으로 갈때가 많다.

그래서 실제 구현을 위한 이야기할 때는 좀 더 구체적이면서 기능과 효용에 기반한 정의가 필요하게 된다.

이런 이유로 개인적으로는 AI 에이전트를 부를 때는 다음과 같은 정의를 염두해두고 이야기를 하는 편이다.

```text
특정한 작업을 주어진 리소스를 이용하여 완료할 수 있는 인공지능 기반의 프로그램
```

위의 내용은 다음과 같은 전제를 포함하고 있다.

- 에이전트는 특정한 작업을 입력으로 받는다.
- 에이전트는 시작시 해당 작업을 완료하기 위해 리소스를 할당 받는다. (마치 프로세스 처럼)
- 리소스는 작업 완료에 필요한 비용을(시간, 도구 등) 의미한다.
- 에이전트는 주어진 작업을 반드시 완료한다. (실패도 완료로 간주한다.)

즉, 현재의 AI 에이전트란:

사용자로 부터 하나의 목적을 가진 작업을 입력으로 받고 작업을 실행하기 위한 리소스를 할당 받아서 실행되는 인공지능 기반의 프로그램이다.

이 프로그램은 작업완료에 대한 정의를 내부에 가지고며 있으므로 지정된 리소스를 최대한 활용하여 반드시 작업을 완료한다.

> 현재라고 제한을 걸어둔 이유는 AGI 와 같이 여러개의 서로 다른 복잡한 작업을 처리하는 능력이 현재의 LLM 에게 아직 없다고 보기 때문이다.

## 프레임워크 선택

위와 같이 에이전트에 대한 정의를 내리고 구현 단계에 들어가게 되면 어떤 프레임워크를 이용하여 개발을 진행할 지 고민하게 된다.

현재 잘 알려진 에이전트 프레임워크로는 다음과 같은 것들이 있다.

- Autogen[^2]
- CrewAI[^3]
- Llama Index[^15]
- Langchain Agent[^4]
- LangGraph[^5]
- 직접 만들기

모든 프레임워크는 각각의 장단점이 있어서 뭘 써야할 지 고민이 많이 될 것이다. 나도 툴 선택에 있어서 고민을 많이 하고 자료를 찾아봐도 잘 모르겠어서 결국 튜토리얼을 다 해봤다. 그리고 나서도 장단점들이 명확해서 계속 고민을 하게 되었다.

이 때 도움이 되는 것이 위에 설명한 에이전트의 정의였다.

`에이전트는 주어진 작업을 완료하기 위해서 스스로 생각하고 동작한다.`
에이전트의 내부 구현 자체는 대부분 ReAct[^6] 또는 OpenAI Agent[^7] 기반이며 둘다 탈출조건(작업 완료) 이 만족되기 전까지 재귀적으로 LLM 을 계속해서 호출하게 된다. 
그런데 두 방식 모두 특별한 구현이 없다면 이를 중간에 끊을 수 있는 방법이 딱히 없다.
(예를 들면, 스스로 코드를 수정하면서 코드 생성을 하는 에이전트의 경우 LLM 이 특정 에러에 대해서 코드를 고치지 못하고 같은 에러를 계속해서 내면서 반복하는 경우가 있다.)

이런 `리소스 제어` 의 측면에서 현재 langgraph 외에는 위의 정의를 만족하지 못하기 때문에 실제 프로젝트를 진행할 때는 llama-index workflow, langgraph 외에 다른 프레임워크를 선택하기 어려운 것 같다.

상태 전이를(혹은 추론과정) 기반으로 동작 제어 하는 기능을 직접 구현한다면 다른 프레임워크를 사용할 수도 있겠지만 그렇게 되면 프레임워크를 사용하는 이유가 없어지는 것이기 때문에 직접 state machine 을 구현하거나 llama-index workflow, langgraph 를 사용하는 것이 가장 현명한 선택이 될 것이다.

### 예외상황

그래서 개인적으로 추천하는 것은 llama-index workflow, langgraph 를 사용하거나 직접 구현하는 것이지만 예외적인 상황도 있다.

바로 상태 전이를 정의할 수 없는, 처음 보는 워크로드의 경우이다. (리서치 분야 같이)
이런 경우에는 crewai 나 autogen 처럼 그냥 상태의 설계 자체도 에이전트에 맡기는 것이 더 나은 선택이 될 수도 있다.

또한, RL (Reinforcement Learning) 를 써보면 알 수 있지만 학습된 최적의 보상함수는 직관에 어긋나는 경우가 많다. 
같은 의미로 사람이 만든 워크플로우(state machine) 이 최적이 아닐 수도 있다. 이런 경우를 고려했을때도 autogen 처럼 에이전트에게 계획 세우는 부분을 맡겨보는 것도 나쁘지 않은 선택이 될 수도 있다.

## Observability

리소스 관점에서 에이전트는 자신의 아웃풋을 다음에 자신이 사용할 LLM 프롬프트에 증분해가면서 재귀적으로 동작한다.
이 때문에 에이전트가 어떻게 동작하는지, 어떤 데이터를 사용하고 있는지, 어떤 리소스를 사용하고 있는지 등을 파악하기 위해서는 Observability (특히 Traceability) 가 필요하다.

이를 위한 툴들로 많이 쓰이는 것은 다음과 같다.

- Langsmith[^8]
- Weights & Biases[^9]
- Langfuse[^10]
- Arize Pheonix[^16]

langsmith 가 langchain 과 가장 쉽게 호환되는 툴이기 때문에 langsmith 를 사용하는 것이 가장 무난한 선택이지만 약간의 코드를 추가 한다면 비용측면에서 wandb 가 더 매력적이며, 로컬에서 테스트 하거나 비용효율적인 방식을 원한다면 langfuse 가 더 나은 선택이 될 수도 있다.

특히 보안이 필요한 기업환경에서 라이센스를 같이 고려했을 땐 self-hosting 이 가능하면서 MIT 라이센스를 가지고 있는 langfuse 나 Arize Pheonix 를 사용해야 한다.

## 배포

에이전트 개발을 했다면 배포를 해야하는데 이 때 가장 크게 고민되는 부분은 에이전트를 `어떤 단위로 패키징해서 배포할 것인가` 일 것이다.

가장 일반적인 방식은 에이전트와 툴을 한번에 패키징해서 배포하는 방식이다. 
툴들을 에이전트와 통합해서 배포하게 되면 에이전트가 동작하는 환경을 쉽게 구축하고 배포할 수 있다. 
다만 툴의 업데이트가 빈번하게 일어나는 경우에는 에이전트를 업데이트 하기 위해서 전체를 다시 배포해야 하는 단점이 있다.

이에 반해 Amazon Bedrock Agent[^11] 의 경우에는 에이전트와 툴을 따로 분리해서 배포하는 방식을 쓰고 있다. 
툴은 람다를 통해서 배포되고 에이전트는 람다에 배포된 툴들을 호출하는 방식을 가지고 있기 때문에 툴과 에이전트의 배포를 서로 독립적으로 가져갈 수 있다는 장점이 있다.

전자의 방식은 모노리스 방식에 가깝고 후자의 방식은 마이크로 서비스 방식과 가깝다고 생각하는데 실제로 운영할 때 분산 트레이싱을 통한 디버깅의 편의성 측면에서도 비슷한 특성을 가지고 있다.

## 마치며

Devin[^12], MultiOn[^13] 과 같은 서비스를 보면서 앞으로 필요한 에이전트를 API 처럼 제공받는 에이전시(또는 OpenAPI 같은 개념으로의 OpenAgent, Meshup) 가 나오지 않을까 하는 생각이 들었다.

이런 서비스가 나오면 개발자들은 에이전트를 직접 개발하지 않고도 쉽게 에이전트를 사용할 수 있게 되어서 더 많은 사람들이 AI 에이전트를 사용하게 될 것이다.

Langgraph 에 대한 정말 좋은 강의[^14]가 DLAI 에 무료로 올라와 있으니 에이전트에 관심있는 사람들은 반드시 들어보는 것을 권장한다.

---

[^1]: [What are AI Agents?](https://aws.amazon.com/what-is/ai-agents/)
[^2]: [Autogen](https://microsoft.github.io/autogen/)
[^3]: [CrewAI](https://www.crewai.com/)
[^4]: [Langchain Agent](https://python.langchain.com/v0.1/docs/modules/agents/)
[^5]: [Langgraph](https://langchain-ai.github.io/langgraph/)
[^6]: [ReAct](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/react/)
[^7]: [OpenAI Agent](https://platform.openai.com/docs/guides/function-calling)
[^8]: [Langsmith](https://www.langchain.com/langsmith)
[^9]: [Weight & Biases Tracing](https://wandb.ai/site/traces)
[^10]: [LangFuse](https://langfuse.com/)
[^11]: [Amazon Bedrock Agent](https://aws.amazon.com/ko/bedrock/agents/)
[^12]: [Devin](https://www.cognition.ai/blog/introducing-devin)
[^13]: [MultiOn](https://www.multion.ai/)
[^14]: [DLAI Langgraph](https://learn.deeplearning.ai/courses/ai-agents-in-langgraph/)
[^15]: [Llama Index](https://docs.llamaindex.ai/en/stable/getting_started/concepts/)
[^16]: [Arize Pheonix](https://github.com/Arize-ai/phoenix)
