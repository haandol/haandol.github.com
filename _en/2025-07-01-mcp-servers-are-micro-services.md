---
layout: post
title: "What to Consider Before Taking MCP Servers to Production"
excerpt: Preparing MCP-powered agents for production
author: haandol
email: ldg55d@gmail.com
tags: mcp msa observability llm efficiency agent
publish: true
lang: en
date: 2025-07-01 00:00:00 +0900
translation_key: mcp-servers-are-micro-services
korean_url: /2025/07/01/mcp-servers-are-micro-services.html
permalink: /en/2025/07/01/mcp-servers-are-micro-services.html
---

## TL;DR

- Adding MCP servers to an agent turns it into a microservices architecture.
- MCP adoption ultimately requires the organization, platform, and operations to mature together, just like a monolith-to-microservices migration.
- What matters is not how many MCP servers you connect, but how many tools they provide.

## Introduction

I recently worked on a project to build an MCP-based chatbot.

Once I tried taking it to production, however, I found that there was quite a lot to consider.

Based on that personal experience, I will summarize a few things to keep in mind when developing an agent with MCP servers.

## The Important Points

If I had to choose only the two most important points, they would be:

1. Observability
2. Context management

## 1. Adopting Remote MCP Servers Is Like Adopting Microservices

When I previously developed agents with tools, all the logs were collected on one server, which made debugging easy.

This does not apply when MCP is used over stdio, but that usage is uncommon outside personal use or debugging. Connecting to remote MCP servers over Streamable HTTP will probably be the more common approach.

With remote MCP servers, however, logs are distributed across multiple servers, making debugging more difficult. It becomes even harder when other teams manage those servers.

In the end, adopting remote MCP servers was similar to adopting a microservices architecture in many respects. Without observability—logs, metrics, and traces—such an environment becomes a black box that is difficult to debug.

If you do not have microservices-level development and operational experience, you should therefore compare the tradeoffs against conventional tools more carefully before adopting MCP servers.

| Stage | What to do | Stack I use |
|------|-----------|---------------|
| **① Logs** | Structured JSON logs with a required `trace_id` | Fluent Bit → Loki / CloudWatch Logs |
| **② Metrics** | Tool-call TPS, latency, error rate, and token usage | Prometheus + Grafana |
| **③ Tracing** | Trace the entire LLM → Agent → tool path with OpenTelemetry | Jaeger, starting with 1% sampling |
| **④ Service map** | Automatically visualize dependencies | Jaeger Service Dependencies |
| **⑤ Alerts** | 95th-percentile latency > X ms, error rate > Y% | PagerDuty → Slack |
| **⑥ Health checks** | A `/healthz` endpoint for every tool | Service-mesh liveness probe |
| **⑦ Environment separation** | Isolate sensitive information such as production tokens from staging | Separate environments with Terraform |

### Tips That Helped in Practice

- OpenTelemetry traces let you follow the entire path of a tool call. Most LLM tracing tools are moving toward native OpenTelemetry support.
- Connecting Trace IDs makes it possible to move between logs and the trace UI with one click.
- Separate graphs for `input_tokens` and `output_tokens` are useful for cost optimization.
- Saving failed trace payloads makes them available for reproduction tests.

I personally use Arize Phoenix for observability.

## 2. MCP Servers and Tools Are Context

Whether you give an agent tools or connect MCP servers, the fact that an LLM is invoked does not change.

Nor does an LLM gain some additional capability merely because tools or MCP are supplied through dedicated API fields.

An LLM is ultimately a machine that receives text and produces text. We call that input and output text context.

No matter how I provide tools from the client—a hard-coded prompt, MCP, or an API's JSON field—they are ultimately passed to the LLM as context and executed. Tools therefore need to be viewed from the perspective of context.

### Problems Caused by Adding More Tools

We know that as an LLM's input context grows, accuracy declines, latency increases, and costs rise.

