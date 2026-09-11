---
layout: post
title: "Multi-Agent Without a Harness Is Just Context Engineering"
excerpt: Multi-agent without harness is just large-scale context engineering
author: haandol
email: ldg55d@gmail.com
tags: ai agent multi-agent harness-engineering context-engineering agentic-development
publish: true
lang: en
date: 2026-03-31 00:00:00 +0900
last_modified_at: 2026-09-11 16:33:32 +0900
translation_key: multi-agent-without-harness-is-just-context-engineering
korean_url: /2026/03/31/multi-agent-without-harness-is-just-context-engineering.html
permalink: /en/2026/03/31/multi-agent-without-harness-is-just-context-engineering.html
---

## TL;DR

- Each agent should be able to validate its work and recover from failures.
- Divide tool and context boundaries to match each role.
- Stabilize one execution unit before increasing the number of agents.

## Introduction

Reading Anthropic's article on designing harnesses for long-running agents[^1] helped me reorganize questions I had long held about multi-agent systems.

Something had bothered me ever since I first heard the phrase "agent swarm." Does connecting several agents really improve performance dramatically? Human developers do not always reach better conclusions simply because more of them gather to discuss a problem, so why would agents be different? Today's LLMs are also fairly stubborn. Can they really complement one another just because we assign them different roles?

Earlier posts covered context engineering[^2] and harness engineering[^3] separately. This time, I want to connect those two perspectives and examine when multi-agent systems have real meaning—and when they are merely context engineering at a larger scale.

## 1. Role-specific prompts are not enough

There is a common trap in discussions of multi-agent systems: the belief that changing the system prompt is enough to create a new agent. We assign roles such as "You are a code reviewer," "You are a tester," or "You are an architect," expecting each one to examine the problem from a different perspective.

Role-specific prompts can elicit different perspectives. What I want to examine, however, is **which tools and information the model uses and how it checks its results**, beyond the role name.

In the earlier post,[^3] I distinguished providing and updating information for model decisions from validating execution results and retrying. System prompts, `CLAUDE.md`, and retrieved documents provide context for decisions. Linters, tests, and retry loops let agents find and fix execution errors. I use harness to mean the execution environment connecting the two.

Even with role-specific prompts, an earlier agent's mistakes can reach the next agent if there is no path for validating results and recovering from failures. Communication costs and information lost during context transfer further reduce the benefits of dividing roles.

## 2. When multi-agent systems become meaningful

When building a multi-agent system, the first thing I want to check is **whether each agent can finish and validate its own work**.

When dividing coding work among agents, I think we need to design the tools and information each can use, what happens after failure, and how results will be checked, alongside their role names. Creating an agent does not automatically provide these procedures.

- **Tool boundaries**: Separate the tools each agent can access. For example, a coding agent gets the file system and a linter; a testing agent gets the test environment and coverage tools; a review agent gets diff tools and architecture-validation rules.
- **Recovery loops**: Each agent should be able to recover from failures in its area. A coding agent fixes lint failures automatically; a testing agent analyzes failed tests and reports their causes.
- **Validation**: Before passing one agent's output to the next, check it with tests or architecture checks. Record conditions that could not be verified so the next stage can see them.
- **Context boundaries**: Share common goals and requirements while defining the information and scope each role needs. Agents can read the same material and still perform different work and checks. Copying every exploration record, however, can pass along irrelevant information and errors in earlier judgments.

These four elements help agents **take responsibility for their own work and validation**. They do not require separate harnesses. Anthropic's example also uses the same tools and harness for its initializer and coding agents.[^1] The important distinction is between shared infrastructure and the results each role must check.

## 3. What to Do Before Adding More Agents

At this point, increasing the number of agents matters less than **designing a harness that lets one agent work reliably to completion**.

Can a single agent complete a long-running task reliably with linters, CI, structural tests, and retry loops? Only when the answer is "yes" does adding a second agent become meaningful.

As Anthropic's article on harness design for long-running agents emphasizes,[^1] **limiting the agent to one feature at a time, recording state at the end of every session, and helping the next session understand the previous work quickly** are central to making even one agent reliable. Without this foundation, adding more agents merely combines unstable units into an even less stable system.

## Conclusion

Rather than starting with how many roles have been created, I want to see who decides the next action after a failure and what evidence supports that decision.

If that path cannot be explained, I think it is better to strengthen tools and validation before adding agents. That validation must remain in place after roles are divided for the work to be entrusted to them.

---

[^1]: [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
[^2]: [Context Engineering — Static Context and Dynamic Context](/en/2026/03/11/context-engineering-static-vs-dynamic.html).
[^3]: [Demystifying Harness Engineering](/en/2026/03/15/harness-engineering-beyond-context-engineering.html).
