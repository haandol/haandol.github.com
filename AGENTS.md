# Haandol Blog Project Guide

This file acts as a living wiki for the repository.
Use it to quickly understand the project layout, common tasks and key documentation.

## Overview

Haandol is a Korean tech blog built on Jekyll and hosted via GitHub Pages.
Topics include AI/ML, AWS, software engineering, startup/lean startup, and more.

- **Site URL**: https://haandol.github.io
- **Author**: DongGyun Lee (haandol)
- **Theme**: Hyde (based on Poole)

## Repository Structure

### Core Directories

- **`_posts/`** – Blog posts (Markdown)
  - Filename convention: `YYYY-MM-DD-slug-title.md`
  - Must include front matter (layout, title, excerpt, author, email, tags, publish)
- **`_drafts/`** – Work-in-progress drafts (pre-publish)
- **`_layouts/`** – HTML layout templates
  - `default.html` – Base layout (Google Analytics, sidebar)
  - `post.html` – Post layout (tags, date, related posts)
  - `page.html` – Generic page layout
- **`_includes/`** – Reusable HTML components
  - `head.html` – HTML head tag
  - `sidebar.html` – Sidebar navigation
  - `comments.html` – Comment system
- **`public/css/`** – Stylesheets
  - `poole.css` – Base styles
  - `hyde.css` – Hyde theme styles
  - `syntax.css` – Code highlighting
- **`assets/img/`** – Image assets
  - Directory convention: `assets/img/YYYY/MMDD/` (e.g., `assets/img/2026/0205/`)
  - Older posts may use `assets/img/YYYYMMDD/` format
- **`_site/`** – Jekyll build output (should not be tracked by git)

### Configuration Files

- **`_config.yml`** – Jekyll site configuration
- **`Gemfile`** – Ruby dependencies (github-pages, jekyll-sitemap, jekyll-feed, jekyll-paginate)
- **`about.md`** – About page

## Development Commands

### Local Server

```bash
bundle install
bundle exec jekyll serve --watch
```

### Serve with Drafts

```bash
bundle exec jekyll serve --watch --drafts
```

## Technology Stack

- **Static Site Generator**: Jekyll (GitHub Pages)
- **Theme**: Hyde (based on Poole)
- **Markdown Engine**: kramdown
- **Syntax Highlighter**: rouge
- **Plugins**: jekyll-sitemap, jekyll-feed, jekyll-paginate
- **Language**: HTML (ko-kr), Markdown, CSS/SCSS, Liquid

## Blog Post Conventions

### Front Matter Format

```yaml
---
layout: post
title: Post title in Korean
excerpt: English excerpt for the post
author: haandol
email: ldg55d@gmail.com
tags: tag1 tag2 tag3
publish: true
---
```

### Post Structure Pattern

1. **TL;DR** – Key takeaways as bullet points
2. **시작하며 (Introduction)** – Background and personal experience leading to the topic
3. **Body sections** – Numbered sections (`## 1. Title`, `## 2. Title`)
4. **마치며 (Conclusion)** – Wrap-up with personal opinion
5. **Footnotes** – Reference links using `[^1]` format

### Writing Style

- Written in Korean; technical terms remain in English
- Essay style with personal experience and opinions
- Explanations use analogies and real-world examples
- **Bold** for key messages
- Code blocks and images used where appropriate

### Image Insertion

```markdown
![description](/assets/img/YYYY/MMDD/filename.png)
```

## Agent-specific Instructions

### Safe to Modify

- Post files in `_posts/`
- Draft files in `_drafts/`
- `about.md`
- `README.md`

### Approach with Caution

- `_config.yml` – Affects entire site configuration
- `_layouts/` – Affects all page rendering
- `_includes/` – Reusable components, site-wide impact
- `public/css/` – Affects entire site styling
- `Gemfile` – Build dependency changes

### Key Patterns to Follow

- Post filenames must follow `YYYY-MM-DD-slug.md` format
- All required front matter fields must be present
- Images go under `assets/img/YYYY/MMDD/`
- `excerpt` field is written in English
- Tags are space-separated (not comma-separated)
- Match tone and structure of existing posts for consistency
