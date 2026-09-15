---
layout: post
title: "Why AI Code Review Feels Harder — Context Familiarity and Cognitive Debt"
excerpt: Why compressed understanding makes review the bottleneck
author: haandol
email: ldg55d@gmail.com
tags: ai agent cognitive-load cognitive-debt code-review developer-experience backpressure
publish: true
lang: en
date: 2026-08-18 09:00:00 +0900
last_modified_at: 2026-09-15 23:00:13 +0900
translation_key: ai-coding-review-cognitive-load
korean_url: /2026/08/18/ai-coding-review-cognitive-load.html
permalink: /en/2026/08/18/ai-coding-review-cognitive-load.html
---

## TL;DR

- Time to become familiar with context is compressed into review.
- Accepting code because it works can leave debt the team cannot see.
- Reduce human review effort or automate recurring checks.

## Introduction

While talking with a customer about AI coding, I heard that reviewing agent-generated code creates overwhelming cognitive load: the mental effort of holding information needed to understand and judge the work.

I had rarely felt that way myself. I suspect that is because I started using AI coding tools with the beta version of GitHub Copilot and became accustomed to small tasks, small commits, and short feedback loops.

Those models failed at large tasks. I split problems, read and corrected the results, and gradually became familiar with the code and its constraints. My understanding of where to trust the models grew alongside their capabilities.

Today, a model can produce a large amount of code at once. But **time to become familiar with its context does not automatically shrink in proportion to coding time**. When understanding no longer develops alongside implementation, the burden collects when the result arrives.

I think this pressure can lead people to accept unfamiliar code because it works, leaving debt they do not recognize. Breaking that path requires reducing the burden of reviewing code, architecture, and documents, or removing people from repetitive reviews.

## 1. Time to build familiarity is compressed

Writing code involved reading its surroundings, translating requirements into implementation, and fixing failed tests. Along the way, a developer learned why the structure was needed and which conditions could break it.

Coding time was also time spent becoming familiar with context. Even incomplete understanding left a working model for the next decision.

Delegating implementation presents the finished result first. The human must trace code and tests backward to reconstruct intent, assumptions, and exceptions. Work previously spread across implementation now competes for a short review window.

DORA describes the movement of time from generation to verification and makes the distinction explicit.[^14]

> “Verification is a fundamentally different cognitive task than creation.”
>
> — DORA

![Conceptual diagram showing effort distributed across traditional implementation but concentrated around intent and review in AI development](/assets/img/2026/0818/cognitive-load-shift-en.svg)

This diagram illustrates where effort occurs. Producing the same amount of code faster does not make the entire task proportionally faster if the human must build familiarity separately.

Keeping the same deadlines while taking on more simultaneous changes can force people to switch repeatedly between unfamiliar contexts. Individuals experience cognitive load; teams accumulate review waits and rework.

In this post, **review backpressure** means progress being constrained because human understanding and verification cannot absorb upstream output. Increasing generation while familiarity-building time is compressed can intensify that pressure.

## 2. Debt chosen knowingly and debt left unrecognized

Technical-debt discussions often bring to mind a trade-off among release timing, performance, and maintenance cost. A team might knowingly defer removing duplicate implementation to ship sooner.

When describing deliberate technical debt, Fowler makes this awareness explicit.[^26]

> “the team knows they are taking on a debt”
>
> — Martin Fowler

Knowing what was deferred and what it may cost makes repayment a decision the team can discuss. Technical debt can also be unintentional. The comparison here is between a recognized compromise and a gap in understanding that passes through review unnoticed.

Cognitive debt is inadequate shared understanding of the system's contracts and behavior for reasoning about change. I am focusing on situations where a team accepts code without adequately recognizing that gap.

Consider a hypothetical duplicate-payment prevention feature. Payments work through the interface and retry tests pass, but nobody explored retries after record loss or two requests arriving simultaneously.

Knowing the contract—one request must not cause two charges—is different from understanding the conditions under which the implementation satisfies it. Accepting the result simply because it works can leave the team unaware of what it missed.

Deferring understanding under deadline and approval pressure can be a conscious choice. That does not mean the team recognizes the size or consequences of the gap it leaves. Storey distinguishes those two things.[^10]

