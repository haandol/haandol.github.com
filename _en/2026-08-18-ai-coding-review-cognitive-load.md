---
layout: post
title: "AI Wrote the Code Faster—Why Is Review Harder? Reducing Shifted Cognitive Load"
excerpt: Close smaller cycles and review contracts before code
author: haandol
email: ldg55d@gmail.com
tags: ai agent cognitive-load developer-experience code-review hitl
publish: true
lang: en
date: 2026-08-18 09:00:00 +0900
translation_key: ai-coding-review-cognitive-load
korean_url: /2026/08/18/ai-coding-review-cognitive-load.html
permalink: /en/2026/08/18/ai-coding-review-cognitive-load.html
---

## TL;DR

- AI can move cognitive load from implementation into review.
- Keep the build-understand-commit cycle small.
- Use contracts and evidence to narrow what humans must inspect.

## Introduction

While talking with a customer about AI coding, I heard that reviewing agent-generated code creates overwhelming cognitive load.

Looking back at my own experience, I realized I had rarely felt that way.

I suspect that is because I started using AI coding tools with the beta version of GitHub Copilot.

The models were not reliable enough to handle large tasks. I had to split problems into small pieces, make small commits and pull requests, and keep the development feedback loop as short as possible.

As the models improved, I also learned gradually where I could and could not trust them.

People who begin AI coding today meet capable models from the start. They therefore seem more likely to ask for the largest result the model can produce in one pass.

The code arrives quickly, but changes that no human understands accumulate just as quickly.

I started to see this experience through the `Cognitive Load` dimension of Developer Experience described by Max Kanat-Alexander.[^1] A good Developer Experience reduces the amount of knowledge and the number of decisions required to complete a task.

The cognitive load removed by AI does not necessarily disappear. **It can move from implementation into review.**

For now, small changes and short feedback loops can divide that load. Over time, however, I think humans need to understand the contract between business requirements and code, while agents prove that they satisfied that contract, rather than requiring humans to understand every implementation detail.

## 1. Cognitive load during implementation has fallen

Paul Graham distinguishes between the Maker's Schedule and the Manager's Schedule.[^2]

A manager's day can be divided into one-hour blocks. A maker needs enough uninterrupted time to load a problem into their head, so half-day blocks often work better.

Traditional development fit this description well.

You read the surrounding code, understand the requirements and constraints, and build a mental model of the behavior. You keep that model active while writing and testing the code.

A meeting in the middle does not cost only one hour. You also lose the state that had not yet been transferred from your head into the code, then reread the code when you return.

An agent separates this process.

After a human provides the intent and constraints, the agent explores the code, implements the change, and runs tests. The human can do something else, and stepping away does not erase the files or task state the agent has already loaded.

At least during **implementation time**, context switching has become less expensive.

Makers gain a little room to work in manager-sized time blocks. Defining requirements and judging results still demand deep focus, but the human no longer needs to hold the same code in their head throughout implementation.

At first, I saw this as an uncomplicated improvement.

Once I started running multiple agents, however, I saw the cognitive load removed during implementation collect at the moment when their results had to be reviewed.

## 2. The missing understanding process collects in review

Traditional coding took time.

During that time, the developer repeatedly read both the new code and its surroundings. Implementation forced one decision after another, and each failed test updated the mental model along with the code.

By the time the work was complete, the developer generally knew why the structure looked this way and where the risks were. Code understanding was less a separate task than a byproduct accumulated during implementation.

AI development presents the completed result first.

The human starts with finished code and works backward to reconstruct what the agent read, which assumptions it made, and why it selected this implementation. There is no guarantee that a human can understand in a similar amount of time what an agent produced over tens of minutes.

Placed on a timeline, the change looks like this.

In traditional development, the burden of reading surrounding code, choosing among alternatives, and testing was distributed across implementation. In AI development, it rises while intent and constraints are defined, falls sharply while the agent codes, and rises again when the human must inspect the result and uncover hidden assumptions.

![Conceptual diagram showing cognitive load spread across implementation in traditional development but concentrated at the beginning and end of AI development](/assets/img/2026/0818/cognitive-load-shift-en.svg)

This is not a measurement of total cognitive load. It is a simplified model of where human effort may sit during the same task.

Rather than assuming AI automatically removes the total burden, I think it is more accurate to say that the understanding once accumulated during implementation is compressed into specification at the front and review at the back. If intent and constraints are weak at the start, the reviewer must reverse-engineer more agent decisions at the end, making the second peak even higher.

This is related to the familiar problem of large pull requests, but it is not exactly the same.

