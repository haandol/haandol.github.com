---
layout: post
title: "Agentic Engineering and Transitional Technologies"
excerpt: HITL removal is the direction, and coexistence-oriented tools are transitional
author: haandol
email: ldg55d@gmail.com
tags: ai agent harness-engineering agentic-development claude-code headless
publish: true
lang: en
date: 2026-05-11 00:00:00 +0900
translation_key: direction-of-agentic-engineering
korean_url: /2026/05/11/direction-of-agentic-engineering.html
permalink: /en/2026/05/11/direction-of-agentic-engineering.html
---

## TL;DR

- The destination of agentic engineering is **removing humans from the loop**, which may leave tools designed to keep people in the pipeline as **transitional technologies**.

## Introduction

I do not think software development is an end in itself. It is closer to a **byproduct** of making business requirements executable by computers. To put it more bluntly, development is **a compiler that translates business requirements into code**.

Until now, this compilation process has required many specialists: product managers, designers, frontend developers, backend developers, QA engineers, and more. But as agents begin automating this intermediate process, the middle layer is rapidly becoming thinner.

Today, I want to organize my recent thoughts on the direction of this trend and where today's tools stand along that path.

## 1. The final goal is removing humans from the loop

I have already covered the development process in earlier posts,[^1][^2] so I will move on. If I had to summarize the direction of what we call **agentic engineering** in one sentence, it would be this:

**The final goal is removing humans from the loop.**

The goal is to remove the human element entirely from the compilation process that turns business requirements into code. Whether that is actually possible is not especially important when explaining the direction itself. **Unless someone rigorously proves that it is impossible, the companies working in this area will keep trying as long as resources continue to flow.** As with autonomous driving and cloud migration, once an entire industry begins moving in one direction, individual skepticism does not reverse the current.

## 2. Why people remain—and why those reasons are finite

In practice, people still remain throughout the pipeline. The most immediate bottleneck today is **review**. Because current agent output is not considered to fully reflect business and technical requirements, the pipeline still assumes that a person must inspect it one more time at the end. Generation speed has already surpassed human review capacity, and complaints that "code produced with a click is hard to review" come from this assumption.

But I think this problem is likely to be resolved naturally as coding agents and development methods improve. We are already moving toward a structure in which the system that generates the code also owns verification. Because this progress rides on improvements in the model's baseline capabilities, it seems closer to a problem that time will solve than one that requires an entirely new engineering discipline.

The bottleneck after review is **deployment**. A human still has to participate in the handoff from something built locally to something running in production. Packaging the code, building an image, configuring environment variables and permissions, and deciding whether to roll back after a failure all fall into this category.

This point also reaches backward into the development stage. **If even one point of human intervention remains at the end of the pipeline, the stages before it are ultimately designed around that person.** If someone must inspect the code and make a judgment during deployment, the development stage must preserve code in a form that "a person can understand and review." Human dependence in deployment ends up setting the limit on automation in development.

Both bottlenecks are real today, but they are **finite bottlenecks** in the sense that time can resolve them. What matters is which tools can ride the trend when these bottlenecks begin to disappear.

## 3. Designs that assume coexistence and designs that assume human removal

I think today's agentic development tools are splitting around two broad design assumptions: those **designed for coexistence with people** and those **designed for removing people**.

Cursor is a representative example of the coexistence-oriented approach. It optimizes the experience of a person sitting beside an agent in an IDE, moving forward while checking each line. It is a good experience and extremely powerful for productivity today. But leaving a person in the starting assumptions of the design also means that **no matter how much automation is added, the speed at which a person can inspect the work becomes the pipeline's upper bound**. The broader progression of cloud infrastructure so far—VMs, containers, serverless, various PaaS products, and GitOps tools—also sits closer to this axis. It has generally aimed to help "people do this work more easily," not to remove people from it.

On the opposite axis are headless coding-agent configurations and approaches such as Anthropic's Managed Agents. These begin by removing the person. Their default mode assumes that the agent runs its own loop, verifies its own work, and deploys on its own. The immediate experience may be rougher than with coexistence-oriented tools, but their ceiling rises along with advances in LLMs and agents.

The gap between the two matters because it is not merely a UX difference. It is **a difference in design assumptions**. A tool built around coexistence can release the capabilities of a smarter LLM only within "the range a person can verify." A tool designed around human removal, by contrast, can absorb model improvements directly.

## 4. Coexistence-oriented technologies are transitional

Placed against the direction described in Section 1, this distinction leads to a fairly clear conclusion. **Technologies designed to preserve people inside the pipeline are transitional.**

Because review and deployment remain bottlenecks today, coexistence-oriented tools are currently the most practical choice. But once those bottlenecks disappear one by one, the reason for those tools to exist also begins to shrink. Coexistence itself was valuable because of the assumption that "a person must intervene," and that assumption is the first thing beginning to shake.

From this perspective, the difference between transitional and enduring technologies is not how polished they are today but **the direction of their design assumptions**. A good tool built around coexistence is powerful **now**, while a tool built around human removal becomes powerful **later**. The former binds the benefits of model progress to "the speed at which a person can inspect," while the latter absorbs that progress as it comes.

## Conclusion

The direction of agentic engineering is clear: removing humans from the loop. People still occupy places in the pipeline because bottlenecks such as review and deployment remain, but those bottlenecks will gradually be dismantled as models and agents improve.

In that process, **tools designed around coexistence are like lights illuminating a transitional period**. They are extremely useful for raising productivity today, but viewed along the direction of travel, they are likely to be replaced by agentic engineering itself or quietly pushed into obscurity.

Which tool to use today is a practical question. Which direction to bet on is a separate one. For the latter, I personally think **tools designed around removing people** are the better long-term choice.

---

[^1]: [Demystifying Harness Engineering](/en/2026/03/15/harness-engineering-beyond-context-engineering.html).

[^2]: [Multi-Agent Without a Harness Is Just Context Engineering](/en/2026/03/31/multi-agent-without-harness-is-just-context-engineering.html).
