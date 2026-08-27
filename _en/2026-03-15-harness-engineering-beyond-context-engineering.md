---
layout: post
title: "Demystifying Harness Engineering"
excerpt: How short-cycle recovery keeps long-running agents on track
author: haandol
email: ldg55d@gmail.com
tags: ai agent harness-engineering context-engineering prompt-engineering agentic-development long-running-agent
publish: true
lang: en
date: 2026-03-15 00:00:00 +0900
translation_key: harness-engineering-beyond-context-engineering
korean_url: /2026/03/15/harness-engineering-beyond-context-engineering.html
permalink: /en/2026/03/15/harness-engineering-beyond-context-engineering.html
---

## TL;DR

- Can agents alone build and maintain production code at a scale of millions of lines? **Yes.** OpenAI[^4] and Anthropic[^6] have demonstrated it.
- **Context engineering** and **harness engineering** complement each other, with the harness extending control beyond context: context sets the broad direction, while the harness preserves it through automatic error recovery during every short execution cycle.
- If you do not intend to delegate the entire development process to agents, you do not need to adopt harness engineering yet.

## Introduction

Earlier posts discussed context engineering[^1] and how to embed business context in code.[^2]

The argument was that an agent operates more reliably when it receives good static context and the code itself explains the business clearly.

But once you run agents at production level, problems appear that context alone cannot solve.

An agent ignores lint rules, drifts away from architectural principles, or repeats a mistake that has already been corrected. You may have experienced unstable output even after providing a good prompt and strong context.

The emergence of always-on, long-running agent environments such as OpenClaw has made this problem more visible.

As agents begin working for hours or days across multiple context windows, small errors within one execution loop accumulate and repeatedly derail the overall direction.

Although AI adoption among most developers is still immature, harness engineering has rapidly become an important topic across the community.

In February 2026, Mitchell Hashimoto[^3] and OpenAI[^4] gave this area a name: **harness engineering**.

Anthropic later published an article on effective harnesses for long-running agents,[^6] helping form a broader industry consensus.

## 1. What is a harness?

A harness originally refers to the tack placed on a horse: equipment such as reins and a saddle that keeps the horse from running wherever it wants.

A harness for an AI agent serves the same purpose. It means **the entire environment that surrounds an agent and prevents it from wandering down the wrong path**.

Let us begin by clarifying what we can control. An agent is a combination of **context + LLM (model) + tools**. Of those three, **we cannot modify the model**. Whether it is GPT or Claude, we can choose the model, but we cannot open it up and change how it works internally. It is a fixed constant.

In other words, what we can actually manipulate is **everything except the model**: the context, the tools, and the environment in which they operate.

{% raw %}
```mermaid
flowchart LR
    subgraph AGENT["Agent"]
        direction TB
        CTX["Context — controllable"]
        LLM["Model (LLM) — fixed · cannot be modified"]
        TOOL["Tools — controllable"]
    end
    HAR["Harness<br/>Controls everything except the model"]
    HAR -. controls .-> CTX
    HAR -. controls .-> TOOL
    HAR -. cannot modify .-> LLM
    classDef fixed fill:#eee,stroke:#999,stroke-dasharray:4 3;
    classDef ctl fill:#ffe9c7,stroke:#e8973a;
    classDef har fill:#dce8ff,stroke:#46c,stroke-width:2px;
    class LLM fixed;
    class CTX,TOOL ctl;
    class HAR har;
```
{% endraw %}

A harness therefore does more than surround the "outside" of an agent. It fixes only the model and **actively manipulates the context and tools**. As we will see, feedback loops place validation results back into the context and verify them through tools, so the harness effectively operates the inside of the agent as well.

Look inside this harness and it ultimately comes down to two mechanisms: **feedback loops** and **guardrails**. Let us examine them one at a time.

### Feedback loops — "inspect the result, then retry if it is wrong"

A feedback loop is **a cycle that validates the agent's output and makes the agent retry on its own until the result meets the criteria**.

Instead of a person saying, "This is wrong, fix it," the system automates that role. It runs tests, lets the agent correct the code when they fail, runs them again, and repeats until they pass.

One property matters here: the feedback loop is **nondeterministic**. Even in the same situation, the agent may make a slightly different correction each time. This is the flexible but imprecise area where we delegate the instruction, "Decide whether this is correct and fix it yourself."

