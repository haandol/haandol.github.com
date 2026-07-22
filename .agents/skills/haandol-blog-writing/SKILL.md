---
name: haandol-blog-writing
description: Write, revise, or review Korean technical blog posts for the Haandol Jekyll repository. Use for `_posts/*.md` and `_drafts/*.md` work involving logical flow, section structure, personal-opinion tone, terminology, citations, Mermaid diagrams, conceptual SVG charts, or publication validation.
---

# Haandol Blog Writing

Read the repository `AGENTS.md` before editing. Preserve its front matter, title, TL;DR, file, image, and Jekyll conventions.

## Workflow

1. Read the entire target post and identify its thesis, audience, and epistemic status.
2. Read 2-4 related recent posts before changing definitions, terminology, or the author's recurring argument. Prefer internal links for ideas already established elsewhere.
3. Separate conceptual overview, organizational execution, and evaluation. Keep each detail in the section whose title promises it.
4. Edit paragraphs and diagrams together so both express the same causal model.
5. Validate Markdown, Liquid, diagrams, links, and Git diff before finishing.

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
- Present personal interpretations as opinions: use `생각한다`, `가정한다`, `볼 수 있다`, or `지표로 삼아볼 수 있다`.
- Avoid `나는 ... 본다` when `...라고 생각한다` reads more naturally.
- Avoid aggressive or universal claims unless a cited source establishes them or the user explicitly confirms firsthand knowledge.
- Allow a deliberate logical leap when it follows the post's stated vision. Mark it as a hypothesis, conceptual model, or assumption rather than a measured result.
- Separate observation, inference, and proposal:
  - observation: cite evidence;
  - inference: explain the causal link;
  - proposal: state that it is the author's lens or suggestion.
- Preserve direct wording for facts the user explicitly says can be stated without qualification.

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

Run the relevant checks before reporting completion:

```bash
git diff --check
rg -n '^\\{% raw %\\}$|^\\{% endraw %\\}$|^```mermaid$|^```$' path/to/post.md
rg -n 'eval|\\bgate\\b|TODO|TBD' path/to/post.md
```

Also verify:

- required front matter exists and `excerpt` is English;
- TL;DR has at most three short, single-clause bullets;
- section headings and their contents agree;
- Mermaid/raw and code-fence counts balance;
- footnote references and definitions match;
- referenced images exist;
- SVGs render correctly;
- Jekyll builds when the required Bundler version is available.

Do not commit or push unless the user explicitly asks.
