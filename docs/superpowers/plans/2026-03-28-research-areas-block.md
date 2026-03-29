# Research Areas Block Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a data-driven "Research Areas" section with 6 overlay-style cards to the homepage, placed before the news section.

**Architecture:** YAML data file defines research areas → Liquid include renders a Bootstrap card grid with CSS background images and gradient overlays → Layout inserts the section conditionally via front matter flag. A `/research/` page provides link targets for each card.

**Tech Stack:** Jekyll, Liquid, Bootstrap 5 grid, SCSS, YAML data files

---

## File Map

| Action | File | Responsibility |
|--------|------|---------------|
| Create | `_data/research_areas.yml` | Research area definitions (name, description, image, anchor) |
| Create | `_includes/research_areas.liquid` | Card grid template |
| Create | `_pages/research.md` | Destination page with anchored sections |
| Create | `assets/img/research/` | Image directory (placeholder images for dev) |
| Modify | `_sass/_components.scss` | Research area card styles |
| Modify | `_layouts/about.liquid` | Insert research areas section before news |
| Modify | `_pages/about.md` | Add `research_areas.enabled` front matter flag |

---

### Task 1: Create research areas data file

**Files:**
- Create: `_data/research_areas.yml`

- [ ] **Step 1: Create the YAML data file**

```yaml
- name: AI Agent Security
  description: "Securing autonomous AI agents against adversarial manipulation, prompt injection, and unintended behaviors in real-world deployments."
  image: research/ai-agent-security.jpg
  anchor: ai-agent-security

- name: Interpretable AI Security
  description: "Leveraging interpretability and explainability techniques to understand, diagnose, and mitigate vulnerabilities in AI systems."
  image: research/interpretable-ai-security.jpg
  anchor: interpretable-ai-security

- name: Usable Security of AI
  description: "Designing intuitive security mechanisms and interfaces that help users safely interact with and configure AI systems."
  image: research/usable-security-of-ai.jpg
  anchor: usable-security-of-ai

- name: AI Misuse Measurement
  description: "Developing methods to quantify and detect malicious applications of AI, from deepfakes to automated cyber attacks."
  image: research/ai-misuse-measurement.jpg
  anchor: ai-misuse-measurement

- name: AI Society Security
  description: "Investigating the societal impacts of AI security risks, including misinformation, surveillance, and governance challenges."
  image: research/ai-society-security.jpg
  anchor: ai-society-security

- name: AI for Security
  description: "Applying AI techniques to strengthen cybersecurity defenses, including threat detection, vulnerability analysis, and automated response."
  image: research/ai-for-security.jpg
  anchor: ai-for-security
```

Write this to `_data/research_areas.yml`.

- [ ] **Step 2: Create placeholder image directory**

```bash
mkdir -p assets/img/research
```

Create 6 simple placeholder images (1x1 colored PNGs or use any small image) so the site builds without errors before the user provides real images. Alternatively, create a `.gitkeep` file:

```bash
touch assets/img/research/.gitkeep
```

- [ ] **Step 3: Commit**

```bash
git add _data/research_areas.yml assets/img/research/.gitkeep
git commit -m "feat: add research areas data file and image directory"
```

---

### Task 2: Add research area card styles

**Files:**
- Modify: `_sass/_components.scss` (append after the existing `// diff2html` section at end of file, around line 262)

- [ ] **Step 1: Append SCSS styles to `_sass/_components.scss`**

Add the following block at the end of the file:

```scss
// Research Areas

.research-areas {
  a {
    text-decoration: none;
  }
}

.research-area-card {
  position: relative;
  height: 180px;
  border-radius: 0.5rem;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.02);
  }
}

.research-area-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.75));
  padding: 1rem;

  h3 {
    color: #fff;
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0 0 0.25rem 0;
  }

  p {
    color: rgba(255, 255, 255, 0.85);
    font-size: 0.75rem;
    line-height: 1.4;
    margin: 0;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add _sass/_components.scss
git commit -m "feat: add research area card styles"
```

---

### Task 3: Create research areas Liquid template

**Files:**
- Create: `_includes/research_areas.liquid`

- [ ] **Step 1: Create the Liquid include**

Write the following to `_includes/research_areas.liquid`:

```liquid
<div class="research-areas">
  <div class="row row-cols-1 row-cols-md-3 g-3">
    {% for area in site.data.research_areas %}
      <div class="col">
        <a href="{{ '/research/' | relative_url }}#{{ area.anchor }}">
          <div
            class="research-area-card"
            style="background-image: url('{{ area.image | prepend: 'assets/img/' | relative_url }}');"
          >
            <div class="research-area-overlay">
              <h3>{{ area.name }}</h3>
              <p>{{ area.description }}</p>
            </div>
          </div>
        </a>
      </div>
    {% endfor %}
  </div>
</div>
```

