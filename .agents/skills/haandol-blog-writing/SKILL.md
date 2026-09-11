---
name: haandol-blog-writing
description: Write or revise Haandol technical blog posts and their English translations with the author's voice, clear reasoning, and AI-slop prevention. Use for blog copy in conversation or in _posts/, _drafts/, and _en/. Finish every drafting or revision task with haandol-blog-review; route review-only requests there.
---

# Haandol Blog Writing

Read the repository `AGENTS.md` before editing. Preserve its front matter, title, TL;DR, file, image, and Jekyll conventions.

## Workflow

1. Read the entire target post or supplied material. Identify the reader's question, the author's answer, the audience, and which claims are observations, inferences, or proposals. For review-only requests, use [haandol-blog-review](../haandol-blog-review/SKILL.md) in report-only mode.
2. Read 2-4 related recent posts before changing definitions, terminology, or the author's recurring argument. Also compare at least two older author posts for voice; reuse suitable posts already read. Prefer internal links for ideas established elsewhere.
3. Draft toward that question and answer. Separate conceptual overview, organizational execution, and evaluation. Keep each detail in the section whose title promises it.
4. Apply "Remove AI Slop" and "Write for Junior Developers and Interested Non-Developers" while composing, not only after drafting. Edit paragraphs and diagrams together so they express the same causal model.
5. After every draft, prose revision, or translation, read and execute [haandol-blog-review](../haandol-blog-review/SKILL.md). Cover the whole article, including title, excerpt, TL;DR, headings, diagrams, conclusion, and an accompanying translation. List findings, apply supported fixes within the user's scope, and re-review without asking for routine approval. This also applies to blog copy written in conversation.
6. Repeat the review's fix-and-recheck loop until a full review of the latest article finds **High: 0 and Medium: 0**, using the severity definitions in the review skill. Review is mandatory even for an apparently clean first draft. Do not stop after listing suggestions, one round of fixes, or an arbitrary number of rounds. Low findings alone do not block completion.
7. Complete the applicable validation below, then report the fixes and final High/Medium counts. If a real source, permission, or author-decision blocker prevents resolving a finding, finish independent work and state the unresolved finding and needed input; do not call the article complete or count the finding as resolved.

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

- Keep paragraphs focused, with sentence length and breaks following the thought. A compact paragraph can contain a naturally connected sentence; do not chop it into short declarations to meet a sentence-length or sentence-count target.
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
- Treat the user's supplied firsthand details as source material. Do not remove or turn them into hypothetical examples merely because a shorter brief does not repeat them. Investigate actual contradictions or details identified as unverified or model-invented; absence from a summary alone is not evidence of fabrication.

## Remove AI Slop

Treat AI slop as an editorial problem: generic, repetitive, inflated prose that obscures the author's reasoning. Do not claim to detect AI authorship from wording.

Use the older author posts read in the workflow to match directness, paragraph rhythm, and specificity without copying old factual claims, typos, or mannerisms. Human writing here means a recognizable judgment, supported detail, and connected reasoning; it does not mean adding invented experiences or artificial imperfections.

### Three Layers To Check While Writing

The signals below prompt contextual review; they are not automatic errors or an AI-authorship test. Review connections first, then sentence structure, then expressions, so polishing words does not conceal an unsupported argument.

**Expressions — name the actor, action, object, and supported consequence.**

- Replace unsupported significance claims (`혁신적인`, `획기적인`, `패러다임을 바꾼다`, `새로운 가능성을 열어준다`) with a verified change or remove them. Swapping one grand adjective for another is not a fix.
- Unpack abstract noun chains such as `효율성 극대화를 통한 가치 창출`. Restore verbs in padded constructions such as `검토를 수행한다`; if `개선한다` is still vague, name what changes.
- Delete stock openings and reader-address filler (`빠르게 변화하는 시대에`, `오늘날 그 어느 때보다`, `함께 살펴보자`, `여러분도 경험해 보았을 것이다`) when they add no context.
- State the author's judgment directly instead of `중요하다고 할 수 있을 것이다`. Retain uncertainty that names an actual condition or limitation.
- Remove ornamental English labels used only once, such as `Human Decision Surface`, `Comprehension Bandwidth`, or `Evidence Package`. Preserve established terms and names needed for a recurring distinction.
- Ask whether a sentence could move unchanged into an unrelated article. If so, connect it to this case using supported detail or remove it.

**Sentence structure — let the reasoning determine the shape and length.**

- Review repeated contrasts (`단순히 A가 아니라 B다`, `A가 아니다. B다`, `이것은 X 이상의 의미다`). Keep them when they resolve a real misconception or tradeoff; otherwise state the intended claim directly.
- Replace consecutive dictionary definitions (`A는 …다. B는 …다. C는 …다.`) with an explanation of why the next concept is needed here.
- Keep a condition and its action, or a cause and its consequence, together when naturally readable. Do not chop connected reasoning into standalone slogans and then add a sentence restating the relationship.
- Split long `~하며, ~하고, ~함으로써` chains where the actor or subject changes. Make sequence, conditions, and causality explicit; do not join sentences merely to vary length.
- Avoid forcing every section into `첫째/둘째/셋째`, a rhetorical question and answer, or the same problem/solution/lesson template. Useful lists and short emphasis remain valid.

**Connections — carry forward a known subject and add useful information.**

