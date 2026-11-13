# Independent Final Review

Use this at the end of a writing, revision, or translation task, after the writer's
own editorial pass. The writer owns changes; a separate reviewer tests whether the
manuscripts communicate the user's intent without explanations from their author.

## Prepare the intent and manuscripts

- Write one short intent paragraph from the user's request and accepted corrections:
  the reader's question, the author's intended answer, the audience, article form, and essential
  user constraints such as a fixed title or language restriction. Do not infer the
  intended answer from the current draft merely to make the draft pass.
- Provide current Korean and English manuscript paths, subject to the user's
  language scope. These are review inputs, not extra background. For conversational
  copy, save exact snapshots in a task scratch location and provide their paths.
- Do not include the drafting conversation, plans, revision history, implementation
  explanations, source summaries written by the authoring agent, suspected issues,
  preferred rewrites, prior findings, pass counts, or arguments defending the draft.
  Necessary context must be in the manuscript itself.
- Finish pending edits before dispatch and keep the manuscripts unchanged during
  review. Identify their content versions, for example with SHA-256 hashes, so a
  report cannot be mistaken for a review of later text.

## Dispatch a fresh reviewer

Use an actual isolated subagent, not a role-play by the writer or a conversation
fork. With `spawn_agent`, explicitly set `agent_type: "default"` and
`fork_context: false`; omit model overrides unless the user requested one. Use a
new reviewer for each revised version rather than reusing a reviewer that already
knows the fixes or earlier verdict. Never use a new user-owned chat as a substitute.

The handoff contains the intent paragraph, manuscript locations, and the reusable
review instructions only. This is what "intent-only" means: no authoring context
other than intent, while still giving the reviewer the text it must review.

Use a neutral handoff such as:

```text
Review these manuscripts in independent final-review mode, report-only.
Intent: [short user-grounded intent paragraph]
Manuscripts: [absolute paths to the current versions]
Review instructions: [absolute path to haandol-blog-review/SKILL.md]
Read the complete manuscripts yourself. Do not edit files, spawn agents, or consult
drafting history and prior reviews. Return your review to the writer.
```

If isolated delegation is unavailable, finish independent writing and mechanical
checks and state that the required final review could not run. Do not claim a pass
from self-review or silently use a reviewer with shared history.

## What the reviewer returns

Apply the six axes and severity criteria in `haandol-blog-review`. First read the
body without using linked sources or summaries to fill missing context. Then check
titles, summaries, figures, citations, and language equivalence. Read relevant
author posts or cited sources independently when necessary; do not use them to
excuse a missing explanation in the article. Do not read task logs or prior reviews.

Return a concise report that identifies:

1. The reviewed files and content versions, and the argument the text actually
   communicates compared with the supplied intent.
2. Concrete High/Medium/Low findings using the review skill's finding columns.
   Include unnecessary sections, defensive asides, repetition, personal work status, or detail that
   distracts from the intent and article form, not just sentence-level edits.
   Preserve supported facts and qualifications.
3. At least one consequential transition: what the reader already knows and what
   the next passage adds. Note any missing context or needed source verification.
4. Final High/Medium/Low counts and review limits. Do not manufacture findings or
   assume that the expected outcome is a pass.

## Use the feedback and recheck

The writer evaluates every finding and applies supported in-scope fixes without
routine reconfirmation. If a finding is mistaken or conflicts with user intent,
record the passage and reason for rejecting it. Do not blindly apply suggestions,
weaken the author's position, or downgrade a real problem to finish sooner.

Keep a writer-side list of material findings and their resolution. A new reviewer
overlooking an earlier issue does not resolve it. Missing facts or decisions that
prevent a supported repair remain explicit blockers after other fixes are done.

After changing prose, captions, or diagrams, run the affected mechanical checks and
request a fresh review using the same neutral protocol. Update the intent only
when the user changes it. Do not send the new reviewer the previous report, your
fix log, or rebuttals. Completion requires High: 0 and Medium: 0 on the current
manuscripts and an evidence-based disposition of earlier material findings. Low
findings can remain; metadata-only changes that do not affect meaning need only
the applicable mechanical checks. Report actual independent results, not a guarantee
of perfect writing. This workflow does not authorize commits, pushes, or publication.
