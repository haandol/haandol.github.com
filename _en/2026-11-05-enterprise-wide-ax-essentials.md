---
layout: post
title: "What Platforms Does Company-Wide AX Need?"
excerpt: Platform requirements for scaling agentic work across a company
author: haandol
email: ldg55d@gmail.com
tags: ai agent ax platform organization software-factory knowledge harness-engineering
publish: true
published: true
date: 2026-11-05 14:30:00 +0900
last_modified_at: 2026-11-13 10:01:36 +0900
lang: en
translation_key: enterprise-wide-ax-essentials
korean_url: /2026/11/05/enterprise-wide-ax-essentials.html
permalink: /en/2026/11/05/enterprise-wide-ax-essentials.html
---

## TL;DR

- Company-wide AX needs requirements, knowledge, development, and automation platforms.
- Each platform's output must become the next stage's input.
- Reviews should improve the business model, execution, and code together.

## Introduction

Writing about harness engineering, the cognitive load of reviewing AI-generated code, internal FDEs—engineers working on automation with business teams—and Software Factories has led me to think about how a company should approach AX as a whole.

By AX (Agentic Transformation), I mean automating business processes by removing human intervention, and eventually allowing those processes to improve themselves based on operating results.

If one team automates a task with an agent, another team can try something similar. But if every team has to prepare its own data connections, agent environment, review and approval process, and result tracking, the work of setting up and maintaining automation grows along with the number of tasks.

I think **company-wide AX requires platforms for requirements, shared knowledge management, software development, and business automation**. Teams need to reuse common capabilities and working procedures while adapting them to their own business rules and systems.

This post describes the capabilities needed in these four platform areas and how they should connect. I use examples from platforms I am developing to make these requirements concrete.[^7]

## 1. Four platform areas for company-wide AX

The diagram below shows the platform structure I have in mind. Boxes show platform roles, and dashed lines represent the artifacts and knowledge that need to pass between them.

{% raw %}
```mermaid
flowchart TB
  subgraph X1["1. Requirements"]
    H["Requirements"]
  end
  subgraph X2["2. Shared knowledge"]
    K["Data and knowledge"]
  end
  subgraph X3["3. Software development"]
    F["Build and verify"]
  end
  subgraph X4["4. Business automation"]
    S["Process discovery"]
    W["Agent operations"]
    S -.->|"Automation requirements"| W
  end
  H -.->|"Agreed requirements"| F
  F -.->|"Code and tools"| W
  W -.->|"Change requests"| H
  K -.->|"Research evidence"| H
  K -.->|"Business context"| F
  K -.->|"Process data"| S
  S -.->|"Data requirements"| K
  K -.->|"Permitted knowledge"| W
```
{% endraw %}

Creating a new capability in a company involves defining a business requirement, implementing it in code, and applying the resulting system to real work. Problems found in operation become new requirements. Managing the business definitions and rules used throughout this work is another responsibility.

Platforms for company-wide AX can be organized around these four responsibilities.

| Platform area | What the platform does | Outputs to share |
| --- | --- | --- |
| 1. Requirements | Research, specification and prototype creation, joint review | A version of agreed requirements, prototype, and success criteria |
| 2. Shared knowledge | Authoring, review, and retrieval of business knowledge; data mappings, evidence, access, and versions | Sources and business knowledge shared across platforms |
| 3. Software development | Impact analysis, code changes and checks, review, merge, and deployment automation | Verified code, validation evidence, and operating results |
| 4. Business automation | Discover current work, select automation candidates, configure and operate agents | Process maps, automation requirements, and execution records |

The shared knowledge platform supports the other areas by securing data and managing access. It also owns knowledge authoring, review, and updates, so requirements research, development, process analysis, and agent execution can use consistent definitions and rules.

Business automation must connect **understanding current work and choosing what to automate** with **executing the selected work**. These responsibilities can be handled by a process discovery platform and an agent operations platform.

The build order depends on the approach. A team can analyze processes with business experts before securing the required data. Automating that analysis may instead require preparing its knowledge foundation first. Either way, shared knowledge supports both analysis and execution and needs early attention.

