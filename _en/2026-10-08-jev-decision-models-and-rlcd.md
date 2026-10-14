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
last_modified_at: 2026-10-14 10:38:54 +0900
lang: en
translation_key: jev-decision-models-and-rlcd
korean_url: /2026/10/08/jev-decision-models-and-rlcd.html
permalink: /en/2026/10/08/jev-decision-models-and-rlcd.html
---

## TL;DR

- I suspect RLCD contributes substantially to Jev's practical advantage.
- Preference training may still influence a model after its head is replaced.
- That influence and RLCD's contribution have yet to be tested in isolation.

## Introduction

After Jev came out, models and APIs such as Kev, Jeff, Strands Decider, and OpenAI Decisions offered quick ways to add classification and scoring to an application. Returning fixed choices and probabilities instead of long responses made them look useful for putting AI decisions into an early product.

Some projects published benchmarks suggesting a small gap from Jev. But Jev felt considerably better on the tasks I tried.

It is similar to cases where an open model beats a commercial model on a benchmark but starts failing when given something a little harder in practice.

**Despite similar benchmark scores, the alternatives I tried did not yet seem capable of replacing Jev.**

That gap made me interested in RLCD, Jev's approach to training decisions and their probabilities. TypeSafe, the company behind Jev, argues that responses people prefer and decisions software can act on need different training objectives. I agree, and **I suspect RLCD is what makes Jev different.**

If that is right, replacing an existing model's head, the component that produces its outputs, may not give it the same qualities. In particular, I think replacing only the head of a model trained to produce responses people prefer leaves it likely to fail on questions that require choosing against those preferences. This is still a hypothesis. I want to explain why I find it plausible.

## 1. A benchmark can change when you reverse the question

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

What catches my attention is behavior that seems to follow a familiar judgment even when the question changes its criterion.

This table cannot establish that human preference training caused the difference. Handling negation or the question wording in the training data could also explain it. OpenAI Decisions was stable under both wordings too, so this is not evidence that only Jev can handle such questions.

But it does reveal a problem: **the judgment a question calls for can differ from the one a model habitually produces.** That is why I want to compare RLCD with the objectives used to train existing models.

## 2. What RLCD aims to train differently

### 2.1. A preferred response and a correct answer

Reinforcement learning, or RL, trains a model to **take actions that earn more of a specified reward**. What the reward evaluates changes what the model learns to do well.

Reinforcement learning from human feedback, or RLHF, uses people's preferences between responses as a training signal. InstructGPT, a model trained to follow instructions, first learned from demonstrations written by people, then used their rankings of responses to train a reward model for reinforcement learning.[^2]

Human preference training helps produce conversations people want. But TypeSafe argues that rewarding preferred responses can also reinforce agreement with the user and confident-sounding errors.[^3]

In classification, the sentence someone would like to receive can differ from the one that satisfies the question. Suppose we ask which is ruder: “Sorry to keep you waiting” or “Can't you even wait that long?” The answer should be the latter. Preferring a polite response does not change the correct answer here.

### 2.2. A brief explanation of RLCD from the official documentation

TypeSafe calls its approach **Reinforcement Learning for Calibrated Decisions**, or RLCD. It trains decisions and calibrated probabilities. The goal is to provide judgments over predefined options and their probabilities for software to use directly, instead of generating free-form text.[^3][^4]

Suppose a model estimates whether a customer inquiry is a refund request. If we collect enough inquiries assigned roughly 80%, and roughly 80% really are refund requests, the probabilities in that range are well calibrated. This agreement is what calibration means.

An 80% prediction does not guarantee the answer for that individual inquiry. Returning the same probability for every inquiry to match the overall rate is not useful for classification either. The model needs to distinguish the requests as well as express uncertainty accurately.

Reliable probabilities let code route clear cases immediately and send ambiguous ones for more information or to a larger model. For choice and score questions, Jev's `confidence` field summarizes the probability distribution, so it needs to be read differently from an individual option's probability.[^5]

The public material explains this training objective. The official documentation and launch post I checked do not provide enough detail to reproduce Jev's training data or reward calculation. We therefore cannot equate RLCD with a particular loss function or a public training implementation.