### Guardrails — "cross the line and the system blocks you"

Guardrails, by contrast, are **deterministic**. They define explicit rules and block anything that violates them.

A linter catches style violations, tests reject broken code, and Hooks block prohibited actions. Rather than asking the agent, "Please do it this way," guardrails build rails on both sides of the path so that **the work cannot pass unless it follows the rule**.

They are predictable automatic blocking mechanisms that produce the same result from the same input.

### They serve different roles

| Mechanism | Character | What it does | Example |
| --- | --- | --- | --- |
| Feedback loop | Nondeterministic · flexible | Validates the result and retries autonomously until it is correct | Run tests → revise after failure |
| Guardrail | Deterministic · strict | Automatically blocks rule violations | Linter · type check · Hooks |

Guardrails draw the lines the agent must not cross, while feedback loops refine the work within those lines until it is correct. Together, they form the environment surrounding the agent: the harness.

Placed into an actual workflow, the system operates like this.

{% raw %}
```mermaid
flowchart TB
    REQ["User request"] --> AGENT["Agent performs the task<br/>(context + LLM + tools)"]
    AGENT --> OUT["Task output"]
    OUT --> GR{"🛡️ Guardrails<br/>linters · tests · Hooks"}
    GR -->|Violation| BACK["Block → agent revises"]
    BACK --> AGENT
    GR -->|Pass| FB{"🔄 Feedback loop<br/>Does it satisfy the requirements?"}
    FB -->|No| BACK
    FB -->|Yes| DONE["✅ Complete"]
    classDef agent fill:#ffe9c7,stroke:#e8973a,stroke-width:2px;
    classDef guard fill:#d9f2e0,stroke:#3a9d5d;
    classDef loop fill:#dce8ff,stroke:#46c;
    classDef done fill:#d9f2e0,stroke:#3a9d5d;
    class AGENT agent;
    class GR guard;
    class FB loop;
    class DONE done;
```
{% endraw %}

The important point is that these mechanisms **leave the model fixed while validating and correcting everything else—the context, tools, and execution environment—at every step**.

Guardrails filter the output, and feedback loops place that result back into the context and run the agent again. The harness does not merely wrap the agent from a distance. It reaches inside and steers it. That is what a harness is.

## 2. The relationship between context engineering and harness engineering

The most intuitive way to understand the difference is along the **time axis**.

**Context engineering adjusts the broad direction.** It tells the agent what to do, which architecture to follow, and which business context governs its work.

System prompts, CLAUDE.md, documents retrieved through RAG, and memory all belong here. They give the agent **a destination and a route**.

**Harness engineering automatically recovers errors during short execution cycles, allowing the agent to complete a long-running task without drifting far from the broad direction.**

A linter catches a style violation and the agent immediately corrects it. CI reports a failed test and the agent fixes it automatically. A structural test detects an architectural violation and forces the agent to reverse course. These mechanisms are **safety systems that check the ground beneath every step**.

To use an analogy, context engineering hands you a map and route before a mountain climb, while harness engineering is the safety rope that catches you whenever you lose your footing along the way.

Without a map, you do not know where to go. Without a safety rope, one mistake can send you over a cliff. **The longer the task, the more valuable the safety rope becomes.**

{% raw %}
```mermaid
flowchart LR
    CTX["🗺️ Context engineering<br/>Once at task start<br/>Provides destination · route"]
    CTX -.broad direction.-> START(("Start"))
    START --> S1["Step"] --> S2["Step"] --> S3["Step"] --> GOAL(("Finish"))
    ROPE["🪢 Harness engineering<br/>Repeated at every step<br/>Recovers immediately after a misstep"]
    ROPE -.safety rope.-> S1
    ROPE -.-> S2
    ROPE -.-> S3
    classDef ctx fill:#ffe9c7,stroke:#e8973a;
    classDef harness fill:#dce8ff,stroke:#46c;
    class CTX ctx;
    class ROPE harness;
```
{% endraw %}

Anthropic's article on harness design for long-running agents[^6] emphasizes the same point.

When agents work across several context windows, **"compaction alone is not enough. Even with more capable models, high-level prompting is insufficient for producing production-ready results while cycling through multiple context windows."**

