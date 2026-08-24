---
name: haandol-linkedin-writing
description: Write, revise, or review Korean LinkedIn posts for Haandol from a repository post, draft, or firsthand engineering experience. Use for LinkedIn copy that must remain self-contained even when nobody clicks the link, with a short anecdotal hook and the source insights stated directly. Do not use for editing the blog article itself.
---

# Haandol LinkedIn Writing

Read the repository `AGENTS.md` before writing. When the post is based on a
repository article, read the entire source article before drafting.

## Goal

Produce a concise Korean LinkedIn post that communicates the insight by itself.
The link is optional supporting material, not missing context that the reader
must open.

The author's firsthand experience establishes where the insight came from and
helps the reader relate. It is not the main subject of the post.

## Use the Source Carefully

- Preserve only experiences, numbers, outcomes, and project details supplied by
  the user or present in the repository. Never invent a personal anecdote.
- When the author deliberately departed from their normal workflow, explain why
  if that choice caused the result. For example, improved models and tools may
  explain why several Features were delegated as one Goal.
- Separate observation, interpretation, and the general lesson. Do not present a
  conceptual model as measured evidence.
- If the user's latest explanation differs from an older draft, use the latest
  explanation.

## Shape the Post

1. Open with a concrete experience in roughly 10–20% of the post. Normally this
   is two to four short paragraphs.
2. Move from the experience to the causal mechanism. Explain what happened and
   why it matters beyond the individual case.
3. State two to four load-bearing insights from the source article. The reader
   must understand them without opening the link.
4. End with a general decision rule or implication. Do not end with a personal
   resolution such as `앞으로는 ... 하려 한다` unless the user explicitly asks
   for one.
5. If a link is included, put the URL alone on the final line.

Prefer a clear causal sequence over a forced numbered manifesto. Use a list only
when it materially improves scanning.

## Keep the Experience in Its Role

- Use the anecdote as evidence and common ground, then leave it behind.
- Do not continue narrating the author's feelings or plans after the insight
  section begins.
- Do not make the post primarily about a failed project, productivity, or the
  author's personal learning journey when the intended subject is a general
  engineering principle.
- Include enough context to make the experiment fair. If the code worked but the
  requirements changed after using the PoC, say so; do not imply the model simply
  failed.

## Make It Stand Alone

- Include the article's central reasoning, not a teaser or table of contents.
- Explain important limits and trade-offs. A workaround such as Stacked PR
  should not be presented as a complete solution when surrounding context still
  creates review load.
- Preserve useful analogies when they carry the argument, such as several small
  hills versus one large mountain with the same cumulative height.
- Connect the insight to a practical strategy. For AI implementation, this may
  mean selecting scope from acceptable human cognitive load, workload risk, and
  contract/test evidence rather than the model's maximum output.

## Match the Author's Voice

- Write short paragraphs, usually one or two sentences.
- Use direct Korean and retain established technical terms such as Agent, ADR,
  Vertical Slice, Stacked PR, Goal, and diff when they improve precision.
- Keep useful rough edges and concrete details. Do not polish every paragraph
  into a slogan.
- Avoid generic LinkedIn performance: no engagement bait, rhetorical questions,
  emojis, motivational ending, or hashtags unless the user asks.
- Do not add a title by default.

## Remove AI Slop

Treat these as rewrite signals:

- `단순히 A가 아니라 B다`, `A가 아니다. B다`, and repeated symmetrical
  contrasts;
- `핵심은`, `중요한 것은`, `결국`, or similar bridge phrases used as filler;
- forced `첫째/둘째/셋째` structure;
- abstract declarations that repeat the preceding example;
- a conclusion more certain than the source;
- personal pledges such as `앞으로는 ... 하겠다` when the intended output is
  insight sharing;
- link introductions such as `관련 내용을 정리했다`, `자세한 내용은`, or
  `그래프와 함께 설명했다`.

Do not optimize for eliminating every occurrence. Keep a phrase when it is
natural and necessary.

## Link Rules

- The post must remain complete if the reader never clicks.
- Put the URL alone on the final line. Do not introduce, describe, or promote it.
- Do not write `관련 글`, `더 자세한 내용`, `읽어보세요`, or a call to action.
- For a published local post, verify `publish: true` and construct the URL as
  `https://haandol.github.io/YYYY/MM/DD/slug.html`.
- Omit the link rather than inventing a placeholder.

## Final Pass

Before returning the post, verify:

- the anecdote is only the opening source of the insight;
- the reason for any unusual experiment is understandable;
- the post's main argument is complete without the link;
- the insights match the source article rather than becoming generic AI advice;
- the ending is a general decision criterion, not the author's future plan;
- no facts or outcomes were invented;
- the URL, when present, is alone on the final line.
