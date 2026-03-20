# Academic Website Migration: AcadHomepage to al-folio

## Overview

Migrate all academic content from the former AcadHomepage-based website (`former_website/whilebug.github.io/`) into the current al-folio project. Each major content section gets its own atomic commit. The "My Space"/Showcase section is excluded.

**Already done** (prior commits): `_config.yml` has `first_name: Peiran`, `last_name: Wang`, `title: WhileBug`, `url: https://whilebug.github.io`, `baseurl:` empty.

## Source

- **Path**: `former_website/whilebug.github.io/`
- **Theme**: AcadHomepage (luost26)
- **Content format**: YAML data files (`_data/profile.yml`, `_data/authors.yml`) + Markdown publication files (`_publications/`) + news Markdown files (`_news/`)

## Target

- **Path**: project root (al-folio)
- **Theme**: al-folio (Jekyll)
- **Content format**: YAML data, BibTeX, Markdown

## Migration Plan (6 Commits)

### Commit 1: Config & Profile Assets

**Files modified:**

`_config.yml`:
- Clear `middle_name` (line 7) — remove "R."
- Update `contact_note` — set to empty or a meaningful note
- Update `description` — replace template text with personal site description
- Update `keywords` — replace with relevant keywords (e.g., "academic, computer-science, security, machine-learning")
- Remove `Photos from Unsplash` line in `footer_text`
- Update Jekyll Scholar section (around line 282):
  ```yaml
  scholar:
    last_name: [Wang]
    first_name: [Peiran, P.]
  ```

`_data/socials.yml` — Replace entirely using al-folio field names:
- `cv_pdf: /assets/pdf/CV-11242025.pdf`
- `email: whilebug@gmail.com`
- `github_username: whilebug`
- `twitter_username: WhileBugWang`
- `linkedin_username: peiran-wang-67b997381`
- `orcid_id: 0000-0001-6881-2855`
- `scholar_userid: mHy2_KIAAAAJ`
- `rss_icon: true`
- Remove `inspirehep_id` and `custom_social` template entries

**Files added:**
- `assets/img/prof_pic.png` — Copy from `former_website/.../assets/images/photos/YoungPeiran.png` (keep as PNG, update reference in about.md)
- `assets/pdf/CV-11242025.pdf` — Copy from `former_website/.../assets/files/CVs/CV-11242025.pdf`

**Verification:** Site builds, profile image displays, social links resolve.

### Commit 2: About Page

**Files modified:**
- `_pages/about.md`:
  - `subtitle`: "Ph.D. Student in CS at UCLA"
  - `profile.image`: `prof_pic.png` (updated from `prof_pic.jpg`)
  - `profile.more_info`: UCLA CS affiliation
  - Body text: Use `short_bio` from `former_website/_data/profile.yml`
  - Keep: `selected_papers: true`, `social: true`, `announcements.enabled: true`, `latest_posts.enabled: true`

**Verification:** Homepage shows real bio, correct subtitle, profile image.

### Commit 3: Publications

**Files modified:**
- `_bibliography/papers.bib` — Replace Einstein examples with 28 BibTeX entries converted from YAML files in `former_website/_publications/` (years 2021-2026)

**BibTeX conversion details:**
- Source: Each file in `former_website/_publications/` has `title`, `authors`, `conference`/`journal`, `paper_url`, `image`, `selected`, etc.
- Convert to standard BibTeX fields: `title`, `author`, `year`, `booktitle`/`journal`
- Add al-folio custom fields:
  - `selected = {true}` for: Moderator, AgentArmor, DSAgentSurvey, HaluProbe, PI-SoK
  - `preview` = cover image filename
  - `bibtex_show = {true}`
  - `html` / `arxiv` / `pdf` = paper URLs from source `links` section
- Award info (cross-referenced from `former_website/_data/profile.yml` awards section):
  - `2024-CCS-Moderator` → `award = {CCS Distinguished Paper Award}`
  - `2021-ISCC-FLPhish` → `award = {Best Paper Award}`

**Files added:**
- `assets/img/publication_preview/` — Copy 28 paper cover PNG images from `former_website/assets/images/papers/`

**Verification:** Publications page lists all 28 papers. Selected papers appear on homepage. Cover images display. Award badges show on awarded papers.

