# UCLA Homepage Redesign — Design Spec

## Overview

Restyle Peiran Wang's al-folio site after the clean, text-first look of
[yrbding.github.io](https://yrbding.github.io/) (Jon Barron-style academic page), with a
UCLA identity. The homepage becomes a single long page with flat sections; the other
pages (Publications, Research, News, Blog, CV, 404) are re-skinned to match. All content
and automation stay as they are.

This is a restyle in place on top of al-folio, not a theme switch.

## Goals

- White, card-free, document-like pages in a centered 930px column.
- UCLA blue-box wordmark in the navbar, UCLA colors throughout, light and dark mode.
- Homepage sections in yrbding order, but Selected Publications keep their thumbnails.
- Keep every existing pipeline working: `papers.bib` (jekyll-scholar), `_news/`,
  `_data/cv.yml` (rendercv), Google Scholar citation updates, CV rendering, blog.

## Non-Goals

- No content rewrites (bio text, news, papers, CV entries stay as written).
- No lab rename or lab logo design. The lab website is a separate repo; this spec only
  reserves a lab-logo slot in the navbar (see Open Items).
- No push or deploy. Merging `ucla-redesign` into `main` is the user's call.
- No al-folio version upgrade.

## Context

- Live site: `origin/main` (al-folio), deployed by `.github/workflows/deploy.yml` to
  `gh-pages`. Work happens on branch `ucla-redesign` created from `origin/main`.
- Earlier work in this repo: the March 2026 migration spec and the Research Areas block
  spec (`docs/superpowers/specs/2026-03-28-research-areas-block-design.md`). This redesign
  replaces the homepage card grid from that block with a compact list, but reuses its data
  file `_data/research_areas.yml` and keeps `/research/`.
- Current homepage (`_pages/about.md`, layout `_layouts/about.liquid`): title + subtitle,
  floated profile photo, bio, research-area cards, news (limit 5, scrollable), latest
  posts, selected papers, social icons.
- Data available: 33 bib entries (all with `preview`, 5 `selected`, 2 `award`),
  8 news items, `cv.yml` sections Education / Experience / Awards (entries carry `logo`
  under `assets/img/badges/`). No Service or Talks data.

## 1. Visual System

### Colors

UCLA brand palette. Gold is decorative only, never body text.

| Token         | Light               | Dark                        | Use                                      |
| ------------- | ------------------- | --------------------------- | ---------------------------------------- |
| Background    | `#FFFFFF`           | `#0F1C27`                   | page                                     |
| Text          | `#303740`           | `#E6EDF3`                   | body                                     |
| Muted text    | `#5B6B7A`           | `#9FB3C8`                   | dates, venues, secondary                 |
| Theme / links | UCLA Blue `#2774AE` | UCLA Lighter Blue `#8BB8E8` | links, paper titles, active states       |
| Headings      | Dark grey `#252525` | `#E8EAED`                   | h1–h3, section titles, navbar name       |
| Accent        | UCLA Gold `#FFD100` | `#FFD100`                   | active-nav underline, section-title rule |
| Award text    | Dark gold `#8A6500` | `#FFD100`                   | award line under a paper                 |
| Divider       | `rgba(0,0,0,.1)`    | `rgba(255,255,255,.12)`     | hairlines between items                  |

Contrast: all text tokens are at least 4.5:1 on their background (award `#8A6500` on
white is about 5.3:1).

Implementation: set the al-folio CSS variables in `_sass/_themes.scss`
(`--global-theme-color`, `--global-hover-color`, `--global-text-color`, etc.) for both
`:root` and `html[data-theme="dark"]`, and add any new tokens there.

### Typography

> **Revision 2026-09-28 (user review):** typography switched from Source Serif 4 +
> Inter to Lato everywhere, and headings from UCLA Darkest Blue to yrbding's dark grey,
> to match yrbding.github.io more closely. Mentions of Source Serif 4 / Inter below are
> superseded.

- Everything (headings, page titles, section titles, navbar name, body, UI): **Lato**
  400/700 with italics, stack `"Lato", Verdana, Helvetica, sans-serif`, as on
  yrbding.github.io. Body 16px with line height 1.55; name 28px bold with −0.02em
  letter spacing; section titles 24px bold.
- Load it by replacing the Roboto URL in `_config.yml` →
  `third_party_libraries.google_fonts` (Material Icons is not referenced anywhere).

### Surfaces

- No cards or drop shadows for content blocks. Items are separated by hairline dividers.
- Profile photo: 8px radius, one soft shadow. Paper thumbnails: 6px radius, no shadow.
- Content width stays `max_width: 930px`.

## 2. Navbar (`_includes/header.liquid`, `_sass/_navbar.scss`)

- Left, on every page including the homepage:
  UCLA wordmark in a UCLA Blue box, then "Peiran Wang" in Source Serif 4. Both link
  to `/`.
  - Wordmark: official white SVG from brand.ucla.edu, saved as
    `assets/img/logos/ucla-wordmark-white.svg`, rendered with an `<img>` inside a blue box.
    The SVG paths are used unmodified.
- Lab-logo slot: rendered only if `_config.yml` has `lab_logo: {image, url, alt}`. Left
  unset in this project for now.
- Right: nav pages in the order Publications, Research, Blog, CV. Today `nav_order` is
  blog 1, publications 2, research 2, cv 5, so set it to publications 1, research 2,
  blog 3, cv 4 in the pages' front matter. The separate "about" item is removed because
  the brand links home. Search and the
  light/dark toggle stay at the far right.
- Active page: 3px gold underline. Hover: UCLA Blue.
- Fixed to the top, white background (dark: page background), 1px bottom hairline,
  no shadow. Mobile keeps al-folio's collapse toggle.
- Scroll progress bar removed: `enable_progressbar: false`.

## 3. Homepage (`_pages/about.md`, `_layouts/about.liquid`)

Section order, top to bottom:

1. **Hero** (new include `_includes/home/hero.liquid`)
   - Left: full name `first_name last_name` ("Peiran Wang") as the page `h1`, replacing
     the current `site.title` ("WhileBug"), which stays as the browser-tab/SEO title.
     Below it two blocks, each with a thin left rule:
     - "Ph.D. Student" / "Department of Computer Science" (link) /
       "University of California, Los Angeles" (link)
     - "Advisor: Prof. Yuan Tian" / "UCLA Security Lab" (link to the lab site)
   - Right: profile photo (`assets/img/prof_pic.jpg`).
   - Under the blocks: icon row from `{% social_links %}`, showing whatever
     `_data/socials.yml` enables (currently email, Google Scholar, CV PDF, RSS; GitHub,
     Twitter, LinkedIn, ORCID are commented out there and stay that way).
   - Hero fields come from `about.md` front matter (`profile.*`), not hard-coded.
2. **Bio**: `about.md` body, unchanged text. Small inline org icons may follow institution
   names, using existing `assets/img/badges/*.png` (class `org-icon`, 1em tall).
3. **News**: `_includes/news.liquid` restyled to a two-column list (date | text) with
   hairlines; homepage shows the latest 6, not scrollable; "All news →" links `/news/`.
4. **Research Interests** (new include `_includes/research_interests.liquid`): one line
   per entry in `_data/research_areas.yml`, linking to `/research/#<anchor>`. The old
   card grid include stays in the repo but is no longer used on the homepage.
5. **Selected Publications**: existing `selected_papers.liquid` (bib query
   `selected=true`), styled as in section 4 below; "Full list →" links `/publications/`.
6. **Honors & Awards** (new include `_includes/home/awards.liquid`): from
   `site.data.cv.cv.sections.Awards`, one line each: "Title, Awarder. Year".
7. **Experience** (new include `_includes/home/experience.liquid`): from
   `site.data.cv.cv.sections.Experience`: small logo, "Mon YYYY – Mon YYYY: Position @
   Company", with an empty `end_date` shown as "Present".
8. **Footer**: see section 4.

Not on the homepage: Education (covered in the bio and CV page) and latest blog posts
(`latest_posts.enabled: false`). Adding news, papers, or CV entries keeps working through
the existing files.

Section titles: Source Serif 4, Darkest Blue, with a short gold rule. Titles are plain
text; the "All news →" / "Full list →" links sit at the right end of the title row.

## 4. Other Pages

- **Publications** (`_layouts/bib.liquid`, `_sass/_publications.scss`), shared with the
  homepage's Selected Publications:
  - Thumbnail left, text right: blue title, authors with "Peiran Wang" bold, italic
    venue, and, for entries with `award`, an always-visible dark-gold line
    ("🏆 <award text>") instead of the collapsible award button.
  - Button row (ABS / BIB / PDF / HTML …) restyled as small blue text links in brackets.
  - Google Scholar citation count kept, shown as muted "Cited by N".
  - Year headings in Source Serif 4 with a hairline; the bib search box stays, simplified.
- **Research** (`_pages/research.md`): content untouched; inherits typography; figure
  shadows removed, 8px radius.
- **News page**: same list style as the homepage news (shared include).
- **Blog, posts, CV, 404**: inherit fonts and colors; CV PDF button in UCLA Blue.
- **Footer** (`_includes/footer.liquid`, `_sass/_footer.scss`): `footer_fixed: false`;
  a light, small-text line at the end of the page ("Last updated …", template credit)
  instead of the fixed dark bar.

## 5. Implementation & Verification

- Branch: `ucla-redesign` from `origin/main`. The earlier restyle of the old template is
  archived on local branch `archive/academic-homepage-restyle`.
- Styles: color/tokens in `_sass/_themes.scss`; component changes in the existing
  partials (`_navbar`, `_publications`, `_footer`, `_layout`, `_typography`); new
  homepage section styles in a new partial `_sass/_home.scss`, added to
  `assets/css/main.scss`.
- Local run: Docker per `AGENTS.md` (`docker compose up`, <http://localhost:8080>).
- Commits: one per module, message format `<type>: <subject>` per
  `.github/GIT_WORKFLOW.md`, `npx prettier . --write` before every commit, files staged
  explicitly.
- Verification after each module:
  - Site builds with no errors.
  - Screenshots of Home, Publications, Research, News, Blog, CV, 404 at 1400px and 390px,
    light and dark.
  - Counts match data: 33 papers on Publications, 5 selected and 6 news on Home,
    Awards and Experience entries equal `cv.yml`.
  - No broken internal links (crawl `_site`).
  - Text contrast at least 4.5:1; gold never used for body text.

## Open Items

- **Lab logo**: the lab (UCLA Security Lab) is choosing a new name and logo in its own
  repo. When decided, set `lab_logo` in `_config.yml` to show it next to the UCLA box.
- **Docker Desktop** must be running for local builds (installed, currently stopped).
- The repo tracks a stray `.superpowers/brainstorm/` folder from an earlier session
  (server logs, pid). Not touched by this redesign; can be removed separately.
