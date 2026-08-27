---
layout: post
title: "Agent-Driven Development, Demystified"
excerpt: A practical workflow for building software with agentic IDEs
author: haandol
email: ldg55d@gmail.com
tags: ai agent agent-driven-development agentic-ide cursor windsurf cline roo aider
publish: true
lang: en
date: 2025-02-10 00:00:00 +0900
translation_key: demystifying-agent-driven-development-process
korean_url: /2025/02/10/demystifying-agent-driven-development-process.html
permalink: /en/2025/02/10/demystifying-agent-driven-development-process.html
---

## TL;DR

- Use Cursor.
- Create specification documents and build each feature.
- Deploy.

## Introduction

At work, every AI coding assistant was blocked for security reasons, while only tools that were more distracting than helpful were allowed. I therefore stopped using AI assistants entirely for company work. Even for personal work, I was using only the Edits beta in GitHub Copilot.

Then I watched videos and read articles about development with Cursor and realized that the market had already begun adopting agent-based development methods.

After taking an old personal project[^1] back out, running it through several iterations, and implementing a chatbot, the ideas began to settle into a clearer shape in my head.

In this post, I will briefly introduce the best practices I have organized so far for agent-based development, which I will call **agent-driven development** from this point on. There is no single established name; it is described in many ways, including agentic dev workflow and agent dev process.

## Cursor vs. Others

The agent-driven development described below assumes the use of an agentic IDE. The first step is therefore choosing an agent-based IDE.

Representative agentic IDEs include Windsurf,[^2] Cursor,[^3] Aider, Roo, GitHub Copilot, Cline, and Amazon Q Developer.

There are many comparisons online, but unless spending $20 per month is genuinely impossible, choose either Windsurf or Cursor.

Personally, I think Windsurf places more emphasis on agent-based automation than on developer control—at least in the direction it is pursuing—while Cursor balances control and automation well.

To exaggerate slightly, if you want to create an MVP automatically and quickly, use Windsurf. If you want a tool you can keep using in production after the MVP, use Cursor.

I think Cursor is the IDE leading agent-based development. If you are a developer and have no particular reason to use another IDE, I recommend starting with Cursor.

The rest of this post explains the process in terms of Cursor's features.

> In practice, you eventually alternate among Claude Sonnet 3.5 (v2), Gemini 2.0 Pro, and o3-mini. If you want to choose whichever model you need while developing, it is cleaner to use Cursor than to subscribe to and configure everything separately. Give up coffee for a day or two, and you can spend the rest of the month focused on business logic.

## Best Practices for the Agent-Driven Development Process

Agent-driven development reverses responsibility for code generation. Instead of a person producing most of the code while AI acts as an assistant, AI produces most of the code while the user acts as the evaluator.

The **core problem** in agent-driven development is that it is difficult to **guide** an LLM to generate the code we want **reliably**. This assumes that the LLM has the capability to generate the desired code.

Many different methods have been proposed to overcome this problem. When the approaches currently recognized and shared as the most reliable are organized, they broadly follow this process:

1. Write a PRD (Product Requirements Document).
2. Set up the development environment.
3. Implement the PRD's technical requirements in sequence through Chat or Composer.
4. Connect a storage layer to the service.
5. Connect an authentication layer to the service.
6. Optionally improve the UI through a specialized service such as V0.[^4]
7. Deploy the service.

I will finish the post by explaining each step in a little more detail.

### 1. Write the PRD

Most development processes contain many variables, or ambiguities. Everyone knows that the speed and stability of later development depend on how many of those variables are turned into constants at the beginning. Agile, for example, can be understood as a process that turns roughly two weeks of project variables into constants at a time.

For an agent to carry out development, the distinction between variables and constants must be described clearly in natural language and delivered to it. We generally call those variables and constants requirements.

In the best-practice process, creating the requirements document that will later be given to the agent happens at the very beginning.

Many articles call this document a PRD and use their own document templates.[^5][^6]

An ordinary PRD defines requirements and criteria from a business perspective. A conventional PRD template therefore cannot be considered well suited to development.

More technical document forms, such as an ADR (Architecture Decision Record) or TSD (Technical Specification Document), are better suited to technical requirements. In real development, however, the business requirements in a PRD—including non-functional requirements—often turn out to be important as well.

We therefore need a document that includes the non-functional requirements normally organized in a PRD, the functional requirements found in a TSD, and the architecture decisions recorded in ADRs. If frontend development is included, it must also contain UI/UX information.

This PRD document has two main characteristics.

1. It is not created once and put away. It is updated continuously throughout development and changes along with the code. Agents generally handle these document updates as well, naturally keeping the document current.
2. It does not contain every piece of information in one document. Instead, additional documents are created whenever features are added, reflecting the structure of the code or team through units such as features or domains. The document-generation process therefore needs to be automated.

#### Automating Specification-Document Generation

Let us briefly examine how to automate the generation of specification documents, or PRDs.

The process usually looks like this:

1. Create the template to use, generally by organizing the required content in Markdown.
2. Complete the template conversationally with Claude Sonnet or GPT-4o.[^5]
3. Have a reasoning model such as o3-mini or o1 review the completed document, then revise it.

The third step is particularly important. Ask a reasoning model to identify, with explanations, the ambiguous points that could reduce a developer's productivity when using the document, and to explain what information needs to be added.

The reasoning model can fill in the content itself, but I did not see a large difference in quality when I used it only to identify what was missing, then passed that information as a prompt and improved the document conversationally with GPT-4o.

