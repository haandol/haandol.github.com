---
layout: post
title: "Why AI Adoption Should Not Start with Token Savings — The 3S Stages 1/2"
excerpt: Match AI investment to each adoption stage
author: haandol
email: ldg55d@gmail.com
tags: ai agent agentic-development harness-engineering organization token-economics
publish: true
lang: en
date: 2026-06-15 00:00:00 +0900
translation_key: organizational-ai-adoption-3s
korean_url: /2026/06/15/organizational-ai-adoption-3s.html
permalink: /en/2026/06/15/organizational-ai-adoption-3s.html
---

## TL;DR

- Early token savings can prevent investment in the harness.
- 3S separates the stages of connection, learning, and reuse.
- Investment and evaluation criteria should change by stage.

## Introduction

Two demands often appear together when organizations discuss AI adoption.

Employees are told to use AI more. At the same time, they are told to reduce token use and tool costs quickly.

Both demands are necessary. The problem is their order.

During the early work of connecting AI to a workflow, teams need to observe many failures, build evaluation cases and tools, and move repeated human decisions into rules. This process consumes not only tokens but also domain-expert time and engineering capacity.

If reducing usage becomes the goal from the beginning, people are likely to finish the immediate task with fewer tokens instead of building the harness. That is rational for the individual, but the same failure returns in the next task.

If experimentation grows without limits, however, review, rework, and maintenance costs also grow.

Rather than searching for one budget principle between these extremes, I think it is better to first identify **which stage the current workload is in**.

I divide those stages into `Streamlining`, `Shape`, and `Scale`. [Part 2](/en/2026/08/18/measuring-ai-adoption-ahead-lever-part-2.html) continues with how to evaluate each stage using AHEAD and LEVER.

## 1. Tokens are only part of the total cost

Token prices are immediately visible.

But turning a business requirement into something that reaches customers also requires tool execution, retries, human review, CI, deployment, and incident response.

When AI produces code faster, the review queue can grow longer. If cognitive load removed from implementation moves into review, token cost may look low while total delivery cost remains unchanged.[^1]

That is why token use is dangerous as a standalone goal.

The question should be whether the total input required to deliver a feature of the same quality to customers has fallen. This is also why I argued in the [CTS-SW post](/en/2026/08/14/cts-sw-software-delivery-cost.html) that code volume needs to be replaced by a connection between customer-delivered software and total cost.[^2]

It is equally unrealistic to expect CTS-SW or short-term ROI to improve at the beginning of adoption.

Cost comes first while teams connect data and tools and move failures into evaluations and guardrails. Until that investment is reused by later workloads, it can look inefficient when judged by the numbers alone.

## 2. Teams need room to build the harness

A harness is broader than giving an agent a long prompt.

It is closer to an environment that combines the data and tools required for a workflow, quality criteria, tests, permissions, observability, and exception handling so the agent does not repeat the same failure.[^3]

A harness is not completed in one pass.

When the agent fails, examine the cause and add an evaluation case. When the same review comment repeats, move it into a test or architecture rule. When a human makes the same exception decision every time, clarify the contract and escalation conditions.

The result of spending tokens in this process must remain available to the next execution.

Using many tokens merely to finish the current task is different from using them to reproduce a failure and update the harness. The latter can reduce review and rework in future tasks.

The following figure is a conceptual illustration of that relationship, not a measured result.

![Conceptual curve in which team productivity rises after available tokens pass a minimum threshold, then falls again under excessive allocation](/assets/img/2026/0615/token-governance-productivity-curve-en.svg)

On the left, the team lacks enough room to begin exploration and validation. On the right, experiments unrelated to business goals and maintainable outputs both increase.

The appropriate point depends on the risk and complexity of the workflow and the current maturity of its harness. Even so, I think it is clear that early investment and operational optimization should not be evaluated by the same standard.

## 3. Divide adoption into the 3S stages

Kent Beck's 3X model divides product development into Explore, Expand, and Extract and argues that each stage requires a different strategy.[^4]

Applying that idea to AI adoption, I divided the process into three stages: `Streamlining`, `Shape`, and `Scale`.

3S is not a validated standard model. It is a lens I propose for changing investment and evaluation questions according to the state of a workload.

{% raw %}
```mermaid
flowchart LR
    S1["Streamlining<br/>Connect workflow boundaries and tools"] --> S2["Shape<br/>Move failures into the harness"]
    S2 --> S3["Scale<br/>Reuse a validated harness"]
    S3 -. "New workflow · new contract" .-> S1
```
{% endraw %}

During Streamlining, build an environment in which the agent can complete the workflow end to end.

During Shape, feed real failures and review feedback back into the harness.

During Scale, reuse the validated harness for other requirements to reduce total delivery cost and time.

These stages are not one maturity rating for the entire organization.

Within one team, order-cancellation automation may be in Scale while a newly started settlement workflow is in Streamlining. An existing workload also returns to an earlier stage when its data contract or risk criteria change.

## 4. Streamlining — connect the workflow so it can finish end to end

Streamlining starts with the workflow, not the model.

Suppose we want to automate order cancellations.

