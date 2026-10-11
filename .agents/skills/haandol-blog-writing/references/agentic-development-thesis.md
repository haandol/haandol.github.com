# Context Abstraction and Code That Explains Its Purpose

Use this reference for the context-engineering series and related writing about delegating development work to agents. It records the author's position confirmed on 2026-10-11. A newer explicit brief takes precedence. Do not apply this thesis to unrelated articles or treat it as a permanent statement about product capabilities.

## Context Abstraction and Intermediate Work

The main argument is that development context should be abstracted and managed at the level needed for decisions. As agents improve, they absorb more of the work between requirements and code: finding relevant information, breaking down tasks, planning, tracking progress, and updating that state from implementation and validation results. The author expects this absorption to accelerate.

TaskMaster and GSD are examples of tools that organize this intermediate work. Explain the problem they solve before discussing its movement into coding agents. TaskMaster is not merely a session-local to-do list, and GSD is not merely a redundant code summary. Verify their relevant capabilities and the agent features being compared from current primary sources; do not claim that every feature has already been replaced.

The continuing need for plans and state is compatible with less manual coordination by people. People maintain business intent and lasting decision criteria; agents increasingly manage the concrete work and its changing state. Static context means criteria that outlast a task, not immutable documents. Dynamic context includes useful deliverables and handover state, not just disposable records.

Cleaning up obsolete records is a supporting practice. It must not replace the article's main conclusion about abstraction and who manages the intermediate process. Preserve the acceleration outlook as the author's reasoned expectation, not as a measured adoption trend or a claim that every project is already autonomous.

## Code as Context for the Next Agent

As agents take on more intermediate work, they also read the current implementation to plan the next change. Good code should explain the business it handles through meaningful names, responsibility boundaries, visible relationships, and tests of required behavior.

The author calls this “외치는 코드” or “screaming code,” extending the perspective of Screaming Architecture to code read by agents. Attribute Screaming Architecture to Robert C. Martin; distinguish the author's application from the original source. Develop the idea through a concrete business rule and show how a reader connects the requirement to code and tests. A label or a long comment alone does not establish that connection.

Code explains current behavior. Requirements and architecture decision records preserve intent, constraints, and design reasons that cannot reliably be reconstructed from the implementation. The thesis does not eliminate documentation or make implementation-mirroring tests sufficient evidence of correctness.

The author's domain judgment and reduced implementation costs can support this argument: people can use agents to propose refactorings, judge their business meaning, and improve the code future agents will read. Those observations must lead back to good code rather than displacing the subject with a general claim about developers' value.

## Distinct Questions in the Series

These are the roles of the revised articles, not a template for every future post. Read their full current versions when using them as evidence.

| Article | Question and answer to preserve |
| --- | --- |
| [March 11: Context engineering](../../../../_posts/2026-03-11-context-engineering-static-vs-dynamic.md) | Which context should people manage as agents absorb intermediate work? Preserve intent and lasting criteria at a useful abstraction level; delegate more task planning and state management. |
| [March 13: Business-aligned code](../../../../_posts/2026-03-13-agentic-dev-business-aligned-code.md) | What makes code useful to the next agent? It reveals business concepts, rules, and relationships, with tests checking the required behavior. |
| [March 15: Harness engineering](../../../../_posts/2026-03-15-harness-engineering-beyond-context-engineering.md) | What environment makes that delegation practical? Connect context and tools to checks, revisions, and unresolved-state handover; supplying information alone does not guarantee compliance. |
| [March 31: Multi-agent work](../../../../_posts/2026-03-31-multi-agent-without-harness-is-just-context-engineering.md) | When does dividing work help? Compare parallel work or separate review with handover and integration costs, preserving validation and failure ownership. |

## Evidence and Scope

Explain the mechanism behind an expectation without inventing measurements, product history, or firsthand experience. A condition such as stronger planning and tool use enabling longer delegated work can support the author's outlook without proving universal success. Distinguish the current capability from the expected direction.

Keep diagrams within the same claim: a passing check covers its defined conditions, retries can remain unresolved, and dividing agents does not automatically provide validation. Apply the same distinctions to English prose and diagram labels. Related posts may share this perspective while answering different questions.