This division defines responsibilities and outputs. One product may cover several roles, but a late input or an output the next stage cannot use will hold up the overall flow.

## 2. Requirements: developing and agreeing on what to build

Turning an idea into a prototype immediately does not settle the business rules and success criteria developers need. When the document and interface change separately, designers and developers have to reconcile what they are reviewing.

The requirements platform should let **planners develop an idea, try it themselves, and preserve the agreement needed to start development in one version**.

### Research and requirements authoring

Planners need to gather references and describe whose problem they are solving and which business rules apply. The platform should distinguish facts found in sources, AI suggestions, and unconfirmed assumptions, then incorporate content the planner has reviewed.

Internal sources need organization-approved connections. MCP (Model Context Protocol), a protocol connecting agents to external tools and data, can be used here. Establishing a connection does not grant access to every source.

### Working prototypes and review criteria

A planner should be able to generate, revise, and try a prototype without managing a development environment. A demo scenario describing what to check and in what order helps distinguish an interface that opens from one that supports the intended work.

New prototype generation should run separately from the version under review. If a failed candidate overwrites that version, it also removes the result other people were reviewing.

### Joint review and version handoff

The specification, demo scenario, and validated prototype should be bound to one version that designers and developers can review and comment on. When changes are needed, the document and prototype should be revised together for the next review.

{% raw %}
```mermaid
sequenceDiagram
  actor P as Planner
  participant H as Requirements platform
  actor R as Designer and developer
  P->>H: Write the spec
  H-->>P: Requirements and prototype
  P->>H: Try and revise
  H-->>R: Fixed review version
  R-->>P: Feedback
  opt Revisions needed
    P->>H: Revise spec and prototype
    H-->>R: New review version
  end
  R-->>P: Agree to start
  P->>H: Select build version
```
{% endraw %}

Having a version to share is different from agreeing to start development. The platform should record the conditions agreed upon and the questions still open, not just the date a link was shared.

In the requirements platform I built, planners work with AI to write a PRD (Product Requirements Document), generate and revise a prototype, then publish the document, demo scenario, and validated prototype as one review version. Organization-level access and sharing are also part of making this work reusable across teams.

## 3. Shared knowledge: providing data and business knowledge

The shared knowledge platform manages the data and business knowledge needed for requirements, development, and automation. Preparing sources separately duplicates work and can leave platforms using different rule versions, so business definitions, evidence, and data mappings need shared management.

One starting point is agent storming: defining the current process (As-Is) and the process to be handled by agents (To-Be). If a team first works with business experts to define those processes, the next task is to secure the data the agents need to execute the target process.

That data is accumulated on the shared knowledge platform, with its owner, source, and permitted uses recorded. **The platform uses these governance rules to grant agents and external services access to the knowledge they need.** Securing data and deciding which services may use it need to be managed together.

The order changes when agent storming itself becomes a solution for automating process analysis. The analysis agent first needs business documents and process data to read. In this approach, the shared knowledge platform must be built first to prepare the relevant sources and access permissions, enabling the agent to retrieve them, analyze the As-Is process, and design the To-Be process. The analysis then clarifies what additional data and permissions are needed.

{% raw %}
```mermaid
flowchart TB
  subgraph P["Start with process analysis"]
    direction LR
    P1["Define As-Is and To-Be"] --> P2["Acquire and store data"]
    P2 --> P3["Grant access"]
  end
  subgraph A["Start with automated analysis"]
    direction LR
    A1["Build knowledge platform"] --> A2["Prepare sources and access"]
    A2 --> A3["Automate process analysis"]
  end
```
{% endraw %}

**The first task can differ, but shared knowledge is difficult to postpone.** Securing data and managing access for the initial business scope need to start early so process analysis can lead to actual agent execution.

The shared knowledge layer needs **hybrid retrieval for general information** and **ontology retrieval for business processes and rules**. Finding similar support cases and understanding the sequence and conditions for handling a refund call for different forms of knowledge.

The shared knowledge platform I am developing preserves source evidence from tables, documents, and existing ontologies, distinguishing observations, source meaning, concepts connected across sources, and business rules. It also connects the storage of business definitions and actual cases with scoped retrieval and correction against the original sources.[^9]

