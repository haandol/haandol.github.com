---
name: haandol-blog-writing
description: Write, revise, or review Korean technical blog posts for the Haandol Jekyll repository. Use for `_posts/*.md` and `_drafts/*.md` work involving logical flow, author voice, AI-slop removal, terminology, citations, diagrams, or publication validation.
---

# Haandol Blog Writing

Read the repository `AGENTS.md` before editing. Preserve its front matter, title, TL;DR, file, image, and Jekyll conventions.

## Workflow

1. Read the entire target post and identify its thesis, audience, and epistemic status.
2. Read 2-4 related recent posts before changing definitions, terminology, or the author's recurring argument. Prefer internal links for ideas already established elsewhere.
3. Separate conceptual overview, organizational execution, and evaluation. Keep each detail in the section whose title promises it.
4. Edit paragraphs and diagrams together so both express the same causal model.
5. Run the "Remove AI Slop" prose pass across the whole post, including the title, excerpt, TL;DR, headings, and conclusion. For review-only requests, report specific passages and suggested rewrites without editing.
6. Validate Markdown, Liquid, diagrams, links, and Git diff before finishing.

## Build The Argument

- State the problem before naming the framework proposed to solve it.
- Do not use framework terms before defining them. In an introductory section, explain the underlying concept without later labels such as `Shape`, `AHEAD`, or `LEVER`.
- Keep an overview section concise. Move mechanisms, examples, organizational roles, and diagrams into a later detail section.
- Make a section's internal structure match its title. A section promising `3S` must explain `Streamlining`, `Shape`, and `Scale` in that order.
- Preserve detail where the causal mechanism matters. Do not over-compress concrete explanations of short-term incentives, trial and error, or operational work.
- Remove repeated setup, ornamental naming explanations, and meta-commentary that does not advance the thesis.
- Prefer explicit causal chains:
  `evaluation criterion -> locally rational behavior -> organizational consequence`.
- When a diagram or paragraph contrasts approaches, show both the failure mode and the proposed correction.
- Treat boundaries carefully. Do not assume team, system, domain, and bounded-context boundaries coincide.

## Match The Author's Voice

- Write short Korean paragraphs, usually one or two sentences.
- Present personal interpretations as opinions: use `생각한다`, `가정한다`, `볼 수 있다`, or `지표로 삼아볼 수 있다` where needed to establish their status. Do not append the same hedge to every sentence in an already qualified paragraph.
- Avoid `나는 ... 본다` when `...라고 생각한다` reads more naturally.
- Avoid aggressive or universal claims unless a cited source establishes them or the user explicitly confirms firsthand knowledge.
- Allow a deliberate logical leap when it follows the post's stated vision. Mark it as a hypothesis, conceptual model, or assumption rather than a measured result.
- Avoid `모르겠다`, `잘 모르겠다`, `판단하기 이르다`, or similar expressions that evade the author's position. State what the author currently thinks, even when it is provisional.
- Put uncertainty after the opinion and tie it to a specific limitation. Prefer `지금은 A가 더 낫다고 생각한다. 다만 B에서는 아직 확인이 필요하다` over generic statements about experimenting, insufficient evidence, or withholding judgment.
- Separate observation, inference, and proposal:
  - observation: cite evidence;
  - inference: explain the causal link;
  - proposal: state that it is the author's lens or suggestion.
- Preserve direct wording for facts the user explicitly says can be stated without qualification.

## Remove AI Slop

Treat AI slop as an editorial problem: generic, repetitive, inflated prose that obscures the author's reasoning. Do not claim to detect AI authorship from wording.

Before finishing a draft or revision, compare it with at least two older posts by the author, not only recent AI-related posts. Reuse posts already read when suitable. Match their directness, paragraph rhythm, and specificity without copying old factual claims, typos, or mannerisms.

### Review Signals

Treat the following as review signals, not automatic errors:

- repeated contrast templates such as `단순히 A가 아니라 B다`, `A가 아니다. B다`, or `이것은 X 이상의 의미다`, especially when A was never a plausible claim in the discussion;
- stock openings and reader-address filler such as `빠르게 변화하는 시대에`, `오늘날 그 어느 때보다`, `함께 살펴보자`, or `여러분도 경험해 보았을 것이다`;
- unsupported significance claims such as `혁신적인`, `획기적인`, `패러다임을 바꾼다`, or `새로운 가능성을 열어준다`;
- abstract noun chains such as `효율성 극대화를 통한 가치 창출`, and padded constructions such as `개선을 수행한다` or `중요하다고 할 수 있을 것이다`;
- ornamental English labels for ideas that are used only once, especially title-cased names such as `Human Decision Surface`, `Comprehension Bandwidth`, or `Evidence Package`;
- symmetrical `첫째/둘째/셋째` manifestos, question-and-answer hooks, or identical problem/solution/lesson templates repeated in every section;
- introductions that define a framework before showing the personal problem that made it useful;
- tables, diagrams, blockquotes, or bold sentences that merely repeat the adjacent prose;
- generic bridge phrases repeated across sections, such as `핵심은`, `중요한 것은`, `이 관점에서`, `결국`, and `방향은 분명하다`;
- conclusions that replay every section, add a generic call to action, or sound more certain than the evidence developed in the body;
- personal anecdotes, project details, measurements, or outcomes inferred by the model rather than supplied by the user or verified in the repository.

