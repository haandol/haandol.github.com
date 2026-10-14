---
layout: post
title: "What makes Jev different? — Replacing the head and RLCD"
excerpt: Why RLCD may explain Jev's practical advantage
author: haandol
email: ldg55d@gmail.com
tags: ai jev decision-model reinforcement-learning rlcd evaluation
publish: true
published: true
date: 2026-10-08 11:23:38 +0900
last_modified_at: 2026-10-14 10:55:46 +0900
lang: en
translation_key: jev-decision-models-and-rlcd
korean_url: /2026/10/08/jev-decision-models-and-rlcd.html
permalink: /en/2026/10/08/jev-decision-models-and-rlcd.html
---

## TL;DR

- RLHF trains responses that people read and prefer.
- Replacing the head alone is unlikely to substitute for training toward task completion.
- I suspect RLCD contributes substantially to Jev's production performance.

## Introduction

After Jev came out, models and APIs such as Kev, Jeff, Strands Decider, and OpenAI Decisions offered quick ways to add classification and scoring to an application. Returning fixed choices and probabilities instead of long responses made them look useful for putting AI decisions into an early product.

Some projects published benchmarks suggesting a small gap from Jev. But Jev felt considerably better on the tasks I tried.

It is similar to cases where an open model beats a commercial model on a benchmark but starts failing when given something a little harder in practice.

**Despite similar benchmark scores, the alternatives I tried did not yet seem capable of replacing Jev.**

That gap made me interested in RLCD, Jev's approach to training decisions and their probabilities. TypeSafe, the company behind Jev, argues that responses people prefer and decisions software can act on need different training objectives. I agree, and **I suspect RLCD is what makes Jev different.**

The difference I have in mind is between **producing responses that are good for people to read and producing decisions that help software complete a task**. Replacing the head, the component that produces a model's outputs, does not by itself align the training objective with the latter.

That is why I think reinforcement learning that rewards the decisions needed for task completion is necessary. I would expect a model trained with RLCD to perform differently in production from an RLHF-trained model with only its head replaced.

TypeSafe, however, introduced a new architecture, parallel output mechanism, and RLCD together. I did not find a controlled comparison isolating RLCD's contribution in the public material. My hypothesis is that this difference in training objectives produces the practical gap I experienced with Jev.[^4]

## 1. Benchmark scores and actual task performance

Changing decision models can change how the same question is understood. Arize, which builds AI evaluation tools, published a comparison that illustrates this.[^1]

The experiment asks whether a response is supported by the supplied evidence. On the same 1,338 test cases, it asks both “Is every claim supported?” and “Does it contain an unsupported claim?” Reversing the question's polarity should reverse the expected answer.

| Model | Is every claim supported? | Does it contain an unsupported claim? |
| --- | --- | --- |
| Jev 1.13 | 0.93 | 0.93 |
| OpenAI Decisions | 0.90 | 0.89 |
| Kev 9B | 0.85 | 0.54 |
| Strands Decider 2B | 0.75 | 0.26 |

These values are ROC AUC, not accuracy. Here, the metric measures how well the model's scores distinguish supported responses from unsupported ones; closer to 1 is better, while 0.5 is random performance. The B in model names indicates billions of parameters.

Jev and OpenAI Decisions produced similar results under both wordings, while Kev and Strands Decider changed substantially.

If code uses this judgment to filter out unsupported responses, interpreting the question backward can let an incorrect response through. A model can return the required choice and probability while the task that uses those values still fails.

This table does not establish that RLHF caused the errors or that RLCD reduced them. It does illustrate why similar APIs and benchmark scores do not guarantee the same behavior in an actual task.

To test the effect of the training approach, we would need the same base model and task conditions, comparing head replacement alone with RL targeting the decisions the task needs. We would also need to distinguish the effects of training data and which weights are updated.

That evaluation should measure individual answer accuracy and the reliability of predicted probabilities, as well as whether software using those outputs actually completes the task. It needs to cover gathering necessary information, executing operations when their conditions are met, and stopping after completion.

## 2. What RLCD aims to train differently

### 2.1. Responses people read and decisions software uses

Reinforcement learning, or RL, trains a model to **take actions that earn more of a specified reward**. What the reward evaluates changes what the model learns to do well.

Reinforcement learning from human feedback, or RLHF, uses people's preferences between responses as a training signal. InstructGPT, a model trained to follow instructions, first learned from demonstrations written by people, then used their rankings of responses to train a reward model for reinforcement learning.[^2]

This training is useful for producing responses that people read and judge helpful. By good to read, I mean more than tone. I also mean explanations that are easy to understand, seem to address the request well, and help a person make a judgment and act.