### General information: hybrid retrieval combining similarity and BM25

For documents, meeting notes, and support records, it helps to combine similarity search, which finds passages close in meaning to the question, with BM25 search, which checks how well the actual words match. BM25 ranks documents using factors such as term frequency, rarity, and document length.

For example, similarity search can connect a customer's ‘I want my money back’ with ‘refund request’ in an internal document. For a specific product code or error message, searching for the actual string is useful. Hybrid retrieval combines and ranks the two sets of results to cover these different needs.

Results should include relevant passages, source locations, and revisions. An agent using them to answer a question or support a requirement needs a way to check the original explanation and its conditions.

The local search I implemented also combines keyword and vector-similarity rankings. Its keyword scores use a custom formula, so the BM25 combination above is a requirement for the shared platform rather than a description of the current implementation.

Document retrieval selects relevant documents, then searches for the needed passages within them. Using only documents linked to the knowledge model could miss material that has not yet been organized, so it also includes document candidates found by directly searching source passages within the same permitted scope. It verifies the text and citation locations against the selected document's exact revision instead of answering directly from text retained in a search summary or vector index.

### Business knowledge: ontology retrieval through abstraction layers

A few relevant passages may be insufficient to understand the refund sequence, approval conditions, and effects on other work. An ontology explicitly records business concepts, relationships, processes, and rules, helping the agent navigate while keeping track of which business activity and condition it is reading.

**Ontology retrieval does not require a graph database or a graph traversal engine.** Business processes can be written in Turtle, a text format for recording concepts and relationships, and organized into abstraction layers that an agent can search and follow into detail. Here, layers separate different levels of detail: a business area's responsibilities and core rules, its internal processes, and the conditions its implementation must satisfy.

This platform first provides a map of bounded contexts (BCs), the scopes responsible for particular business terms and rules. The map contains each area's responsibilities, core business logic, and connections to other areas. When the prepared overviews fit within the agent's input limit, it can read the entire permitted map and search for heavier internal detail inside selected BCs.

For example, an agent changing refund functionality can read the ordering and payment overviews, choose the relevant areas, and use similarity search to find refund processes, approval rules, and exceptions within them. For implementation work, it can descend into related ADRs (Architecture Decision Records) and current code. If it already knows the required rule or ADR, it can also enter at that detail directly.

**Business scope and detail level are selected before similarity is compared within them.** Retrieval can work with known BC membership and detail levels without a complete hierarchy of internal parent-child relationships. Rules that apply to several BCs retain those relationships, while material with unknown membership is not assigned to an arbitrary area.

{% raw %}
```mermaid
sequenceDiagram
  participant A as Agent
  participant K as Shared knowledge
  participant C as Code repository
  A->>K: Read business map
  K-->>A: BC overviews and links
  A->>K: Search chosen BC and layer
  K->>K: Filter, then rank similarity
  K-->>A: Rules, sources, references
  A->>K: Read details and conditions
  K-->>A: Definitions, evidence, gaps
  opt More context needed
    A->>K: Search details and sources
    K-->>A: More evidence or gaps
  end
  A->>C: Find implementation
  C-->>A: Code and tests
```
{% endraw %}

Today's agents are quite good at reading an overview and deciding which area and item to examine next. I think giving them the necessary explanations at each layer and paths into the next one is often enough to handle business knowledge at a substantial scale.

That abstraction design matters more as the scope grows toward an enterprise. Searching one enormous data lake and returning detailed material from many business areas leaves the agent to sort out the conditions relevant to its current task. Narrowing the scope at the upper layer and searching within each layer reduces the unrelated detail brought into context.

Centrally stored data can still support retrieval by layer. The efficiency I mean is **how little context an agent needs to receive the relevant information**, rather than how quickly the storage is read.

Rare exceptions omitted from an overview must remain available. The navigation feature I built reads selected definitions together with their required conditions and also supports direct retrieval of details and sources within the same permitted scope. When a definition exceeds the input limit, it leaves the unread dependencies and scope visible so the agent can split the read or adjust its selection, rather than truncating the definition and presenting it as complete.

