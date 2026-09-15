---
layout: post
title: "Did AI Coding Tools Actually Cut Development Cost? — Understanding CTS-SW"
excerpt: Measuring AI by software delivery cost
author: haandol
email: ldg55d@gmail.com
tags: ai engineering-productivity cts-sw developer-experience organization
publish: true
lang: en
date: 2026-08-14 00:00:00 +0900
last_modified_at: 2026-09-15 09:42:42 +0900
translation_key: cts-sw-software-delivery-cost
korean_url: /2026/08/14/cts-sw-software-delivery-cost.html
permalink: /en/2026/08/14/cts-sw-software-delivery-cost.html
---

## TL;DR

- CTS-SW measures cost per unit of software delivered to customers.
- Keep cost scope and delivery-unit definitions stable within a team.
- Read cost alongside quality and unfinished work.

## Introduction

When a team adopts AI coding tools, it naturally starts with numbers that are easy to collect: coding time, autocomplete acceptance rate, and pull request count. A pull request, or PR, asks others to review and merge code changes.

These numbers show tool usage and code-generation speed. They do not tell us whether delivering a feature to customers has become cheaper.

Code may arrive quickly while reviews wait. Slow continuous integration (CI), which builds and tests changes automatically, or manual deployment can consume the time saved during generation.

In an earlier post, I argued for examining the **cost of realizing a requirement**, including models, tools, retries, and human review, rather than token prices alone.[^1] Amazon's Cost to Serve Software, or CTS-SW, offers a way to examine software delivery cost.[^2]

This post explains how to define and interpret CTS-SW. A companion post examines cognitive debt and review bottlenecks when people have less time to become familiar with context.[^5]

## 1. The cost of one unit delivered to customers

The basic calculation is simple.

```text
CTS-SW = cost to build and operate software during a period
         / software units delivered to customers during that period
```

Amazon connects input cost with delivered output without first allocating costs to every development activity. It then investigates which tools and practices are associated with changes in cost.[^2]

If exact cost is difficult to obtain, developer count and time can serve as a proxy. The result must then be expressed in developer time, not money.

Suppose eight developers produce 16 customer-facing deployments in one week. This is a hypothetical calculation example.

```text
8 developer-weeks / 16 deployments = 0.5 developer-weeks per deployment
8 developer-weeks / 20 deployments = 0.4 developer-weeks per deployment
```

Completing 20 deployments with the same people and time reduces input per deployment by 20%. A developer-week means one developer's time for one week.

For a monetary measure that includes tool fees, combine labor, tool and model charges, and operating costs in the same currency. Token charges cannot simply be added to developer-weeks.

Keep work on contracts, tests, and development tools—the harness—inside the agreed cost scope. Excluding it can make adoption look cheaper than it was.

## 2. Decide what counts as one unit

Defining **one software unit** is harder than doing the arithmetic.

Amazon describes deployments as a possible unit for service-oriented architectures and customer-delivered code changes as an alternative for large applications released together.[^2] A PR merged into a repository but not delivered to customers is not equivalent.

Agree on the following before measuring.

| Definition | An example agreement |
| --- | --- |
| Delivery unit | A production deployment serving customer traffic, or a change bundle customers can use |
| Completion point | Deployment, or the point when the feature becomes available to customers |
| Cost scope | Which development, review, testing, harness, and operating costs are included |
| Rework treatment | How to avoid counting a rollback and redeployment as new output |
| Comparison period | Equal-length periods, with changes in team composition and unit definitions recorded |

One deployment may contain ten features; another may change one setting. Deployment count does not directly measure customer value.

I therefore treat CTS-SW as a **delivery-cost measure**, separate from revenue or customer satisfaction. A lower number does not establish that the product has become more valuable.

Record changes in how work is split as well. Releasing the same feature in four deployments does not by itself make delivery four times more economical.

## 3. Read cost alongside other measures

Amazon uses CTS-SW together with measures such as security and resilience. A tension metric checks whether an important property is deteriorating while cost improves.[^4]

I also want to track **work that has started but has not reached customers**. The unfinished-work measures discussed here are my proposed companions to CTS-SW, not additions to its official formula.