The cancellation request may live in the order system, the payment reversal may go through the payments team's API, and the refund policy may live in a customer-support tool. If every team simply wraps its system in MCP, the agent receives several API fragments but may not know the order or permissions required to combine them.

First, lay out the data, rules, permissions, and responsibilities required for the order-cancellation workflow.

Event Storming can help identify the real workflow and its bounded contexts.[^5] Instead of assuming that the organization chart matches domain boundaries, it reveals what must be read and changed together.

Then connect the required reads and mutations through explicit contracts.

There is no need to merge all data into one place. The agent only needs to check the order state, decide whether cancellation is allowed, and issue the refund within its authorized scope. Least privilege, audit records, and the conditions for handing work to a human should also be defined here.

The questions in this stage are closer to readiness than performance.

- Are the workflow's start and completion conditions clear?
- Can the agent access the required data and tools?
- Are permission and responsibility boundaries connected?
- Is there a baseline for the current manual workflow's time, quality, and cost?

Without these conditions, failures observed during Shape are difficult to classify as model problems or environment problems.

## 5. Shape — move recurring decisions into the harness

During Shape, give the connected workflow to the agent and observe its failures.

Instead of aiming for high autonomy from the beginning, find which decisions repeat and where humans return to reading the code.

If reviewers repeatedly point out the same import direction, move it into an architecture test. If the same requirement must be confirmed every time, turn it into a contract and test case. If missing evidence forces a human to read the entire codebase, require the next execution to leave verification results for each contract.[^1]

In my view, the output of Shape is not an automation rate.

It is a harness that detects the same failure faster when it returns or prevents it entirely. This stage also separates decisions that can be repeated from high-risk exceptions instead of trying to eliminate every human judgment.

Domain experts and harness engineers need to work together during this stage.

Domain experts define what a correct result is and which exceptions are dangerous. Harness engineers move that knowledge into evaluation cases, tools, contracts, and guardrails. Policies that require security or legal judgment remain owned by those organizations.

Harness engineers do not need to remain permanently embedded in every domain.

Early on, they can establish the shared foundation and feedback loop. Once the domain team can classify failures and repair the harness directly, it is better for the harness engineer to move to the next workload. For the harness to become an organizational capability, the domain team must take over operational ownership.

## 6. Scale — reuse the earlier investment for the next requirement

During Scale, a team does not rebuild the environment and evaluation criteria from scratch for every new requirement.

It reuses validated data contracts, connectors, tests, guardrails, and observability. The agent should close normal paths independently and escalate only new contracts or risks that have not been verified.

At this point, the earlier investment can be examined as a reduction in total delivery cost.

Look not only at code generation time but also at the time required for a requirement to reach customers, human review and waiting, deployment, and operating cost. In this stage, a metric such as CTS-SW can help track the trend within the same team.[^2]

Scale does not mean cost reduction alone.

It may allow the same number of people to handle more customer requests, reduce incident risk, or automate small workflows that were previously uneconomical. The workload's definition of value should be chosen when the work begins.

I also do not think decisions to replace a model or agent should be made in this stage without evaluation.

I could not move for a while because a harness I had built around Cursor did not work unchanged in Claude Code. When the model and tools change, context usage and failure patterns can change as well.

Separating contracts and evaluation cases that should remain common assets from tools tailored to a particular agent makes it possible to compare the system before and after replacement using the same standard.

## Conclusion

Token use may increase during the early stages of AI adoption.

Connecting data and tools, reproducing failures, and moving repeated human decisions into the harness all create costs before savings appear.

That does not mean early investment should be unlimited.

During Streamlining, establish the workflow and baseline. During Shape, verify that failures remain in the harness. For workloads in Scale, examine total delivery cost and business outcomes.

3S is less a model for assigning an organizational maturity score than **a lens for distinguishing what to invest in and what not to ask of the current workload**.

The next post, [part 2](/en/2026/08/18/measuring-ai-adoption-ahead-lever-part-2.html), explains how I use AHEAD to examine harness learning and review burden during Shape, and LEVER to examine total delivery cost and value capture during Scale.

---

[^1]: [Why Does AI-Generated Code Make Review Harder?](/en/2026/08/18/ai-coding-review-cognitive-load.html) — examines how cognitive load removed from implementation can move into review and how contract-based review can narrow that burden.

[^2]: [Did AI Coding Tools Actually Cut Development Cost?](/en/2026/08/14/cts-sw-software-delivery-cost.html) — explains CTS-SW as a connection between customer-delivered software and total delivery cost rather than generated code volume.

[^3]: [Demystifying Harness Engineering](/en/2026/03/15/harness-engineering-beyond-context-engineering.html) — explains the scope of a harness that combines context, tools, evaluations, and guardrails.

[^4]: Kent Beck, [The Product Development Triathlon](https://medium.com/@kentbeck_7670/the-product-development-triathlon-6464e2763c46) — the 3X model of Explore, Expand, and Extract.

[^5]: [Demystifying Event Storming](/2020/12/10/demystifying-event-storming.html) (Korean) — explains how to identify domain events and boundaries from the real workflow.