Every execution loop needs mechanisms that record state, detect failure, and recover automatically.

| Category | Primary role | Time axis | Design target |
| --- | --- | --- | --- |
| Context engineering | Adjust the broad direction | At task start | Every token visible to the LLM |
| Harness engineering | Automatic recovery in short cycles | Every execution loop | Guardrails and feedback loops, excluding the model |

Martin Fowler's summary[^5] likewise explains that **"context engineering helps the model think well, while harness engineering keeps the system from going off track."**

The practical issue is not the framing itself. It is the recognition that setting only the broad direction is not enough for a long-running task to reach completion.

### Ultimately, the question is how far we reduce human intervention

Why these two forms of engineering must work together becomes clear when we consider **the points where people intervene** in the development process.

People typically intervene in three places while turning a business requirement into code: **organizing the context for what to build**, **writing the code itself**, and **checking and correcting the result**.

Delegating work to an agent means removing human hands from these three points one by one.

{% raw %}
```mermaid
flowchart TB
    REQ["Business requirements"]
    REQ --> S1["① Organize context<br/>What to build · which rules to follow"]
    S1 --> S2["② Generate code<br/>Actual implementation"]
    S2 --> S3["③ Validate · revise<br/>Inspect and correct the result"]
    S3 --> CODE["Code"]
    CTX["Context engineering<br/>Reduces human work in ①"] -.-> S1
    HAR["Harness engineering<br/>Reduces human work in ③<br/>(and increasingly ②)"] -.-> S3
    classDef ctx fill:#ffe9c7,stroke:#e8973a;
    classDef har fill:#dce8ff,stroke:#46c;
    class CTX ctx;
    class HAR har;
```
{% endraw %}

**Context engineering reduces the human work in step ①.** Instead of a person repeatedly explaining, "Do it this way," the rules and context are placed in documents in advance.

**Harness engineering reduces the human work in step ③.** Instead of a person inspecting every result and saying, "This part is wrong, fix it," linters and tests validate the work automatically, and the agent corrects itself.

The important point is that **step ① must be established properly before we can remove the human from step ③**. The definition of correctness—the context—must be clear before we can build mechanisms that automatically catch errors—the harness.

The two are therefore not separate practices. They lie along **one progression that gradually reduces human intervention**. Context first reduces the hand that sets the direction. The harness then reduces the hand that validates the result. The process moves toward leaving people only with the act of "providing business requirements."

## 3. Why short-cycle automatic error recovery matters

Assume that context engineering has established the broad direction well.

During a 30-minute task, however, the agent generates code that violates a lint rule at minute 5. At minute 10, it builds more code on top of that violation. By minute 20, the original mistake has spread across the architecture.

At minute 30, the result points in the right direction, but the code is unusable.

{% raw %}
```mermaid
flowchart TB
    subgraph WO["Without a harness — mistakes accumulate"]
        direction TB
        W5["5 min<br/>One lint violation"] --> W10["10 min<br/>More code built on top"] --> W20["20 min<br/>Spreads into the architecture"] --> W30["30 min<br/>❌ Unusable code"]
    end
    subgraph WH["With a harness — every cycle recovers"]
        direction TB
        H5["5 min<br/>Violation occurs"] --> H5F["Detected · corrected immediately"] --> H10["10 min<br/>Continue from a clean state"] --> H30["30 min<br/>✅ Complete"]
    end
    classDef bad fill:#ffd9d9,stroke:#d44;
    classDef good fill:#d9f2e0,stroke:#3a9d5d;
    class W5,W10,W20,W30 bad;
    class H5,H5F,H10,H30 good;
```
{% endraw %}

**The problem is not the mistake itself, but the fact that it accumulates without being recovered.** This is the essential difficulty of long-running agents.

Anthropic's article[^6] compares the situation to **"an engineer arriving without any memory of the previous shift."** If an agent starting with a fresh context does not recognize earlier mistakes, it repeats them or builds more work on top of them.

The core of harness engineering is to **recover from this problem automatically during every short execution cycle**.

**The linter checks the code on every run.** When the agent generates code, the linter catches the violation immediately and returns failure feedback. The agent fixes it at minute 5, preventing the violation from accumulating through minutes 10 and 20.

