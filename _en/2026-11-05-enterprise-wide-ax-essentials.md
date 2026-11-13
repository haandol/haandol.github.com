---
layout: post
title: "Why Enterprise AX Needs Reusable Solutions and Business Models"
excerpt: Building enterprise AX on reusable solutions and business models
author: haandol
email: ldg55d@gmail.com
tags: ai agent ax ddd platform organization software-factory knowledge harness-engineering
publish: true
published: true
date: 2026-11-05 14:30:00 +0900
last_modified_at: 2026-11-13 20:11:15 +0900
lang: en
translation_key: enterprise-wide-ax-essentials
korean_url: /2026/11/05/enterprise-wide-ax-essentials.html
permalink: /en/2026/11/05/enterprise-wide-ax-essentials.html
---

## TL;DR

- Enterprise AX should be built on reusable solutions.
- Business models keep business language and implementation consistent.
- Business changes should flow into agent-led implementation, verification, and improvement.

## Introduction

AX (Agentic Transformation)—moving business work to agent-based systems—requires data connections, access controls, business knowledge, evaluation, and ongoing operations. When each team builds these capabilities from scratch, it repeats the setup work, and later changes can remain dependent on the technical specialists who built the first version.

**Enterprise AX should be built on reusable solutions while keeping the customer's business and its implementation aligned in meaning.** Products and shared platforms provide recurring capabilities, with customer-specific business rules and processes configured on top.

In traditional software development, business processes were often recast to fit resource limits or technologies and structures familiar to the development team. If this changed their meaning or flow, business teams discussed the original work while developers answered in terms of the implemented system. Different interpretations of the same work made recurring conflicts likely.

Reducing this conflict requires the business language and rules agreed by business and development teams to remain intact in the implementation. **Keeping business models and implementation aligned in meaning**, a core principle of DDD (Domain-Driven Design), fits AX's aim of connecting business experts' intent to agent execution. This article borrows that perspective for AX design without requiring adoption of the entire methodology.

Agent-based business automation and self-improving agents can help put this model into practice and maintain it. When a domain expert who understands the rules and exceptions recognizes a business change and requests an update, agents should revise the workflow against the same business model. A Software Factory carries the necessary code through implementation, verification, and delivery.

This post describes the solutions that support this flow and the organizational responsibilities needed for domain experts to lead changes.

## 1. Business meaning and bounded contexts

### When technical structure changes the business process

Suppose the business rule is: “Refund orders canceled before shipping, and mark the refund complete when the return of funds is confirmed.” A layered architecture can separate request handling (Controller), coordination (Service), and data storage (Repository).

Problems arise if deadlines, shared-code reuse, and an existing database schema take priority: cancellation and refund are collapsed into one “done” state, while the actual refund is deferred to a batch job. The code has finished updating a status, but the business has not yet finished returning the customer's money.

{% raw %}
```mermaid
flowchart TB
  subgraph B["Business process"]
    direction LR
    B1["Cancel before shipping"] --> B2["Issue refund"] --> B3["Confirm returned funds<br/>Refund complete"]
  end
  subgraph T["Technical convenience first"]
    direction TB
    T1["Controller<br/>Check shipping state"] --> T2["Shared Service<br/>updateStatus(9)"]
    T2 --> T3["Repository<br/>9 = cancellation done<br/>and refund done"]
    T3 --> T4["RefundBatch<br/>Return funds later"]
  end
  subgraph D["Business meaning preserved"]
    direction TB
    D1["Order.cancel()<br/>Check cancellation rules"] --> D2["Refund.request()<br/>Refund in progress"]
    D2 --> D3["Refund.complete()<br/>Confirm returned funds"]
  end
  B -.->|"Technical structure first"| T
  B -.->|"Model the business rules"| D
  classDef mismatch fill:#fde8e8,stroke:#b52d36,color:#821d25
  classDef aligned fill:#e9f6ec,stroke:#3c7754,color:#23452b
  class T3 mismatch
  class D3 aligned
```
{% endraw %}

Changing the “refund completed” rule in this structure requires piecing it together from Controller checks, Service updates, database values, and batch timing.

Treat “cancellation confirmed” and “refund completed” as distinct business concepts, with their conditions enforced in code. `Refund.complete()` must use confirmation of returned funds as its completion criterion; updating a shared status value is not sufficient.

A layered architecture can still **give the domain model responsibility for business meaning and rules, while APIs, databases, and batch jobs perform the technical work needed to carry out its decisions**. Clear ownership of the business criteria helps preserve their meaning when implementation technology changes.

