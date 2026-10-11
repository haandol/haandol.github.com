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
last_modified_at: 2026-10-11 10:07:45 +0900
translation_key: considerations-before-developing-mcp-server
korean_url: /2026/03/02/considerations-before-developing-mcp-server.html
permalink: /en/2026/03/02/considerations-before-developing-mcp-server.html
---

## TL;DR

- Identify what existing tools cannot solve before building your own.
- Where the LLM runs changes the tool provider's responsibilities.
- Delegating execution to the client requires handling interruptions and model differences.

## Introduction

One habit I have developed in the age of agents is building tools to hand off work I do not want to do.

I recently needed to create a PowerPoint presentation. To avoid manually drawing what I had in mind, I tried Claude PowerPoint skills,[^3] a PowerPoint-generation MCP server,[^4] and paid tools.[^5][^6] The open-source tools either fell short of the quality I wanted for customer presentations or made precise slide edits difficult. Commercial tools generally produced good results, but I could not use them when internal material could not be sent outside the company.

I decided to build my own PowerPoint generator. One decision occupied much of my attention: who should execute the work that needs a model? The tool could call a model itself, or delegate that work to the coding agent the user already has.

MCP, the Model Context Protocol, connects agents to external tools. Choosing to build an MCP server does not settle where the model runs. Here is what I learned while separating **the reason to build the tool from the choice of where to execute its model work**.

## 1. Identify the Unsolved Problem Before Implementing

I often say that the value of coding itself is falling. What I experience is a declining cost of implementing the same feature. That makes me want to spend more time finding and validating what to build.

Yet easier implementation makes me reach for the keyboard first. Even if execution costs less, it still consumes my time. Changing that traditional builder's habit takes practice.

For a business, I first look for `a problem worth paying to solve && a problem that has not yet been solved`. With the PowerPoint tool, precise editing and restrictions on sending material outside the company remained unsolved after I tried existing products. Those were my reasons to build it.

I also feel that implementation complexity alone is becoming a weaker competitive advantage. An agent can investigate a service's visible behavior and inspect it with browser automation, reducing the cost of building similar features. Visible behavior, however, does not reveal every internal rule or lesson learned from operating the service.

That draws my attention toward unique customer data and how a service uses it. Copying screens does not tell you what actual customers want or which results they find useful.

## 2. Decide Where the LLM Runs

Once there is a clear reason to build, the next decision is who calls the LLM—a large language model—and manages execution.

An MCP server or skill can make the tool available through an agent the user already uses. Here, I use offloading to mean **delegating LLM processing to that user's client**.

I went through all three approaches below while building alps-writer,[^1] and intended to delegate LLM processing to the client in ppt-generator[^2] as well.

| Delivery approach | Where the LLM runs | What the tool handles |
| --- | --- | --- |
| A web service installed and run by the user | Inside the service | Web interface, model calls, and task state |
| An MCP server that calls a model itself | Inside the MCP server | Model calls and result processing in response to tool requests |
| Skills and MCP tools delegating execution to the client agent | In the user's client | Workflow instructions, state management, and data processing |

In the first two approaches, the provider controls the model and prompt flow. In the last, the user's existing agent handles reasoning, reducing the tool's burden of operating a separate model-calling path.

Skills supply instructions for doing work; MCP connects tools. They can be used together. **How much direct control the model execution requires** has more impact on this design than the delivery format alone.

## 3. Delegating Execution Reduces Control Over Its Conditions

Offloading LLM processing can reduce the user's burden of configuring a model separately for each tool. It also means the provider cannot determine the entire execution environment.

### Conflicts with Existing Instructions

A coding agent already has system instructions governing its role and behavior. The PowerPoint tool's instructions must operate within that environment.

Assigning a new role at length is not enough to obtain the desired behavior. Conflicting instructions can change how the task proceeds. The tool needs to specify its inputs, expected results, and next steps clearly.

### Interruptions and Model Differences

The provider cannot always know the user's remaining execution allowance or how much information the client can process at once. State needs to be saved so work can resume after an interruption at any stage.

With direct model calls, the provider can design caching around repeated prompt content. A client agent does not offer the same control over conversation construction and caching.

Users also choose different models. A complex workflow tested with Claude Sonnet 4.6 needs separate validation on Gemini 3.1 Flash. Assuming that changing the model name is sufficient makes it hard to preserve the intended experience.

## 4. Define What the Tool Provider Still Owns

Building these tools has made me feel that client agents are becoming part of the execution infrastructure. Instead of operating every model call and agent process ourselves, we can use capabilities supplied by the user's agent.

Cloud infrastructure does not disappear. Providing execution behind the scenes resembles serverless computing in that respect. The tool provider still needs to decide which responsibilities remain: state storage, file processing, and result validation, for example.

Adapting to model changes remains a responsibility, too. I left Cursor after feeling that its usability changed around the transition from Claude 3.5 v2 to 3.7. That experience made me wary of assuming a tool's instructions will keep working unchanged with external models.

An environment offering several models, such as Bedrock, can help us try alternatives. Availability alone does not establish compatibility. For a PowerPoint tool, we should also be able to check whether the generated file opens and whether only the requested part was changed.

## Conclusion

If I build another MCP server, I will first identify what existing tools leave unsolved. Then I will decide whether I need direct control over LLM execution or can delegate it to the user's agent.

Delegating execution reduces what I need to build and operate. It makes resumable state and result criteria that remain checkable across models more important. **Deciding what to delegate and what the tool must own** is work to do before implementation begins.

---

[^1]: [alps-writer](https://github.com/haandol/alps-writer)
[^2]: [ppt-generator](https://github.com/haandol/ppt-generator)
[^3]: [claude-office-skills](https://github.com/tfriedel/claude-office-skills)
[^4]: [Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server)
[^5]: [Genspark](https://www.genspark.ai/)
[^6]: [Canva](https://www.canva.com/)