### Abstracting business processes and separating layers with DDD

Navigating from a business overview into the relevant details requires clear business boundaries and layer responsibilities when the knowledge is created. I used DDD (Domain-Driven Design), which designs models around business language and rules, as the basis for those boundaries.

First, bounded contexts separate the scopes in which terms and rules have consistent meanings. Each BC records the work it owns and the results it passes to other BCs. For example, ‘cancellation completed’ in ordering and ‘refund completed’ in payments are different events. A refund process can cross both areas while retaining the distinct concepts and the events and conditions connecting them.

The BCs identified through this work must also shape how agents handle requests. Execution needs to connect each task to the business context and rules it reads, the tools and permissions it uses, and the results it passes to other BCs. Even when one agent handles work across several BCs, each step must retain the appropriate terms, decision criteria, and meaning of its outputs.

Processes within those boundaries are abstracted through their purpose, participants, inputs and outcomes, and each step's conditions and exceptions. Business knowledge explains why the work exists and what it must preserve; table names, code files, and task commands belong in the layer concerned with implementation. This lets the meaning of a process survive changes in storage or implementation tools.

**An upper layer must answer the questions at its own level, and lower layers must satisfy its criteria.** Business knowledge holds processes and rules; ADRs hold implementation decisions and exact conditions; code and data mappings hold concrete handling methods. Conditions that change an outcome, such as approval limits and exceptions, must remain complete in the layer that owns them. Abstraction must not make those conditions vague.

The diagram shows which criteria a lower implementation depends on.

{% raw %}
```mermaid
flowchart BT
  I["Code and data mappings"] -->|"Meet implementation conditions"| A["ADRs"]
  A -->|"Preserve business rules"| B["Business knowledge"]
```
{% endraw %}

An agent should read the same fixed version of the upper criteria alongside the current implementation and propose changes that preserve those boundaries. If a refund-status column changes, it updates the data mapping to satisfy the existing completion criterion, without changing the meaning of completion or its verification criteria to make the mapping fit. If the business owner changes the completion criterion itself, that decision comes first, followed by revalidation of the affected ADRs, implementation, and data mappings.

This separation of responsibilities is also distinct from the level of detail used to read business knowledge. A BC overview and its internal processes can show the same knowledge at different levels of detail, but shortening an overview or rebuilding a search index must not change business rules.

### Improving stored business knowledge against its sources

Business knowledge needs maintenance after it is first created. A new case may reveal an exception, or an existing definition may have misrepresented a source condition. Those corrections need to remain available for the next task.

I built the correction feature to keep an inventory of sources and cases separate from business definitions and read selected originals alongside current definitions to propose corrections. Its review interface shows the original source, existing clause, and proposed clause side by side, making changes to conditions, negation, quantities, and exceptions visible. The correction guidance also preserves successful methods and confirmed facts, rather than deleting an existing fact simply because it is absent from the sources selected this time.

{% raw %}
```mermaid
sequenceDiagram
  actor O as Business owner
  participant K as Shared knowledge
  participant A as Correction agent
  O->>K: Request correction
  K->>A: Current definitions and sources
  A-->>K: Candidate and evidence
  K-->>O: Compare sources and changes
  O->>K: Review and adopt
  Note over O,K: Publication is separate
```
{% endraw %}

The current correction feature produces a candidate on request for the business owner to adopt. Connecting evidence from session and workflow reviews to that correction flow is a further capability the platform needs. Stored cases can be retrieved within the same business scope and revision, without automatically generalizing their inputs and observed results into current rules or facts about other work.

Whether a correction helps needs a separate check. The comparison tool I built for this uses the same sources and questions for three configurations: source retrieval alone, current business knowledge with sources, and corrected business knowledge with sources. Alongside answer quality, it records initial knowledge and index preparation costs, correction costs, and retrieval and answer costs per question separately.

A correct answer may still have relied on source retrieval to compensate for a wrong business definition. The comparison therefore separates which retrieval path recovered required evidence from whether the definitions themselves preserve the source conditions and exceptions. I think **final answers and the accuracy of stored knowledge need separate evaluation**.