**CI runs tests on every commit.** When the agent implements a feature, automated tests validate it immediately. If they fail, the agent attempts a correction automatically.

To support this, Anthropic proposes **limiting the agent to one feature at a time and requiring a git commit and progress summary at the end of every session**.[^6]

**Structural tests detect architectural violations.** Custom lint rules or architecture tests verify that the agent's output remains within the overall structure.

These three mechanisms ultimately form one short feedback loop. The agent produces an output, validation mechanisms immediately decide whether it passes, and a failure sends feedback back to the same point for another attempt.

{% raw %}
```mermaid
flowchart TB
    GEN["Agent generates code"] --> CHECK{"Validation<br/>linters · CI · structural tests"}
    CHECK -->|Fail| FIX["Failure feedback → immediate revision"]
    FIX --> GEN
    CHECK -->|Pass| NEXT["✅ Next step"]
    classDef loop fill:#dce8ff,stroke:#46c;
    classDef pass fill:#d9f2e0,stroke:#3a9d5d;
    class GEN,CHECK,FIX loop;
    class NEXT pass;
```
{% endraw %}

The shorter each loop is, the sooner it stops a mistake from accumulating. This is why "keep feedback loops short" is a core principle of the harness.

Mitchell Hashimoto summarized it in one sentence: **"When an agent makes a mistake, engineer the environment so the agent can never make that mistake again."**[^3]

The solution is mechanical enforcement, not hope. The more often that enforcement repeats in **short cycles**, the more likely the agent is to complete a long-running task without drifting from the broad direction.

## 4. What OpenAI and Anthropic demonstrated

In February 2026, OpenAI published the results of a five-month internal experiment.[^4]

A small team used only Codex agents to complete more than one million lines of production code, without manually writing any of it.

The engineers in this experiment did not spend their time writing code. They spent it **designing the harness**. OpenAI grouped the harness into three broad components.

1. **Context engineering**: Continuously improve the knowledge base inside the codebase and give agents access to dynamic context such as observability data and browser exploration.
2. **Architectural constraints**: Monitor the system not only with LLM-based agents, but also with deterministic custom linters and structural tests.
3. **Garbage collection**: Run agents periodically to find documentation drift and architectural violations, countering entropy and decay.

{% raw %}
```mermaid
flowchart TB
    OAI["OpenAI Codex experiment<br/>5 months · 1M lines · zero manually written code"]
    OAI --> C1["① Context engineering<br/>Improve knowledge base · access dynamic context"]
    OAI --> C2["② Architectural constraints<br/>Custom linters · structural tests"]
    OAI --> C3["③ Garbage collection<br/>Periodically detect drift · violations"]
    classDef root fill:#ffe9c7,stroke:#e8973a,stroke-width:2px;
    classDef comp fill:#dce8ff,stroke:#46c;
    class OAI root;
    class C1,C2,C3 comp;
```
{% endraw %}

Anthropic published harness-design principles for long-running agents in the same context.[^6] The central idea is a **two-part architecture**.

An initializer agent sets up the environment—`init.sh`, a progress file, and the initial commit—while a coding agent implements one feature at a time, incrementally. Every session records its state so the next session can understand the previous work quickly.

The conclusion is that **leaving a clear artifact and validating it after every short execution cycle** is what makes a long-running agent reliable.

{% raw %}
```mermaid
flowchart TB
    INIT["Initializer agent<br/>init.sh · progress file · initial commit"]
    INIT --> CODE["Coding agent"]
    subgraph SESSION["Coding agent — repeated sessions"]
        direction LR
        ONE["Implement only one feature"] --> VERIFY["Validate"] --> COMMIT["git commit + progress summary"]
    end
    CODE --> SESSION
    COMMIT -.next session understands previous work.-> ONE
    classDef init fill:#ffe9c7,stroke:#e8973a,stroke-width:2px;
    classDef sess fill:#dce8ff,stroke:#46c;
    class INIT init;
    class ONE,VERIFY,COMMIT sess;
```
{% endraw %}

Both articles ultimately emphasize the same point. Context should establish the broad direction, but an agent also needs **mechanisms that automatically detect and recover errors during every execution cycle** if it is to complete a long-running task.

## 5. The progression over time

The three concepts appeared in sequence because the way we use AI has changed.

