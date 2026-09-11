---
name: haandol-blog-review
description: Review Haandol blog posts for natural sentences and flow, clear themes, grounded explanations, AI slop, and the author's established voice. Required after drafting, revising, or translating blog copy in conversation or in _posts/, _drafts/, and _en/. Classify findings as High, Medium, or Low and fix until High and Medium are zero; explicit review-only requests remain report-only.
---

# Haandol Blog Review

Finish with a post that answers its intended reader's question in the author's voice, plus an honest account of the review. This is an editorial review, not AI-authorship detection.

## Scope And Inputs

- Read the repository `AGENTS.md` and [the writing skill](../haandol-blog-writing/SKILL.md). Use its editorial and validation criteria without restarting its workflow or recursively invoking this skill.
- Read the complete current article and the user's brief. Include title, excerpt, TL;DR, headings, tables, diagrams, conclusion, footnotes, and an accompanying English translation. For conversation-only drafts, review the full composed text and apply file checks only if a file exists.
- Use available source material and repository evidence to distinguish facts, interpretations, and proposals. Reuse context already collected by the writing skill instead of fetching it again. If voice references are missing, read at least two older author posts; read related recent posts when terminology or a recurring argument is at issue.
- Preserve firsthand details supplied in the user's article as well as the brief. A shorter brief's silence is not a contradiction and does not justify deleting a detail or relabeling it as hypothetical. Flag actual conflicts or explicitly unverified/model-invented additions instead.
- Normal writing, revision, translation, or review-and-fix tasks include supported edits without another approval. An explicit request to review only, report findings, or leave the file unchanged is report-only.
- Review the whole article to understand the context, but respect a narrower authorized edit scope. Report issues outside that scope without changing unrelated passages.
- Do not commit, push, or publish without the user's explicit instruction.

## 1. Establish The Review Context

Write a short review anchor: the reader's question, the author's current answer, the intended audience, and the kind of article (for example, a personal essay or a practical walkthrough). Infer this from the brief and article when clear; do not ask the user to repeat known context.

Use the older author posts required above to identify a few recurring voice traits relevant to this article: paragraph rhythm, directness of opinion, how examples enter the explanation, vocabulary, and emphasis. Record the reference post paths and the observed traits. Reuse the writer's existing comparison when available. Compare representative passages, not just titles or word counts; do not infer the author's style from recent AI-related posts alone.

The author's current explicit preference takes priority over historical habits. Preserve recognizable voice while allowing the structure and tone to fit the article. Do not copy old errors, force the same sentence endings, or turn one unusual passage into a universal rule. If reference material is unavailable, state the assessment limit rather than inventing a style profile.

## 2. Evaluate Along Six Axes

These axes define what to examine, not a checklist of mandatory sentence forms. The LLM judges the detailed quality in context using the complete article, its audience and purpose, supplied evidence, and author references.

| Evaluation axis | Guiding question |
| --- | --- |
| **문장의 자연스러움** | Do wording, syntax, and rhythm read naturally at the intended reading level? Does sentence length follow the thought without awkward translation, overloaded clauses, or artificially chopped statements? |
| **문장·문단 연결의 자연스러움** | Can the reader follow why one sentence, paragraph, or section leads to the next? Are the relationships and referents clear, with useful development rather than abrupt shifts or repetition? |
| **주제 전달과 구성의 명확성** | Is the author's central point clear, and does the article fulfill the promise of its title and introduction? Do its structure, emphasis, and conclusion help the reader understand that point? |
| **구체성·근거·설명력** | Do details, examples, and evidence make the reasoning understandable and support the strength of its claims? Can the reader distinguish observed facts, interpretations, and proposals without having to supply missing reasoning? |
| **AI Slop 여부** | Does generic, repetitive, inflated prose obscure the author's reasoning? Do formulaic rhetoric, ornamental labels, empty summaries, or fabricated specificity substitute for actual thought in this passage? |
| **저자 문체·스타일의 일관성** | Does the article retain the author's characteristic way of reasoning and expressing opinions, supported by the reference posts and current preferences? Are its rhythm, vocabulary, examples, and emphasis appropriate to this author and this article? |

Read the whole article across all six axes, including title, excerpt, TL;DR, headings, diagrams, conclusion, and any accompanying translation. A reverse outline can help assess the topic and composition; reading neighboring paragraphs together can expose breaks in flow and repeated forms. Use these methods when useful, not as mandatory output templates.

Use the writing skill's **Three Layers To Check While Writing** as examples of signals and possible repairs, not an exhaustive rubric. A natural passage can still be off-topic or unsupported; a passage free of stock phrases can still lose the author's voice. Conversely, a useful contrast or repeated technical term is not a defect merely because it resembles a listed signal.

Do not assign numerical scores, weights, sentence-length quotas, banned-word counts, or an “AI probability.” Do not require every axis to yield a finding. Judge a defect by the passage's role and effect on this reader, and explain the evidence for that judgment. Preserve a coherent author opinion even when another opinion is possible; do not replace the topic or erase useful detail merely to shorten the article.

