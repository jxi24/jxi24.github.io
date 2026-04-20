# Website Improvement Todo

## Critical — Broken or Misleading Content

- [ ] **Fix CV data** — The CV is rendered from `assets/json/resume.json` (JSON Resume format), NOT `_data/cv.yml`. Work and education are mostly real, but several fields are still template placeholder:
  - `basics.location`: "2712 Broadway St, San Francisco, CA 94115" — template address, replace with Fermilab or remove
  - `basics.profiles`: Twitter username `AlbertEinstein` / URL to Einstein's Twitter — remove or replace with Joshua's actual handle
  - `basics.summary`: empty string — add a short bio sentence
  - `projects`: empty array — add Achilles, ResBos2, Pepper, NuHepMC, i-flow
  - `interests.keywords`: empty array — fill in research keywords or remove
  - Consider adding `awards`, `volunteer`, `certificates` sections for honors/service

- [ ] **Replace placeholder coauthors** — `_data/coauthors.yml` lists Einstein, Schrödinger, Planck, etc. Add actual frequent collaborators with links to their faculty/profile pages so author names on the publications page become clickable.

- [ ] **Remove or replace Project 6** — `_projects/6_project.md` is an unmodified template with category "fun" and no real content. Either delete it or replace with a real project (i-flow, NeuCol, or a catch-all "Other" entry).

---

## High Priority — Empty Pages that Visitors Will Click

- [ ] **Write real project descriptions** — every file in `_projects/` contains template boilerplate ("beautiful feature showcase pages"). Replace with actual content for each:
  - **Achilles**: physics motivation (neutrino–nucleus interactions), what it calculates, current status, links to the GitHub repo and key papers
  - **ResBos2**: what resummation does and why it matters for W-mass/Drell-Yan, status, links
  - **Pepper / Chili**: portable GPU event generation story, performance numbers, links
  - **Sherpa**: Joshua's contributions to v3 (phase-space generation, amplitudes on GPUs), links
  - **NuHepMC**: why a standard format matters, adoption status, links to spec repo
  - Add a project for **i-flow** (normalizing flows for phase-space integration) — listed in repositories but absent from projects
  - Add a project for **NeuCol SciDAC5** collaboration if appropriate

- [ ] **Add project images** — NuHepMC and i-flow have no preview thumbnails. Add a representative figure (Feynman diagram, architecture plot, result plot) for each project card.

- [ ] **Populate the teaching page** (`_pages/teaching.md`) — currently one line of placeholder text:
  - List courses taught (course number, title, institution, year, enrollment if notable)
  - Add a short teaching philosophy statement (2–3 sentences)
  - Enable the page in the nav bar (`nav: true` in front matter)
  - If no formal teaching yet: reframe as "Mentoring & Training" and list students/postdocs supervised, tutorials given, schools attended as lecturer

---

## Medium Priority — Professionalism and Discoverability

- [ ] **Refresh the news section** — the three existing announcements are from 2015–2016 and are placeholder text. Add recent items (and enable news display on the about page by setting `news: true` in `_pages/about.md` if desired):
  - New paper postings (especially high-impact ones)
  - Conference talks (PHYSTAT, Neutrino, DPF, etc.)
  - Software releases / new versions
  - Collaboration milestones
  - Job/funding news if shareable

- [ ] **Expand the about page bio** — the current bio is accurate but brief. Consider adding:
  - One sentence on research vision / longer-term goals
  - Explicit mention of open-source philosophy
  - Any postdoc/student openings or collaboration invitations
  - A "Recent news" snippet (the theme supports this natively)

- [ ] **Add missing selected publications** — review the `selected = {true}` flags in `_bibliography/papers.bib`. Ensure the 4–6 most representative/impactful papers are marked selected so they appear on the about page.

- [ ] **Add conference proceedings and talks** — the bib file covers journal papers and arXiv preprints well. Add a separate section or tag for invited talks, review articles, and proceedings (Snowmass contributions are already there; check for ICHEP, Les Houches, etc.).

- [ ] **Verify and add social/professional links** in `_config.yml`:
  - LinkedIn username (currently blank) — useful for non-physics visitors
  - Institutional page URL (`work_url`) — Fermilab theory division profile
  - Any active X/Mastodon handle

---

## Lower Priority — Polish and Completeness

- [ ] **Add a service section to the CV** — referee work (journals, list is optional), committee memberships, workshop organization, outreach. These matter for promotion dossiers.

- [ ] **Add grants/funding to CV** — NeuCol SciDAC5 and any DOE SCGSR or other awards. Include role (PI, co-PI, senior personnel), funding agency, period, and amount if public.

- [ ] **Improve repository cards** (`_data/repositories.yml`) — add a one-line description for each repo so the repository page is informative rather than just a list of links.

- [ ] **Add site description** — `_config.yml` has a generic al-folio description. Replace with a real one (used by search engines and link previews):
  ```yaml
  description: >
    Joshua Isaacson — Applications Physicist at Fermilab working on
    computational tools for high-energy and neutrino physics.
  ```

- [ ] **Set site title** — `title: blank` falls back to full name, which is fine, but consider setting it explicitly to control how tabs and bookmarks display.

- [ ] **Enable blog or remove it from the codebase** — the blog is disabled (`nav: false`) but all the infrastructure is in place. Either write occasional research-update posts (good for SEO and visibility) or clean up the dead nav entry.

- [ ] **Add an abstract/blurb to featured publications** — al-folio supports an `abstract` field in BibTeX entries that appears as a collapsible on the publications page. Adding it to the 10–15 most important papers improves accessibility for non-specialists.

- [ ] **Accessibility and performance** — once content is filled in, run the Lighthouse and axe CI checks locally to catch any contrast or heading-structure issues introduced by new content.
