---
name: haandol-blog-review
description: Review Haandol blog posts for thesis alignment and AI slop in expressions, sentence structure, and sentence connections. Required after drafting, revising, or translating blog copy in conversation or in _posts/, _drafts/, and _en/. List findings, fix supported issues, and re-review; explicit review-only requests remain report-only.
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

## 1. Check The Topic And Argument

Write a short review anchor: the reader's question, the author's current answer, and the intended audience. Infer this from the brief and article when clear; do not ask the user to repeat known context.

Use a reverse outline: describe what each section contributes to the answer. Keep this working outline concise; only surface it when it explains a finding.

Check:

- The title and TL;DR promise what the body actually delivers. The excerpt adds a concise subtitle rather than making a larger claim.
- The introduction establishes a concrete problem before naming a framework. Personal experience appears only when supplied or verified.
- Each section advances the main argument or provides necessary context. Identify missing reasoning, topic drift, duplicated setup, and headings whose contents do not match.
- Examples and diagrams explain the same relationships as the prose; they do not imply unverified effects, ownership, or measurement.
- Claims have the right strength. A reported observation, the author's inference, and a proposed method remain distinguishable. An illustrative case does not become proof of a general result.
- The conclusion answers the original question with the author's resulting position. It does not replay the outline, add an unsupported promise, or evade the author's judgment with a generic hedge.
- An accompanying translation preserves the thesis, qualifications, and terminology without reproducing awkward noun chains.

Preserve a coherent author opinion even when another opinion is possible. Do not redefine the topic, replace the author's position, or remove a necessary explanation merely to make the post shorter.

## 2. Check Connections, Structure, And Expressions

Apply all three layers in the writing skill's **Three Layers To Check While Writing**, in this order:

1. **Connections:** identify the new contribution of each sentence and paragraph; check premises behind conclusions, referents of pronouns, and consistent names for the same concept.
2. **Sentence structure:** check cause-and-effect and condition-and-action relationships, broken sentence rhythm, long chains with changing actors, repeated contrasts, and forced symmetry.
3. **Expressions:** check unsupported praise, abstract noun chains, filler, ornamental labels, and generic uncertainty. Prefer supported subjects and actions.

Read neighboring paragraphs together and scan the whole article for repeated openings, endings, definitions, transitions, and section templates. Include headings and diagram labels, not just body paragraphs.

Search may locate candidates but cannot establish a defect or a pass. Do not report a phrase solely because it appears in the signal list. Keep useful contrasts, lists, repeated technical terms, and specific uncertainty. Do not score “humanlikeness,” enforce sentence-length quotas, or add slang, deliberate errors, or fabricated anecdotes.

## 3. List Concrete Findings Before Fixing

Assign severity by the effect on the reader, not by whether a signal word appears:

- **High:** the article materially misleads the reader or fails its central promise. Examples include a thesis/body contradiction, a fabricated experience or result, a conclusion resting on an unsupported causal claim, or a rewrite that changes the author's position or technical meaning.
- **Medium:** a passage materially impairs comprehension or the argument while the central thesis remains recoverable. Examples include a missing explanatory step, an ambiguous referent or changing term that confuses the subject, repeated structures that obscure relationships, or abstract and inflated prose that hides the actual action or evidence.
- **Low:** optional local polish that does not change meaning, evidence, topic alignment, or the reader's ability to follow the explanation. Examples include a minor rhythm improvement or a redundant word in an otherwise clear passage.

Use the same criteria in every round. A pattern repeated across the article may have greater impact than one isolated occurrence. Do not manufacture findings, downgrade unresolved issues merely to pass, or treat personal stylistic preference as Medium.

Present a concise findings table in the conversation before edits. This is a progress report, not an approval request; continue with supported fixes in the same task.

Use these columns:

| Severity | Location and short excerpt | Category | Why it matters | Proposed change |
| --- | --- | --- | --- | --- |

- Give a file and current line or a section/paragraph locator for conversation text.
- Use `주제·논리`, `연결`, `구조`, or `표현` as the category.
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
5. Re-read the whole revised article for topic alignment and all three layers, including new issues introduced or exposed by edits. Report each round's remaining High/Medium counts and the new or unresolved findings. Repeat supported fixes and full re-review until the latest article has **High: 0 and Medium: 0**. A finding is resolved only when the revised passage no longer has the stated problem. There is no fixed round limit; neither partial improvement nor a passing lint ends this loop.
6. Run the writing skill's applicable validation on changed article files, including `post-lint.sh` and `git diff --check`. Re-run affected checks after further edits. A passing script does not replace editorial review; disclose unavailable checks accurately.

Low findings alone do not require another round. Apply useful low-risk polish when warranted, but do not churn wording or optimize for zero search matches. If a necessary fix is genuinely blocked by missing evidence, a user decision, or a narrower authorized edit scope, complete independent fixes and report the remaining severity, passage, and needed input. Do not repeat an unchanged blocked review or present it as a completed article.

Before completing, briefly report the fixes made, the final High/Medium counts from the latest full review, and validation results. Mention remaining Low findings when useful. Explicit report-only requests may finish with unresolved High/Medium findings because no edits are authorized; state that distinction. Use a normal review summary, not an “AI-free” guarantee. Do not call self-review independent review unless a separate reviewer actually performed it.
