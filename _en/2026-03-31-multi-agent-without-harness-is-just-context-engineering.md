---
layout: post
title: "Multi-Agent Without a Harness Is Just Context Engineering"
excerpt: When multi-agent systems become more than role-split prompting
author: haandol
email: ldg55d@gmail.com
tags: ai agent multi-agent harness-engineering context-engineering agentic-development
publish: true
lang: en
date: 2026-03-31 00:00:00 +0900
translation_key: multi-agent-without-harness-is-just-context-engineering
korean_url: /2026/03/31/multi-agent-without-harness-is-just-context-engineering.html
permalink: /en/2026/03/31/multi-agent-without-harness-is-just-context-engineering.html
---

## TL;DR

- An agent is not merely an LLM with a different prompt, but an **execution unit** combining an LLM, tools, context, and a harness.
- Multi-agent systems become meaningful when every agent has an **independent execution structure** with its own tools, recovery loops, validation methods, and context boundaries.
- Splitting roles without harnesses merely gives one LLM more roles and fragments of context.

## Introduction

Reading Anthropic's article on designing harnesses for long-running agents[^1] helped me reorganize questions I had long held about multi-agent systems.

Something had bothered me ever since I first heard the phrase "agent swarm." Does connecting several agents really improve performance dramatically? Human developers do not always reach better conclusions simply because more of them gather to discuss a problem, so why would agents be different? Today's LLMs are also fairly stubborn. Can they really complement one another just because we assign them different roles?

Earlier posts covered context engineering[^2] and harness engineering[^3] separately. This time, I want to connect those two perspectives and examine when multi-agent systems have real meaning—and when they are merely context engineering at a larger scale.

## 1. An agent is not an LLM with a different prompt

There is a common trap in discussions of multi-agent systems: the belief that changing the system prompt is enough to create a new agent. We assign roles such as "You are a code reviewer," "You are a tester," or "You are an architect," expecting each one to examine the problem from a different perspective.

But an agent is not simply "an LLM with a different prompt." **An agent is closer to an execution unit that combines an LLM, tools, context, and a harness.**

The important point is that context and harnesses play different roles. As discussed in the earlier post,[^3] **context engineering keeps an agent moving in the intended direction over a long cycle.** System prompts, CLAUDE.md, RAG documents, and memory tell it "where to go." **Harness engineering lets the agent work autonomously by recovering errors, retrying, and managing failures within short cycles.** Linters, CI, structural tests, and retry loops let it "get back up automatically when it stumbles along the way."

An agent created only by changing the prompt is missing the harness. Context can provide the broad direction, but there is no error recovery or validation within the short execution cycle. Dividing roles may make each agent appear busy, but mistakes accumulate, agents fail to validate one another's output properly, and the expected performance never materializes.

## 2. When multi-agent systems become meaningful

When, then, does a multi-agent system make sense?

**When the agents differ not only in role or prompt, but each has a sufficiently harnessed execution structure of its own.**

In an environment such as Claude Code, for example, each agent can be harnessed in considerable detail. You can design agent-specific tools, recovery loops, validation methods, and context boundaries.

What does that require in practice?

- **Tool boundaries**: The tools available to each agent should be separate. A coding agent might receive filesystem access and a linter, a testing agent a test environment and coverage tools, and a review agent diff tools and architectural validation rules.
- **Recovery loops**: Each agent should be able to recover from failures in its own area. A coding agent should automatically correct lint failures, while a testing agent should analyze a failed test and report the cause.
- **Validation methods**: There must be mechanisms that validate agent output mechanically. This is enforcement, not hope. One agent's output should pass automated validation before becoming the next agent's input.
- **Context boundaries**: The context visible to each agent should be clearly separated. If every agent shares the same context, the system is effectively no different from assigning several roles to one agent.

Only with these four elements can a multi-agent system operate as a collection of **truly independent execution units**. In human organizations, it is the difference between merely saying, "You handle the frontend and you handle the backend," and giving each team its own CI/CD pipeline, code-review process, deployment permissions, and monitoring dashboards.

## 3. What a multi-agent system without harnesses really is

What happens when a multi-agent system divides roles without providing harnesses?

From the outside, several agents appear to collaborate. The picture is intuitive and attractive: "A planning agent organizes the requirements, a coding agent implements them, and a review agent checks the result."

**In practice, however, this may amount to nothing more than giving one LLM more separated roles and more fragments of context.** If each agent is just another call to the same LLM with a different system prompt, without an independent execution environment or validation mechanism, the structure is fundamentally equivalent to asking one LLM to take on different roles in sequence.

In that state, it is difficult to achieve the expected performance gains or ROI. Instead, the system adds communication overhead between agents, loses information while passing context, and allows one agent's mistakes to propagate to the next without validation.

The same is true in human organizations. Dividing roles without processes, tools, or validation systems only increases communication costs. Agents are no different.

## 4. What to do before adding more agents

At this point, increasing the number of agents matters less than **designing a harness that lets one agent work reliably to completion**.

Can a single agent complete a long-running task reliably with linters, CI, structural tests, and retry loops? Only when the answer is "yes" does adding a second agent become meaningful.

As Anthropic's article on harness design for long-running agents emphasizes,[^1] **limiting the agent to one feature at a time, recording state at the end of every session, and helping the next session understand the previous work quickly** are central to making even one agent reliable. Without this foundation, adding more agents merely combines unstable units into an even less stable system.

## Conclusion

Multi-agent systems become effective not when we create many agents, but **when each agent has its own harness and operates as a genuinely independent execution unit**.

Until then, many multi-agent systems may be little more than context engineering at a larger scale.

Before increasing the agent count, build an environment in which one agent can get back up after it falls. That is ultimately the fastest path to a multi-agent system.

---

[^1]: [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
[^2]: [Context Engineering — Static Context and Dynamic Context](/en/2026/03/11/context-engineering-static-vs-dynamic.html).
[^3]: [Demystifying Harness Engineering](/en/2026/03/15/harness-engineering-beyond-context-engineering.html).
