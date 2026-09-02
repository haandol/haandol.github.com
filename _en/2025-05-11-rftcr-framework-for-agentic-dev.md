---
layout: post
title: "RFTCR — A New SDLC Framework for Agent-Driven Software Development"
excerpt: A five-stage SDLC for turning business requirements into code
author: haandol
email: ldg55d@gmail.com
tags: ai agent agent-driven-development agentic-ide cursor vibe-coding
publish: true
lang: en
date: 2025-05-11 00:00:00 +0900
translation_key: rftcr-framework-for-agentic-dev
korean_url: /2025/05/11/rftcr-framework-for-agentic-dev.html
permalink: /en/2025/05/11/rftcr-framework-for-agentic-dev.html
---

> **September 2026 update:** This post records the proposal as I understood it in 2025. I no longer keep every Requirement, Feature, and Task document as long-lived context. Before handoff, the ALPS PRD owns product intent and feature contracts. After handoff, ADRs become the implementation authority, while plans and task lists are regenerated when needed. The current approach is described in [Why Does a More Detailed PRD Become Outdated Faster? — Separating ALPS and ADR Boundaries](/en/2026/07/25/alps-adr-abstraction-boundaries.html).

## TL;DR

- The hardest part of agent-based development is **translating business requirements accurately into code**.
- The **RFTCR** (Requirement–Feature–Task–Code–Reflect) framework is the most effective framework known so far.
- As in the **C4 model**, the abstraction level of each stage's **inputs and outputs must be defined clearly** for the process to be reproducible.

## Introduction

As AI **agents** take on a larger role in software development, a paradigm of **agent-driven development** has emerged in which AI takes the lead in generating code and people evaluate the result.

In this approach, developers do not write most of the code directly. An **LLM**-based AI creates it, while the developer reviews and coordinates the work. Early practitioners, however, encounter a central problem: `it is difficult to guide AI to produce the code we want reliably`.

It is hard to obtain a perfect result from one or two prompts, and even slightly ambiguous requirements often send the AI in the wrong direction. Solving this problem requires guidelines that let the AI work through the problem stage by stage through Plan and Solve.

When the fragmented knowledge currently available is brought together, it naturally leads to a five-stage SDLC (Software Development Life Cycle) framework called **RFTCR**, which proceeds in the order **Requirement → Feature → Task → Code → Reflect**.

![RFTCR stages from Requirement to Code](/assets/img/2025/0511/rftc.png)

It is easy to find community posts recommending this sequence for working with agent-based IDEs, and a variety of supporting tools have also appeared.

RFTCR emerged from the search for a **best practice that gives agents clear guidance and produces the desired result without confusion**.

In this post, I will examine how each stage of the framework is carried out and why this structure is effective for agent-driven development.

## RFTCR Overview: Stages and Division of Roles

![RFTCR stages and role ownership](/assets/img/2025/0511/rftc-with-role.png)

The RFTCR process proceeds through **Requirement → Feature → Task → Code → Reflect**.

Two roles are involved in carrying out these stages: the **product owner, or planner**, and the **developer**.

- The planner defines *what* should be built from a business perspective.
- The developer is responsible for *how* it should be built from a technical perspective.

In RFTCR, the two collaborate by exchanging clearly defined **artifacts** at each stage. Collaboration between planners and developers is important in ordinary software development as well. In agent-driven development, however, the artifacts they produce become the AI agent's **prompts** and directly determine the quality of generated code, so the division of roles needs to be more systematic.

The role that leads differs by stage, but **both roles are involved to some degree in every stage**. In the Requirement stage, for example, the planner leads the documentation, but the developer also contributes through early technical review and feedback. Conversely, in the Code stage, the developer generates code with the agent, but the planner can adjust priorities from the broader product perspective or validate the outputs.

The central principle of RFTCR is therefore that **one role does not work unilaterally in a stage; even when one role leads, it still considers the other role's perspective**.

This reduces the chance of discovering requirement mismatches or technical problems late in the process and improves alignment between requirement fulfillment and technical implementation from the beginning.

In real organizations, a planner cannot call in a developer every time a plan needs technical validation. The tools used by the planner therefore need some ability to provide that technical validation.

We will now walk through the RFTCR stages in order and look more specifically at **what work** happens in each stage, **what artifacts** it produces, **what tool support** it requires, and how planners and developers collaborate.

### 1. Requirement

The first stage is to define the **requirements** clearly.

Led by the planner, the team writes the requirements for a product or feature in natural language.