In a traditional large pull request, at least one author understood the change. With an agent, the gap between the entity that acted as author and the human who carries final responsibility exists from the beginning.

Running multiple agents in parallel does not reduce this gap. It only accumulates unread changes faster.

The current review model, in which a human checks every result, therefore protects quality while also limiting throughput. If every line must be understood before work can proceed, development speed eventually converges on the human's reading speed.

Personally, I think this is the first cognitive-load bottleneck AI coding needs to address.

We already have many ways to generate code faster. The next question is how much of the result a human must understand and which evidence should be sufficient for trust.

This does not mean code understanding itself should disappear.

Geoffrey Litt distinguishes understanding for correctness verification from understanding needed to participate in the next change. Even when an agent produces a correct result, a human who learns nothing from the change loses the conceptual material needed for the next idea. The talk describes the accumulation of changes no one understands as `Cognitive Debt`.[^7]

I think this distinction supports contract-centered review. Instead of reading every line at the same depth, use contracts and evidence for correctness while preserving a human-readable explanation of the behavior needed for the next decision.

## 3. Two ways to reduce cognitive load

At the moment, I see two practical approaches.

One moves the object humans must understand from code to a contract. The other keeps generated units small in areas where humans still need to read the code.

They are not mutually exclusive. A team can combine them according to the risk of the code and the strength of its tests.

### Understand the contract, not the entire codebase

The first approach moves human understanding from code to the **contract between business requirements and code**.

Here, a contract is not merely a document. It is the standard used to determine whether a business requirement is true in the implementation.

The human does not need to specify everything:

- Behavior visible to users
- Conditions that must always hold
- Architectural boundaries that must not be crossed
- Decisions the agent may make independently
- Situations that must return to a human

Trying to write a perfect document from the start begins to resemble implementing the feature in advance.

Some constraints become visible only after opening the code. Specifying algorithms and class structures also removes useful implementation freedom from the agent. A better approach is to provide a thin statement of intent and acceptance criteria, let the agent explore the repository, and feed discovered facts back into the contract.

Only the facts that must survive into future implementations should be promoted into a PRD or ADR. Data structures or function boundaries that matter only to the current implementation can stay in the code.[^3]

The agent implements and tests against the contract, then reports what satisfied each requirement and which evidence supports it.

The coding agent's responsibility should shift from producing a lot of code to satisfying the complete contract and proving that it did so.

The human then checks two things:

- Were all explicit contract conditions satisfied?
- Which decisions outside the contract were based on assumptions?

Before reading an entire payment implementation, for example, the reviewer might begin with this:

```text
Requirement
The same payment_id must never be charged twice.

Verification
- duplicate_webhook_does_not_charge_twice: PASS
- retry_after_timeout_returns_previous_result: PASS

Obligation derived from the contract
- A retry with the same payment_id returns the existing payment result.

Implementation discretion
- Store the idempotency key in the existing Redis cluster.
- Follow the key format used by neighboring modules.

Open product decision
- What happens when the amount or currency changes for the same payment_id?
- Recommendation: reject the request as a conflict.
- Alternatives: return the existing result / treat it as a new request.
- Impact: this changes payment safety and data meaning, so ask a human.
```

This does not mean implementation details are never inspected.

Start with requirements and tests, then check the assumptions behind decisions not covered by the contract. Drop into the code only when the evidence is weak or the risk is high.

An assumption here does not mean exposing the model's internal chain of thought.

It means an externally verifiable premise on which the code depends: whether a provider guarantees durable responses, whether tenant information comes from a trusted source, or whether callback order and uniqueness are guaranteed.

If a false premise would break the contract or safety boundary, it must be checked against code, tests, configuration, or authoritative documentation. If it cannot be verified, the work should remain incomplete and return to a human as an unverified risk.

Not every gap in the contract needs to become a question.

The agent should first derive obligations that logically follow from the explicit contract, then follow repository conventions and neighboring code. If a gap remains, it can consult an authoritative protocol or domain rule and choose a reversible default that does not change external behavior.

Function names and internal data structures can remain implementation discretion. Assumptions that change user-visible behavior, data meaning, security, or permission boundaries need a new contract or decision.

When several product choices remain, the agent should not merely ask a vague question. It should present a recommendation, the reason, realistic alternatives, the effect of each, and the contract language that would need to be added.

Bad tests or missing contract requirements can still cause failures. Even so, narrowing review from the entire codebase to requirements, evidence, and exceptions is a substantial improvement.

Perfect contract compliance does not mean declaring that errors are impossible.

It means the agent does not hide an unverified contract item behind a successful status. If evidence is missing or a new decision is required, the agent stops and escalates instead of silently closing the work.

