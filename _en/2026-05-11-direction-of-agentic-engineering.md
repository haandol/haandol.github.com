---
layout: post
title: "Agentic Engineering and Transitional Technologies"
excerpt: HITL removal is the direction, and coexistence-oriented tools are transitional
author: haandol
email: ldg55d@gmail.com
tags: ai agent harness-engineering agentic-development claude-code headless
publish: true
lang: en
date: 2026-05-11 00:00:00 +0900
last_modified_at: 2026-09-10 10:44:38 +0900
translation_key: direction-of-agentic-engineering
korean_url: /2026/05/11/direction-of-agentic-engineering.html
permalink: /en/2026/05/11/direction-of-agentic-engineering.html
---

## TL;DR

- I expect agentic engineering to move toward removing recurring human intervention.
- Designs that make human review mandatory are likely to change over the long term.

## Introduction

I do not think software development is an end in itself. It is closer to a **byproduct** of making business requirements executable by computers. To put it more bluntly, development is **a compiler that translates business requirements into code**.

Until now, this compilation process has required many specialists: product managers, designers, frontend developers, backend developers, QA engineers, and more. But as agents begin automating this intermediate process, the middle layer is rapidly becoming thinner.

Today, I want to organize my recent thoughts on the direction of this trend and where today's tools stand along that path.

## 1. The final goal is removing humans from the loop

I have already covered the development process in earlier posts,[^1][^2] so I will move on. If I had to summarize the direction of what we call **agentic engineering** in one sentence, it would be this:

I think the long-term goal is **removing the human in the loop: the person who repeatedly intervenes during execution**.

That means reducing the reasons people must implement and check every step of turning business requirements into code. Whether they can be removed entirely is a separate question, but I expect the companies involved to keep investing in attempts to move in this direction.

## 2. Why people remain—and why those reasons are finite

In practice, people still remain throughout the pipeline. The most immediate bottleneck today is **review**. Because current agent output is not considered to fully reflect business and technical requirements, the pipeline still assumes that a person must inspect it one more time at the end. Generation speed has already surpassed human review capacity, and complaints that "code produced with a click is hard to review" come from this assumption.

But this problem will not disappear automatically as models improve. We are moving toward a structure in which the system that generates the code also owns verification, but that structure still needs a harness that moves repeated review judgments into contracts, tests, and guardrails, escalating only new contracts, contradictions, and high-risk exceptions to people.[^3]

Model progress expands the range that an agent can close on its own, but reducing the actual bottleneck remains an engineering problem in its own right.

The bottleneck after review is **deployment**. A human still has to participate in the handoff from something built locally to something running in production. Packaging the code, building an image, configuring environment variables and permissions, and deciding whether to roll back after a failure all fall into this category.

This point also reaches backward into the development stage. **If even one point of human intervention remains at the end of the pipeline, the stages before it are ultimately designed around that person.** If someone must inspect the code and make a judgment during deployment, the development stage must preserve code in a form that "a person can understand and review." Human dependence in deployment ends up setting the limit on automation in development.

Both bottlenecks are real today, but they are **finite bottlenecks** in the sense that their scope can shrink as models, harnesses, and deployment and operations automation improve. What matters is which tools can ride the trend when these bottlenecks begin to disappear.

## 3. Designs that assume coexistence and designs that assume human removal

I think today's agentic development tools are splitting around two broad design assumptions: those **designed for coexistence with people** and those **designed for removing people**.

The way I became accustomed to using Cursor inside an IDE was to proceed while checking the agent's changes myself. That is useful for current work, but **as long as every change requires human review, throughput can remain tied to review speed**.

This does not mean that a particular product cannot change in the future. Here, I want to distinguish designs by where they require human review rather than by product name.

On the opposite axis are headless coding-agent configurations and approaches such as Anthropic's Managed Agents. These begin by removing the person. Their default mode assumes that the agent runs its own loop, verifies its own work, and deploys on its own. The immediate experience may be rougher than with coexistence-oriented tools, but their ceiling rises along with advances in LLMs and agents.

Even if models improve, review queues remain if people must still check every change. To use the wider scope of work models can handle, we need to move repeatable judgments into tests and the harness.

## 4. Coexistence-oriented technologies are transitional

From this perspective, I consider designs that require repeated human review **transitional**.

Because review and deployment remain bottlenecks today, coexistence-oriented tools are currently the most practical choice. But once those bottlenecks disappear one by one, the reason for those tools to exist also begins to shrink. Coexistence itself was valuable because of the assumption that "a person must intervene," and that assumption is the first thing beginning to shake.

When evaluating tools, I therefore want to consider both their current maturity and how much repeated human review they can remove as models take on more work.

## Conclusion

We can choose today's tools based on how well they work for the task at hand. But I want to consider the direction of long-term investment separately.

I intend to spend more time on tools and designs that move recurring decisions on normal execution paths from people into the harness. Whether they actually reduce the remaining review and deployment bottlenecks will be the test of that choice.

---

[^1]: [Demystifying Harness Engineering](/en/2026/03/15/harness-engineering-beyond-context-engineering.html).

[^2]: [Multi-Agent Without a Harness Is Just Context Engineering](/en/2026/03/31/multi-agent-without-harness-is-just-context-engineering.html).

[^3]: [AI Made the Code Faster, So Why Is Review Harder?](/en/2026/08/18/ai-coding-review-cognitive-load.html) — moving repeated review judgments into contracts and guardrails so that people decide only new contracts and exceptions.