### Defining boundaries of business meaning

Keeping cancellation and refund rules distinct also requires defining each business model's scope of responsibility.

**A bounded context (BC) is the scope within which a business model's terms and rules have consistent meanings.** Ordering and payments have separate boundaries, with business meaning and implementation kept aligned inside each.

{% raw %}
```mermaid
flowchart LR
  subgraph O["Ordering BC"]
    direction TB
    OR["Order and cancellation rules"] --> OC["Ordering model and code"]
  end
  subgraph P["Payments BC"]
    direction TB
    PR["Payment and refund rules"] --> PC["Payments model and code"]
  end
  O -->|"Cancellation event"| P
```
{% endraw %}

The payments BC handles an order-cancellation event according to its own approval and refund rules. Contracts between BCs define what information is exchanged and what it means, keeping order cancellation distinct from refund completion.

Organizational and service responsibilities should reflect these boundaries. Several services may implement one BC; the BC defines a boundary of business meaning. For more on terminology and context boundaries, see [Notes for DDD beginners](/2021/10/11/thoughts-for-ddd-starters.html) (Korean).

## 2. Connecting solutions to introduce AX

An organization introducing AX can start with these five steps. After the initial build, domain experts' change requests should enter the same flow and lead to system improvements.

{% raw %}
```mermaid
flowchart TB
  K["1. Shared knowledge"] --> P["2. Process analysis"]
  U["Domain expert"] -->|"Business change request"| P
  P --> R["3. Requirements"]
  R --> A["4. Automation design"]
  A --> D{"Existing capabilities enough?"}
  D -->|"Yes"| E["Execute and verify"]
  D -->|"Implementation needed"| F["5. Software Factory"]
  F --> E
  E --> V["Business review"]
  V -.->|"Update knowledge"| K
  V -.->|"Improve process"| P
```
{% endraw %}

Existing solutions provide the common capabilities at each step. Teams configure the rules and connections for their business. If the automation design needs a missing capability, the Software Factory implements it before it is used in execution.

| Step | Role | Result |
| --- | --- | --- |
| 1. Shared knowledge | Prepare business and implementation knowledge and access | Knowledge with traceable evidence |
| 2. Process analysis | Analyze current and target work and responsibility | Target processes and transformation candidates |
| 3. Requirements | Agree on business rules and success criteria | Criteria for implementation and verification |
| 4. Business automation | Configure and test existing agents and tools | An execution flow and any missing capabilities |
| 5. Software development | Implement and verify missing capabilities | Code and tools for automation |

A team that has already mapped processes with business experts can use that work to identify the data it needs. Automating process analysis itself requires readable sources and access first. Either way, shared knowledge is difficult to postpone.

### How AWS and Palantir FDEs build on reusable solutions

An FDE (Forward Deployed Engineer) works inside a customer or business team to build systems with them. Public AWS and Palantir materials describe how customer-specific work is implemented on shared technical foundations.

AWS describes deploying a semantic layer connecting business meaning to data in the customer's account and letting agents use a governed, versioned knowledge graph. The graph, runbooks, and architecture documentation remain with the customer, with customer engineers progressing from co-builders to independent operators.[^1]

Its partner guidance identifies a reusable **harness** of business knowledge, tools, and checks. Partners accumulate ontologies, evaluation frameworks, external-tool connections, agent operations capabilities, and design records for use in later engagements.[^2]

Palantir provides Foundry for data and business models, AIP for agents and AI workflows, and Apollo for deployment and infrastructure. FDEs work with customers to build capabilities on this foundation.[^3] The Ontology at its center connects business objects and relationships with actions and functions, carrying business meaning into executable logic.[^4]

The common pattern is **combining a reusable technical foundation with each customer's business model**. Using shared capabilities still requires a design that preserves the meaning of customer-specific rules in both the model and implementation.

## 3. Shared knowledge for business and coding agents

AX requires agents to find not only business documents but also relationships between processes and implementation knowledge spread across repositories and services. Shared knowledge provides the context management foundation for retrieving the information each task needs.

The required capabilities include RAG (Retrieval-Augmented Generation), which uses retrieved information in model responses or work; graph traversal, which follows relationships; and ontology retrieval, which finds business concepts and rules. **Both business agents and coding agents need access to all three capabilities.**

