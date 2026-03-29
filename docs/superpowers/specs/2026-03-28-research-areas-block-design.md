# Research Areas Block — Design Spec

## Overview

Add a "Research Areas" section to the homepage (`_pages/about.md`), placed between the bio content and the news section. The block displays 6 research area cards in a 2-row x 3-column grid. Each card shows a background image with a gradient overlay containing the area name and a 2-sentence description. Cards link to anchored sections on a dedicated `/research/` page.

## Approach

Data-driven with YAML + Liquid include, following al-folio's existing patterns for news, projects, and selected papers.

## Files to Create

### 1. `_data/research_areas.yml`

Data file defining the 6 research areas. Each entry:

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

Images are expected at `assets/img/research/<name>.jpg` — provided by the user.

### 2. `_includes/research_areas.liquid`

Liquid template that renders the card grid:

- Uses Bootstrap `row row-cols-1 row-cols-md-3 g-3` for the 3-column responsive grid
- Each card: `position: relative` container with background image, gradient overlay (`linear-gradient(transparent, rgba(0,0,0,0.75))`), and white text at the bottom
- Each card wraps in an `<a>` tag linking to `/research/#{{ area.anchor }}`
- Card height: fixed at ~180px to maintain uniform grid appearance
- Background image: `background-size: cover; background-position: center`
- Hover effect: subtle scale or brightness change via CSS transition

### 3. Styles in `_sass/_components.scss`

Append research area card styles to the existing `_sass/_components.scss` file (where other card/component styles live):

- `.research-area-card` — fixed height (180px), overflow hidden, border-radius, position relative, background-size cover
- `.research-area-card:hover` — subtle `transform: scale(1.02)` with CSS transition
- `.research-area-overlay` — absolute positioned gradient overlay at bottom, padding
- `.research-area-card h3` — white, semi-bold title
- `.research-area-card p` — white with slight transparency, small font size

### 4. `_pages/research.md`

A new page at `/research/` with:

- Layout: `page`
- Navigation: optionally added to nav
- 6 anchored `<h2 id="anchor">` sections, one per research area
- Placeholder content for each section (user fills in later)

## Files to Modify

### 5. `_layouts/about.liquid`

Insert before the `<!-- News -->` comment block (line 43):

```liquid
<!-- Research Areas -->
{% if page.research_areas and page.research_areas.enabled %}
  <h2>
    <a href="{{ '/research/' | relative_url }}" style="color: inherit">research areas</a>
  </h2>
  {% include research_areas.liquid %}
{% endif %}
```

### 6. `_pages/about.md`

Add to front matter:

```yaml
research_areas:
  enabled: true
```

### 7. No SCSS import needed

Styles are appended to the existing `_sass/_components.scss`, which is already imported via `@use "components"` in `assets/css/main.scss`.

## Visual Design

- **Grid:** 2 rows x 3 columns on desktop, stacks to 1 column on mobile
- **Card style:** Full background image with bottom gradient overlay (transparent to dark)
- **Text:** White title (semi-bold, ~15px) and description (slightly transparent, ~12px) over gradient
- **Hover:** Subtle brightness increase or slight scale (1.02) with CSS transition
- **Card height:** ~180px uniform
- **Gap:** Bootstrap `g-3` spacing (~1rem)
- **Section title:** "research areas" as an `<h2>` link to `/research/`, matching the style of "news" and "selected publications" headings

## Responsive Behavior

- **>=768px (md):** 3 columns
- **<768px:** 1 column, full width cards

## Dependencies

- No new JS required
- No new gems or npm packages
- Uses existing Bootstrap grid and al-folio's `figure.liquid` or direct CSS background-image
- User must provide 6 images at `assets/img/research/`
