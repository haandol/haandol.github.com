---
layout: post
title: Robotics + AI 트렌드 대충 정리
excerpt: Breif summary of AI application in Robotics
author: vincent
email: ldg55d@gmail.com
tags: ai agent robotics foundation-model
publish: true
---

## TL;DR

- Pre-trained Foundation Model for Robotics
- Leverage Foundation Model for Robotics

## 시작하며

몇달전 알게된 Rabbit R1 과 MultiOn 이 후 개인적인 관심사는 AI Agent 이다.

Figure1 을 보고 나서 찾아보니 Agent 가 가장 진지하게 연구되는 분야가 로보틱스 인 것 같다.

나는 로보틱스 관련된 지식과 로보틱스 분야에서 AI 가 어떻게 진행되고 있는지 지식이 전무한 상태인데, 며칠간 공부를 하면서 감을 잡아보고 있다.

나처럼 아예 로보틱스에 대한 지식이 없는 사람들이 AI 가 어떻게 로보틱스 쪽을 혁신하고 있는지 알아두면 좋은 내용일 것 같아서 두서없지만 정리해본다.

## Trend

CS 에서 새로운 기술은 기존의 한계를 극복하기 위해서 나오는 경우가 많다.

따라서 CS 에서 새로운 분야에 들어갈 땐, 최신의 기술이 해결하고자 하는 바를 파악하고 거기서부터 역으로 돌아가는 것이 가장 효율적이라고 생각한다.

따라서 로보틱스와 AI 에 대한 최신의 트렌드를 먼저 파악하면 좋겠다고 생각했다.

이런 관점에서 전체적인 그림을 그리기 가장 좋은 영상은 Jim Fan 의 TED 영상[^1] 이다.

Skill 과 Embodiment 를 축으로 로보틱스와 AI (특히 Agent) 의 발전방향에 대해서 설명해주는데, 가장 간결하고 명확하게 설명해주는 자료라고 생각한다.

Skill 은 새로운 툴을 에이전트가 스스로 만들어낼 수 있는 능력이고, Embodiment 는 새로운 몸을 에이전트가 적응할 수 있는 능력이다.

Voyager 라는 실험을 통해 Skill 생성을, Eureka 라는 실험을 통해 Embodiment 적응에 대한 실험을 했었고, 결과가 꽤 성공적이었다.

앞으로 나가는 방향은 이 둘을 모두 아우르는 Generalist Robotics Agent 을 만드는 것이 목표라고 한다.

Jim Fan 은 위의 내용에서 조금 더 진행된 내용을 이번 GTC 에서 발표[^2]했는데, 해당 내용을 같이 보면 좋을 것 같다.

시간이 좀 흘렀지만, 전체적인 방향성이 기존과 같다는 점과 이번에 발표한 GR00T 를 보면, 올바른 방향으로 가고 있다고 판단하는 것 같다.

이런 방향을 전체적으로 가장 잘 정리한 논문이 이 논문[^9] 인 것 같다.

최근 딥마인드에서 발표한 SIMA[^4] 도 분야가 다르지만 비슷한 느낌인데, 결국 다양한 Skill 과 Embodiment 에 대해 적응가능한 Agent 를 만들어내는 방향으로 진행하고 있는 것 같다.

### Other trajectories

다만, 위의 내용인, Generalist Robotics Agent, 가 현재 가장 유망해보이는 보이는 방향은 맞지만 유일한 방향은 아닌 것 같다.

스탠포드의 강의[^5]를 보면 학계는 에이전트보다는 모델을 중심으로 연구가 진행되고 있는 것 같다. 하지만 Code as Policies, L2R 같은 방식들이 나오면서 에이전트에 대한 관심이 다시 높아지고 있는 것 같다.

딥마인드 강의에서[^6] 딥마인드는 정말 다양한 분야(?)에 대한 실험을 해오고 있었는데, 최근 RT-X 데이터셋[^7] 을 봤을 땐 딥마인드도 Foundation Model for Robotics 를 만들려고 하는 것 같다. (다만 자사 제품인 everydayrobots 를 메인으로 실험하고 있어서 embodiment 적응에 대한 실험은 어느정도 인지 알 수 없다.)

또 이와 별개로, Mobile ALOHA, DROID 와 같이 Imitation Learning + RL (Reinforcement Learning) 을 이용한 연구도 활발히 진행되고 있다.

## Foundation Model

결국 Generalist Robotics Agent 를 만드는 것이 최신 트렌드라고 할 수 있을 것 같다.

그리고 이 Generalist Robotics Agent 를 만들기 위해서는 Foundation Model 이 필요하며 Foundation Model 을 활용하는 방법은 크게 아래의 2개로 나눠 볼 수 있다.

- Pre-trained Foundation Model for Robotics
- Leverage Foundation Model for Robotics

그리고 위의 방식들은 공통적으로 강화학습과 Self-reflextive code generation (Reflexion, LATS 같은) 어떤 식으로든 이용하고 있는 것 같다.

### Pre-trained Foundation Model for Robotics

이 방식은 로보틱스를 위해 FM 을 학습하는 것이다.

대표적인 예가 구글의 RT-1, RT-2 모델이다. (RT = Robotic Transformer)

멀티모달 데이터와 인스트럭션(planning), 로봇의 액션(control) 데이터를 입력으로 받을 수 있는 트랜스포머 모델을 보유하고 있는 데이터로 직접 학습하여 해당 로봇에 대한 Foundation Model 을 만드는 것이다.