The same applies to tools. As the number of tools grows, cost and latency increase. Tool-selection accuracy falls in particular.

The table below shows the results of an experiment from the perspective of tools. The figures are averages from 1,000 runs of the same query using GPT-4o-32k in function-calling mode.

| Number of tools | Tool-description tokens | Additional tokens per call | Response latency | Tool-selection accuracy |
|-------|-------------|------------------|----------|-------------|
| 2   | 120        | +240           | +80ms    | 98% |
| 6   | 110        | +660           | +320ms   | 92% |
| 15  | 105        | +1,575         | +900ms   | 78% |
| 30  | 95         | +2,850         | +1,800ms | 63% |

As you can see, cost and latency do not rise linearly as tools are added. They rise in **steps**. The model also becomes much more confused between similar tools.

When multiple MCP servers are written and managed by different organizations, it is especially important to make tool descriptions consistent. Accuracy falls even further when words in those descriptions are used with different meanings, descriptions overlap, or wording is ambiguous.

Some LLM providers allow as many as 128 registered tools, but **performance actually starts to decline once the count passes about ten**.

An MCP server usually provides three or four tools, so **about three MCP servers at most is appropriate**.

### Tool-Diet Strategies

I could write an enormous amount about this topic, or summarize it briefly as below.

Most of it is intuitive, so I will keep it short. What matters is keeping the number of tools an MCP server provides and their scope—the bounded context—at an appropriate size.

- Define tool boundaries **top-down** rather than bottom-up.
- **A tool is not an API.** Design fewer tools that can perform more kinds of work.
- If the parameters become too large, it may be better to **query directly with code**, such as a Python REPL, SQL, or GraphQL.

### Strategies for Mitigating Token and Cost Explosions

The following practices are common in agent-based applications, but they apply equally to MCP.

1. **Dynamic tool filtering**
   - Use a router model or rules to include only the tools needed for the current query in the prompt.
2. **Slim down tool metadata**
   - Shorten descriptions and parameter text, and minimize example JSON.
3. **Condense conversations**
   - Replace old conversations with summaries and use retrieval only.
4. **Use caching aggressively**
   - Reuse identical queries and tool results through semantic caches, prompt caches, and tool caches.
5. **Set guardrails**
   - Prevent infinite loops by setting `max_tool_calls`.
   - Separate tools such as search and payment into dedicated agents, and mount them only when needed.

## PoC → Production Checklist

- [ ] **Complete the observability stack** with log, metric, and trace dashboards and alerts
- [ ] **Introduce a cache system** for tool and prompt caching
- [ ] Apply a **tool-filtering router** and limit prompt tokens to < N k
- [ ] Set a **TPS limit for every tool** with rate limits and circuit breakers
- [ ] Set a **monthly token-budget alert** that notifies Slack when cost exceeds the budget by 5%
- [ ] Prepare a **rollback plan** that automatically unmounts a newly deployed tool if deployment fails
- [ ] Add a **security gate** in which a tool-registration PR is merged only after an LLM safeguard check
- [ ] Run a **load test** at twice the expected peak TPS
- [ ] Prepare a **DR/HA strategy** that deploys MCP servers and tool containers across multiple Availability Zones, with RTO ≤ 15 minutes

## Conclusion

MCP is appealing because, as the phrase "the USB port for LLMs" suggests, it lets us connect many different tools. Just as a physical device has a limited number of USB ports, however, there is also a physical limit to how many MCP connections an LLM can handle.

That port count ultimately corresponds to the effective context size an LLM can process. Unless the accuracy problems caused by growing context improve as well, simply increasing context-window size and lowering prices will not increase the number of usable ports.

A strategy in which a single agent performs many different tasks through many MCP servers is therefore unlikely to be effective in most cases.

The likely answer will be domain-specific multi-agent systems in which each agent uses tools appropriate to its domain. In that environment, observability will become even more important.