{% raw %}
```mermaid
flowchart LR
    P["2023–2024<br/><b>Prompt engineering</b><br/>One-off questions and answers<br/>Optimize the instruction itself"]
    P --> C["2025<br/><b>Context engineering</b><br/>RAG · MCP · memory<br/>Design system-level context"]
    C --> H["Early 2026<br/><b>Harness engineering</b><br/>Feedback loops · guardrails<br/>Design an automatic error-recovery environment"]
    classDef era fill:#dce8ff,stroke:#46c;
    classDef latest fill:#ffe9c7,stroke:#e8973a,stroke-width:2px;
    class P,C era;
    class H latest;
```
{% endraw %}

The direction is consistent: **the target of control expands from "input text" to "the entire process in which the agent works."** As the model becomes more autonomous and works for longer, areas that input alone cannot control become visible.

**2023–2024, the era of prompt engineering.** The interaction consisted of sending ChatGPT one question and receiving one answer.

Assigning a role, providing step-by-step instructions, and including examples were enough to draw out the desired result. Because the model interaction was one-off, optimizing the instruction itself was central.

**2025, the rise of context engineering.** As agents appeared, it became important to design system-level context—including RAG, MCP, memory, and search results—rather than a single prompt.

The term spread widely after Andrej Karpathy described the shift "from prompt engineering to context engineering."

**Early 2026, the emergence of harness engineering.** As agents began performing more autonomous, longer-running, and broader tasks, the limits of controlling only the input became clear.

Mitchell Hashimoto first used the term "harness engineering" while sharing his AI adoption journey on February 5, 2026. One week later, OpenAI formalized it in a report on its Codex experiment. Anthropic then published its article on harness design for long-running agents.[^6]

The rise of always-on, long-running agent environments such as OpenClaw, NanoClaw, and NemoClaw is especially notable. They provide environments in which agents work autonomously for days without human intervention.

Most developers still use AI coding tools at roughly the level of autocomplete. The rapid emergence of these environments nevertheless shows where the industry is heading.

## 6. What this means in practice

The concrete practices of harness engineering are too broad to cover fully in this post. The central principle, however, is clear.

**Keep feedback loops short and automatic recovery fast.** This is the core of harness engineering.

When an agent makes a mistake, the system should discover it quickly, and the agent should be able to correct it as soon as it knows. The faster failure feedback arrives, the fewer errors accumulate and the less the agent drifts from the broad direction.

**Choose mechanical enforcement over hope.** Do not merely ask the agent, "Please do it this way." Build guardrails that make the work fail if it does not. Linters, tests, and Hooks serve this role.

**Fight entropy.** The more code an agent generates, the more consistency decays. The codebase needs a periodic process that finds architectural violations and mismatches between documentation and code.

**Set the direction with context and protect every step with the harness.** Without good context, the harness cannot tell the agent what it should do.

Without a good harness, context alone cannot keep the agent on track. Context owns the broad direction, while the harness owns the stability of every step.

## Conclusion

The overall direction I see in agent development is clear: **testing whether we can delegate to AI the entire process of translating business requirements into code**.

The attention around harness engineering and the flood of Claw environments such as OpenClaw, NanoClaw, and NemoClaw can be read as agreement with that direction from several different perspectives.

Context engineering tells the agent "where to go." Harness engineering lets it "get back up automatically when it falls along the way."

Only with mechanisms that catch and recover errors during every short execution cycle can an agent complete a long-running task without drifting from the broad direction.

Harness engineering is, of course, still at an early stage. The term itself has existed for only about a month, and the tools and methods continue to evolve.

But the fact that both OpenAI[^4] and Anthropic[^6] have begun addressing the importance of this area publicly means that the future of agents operating autonomously for long periods is already underway.

---

[^1]: [Context Engineering — Static Context and Dynamic Context](/en/2026/03/11/context-engineering-static-vs-dynamic.html).
[^2]: [The Value of Developers Who Understand the Business in the Age of Agentic Development](/en/2026/03/13/agentic-dev-business-aligned-code.html).
[^3]: [Mitchell Hashimoto — My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) (2026.02.05).
[^4]: [OpenAI — Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (2026.02.11).
[^5]: [Martin Fowler — Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) (2026.02.17).
[^6]: [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