These requirements include business goals, user stories, functional and non-functional requirements, constraints, and other relevant information.

#### Description

In agent-driven development, the requirements document serves as the **PRD (Product Requirements Document)** and is later given to the AI agent as its **guide**.

In my experience, the specificity of the initial requirements has a major effect on the speed and direction of later development.

The key is turning as many uncertain elements—variables—as possible into things that are clearly defined like constants. The RFTCR process should devote sufficient time to this stage.

Well-defined requirements reduce opportunities for the AI to become confused in later stages and also reduce the burden of communication between people.

#### Deliverable

The main **deliverable** of this stage is a structured **requirements specification, or PRD**. It can be seen as a document one step beyond an ordinary PRD: a comprehensive specification that includes not only business requirements but also major **technical requirements from the TSD** and **architecture decisions from ADRs**.

The reason for doing this is to give the agent enough context to reduce unnecessary questions and confusion when code is generated later. If the product includes several areas such as frontend and backend, UI/UX requirements should also be included so that as much development information as possible is specified in advance.

Another important aspect of the Requirement stage is **standardization of the deliverable**.

To apply RFTCR, the format and level of detail in the PRD must follow a consistent standard.

Each requirement should have a clearly marked identifier, priority, acceptance criteria, and other required fields. The sentences themselves should be concrete and free of ambiguity.

Otherwise, AI and people will become confused in later stages, such as when deriving the feature list.

If the deliverable from this stage differs completely from person to person, it becomes difficult to provide the agent with the right prompt, and the results will inevitably be inconsistent.

Just as the **C4 model** standardizes the content and scope of architecture diagrams at each level to make team communication easier, RFTCR's requirement deliverable should follow a consistent abstraction level and format.

The goal of this stage is to make the specification the team's **common language**—or, in DDD terms, its ubiquitous language—when work moves into the next stage of feature design.

#### Tool Support

An AI-based **PRD-writing assistant**[^1] is extremely useful during the Requirement stage.

For example, an agent-based tool can ask questions automatically, elicit requirements that the planner had not considered, and complete the document according to a predefined template.

PRDs generally suffer from two problems: **not knowing which questions to ask** and **not knowing how much detail is enough**. Naturally, the quality of the result also varies too widely with the author's ability.

With an AI-based PRD-writing tool, the AI becomes the author of the document and the user answers its questions. This **reversal of responsibility** reduces dependence on the author's ability and makes it possible to generate documents at a consistent level.

Fixing the document template also makes the completion criteria explicit and reduces variation in quality caused by the author's level of experience.

A tool such as a **PRD Writer** therefore gives the planner systematic guidance and gives the developer consistently structured requirements that make the later stages easier.

The agent in a PRD-writing tool can also incorporate part of a developer's perspective, which helps preserve a minimum level of quality and consistency even when the planner has little technical background.

### 2. Feature

The second stage groups and designs the selected requirements as **features that can be implemented**.

This stage is where the planner and developer meet and collaborate.

#### Description

While reviewing the requirements specification, the team groups related requirements into a **feature** or **module** and derives a high-level **design** for each feature.

Here, design does not mean detailed code design. It means defining the **components and behavioral flow** required to satisfy the feature.

As if describing the system at the level of an epic or user story, the team explains what each feature does and roughly how it will operate.

This creates an **intermediate bridge** between requirements and implementation.

#### Deliverable

The main deliverable is a **feature specification** or **technical specification** for each feature.

If the PRD created in the Requirement stage is the high-level document for the entire project, the Feature stage breaks it down into **multiple lower-level documents**.

In real projects, it is also more efficient to manage extensive requirements across documents divided by domain or feature rather than putting everything into a single document.

In the RFTCR process, this **division** occurs during the transition from *Requirement to Feature*. Each feature document becomes a blueprint for implementing a particular set of requirements.

For example, a feature called "User Registration" includes every requirement related to that feature, such as support for registration by email and compliance with a password policy. It can also contain design information such as screen flows, an API outline, and a data model for satisfying those requirements.

> Personally, I think one of the most important elements is a vertically sliced feature specification. Each feature specification is later converted into work. To make it usable across different team topologies, a vertical feature specification is more useful than a horizontal, layer-based one. The goal is to support both organizations divided into frontend and backend teams and autonomous structures such as two-pizza teams.

#### Tool Support

The Feature stage can use a **feature-design assistant** or **automatic specification generator**.

Given a requirements document, AI can cluster related requirements, propose a feature list, and draft a design for each feature.

