---
layout: post
title: "What to Consider Before Building an MCP Server"
excerpt: Design tradeoffs to examine before building an MCP server
author: haandol
email: ldg55d@gmail.com
tags: mcp model-context-protocol mcp-server ai agent skills
publish: true
lang: en
date: 2026-03-02 00:00:00 +0900
translation_key: considerations-before-developing-mcp-server
korean_url: /2026/03/02/considerations-before-developing-mcp-server.html
permalink: /en/2026/03/02/considerations-before-developing-mcp-server.html
---

## TL;DR

- I need to break the habit of reaching for the keyboard first.
- Complex business logic is no longer a moat. Competitive advantage lies in customer data that cannot be replicated.
- Whether to offload LLM processing to the client is the core design decision, and the cost is prompt conflicts and uncertainty about the token budget.

## Introduction

One thing that has happened to me in the age of agents is that I keep building tools that let me hand off as much of the work I really do not want to do as possible.

I recently needed to create a PowerPoint presentation. For most people, the most tedious part of making a presentation is probably turning the picture in their head into something drawn by hand. GenAI is an ideal tool for automating that kind of work.

As part of my struggle to avoid doing the work myself, I tested Claude PowerPoint skills,[^3] a PowerPoint-generation MCP server,[^4] and other paid tools.[^5][^6] The open-source tools either produced quality that felt questionable for customer-facing material or made it difficult to revise exactly the part of a slide I wanted. The commercial tools generally produced good quality, but I could not use them when internal company material must not be exposed.

In the end, I decided to build my own vibe PowerPoint generator. I noticed several things while vibe coding it, and I will share one or two of them here.

## 1. Coding Has Little Value, and It Will Fall Further

One thing I have been saying almost habitually lately is that the value of coding has fallen dramatically. Judging from my daily experience, I think that trend will continue downward.

If I stretch the idea slightly from coding to execution in general, execution now has less value than finding a meaningful problem. I therefore need to change how I think so that I spend more time finding and validating meaningful problems. As someone with the mindset of a traditional builder, this seems to require some training.

Perhaps the lower cost of execution actually makes me more likely to execute first. But the value of time has not changed, so I need to adjust how I think and spend that time on higher-value activities.

There are many ways to define a meaningful problem, but I personally think it is `a problem worth paying to solve && a problem that has not yet been solved`. Most other problems are secondary and reduce the already diminished value of execution even further.

It is natural for a developer's hands to move toward code first. But as the value of coding falls, we need to practice holding back. **Let us ask one more time whether this truly needs to be built, and do much more research first.** Time has become the most important resource.

## 2. Complex Business Logic Is No Longer a Moat

In the past, complex business logic itself was an important source of competitive advantage. Carefully designed logic was difficult to copy, and that became the service's moat. Advances in agent tools are breaking down that assumption. With agent tools such as deep research and Playwright, it has become entirely possible to analyze and reproduce a service's logic in detail. No matter how sophisticated the logic is, if an agent can observe and analyze its behavior, replication is only a matter of time.

The data supporting that logic, however, cannot be copied. Only high-fidelity customer data acquired through agents remains genuinely impossible to reproduce. Accumulating this kind of data is what makes a service unique, and **competitive advantage is moving from implementation complexity to data uniqueness**.

## 3. The Form of Tools Is Changing

As users change, the form of tools changes with them. Tools were previously developed and delivered mainly for developers. As Claude Desktop and vibe coding became more common, tools began to be built as MCP servers. Now Skills and plugins are becoming the mainstream approach.

Whether the tool is an MCP server or a Skill, the most important implementation decision is ultimately **whether to offload the LLM processing**.

For an MCP server, for example, the question is whether the server accepts an API key and calls the LLM itself, or whether a client such as Claude Code handles all LLM processing while the MCP server manages only state.

The former was common when the target users were early-adopter developers. Recently, however, the number of non-developer and general developer users has grown, increasing cost pressure and making the latter approach—offloading LLM processing to the user's client—more common.

