---
layout: post
title: "The Value of Developers Who Understand the Business in the Age of Agentic Development"
excerpt: Helping agents find business meaning in code
author: haandol
email: ldg55d@gmail.com
tags: ai agent agentic-development ddd business vibe-coding claude-code
publish: true
lang: en
date: 2026-03-13 00:00:00 +0900
last_modified_at: 2026-09-11 16:33:32 +0900
translation_key: agentic-dev-business-aligned-code
korean_url: /2026/03/13/agentic-dev-business-aligned-code.html
permalink: /en/2026/03/13/agentic-dev-business-aligned-code.html
---

## TL;DR

- Business terminology in code helps agents locate what needs to change.
- Knowledge of the business and organization matters when judging an agent's proposals.
- As execution costs fall, deciding what to build becomes more important.

## Introduction

Now that Claude Code is available through Bedrock, I have been trying it for the first time, and GSD (Get Shit Done) seems to be widely used for managing project state. It keeps requirements, plans, and progress in documents that later tasks can read.[^2]

Unlike tools such as TaskMaster or todo lists that track work within a session, I personally think managing development progress through documents, as GSD does, is a transitional technology.

Code that reveals what it does helps an agent understand current behavior. That is also why I suggested in the previous post[^1] cleaning up temporary execution records while retaining code and tests: the current state can be checked again in those artifacts.

Separate summary documents can miss updates or omit necessary details. If the agent must read the relevant code when making changes anyway, I start asking whether continuously maintaining a summary is worth the cost.

Then how can we make an agent understand the business simply by reading the code?

## 1. Aligning Business Processes and Code

To find the code to modify, an agent needs to connect business terms in the requirements to names in the code. **The more clearly the code shows which workflow it handles, the easier that connection becomes.**

I think Domain-Driven Design (DDD), which organizes software around business concepts and rules, may become more important in requirements analysis and design. Domain experts and developers share words that also appear in class and method names—an approach called ubiquitous language. Those names give agents clues for connecting a business request to code.

For example, given a request to change the refund policy for order cancellations, names such as `OrderCancellation` and `RefundPolicy` provide clues to the relevant logic. The agent still needs to read the code connected to those objects and verify the revised policy with tests.

When business logic is scattered or names differ from business terminology, an agent may miss relevant code or create duplicate logic. I therefore think making the connection between workflows and code explicit also helps when developing with agents.

## 2. Agents Propose, Humans Decide

Agents are often used only to execute work proposed by a person. But if you give the agent the role of proposing work as well as executing it, then provide feedback on those proposals as you proceed, you can see results that exceed expectations.

In the future, the knowledge that people will continue to understand better than agents will probably be domain knowledge and operational knowledge about the organization. A good developer may ultimately be someone who gives an agent enough domain information, lets it produce three or four proposals, and then makes a judgment informed by the organization, including the team's capabilities and the direction of the business.

As agents take on more implementation and refactoring, I expect to spend more time deciding what to change. That requires understanding the domain and organizational circumstances, and communicating those decisions precisely to the agent.

## 3. What Changes as Execution Costs Fall

Over the past few years of developing with AI, the cost of execution has steadily fallen. As a result, I have experienced having time for things I otherwise would not have done.

Documentation, refactoring, and optimization are representative examples of work that is hard to make time for ordinarily but has become easy to try with AI. This effect is also expanding beyond code.

Even when execution costs fall, someone must decide which changes are needed and which should take priority now. I want to solicit the agent's proposals and use human knowledge to judge whether they fit the domain and the organization.

## Conclusion

AI has given me room to attempt documentation and refactoring that I used to postpone. I also want to use that time to clarify the connection between business terminology and code.

When evaluating an agent's changes, I want to start with which workflow is changing and why. As more things become feasible to execute, I think the domain knowledge needed for that judgment will matter more.

---

[^1]: [Context Engineering — Static Context and Dynamic Context](/en/2026/03/11/context-engineering-static-vs-dynamic.html).
[^2]: [GSD README](https://github.com/gsd-build/get-shit-done/blob/main/README.md) — a tool that preserves requirements, plans, and state in documents to carry work context across sessions.