### Commit 4: CV Data

**Files modified:**
- `_data/cv.yml` — Replace Einstein template. Map to al-folio's structure:

```yaml
cv:
  name: Peiran Wang
  label: Ph.D. Student
  email: whilebug@gmail.com
  location: Los Angeles, CA
  summary: (brief research summary)

  social_networks:
    - network: GitHub
      username: whilebug
    - network: LinkedIn
      username: peiran-wang-67b997381
    - network: X
      username: WhileBugWang

  sections:
    Education:
      # 3 entries using al-folio structure:
      # institution, location, url, area, studyType, start_date, end_date
      - institution: UCLA (PhD, Sep 2025 - Present)
      - institution: Tsinghua University (Master, Sep 2022 - Jul 2025)
      - institution: Sichuan University (Bachelor, Sep 2018 - Jul 2022)

    Research Experience:
      # 5 entries (merge SCU Beck Lab & CodeSec Lab into one entry)
      # Use al-folio "Experience" format: company, position, location, start_date, end_date
      - UCLA (Sep 2025 - Present)
      - UW-Madison SaFoLab (Aug 2024 - Mar 2025)
      - UIUC Dream Lab (Sep 2024 - Mar 2025)
      - UCSD DataSmith Lab (May 2023 - Feb 2024)
      - SCU Beck Lab & CodeSec Lab (May 2020 - Jun 2022)

    Industry Experience:
      # 4 entries (separate section from research)
      - ByteDance (Mar 2025 - Aug 2025, Jul 2024 - Jan 2025)
      - Baidu (May 2024 - Jul 2024)
      - Future Capital (May 2023 - Aug 2023)
      - Microsoft Research Asia (Aug 2021 - Jun 2022)

    Awards:
      # 5 entries using al-folio awards format: title, date, awarder, summary
      - CCS Distinguished Paper Award (2024)
      - Star of Tomorrow - MSRA (2022)
      - ISCC Best Paper Award (2021)
      - National Scholarship (2019)
      - SCU 1st Level Scholarship (2019)
```

Note: Research Experience and Industry Experience are kept as separate sections for clarity. Each entry uses the actual al-folio YAML structure with `company`/`institution`, `position`, `location`, `start_date`, `end_date`, `highlights`.

**Verification:** CV page renders with all sections populated.

### Commit 5: News

**Files modified/added in `_news/`:**
- Remove 3 template announcements
- Add 6 real news items from `former_website/_news/`:
  1. 2021-09-05: FLPhish ISCC Best Paper Award
  2. 2022-06-12: MSRA internship completion
  3. 2024-07-28: Baidu internship completion
  4. 2024-10-18: CCS Distinguished Paper Award
  5. 2025-01-22: ByteDance internship completion
  6. 2025-03-30: UCLA CS PhD offer

**Verification:** News section on homepage shows real announcements.

### Commit 6: Cleanup

**Files removed:**
- 31 example blog posts from `_posts/` — keep exactly 4 for reference: `formatting-and-links`, `images`, `code`, `math`
- 9 example project files from `_projects/`

**Files modified:**
- `_data/coauthors.yml` — Clear Einstein-era template entries (empty file with comment)
- `_data/repositories.yml` — Clear or update with real repos
- `_config.yml` — Set `enable_publication_badges.inspirehep: false`

**Verification:** Site builds cleanly. No template placeholder content visible on any page.

## Out of Scope

- "My Space"/Showcase section (cat photos, badges, personal cards) — excluded per user decision
- Blog post creation — no blog posts exist in former site
- Institution badge images — not needed without Showcase section
- Custom styling or theme modifications
- Deployment configuration
- Paper PDF file migration (only cover images are migrated)

## Risks & Mitigations

- **BibTeX conversion accuracy**: Former site uses YAML; manual conversion to BibTeX needed. Mitigation: verify each entry renders correctly. Build and test incrementally.
- **Image paths**: al-folio expects images in specific locations. Mitigation: follow al-folio conventions (`assets/img/` for images, `assets/pdf/` for PDFs).
- **Profile image format**: Keep as PNG (`prof_pic.png`) and update reference in `about.md` to avoid format conversion issues.
- **BibTeX syntax errors**: A single syntax error breaks the entire publications page. Mitigation: validate BibTeX syntax before committing.