### Divide work into units a human can understand

Some code cannot yet be approved from contracts and tests alone.

Security, payments, and data migrations are examples where implementation choices directly create risk. Humans may also need to read code in older systems with weak test coverage.

In these cases, the important limit is not the number of files but **the number of new concepts that must be understood at once**.

Instead of creating one pull request for an entire payment feature, the work could be divided like this:

```text
PR 1 - Add the Payment state model
PR 2 - Isolate the external provider behind a Port
PR 3 - Prevent duplicate charges
PR 4 - Finalize state from the webhook
```

Each pull request should make clear why the change is needed, which new concept it introduces, which conditions must hold, and which tests demonstrate them.

Waiting for each small pull request to merge before starting the next one, however, wastes much of the agent's generation speed.

Stacked pull requests reduce this cost by allowing later work to continue on top of an unmerged earlier pull request.[^4] The agent keeps moving while the human reviews only the newly added material in sequence.

From the cognitive-load perspective, stacked pull requests divide one large review peak into several smaller peaks.

![Conceptual diagram showing smaller review peaks in stacked pull requests while a base load remains for surrounding context](/assets/img/2026/0818/stacked-pr-cognitive-load-en.svg)

The human still cannot accumulate understanding during the early implementation period before the first pull request is reviewable. The load is not spread evenly across implementation as in traditional development; it appears as several smaller units near the end.

Each peak is also larger than the pull request diff alone.

Understanding one pull request requires the previous behavior, decisions made in earlier pull requests, the effect on later pull requests, and the scope that must be rechecked after revisions.

```text
Actual review scope
= current PR diff
+ behavior before the change
+ decisions in earlier PRs
+ effects on later PRs
+ scope to recheck after revisions
```

Stacked pull requests therefore retain a base load for surrounding context underneath the smaller peaks. As the stack grows, the real understanding scope becomes wider than each individual diff.

I still find stacked pull requests useful because they reduce how much context must be restored at once and lower the instantaneous review peak. But a human remains involved at every step, and if the agent gets several pull requests ahead, the context the reviewer must recover grows again.

#### Turn the development cycle into a small hill

In practice, reducing this load requires more than splitting pull requests. **The development cycle itself must close at a small scale.**

Define one piece of the requirement. Let the agent implement it. Have a human understand and verify the change, then commit it before moving to the next piece.

```text
One requirement slice → implement → understand and verify → commit
```

Small generated units do not create a small development cycle unless human understanding closes at the same boundary. If four small pull requests are stacked first and read in one batch later, generation was divided but the development cycle remained large.

Climbing a neighborhood hill three times is not the same as climbing one large mountain with a similar total elevation.

The large mountain demands more preparation, sustained effort for longer, and slower recovery. Some people cannot complete it with their current capacity.

AI implementation does not change where the peaks occur.

A small cycle still starts with human work to define intent and constraints, drops while the agent implements, and rises again when the human understands, verifies, and commits the result.

The difference is whether the whole feature closes as one large cycle or as several smaller cycles with the same shape. In the following graph, each color represents one cycle that closes only after understanding and commit.

![Conceptual diagram showing one large AI development cycle divided into three smaller cycles whose peaks remain below individual cognitive capacity](/assets/img/2026/0818/small-cycle-cognitive-load-en.svg)

I do not think cognitive load can be compared by adding up a total area alone.

People differ in how much context they can hold at once. Even the same person's capacity changes with domain experience, practice, fatigue, and interruption. The capacity line in the graph therefore sits at a different height for each person and situation.

When a review exceeds current capacity, the cost is not merely slower reading. The reviewer repeatedly loads fragments of context, restores what was lost, and rereads affected areas after revisions.

The longer the review lasts, the longer the person must sustain high cognitive load. Small development cycles lower each peak below the current capacity and close understanding into a commit that becomes the starting point for the next cycle.

## 4. Move recurring decisions out of review

Traditional code review assumes that the author understands the implementation.

The reviewer reads the author's explanation, asks about suspicious parts, and looks for missed risks. The author can explain why the implementation took this form.

When an agent produces most of the code, the human is no longer the author in the same sense.

If we still require that human to explain every line, the implementation time saved by the agent is simply paid again during review.

I think human review therefore needs to move away from reconstructing the entire implementation and toward checking business requirements and contract boundaries.

The agent should run tests and architecture checks, then organize evidence for each contract condition, assumptions used for decisions outside the contract, and remaining risks. The human starts by looking for unproven conditions and hidden assumptions.

When the normal path has sufficient evidence and exposes its out-of-contract assumptions, it should not require repetitive human approval.