- [ ] **Step 2: Commit**

```bash
git add _includes/research_areas.liquid
git commit -m "feat: add research areas Liquid template"
```

---

### Task 4: Insert research areas section into about layout

**Files:**
- Modify: `_layouts/about.liquid` (insert before line 43, the `<!-- News -->` comment)
- Modify: `_pages/about.md` (add front matter flag)

- [ ] **Step 1: Edit `_layouts/about.liquid`**

Insert the following block **before** the `<!-- News -->` line (line 43):

```liquid
    <!-- Research Areas -->
    {% if page.research_areas and page.research_areas.enabled %}
      <h2>
        <a href="{{ '/research/' | relative_url }}" style="color: inherit">research areas</a>
      </h2>
      {% include research_areas.liquid %}
    {% endif %}

```

The file should now read (lines 42–52):

```liquid
    <div class="clearfix">{{ content }}</div>

    <!-- Research Areas -->
    {% if page.research_areas and page.research_areas.enabled %}
      <h2>
        <a href="{{ '/research/' | relative_url }}" style="color: inherit">research areas</a>
      </h2>
      {% include research_areas.liquid %}
    {% endif %}

    <!-- News -->
    {% if page.announcements and page.announcements.enabled %}
```

- [ ] **Step 2: Edit `_pages/about.md` front matter**

Add `research_areas` block after the `latest_posts` section. The front matter should become:

```yaml
---
layout: about
title: about
permalink: /
subtitle: Ph.D. Student in Computer Science at <a href='https://www.ucla.edu/'>UCLA</a>

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Department of Computer Science</p>
    <p>University of California, Los Angeles</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: true
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts

research_areas:
  enabled: true
---
```

- [ ] **Step 3: Commit**

```bash
git add _layouts/about.liquid _pages/about.md
git commit -m "feat: wire research areas section into homepage"
```

---

### Task 5: Create the research destination page

**Files:**
- Create: `_pages/research.md`

- [ ] **Step 1: Create `_pages/research.md`**

Write the following:

```markdown
---
layout: page
title: research
permalink: /research/
description: Our research spans six key areas in AI security.
nav: true
nav_order: 2
---

## AI Agent Security
{: #ai-agent-security}

Securing autonomous AI agents against adversarial manipulation, prompt injection, and unintended behaviors in real-world deployments.

<!-- Add detailed content here -->

---

## Interpretable AI Security
{: #interpretable-ai-security}

Leveraging interpretability and explainability techniques to understand, diagnose, and mitigate vulnerabilities in AI systems.

<!-- Add detailed content here -->

---

## Usable Security of AI
{: #usable-security-of-ai}

Designing intuitive security mechanisms and interfaces that help users safely interact with and configure AI systems.

<!-- Add detailed content here -->

---

## AI Misuse Measurement
{: #ai-misuse-measurement}

Developing methods to quantify and detect malicious applications of AI, from deepfakes to automated cyber attacks.

<!-- Add detailed content here -->

---

## AI Society Security
{: #ai-society-security}

Investigating the societal impacts of AI security risks, including misinformation, surveillance, and governance challenges.

<!-- Add detailed content here -->

---

## AI for Security
{: #ai-for-security}

Applying AI techniques to strengthen cybersecurity defenses, including threat detection, vulnerability analysis, and automated response.

<!-- Add detailed content here -->
```

- [ ] **Step 2: Commit**

```bash
git add _pages/research.md
git commit -m "feat: add research areas destination page"
```

---

### Task 6: Visual verification

- [ ] **Step 1: Build the site locally**

```bash
docker compose up --build
```

Or if not using Docker:

```bash
bundle exec jekyll serve
```

- [ ] **Step 2: Verify the homepage**

Open `http://localhost:8080` (or `http://localhost:4000`) and check:

1. "research areas" heading appears between the bio text and "news"
2. 6 cards display in a 2x3 grid layout
3. Cards show placeholder backgrounds (or gradient if no images yet) with white overlay text
4. Each card's name and description are visible
5. Hovering a card shows a subtle scale effect
6. Clicking a card navigates to `/research/#<anchor>`

- [ ] **Step 3: Verify responsive behavior**

Resize browser to mobile width (<768px) and check:

1. Cards stack into a single column
2. Text remains readable
3. Cards maintain their 180px height

- [ ] **Step 4: Verify the research page**

Navigate to `/research/` and check:

1. All 6 sections are present with correct headings
2. Clicking a card on the homepage scrolls to the correct section
3. Page appears in the navigation bar

- [ ] **Step 5: Check dark mode**

Toggle dark mode (if enabled) and verify:

1. Cards still look good — overlay text remains white/readable
2. Section heading color inherits correctly

- [ ] **Step 6: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: visual adjustments for research areas block"
```
