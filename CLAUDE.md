# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic portfolio website for Joshua Isaacson (physicist at Fermilab) built on the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme. It showcases research in high-energy and neutrino physics, publications, projects, and CV.

## Commands

### Local Development

```bash
# Install Ruby dependencies
bundle install

# Serve locally with live reload (default: http://localhost:4000)
bundle exec jekyll serve

# Build without serving
bundle exec jekyll build

# Serve with Docker (recommended for full feature support including Jupyter notebooks)
docker-compose up
```

### Formatting

```bash
# Format Liquid/HTML templates with Prettier
npx prettier --write "**/*.{html,liquid}"

# Check formatting without writing
npx prettier --check "**/*.{html,liquid}"
```

All PRs must pass Prettier formatting checks (enforced by CI). The Prettier config is in `.prettierrc` (printWidth: 150 for Liquid files).

### No test suite exists — CI validates via:
- Prettier formatting (`.github/workflows/prettier.yml`)
- Broken link detection (`.github/workflows/broken-links.yml`)
- Accessibility checks (`.github/workflows/axe.yml`)
- Lighthouse performance audits (`.github/workflows/lighthouse-badger.yml`)

## Architecture

### Content Organization

| Directory | Purpose |
|-----------|---------|
| `_pages/` | Top-level site pages (about, publications, projects, cv, blog, etc.) |
| `_projects/` | Individual project entries rendered as cards |
| `_news/` | News/announcement items shown on the about page |
| `_bibliography/papers.bib` | All publications in BibTeX format |
| `_data/` | Structured YAML data: `cv.yml`, `coauthors.yml`, `repositories.yml`, `venues.yml` |
| `_layouts/` | Liquid page templates (`about`, `page`, `post`, `distill`, `cv`, `bib`) |
| `_includes/` | Reusable Liquid components (header, footer, social links, figures, etc.) |
| `_sass/` | SCSS stylesheets (`_base.scss`, `_themes.scss`, `_variables.scss`) |
| `_plugins/` | Custom Jekyll Ruby plugins (citation fetchers, cache busting, etc.) |
| `assets/` | Static files: images, JS, CSS, PDFs, fonts |

### Publications System

Publications are managed entirely through `_bibliography/papers.bib`. The `jekyll-scholar` plugin renders them on `/publications/`. Custom BibTeX fields control display behavior:
- `bibtex_show = {true}` — adds a collapsible BibTeX block
- `selected = {true}` — surfaces the paper on the about page
- `preview = {filename.png}` — thumbnail image from `assets/img/publication_preview/`
- `inspirehep_id = {XXXX}` — enables InspireHEP citation badge

The `_data/coauthors.yml` file maps author names to their profile URLs for automatic linking.

### Projects System

Each `.md` file in `_projects/` renders as a card on `/projects/`. Front matter controls display:
- `importance` — integer for sort order (lower = higher priority)
- `category` — groups cards (currently: Collider, Neutrino, General)
- `img` — card thumbnail from `assets/img/`

### CV System

The CV at `/cv/` is driven by `_data/cv.yml` structured as sections with entries. The `_layouts/cv.liquid` template iterates over this data. Do not put CV content directly in `_pages/cv.md`.

### Configuration

All major feature flags live in `_config.yml`. Key toggles:
- `scholar.bibliography_template` — controls publication rendering
- `enable_darkmode`, `enable_math`, `enable_masonry` — feature flags
- `giscus` block — comment system configuration
- `jekyll-archives` — auto-generates tag/category pages for blog

### Deployment

GitHub Actions (`.github/workflows/deploy.yml`) builds and deploys to GitHub Pages on every push to `main`. The build:
1. Installs Ruby 3.2.2 + all gems
2. Installs Python/Jupyter (for notebook rendering)
3. Runs `jekyll build --lsi` (latent semantic indexing for related posts)
4. Runs PurgeCSS to strip unused styles
5. Deploys to `gh-pages` branch

## Key Conventions

- **Liquid templates** use `.liquid` extension (not `.html`) — this triggers the Prettier Liquid plugin
- **Page permalinks** are set in front matter, not inferred from filename
- **Navigation** is controlled by `nav: true` and `nav_order` in page front matter
- **Math** uses MathJax; enable per-page with `math: true` in front matter
- **Images in posts/projects** use the `{% include figure.liquid %}` helper, not raw `<img>` tags
- **Blog posts** go in `_posts/` with filename format `YYYY-MM-DD-title.md`