> “Even when surrender is intentional, the resulting debt accumulates invisibly.”
>
> — Margaret-Anne Storey

Later, someone shortens payment-record retention to reduce storage cost. A reviewer who does not understand the relationship with retries may accept a faulty change. Cognitive debt can impair later judgment, creating technical debt or delaying discovery of an existing problem.

{% raw %}
```mermaid
%%{init: {"flowchart": {"nodeSpacing": 20, "rankSpacing": 30}}}%%
flowchart TD
    A["Less time for familiarity<br/>More review demand"] --> B["Individual and<br/>team pressure"]
    B --> C["Defer exploring<br/>contracts, behavior,<br/>and edge cases<br/>Accept working results"]
    C --> D["Cognitive debt<br/>Unrecognized gaps"]
    D --> E["Faulty later decisions<br/>Technical debt may grow"]
    B -. "Response" .-> F["Lower understanding cost<br/>Automate recurring<br/>judgment"]
    F --> G["Necessary understanding<br/>and verification completed"]
```
{% endraw %}

This is the path I want to explain, not a law applying to all AI development. Cognitive debt does not disappear and become technical debt. Inadequate understanding and the faulty code it enables can remain together.

## 3. Team velocity is constrained by the slower verification stage

Once generation is sufficiently fast, the next constraint to examine is verification capacity. Microsoft's guidance on system bottlenecks states this principle for sustainable throughput.[^27]

> “a system can only process as fast as its slowest performing component.”
>
> — Microsoft

Apply that principle to review. Assume generation and delivery impose no other bottleneck and enough changes arrive to use review capacity. Every change passes automated checks, and only changes requiring human judgment proceed to human review. The two stages can process different changes concurrently. Keep work units and quality criteria consistent.

{% raw %}
```mermaid
flowchart TD
    A["Automated checks<br/>Every change"] --> Q{"Human judgment needed?"}
    Q -->|Yes| H["Human review<br/>Relevant code, design, and docs"]
    Q -->|No| D["Delivery"]
    H --> D
```
{% endraw %}

Express both stages' capacities in terms of total changes, and review-limited team velocity can be approximated as follows. This is a bottleneck model for choosing improvements, not a formula obtained by measuring actual teams.

```text
team velocity ≈ min(human review velocity, automated review velocity)
```

Velocity here counts changes meeting the same quality criteria, not approvals alone. Rework and waiting can lower actual throughput. If generation or delivery is slower, that stage must also be included in the bottleneck analysis.

Human capacity can be broken down further:

```text
H = human review time available per day
C = average review time per change requiring human review
p = fraction of all changes requiring human review

human review velocity = H / (p × C)
```

This is the total change volume supported by human capacity, not the number of reviews people personally perform.

C includes reading code, reconstructing context, checking assumptions in architecture and documentation, and exploring exceptions. **This human-time cost is how I interpret cognitive load acting inversely to team velocity here.** It is not the reciprocal of a psychological load score.

For a hypothetical example, 240 available review minutes per day and 30 minutes per change give human capacity of eight changes per day. Reducing familiarity-building cost enough to review at the same quality in 15 minutes raises it to sixteen. But if automated checks can process only twelve changes per day, the team cannot sustainably exceed twelve.

Holding staffing and available time constant leaves C and p as the human-side levers: reduce the cost of understanding and judgment, or reduce the fraction needing direct human review. For a route with no human review, remove that stage from the capacity model rather than divide by zero.

## 4. Lower the cost of becoming familiar with context

The first direction is to make necessary human reviews less burdensome. C grows when people must reconstruct purpose and assumptions from scratch for every code, architecture, or requirements-document review.

I would establish the contract before implementation and connect the result to before-and-after behavior, failure conditions, and verification evidence. A contract is the basis for judging acceptance: observable behavior, conditions that must hold, and permission or data boundaries.

For the payment example, a passing-tests summary is less useful than knowing which retries were checked, how record loss and concurrent requests were covered, and which decisions remain open. Explanations should lead directly to code and executed tests to reduce the cost of recovering context.