### Revise In Context

1. Check each paragraph's contribution. Delete or merge it if it adds no fact, causal explanation, useful example, or author judgment. Preserve the required TL;DR and conclusion, but let the conclusion state the author's resulting position rather than recap the outline.
2. Replace vague claims with the actor, action, affected object, and consequence supported by the material. If a sentence could appear unchanged in an unrelated technical post, make its connection to this case explicit or remove it.
3. State the intended claim directly. Keep a contrast when it resolves an actual misconception or explains a technical tradeoff; otherwise remove the invented opposing claim. Use transitions that explain why one paragraph follows another.
4. Read neighboring paragraphs together for repeated openings, endings, rhetorical questions, and punchlines. Let explanation length follow the reasoning. Keep short paragraphs, but do not turn every sentence into a standalone slogan or force every section into the same shape.
5. Check factual strength after rewriting. Preserve negation, conditions, quantities, citations, established technical terms, and the distinction between observation, inference, and proposal. Do not invent a personal experience, failure, measurement, or project detail to make the prose sound human. Label hypothetical examples as hypothetical.

Start from a supplied experience, annoyance, failed attempt, or concrete project situation when available. Otherwise introduce the concrete problem without pretending the author experienced it. Explain one useful example far enough that the reader can follow the reasoning.

Keep useful parenthetical qualifications and specific uncertainty. Do not add slang, typos, forced humor, or artificial roughness. Use Korean descriptions first; retain established technical terms and coined terms that actually carry a reused distinction. Reserve bold emphasis for the few claims the reader needs to remember.

These examples show editing decisions, not replacement templates. The concrete details in a rewrite must already be supported by the target material:

| Before | After / decision |
| --- | --- |
| `이제 이 혁신적인 접근법의 핵심을 함께 살펴보자.` | Delete the preview and begin the explanation. |
| `단순히 테스트를 추가하는 것이 아니다. 신뢰를 설계하는 것이다.` | `배포 전에 같은 입력으로 테스트를 반복해 회귀 오류를 확인한다.` — only if this is the actual process. |
| `운영 효율성 극대화를 통한 개발자 경험 개선을 도모한다.` | `배포 스크립트를 하나로 묶어 개발자가 실행할 명령을 줄인다.` — only if the source describes this change. |
| `캐시는 원본 데이터가 아니다. 만료되거나 삭제될 수 있다.` | Keep when this distinction explains the failure being discussed. |

Use search to find candidates, then read the full post to catch structural repetition that search misses:

```bash
POST=_posts/YYYY-MM-DD-slug.md
rg -n '단순히|그저|핵심은|중요한 것은|이 관점에서|첫째|둘째|셋째|결국|방향은 분명|함께 살펴|여러분도|빠르게 변화|그 어느 때보다|혁신적|획기적|패러다임|가능성을 열|극대화|가치 창출|도모|할 수 있을 것이다|모르겠다|잘 모르|[A-Z][A-Za-z]+ (Surface|Bandwidth|Package|Framework)' "$POST"
```

Substitute the actual post path. A search exit code of 1 means no candidates were found, not that the prose passed review. Do not optimize for zero matches or add these signals as hard failures in `post-lint.sh`; judge their purpose in context.

## Write Concise Front Matter

- Keep `excerpt` in English, but treat it as a short subtitle for post lists rather than an abstract.
- Prefer one clause of roughly 6-12 words. If it starts listing the argument, methods, and conclusion, keep only the central question or payoff.
- Avoid repeating the Korean title word for word. Let the title provide the hook and the excerpt clarify the thesis.

## Choose Natural Terminology

- Keep established framework names and technical terms in English when translation would reduce precision.
- Translate isolated English process jargon when ordinary Korean is clearer:
  - `eval` -> `평가`, `평가 체계`, `평가 기준`, `평가 사례`, or `평가 데이터셋` according to context;
  - stage `gate` -> `다음 단계로 넘어가는 기준`;
  - preserve exact English only inside source quotations such as `Start with evals`.