The earlier process of dividing one PRD into multiple documents can also be **automated** with an agent.

It is recommended that an agent create a new specification document whenever a feature is added and keep that document up to date.

One possible approach is to generate feature documents from a template, use an AI **reasoning model** to review ambiguous sections, and then improve them.

In short, a **Feature-stage tool** takes requirements as input and produces standardized feature designs, giving the developer a foundation from which an implementation plan can be created immediately.

For the planner, such a tool makes the mapping from requirements to implementable features transparent. For the developer, it provides structured material from which tasks can be derived.

The core of the Feature stage is **restructuring requirements from the perspective of implementation**.

Each feature design should be neither too abstract nor too detailed.

Its abstraction level is sufficient when the feature can be **understood independently** and the team can **decide whether to begin development**.

If this stage is skipped and the process moves directly from requirements to tasks, tasks emerge in a scattered form, making it difficult to set development priorities or understand the scope of impact.

Structuring the work once at the feature level makes it possible to discuss which feature should be developed first and what dependencies exist between features. It also lets the agent focus on one feature at a time.

This is similar to drawing the **Container level** in the C4 model before beginning component work: establish the broad picture, then divide it into detailed work.

### 3. Task

This stage derives the **detailed tasks** required to implement each feature.

From this point, the developer takes the lead. It is recommended that the planner participate only in a supporting role or not participate at all.

#### Description

Based on the feature specification, the developer turns the question "What work must be performed to build this feature?" into a concrete list of work.

Tasks are generally a **developer-oriented to-do list**. Ideally, each task is divided into a small unit such as implementing one function, making one database change, or building one screen.

The reason for this division is to let an AI agent **handle one task at a time**, minimizing the blast radius when an error occurs.

Isolating work into small units limits the impact of failures and makes debugging easier, which improves system stability.

A well-designed system limits the **blast radius** so that a failure has only a localized effect. If we map a failure to an AI malfunction, RFTCR's task decomposition can be understood in the same way.

#### Deliverable

The main deliverable is an organized **task list**.

The list includes priority, estimated difficulty, the assignee—person or agent—and mappings to the detailed requirements or design elements that each task must reference.

Within a "Develop User Registration API" feature, for example, tasks might include "Create a user table in the database," "Implement the registration API endpoint," and "Add input-validation logic." A feature can be expressed as one or more user stories, in which case the hierarchy becomes *Feature → User Story → Task*.

Each task should be written to be as **independently executable** as possible. Doing so requires understanding the dependencies between tasks.

Only when those dependencies are known can work proceed in parallel or sequentially without significant interference.

#### Tool Support

The Task stage can use a **Task Manager** or **AI task-planning** tool.

Such a tool can take a feature specification and automatically generate detailed work, or understand a task list written by a developer and format it so that an agent can execute the next stage more easily.

A specialized agent such as `Claude TaskMaster` is one example.

This Task Manager agent can use a CoT (Chain-of-Thought) approach to output what should happen first and what should follow, or display the **dependencies** among the generated tasks.

The important points in the Task stage are **decomposition and ordering**.

If tasks are not divided appropriately, the AI attempts too much at once during coding, increasing the probability of errors.

If they are divided too finely, however, the overall context becomes fragmented and efficiency falls.

In my experience, an appropriate size is enough to create one PR or one commit for one feature at a time.

The **agent workflow** must then be designed by determining the order among tasks.

For example, the task that sets up the database schema should precede the task that implements the API, while UI development should follow completion of the API.

This order can be stated explicitly when instructing the AI, or a TaskMaster agent can manage the task-processing order automatically.

Because this Task stage is led by the developer and closely connected to the code, it is most effective when provided through an agent-based IDE such as Cursor in the form of MCP.

Claude TaskMaster itself maximizes developer convenience by making a CLI tool available through MCP.

### 4. Code

The fourth stage is the actual **code implementation** stage.

Led by the developer, the team writes code by processing the previously defined tasks one at a time.

#### Description

Here, the "developer" can be seen as a **hybrid of a human developer and an AI coding agent**.

The role of the Code stage in RFTCR is similar to coding in conventional development. In the context of **agent-driven development**, however, the AI generates the code while the developer reviews and modifies it.

For each task, the developer gives the AI a prompt containing context and instructions and **requests code generation**. The developer then reviews the AI's code and either modifies it or prompts again when necessary.

The well-prepared artifacts from the earlier stages—the PRD, feature design, and task definition—provide accurate context to the AI and help it produce correct code from the beginning whenever possible.

#### Deliverable