Likewise, if a detailed structured template is defined well, GPT-4o can produce a specification document close in quality to the output of o1. If you do not have a template, it is also useful to create one first with a model such as o3-mini.

Below is part of a template I often use when creating an MVP.

```markdown
## 2. MVP Goals and Key Metrics

### 2.1 Purpose

- Briefly describe the hypothesis or goals to be validated through this MVP.

**Example**

"If we provide a 30% discount coupon upon sign-up, the revisit rate within 14 days will increase."

### 2.2 Key Performance Indicators (KPIs)

- Define the quantitative metrics to evaluate the purpose (hypothesis) stated above.

**Example**

"Revisit rate within 14 days after sign-up: 30% or higher."
```

### 2. Set Up the Development Environment

The next step is to configure the development environment in which the actual code will be generated.

Many videos and articles create this environment directly.

Personally, however, if a specification document already exists, I think asking the agent to generate a README.md from that document is also a good approach.

```prompt
Read @SPEC.md and write a README.md file. It must include an Installation section.
```

Run the Installation instructions, revising them together with the specification document as needed. By the time the documentation is complete, the development environment will naturally be set up as well.

Most agentic IDEs are based on VS Code, so using a Dev Container is especially helpful. Installing a language from scratch or aligning versions takes more time and effort than expected, particularly when team members use a mixture of Windows, macOS, and Linux.

### 3. Implement

Implementation proceeds from the specification document, usually with a prompt like this:

```prompt
Implement section 6.4 of @SPEC.md.
```

As discussed at the beginning of this post, LLMs can generate most code. When they fail to produce the code we want—that is, when they fail to produce reliable code—it is because some required information was not provided or the requirements contain ambiguity.

API specifications are a representative example of required information. You can find the API documentation online in advance and include it in the specification, but Cursor's Docs feature can provide the desired online documentation to the LLM when it is needed.

For example, after registering documentation as shown below, Cursor reads the URL and stores its embeddings.

```prompt
@Add new doc https://daisyui.com/components/card/
```

Once registered, referring to that source automatically supplies its content to the prompt through RAG.

```prompt
Use the `@DaisyUI Card API` card component to build the product-list page.
```

If needed, you can also add the following to the specification document:

```prompt
Add to @SEC.md that section 6.4 should be implemented with DaisyUI's card component.
```

#### Align the Implementation Method with the SPEC Template

When this method is used for production-level development, incorporating the following elements into the template makes the implementation easier to test reliably.

1. Structure the document so that business requirements and technical requirements align.
2. Organize the technical-requirement sections vertically rather than by layer.
3. Divide the technical-requirement sections into detailed levels, such as user story → implementation task.

When the agent is responsible for most of the implementation, the document needs to make it easy to check and validate the agent's output in logical units.

It is therefore important to shift from thinking first about how to implement something to thinking first about how the implementation will be verified.

### 4 and 5. Connect Authentication and Storage

Services such as Supabase and Firebase, which provide both authentication and storage, are commonly used.

Even when an MVP does not use one of those two services, it generally favors a service where both authentication and storage can be used immediately with an `API_KEY`, without a provisioning process. Airtable is one example.

Authentication is implemented first because the usual frontend flow is to authenticate a user and then use the resulting auth information to connect infrastructure such as the storage layer behind it.

The basic configuration in each service's console must be completed by hand. The code integration, however, can be handled easily by giving the agent the relevant documentation through RAG—Cursor's Docs feature—and letting it implement the connection.

### 6. Optionally Improve the UI/UX with a Specialized Service Such as V0

Most agentic IDEs support multimodal input, so you can give an image directly to the agent and ask it to implement the UI.

Services such as V0, however, are trained on datasets more specialized for UI and produce much better results than requesting the same work directly from a general LLM.

One useful process is to give V0 a screenshot of a reference website, generate code that reflects its layout and look and feel, and then bring that code into the project.

Approaches for applying UI components through prompts are also being explored through sites such as 21st.dev.

### 7. Deploy the Service

A simple SPA MVP can be deployed conveniently to a service such as Vercel or Cloudflare.

Deploying a service with a backend to the cloud, however, has to be done manually. Just do it manually.

There are recent attempts to improve this part of the process. Google Project IDX[^7] is a representative example.

With Google Project IDX, you can develop a backend in a VS Code-based web IDE—similar to the old AWS Cloud9—and deploy the server to GCP Cloud Run with a few clicks through an integrated plugin.

## Conclusion

I think agent-driven development methods will continue to evolve throughout this year.

Each process introduced above is still at an early stage and has considerable room for improvement.

Just as services such as Tavily and SerpApi emerged because of LLM tool calling, I expect methods that help agents understand and access development documentation to advance as well—whether vendors make their API documentation more LLM-friendly, a separate service appears, or the capability is developed directly in the IDE.

---

[^1]: [EncBird](https://www.encbird.com)
[^2]: [Windsurf](https://codeium.com/windsurf)
[^3]: [Cursor](https://www.cursor.com/)
[^4]: [V0](https://v0.dev/)
[^5]: [Cursor PRD Crash Course](https://x.com/marioyordanov_/status/1875213900188143852)
[^6]: [Best Cursor Workflow That No One Talks About](https://www.youtube.com/watch?v=2PjmPU07KNs)
[^7]: [Google Project IDX](https://idx.dev/)
