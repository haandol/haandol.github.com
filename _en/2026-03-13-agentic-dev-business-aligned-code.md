---
layout: post
title: "The Value of Developers Who Understand the Business in the Age of Agentic Development"
excerpt: In the agentic development era, developers who understand business become far more valuable
author: haandol
email: ldg55d@gmail.com
tags: ai agent agentic-development ddd business vibe-coding claude-code
publish: true
lang: en
date: 2026-03-13 00:00:00 +0900
translation_key: agentic-dev-business-aligned-code
korean_url: /2026/03/13/agentic-dev-business-aligned-code.html
permalink: /en/2026/03/13/agentic-dev-business-aligned-code.html
---

## TL;DR

- Managing development progress in a separate document is a transitional approach. When the code itself explains what it does well, that code is the best context.
- Give agents the role of proposing work as well as executing it, while people make decisions based on the domain and the organization.
- The value of coders will decline, while the value of developers who understand the business will rise significantly.

## Introduction

Now that Claude Code is available through Bedrock, I have been trying it for the first time, and GSD seems to be widely used for managing project state.

Unlike tools such as TaskMaster or todo lists that track work within a session, I personally think managing development progress through documents, as GSD does, is a transitional technology.

If the code itself is written to explain clearly what it does, an agent can generate reliable code simply by reading and understanding it. In an earlier post,[^1] I argued that dynamic context should be allowed to disappear, leaving only code and tests. Seen as an extension of that argument, the code itself is the most trustworthy context. A separate summary document may fail to be updated and cannot contain all the detailed context, so it may instead leave room for the agent to generate incorrect code. It also seems to offer little advantage in terms of tokens, because the agent will read the code related to the target of a change during development anyway.

Then how can we make an agent understand the business simply by reading the code?

## 1. Aligning Business Processes and Code

When you think about how to make an agent write code more consistently and maintain it better, you eventually arrive at one conclusion. **When the code clearly explains the business and what it does, that code becomes the best context.**

From the perspective of requirements analysis and design, I think DDD, or Domain-Driven Design, may become even more important. One of DDD's core principles is encouraging real business processes to be reflected in code. With a ubiquitous language, domain experts and developers use the same words, and those words appear directly in class and method names. This becomes even more valuable in the age of agents.

When business processes are reflected clearly in code, you can make consistent code changes simply by explaining a change in the business process to the agent. If you say, "The refund policy for order cancellations has changed," the agent can find domain objects such as `OrderCancellation` and `RefundPolicy` and modify precisely the relevant logic.

Conversely, if business logic is scattered across the codebase or code names are disconnected from business terms, the agent misunderstands the context, changes the wrong place, or creates duplicate logic. In the end, **as agentic development advances, it creates an environment in which business processes and code can align more closely, while a codebase with strong alignment becomes the foundation for using agents more effectively.**

## 2. Agents Propose, Humans Decide

Agents are often used only to execute work proposed by a person. But if you give the agent the role of proposing work as well as executing it, then provide feedback on those proposals as you proceed, you can see results that exceed expectations.

In the future, the knowledge that people will continue to understand better than agents will probably be domain knowledge and operational knowledge about the organization. A good developer may ultimately be someone who gives an agent enough domain information, lets it produce three or four proposals, and then makes a judgment informed by the organization, including the team's capabilities and the direction of the business.

In this flow, the value of coding skill itself continues to decline. In an era when agents write, refactor, and even optimize code, "the ability to write code well" is no longer scarce. By contrast, **the ability to understand a business domain deeply and communicate that understanding accurately to an agent** becomes increasingly scarce.

## 3. What Changes as Execution Costs Fall

Over the past few years of developing with AI, the cost of execution has steadily fallen. As a result, I have experienced having time for things I otherwise would not have done.

Documentation, refactoring, and optimization are representative examples of work that is hard to make time for ordinarily but has become easy to try with AI. This effect is also expanding beyond code.

Ironically, as the cost of execution falls, what becomes more important is not execution itself but **the ability to decide what to execute**. If you tell an agent, "Build this," without understanding the business, it will build it. But only a person can decide whether the result is actually needed by the business and whether it has the right priority.

## Conclusion

As agentic development advances, the role of the coder will shrink, while the value of developers who understand the business will rise significantly.

Making code explain the business clearly, letting agents make proposals and judging them from a domain perspective, and using lower execution costs to spend time on the problems that truly matter—these are becoming core capabilities that developers will need.

More than writing a good separate summary document, **building a codebase in which the business is directly embedded in the code** is the most powerful form of context engineering in the age of agents.

---

[^1]: [Context Engineering — Static Context and Dynamic Context](/en/2026/03/11/context-engineering-static-vs-dynamic.html).