위의 모델은 현재 구글이 everydayrobots 라는 로봇의 액션만 학습하기 때문에 Embodiment 적응에 대한 실험은 따로 진행하고 있지 않다고 볼 수 있으며, Generalist Robotics Agent 가 아니라고 생각될 수 있다.

하지만 MS 의 연구[^8]를 보면, 2개의 서로 다른 도메인의 low-level 액션을 학습시킨 FM 모델은, 또 다른 도메인의 high-level instruction 으로 파인튜닝 하면 action 에 대한 적응이 빠르게 이루어진다는 것을 보여주고 있다.

따라서 RT-X 데이터셋으로 학습된 RT-1, RT-2 모델을 다른 도메인의 instruction 으로 파인튜닝하면, embodiment 적응이 가능한 Generalist Robotics Foundation Model 도 만들 수 있을 것으로 보인다.

가장 최근에 Covariant 가 발표한 RFM-1[^7] 도 이 방식에 속한다.

RFM-1 은 8B 파라미터를 가진 멀티모달(텍스트, 이미지, 비디오, 로봇동작 액션) Transformer 모델로, RT 시리즈와 모델 아키텍쳐 측면에서는 비슷한 아이디어지만 비해 훨씬 더 앞서있는 방식이다. RFM-1 모델은 SORA[^14] 와 같이 현재 씬에 대해서 액션의 수행결과를 예측하는 영상을 생성하고 해당 영상에 맞춰 액션을 취할 수 있다. (즉, Covariant 도 SORA 와 같이 intuitive physics 를 학습하여 영상을 생성하는 모델을 가지고 있고, 앞서 GTC 영상을 비춰볼 때 NVidia 도 해당 모델을 가지고 있거나 학습 중인 것 같다. Meta 도 V-JEPA 모델을 생각해볼 때 유사한 모델을 만들 수 있는 능력은 있을 것 같다.)

### Leverage Foundation Model for Robotics

Emergent abilities 라는 논문에서는 LLM 모델이 특정크기를 넘어서면 작은 모델은 하지 못했던 능력이 갑자기 생긴다는 것을 발견했다.

위의 모델들의 크기는 66M 부터 8B 정도로, 정말 작은 크기의 모델들이다. 해당 모델들은 일정작업은 잘 해내는 것으로 보이지만 좀 더 복잡한 작업들은 모델 크기를 emergent 가 나타날 때까지 키울 수 밖에 없을 것이고 이를 위해서는 더 많은 데이터를 확보해서 학습해야한다.

Claude, GPT-4 와 같이 1.5T 이상의 파라미터 크기를 가진 모델이 가진 emergent behavior 를 로보틱스에 활용하려면 현재로서는 파인튜닝 없이 모델을 그대로 이용할 수 밖에 없다.

Code as Policies[^10]], Learning to Reward[^11], SayCan[^12] 같은 실험들을 통해 거대한 모델을 활용하여 로봇의 행동 코드 또는 RL 에 사용되는 보상함수를 LLM 을 통해 만들어내는 것이 가능하다는(그리고 더 optimal 하다) 것을 보여주고 있다.

아직 여러가지 제약으로 메인스트림은 아닌 것 같지만, 충분히 연구해볼 만한 분야인 것 같다.

## 마치며

결국 Robotics Foundation Model 을 만들 거나, 혹은 NVidia 든 구글이든 현재의 ChatGPT 처럼 모델을 공개한다면 그것을 활용하기 위해서 어떤 준비를 해야하는지가 중요할 것 같다.

개인적으로는 앞으로 트랜스포머 모델을 원하는 대로 고쳐서 학습시킬 수 있는 능력이 필요할 것 같아서, 트랜스포머를 만들어보고 학습하는 것을 해보고 있는데[^13] 툴들이 좋아져서 생각보다 어렵지 않고 재미있는 것 같다.

---

[^1]: [The next grand challenge for AI](https://www.ted.com/talks/jim_fan_the_next_grand_challenge_for_ai)
[^2]: [GR00T and Isaac Robotics](https://www.youtube.com/watch?v=O3USP-na3PI)
[^3]: [Toward General-Purpose Robots via Foundation Models: A Survey and Meta-Analysis](https://arxiv.org/pdf/2312.08782.pdf)
[^4]: [SIMA](https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/)
[^5]: [Stanford Seminar - Robot Learning in the Era of Large Pretrained Models](https://www.youtube.com/watch?v=zggAEHm8dXc)
[^6]: [Stanford CS25: V2 I Robotics and Imitation Learning](https://www.youtube.com/watch?v=ct4tdyyNDY4)
[^7]: [RFM-1](https://covariant.ai/insights/introducing-rfm-1-giving-robots-human-like-reasoning-capabilities/)
[^8]: [An Interactive Agent Foundation Model](https://arxiv.org/pdf/2402.05929.pdf)
[^9]: [Toward General-Purpose Robots via Foundation Models: A Survey and Meta-Analysis](https://arxiv.org/pdf/2312.08782.pdf)
[^10]: [Code as Polices](https://code-as-policies.github.io/)
[^11]: [Learning to Rewards](https://language-to-reward.github.io/)
[^12]: [SayCan](https://say-can.github.io/)
[^13]: [Coding a Transformer from scratch on PyTorch, with full explanation, training and inference.](https://www.youtube.com/watch?v=ISNdQcPhsts)
[^14]: [Sora](https://openai.com/blog/sora-first-impressions)