The amount to learn at once can also shrink. Implement one requirement slice, understand and verify it, then commit. Generating several small pull requests—requests to review and merge changes—and reading them all later pushes familiarity-building time to the end again.

![Conceptual diagram distributing understanding and verification across smaller development cycles](/assets/img/2026/0818/small-cycle-cognitive-load-en.svg)

The diagram represents restoring understanding work between implementation steps, rather than doing less work. Familiarity with the current small change becomes the starting point for the next one.

Existing cognitive debt still needs repayment. Tracing code and design together, finding missed assumptions and failure conditions, and repairing faulty implementation take time. The goal is to avoid repeating the same reconstruction and overload on later tasks, not to eliminate that necessary concentration.

In the [ALPS Writer Plugins](https://github.com/haandol/alps-writer-plugins) I maintain, I have built in criteria for dividing work and reviewing evidence against contracts. Lasting decisions go into Architecture Decision Records (ADRs), and implementation explanations connect request and failure paths to code and tests.[^3]

The presence of documentation does not establish understanding. Maintainers need to be able to explain behavior relevant to future changes and incident response. Small implementation units and readable evidence support that understanding.[^7]

## 5. Remove people from repetitive reviews

The second direction is to stop requiring the same human review for every change. If people repeatedly reread conditions automated checks can verify, p remains high.

Repeated comments on module dependency direction should become architecture tests. Repeated checks for duplicate requests should become regression tests. Accumulating such decisions in the harness—the working instructions, tools, and verification environment—makes them reusable.[^5]

In the normal path I want, sufficient automated verification of an agreed contract removes the need for repetitive human approval. People decide new product behavior, contract changes, high-risk conditions, and assumptions automation could not verify.

An agent's claim that everything is fine is not enough to remove human review. What was verified and the evidence must be inspectable. Otherwise the process merely passes unfamiliar code faster.

Automating verification is also separate from maintaining necessary understanding. People need not read every implementation detail, but the team still needs to set intent and quality criteria and take responsibility for later changes.

While this transition is incomplete, control new work entering the process. Reducing arrivals alone does not lower the understanding cost of one review. Use the available time to improve explanations, contracts, tests, and tools so later capacity can grow.

After automation, reassess the difficulty of remaining human reviews. Removing routine changes can lower p while increasing C for the harder decisions left behind. Check actual review time and quality; evaluate cost against customer-delivered units, as CTS-SW does.[^19]

## Conclusion

AI reduces coding time, but people may still need separate time to become familiar with the context. Accepting working results while ignoring that gap can leave cognitive debt whose missing pieces the team cannot see.

Demanding faster approvals under the same pressure will not easily break that path. **At the same quality, we need to reduce the effort required for human review or remove people from recurring checks.** I think that is the main work of improving team velocity after code generation becomes fast.

---

[^14]: Jessica Baolin and Nathen Harvey, [Balancing AI tensions](https://dora.dev/insights/balancing-ai-tensions/) (DORA, 2026). Describes effort moving from generation to verification.

[^26]: Martin Fowler, [Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html) (2009). The quotation describes deliberate technical debt; the same article also covers inadvertent debt.

[^10]: Margaret-Anne Storey, [From Technical Debt to Cognitive and Intent Debt](https://arxiv.org/pdf/2603.22106v3) (2026). Distinguishes intentional surrender from the visibility of the debt that results.

[^27]: Microsoft Learn, [How to Investigate Bottlenecks](https://learn.microsoft.com/en-us/biztalk/core/how-to-investigate-bottlenecks). The principle concerns sustainable computer-system throughput; its application to team review, including the formula and assumptions, is this post's model.

[^3]: [Why Separate PRDs, ADRs, and Code? — Reading One Abstraction Level at a Time](/en/2026/07/25/alps-adr-abstraction-boundaries.html).

[^7]: Geoffrey Litt, [Understanding is the new bottleneck](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck) — separates correctness verification from understanding needed for the next change.

[^5]: [How I Built the EncBird Harness Layer by Layer](/en/2026/06/16/harness-engineering-in-practice.html).

[^19]: [Did AI Coding Tools Actually Cut Development Cost? — Understanding CTS-SW](/en/2026/08/14/cts-sw-software-delivery-cost.html).
