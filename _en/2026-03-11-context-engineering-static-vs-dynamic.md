---
layout: post
title: "Context Engineering — Static Context and Dynamic Context"
excerpt: Context engineering for agentic development - static context vs dynamic context
author: haandol
email: ldg55d@gmail.com
tags: ai agent context-engineering agentic-development vibe-coding prd adr
publish: true
lang: en
date: 2026-03-11 00:00:00 +0900
last_modified_at: 2026-09-10 10:44:38 +0900
translation_key: context-engineering-static-vs-dynamic
korean_url: /2026/03/11/context-engineering-static-vs-dynamic.html
permalink: /en/2026/03/11/context-engineering-static-vs-dynamic.html
---

## TL;DR

- PRDs and ADRs preserve criteria and constraints for future tasks.
- Clean up temporary plans and exploration records once they are no longer needed.
- Preserve code and tests as verifiable deliverables.

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

Dynamic context is information we read and create while performing the current task. It includes both temporary execution records and deliverables that should remain.

- **Tasks and exploration records** help organize and advance the current work. Temporary plans and search results that the next task does not need can be cleaned up.
- **Code and tests** implement and validate requirements and constraints. They change during work but must remain in the repository after completion.

Frequently changing information is not necessarily disposable. I think it is better to decide what to keep based on whether the next execution needs it and whether it can already be checked again in code and tests.

## 4. Keep Temporary Execution Records Lightweight

If agents keep reading plans and exploration records for completed tasks, context grows with each change. A summary of code that has already changed can also confuse decisions based on the current code.

Clean up temporary records that the next task does not need, while retaining code and tests as deliverables. New requirements and lasting decisions made during work should be reflected in PRDs and ADRs.

There is no need to delete the state or unresolved issues needed to hand ongoing work to the next session. First check whether that information has served its purpose.

## Conclusion

I want to retain the requirements, decisions, code, and tests needed for future tasks, while cleaning up temporary plans and exploration records when they are no longer needed.

For the retained code to help the next agent, it needs to reveal which workflow it handles. I discuss that in the [next post][^2].

---

[^1]: [RFTCR — A New SDLC Framework for Agent-Driven Software Development](/en/2025/05/11/rftcr-framework-for-agentic-dev.html).
[^2]: [The Value of Developers Who Understand the Business in the Age of Agentic Development](/en/2026/03/13/agentic-dev-business-aligned-code.html).