When software uses that output to continue a task, the conditions for success change. It needs to decide which operation to execute, what to check when information is missing, and when the task is complete. If that decision is wrong, even correctly executed code can produce the wrong outcome.

TypeSafe likewise describes human-preferred responses and the reliability needed for unattended automation as different training objectives. The concern is that a person's preference after reading an output cannot stand in for an assessment of whether that output enables a task to be completed.[^3]

### 2.2. A brief explanation of RLCD from the official documentation

TypeSafe calls its approach **Reinforcement Learning for Calibrated Decisions**, or RLCD. It trains decisions and calibrated probabilities. The goal is to provide judgments over predefined options and their probabilities for software to use directly, instead of generating free-form text.[^3][^4]

Suppose a model estimates whether a customer inquiry is a refund request. If we collect enough inquiries assigned roughly 80%, and roughly 80% really are refund requests, the probabilities in that range are well calibrated. This agreement is what calibration means.

An 80% prediction does not guarantee the answer for that individual inquiry. Returning the same probability for every inquiry to match the overall rate is not useful for classification either. The model needs to distinguish the requests as well as express uncertainty accurately.

Reliable probabilities let code route clear cases immediately and send ambiguous ones for more information or to a larger model. For choice and score questions, Jev's `confidence` field summarizes the probability distribution, so it needs to be read differently from an individual option's probability.[^5]

The public material explains this training objective. The official documentation and launch post I checked do not provide enough detail to reproduce Jev's training data or reward calculation, including whether completion of an entire workflow is used directly as a reward. We therefore cannot equate RLCD with a particular loss function or a public training implementation.

What interests me about RLCD is **its objective of learning the decisions and uncertainty software needs to continue a task**. In the refund inquiry example, the software needs to decide which team should receive the inquiry and whether further checking is needed before processing can continue. I understand RLCD as an approach to training a model for decisions that support task completion.

## 3. Replacing the head and training for task completion

A head turns information computed inside a model into its final output. Replacing a next-token prediction head with one that scores options lets a model return choices and probabilities instead of long responses.

But if we freeze the base model and train only the head, the way the base reads and represents the input stays the same. A new head can use that information differently, but **whether the model has sufficiently learned the decisions needed to complete a task is a separate question**.

Suppose we connect the inquiry classifier to an automated refund workflow. After recognizing a refund request, the software still needs to choose between looking up the order, asking for more information, and issuing the refund. If it chooses to issue a refund before it has enough order information, the task proceeds incorrectly even when the output has the right format.

The model needs to learn which decision, given the current state, leads to the task being completed correctly. Having learned to earn rewards for responses people find convincing does not give me enough reason to expect that it has also learned these operational decisions and their uncertainty sufficiently well.

I think **replacing only the head without addressing this difference in training objectives will leave many production cases where the model's behavior does not match the task's requirements**. That is why I think RL rewarding decisions that help complete tasks is necessary, and why I suspect RLCD's training in that direction is what distinguishes Jev.

When comparing actual products, we also need to distinguish their additional training. The public implementations do not support treating Kev, Jeff, and Strands Decider as RLHF-trained models with only their heads replaced.

| Project | Differences described in the public documentation |
| --- | --- |
| Kev | The 0.8B, 4B, and 9B models start from pretrained Qwen base models and train adapters, small sets of added weights, along with the head. The 27B model fine-tunes all weights of a post-trained model.[^6] |
| Jeff (`firelex/jeff`) | Fine-tunes all weights of its base models and calibrates probabilities after training.[^7] |
| Strands Decider | Replaces a pretrained Qwen base model's output head and also applies LoRA, which trains small sets of added weights within the base model.[^8] |

These implementations differ in both their starting models and the scope of additional training. The earlier benchmark therefore cannot be read as a controlled comparison between simply replacing an RLHF-trained model's head and applying RLCD.

---

[^1]: Arize, [Decision model benchmark](https://arize.com/blog/decision-model-benchmark/). The table cites four models from its published question-reversal experiment. I did not rerun the experiment for this article.
[^2]: Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155). Describes InstructGPT's training on demonstrations and reinforcement learning using human preferences.
[^3]: TypeSafe, [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer). Explains its concerns about RLHF, RLCD's objective, and probability calibration.
[^4]: TypeSafe, [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev). Introduces the architecture, parallel output mechanism, and RLCD together.
[^5]: TypeSafe, [Confidence](https://docs.typesafe.ai/confidence). Distinguishes option probabilities from confidence calculated from the distribution.
[^6]: [jaredpalmer/kev](https://github.com/jaredpalmer/kev), Models and training description.
[^7]: [firelex/jeff](https://github.com/firelex/jeff), Train your own. This is the Jeff project discussed here.
[^8]: Strands Decider, [Architecture](https://github.com/strands-labs/strands-decider/blob/main/docs/architecture.md).