- For neighboring sentences, identify what the later one adds: evidence, example, condition, consequence, distinction, or author judgment. When no relationship exists, reorder, supply supported reasoning, or remove the detour.
- Check `또한` and `더 나아가` for accumulation without progress. Check `따라서`, `결국`, and `방향은 분명하다` for conclusions the preceding material does not establish. A smoother connector cannot repair a missing premise.
- Resolve ambiguous `이는`, `이러한 접근`, and `이 관점에서` by naming the relevant subject. Keep core terms consistent instead of cycling through synonyms for variety.
- Start from information the reader already has when it helps the transition, then add something new. Do not treat this as a fixed word-order template.
- Keep `즉` and `다시 말해` only when the restatement clarifies, narrows, or illustrates the point. Remove repeated bridges such as `핵심은` and `중요한 것은` when they add only emphasis.
- Apply the same test between paragraphs and sections. Introduce the concrete problem before a framework, remove tables or diagrams that merely duplicate prose, and let the conclusion state the resulting position within the body's evidence.

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

## Write for Junior Developers and Interested Non-Developers

The author does not normally use academic or grand language. Assume the reader is a junior developer or someone interested in software development who does not work as a developer. They should understand the argument without following links to learn the vocabulary.

- Prefer familiar words and a visible actor doing something: who checks what, why, and what happens next. Replace abstract noun chains with actions rather than exchanging one difficult noun for another.
- Easy language does not mean short sentences. Keep a cause and its consequence, a condition and its action, or a point and its immediate explanation together when they read naturally. Split only when the subject changes, the idea turns, or the reader would otherwise lose the thread; do not mechanically join every sentence either.
- Explain the relationship between concepts in the article's context instead of producing a row of dictionary definitions. Do not repeat that relationship again in a summary sentence. Read neighboring sentences aloud and repair repeated endings, isolated setup lines, and stop-start rhythm while keeping the vocabulary accessible.
- Explain an unfamiliar term or acronym briefly on first use, in the sentence where it matters. Expanding the English acronym alone is not an explanation. Retain a technical name when it is needed later or helps readers find the source; omit incidental jargon when ordinary words carry the meaning.
- Explain metaphors such as `경계`, `계약`, `부채`, and `루프` through the actual behavior in that passage. A familiar word used as specialist shorthand still needs context.
- Paraphrase sources in the author's plain voice. Do not carry over expressions such as `신뢰의 초석`, `협업형 승인 사이클`, `기본 형태로 수렴`, or `인과적 효과` merely because they sound authoritative. Preserve the source's reason, scope, conditions, and strength of claim. Keep literal quotations visibly distinct from paraphrases.
- Check headings, tables, diagram labels, and footnote descriptions as well as prose. A simplified paragraph does not help if its diagram introduces unexplained jargon again. English translations should read naturally at the same level, not reproduce Korean noun chains.
- Read the result as a newcomer: can the reader say what is happening and why? If not, name the missing actor or action, define the necessary term, or use a concrete example already supported by the article. This requires editorial judgment, not a banned-word list or a fixed sentence-length limit.

Examples show the intended reading level, not mandatory replacements:

| Before | Plain-language version |
| --- | --- |
| `공식 글도 HITL을 신뢰, 책임과 정확성의 초석으로 두고 모든 단계에 협업형 승인 사이클을 요구한다.` | `공식 글도 AI의 결과를 믿고 쓸 수 있는지, 누가 책임지는지, 결과가 정확한지를 확인하려면 사람이 필요하다고 설명한다. 그래서 모든 단계에서 팀이 함께 결과를 검토하고 승인하도록 한다.` |
| `앞으로 프로덕션 개발이 수렴할 기본 형태` | `앞으로 실제 서비스를 개발하는 방식` |
| `전체 방법론의 인과적 효과를 증명하지는 않는다` | `그 성과가 방법론 전체 덕분이라고 단정할 수는 없다` |
| `컨셉은 어떤 미래를 목표로 하는지다. 프로세스는 그 목표를 향해 일을 어떻게 나누고 반복하는지다. 구현은 그 일하는 방식을 실제 도구와 실행 환경에 어떻게 담는지다.` | `어떤 미래를 목표로 하느냐에 따라 일을 나누고 반복하는 방식이 달라지고, 그 차이는 실제 도구와 실행 환경을 만드는 방식에도 이어진다.` |

## Choose Natural Terminology

- Keep established framework names and technical terms in English when translation would reduce precision.
- Translate isolated English process jargon when ordinary Korean is clearer:
  - `eval` -> `평가`, `평가 체계`, `평가 기준`, `평가 사례`, or `평가 데이터셋` according to context;
  - stage `gate` -> `다음 단계로 넘어가는 기준`;
  - preserve exact English only inside source quotations such as `Start with evals`.
- Do not mix English and Korean merely for novelty. Keep terminology consistent across prose, tables, and diagrams.
- Prefer concrete business language such as `업무에 필요한 데이터를 찾아 읽거나 바꾼다` over abstract cost or outcome jargon.

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

- a junior developer or interested non-developer can follow the argument without looking up unexplained terminology; source paraphrases and English translations use the same plain reading level and natural sentence flow, rather than chopping explanations into short statements;
- the AI-slop prose pass is complete; rewrites preserve factual meaning and the author's position without fabricated detail;
- `haandol-blog-review` has listed findings with severity, applied supported in-scope fixes, and reviewed the latest whole article for thesis alignment, connections, structure, and expressions until High and Medium findings both reach zero; an explicit review-only request reports findings without editing;
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