Search may locate candidates but cannot establish a defect or a pass. Do not add slang, deliberate errors, forced humor, or fabricated anecdotes to simulate human writing.

## 3. List Concrete Findings Before Fixing

Keep evaluation axis and severity separate: the axis identifies what is affected, while **High / Medium / Low** expresses how much repair is needed. Any axis can produce any severity; do not automatically classify all wording or voice issues as Low.

- **High:** the article fails its central purpose, materially misleads the reader, or distorts the author's intended position. This may arise from a central contradiction, fabricated support, pervasive loss of intelligibility, or a replacement of the author's voice that changes the meaning or stance.
- **Medium:** a meaningful passage or recurring pattern needs correction to meet the intended reading experience or established author style, while the central point remains recoverable. Examples include a missing explanatory step, disruptive flow, materially unnatural phrasing, empty rhetoric that hides the point, or a sustained voice mismatch supported by reference passages and current preferences.
- **Low:** an optional local improvement when meaning, flow, purpose, credibility, and author voice already work. Examples include a small rhythm improvement or removing a redundant word. A merely different but equally effective phrasing may warrant no finding at all.

Use the same criteria in every round. Consider scope, repetition, reader impact, and the author's intent rather than mapping a symptom mechanically to a severity. For voice findings, cite the actual comparison or explicit preference; the reviewer's personal taste alone does not justify Medium. Do not manufacture findings or downgrade unresolved issues merely to pass.

Before edits, briefly summarize the assessment across all six axes and name the author references used. State when an axis has no actionable issue or has an assessment limit; this summary is not a scorecard. Then present concrete findings. This is a progress report, not an approval request; continue with supported fixes in the same task.

Use these columns:

| Severity | Evaluation axis | Location and short excerpt | Evidence and reader/author impact | Proposed change |
| --- | --- | --- | --- | --- |

- Give a file and current line or a section/paragraph locator for conversation text.
- Use one of the six axis names as the primary category. Mention secondary axes when useful, but count the same underlying issue once rather than duplicating it across axes.
- Explain the actual reader problem and a concrete replacement or edit action. Avoid vague findings such as “sounds AI-generated.”
- Put High findings before Medium, then Low. Group instances of one repeated pattern with their locations instead of repeating the same explanation.
- Record all actionable findings, without manufacturing a minimum number. If none are found, say so and summarize what was checked.
- Mark source-dependent issues or out-of-scope changes explicitly. Keep them in the unresolved counts until actually resolved; do not silently omit them to claim a pass.

For report-only requests, finish with findings and suggested rewrites without edits. State the review scope and any uncertainty. Do not claim a fix-and-recheck cycle was completed.

## 4. Fix And Recheck

For tasks that authorize editing:

1. Apply the supported in-scope changes, starting with topic and reasoning, then connections, structure, and expressions. Preserve the useful detail needed to understand the mechanism.
2. Resolve unsupported statements using available evidence. If the author's intended position stays intact, narrow the claim, mark it as a proposal, or remove unsupported embellishment. Never invent a fact, personal experience, causal link, measurement, or outcome to make a sentence concrete.
3. If a necessary repair would change the user's intended thesis or requires an unavailable firsthand fact, finish independent edits and ask only for that missing decision or fact. Report the unresolved passage rather than guessing.
4. Compare the revised text with the original for negation, conditions, quantities, citations, technical meaning, and author position. Update affected diagrams and translations within scope; disclose related material that remains out of scope.
5. Re-read the whole revised article across all six axes, including new issues introduced or exposed by edits. Report each round's remaining High/Medium counts and the new or unresolved findings. Repeat supported fixes and full re-review until the latest article has **High: 0 and Medium: 0**. A finding is resolved only when the revised passage no longer has the stated problem; fixing wording must not introduce a new loss of voice, evidence, or meaning. There is no fixed round limit; neither partial improvement nor a passing lint ends this loop.
6. Run the writing skill's applicable validation on changed article files, including `post-lint.sh` and `git diff --check`. Re-run affected checks after further edits. A passing script does not replace editorial review; disclose unavailable checks accurately.

Low findings alone do not require another round. Apply useful low-risk polish when warranted, but do not churn wording or optimize for zero search matches. If a necessary fix is genuinely blocked by missing evidence, a user decision, or a narrower authorized edit scope, complete independent fixes and report the remaining severity, passage, and needed input. Do not repeat an unchanged blocked review or present it as a completed article.

Before completing, briefly report the fixes made, the final High/Medium/Low counts from the latest full six-axis review, and validation results. Summarize any remaining Low findings and assessment limits. Explicit report-only requests may finish with unresolved High/Medium findings because no edits are authorized; state that distinction. Use a normal review summary, not an “AI-free” guarantee. Do not call self-review independent review unless a separate reviewer actually performed it.
