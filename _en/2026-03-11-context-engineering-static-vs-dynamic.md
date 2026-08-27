---
layout: post
title: "Context Engineering — Static Context and Dynamic Context"
excerpt: Managing durable constraints separately from temporary execution context
author: haandol
email: ldg55d@gmail.com
tags: ai agent context-engineering agentic-development vibe-coding prd adr
publish: true
lang: en
date: 2026-03-11 00:00:00 +0900
translation_key: context-engineering-static-vs-dynamic
korean_url: /2026/03/11/context-engineering-static-vs-dynamic.html
permalink: /en/2026/03/11/context-engineering-static-vs-dynamic.html
---

## TL;DR

- It is effective to manage development context as static context—PRDs and ADRs—and dynamic context—tasks, code, and tests.
- Static context contains durable standards and constraints, while dynamic context is created and consumed temporarily.
- As models and tools improve, dynamic context should stay lightweight and disappear whenever possible.

## Introduction

As I work with agentic coding and vibe coding, I increasingly feel that we are returning to the essence of development.

Turning business requirements into code.

I used to describe a framework that managed development context as a hierarchy that became progressively more concrete: [Requirement → Feature → Task → Code][^1].

At the time, I thought it was important to divide the intermediate stages more finely, document more of them, and keep everything continuously up to date. Models and tools were weaker than they are now, so people had to manage more of the intermediate context themselves.

My thinking has changed considerably.

## 1. Models and Tools Have Changed

Models have become much smarter, and coding tools have advanced significantly. Agents can now find the information they need, create their own sequence of work, and construct the next execution path from the codebase on their own.

For that reason, I now think it is better to divide development context into **static context and dynamic context**.

## 2. Static Context

Static context consists of standards and constraints that must remain in place for a long time.

- A **PRD** defines what must be built.
- An **ADR** records why it should be implemented that way and which constraints must be preserved.

These are pieces of information that must remain available for reference throughout the life of a project. No matter how intelligent agents become, people still have to define and manage **what should be built** and **why the team decided to build it this way**. If those foundations shift, the agent will generate code in a different direction each time.

## 3. Dynamic Context

Dynamic context, by contrast, is execution information created and consumed temporarily to move the current work forward.

- A **Task** is closer to a unit of execution created briefly for the work at hand.
- **Code and tests** are the final outputs showing whether the requirements and constraints have actually been satisfied.

People used to have to manage this dynamic context as well. That is no longer the case. Once implementation is complete, what matters is not the record of every intermediate step but **whether the requirements and constraints are properly reflected in the code and tests**.

## 4. Dynamic Context Should Be Ephemeral

If dynamic context is kept around for too long, documents accumulate with every repeated change, and the amount of context that both people and agents must read continues to grow. That bloated context can sometimes interfere with the exploration and execution of an agent that has otherwise become much more capable.

By its nature, dynamic context should therefore remain **lightweight and clear**. Whenever possible, I think it is better to keep only the code and tests and let the rest disappear. As agents and tools become smarter, the amount of context we can allow to disappear keeps growing.

## Conclusion

The core of context engineering today is not preserving every intermediate step forever. It is **keeping static context sharp while treating dynamic context as something more ephemeral**.

As models improve and tools advance, the work left for people seems to move closer to managing good requirements, good constraints, and good validation criteria.

For the code that remains after the dynamic context disappears to become genuinely good context, the code itself must explain the business well. I will discuss that further in the [next post][^2].

---

[^1]: [RFTCR — A New SDLC Framework for Agent-Driven Software Development](/en/2025/05/11/rftcr-framework-for-agentic-dev.html).
[^2]: [The Value of Developers Who Understand the Business in the Age of Agentic Development](/en/2026/03/13/agentic-dev-business-aligned-code.html).