Adopted knowledge and the version published for operational use need distinct version records. Source changes and revoked access must affect retrieval paths. Current access must be checked both when retrieving information and when returning it; material already found must not be returned if access was revoked during the search.

The shared knowledge platform's search and business-context retrieval can be exposed to multiple platforms through an open standard such as MCP.[^5] Connections need to carry the requester's permissions and the exact knowledge revision as well as the authentication method. Platforms may reuse the same knowledge, but they still need a record of which version of a rule they read.

## 4. Software development: connecting implementation and verification

Once requirements are agreed, the development platform needs to turn them into verified code and deliver them to the actual service. A coding agent can implement quickly while disconnected review, checks, and deployment still limit company-wide delivery speed.

Faros AI's 2025 report used data from more than 10,000 developers to compare periods of lower and higher AI adoption within teams. Merged PRs increased by 98%, but review time also rose by 91%, with no significant correlation between AI adoption and performance improvements at the company level.[^1] A PR (Pull Request) is a request to review a code change and merge it into the existing code.

This was an observational analysis as of June 2025, when most usage was autocomplete. It does not establish the same result for today's agents, but it does show that later stages can fail to keep up with increased implementation throughput.

That is why I think software development needs **a development platform connecting request intake, impact analysis, isolated implementation, checks, and delivery**.

### Project-specific standards and execution environments

The platform should connect existing repositories, tickets, operational alerts, and CI. CI (Continuous Integration) automatically builds and checks code changes. Connecting agent work to a team's current development flow is easier to adopt than replacing all of its tools.

Project-specific design standards, task instructions, and check commands need to be registered, with the version used for each run recorded. Work needs coordination so that agents do not overwrite one another's changes in the same repository. Execution time, cost, and retry budgets also need management.

### Changes and verification evidence

Code changes should run in an environment separate from existing work, with real builds, tests, and business scenarios checking whether the requirements are met. Failed or unavailable checks need to remain visible, and their results should not be delivered as if the change had succeeded.