Calibration alone does not guarantee that a model understands negation or follows the question's criterion. What interests me about RLCD is **its objective of learning decisions that answer the question together with their uncertainty**. I think that difference in objective has contributed to Jev's practical performance.

## 3. What replacing the head may leave behind

A head turns information computed inside a model into its final output. Replacing a next-token prediction head with one that scores options lets a model return choices and probabilities instead of long responses.

But if we freeze the base model and train only the head, the way the base reads and represents the input stays the same. A new head can use that information differently, but there is no guarantee that it removes every influence of the earlier training.

In the rude-sentence example, the failure I suspect is assigning a higher score to the more polite sentence the model was trained to prefer as a response, even though the question asks for the ruder one. **If RLCD accounts for Jev's difference, I think models whose heads are replaced without sufficiently changing the influence of preference training are likely to fail on questions like this.**

This does not mean a model trained on human preferences cannot identify rude language. My hypothesis is that **preferences which survive a change in output format can conflict with the question's decision criterion**. How often that actually happens needs to be tested separately.

Applying this hypothesis to products requires distinguishing their starting models and additional training. Their public implementations do not support treating Kev, Jeff, and Strands Decider as chat models with only their heads replaced.

| Project | Differences described in the public documentation |
| --- | --- |
| Kev | The 0.8B, 4B, and 9B models start from pretrained Qwen base models and train adapters, small sets of added weights, along with the head. The 27B model fine-tunes all weights of a post-trained model.[^6] |
| Jeff (`firelex/jeff`) | Fine-tunes all weights of its base models and calibrates probabilities after training.[^7] |
| Strands Decider | Replaces a pretrained Qwen base model's output head and also applies LoRA, which trains small sets of added weights within the base model.[^8] |

In particular, these documents do not support assuming that the smaller Kev models and Strands Decider start from chat models trained on human preferences. There is therefore no basis here for attributing their errors in the earlier benchmark to human preference training. These implementation descriptions reflect documentation checked on October 14, 2026.

## 4. What still needs to be tested

The TypeSafe material I checked did not include an ablation isolating RLCD's contribution: an experiment that changes or removes one component for comparison. TypeSafe introduced a new architecture, parallel output mechanism, and RLCD together, so differences between products cannot be attributed to RLCD alone.[^4]

Testing my hypothesis would require the same starting model, data, and evaluation cases, while varying whether preference training is applied and how decision training follows it. To test RLCD's contribution, we would also need to keep the set of trainable weights the same. That would distinguish gains from updating the base model from gains due to changing the training objective.

The evaluation should pair questions that reverse the criterion, such as choosing the more polite sentence and choosing the ruder one, and measure correct choices separately from probability calibration. If training only the head handles both criteria well, my hypothesis becomes weaker. If errors increase when the criterion conflicts with learned preferences, and applying RLCD under the same conditions reduces those errors, that would support it. The currently public material is not enough to complete this comparison.

## Closing thoughts

I think RLCD contributes substantially to Jev's practical advantage. That leads me to the hypothesis that **replacing only the head of a model still influenced by human preference training leaves it likely to fail when a question requires choosing against those preferences**.

I have not isolated and tested that cause yet. What I want to know about a Jev replacement is whether, beyond similar scores on familiar questions, **it still follows the question when the decision criterion changes**.

---

[^1]: Arize, [Decision model benchmark](https://arize.com/blog/decision-model-benchmark/). The table cites four models from its published question-reversal experiment. I did not rerun the experiment for this article.
[^2]: Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155). Describes InstructGPT's training on demonstrations and reinforcement learning using human preferences.
[^3]: TypeSafe, [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer). Explains its concerns about RLHF, RLCD's objective, and probability calibration. Checked October 14, 2026.
[^4]: TypeSafe, [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev). Introduces the architecture, parallel output mechanism, and RLCD together. Checked October 14, 2026.
[^5]: TypeSafe, [Confidence](https://docs.typesafe.ai/confidence). Distinguishes option probabilities from confidence calculated from the distribution.
[^6]: [jaredpalmer/kev](https://github.com/jaredpalmer/kev), Models and training description.
[^7]: [firelex/jeff](https://github.com/firelex/jeff), Train your own. This is the Jeff project discussed here.
[^8]: Strands Decider, [Architecture](https://github.com/strands-labs/strands-decider/blob/main/docs/architecture.md).