Escalation should be reserved for contract changes, conflicts with existing decisions, important assumptions, and high-risk exceptions that automation could not verify. Human involvement then becomes a mechanism for contracts and exceptions rather than a default step in every implementation.[^6]

It is equally important to make repeated decisions disappear from future reviews.

If reviewers repeatedly point out the same import direction, turn it into an architecture test. If they repeatedly check the same requirement, turn it into a test case. Instead of fixing the same mistake several times, improve the harness so the next agent avoids it from the beginning.[^5]

Seen this way, reducing cognitive load means moving recurring human decisions out of review.

As repeated judgments become contracts and guardrails, humans have fewer decisions to make and less new material to understand in the next review.

I apply this principle to the [ALPS Writer Plugins](https://github.com/haandol/alps-writer-plugins) that I maintain.[^3]

An ALPS Feature is not divided horizontally into frontend, backend, and data layers. It is written as one vertical slice that completes a user-observable behavior from UI through API and data. If the unit is too large, it is divided along independently demonstrable user behavior rather than technical layers.

`/feature-to-adr` moves the contract for that slice into an ADR. `/adr-impl` implements and tests the UI, API, and data together. Mapped to the small AI cycles above, the flow looks like this:

```text
ADR containing intent and contract
→ Agent implements UI, API, and data together
→ Completion review with contract-level evidence and tests
→ Accepted
```

If a slice cannot be divided further by meaning, stacked pull requests can still be used inside it. Each pull request gets one review question and its own tests to lower the instantaneous peak, while the full contract and surrounding context remain active until the stack closes.

Completion review connects each contract item to the implementation, code evidence, and executed tests. The agent repairs code and test defects that do not alter the contract. Humans decide only new contracts, contradictions, and important unverified risks.

I recently added an implementation explanation similar to `Explain Diff` to ADR Writer. It connects the ADR's purpose and scope, the behavior before and after the change, the actual request flow, state and failure paths, and tests to concrete code evidence.

The explanation does not judge whether the implementation is correct. It helps a person understand enough to participate in the next change, while contract-level evidence and executed tests determine whether the work is complete.

The current tooling does not measure individual cognitive capacity or prove that a human understood every commit. It does, however, give each vertical-slice ADR a boundary for what one cycle must implement, verify, and close. That boundary directly helps create smaller development cycles.

## Conclusion

Starting with the early Copilot releases forced me to develop the habit of splitting problems and changes into small pieces.

Even after newer models became capable of large tasks, I kept short development feedback loops instead of asking for the maximum amount of code in one pass. That may be why I did not feel the review burden as strongly.

Small pull requests alone will not remove the long-term bottleneck.

If an agent stacks several pull requests before review, each diff may be small while the human still has to reconstruct all of the surrounding context at once. By a small unit, I mean **a development cycle that closes only after the code is produced, understood, verified, and committed**.

Lowering the peaks still leaves the assumption that a human must understand and approve all code.

Over time, I think the better direction is not to make humans read code faster, but to make them understand the contract between business requirements and code. Agents should present verification evidence for each contract and expose externally verifiable assumptions instead of hiding unverified work behind success.

From this perspective, reducing cognitive load is not merely making review more comfortable. **It is the process of moving recurring human decisions into contracts and harnesses so that human-in-the-loop approval disappears from the normal path.**

---

[^1]: Max Kanat-Alexander, [What Makes a Great Developer Experience?](https://www.codesimplicity.com/post/what-makes-a-great-developer-experience/) (2025).

[^2]: Paul Graham, [Maker's Schedule, Manager's Schedule](https://www.paulgraham.com/makersschedule.html) (2009).

[^3]: [Why Detailed PRDs Age So Fast — Separating ALPS and ADR Boundaries](/en/2026/07/25/alps-adr-abstraction-boundaries.html) — explains how PRDs and ADRs become contracts for code generation and review.

[^4]: GitHub Docs, [Stacked pull requests](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests) — explains how dependent pull requests form a stack while each change remains independently reviewable.

[^5]: [How I Built the EncBird Harness Layer by Layer](/en/2026/06/16/harness-engineering-in-practice.html) — describes moving recurring human decisions into rules, tools, and guardrails.

[^6]: [A Lens for Agentic Engineering](/en/2026/06/12/lens-for-agentic-engineering.html) — explains the view of agentic engineering as removing human-in-the-loop steps from the normal path.

[^7]: Geoffrey Litt, [Understanding is the new bottleneck](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck) — distinguishes understanding for correctness from understanding needed to participate in the next change and introduces `Explain Diff`. [Video with Korean and English subtitles](https://youtu.be/x3e_Yl4NNHY).