The main deliverable is, quite literally, **source code**.

Code is written for each implemented feature and committed to a version-control system such as git.

The agent-development process as a whole has two purposes: making agent-generated output become *more trustworthy code*, and reducing the risk when an agent modifies incorrect code.

An agent receives two broad kinds of context as input: static and dynamic.

Static context, such as API specifications, data models, and business rules, is already provided sufficiently by the artifacts from earlier stages. This reduces the room for the AI to exercise inaccurate imagination and guides it during debugging so that it neither examines nor modifies unrelated code.

When implementing a "User Registration API Endpoint" task, for example, the AI can write the code immediately according to the instructions if the earlier feature design specifies the email-duplication check and password-hashing method. It also becomes less likely to modify or refer to code related to a "Change Password API."

Without such a specification, the AI must either implement from guesswork or read the entire codebase before deciding which parts are relevant. As the context grows longer, the probability that it forgets earlier information and malfunctions also increases.

It is therefore no exaggeration to say that **careful preparation before the Code stage** determines the efficiency and accuracy of the Code stage.

#### Tool Support

The Code stage depends heavily on an **agentic IDE** or **code-generation agent**.

The previously mentioned Cursor, Windsurf, and many other agent-development tools fall into this category.

Within an IDE, these tools generate code instead of, or alongside, the developer. They accept modification requests conversationally and refer to external documentation when necessary.

In an agentic IDE such as Cursor, for example, major pieces of static context such as PRDs and Rules can be registered in advance. The developer can then use the agent feature to say, "Implement the next task," and have the AI write the relevant code.

The developer reads the generated code, reviews its logic and style, and improves missing parts through additional prompts or direct edits.

**Version-control integration** is also important in the Code stage. When an agent makes too many changes at once and those changes are wrong, git should provide checkpoints to which the developer can return.

The essential point is that even when a tool provides automation, **the developer retains the final decision**.

The developer decides whether to accept an agent's code proposal and which parts to modify, while the planner focuses on confirming that the result satisfies the requirements.

Because agents can also help developers understand code, the ideal goal is to keep any code the developer does not understand out of the codebase.

What matters in the Code stage is **stability and consistency**. When implementing one task defined in the earlier stage, code outside that scope should not be changed.

While carrying out a "Create User Table" task, for example, the agent should not make changes that affect unrelated tables.

This naturally leads to a **one task–one commit** principle. Prompts must be constructed carefully so that the agent does not go beyond that scope.

If the principle is followed, the **blast radius** remains small when a bug or problem occurs, reducing the time required to resolve it.

Code style and architecture decisions must also be applied consistently throughout the project. If an agent generates inconsistent code, it will generate erroneous code more often.

In practice, agentic IDEs usually have linting enabled, and agents generally try to fix lint errors whenever possible.

Coding standards and architecture principles can therefore be provided to the agent as **rules**, such as "Follow the repository pattern" or "Keep business logic to a minimum in controllers."

The Code stage is ultimately **where every other RFTCR stage comes together and bears fruit**. Its goal is to provide the agent with well-abstracted static and dynamic context with minimal duplication so that the agent can produce code reliably.

### 5. Reflect

The fifth and final stage is **Reflect**.

This is the process of updating all static and dynamic context based on the development process and the generated code.

By keeping every piece of context current, the ideal goal is to maintain a blueprint—the context—in the codebase that can reproduce the current business logic, rather than merely individual units of code.

#### Tool Support

This process is also carried out through an agent, and tools such as Cline Memory Bank are useful.

## Conclusion

Agent-driven development is opening a new frontier in software engineering.

No matter how innovative the **active participation** of AI agents may be, however, guiding them remains a **human responsibility**. The RFTCR framework serves as a **process** through which people—the planner and developer—control AI effectively and collaborate with it.

By providing five stages of **clear guardrails** from requirements to code, we can draw out AI's creativity in a controllable form and obtain code that accurately realizes business value.

As the artifacts from each stage become standardized and accumulate, the process will become **faster and more robust with repetition**.

RFTCR may initially face obstacles such as establishing a team culture and a lack of tool support.

But as Agile and DevOps did, once its effects are felt, it will bring improvements in productivity and quality stability that make it difficult to return to the old way.

What matters is **a combination of the right tools at the right abstraction levels** and **a working method agreed upon by the team**.

With those elements in place, the RFTCR process will make software development in the age of agents more **standardized, predictable, and collaborative**.

---

[^1]: [ALPS Writer](https://github.com/haandol/alps-writer)