{% raw %}
```mermaid
flowchart LR
  P["Check permissions<br/>Set search scope"]
  subgraph K["3 retrieval methods"]
    direction TB
    R["Document RAG<br/>Similarity + BM25"]
    G["Graph traversal<br/>Relations · dependencies"]
    O["Ontology retrieval<br/>Meaning · rules"]
  end
  P --> R
  P --> G
  P --> O
  R --> C["Task context"]
  G --> C
  O --> C
  subgraph U["2 agent types"]
    B["Business agents<br/>Knowledge · rules"]
    D["Coding agents<br/>Business + implementation<br/>Repos · projects<br/>Service relationships"]
  end
  C --> B
  C --> D
```
{% endraw %}

### Three ways to retrieve knowledge

**Document retrieval and RAG** find evidence in business documents, meeting notes, and design records and use it in a task. Hybrid retrieval combines similarity search with BM25, which ranks documents by matching terms. This covers both different expressions of the same meaning, such as “I want my money back” and “refund request,” and exact terms such as product codes.

**Graph traversal** follows recorded relationships to find connected entities. Following events passed between refund processes, service calls made by a payment service, or dependencies between repositories helps identify where a change may have an effect.

**Ontology retrieval** finds the business meaning of concepts and relationships, along with applicable rules and exceptions. It makes explicit what “cancellation completed” in ordering and “refund completed” in payments mean and when each holds, so agents do not have to reconstruct the business criteria from document fragments each time.

These capabilities work together. Graph traversal provides a way to follow connections, while an ontology defines what those connections and concepts mean. Information retrieved from a graph or ontology can also feed RAG.

### Serving two types of agents

**Business agents** primarily need business knowledge and rules. To handle a refund request, they must read customer and order state, approval conditions, processing steps, and exceptions to determine which actions the business permits.

**Coding agents** need those same business criteria plus the knowledge required to implement them. They need to know which project's repositories to change, how services connect through APIs and events, and which contracts and tests must hold. Searching code within one repository is insufficient for changes spanning projects and services.

The two consumers should not be isolated into separate knowledge systems. They should share business concepts and rules while retrieving the scope relevant to their work. Business agents may need service relationships, and coding agents must also consult the ontology for business meaning.

The shared knowledge platform manages ownership, provenance, versions, and permitted use, applying role- and business-scope access controls before retrieval. Business teams decide the meaning and permitted use of rules; platform teams ensure those decisions govern actual access by agents and external services.

### Navigating business knowledge in layers

Ontology retrieval does not require a graph database. Business knowledge can be written in a text format such as Turtle, with routes from an overview into the required detail.

First show each BC's responsibilities and core work. Agents can then find rules and exceptions inside relevant BCs. Retrieval can work without every internal relationship being complete, provided BC membership and paths into the details are established.

When agents can read an overview and decide where to look next, they can narrow the scope before reading details instead of taking in material from across the enterprise at once. Retrieving details only from relevant areas reduces unrelated context as business knowledge grows. The saving is in how much information agents must read, rather than storage retrieval time.

For this to work, each overview must be accurate enough to guide the next retrieval step. Exceptions omitted from an overview must still be available in detailed rules and original sources.