I went through all three approaches described below while building alps-writer,[^1] so I experienced the trial and error firsthand. I also tried to offload the LLM work in the ppt-generator[^2] I built this time.

### Three Approaches to LLM Offloading

1. **An installable web service that users must run themselves** — The server calls and processes the LLM directly. The user interacts through a web UI.
2. **An agent-based MCP server with a third-party dependency** — The MCP server accepts an API key and calls the LLM directly. The user's client agent invokes the MCP server as a tool, but the actual LLM processing happens inside the MCP server.
3. **The Claude Skills approach** — All LLM processing is offloaded to the client agent. The tool handles only state management and data processing, while prompts and workflow guidance direct the agent's behavior.

## 4. Problems with LLM Offloading

There are two major problems with LLM offloading.

### System Prompt Conflicts

It is difficult to make an agent perform the work I want when the client agent already has a strong system prompt holding it in place.

This is the same reason behind the familiar advice, `Do not assign a role in an agent prompt.` A client agent such as Claude Code has already been assigned the role of coding agent through its system prompt. Adding another role in a prompt creates a conflict and reduces performance.

No matter how general-purpose it is designed to be, the agent was still built for coding. Forcing it to behave as something else requires considerable effort.

### An Unpredictable Execution Environment

LLM offloading itself can become a major obstacle.

First, I cannot know the remaining token budget, so I cannot know how far the work will progress before it stops. Every stage therefore has to be designed with interruption in mind.

With prompt caching, I can optimize token usage by building the most efficient caching flow when I control the prompt and workflow. With an agent, I do not have that control.

Model selection also depends on the user, so there is no way to guarantee that the tool will behave as its creator tested it. The probability that a `complex` prompt that worked well with Claude Sonnet 4.6 will behave the same way with Gemini 3.1 Flash is not high, though it will vary with the complexity of the prompt work.

## 5. The Changing Role of Cloud Infrastructure

After building several tools through this process, I began to think that the value proposition of cloud companies is changing.

As offloading LLM processing to users' client agents becomes the mainstream approach, the traditional cloud proposition—which encourages customers to build their own agents and serve the infrastructure and models—will need a new form of support.

Subscriptions to agent tools such as Claude Code, Codex, and Gemini are beginning to act as infrastructure in their own right. As these tools become available through the web, it feels as if **infrastructure abstraction is moving up another level**. Infrastructure is not disappearing. It is evolving into a form invisible to the user, which is also a natural extension of serverless computing.

## 6. How Quickly Tool Providers Adapt to Models

In this environment, the speed at which a tool provider adapts to changes in models is becoming increasingly important.

When a new model behaves differently from the previous one, the tool must be aligned with it. A tool that depends on external models is much more likely to lose that connection.

Cursor once took a major usability hit when Claude 3.7 arrived with a direction significantly different from Claude 3.5 v2, and many users left—I was one of them. Without a model of its own, a tool provider cannot obtain the insights that emerge from the internal training process, so it must always accept the risk of falling one or two steps behind the official tool. A multimodel approach such as Bedrock can be one strategy for reducing this risk.

Further model advances may reduce these constraints, but for now they remain practical considerations.

## Conclusion

The form of tools is changing rapidly, and today's best choice can become tomorrow's legacy. The role of cloud infrastructure is changing with it, and the challenge ahead will be to find new areas of value that cannot be replaced by agent subscriptions. This seems like a time to spend more time finding meaningful problems and build only after validating them as thoroughly as possible.

---

[^1]: [alps-writer](https://github.com/haandol/alps-writer)
[^2]: [ppt-generator](https://github.com/haandol/ppt-generator)
[^3]: [claude-office-skills](https://github.com/tfriedel/claude-office-skills)
[^4]: [Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server)
[^5]: [Genspark](https://www.genspark.ai/)
[^6]: [Canva](https://www.canva.com/)