| Question | What to examine |
| --- | --- |
| Is delivering one unit cheaper? | CTS-SW |
| Did we sacrifice quality? | Change failures, rollbacks, incidents, security, and recovery criteria |
| Is unfinished work accumulating? | Average work in progress, review waiting time, and old unfinished items |
| Does the output matter to customers? | Task success, actual usage, satisfaction, and other product goals |

If consistently defined CTS-SW falls while review queues and old work grow, the delivered units became cheaper, but the health of future delivery needs investigation.

Queue growth alone does not establish future cost increases or cognitive debt. A temporary large task, leave, or an external approval can also cause it. Treat it as a signal to examine what is waiting, where, and for how long.

Conversely, approvals can shrink a review queue while leaving gaps in the team's understanding. Distinguish increased approvals from increased customer-delivered output, and also check whether people can explain important changes and their failure conditions, alongside later rework.[^5]

Labor and model charges already spent on unfinished work belong in the agreed period cost. Adding an arbitrary inventory penalty could count the same cost twice. **Keep the CTS-SW formula and interpret it alongside unfinished work and quality.**

This month's costs may also include work delivered next month, while this month's output may include work started last month. That is another reason to examine several periods rather than judge an intervention from one week's movement.

## 4. Do not turn the metric into an individual output target

Rewarding deployment count can encourage meaningless deployments. Setting review-completion quotas can encourage approval without sufficient understanding.

DORA warns that delivery metrics used as targets or for competition can invite manipulation.[^6] SPACE likewise argues against reducing developer productivity to a single activity measure.[^3]

CTS-SW is better used to examine changes and their causes within one team. Ranking teams with different products, operating responsibilities, and software units starts from incompatible definitions.

Dividing it into individual scores is difficult too. A developer's coding speed does not determine delivery alone; testing environments, review practices, and deployment permissions also matter. Investigate a cost change before attributing it to someone's performance.

If I introduce CTS-SW, I want an explicit agreement that it will not be used for individual ratings, team rankings, or headcount cuts.

## 5. Start with consistent definitions in one team

Begin by defining the delivery unit, cost scope, and quality criteria in one team. Product can define what reaches customers; development and operations can connect costs and incident records.

Build a baseline from several recent weeks and check whether it roughly matches the team's experience. Record changes in definitions or team composition and distinguish comparable periods.

After introducing a tool or improving one bottleneck, inspect delivered volume, unfinished work, and quality alongside cost. If several things changed at once, do not attribute the outcome to one intervention.

If review queues grow, the next question needs to go beyond approving faster. Diagnose why work waits, then choose an intervention that reduces required human judgment or improves verification. The companion post explains how understanding cost and automation affect review bottlenecks.[^5]

## Conclusion

CTS-SW helps move the evaluation of AI beyond generated code toward what it costs to deliver results to customers.

Stable definitions, combined with quality, unfinished work, and customer value, make changes in the number easier to explain. I want to use it as a starting point for finding improvements within one team.

---

[^1]: [Why AI Adoption Should Not Start with Token Savings — The 3S Stages](/en/2026/06/15/organizational-ai-adoption-3s.html) — examines requirement-realization cost and organizational learning alongside tool usage.

[^2]: Amazon Science, [Measuring the effectiveness of software development tools and practices](https://www.amazon.science/blog/measuring-the-effectiveness-of-software-development-tools-and-practices) — defines CTS-SW, software units, cost proxies, and complementary quality measures.

[^3]: Nicole Forsgren and colleagues, [The SPACE of Developer Productivity](https://queue.acm.org/detail.cfm?id=3454124) — examines productivity across satisfaction, performance, activity, collaboration, and efficiency and flow.

[^4]: AWS Enterprise Strategy, [Business Value of Developer Experience Improvements: Amazon's 15.9% Breakthrough](https://aws.amazon.com/blogs/enterprise-strategy/business-value-of-developer-experience-improvements-amazons-15-9-breakthrough/) — describes cost proxies and tension metrics such as security and resilience.

[^5]: [Why AI Code Review Feels Harder — Context Familiarity and Cognitive Debt](/en/2026/08/18/ai-coding-review-cognitive-load.html) — examines compressed understanding time, unrecognized debt, human review effort, and automation.

[^6]: DORA, [DORA's software delivery performance metrics](https://dora.dev/guides/dora-metrics-four-keys/) — discusses problems with targets and comparisons across applications and teams.