This 3D view in the [ontology tool](https://github.com/haandol/alps-writer-plugins) shows the “Expression dictionary” BC of [EncBird](https://www.encbird.com), an English learning service. It shows how expression registration, expansion, and dictionary management relate to conversations, podcasts, and review.[^5]

![3D ontology view of EncBird's expression dictionary processes and their connections](/assets/img/2026/1105/encbird-ontology-3d-en.png)

This information provides **a bird's-eye view of where the current work sits in the overall learning process and how it connects to other work**. Just as a person explores relationships in the 3D view, an agent can read the processes and conditions in the same model to understand what comes before and after.

Suppose the request is, “Make it easier to register expressions from a podcast.” The agent can follow the relationships from collecting suggested expressions through learner selection and registration checks to review and learning-activity records.

That reveals concrete considerations: whether registration still requires the learner's approval, whether an already registered expression is charged again, and whether successful registration feeds review and learning records. Starting with the overall relationships narrows the scope before the agent reads each process's rules and exceptions, making the relevant conditions easier to identify.

### Separating business meaning from implementation responsibilities

Business models hold process purpose, participants, conditions, and exceptions. Choices of database, API, and framework belong in the implementation. The purpose of this separation is to **contain implementation changes so that replacing technical details does not require changing domain logic**.

As in [Clean and Hexagonal Architecture](/2022/02/13/demystifying-hexgagonal-architecture.html) (Korean), define the operations and results the business needs through interfaces, and isolate connections to specific databases or external APIs in adapters. The concrete implementation depends on interfaces defined on the business side, so the business model does not need to know external technology formats.

The diagram shows **two kinds of change moving through the same business model, contracts, and implementation**. Blue arrows carry business criteria into implementation; orange arrows trace a technical replacement and verification against the existing contract. Technical replacements that preserve that contract should not propagate into changes to domain rules.

{% raw %}
```mermaid
flowchart TB
  M["Business model<br/>Domain rules"]
  P["Business contract<br/>Interfaces · verification"]
  I["Implementation<br/>Code · adapters"]
  T["Technical replacement<br/>DB · API · framework"]
  M -->|"Rule change"| P
  P -->|"Update implementation"| I
  T -->|"Replace"| I
  I -.->|"Verify the contract"| P
  P --x|"Block technical impact"| M
  linkStyle 0,1 stroke:#336fa1,stroke-width:2px
  linkStyle 2,3 stroke:#b87720,stroke-width:2px
  linkStyle 4 stroke:#af3943,stroke-width:2px
```
{% endraw %}

For example, if only the refund API's response field names or the database storage format changes, revise the adapter so that it still provides the same confirmation of returned funds. Keep the business rule in `Refund.complete()` unchanged and verify that the replacement implementation satisfies the existing contract.

Record interface boundaries, implementation choices, and verification criteria in ADRs (Architecture Decision Records). ADRs preserve the reasoning behind those choices; interfaces and adapters in the code contain the changes.

Agent work must follow the same boundaries. Execution configuration must identify which BC's rules to read, which tools and permissions to use, and which results to pass to other BCs. One agent can handle several BCs while preserving the decision criteria of each.

## 4. Connecting process analysis to automation and implementation

With shared knowledge in place, a business change can be developed into requirements and an executable workflow. When a capability is missing, coding agents in the Software Factory implement it.

{% raw %}
```mermaid
sequenceDiagram
  actor O as Domain expert
  participant B as Business agent
  participant K as Shared knowledge
  participant C as Coding agent
  O->>B: Business change request
  B->>K: Retrieve rules and exceptions
  K-->>B: Decision and verification criteria
  B->>B: Define target flow and requirements
  opt Implementation needed
    B->>C: Missing capability and business criteria
    C->>K: Retrieve repo and service relationships
    K-->>C: Implementation context and dependencies
    C->>C: Implement and test
    C-->>B: Verified code and tools
  end
  B->>B: Configure and verify automation
  B-->>O: Results and verification evidence
```
{% endraw %}

### Finding current and target work

Use shared sources and business-expert explanations to understand the current process (As-Is) and design the target process for agents (To-Be). Approaches such as agent storming or [Event Storming](/2020/12/10/demystifying-event-storming.html) (Korean) collect events, rules, and exceptions and identify who owns outcomes and changes.

For refunds, examine how support intake, order-team delivery checks, and finance approval connect. If every case waits for a person to approve it, faster tools still leave that wait in place. The target process must include the conditions and authority for agents to act and the exceptions people retain.

### Turning a change request into verifiable requirements

Suppose a domain expert asks, “Refund orders canceled before shipping without separate approval.” The agent uses the shared model's meanings of shipping, cancellation, approval, and refund to find what is affected and establish which cases should be allowed or rejected.

Requirements need the necessary data, inputs and outputs, conditions and exceptions, and cases with expected results. The expert judges business meaning and success criteria rather than specifying fields or functions. Initial design and development criteria are agreed with technical specialists; subsequent changes within that scope should proceed against the same model.

### Configuring automation with existing agents and tools

Next, check whether existing agents and tools meet the requirements. When the necessary query and action capabilities and permissions are available, connect them into a workflow and test it with business scenarios. Missing capabilities become implementation requests for the Software Factory.

Check that inputs and outputs match, business rules hold, and failures are handled as intended. Self-improving agents should then use change requests, execution records, and review findings to revise the workflow and tool use. The agreed business model remains the reference.

### Implementing missing capabilities with the Software Factory

The Software Factory implements and verifies missing capabilities and supplies code and tools that automation can use. It should read the business model, ADRs, and current implementation together to determine impact, then check the business conditions through tests and scenarios.

Alongside code, it should leave **evidence of which business conditions changed and what was verified**. Generated code alone does not establish correct business behavior. [Software Factory evaluations](/en/2026/10/05/software-factory-evals-and-tension-metrics.html) need to distinguish the two.

This role continues after the initial build. When a business change requires code changes, implementation and verification should follow the same criteria, without requiring a domain expert to rewrite every request in technical terms.

## 5. Reviews and organizational responsibilities that enable self-improvement

Differences found in execution records and session or workflow reviews need changes appropriate to their cause. If the ontology's business model is missing a rule or exception, correct it against the sources. If execution violates an existing rule, fix the workflow or code. Business meaning and verification criteria must not be changed just to accommodate the code.

A correct answer may still have relied on source retrieval to compensate for a wrong business definition. Evaluating the final result and stored knowledge separately helps prevent the same incorrect rule from being reused.

For changes with established business criteria, revise knowledge or execution according to the cause and verify the result. When a new business judgment is needed, the domain expert must establish the criteria first.

{% raw %}
```mermaid
flowchart TB
  R["Execution and session review"] --> D{"Cause of the gap"}
  D -->|"Missing business rule"| K["Update ontology"]
  D -->|"Execution error"| I["Revise workflow or code"]
  D -->|"New judgment needed"| O["Domain expert"]
  O -->|"Criteria agreed"| K
  K --> V["Verify business and implementation"]
  I --> V
  V -->|"Pass"| S["Update knowledge and execution"]
  V -.->|"Fail"| R
  S --> R
```
{% endraw %}

Verified changes must also be reflected in business models and implementation knowledge. Update the ontology when rules change, and implementation knowledge and retrieval indexes when service connections or code locations change. This lets subsequent business agents and coding agents work from the same changes.

### Moving decision authority and verification responsibility together

This flow also requires organizational change. Domain experts accountable for the business model and its outcomes need authority over changes and responsibility for verification. Platform and technical teams should own the shared execution foundation and its access, verification, and recovery standards.

| Role | Responsibility |
| --- | --- |
| Domain experts | Recognize business changes, decide rules and outcome criteria, verify results |
| Platform and technical teams | Operate reusable execution, access, verification, and recovery capabilities |
| FDEs | Establish initial models and adoption; enable business teams to change and verify their work |

When several departments participate in one process, they need shared completion criteria and agreement on change ownership. Moving people without changing decision authority or evaluation criteria leaves teams waiting for one another's judgments.

If the common platform team builds every business-specific feature, growing demand puts teams back in its queue. [Internal FDEs](/en/2026/09/03/developers-to-internal-fde.html) can help establish the system, but should enable business teams to continue changing and verifying their work afterward.

### Checking with one business change

Use an actual business change to check whether the system can handle it without technical specialists reinterpreting the request. When a refund policy changes, check whether the domain expert can request the new conditions in business terms and verify the system's changes through business scenarios.

Include the time experts spend explaining and checking results alongside processing time, failures, and rework. If every change still requires an FDE or developer to reinterpret the request, some execution may have been automated while the dependency for changes and maintenance remains.

## Conclusion

The ideal outcome of AX is **a system whose business processes, organizational responsibilities, and implementation follow the same business model, with implementation details managed autonomously within those criteria**.

If business experts must learn the solution's technical interpretation after an FDE finishes the build and leaves, they have inherited work previously handled by developers. They need to be able to request changes and judge results in their own business terms.

Reaching that goal requires **designing reusable solutions so that business language, models, and implementation remain consistent in meaning**. Software Factories and self-improving agents should maintain that alignment through repeated changes and verification, while organizations give domain experts the authority and responsibility to lead the process.

[^1]: AWS, [AWS invests $1 billion to embed AI forward deployed engineers with customers](https://www.aboutamazon.com/news/aws/aws-1-billion-forward-deployed-ai-engineers), June 30, 2026. Describes the customer-account semantic layer, knowledge graph, and customer engineers' progression toward independent operation.
[^2]: AWS Partner Network Blog, [Introducing Forward Deployed Engineering for Partners](https://aws.amazon.com/blogs/apn/introducing-forward-deployed-engineering-for-partners-winning-the-future-of-enterprise-ai/). Describes the partner-owned, reusable harness of ontologies, evaluation, tool connections, and agent operations.
[^3]: Palantir, [Integrated platforms: AIP, Foundry, and Apollo](https://www.palantir.com/docs/foundry/architecture-center/platforms). Describes the standard platforms, customer-specific customization, and FDEs.
[^4]: Palantir, [Ontology building](https://www.palantir.com/docs/foundry/ontology/overview). Describes the operational layer combining business objects and relationships with actions and functions.
[^5]: [3D view in the business ontology tool](https://github.com/haandol/alps-writer-plugins/tree/main/plugins/ontology-writer). The “Expression dictionary” BC generated from EncBird's business model. Screenshot labels were translated into English for this version.