- Do not mix English and Korean merely for novelty. Keep terminology consistent across prose, tables, and diagrams.
- Prefer concrete business language such as `비즈니스 요구사항에 필요한 데이터를 조회·조작한다` over abstract cost or outcome jargon.

## Design Diagrams

Use a diagram only when it reveals a relationship that prose makes hard to scan.

### Mermaid

Use Mermaid for processes, ownership, comparisons, feedback loops, and relationships.

- Wrap every Mermaid block in `{% raw %}` and `{% endraw %}`.
- For organizational problems, show the current failure path before the intended workflow.
- Keep node text concise and ensure the diagram does not assume the conclusion.
- Make labels in the diagram use the same terminology as the surrounding prose.

### SVG

Use a static SVG for curves, axes, thresholds, maturity bands, or other graph-like conceptual models.

- Match existing files such as `assets/img/2026/0615/3x-curve.svg` and `3s-curve.svg`.
- Default to a `720x380` viewBox, system font stack, white background, restrained phase bands, and readable axis labels.
- Make axis direction intuitive. For example, place low available resources on the left and high resources on the right.
- If the thesis depends on a threshold or sweet spot, draw and label it rather than implying a symmetric curve.
- State in prose or the title that a non-measured curve is a conceptual model.
- Keep labels inside their bands at mobile and desktop sizes.
- Render the SVG before finishing:

```bash
rsvg-convert -w 1440 -h 760 path/to/chart.svg -o /tmp/chart.png
```

Inspect the rendered PNG for clipping, overlap, axis direction, and semantic consistency.

## Cite Evidence

- Use footnotes for external evidence and internal related posts.
- Prefer official or primary sources for product behavior, company practices, benchmarks, and frameworks.
- Link previous Haandol posts when they establish the definition or vision used by the current post.
- Do not present a conceptual curve, proposed index, or maturity model as validated evidence.

## Validate

Most mechanical checks are scripted. Run the script first — it covers the TL;DR bullet cap,
Mermaid `{% raw %}` wrapping, fence balance, internal link form, footnote correspondence,
required front matter, and image existence:

```bash
.agents/scripts/post-lint.sh _posts/YYYY-MM-DD-slug.md
```

A `PostToolUse` hook runs the same script on every `_posts/`/`_drafts/` edit, so a violation
surfaces immediately rather than at review time. Do not treat a passing script as a substitute
for the judgment checks listed after the commands below.

Then run the remaining checks that the script does not cover:

Substitute the real path for `$POST` in each command. Every line below is copy-paste runnable — do not add extra backslash escaping, which silently turns `\b` into a literal and makes `rg` fail to parse or fail to match.

```bash
POST=_posts/YYYY-MM-DD-slug.md

git diff --check

# Liquid/fence balance — raw must equal endraw, and total fences must be even
echo "raw=$(rg -c '^\{% raw %\}$' "$POST") endraw=$(rg -c '^\{% endraw %\}$' "$POST") mermaid=$(rg -c '^```mermaid$' "$POST") fences=$(rg -c '^```' "$POST")"

# Leftover jargon / placeholders — exit 1 means clean
rg -n 'eval|\bgate\b|TODO|TBD' "$POST"

# Internal links must use the .html form — must print 0
rg -oN --no-filename '\]\(/20[0-9]{2}/[0-9]{2}/[0-9]{2}/[a-z0-9-]+/\)' "$POST" | wc -l

# Footnote refs vs definitions — the two lists must correspond
rg -oP '\[\^[0-9]+\](?!:)' "$POST" | sort -u
rg -o '^\[\^[0-9]+\]:' "$POST"
```

Also verify:

- the AI-slop prose pass is complete; rewrites preserve factual meaning and the author's position without fabricated detail;
- required front matter exists and `excerpt` is English;
- every `_en/` translation has `last_modified_at` set to its actual English
  publication or meaningful revision time; update Korean `last_modified_at`
  only for meaningful content revisions;
- `excerpt` is a concise subtitle, normally one clause of roughly 6-12 words;
- TL;DR has at most three short, single-clause bullets;
- section headings and their contents agree;
- Mermaid/raw and code-fence counts balance (`raw == endraw`, `fences` even);
- every footnote definition is actually referenced in the body, and vice versa;
- internal post links end in `.html` (see AGENTS.md "Internal Post Links") — the slash form 404s;
- referenced images exist;
- SVGs render correctly;
- Jekyll builds when the required Bundler version is available. This repo's `Gemfile.lock` pins Bundler 2.6.8, which is absent under the system Ruby 2.6 — when `bundle exec jekyll build` cannot run, say so explicitly rather than implying the build passed, and lean on the checks above.

Do not commit or push unless the user explicitly asks.