Along with code, the agent should leave **evidence of what changed and which conditions were checked**. As discussed in [my post on AI code review's cognitive load](/en/2026/08/18/ai-coding-review-cognitive-load.html), review remains a bottleneck when people have to reconstruct the implementation's intent and impact from scratch.

### Review and merge policies, and operating feedback

Smaller changes, AI review and approval, and risk-based handling can all reduce review work.[^2][^3] The platform should apply the company's adopted policies and manage which changes can be handled automatically and which need human review.

Classifying a change as suitable for automatic merging is not sufficient to merge it. The actual checks, repository protection rules, permissions, and change version must still be valid at merge time. Incidents and change requests after deployment also need to return as new work.

{% raw %}
```mermaid
flowchart TB
  B["Project standards"] --> R["Development request"]
  R --> A["Impact analysis"]
  A --> C["Isolated implementation"]
  C --> V{"Verification"}
  V -->|"Failed or unavailable"| F["Record incomplete work"]
  F -->|"Retry allowed"| C
  V -->|"Passed"| P["PR and evidence"]
  P --> G["Check merge conditions"]
  G -->|"Conditions met"| D["Merge and deploy"]
  D --> O["Operating results"]
  O -.->|"Change request"| R
```
{% endraw %}

The Software Factory I am developing is a self-hosted base project. It connects existing repositories, tickets, alerts, and CI, and manages project standards, requirements decisions, coding-agent changes and checks in isolated environments, PRs, and automation policies. Policies are built from real PR examples and evaluated on separate cases, while classification is kept distinct from actual merge authority.

A Software Factory should carry requirements through implementation, verification, delivery, and fixes for problems found in operation. StrongDM's scenario-based verification[^4] and [my post on Software Factory evals](/en/2026/10/05/software-factory-evals-and-tension-metrics.html) both address how to define success and judge the next change.

## 5. Business automation: connecting process discovery and agent operations

Automating development does not decide which business work to change first. The company needs to understand work scattered across departments, select the scope of automation, and connect it to executable capabilities and operating ownership.

### Process discovery: building a map with evidence

For example, in a refund process, support receives the request, the order team checks delivery status, and finance approves it depending on the amount. Workshops such as [Event Storming](/2020/12/10/demystifying-event-storming.html) (Korean) collect these events and rules into a view of the whole flow.

Across a company, gathering every expert at the same time is difficult. If one department is missing, its approval rules may be missing too. After the workshop, people may have to reconstruct who supplied each explanation behind the map.

A process discovery platform should draft the map from internal documents and read-only tools, then let people answer questions asynchronously or edit it directly. Events, rules, and exceptions need source references, source versions, and confirmation states. Conflicting accounts and unanswered questions must remain visible.

Publication should fix the reviewed map together with its evidence and question state. An unfinished map may be shared, but publication must not be treated as proof that discovery is complete.

### Automation candidates and implementation requirements

Choosing a target process for agents from the current process map requires considering frequent requests and long waits alongside exception frequency and the impact of failure. The team must also check that the shared knowledge platform has the required data, that the executing agent has permission to read it, and that tools can perform the work.

For refunds, small cases with clear rules could be considered first. But if every case waits for a person's approval, reducing that wait requires agreeing with finance on the conditions and limits within which the agent can act. Cases involving frequent judgment calls, such as disputes, can remain with people.

The platform should help distinguish agent judgment, deterministic rules, human work, and insufficient evidence. Selected candidates need requirements the next stage can implement.

| What to preserve | Refund example |
| --- | --- |
| Goal and automation scope | Reduce small-refund handling time while passing disputes to support |
| Data and usage conditions | Owners, permissions, freshness, and retrieval-failure handling for delivery status and refund policy |
| Inputs and outputs | Receive a refund request and return approve, reject, or human review, with the reason |
| Representative cases and success criteria | Expected results for an allowed cancellation, a policy rejection, and a request above the approval limit |

In the process discovery platform I built, business boundaries and automation candidates are analyzed against the same published snapshot, then goals, data, input/output contracts, and three distinct examples are exported as a requirements document and JSON. Links to the original process map and unresolved questions remain in the document.

{% raw %}
```mermaid
flowchart TB
  S["Internal sources"] --> M["Process map and evidence"]
  U["Expert review"] --> M
  M --> P["Publish review version"]
  P --> A["Identify candidates"]
  A --> C["Review candidates"]
  C --> R["Automation requirements"]
```
{% endraw %}

### Agent operations: finding and executing the needed capabilities

Once work has been selected, the agent operations platform should clarify its inputs and expected outputs, then find and connect available agents and tools. A catalog for registration, discovery, and sharing helps departments avoid rebuilding the same capabilities.

If one existing agent supplies the required input/output contract, its version should be reusable directly. Multiple capabilities can be assembled into a workflow, with checks on data types and required values between steps. A missing capability should remain an implementation requirement for the development platform.

The refund example still needs capabilities for checking delivery, checking policy, and processing refunds. Generating a workflow does not itself prepare those capabilities or grant permission to run them.

The operating platform also needs the following capabilities:

- **Trials, review, and sharing:** test new versions, complete required security review and approval, and make them available to permitted users.
- **Version and execution controls:** fix approved versions and check current access and suspension at execution time.
- **Tracing and evaluation:** connect inputs, step-level tool calls, results, failures, and costs.
- **Feedback and improvement:** incorporate failures into evaluations and procedures, then review the improved version.

{% raw %}
```mermaid
flowchart TB
  I["Define inputs and outputs"] --> S["Find evidence and tools"]
  S --> D{"Choose configuration"}
  D -->|"One capability"| A["Select fixed version"]
  D -->|"Combine capabilities"| W["Compose and validate"]
  D -->|"Missing capability"| N["Request development"]
  W -->|"Checks passed"| T["Test, review, approve"]
  A --> R["Check usage conditions"]
  T -->|"Conditions met"| R
  R -->|"Allowed"| O["Execute and trace"]
```
{% endraw %}

The agent operations platform I built registers departmental agents, MCP services, and workflows, then finds and connects approved capabilities matching the input/output contract confirmed through conversation. It distinguishes direct agent selection from workflow composition and rechecks usage conditions during execution.

Someone also needs to use operating results to improve procedures and evaluation cases. The FDE (Forward Deployed Engineer) in [my post on internal FDEs](/en/2026/09/03/developers-to-internal-fde.html) is an engineer working close to business teams on this implementation and improvement. Execution records alone do not sustain improvement if no one owns the work of changing the process.

## 6. Handoffs and company-wide operation

Even with the platforms in place, people explaining everything again and moving data at each transition creates another bottleneck. Each platform therefore needs **an output that lets the next platform retain the agreed conditions and their evidence**.

The requirements platform should pass the specification, prototype, and success criteria as one version. The process discovery platform should attach the original map and open questions to automation requirements. Execution results should identify the requirements and knowledge versions used, so they can support the next change.

Those details need to travel with work passed from the requirements platform to the development platform, or from process discovery to agent operations. Similar file formats or MCP support alone do not complete an automatic integration.

### Turning reviews into the next ontology, workflow, and code changes

Once BCs shape execution, session reviews and agent workflow reviews should use the same business model as their reference. A session review examines which context the agent read and which rules guided its decisions. A workflow review examines whether conditions and results were passed correctly across steps and BCs.

Differences found in review need changes in the layer responsible for their cause. Missing business conditions or exceptions call for an ontology change proposal backed by evidence. When execution fails to follow an existing rule, the agent's procedure, tools, or code need correction. Adopted business changes must reach the related workflows, ADRs, and implementation, with the cases used in review retained for checking the next change.

For example, suppose an agent confirms an order cancellation and then tells the customer that the refund is complete. The review should first check whether the model distinguishes order-cancellation and refund completion conditions. If it does and the agent skipped a required check, revise the workflow; if the necessary query capability is missing, implement it. Then verify that the agent does not tell the customer the refund is complete before confirming refund completion in the payments context.

The Software Factory should carry those business rules and implementation contracts into code and tests. The agent operations platform should connect that code and those tools into executable business processes. Execution records and reviews then become evidence for revising the ontology, workflows, and implementation again.

This is the iterative structure I have in mind for the two platforms.

{% raw %}
```mermaid
sequenceDiagram
  participant K as Ontology
  participant F as Software Factory
  participant W as Agent operations
  participant R as Reviews
  actor O as Business owner
  loop Execute, review, improve
    K-->>F: Rules and contracts
    F-->>W: Verified code and tools
    K-->>W: BC processing rules
    W->>R: Execution records
    opt Business change needed
      R-->>O: Candidate and evidence
      O->>K: Review and adopt
    end
    R-->>W: Workflow changes
    R-->>F: Implementation changes
  end
```
{% endraw %}

Repeated iterations should reduce the gap between the business model and actual behavior. Alongside building the initial model well, the platforms need to carry what is learned in operation into the next model and its execution.

### Shared operation and business-specific customization

Company-wide platforms need owners for organization and project access, usage and cost, versions and security patches, and incident response. Each business team needs someone responsible for its rules, exceptions, and evaluation cases.

I think a common platform organization should work alongside teams that customize and operate what it provides. If the central organization has to build every business-specific feature too, teams will end up waiting on it as requests grow.

Teams also need a harness combining task instructions, tools, checks, and evaluation criteria so they can customize with agents.[^6] Configuration and extension points, along with reviews of changes and their effects, help teams keep receiving security patches and improvements without separately modifying every copy of the common code.

Commercial services can be used where their capabilities are sufficient. Custom development can start from a shared base. Either way, an internal team still needs to own business configuration, evaluation, and improvement.

### Measure adoption speed separately from business outcomes

More teams using a platform or a faster first prototype does not establish the effect of company-wide AX. Faster preparation and better business outcomes need separate measurement.

| Area | What to check |
| --- | --- |
| Requirements | Time from organizing an idea until planners, designers, and developers agree to start |
| Shared knowledge | Missed rules and exceptions in retrieval, correction accuracy, and preparation and query costs |
| Software development | Time from confirmed requirements to stable delivery, failed checks, and rework |
| Business automation | Time from request to completion, human intervention, incorrect handling and reprocessing, total cost per case |

Shared operation also needs measures of whether more teams can run and improve their own work, and of the effort and cost of adopting common changes.

Process maps need checks for omitted items, incorrect additions, and items with unconfirmed evidence as well as creation time. A map containing every confirmed rule can still be poor if it also adds many incorrect rules.

Capture a baseline for the existing approach and compare similar scope and exception mix. Include the time experts spend answering questions and reviewing results, so moving manual work to someone else is not counted as an automation gain.

## Conclusion

If I were pursuing company-wide AX, I would start by defining the requirements for each platform. Requirements, shared knowledge management, software development, and business automation each need different capabilities and responsibilities.

Together, these platforms should let **business language and rules carry through to real execution and the structure and behavior of code**. I see this as the ideal DDD has been pursuing. Agents should use models developed with business experts to guide execution and implementation, then bring what reviews reveal back into those models.

I also built an [ontology tool](https://github.com/haandol/alps-writer-plugins) for authoring business models and connecting them to development. It lets users model processes, steps, events, and rules in Turtle, then move from a business-area overview to searches within that area and on to related ADRs.[^8]

The screenshot below shows this tool displaying the ontology of an English learning service I am developing. Selecting the ‘Expression dictionary’ BC exposes its registration and expansion processes and steps for search and further inspection. The screenshot's Korean text has been translated into English for this version of the article.

![Ontology view of an English learning service with the Expression dictionary area selected. Processes and steps appear on the left, with the business overview and search within the area on the right.](/assets/img/2026/1105/encbird-ontology-knowledge-en.png)

When agents take on finding, changing, and verifying the connections between business models and implementation, they can reduce the effort needed to maintain this structure. Software Factories and agent operations platforms should repeat this process so that business knowledge, workflows, and code evolve together. I think **agents have made it possible to build and maintain the ideal DDD originally set out to achieve**.

---

[^1]: Faros AI, [The AI Productivity Paradox Report 2025](https://www.faros.ai/blog/ai-software-engineering). Observational analysis as of June 2025 of AI adoption, PR throughput, review time, and company-level performance.
[^2]: Google, [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html). The practice of keeping changes small enough to review easily.
[^3]: GitHub, [Copilot code review](https://github.blog/changelog/2026-10-28-copilot-code-review-merge-with-confidence-with-max-and-approvals); Meta Engineering, [Diff Risk Score](https://engineering.fb.com/2025/08/06/developer-tools/diff-risk-score-drs-ai-risk-aware-software-development-meta/). Examples of AI review and approval, and risk-based deployment controls, respectively.
[^4]: StrongDM, [Software Factories and the Agentic Moment](https://factory.strongdm.ai/). Software development using specifications and scenario-based verification without human code review.
[^5]: Anthropic, [Donating the Model Context Protocol and establishing the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation).
[^6]: [My post on harness engineering](/en/2026/03/15/harness-engineering-beyond-context-engineering.html), covering task instructions, tools, execution environments, verification, and recovery.
[^7]: Based on documentation and key implementation paths in the requirements, development, process discovery, agent operations, and shared knowledge platforms I am developing, as of November 6, 2026. Inspection of individual capabilities does not establish integrated execution across the platforms or measured company-wide results.
[^8]: [Layered navigation in the business ontology tool](https://github.com/haandol/alps-writer-plugins/tree/main/plugins/ontology-writer). The view was generated from the business ontology of an English learning service I am developing, on November 9, 2026. The file-based implementation reads the Turtle model on each query but returns only knowledge from the selected layer to the agent. The screenshot illustrates the organization of business knowledge, not measured enterprise-scale retrieval performance.

[^9]: Based on the designs, implementation, and tests for business-context navigation, layer contracts, document retrieval, and source-backed correction in the shared knowledge platform I am developing, as of November 9, 2026. I inspected the paths comparing source-only retrieval, current knowledge, and corrected knowledge; this article does not report new measurements of live-model accuracy or enterprise-scale performance gains.
